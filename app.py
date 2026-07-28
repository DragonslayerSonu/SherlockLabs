from flask import Flask, render_template,jsonify
from datetime import datetime
import platform
import socket
import psutil

app = Flask(__name__)
def is_process_running(process_name):
    for process in psutil.process_iter(["name"]):
        if process.info["name"] == process_name:
            return True

    return False

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time

    return render_template(
        "dashboard.html",
        time=datetime.now().strftime("%d %B %Y %H:%M:%S"),
        hostname=socket.gethostname(),
        os_name=platform.system(),
        python_version=platform.python_version(),
        cpu_usage=psutil.cpu_percent(interval=1),
        ram_usage=memory.percent,
        disk_usage=disk.percent,
        uptime=str(uptime).split(".")[0],
    )
@app.route("/api/metrics")
def metrics():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return jsonify({
        "cpu": psutil.cpu_percent(),
        "ram": memory.percent,
        "disk": disk.percent,
        "nginx":is_process_running("nginx")
    })

if __name__ == "__main__":
    app.run(debug=True)
