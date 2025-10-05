from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import joblib

application = Flask(__name__)

@application.route('/')
@application.route('/about')
def about():

    return render_template("about.html")



if __name__ == '__main__':
    application.debug = True
    application.run(host="localhost", port=5000, debug=True)