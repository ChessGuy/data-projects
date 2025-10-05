from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)

@app.route('/')
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/projects')
def projects():
    return render_template("projects.html")

@app.route('/resume')
def resume():
    return render_template("resume.html")

@app.route('/capstone')
def capstone():
    return render_template("capstone.html")

# if __name__ == '__main__':
#     app.debug = True
#     app.run(host="localhost", port=5000, debug=True)