from flask import Flask, render_template, request, redirect, url_for
from database import ClienteService

app = Flask(__name__)

# 1. ROTA DA TELA INICIAL (Agora abre o painel de boas-vindas)
@app.route("/")
def index():
    return render_template("index.html")

# 2. ROTA DE CLIENTES (Abre a tela bonitona de gerenciamento)
@app.route("/clientes")
def clientes():
    dados_clientes = ClienteService.listar_clientes()
    total_clientes = len(dados_clientes)
    return render_template("clientes.html", dados_clientes=dados_clientes, total_clientes=total_clientes)

# 3. ROTA PARA ADICIONAR CLIENTE
@app.route("/adicionar", methods=["POST"])
def adicionar():
    nome = request.form.get("nome")
    telefone = request.form.get("telefone")

    ClienteService.adicionar_cliente(nome, telefone)
    # Após adicionar, volta para a tela de clientes
    return redirect(url_for("clientes"))

# 4. ROTA PARA DELETAR CLIENTE
@app.route("/deletar/<int:id_cliente>")
def deletar(id_cliente):
    ClienteService.deletar_cliente(id_cliente)
    # Após deletar, volta para a tela de clientes
    return redirect(url_for("clientes"))

if __name__ == "__main__":
    app.run(debug=True)