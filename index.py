from flask import Flask, request, jsonify
import google.generativeai as genai

# ============================
# CONFIG: Google Gemini API KEY
# ============================
GEMINI_KEY = "AIzaSyDuYJW1O3o95gC58nzAlh8320OBIbxlxDw"   # your free key

genai.configure(api_key=GEMINI_KEY)

# Main AI model
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)


# ============================
# HOME TEST (GET)
# ============================
@app.route("/")
def home():
    return "🔥 FREE Gemini Robot Brain Active on Laptop 🔥"


# ============================
# 1) TEXT FROM ESP32  (POST)
# ============================
@app.route("/from_esp_text", methods=["POST"])
def from_esp_text():

    try:
        data = request.get_json(force=True) or {}
        user_text = (data.get("text") or "").strip()

        if not user_text:
            return jsonify({"error": "No text received"}), 400

        print(f"[ESP32 TEXT] {user_text}")

        # ----- Gemini AI Answer -----
        reply = model.generate_content(
            f"You are Dip's cute Bangla robot. "
            f"Answer VERY SHORT, friendly, emotional. User said: {user_text}"
        )

        ai_answer = reply.text.strip()

        # ----- Emotion Logic -----
        lt = user_text.lower()
        emotion = "neutral"

        if any(w in lt for w in ["hello", "hi", "hii", "valo", "bhalo", "khushi"]):
            emotion = "happy"
        elif any(w in lt for w in ["sad", "dukho", "mon kharap", "bad"]):
            emotion = "sad"
        elif any(w in lt for w in ["angry", "rag", "gussa", "boka"]):
            emotion = "angry"

        # ----- Servo -----
        servo = {
            "happy": 20,
            "sad": 80,
            "angry": 60,
            "neutral": 45,
        }.get(emotion, 45)

        # ----- Final JSON -----
        return jsonify({
            "reply_text": ai_answer,
            "emotion": emotion,
            "servo": servo
        })

    except Exception as e:
        print("🔥 ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ============================
# 2) PLACEHOLDER AUDIO
# ============================
@app.route("/from_esp_audio", methods=["POST"])
def from_esp_audio():
    return jsonify({
        "text_reply": "Audio received. Voice system later add korbo.",
        "audio_reply": None
    })


# ============================
# 3) PLACEHOLDER IMAGE
# ============================
@app.route("/from_esp_image", methods=["POST"])
def from_esp_image():
    return jsonify({"vision": "Image received. Vision AI later add korbo."})


# ============================
# RUN SERVER
# ============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
