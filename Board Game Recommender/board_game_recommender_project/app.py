from flask import Flask, request, render_template, redirect, url_for, session
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)
app.secret_key = 'game' 

@app.route('/')
@app.route('/about')
def about():
    return render_template("about.html", active_page='about')

@app.route('/projects')
def projects():
    return render_template("projects.html", active_page='projects')

@app.route('/resume')
def resume():
    return render_template("resume.html", active_page='resume')

@app.route('/capstone', methods = ['GET', 'POST'])
def capstone():

    if 'inputted_list' not in session:
        session['inputted_list'] = []

    if request.method == 'POST':
        game1 = request.form.get('checked_1')
        if game1:
            session['inputted_list'].append(game1)
            session.modified = True

        game2 = request.form.get('checked_2')
        if game2:
            session['inputted_list'].append(game2)
            session.modified = True

        game3 = request.form.get('checked_3')
        if game3:
            session['inputted_list'].append(game3)
            session.modified = True

        input = request.form.get('input')
        if input:
            session['inputted_list'].append(input)
            session.modified = True

        session['inputted_list'] = list(set(session['inputted_list']))
        return redirect(url_for('capstone'))
    
    recommendation_list = []
    error_message = ""
    return render_template("capstone.html", active_page='capstone', inputted_list=session['inputted_list'], recommendation_list=recommendation_list, error_message=error_message)

@app.route('/recommend', methods = ['GET', 'POST'])
def post_recommendations():

    return

def recommend_games_from_list():
    return

@app.route('/clear', methods = ['POST'])
def clear_page():
    session['inputted_list'] = []
    recommendation_list = []
    error_message = ""
    return render_template('capstone.html', active_page='capstone', recommendation_list=recommendation_list, error_message=error_message)

# if __name__ == '__main__':
#     app.debug = True
#     app.run(host="localhost", port=5000, debug=True)