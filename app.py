from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
import os

app = Flask(__name__)

# Initialize OpenAI client (your key will be set in Render)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# HTML page (frontend)
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ask the AI</title>
<style>
body { font-family: Arial, sans-serif; background: #f0f0f0; text-align: center; padding: 40px; }
textarea { width: 80%; height: 80px; border-radius: 10px; padding: 10px; font-size: 16px; }
button { padding: 10px 20px; margin-top: 10px; border-radius: 8px; cursor: pointer; background: #007BFF; color: white; border: none; }
button:hover { background: #0056b3; }
#response { margin-top: 20px; font-weight: bold; color: #333; }
</style>
</head>
<body>
<h2>💬 Ask the AI</h2>
<textarea id="question" placeholder="Type your question..."></textarea><br>
<button onclick="askAI()">Ask</button>
<p id="response"></p>

<script>
async function askAI() {
  const question = document.getElementById("question").value;
  document.getElementById("response").innerText = "Thinking...";
  const res = await fetch("/ask", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({question})
  });
  const data = await res.json();
  document.getElementById("response").innerText = data.answer || data.error;
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
            temperature=0.8,
            max_tokens=200
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
            
