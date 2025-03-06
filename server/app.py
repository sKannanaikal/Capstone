from FLEM import FLEM_FRAMEWORK
from flask import Flask, render_template, request, session, jsonify
from stats import genHistogram, normalizeData
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'blah'

CORS(app)

@app.route("/upload", methods=['POST'])
def loadingPage():
    if request.method == 'POST':
        model = request.form.get('model')
        algorithm = request.form.get('algorithm')
        
        print(f'[+] User Selected {model} {algorithm}')

        if 'fileInput' not in request.files:
            return jsonify({"error": "No file found"}), 400
        
        malwareSample = request.files['fileInput']
        print('malware acquired')
        
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
        response['sortedAttributionIndexes'] = sortedAttributions.tolist()
        response['normalizedAttributions'] = normalizedAttributions.tolist()
        response['assemblyCode'] = malwareCode

        return jsonify(response)


def normalizeAttributions(attributions, sortedAttributions):
    positiveAttributionScores = [attributions[0][sortedAttributions[i]] for i in range(len(sortedAttributions)) if attributions[0][sortedAttributions[i]] > 0]
    negativeAttributionScores = [attributions[0][sortedAttributions[i]] for i in range(len(sortedAttributions)) if attributions[0][sortedAttributions[i]] <= 0]

    positiveNormalized = normalizeData(positiveAttributionScores)
    negativeNormalized = normalizeData(negativeAttributionScores)
    
    return  np.concatenate((positiveNormalized, negativeNormalized)) #TODO multiply by 100 and round to 2 decimal places
    



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
