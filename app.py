import sqlite3  # Importamos o módulo sqlite3 para manipulação do banco de dados SQLite
from flask import Flask, request  # Importamos a classe Flask e o objeto request do módulo flask para criar nossa API

# Aqui estamos criando uma instância do Flask e armazenando na variável "app"
# O parâmetro __name__ é passado para o Flask para que ele consiga identificar o arquivo principal da aplicação
app = Flask(__name__)

# Criamos uma rota para o endpoint "/pagar"
# Quando acessarmos http://127.0.0.0.1:5000/pagar no navegador, a função abaixo será executada
@app.route("/pagar")
def exibir_mensagem():
    # Retorna um texto formatado em HTML para ser exibido na página da rota "/pagar"
    return "<h1>Pagar as pessoas, faz bem as pessoas!!!</h1>"

# Criamos outra rota para o endpoint "/femandaopix"
# Quando acessarmos http://127.0.0.0.1:5000/femandaopix, a função será chamada automaticamente
@app.route("/femandaopix")
def manda_o_pix():
    # Retorna um texto formatado em HTML que será exibido no navegador
    return "<h2>SE TEM DOR DE CUTUVELO, TÁ DEVENDO</h2>"

# Criamos uma terceira rota para o endpoint "/comida"
# Sempre que o usuário acessar http://127.0.0.0.1:5000/comida, essa função será executada
@app.route("/comida")
def comida():
    # Retorna um texto formatado em HTML com uma mensagem sobre comida
    return "<h2>Tomato à milanesa</h2>"

# Função para inicializar o banco de dados SQLite
# Criamos uma conexão com o banco de dados chamado 'database.db'
# Se o banco de dados ainda não existir, ele será criado automaticamente

def init_db():
    # Conectamos ao banco de dados SQLite e usamos "with" para garantir que a conexão seja fechada corretamente após a execução
    with sqlite3.connect("database.db") as conn:
        # Executamos um comando SQL para criar a tabela LIVROS, caso ela ainda não exista
        conn.execute(
            """
                CREATE TABLE IF NOT EXISTS LIVROS(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,  # Identificador único para cada livro, gerado automaticamente
                    titulo TEXT NOT NULL,  # O título do livro, armazenado como texto e obrigatório
                    categoria TEXT NOT NULL,  # A categoria do livro (exemplo: ficção, tecnologia), armazenada como texto e obrigatória
                    autor TEXT NOT NULL,  # O nome do autor do livro, armazenado como texto e obrigatório
                    imagem_url TEXT NOT NULL  # O URL da imagem da capa do livro, armazenado como texto e obrigatório
                )
            """
        )  # A execução desse comando cria a tabela caso ela ainda não exista, garantindo que nossa estrutura de banco esteja configurada

# Chamamos a função para inicializar o banco de dados quando o programa for executado
init_db()

# Criamos uma rota para o endpoint "/doar" que aceita requisições do tipo POST
# Essa rota será utilizada para receber dados de um livro e armazená-los no banco de dados
@app.route("/doar", methods=["POST"])
def doar():
    # Capturamos os dados enviados na requisição em formato JSON
    dados = request.get_json()
    
    # Extraímos as informações do JSON recebido
    titulo = dados.get("titulo")  # Obtém o título do livro
    categoria = dados.get("categoria")  # Obtém a categoria do livro
    autor = dados.get("autor")  # Obtém o nome do autor do livro
    imagem_url = dados.get("imagem_url")  # Obtém a URL da imagem do livro

# Aqui verificamos se o script está sendo executado diretamente e não importado como módulo
if __name__ == "__main__":
    # Inicia o servidor Flask no modo de depuração
    # O modo debug faz com que as mudanças no código sejam aplicadas automaticamente, sem necessidade de reiniciar o servidor manualmente
    app.run(debug=True)
