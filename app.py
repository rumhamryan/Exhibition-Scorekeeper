from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import time 
# Assuming scrimage_scorekeeper.py is correctly set up and accessible
from scrimage_scorekeeper import EightballGame, NineballGame, PlayerStats

app = Flask(__name__)
CORS(app)

def load_player_names():
    with open("player_data.json", "r") as file:
        player_data = json.load(file)
    return list(player_data.keys())  # Assuming the top-level keys are player names


@app.route('/')
def home():
    player_names = load_player_names()
    return render_template('index.html', players=player_names)

@app.route('/game/start', methods=['POST'])
def start_game():
    player1_name = request.form.get('player1')
    player2_name = request.form.get('player2')
    # Initialize game with selected players
    global current_game
    current_game = EightballGame(player1_name, player2_name)
    return jsonify({'message': f'Game started between {player1_name} and {player2_name}'})

@app.route('/game/action', methods=['POST'])
def game_action():
    action = request.form.get('action')
    # Handle different actions
    if action == 'pocket_ball':
        ball_number = int(request.form.get('ball_number'))
        current_game.ball_pocketed(ball_number)
    elif action == 'defensive_shot':
        current_game.defensive_shot()
    elif action == 'switch_turn':
        current_game.shooter_turn_over()
    # Add more actions as needed
    return jsonify({'message': 'Action processed'})

@app.route('/game/stats', methods=['GET'])
def game_stats():
    # Return current game stats
    stats = current_game.get_stats()  # Implement this method in your game class
    return jsonify(stats)

@app.route('/player/create', methods=['POST'])
def create_player():
    # Adjusted to handle form data
    data = request.form.to_dict()  # Convert ImmutableMultiDict to dict
    player = PlayerStats(**data)
    player.create_json_file_player_entry()
    return jsonify({'message': f"Player profile created for {player.player_name}"}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
