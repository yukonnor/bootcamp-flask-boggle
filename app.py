from flask import Flask, request, render_template, redirect, session
from boggle import Boggle

# Flask setup
app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"

# init boggle game and board
boggle_game = Boggle()
board = boggle_game.make_board()
print(board)


@app.route('/')
def index():
    """Show boggle board."""

    # Store board in the session
    session['board'] = board

    return render_template("board.html", board=board)

