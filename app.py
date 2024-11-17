from flask import Flask, render_template, request, redirect, url_for, session
import time
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

questions = ['nam', 'gam', 'palathuru', 'elaulu', 'saththu', 'mal', 'sindu']
players = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/host', methods=['POST'])
def host():
    host_name = request.form.get('name')
    if host_name:
        session['host'] = host_name
        session['game_id'] = random.randint(1000, 9999)  # Generate a random game ID
        session['players'] = [host_name]  # Initialize player list with the host
        return redirect(url_for('host_game'))
    return redirect(url_for('index'))

@app.route('/host_game')
def host_game():
    game_id = session.get('game_id')
    players = session.get('players')
    return render_template('host.html', game_id=game_id, players=players)

@app.route('/join_game', methods=['POST'])
def join_game():
    player_name = request.form.get('name')
    game_id = int(request.form.get('game_id'))
    
    # Validate if the game exists
    if game_id == session.get('game_id'):
        session['players'].append(player_name)
        session.modified = True
        return redirect(url_for('game', game_id=game_id))
    
    return redirect(url_for('index'))

@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        player = request.form.get('player')
        answer = request.form.get('answer')
        session['answers'][player] = answer
        # All players done answering
        if len(session['answers']) == len(session['players']):
            return redirect(url_for('timer'))
    
    game_id = session.get('game_id')
    players = session.get('players')
    return render_template('game.html', game_id=game_id, players=players, questions=questions)

@app.route('/timer')
def timer():
    time_left = 100
    session['time_left'] = time_left
    return render_template('timer.html', time_left=time_left)

@app.route('/start_timer', methods=['POST'])
def start_timer():
    # Countdown logic
    time_left = session.get('time_left')
    while time_left > 0:
        time_left -= 1
        session['time_left'] = time_left
        # Sleep for 1 second
        time.sleep(1)
    
    return redirect(url_for('results'))

@app.route('/results')
def results():
    return render_template('results.html', players=session['players'], answers=session['answers'])

@app.route('/restart')
def restart():
    session.pop('players', None)
    session.pop('answers', None)
    session.pop('game_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
