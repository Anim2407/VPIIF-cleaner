from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/fetch", methods=["POST"])
def fetch():
    return jsonify({
        "clean": "It works!",
        "sha": "dummy123"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
