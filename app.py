from flask import Flask, render_template, request, redirect, jsonify, url_for
import sqlite3
import threading
import time

app = Flask(__name__)

# Global game state
game_state = {
    "questions": ["nam", "gam", "palathuru", "elaulu", "saththu", "mal", "sindu"],
    "answers": {},  # Player answers
    "timer": 100,  # Timer countdown
    "timer_active": False
}

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("game_data.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, name TEXT)''')
    conn.commit()
    conn.close()

init_db()


@app.route("/")
def host_page():
    return render_template("index.html", questions=game_state["questions"])


@app.route("/join")
def join_game():
    return render_template("player.html")


@app.route("/submit_answers", methods=["POST"])
def submit_answers():
    player_name = request.form.get("player_name")
    answers = request.form.getlist("answers[]")
    game_state["answers"][player_name] = answers

    if not game_state["timer_active"]:
        start_timer()
    return jsonify({"status": "success"})


@app.route("/results")
def show_results():
    return render_template("results.html", answers=game_state["answers"])


def start_timer():
    def countdown():
        game_state["timer_active"] = True
        while game_state["timer"] > 0:
            time.sleep(1)
            game_state["timer"] -= 1
        game_state["timer_active"] = False

    threading.Thread(target=countdown).start()


@app.route("/reset_game")
def reset_game():
    game_state["answers"] = {}
    game_state["timer"] = 100
    game_state["timer_active"] = False
    return redirect(url_for("host_page"))


if __name__ == "__main__":
    app.run(debug=True)
