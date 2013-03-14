from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    lesson1 = {
        'sounds': [["static/lessons/1/a_chord.ogg", "a"],
                   ["static/lessons/1/d_chord.ogg", "d"],
                   ["static/lessons/1/e_chord.ogg", "e"]],
        'choices': [["A Chord", 'a'],
                    ["D Chord", 'd'],
                    ["E Chord", 'e']],
    }
    return render_template('index.html', lesson=lesson1)

if __name__ == "__main__":
    app.run(debug=True)
