from flask import Flask, render_template

from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():

    current_time = datetime.now().strftime("%d %B %Y   %H:%M:%S")

    return render_template(
        "dashboard.html",
        time=current_time
    )


if __name__ == "__main__":
    app.run(debug=True)
