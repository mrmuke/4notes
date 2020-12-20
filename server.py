from flask import Flask, render_template, send_file
import os
from predict import generate_music
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')
@app.route('/upload')
def upload():
   return render_template('upload.html')
@app.route('/generateMusic')
def downloadFile():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    filename=generate_music()
    print(filename)
    path = "C:/users/mxing/Coding_Projects/Composer/" +filename
    return send_file(path, as_attachment=True)

@app.route('/generateMusic')
def downloadFile():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    filename=generate_music()
    print(filename)
    path = "C:/users/mxing/Coding_Projects/Composer/" +filename
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
   app.run(debug=True)