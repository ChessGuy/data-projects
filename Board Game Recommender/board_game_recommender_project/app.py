from flask import Flask, request, render_template, redirect, url_for, session
import pandas as pd
import numpy as np

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

        game4 = request.form.get('checked_4')
        if game4:
            session['inputted_list'].append(game4)
            session.modified = True

        game5 = request.form.get('checked_5')
        if game5:
            session['inputted_list'].append(game5)
            session.modified = True

        input = request.form.get('input')
        if input:
            session['inputted_list'].append(input)
            session.modified = True

        session['inputted_list'] = list(set(session['inputted_list']))
        return redirect(url_for('capstone'))
    
    recommendation_list = []
    error_message = ""
    filter_values = ''
    return render_template("capstone.html", active_page='capstone', inputted_list=session['inputted_list'], recommendation_list=recommendation_list, error_message=error_message, filter_values=filter_values)

@app.route('/recommend', methods = ['GET', 'POST'])
def post_recommendations():
    if request.method == "POST":
        min_age = request.form.get('age')
        if min_age:
            min_age = float(min_age)
   
        max_play_time = request.form.get('play_time')
        if max_play_time:
            max_play_time = float(max_play_time)

        min_player_count = request.form.get('player_count')
        if min_player_count:
            min_player_count = float(min_player_count)

        max_complex_rating = request.form.get('complexity')
        if max_complex_rating:
            max_complex_rating = float(max_complex_rating)

        filter_values = f'Min Age: {min_age}, Max Player Count: {max_play_time}, Minimum Player Count: {min_player_count}, Maximum Complexity Rating: {max_complex_rating}'

        [recommendation_list, error_message] = recommend_games_from_game_list(session['inputted_list'], min_age=min_age, max_play_time=max_play_time, min_player_count=min_player_count, max_complex_rating=max_complex_rating)

        return render_template("capstone.html", active_page='capstone', inputted_list=session['inputted_list'], recommendation_list=recommendation_list, error_message=error_message, filter_values=filter_values)

def recommend_games_from_game_list(board_game_list, min_age=None, max_play_time=None, min_player_count=None, max_complex_rating=None):
    cluster_dict = {}
    error_message = ''

    # Load the Dataframe to search
    search_df = pd.read_csv('data/board_game_search.csv')

    # Remove duplicate entries
    board_game_list = list(set(board_game_list))
    
    # Blank input
    if len(board_game_list) == 0:
        error_message = 'No input received'
        return [[], error_message]
    
    # Single input
    elif len(board_game_list) == 1:
        if board_game_list[0].lower() in search_df['Name'].tolist():
            target_cluster = search_df[search_df['Name'] == board_game_list[0].lower()]['Cluster'].iloc[0]
            resulting_games = search_df[search_df['Cluster'] == target_cluster].sort_values(by='Custom Rating', ascending=False)
        else: 
            error_message = f'{board_game_list[0]} not found'
            return [[], error_message]
    
    # Multiple input
    else:
        for game in board_game_list:
            
            if game.lower() in search_df['Name'].tolist():
                # Select the cluster with the board game in it.  If it belongs to more than one cluster, select the first one.  
                current_cluster = search_df[search_df['Name'] == game.lower()]['Cluster'].iloc[0]
                
                # Add cluster to dictionary to keep track of how many times it appears
                if current_cluster in cluster_dict:
                    cluster_dict[current_cluster] += 1
                else:
                    cluster_dict[current_cluster] = 1
            
            # Game not found
            else:
                error_message = error_message + f'{game} not found.  '  
        
        if len(cluster_dict) == 0:
            error_message = error_message + 'No recommendations found based on search parameters'
            return [[], error_message]
        
        else:
            # Loop through clusters that appear the most often to make recommendations
            max_cluster_count = max(cluster_dict.values())
            max_clusters = [key for key, value in cluster_dict.items() if value == max_cluster_count]

            resulting_games = pd.DataFrame()

            for cluster in max_clusters:
                current_games_from_cluster = search_df[search_df['Cluster'] == cluster]
                resulting_games = pd.concat([resulting_games, current_games_from_cluster])

            resulting_games = resulting_games.sort_values(by='Custom Rating', ascending=False)     
        
    # Filtering results
    if min_age:
         resulting_games = resulting_games[resulting_games['Min Age'] <= min_age]
            
    if max_play_time:
         resulting_games = resulting_games[resulting_games['Play Time'] <= max_play_time]
            
    if min_player_count:
        resulting_games = resulting_games[resulting_games['Max Players'] >= min_player_count]
            
    if max_complex_rating:
        resulting_games = resulting_games[resulting_games['Complexity Average'] <= max_complex_rating]
    
    # Printing results
    if len(resulting_games[~resulting_games['Name'].isin([item.lower() for item in board_game_list])]) == 0:
        error_message = 'No recommendations found based on search parameters'
        return [[], error_message]
    
    else:
        final_recs = resulting_games[~resulting_games['Name'].isin([item.lower() for item in board_game_list])]['Name'].head(20).str.title().str.replace("'S", "'s").to_list()
        return [final_recs, error_message]
    
@app.route('/clear', methods = ['POST'])
def clear_page():
    session['inputted_list'] = []
    recommendation_list = []
    error_message = ""
    return render_template('capstone.html', active_page='capstone', recommendation_list=recommendation_list, error_message=error_message)

# if __name__ == '__main__':
#     app.debug = True
#     app.run(host="localhost", port=5000, debug=True)