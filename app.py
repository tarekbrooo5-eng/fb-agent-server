import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# إعداد مفتاح الذكاء الاصطناعي
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "running", "message": "AI Facebook Agent Server is online!"})

@app.route('/process_comment', methods=['POST'])
def process_comment():
    data = request.get_json() or {}
    comment = data.get('comment', '')
    page_context = data.get('context', 'متجر أو صفحة رسمية')

    if not comment:
        return jsonify({"status": "error", "message": "No comment provided"}), 400

    try:
        # صياغة الرد الذكي الديناميكي عبر الذكاء الاصطناعي
        prompt = f"""
        أنت وكيل خدمة عملاء ذكي ومحترف لصفحة على فيسبوك.
        معلومات الصفحة/النشاط: {page_context}
        تعليق المستخدم الذي تحتاج للرد عليه هو: "{comment}"
        
        قم بصياغة رد ذكي، ودود، وطبيعي تماماً (باللهجة المناسبة أو العربية الفصحى المبسطة)، بحيث يتفاعل مع محتوى تعليقه بدقة ويوجهه بلطف لمتابعة التفاصيل عبر الرسائل الخاصة (الخاص). لا تضع ردوداً معلبة، بل اجعل الرد مخصصاً تماماً لهذا التعليق.
        """
        
        # استخدام نموذج جيميناي لتوليد الرد
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        generated_reply = response.text.strip()

        return jsonify({
            "status": "success",
            "comment": comment,
            "generated_reply": generated_reply
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
