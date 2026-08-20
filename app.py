import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-3.6-flash")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    message = request.json.get("message", "").strip()

    if not message:
        return jsonify({"reply": "Please enter a cooking question."})

    prompt = f"""You are CookMate, a friendly AI Cooking Helper.
Help with recipes, ingredients, cooking steps, cooking time,
ingredient substitutions, vegetarian/non-vegetarian dishes, and meal ideas.
Give simple, practical and safe cooking guidance.

User: {message}
"""

    try:
        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Sorry, I couldn't process that. Please try again."})

if __name__ == "__main__":
    app.run(debug=True)
