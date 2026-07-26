from flask import Flask, render_template
from datetime import datetime
import platform
import socket
import psutil

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return render_template(
        "dashboard.html",
        time=datetime.now().strftime("%d %B %Y %H:%M:%S"),
        hostname=socket.gethostname(),
        os_name=platform.system(),
        python_version=platform.python_version(),
        cpu_usage=psutil.cpu_percent(interval=1),
        ram_usage=memory.percent,
        disk_usage=disk.percent
    )


if __name__ == "__main__":
    app.run(debug=True)
