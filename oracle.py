import json
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from pathlib import Path

STATE_FILE = Path("oracle_state.json")

DEFAULT_STATE = {
    "status": "starting",
    "current_task": None,
    "worked": [],
    "failed": [],
    "next": [
        "Initialize ORACLE core",
        "Design progress dashboard",
        "Enable self-development loop"
    ],
    "log": [],
    "last_update": None,
}

def load_state():
    if not STATE_FILE.exists():
        save_state(DEFAULT_STATE)
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        save_state(DEFAULT_STATE)
        return DEFAULT_STATE.copy()

def save_state(state):
    state["last_update"] = datetime.utcnow().isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2))

def oracle_loop():
    state = load_state()
    state["status"] = "running"
    save_state(state)

    while True:
        state = load_state()

        if not state["next"]:
            state["status"] = "idle"
            save_state(state)
            time.sleep(2)
            continue

        task = state["next"].pop(0)
        state["current_task"] = task
        state["log"].append(f"Starting: {task}")
        save_state(state)

        time.sleep(2)  # simulate thinking / work

        # simple success/failure simulation
        if "fail" in task.lower():
            state["failed"].append(task)
            state["log"].append(f"Failed: {task}")
        else:
            state["worked"].append(task)
            state["log"].append(f"Completed: {task}")

        # self-planning (autonomous)
        if task == "Design progress dashboard":
            state["next"].append("Implement live HTML dashboard")
        if task == "Implement live HTML dashboard":
            state["next"].append("Improve execution loop")

        state["current_task"] = None
        save_state(state)
        time.sleep(1)

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        state = load_state()

        html = f"""
        <html>
        <head>
            <title>ORACLE – Autonomous Progress</title>
            <meta http-equiv="refresh" content="2">
            <style>
                body {{ font-family: Arial; padding: 20px; }}
                h1 {{ margin-bottom: 5px; }}
                section {{ margin-bottom: 20px; }}
                .ok {{ color: green; }}
                .fail {{ color: red; }}
                .next {{ color: blue; }}
            </style>
        </head>
        <body>
            <h1>🔮 ORACLE – Autonomous System</h1>
            <p><b>Status:</b> {state["status"]}</p>
            <p><b>Last update:</b> {state["last_update"]}</p>

            <section>
                <h2>Current Task</h2>
                <p>{state["current_task"] or "—"}</p>
            </section>

            <section>
                <h2 class="ok">Worked</h2>
                <ul>{"".join(f"<li>{t}</li>" for t in state["worked"])}</ul>
            </section>

            <section>
                <h2 class="fail">Failed</h2>
                <ul>{"".join(f"<li>{t}</li>" for t in state["failed"])}</ul>
            </section>

            <section>
                <h2 class="next">Next</h2>
                <ul>{"".join(f"<li>{t}</li>" for t in state["next"])}</ul>
            </section>

            <section>
                <h2>Log</h2>
                <ul>{"".join(f"<li>{l}</li>" for l in state["log"][-10:])}</ul>
            </section>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

def start_server():
    server = HTTPServer(("localhost", 9000), DashboardHandler)
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=oracle_loop, daemon=True).start()
    print("ORACLE running at http://localhost:9000")
    start_server()
