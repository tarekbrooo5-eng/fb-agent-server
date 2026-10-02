import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "running", "message": "Server is live and ready!"})

@app.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # هنا يتم استقبال الملف بنجاح وجاهز لمعالجته
        # يمكنك إضافة منطق التفريغ الصوتي هنا لاحقاً

        return jsonify({
            "success": True,
            "message": "File received successfully",
            "segments": [
                {"start": 0.0, "end": 3.5, "text": "تجربة ناجح للتفريغ الصوتي"}
            ]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
