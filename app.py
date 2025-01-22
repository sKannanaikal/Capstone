from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html")

'''
TODO General Pipeline
(done) 1. User fills out form selects (malware sample to upload, explanation model, maybe XAI algorithm)
2. then program will take and dissassemble uploads section malware sample and generate dissassembly file in dissassembled folder
(done) 3. with the dissassembled file the function mapping is going to be generated as a dictionary
4. then with the function mapping an interpretation will be done based on the users requested algorithms and a feature importance score ranked list for each function is given
5. the user is then redirected somewhere else where they will be able to see the results (ranked list, document, IDK)

Beauty standards
- maybe a loading screeen or bar like pizza hut or something so the users know whats going on
- introduce file upload security checks and all
- be mindful of vulnerabilities, etc. and patch them
'''

@app.route("/upload", methods=['POST'])
def analyzeSample():
    if request.method == 'POST':
        malwareSample = request.files['sample']
        model = request.form.get('model')
        algorithm = request.form.get('algorithm')
        filepath = f'./uploads/{malwareSample.filename}'
        malwareSample.save(filepath)
    return 'Success'
   
@app.route("/results")
def displayResults():
    return 'Results Page'

if __name__ == '__main__':
    app.run()