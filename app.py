import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper

app = Flask(__name__)
CORS(app)

print("جاري تحميل نموذج الذكاء الاصطناعي...")
model = whisper.load_model("base")
print("تم تحميل النموذج بنجاح!")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "running", "message": "Video Transcription Server is Live!"})

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "لم يتم العثور على ملف في الطلب"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "لم يتم اختيار ملف"}), 400

    try:
        upload_dir = "/tmp"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        file.save(file_path)

        result = model.transcribe(file_path, language="ar")
        
        segments = []
        for segment in result.get("segments", []):
            segments.append({
                "start": round(segment["start"], 2),
                "end": round(segment["end"], 2),
                "text": segment["text"].strip()
            })

        if os.path.exists(file_path):
            os.remove(file_path)

        return jsonify({
            "success": True,
            "text": result.get("text", ""),
            "segments": segments
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
