from FLEM import FLEM_FRAMEWORK
from flask import Flask, render_template, request, session
from stats import genPieChart

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
    
    return render_template('loading.html')
   
@app.route("/results")
def displayResults():  
    rankedMaliciousFunctions, sortedAttributions, attributionsNP = FLEM_FRAMEWORK(session['filepath'], session['model'], session['algorithm'])
    genPieChart(attributionsNP[0])
    return render_template('results.html', rankedMaliciousFunctions=rankedMaliciousFunctions, sortedAttributions=sortedAttributions, attributionsNP=attributionsNP)

if __name__ == '__main__':
    app.run()
