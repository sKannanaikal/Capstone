#   from FLEM import FLEM_FRAMEWORK
from flask import Flask, render_template, request, session, jsonify
from stats import genHistogram, normalizeData
import numpy as np

app = Flask(__name__)
app.secret_key = 'blah'

@app.route("/upload", methods=['POST'])
def loadingPage():
    if request.method == 'POST':
        malwareSample = request.files['sample']
        model = request.form.get('model')
        algorithm = request.form.get('algorithm')
        
        filepath = f'./uploads/malware.exe'
        malwareSample.save(filepath)
        
        session['model'] = model
        session['algorithm'] = algorithm
        session['filepath'] = filepath
        
        print(f'[+] User selected {filepath} with model: {model} and algorithm: {algorithm}')

        rankedMaliciousFunctions, sortedAttributions, attributionsNP = FLEM_FRAMEWORK(session['filepath'], session['model'], session['algorithm'])
        sortedAttributionScores = [attributionsNP[0][sortedAttributions[i]] for i in range(len(sortedAttributions))]
        normalizedAttributions = normalizeAttributions(attributionsNP, sortedAttributions)

        with open('./disassembled/malware.asm', 'r') as file:
            malwareCode = file.read()

        response = {}
        response['rankedMaliciousFunctions'] = rankedMaliciousFunctions
        response['sortedAttributionIndexes'] = sortedAttributions
        response['normalizedAttributions'] = normalizedAttributions
        response['assemblyCode'] = malwareCode

        return jsonify(response)

def normalizeAttributions(attributions, sortedAttributions):
    positiveAttributionScores = [attributions[0][sortedAttributions[i]] for i in range(len(sortedAttributions)) if attributions[0][sortedAttributions[i]] > 0]
    negativeAttributionScores = [attributions[0][sortedAttributions[i]] for i in range(len(sortedAttributions)) if attributions[0][sortedAttributions[i]] <= 0]

    positiveNormalized = normalizeData(positiveAttributionScores)
    negativeNormalized = normalizeData(negativeAttributionScores)

    #return positiveNormalized + negativeNormalized
    return  np.concatenate((positiveNormalized, negativeNormalized)) #TODO multiply by 100 and round to 2 decimal places
    



if __name__ == '__main__':
    app.run()
