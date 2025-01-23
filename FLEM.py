import os
import torch
from torch import nn, Tensor
import torch.nn.functional as F
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torchvision
import torchvision.transforms as transforms
import pandas as pd
from torch.nn.utils.rnn import pad_sequence
import lief
import pe_sections
import numpy as np
from captum.attr import KernelShap
from captum.attr import Lime
from captum.attr import LayerConductance
from captum.attr import NeuronConductance

GLOBAL_GPU = ''

class MalConvConfig:
    """
    Configuration used by original authors:

        >>> MalConvConfig(
                vocab_size=257,
                embedding_size=8,
                channels=128,
                stride=500,
                kernel_size=500,
                mlp_hidden_size=128,
                pad_token_id=0,
            )
    """

    def __init__(
        self,
        vocab_size: int = 264,
        embedding_size: int = 256,
        channels: int = 128,
        stride: int = 512,
        kernel_size: int = 512,
        mlp_hidden_size: int = 128,
        pad_token_id: int = 0,
        num_labels: int = -1,
    ) -> None:
        self.vocab_size = vocab_size
        self.embedding_size = embedding_size
        self.channels = channels
        self.stride = stride
        self.kernel_size = kernel_size
        self.mlp_hidden_size = mlp_hidden_size
        self.pad_token_id = pad_token_id
        self.num_labels = num_labels


class MalConv(nn.Module):

    def __init__(self, config: MalConvConfig):
        super().__init__()
        self.config = config

        self.embed = nn.Embedding(
            config.vocab_size,
            config.embedding_size,
            padding_idx=config.pad_token_id,
        )
        
        self.conv_1 = nn.Conv1d(
            in_channels=config.embedding_size,
            out_channels=config.channels,
            kernel_size=config.kernel_size,
            stride=config.stride,
        )
        self.conv_2 = nn.Conv1d(
            in_channels=config.embedding_size,
            out_channels=config.channels,
            kernel_size=config.kernel_size,
            stride=config.stride,
        )
        self.pooling = nn.AdaptiveMaxPool1d(1)

    def forward(self, input_ids: Tensor) -> Tensor:

        # B: batch size
        # L: sequence length
        # E: embedding size
        # C: channels
        # S: stride

        B = input_ids.shape[0]
        L = input_ids.shape[1]
        E = self.config.embedding_size
        C = self.config.channels
        S = math.floor((L - self.config.kernel_size) / self.config.stride + 1)

        input_ids: Tensor                                                 # [B, L]
        assert tuple(input_ids.shape) == (B, L), f"{input_ids.shape} != {(B, L)}"

        input_embeddings: Tensor = self.embed(input_ids).transpose(1, 2)  # [B, E, L]
        assert tuple(input_embeddings.shape) == (B, E, L), f"{input_embeddings.shape} != {(B, E, L)}"

        cnn_1_value: Tensor = self.conv_1(input_embeddings)               # [B, C, S]
        assert tuple(cnn_1_value.shape) == (B, C, S), f"{cnn_1_value.shape} != {(B, C, S)}"

        cnn_2_value: Tensor = self.conv_2(input_embeddings)               # [B, C, S]
        assert tuple(cnn_2_value.shape) == (B, C, S), f"{cnn_2_value.shape} != {(B, C, S)}"

        gating_value: Tensor = cnn_1_value * F.sigmoid(cnn_2_value)       # [B, C, S]
        assert tuple(gating_value.shape) == (B, C, S), f"{gating_value.shape} != {(B, C, S)}"

        pooled_value: Tensor = self.pooling(gating_value)                 # [B, C, 1]
        assert tuple(pooled_value.shape) == (B, C, 1), f"{pooled_value.shape} != {(B, C, 1)}"

        hidden_states: Tensor = pooled_value.squeeze(-1)                  # [B, C]
        assert tuple(hidden_states.shape) == (B, C), f"{hidden_states.shape} != {(B, C)}"

        return hidden_states


class MalConvForSequenceClassification(nn.Module):

    def __init__(self, config: MalConvConfig):
        super().__init__()
        self.malconv = MalConv(config)
        self.clf_head = nn.Sequential(
            nn.Linear(config.channels, config.mlp_hidden_size),
            nn.ReLU(),
            nn.Linear(config.mlp_hidden_size, config.num_labels),
        )

    def forward(self, input_ids: Tensor) -> Tensor:
        hidden_states = self.malconv.forward(input_ids)
        logits = self.clf_head.forward(hidden_states)
        return logits

def dissassembleMalwareSample(file):
    command = '~/ghidra_11.2.1_PUBLIC/support/analyzeHeadless ~/FLEMAPP/ testProject -import ~/Capstone/uploads/malware.exe -analysisTimeoutPerFile 60 -loader PeLoader -processor x86:LE:32:default -scriptpath ~/ghidra_11.2.1_PUBLIC/ghidra_scripts/ -postscript Disassembler.java ~/Capstone/disassembled 60 30'
    os.system(command)

def generateFunctionMapping(file):
    fileMap = {}
    
    with open(f'../dissassembled/malware.asm', 'r') as dissassembly:
        code = dissassembly.read()

    functions = code.split('\n\n')
    addressesPattern = r"(?<=\s)[A-Fa-f0-9]{8}(?=\s)"
    functionNamePattern = r"\b[_a-zA-Z][a-zA-Z0-9_@<>=]*(?=\s*\()"
    
    for function in functions:
        addresses = re.findall(addressesPattern, function)
        if len(addresses) >= 2:
            startingAddress = addresses[0]
            endingAddress = addresses[-2]
            start = int(startingAddress, 16)
            end = int(endingAddress, 16)
        else:
            continue
        
        match = re.search(functionNamePattern, function)
        
        if match is not None:
            functionName = match.group()
            fileMap[functionName] = (startingAddress, endingAddress)
        else:
            continue
    
    return fileMap

def rankMaliciousFunctions(attributions, functionMapping):
    maliciousFunctions = []

    attributionsNP = attributions.detach().numpy()
    meanAttributions = np.mean(np.abs(attributionsNP), axis=0)
    sortedAttributions = np.argsort(meanAttributions)[::-1]
    
    for i in range(5):
        maliciousFunctionIndex = sortedAttributions[i]
        functionName = list(functionMapping.keys())[maliciousFunctionIndex]
        maliciousFunctions.append(functionName)
    
    return maliciousFunctions

def extractFunctionsFromBinary(file, functionMapping):
    binaryFunctionBytes = b''
    totalBytesExtracted = 0
    functionCount = 0
    
    fileSize = os.path.getsize(filepath)
    
    with open(filepath, 'rb') as binaryFile:
        for function in functionMapping:
            try:
                startingAddress = int(functionMapping[function][0], 16)
                endingAddress = int(functionMapping[function][1], 16)
            except TypeError:
                print('[-] Type Error Occurred')
                return None
            
            inclusivelength = endingAddress - startingAddress
            
            if inclusivelength == 0:
                continue
            
            if inclusivelength < 0:
                print(f'[-] length error non negative value for {filepath} {function} {inclusivelength}')
                return None
            
            totalBytesExtracted += inclusivelength
            
            binaryFile.seek(startingAddress)
            if binaryFile.tell() > fileSize:
                print(f'[-] seek address outside of bounds of file {startingAddress}')
                return None
            
            functionBytes = bytearray(binaryFile.read(inclusivelength))
            binaryFunctionBytes += functionBytes
            functionCount += 1
        
        if functionCount <= 5:
            print(f'[-] Function Count Less than 5: {filepath} {functionCount} functions')
            return None
        
    vectorizedBinary = torch.frombuffer(binaryFunctionBytes, dtype=torch.uint8)
    vectorizedBinary = vectorizedBinary.to(torch.int64)
    
    return vectorizedBinary

def generateFeatureMask(vectorizedBinary, functionMapping):
    featureMask = torch.zeros_like(vectorizedBinary)
    currentStartOffset = 0
    functionCount = 0
    totalBytesFeatured = 0
    
    for function in functionMapping:
        startingAddress = int(functionMapping[function][0], 16)
        endingAddress = int(functionMapping[function][1], 16)
        length = endingAddress - startingAddress
        
        for byteOffset in range(currentStartOffset, currentStartOffset + length):
            featureMask[0, byteOffset] = functionCount
            totalBytesFeatured += 1
        functionCount += 1
        currentStartOffset = currentStartOffset + length
    
    return featureMask

def interpretation(vectorizedBinary, model, functionMapping, interpreteter):
    try:
        vectorizedBinary = vectorizedBinary.to(GLOBAL_GPU)
        
        if vectorizedBinary.dim() == 1:
            vectorizedBinary = vectorizedBinary.unsqueeze(0)
        with torch.no_grad():
            logits = flem(vectorizedBinary)
        
        probabilities = torch.softmax(logits, dim=-1)
        predictions = torch.argmax(probabilities, dim=-1)
        
        if(predictions == 0): #make sure this is malware?
            print('\t Model predicted correctly')
        
        featureMask = generateFeatureMask(vectorizedBinary,  functionMapping)
        featureMask = featureMask.to(GLOBAL_GPU)
        
        attributions = interpreteter.attribute(vectorizedBinary, target=0, feature_mask=featureMask, return_input_shape=False)
    
    except (ValueError, IndexError, torch.OutOfMemoryError):
        return None, None
    
    return attributions

def FLEM_FRAMEWORK(file, model_name, algorithm_name):
    global GLOBAL_GPU
    
    dissassembleMalwareSample(file)

    functionMapping = generateFunctionMapping(file)

    vectorizedBinary = extractFunctionsFromBinary(file, functionMapping)

    warnings.filterwarnings("ignore")
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    GLOBAL_GPU = device
    
    configuration = MalConvConfig(num_labels=2, pad_token_id=257)
    flem = MalConvForSequenceClassification(configuration)
    flem.load_state_dict(torch.load(f'./models/{model_name}', weights_only=True))#TODO double check this lien after the entire file structure is finalized
    flem.eval()
    flem.to(GLOBAL_GPU)

    if algorithm_name == 'LIME':
        interpreteter = Lime(flem)
    elif algorithm_name == 'SHAP':
        interpreteter = KernelShap(flem)
    
    attributions = interpretation(vectorizedBinary, model, functionMapping, interpreteter)

    maliciousFunctions = rankMaliciousFunctions(attributions, functionMapping)

    systemCleanup()

    return maliciousFunctions

def systemCleanup():
    pass