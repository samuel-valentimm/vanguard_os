from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.cliente_service import ClienteService

clientes_bp = Blueprint('clientes', __name__)


@clientes_bp.route("/clientes", methods=['GET', 'POST'])
def clientes():

    if request.method == 'POST':
        nome = request.form.get('nome').upper().strip()
        telefone = request.form.get('telefone')

        ClienteService.adicionar_cliente({"nome": nome, "telefone": telefone})
        return redirect(url_for('clientes.clientes'))
    
    dados_clientes = ClienteService.listar_clientes()
    return render_template("clientes/clientes.html", clientes=dados_clientes)


@clientes_bp.route("/clientes/excluir/<int:id_cliente>")
def deletar(id_cliente):

    ClienteService.deletar_cliente(id_cliente)
    return redirect(url_for("clientes.clientes"))


@clientes_bp.route("/cliente/<int:cliente_id>")
def ficha_cliente(cliente_id):

    cliente = ClienteService.buscar_cliente_por_id(cliente_id)
    from services.financeiro_service import FinanceiroService
    resumo = FinanceiroService.obter_resumo_cliente(cliente_id)

    return render_template("clientes/ficha_cliente.html", cliente=cliente, resumo=resumo)


@clientes_bp.route("/cliente/baixa/<int:cliente_id>", methods=["POST"])
def dar_baixa(cliente_id):

    from services.financeiro_service import FinanceiroService
    
    try:
        FinanceiroService.processar_pagamento(cliente_id)
        flash("Pagamento registrado com sucesso!", "success")
    except Exception as e:
        flash(f"Erro: {str(e)}", "error")

    return redirect(url_for('clientes.ficha_cliente', cliente_id=cliente_id))