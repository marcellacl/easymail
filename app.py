import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/api/upload", methods=["POST"])
def upload():
    try:
        file = request.files.get("file")

        if not file:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400

        content = file.read().decode("utf-8", errors="ignore")

        prompt = f"""
        ANALISE O TEXTO E RETORNE APENAS JSON.
        NADA DE TEXTO FORA DO JSON.

        {{
            "classificacao": "produtivo ou improdutivo",
            "resumo": "resumo do texto",
            "resposta_sugerida": "resposta curta"
        }}

        Texto:
        {content}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content
        result_json = json.loads(result)

        return jsonify(result_json)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def index():
    return send_from_directory("templates", "index.html")


@app.route("/static/<path:path>")
def static_files(path):
    return send_from_directory("static", path)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
