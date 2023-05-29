from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/events')
def events():
    return render_template("events.html")

@app.route('/howtoplay')
def howtoplay():
    return render_template("howtoplay.html")

@app.route('/regions')
def regions():
    return render_template("regions.html")

if __name__ == "__main__":
    app.run(debug=True)