# Importamos a biblioteca SQLite3 para trabalhar com o banco de dados SQLite
import sqlite3  

# Importamos a biblioteca Flask para criar a API
# "request" permite capturar os dados enviados pelo cliente
# "jsonify" é usado para transformar os dados em formato JSON para resposta
from flask import Flask, request, jsonify  
from flask_cors import CORS
# Criamos a aplicação Flask
# "__name__" indica que este é o arquivo principal do nosso programa
app = Flask(__name__)
CORS(app)

# 🔹 Criamos uma rota no Flask chamada "/femandaopix"
# Quando alguém acessar http://127.0.0.1:5000/femandaopix, essa função será executada automaticamente
@app.route("/femandaopix")
def manda_o_pix():
    # O servidor retorna uma mensagem HTML quando essa rota for acessada no navegador
    return "<h2>SE TEM DOR DE CUTUVELO, TÁ DEVENDO</h2>"

# 🔹 Criamos uma função para inicializar o banco de dados SQLite
# Essa função será chamada quando o sistema for iniciado para garantir que a tabela existe
def init_db():
    # Abrimos uma conexão com o banco de dados SQLite (ou criamos um novo arquivo "database.db" se não existir)
    with sqlite3.connect("database.db") as conn:  
        # Executamos um comando SQL para criar a tabela LIVROS caso ela ainda não exista
        conn.execute(
            """
                CREATE TABLE IF NOT EXISTS LIVROS(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID do livro, gerado automaticamente
                    titulo TEXT NOT NULL,  -- Nome do livro (obrigatório)
                    categoria TEXT NOT NULL,  -- Categoria do livro (ex: Ficção, Programação) (obrigatório)
                    autor TEXT NOT NULL,  -- Nome do autor do livro (obrigatório)
                    image_url TEXT NOT NULL  -- URL da imagem da capa do livro (obrigatório)
                )
            """
        )  # O comando acima cria a tabela apenas se ela ainda não existir

# ----------------------------------------------------------------------------------------------------------------
# ESTRUTURA PARA DEIXAR VALORES SALVOS NO BANCO DE DADOS

# Executa uma consulta SQL para contar quantos livros existem na tabela "livros"
# Depois, usa fetchone()[0] para pegar apenas o número da contagem
    quantidade = conn.execute("SELECT COUNT(*) FROM livros").fetchone()[0]

# Se não existir nenhum livro cadastrado (ou seja, quantidade == 0)
    if quantidade == 0:
    
    # Cria uma lista de livros padrão, cada livro é uma tupla com:
    # (título, categoria, autor, link da imagem)
        livros_padrao = [
            ("O Hobbit", "Fantasia", "J.R.R. Tolkien", "https://m.media-amazon.com/images/I/91M9xPIf10L.jpg"),
            ("1984", "Ficção Científica", "George Orwell", "https://m.media-amazon.com/images/I/819js3EQwbL._AC_UF1000,1000_QL80_.jpg"),
            ("Dom Casmurro", "Romance", "Machado de Assis", "https://m.media-amazon.com/images/I/61Z2bMhGicL.jpg"),
        ]

    # Percorre cada livro da lista de livros padrão
        for livro in livros_padrao:
        # Separa os dados de cada livro em variáveis individuais
            titulo, categoria, autor, image_url = livro
        
        # Insere o livro no banco de dados, preenchendo os campos da tabela
            conn.execute(f'''
                INSERT INTO livros (titulo, categoria, autor, image_url)
                VALUES ("{titulo}", "{categoria}", "{autor}", "{image_url}")
            ''')
        
        # Salva (confirma) a inserção do livro no banco de dados
        conn.commit()
 
# -------------------------------------------------------------------------------------------------------------------

# Chamamos a função init_db() para garantir que o banco de dados seja criado antes do uso
init_db()

# 🔹 Criamos uma rota para cadastrar um novo livro no banco de dados
# Esse endpoint será acessado através de uma requisição HTTP do tipo "POST"
@app.route("/doar", methods=["POST"])
def doar():
    # Capturamos os dados que foram enviados pelo cliente no formato JSON
    dados = request.get_json()

    # Extraímos os valores do JSON recebido
    titulo = dados.get("titulo")  # Pegamos o título do livro
    categoria = dados.get("categoria")  # Pegamos a categoria
    autor = dados.get("autor")  # Pegamos o nome do autor
    image_url = dados.get("image_url")  # Pegamos a URL da imagem do livro

    # Verificamos se algum dos campos obrigatórios está vazio
    if not titulo or not categoria or not autor or not image_url:
        # Retornamos um erro 400 (Bad Request) caso algum campo não tenha sido preenchido
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    # Abrimos a conexão com o banco de dados para salvar os dados do livro
    with sqlite3.connect("database.db") as conn:
        # Executamos o comando SQL para inserir os dados na tabela LIVROS
        conn.execute(f"""
        INSERT INTO LIVROS (titulo, categoria, autor, image_url)
        VALUES ("{titulo}", "{categoria}", "{autor}", "{image_url}")
        """)

        # Salvamos as mudanças no banco de dados
        conn.commit()

        # Retornamos uma mensagem de sucesso com status 201 (Created)
        return jsonify({"Mensagem": "Livro cadastrado com sucesso!"}), 201

# 🔹 Criamos um endpoint para listar todos os livros cadastrados no banco de dados
# Esse endpoint será acessado através de uma requisição HTTP do tipo "GET"
@app.route("/livros", methods=["GET"])
def listar_livros():
    # Abrimos a conexão com o banco de dados
    with sqlite3.connect("database.db") as conn:
        # Executamos um comando SQL para buscar todos os livros na tabela LIVROS
        livros = conn.execute("SELECT * FROM LIVROS").fetchall()

        # Criamos uma lista vazia para armazenar os livros em formato de dicionário
        livros_formatados = []

        # Percorremos cada item da lista retornada do banco de dados
        for item in livros:
            # Criamos um dicionário representando um livro com os campos corretos
            dicionario_livros = {
                "id": item[0],  # Pegamos o ID do livro
                "titulo": item[1],  # Pegamos o título do livro
                "categoria": item[2],  # Pegamos a categoria do livro
                "autor": item[3],  # Pegamos o nome do autor
                "image_url": item[4]  # Pegamos a URL da imagem do livro
            }
            # Adicionamos esse dicionário à lista de livros formatados
            livros_formatados.append(dicionario_livros)

    # Retornamos a lista de livros no formato JSON com o código de status 200 (OK)
    return jsonify(livros_formatados), 200

# 🔹 Verificamos se este arquivo está sendo executado diretamente
# Isso evita que o Flask rode o servidor caso o script seja importado em outro programa
if __name__ == "__main__":
    # Iniciamos o servidor Flask no modo debug
    # O modo debug ajuda a identificar erros e recarrega automaticamente o código sempre que há mudanças
    app.run(debug=True)
