from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    filename = secure_filename(file.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    prompt = f"""
    Analise o texto a seguir e responda somente JSON válido com os seguintes campos:

    {{
        "classificacao": "produtivo" ou "improdutivo",
        "resposta_sugerida": "texto curto e profissional",
        "resumo": "uma frase resumindo o email"
    }}

    Texto:
    {text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    result_raw = print("===== RESPOSTA DA IA =====")
                            print(result_raw)
                print("==========================")


    try:
        result_json = json.loads(result_raw)
    except:
        result_json = {
            "erro": "A IA retornou algo inesperado.",
            "raw": result_raw
        }

    return jsonify({
        "conteudo": text,
        "ia": result_json
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


