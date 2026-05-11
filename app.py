from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
import monitor

app = Flask(__name__)
app.config["SECRET_KEY"] = "calputwiz-dev-key"
socketio = SocketIO(app, async_mode="threading", cors_allowed_origins="*")

monitor.init(socketio)

_tz = pytz.timezone("America/Sao_Paulo")
scheduler = BackgroundScheduler(timezone=_tz)
scheduler.add_job(
    monitor.run_scan,
    CronTrigger(day_of_week="mon-fri", hour="10-17", minute="*/5", timezone=_tz),
    id="market_scan",
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scan")
def manual_scan():
    """Dispara uma varredura manual (útil fora do pregão para testes)."""
    socketio.start_background_task(monitor.run_scan)
    return jsonify({"status": "varredura iniciada"})


if __name__ == "__main__":
    scheduler.start()
    print("=" * 50)
    print("  CalputWiz — Monitor de Opções B3")
    print("  http://localhost:5001")
    print("  GET /scan  →  varredura manual")
    print("=" * 50)
    socketio.run(app, host="0.0.0.0", port=5001, debug=False, use_reloader=False, allow_unsafe_werkzeug=True)
