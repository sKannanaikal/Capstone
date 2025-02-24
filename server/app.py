#from FLEM import FLEM_FRAMEWORK
from flask import Flask, render_template, request, session
from stats import genHistogram, normalizeData
import numpy as np

app = Flask(__name__)
app.secret_key = 'blah'


@app.route("/")
def homepage():
    return render_template("index.html")

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
    
    return {'Message': 'Received Files'}
   
@app.route("/results")
def displayResults():  
    #TODO update this to send json to the frontend
    #Maybe run the FLEM framework for multiple iterations and then take the average highest ranked stuff
    rankedMaliciousFunctions, sortedAttributions, attributionsNP = FLEM_FRAMEWORK(session['filepath'], session['model'], session['algorithm'])
    sortedAttributionScores = [attributionsNP[0][sortedAttributions[i]] for i in range(len(sortedAttributions))]
    genHistogram(sortedAttributionScores)
    normalizedAttributions = normalizeAttributions(attributionsNP, sortedAttributions)

    with open('./disassembled/malware.asm', 'r') as file:
        malware_code = file.read()

    return render_template('results.html', 
                            rankedMaliciousFunctions=rankedMaliciousFunctions, 
                            sortedAttributions=sortedAttributions, 
                            normalizedAttributions=normalizedAttributions, 
                            malware_code=malware_code)

def normalizeAttributions(attributions, sortedAttributions):
    positiveAttributionScores = [attributions[0][sortedAttributions[i]] for i in range(len(sortedAttributions)) if attributions[0][sortedAttributions[i]] > 0]
    negativeAttributionScores = [attributions[0][sortedAttributions[i]] for i in range(len(sortedAttributions)) if attributions[0][sortedAttributions[i]] <= 0]

    positiveNormalized = normalizeData(positiveAttributionScores)
    negativeNormalized = normalizeData(negativeAttributionScores)

    #return positiveNormalized + negativeNormalized
    return  np.concatenate((positiveNormalized, negativeNormalized)) #TODO multiply by 100 and round to 2 decimal places

if __name__ == '__main__':
    app.run()
