from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dados "mockados"
conversations = {
    1: {"name": "Análise de CX", "messages": [{"role": "agent", "text": "Olá, como posso ajudar?"}, {"role": "user", "text": "aeee"}]},
    2: {"name": "NPS 1sem24", "messages": [{"role": "agent", "text": "Oi, em que posso ser útil?"}]}
}
chat_counter = 3

# Rota principal
@app.route('/', methods=['GET'])
def index():
    chat_id = request.args.get('chat_id', default=None, type=int)
    chat = None
    if chat_id and chat_id in conversations:
        chat = conversations[chat_id]
    return render_template('index.html', conversations=conversations, chat=chat, chat_id=chat_id)

# Rota para enviar mensagem
@app.route('/send_message', methods=['POST'])
def send_message():
    chat_id = int(request.form['chat_id'])
    message = request.form['message']
    if chat_id not in conversations:
        return redirect(url_for('index'))
    # Adiciona mensagem do usuário
    conversations[chat_id]['messages'].append({"role": "user", "text": message})
    # Adiciona mensagem do agente (mock)
    conversations[chat_id]['messages'].append({"role": "agent", "text": "Esta é uma resposta automática."})
    return redirect(url_for('index', chat_id=chat_id))

# Rota para criar novo chat enviando mensagem
@app.route('/create_chat', methods=['POST'])
def create_chat():
    global chat_counter
    message = request.form['message']
    # Cria novo chat com a mensagem inicial
    conversations[chat_counter] = {
        "name": f"Chat {chat_counter}",
        "messages": [{"role": "user", "text": message}]
    }
    # Adiciona resposta do agente (mock)
    conversations[chat_counter]['messages'].append({"role": "agent", "text": "Bem-vindo ao novo chat!"})
    chat_counter += 1
    return redirect(url_for('index', chat_id=chat_counter - 1))

# Rota para criar novo chat (via sidebar)
@app.route('/new_chat', methods=['POST'])
def new_chat():
    global chat_counter
    chat_name = request.form['chat_name']
    conversations[chat_counter] = {"name": chat_name, "messages": []}
    chat_counter += 1
    return redirect(url_for('index', chat_id=chat_counter - 1))

if __name__ == '__main__':
    app.run(debug=True)
