import sqlite3  # Biblioteca para interagir com o banco de dados SQLite
from flask import Flask, request, jsonify  # Importamos Flask para criar a API e request/jsonify para manipular requisições e respostas

# Criamos a aplicação Flask
# O Flask precisa saber qual é o arquivo principal do programa, então passamos "__name__" como referência
app = Flask(__name__)

# Criamos uma rota para o endpoint "/femandaopix"
# Quando acessarmos http://127.0.0.1:5000/femandaopix, essa função será chamada automaticamente
@app.route("/femandaopix")
def manda_o_pix():
    # Quando o usuário acessar essa rota no navegador, ele verá essa mensagem HTML na tela
    return "<h2>SE TEM DOR DE CUTUVELO, TÁ DEVENDO</h2>"

# Função para inicializar o banco de dados SQLite
# Ela cria o banco de dados caso ele ainda não exista

def init_db():
    # Abrimos uma conexão com o banco de dados "database.db"
    # O comando "with" garante que a conexão será fechada automaticamente após a execução
    with sqlite3.connect("database.db") as conn:
        # Criamos uma tabela chamada "LIVROS", caso ela ainda não exista
        conn.execute(
            """
                CREATE TABLE IF NOT EXISTS LIVROS(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,  # Cada livro recebe um ID único automaticamente
                    titulo TEXT NOT NULL,  # O título do livro, obrigatório
                    categoria TEXT NOT NULL,  # A categoria do livro, como Ficção ou História, obrigatório
                    autor TEXT NOT NULL,  # Nome do autor do livro, obrigatório
                    image_url TEXT NOT NULL  # Link para a imagem da capa do livro, obrigatório
                )
            """
        )  # Esse comando SQL cria a tabela "LIVROS" caso ela ainda não exista

# Chamamos a função para garantir que o banco de dados esteja pronto antes de rodar a aplicação
init_db()

# Criamos uma rota que recebe dados de um novo livro e os armazena no banco de dados
@app.route("/doar", methods=["POST"])
def doar():
    # Capturamos os dados enviados pelo usuário na requisição HTTP
    # Eles devem estar no formato JSON
    dados = request.get_json()
    print(f" AQUI ESTÃO OS DADOS RETORNADOS DO CLIENTE {dados}")  # Exibe os dados no terminal para conferência

    # Extraímos as informações do JSON recebido
    titulo = dados.get("titulo")  # Obtém o título do livro
    categoria = dados.get("categoria")  # Obtém a categoria do livro
    autor = dados.get("autor")  # Obtém o nome do autor do livro
    image_url = dados.get("image_url")  # Obtém a URL da imagem do livro

    # Verificamos se todos os campos obrigatórios foram preenchidos
    # Se algum campo estiver vazio, retornamos um erro 400 (Bad Request)
    if not titulo or not categoria or not autor or not image_url:
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400  
    
    # Conectamos ao banco de dados SQLite
    # O comando "with" garante que a conexão será fechada corretamente após a execução do bloco
    with sqlite3.connect("database.db") as conn:
        # Inserimos os dados do novo livro na tabela "LIVROS"
        conn.execute(f"""
        INSERT INTO LIVROS (titulo, categoria, autor, imagem_url) 
        VALUES ("{titulo}", "{categoria}", "{autor}", "{image_url}")
        """)
    
    conn.commit()  # Confirma a inserção dos dados no banco de dados

    # Retornamos uma mensagem confirmando que o livro foi cadastrado com sucesso
    # `jsonify()` transforma um dicionário Python em JSON válido para a resposta HTTP
    # O código HTTP 201 indica que um novo recurso foi criado com sucesso
    return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201

# Aqui verificamos se o script está sendo executado diretamente e não importado como módulo
if __name__ == "__main__":
    # Inicia o servidor Flask no modo de depuração
    # O modo debug permite que qualquer alteração no código seja aplicada automaticamente sem precisar reiniciar o servidor
    app.run(debug=True)
