from flask import Flask, request, render_template, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

# Flask setup
app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
debug = DebugToolbarExtension(app)

# init boggle game and board
boggle_game = Boggle()
board = boggle_game.make_board()
print(board)


@app.route('/')
def index():
    """Show boggle board and word guess form."""

    # Store board in the session
    session['board'] = board

    return render_template("board.html", board=board)

@app.route('/check-word')
def check_word():
    """Check if word is valid"""

    # guess guess from query string
    word_guess = request.args["word-guess"]

    # check guess: "ok", "not-on-board", "not-word"
    result = boggle_game.check_valid_word(board, word_guess)

    # return result in a JSON payload
    payload = {"result": result}
    return jsonify(payload)

@app.route('/update-stats', methods=["POST"])
def update_stats():
    """Update stats (sent from client) after the game is complete."""

    # receive score from the client
    score = request.json.get('score')

    # get the high score and count times played from the session (or set if doesn't exist)
    if session.get('high_score'):
        session['high_score'] = score if (score > session['high_score']) else session['high_score']
        session['times_played'] += 1
    else:
        session['high_score'] = score
        session['times_played'] = 1

    # return result in a JSON payload
    payload = {'high_score': session['high_score'], 'times_played': session['times_played'] }
    return jsonify(payload)

@app.route('/stats',)
def get_stats():
    """Provide stats (stored in session) to client when requested"""

    # Set the high score and count times played if they don't exist in the session
    if not session.get('high_score'):
        session['high_score'] = 0
        session['times_played'] = 0

    # return result in a JSON payload
    payload = {'high_score': session['high_score'], 'times_played': session['times_played'] }
    return jsonify(payload)
    

