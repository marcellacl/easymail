# EasyMail – Guia para Rodar o Projeto

1. Clonar o repositório
git clone https://github.com/marcellacl/easymail.git
cd easymail

2. Instalar dependências
pip install -r requirements.txt

3. Editar o arquivo .env.example
Edite o arquivo chamado `.env.example` na raíz do projeto para `.env`:
OPENAI_API_KEY=SUA_CHAVE_AQUI

4. Rodar a aplicação
python app.py

Acesse:
http://127.0.0.1:5000/

## 6. Como usar
- Você pode enviar um arquivo (.txt, .pdf, .docx)
- OU colar o texto diretamente no campo
A IA retorna:
- classificação (produtivo ou improdutivo)
- resumo
- resposta sugerida