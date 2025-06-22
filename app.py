from flask import Flask, request, jsonify
import requests, re, hashlib
from bs4 import BeautifulSoup, Comment

app = Flask(__name__)

def clean_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "lxml")
    for tag in soup(["script","style","nav","header","footer","noscript"]):
        tag.decompose()
    for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()
    parts=[]
    for t in soup.find_all(["h1","h2","h3","h4","li"]):
        txt = re.sub(r"\s+"," ", t.get_text(" ", strip=True))
        if txt: parts.append(txt)
    return "\n".join(parts)

@app.route("/fetch", methods=["POST"])
def fetch():
    url = request.json.get("url")
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    clean = clean_html(resp.text)
    checksum = hashlib.sha256(clean.encode()).hexdigest()
    return jsonify({"clean": clean, "sha": checksum})

if __name__ == "__main__":
    app.run(port=8080)
