from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/upload", methods=['POST'])
def analyzeSample():
    if request.method == 'POST':
        malwareSample = request.files['sample']
        filepath = f'./uploads/{malwareSample.filename}'
        malwareSample.save(filepath)
        print('[+] Malware Sample Uploaded and Saved')
    #TODO some rendering of stuff but uploading functionality complete

if __name__ == '__main__':
    app.run()