def dissassembleMalwareSample(file):
    pass

def generateFunctionMapping(file):
    fileMap = {}
    
    #TODO generate dissassembled file as malware.asm in dissassembled
    #TODO cleanup folder structure (uploads and dissassembled afterwards)
    
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

def rankMaliciousFunctions():
    pass