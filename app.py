from flask import Flask, render_template, request, redirect, url_for
from database import ClienteService

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/clientes")
def clientes():
    dados_clientes = ClienteService.listar_clientes()
    total_clientes = len(dados_clientes)
    return render_template("clientes.html", dados_clientes=dados_clientes, total_clientes=total_clientes)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    nome = request.form.get("nome")
    telefone = request.form.get("telefone")

    ClienteService.adicionar_cliente(nome, telefone)
    # Após adicionar, volta para a tela de clientes
    return redirect(url_for("clientes"))

@app.route("/deletar/<int:id_cliente>")
def deletar(id_cliente):
    ClienteService.deletar_cliente(id_cliente)
    # Após deletar, volta para a tela de clientes
    return redirect(url_for("clientes"))

if __name__ == "__main__":
    app.run(debug=True)