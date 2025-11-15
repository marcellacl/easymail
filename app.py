import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/api/upload", methods=["POST"])
def upload():
    try:
        file = request.files.get("file")

        if not file:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400

        content = file.read().decode("utf-8")
        prompt = f"Analise o conteúdo do seguinte arquivo:\n\n{content}"

        # CHAMADA CORRETA PARA API NOVA
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result_raw = response.choices[0].message["content"]

        return jsonify({
            "success": True,
            "analysis": result_raw
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "API running!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
