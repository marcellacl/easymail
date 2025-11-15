import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/upload", methods=["POST"])
def upload():
    try:
        file = request.files.get("file")

        if not file:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400

        content = file.read().decode("utf-8")
        prompt = f"""
        Você é um assistente que analisa textos.
        Leia o conteúdo abaixo e retorne obrigatoriamente em JSON no formato:

        {{
            "ia": {{
                "classificacao": "",
                "resumo": "",
                "resposta_sugerida": ""
            }}
        }}

        Texto analisado:
        {content}
        """

        # API nova
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        raw = response.choices[0].message["content"]

        # Tenta transformar a resposta da IA em JSON
        import json
        try:
            parsed = json.loads(raw)
        except:
            # Se a IA não retornar JSON válido, ainda retornamos o texto bruto
            parsed = {"ia": {
                "classificacao": "Erro ao interpretar resposta.",
                "resumo": "-",
                "resposta_sugerida": "-"
            }}

        return jsonify(parsed)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
