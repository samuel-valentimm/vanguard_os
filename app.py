from flask import Flask, flash, render_template, request, redirect, url_for
from database import ClienteService, ProdutoService
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


# ---- INTERFACE PRINCIPAL (DASHBOARD) ----
@app.route("/")
def index():
    return render_template("index.html")


# ---- MÓDULO DE CLIENTES ----
@app.route("/clientes", methods=['GET', 'POST'])
def clientes():
    if request.method == 'POST':
        nome = request.form.get('nome').upper().strip()
        telefone = request.form.get('telefone')
        ClienteService.adicionar_cliente({"nome": nome, "telefone": telefone})
        return redirect('/clientes')
    
    dados_clientes = ClienteService.listar_clientes()
    return render_template("clientes.html", clientes=dados_clientes)


@app.route("/clientes/excluir/<int:id_cliente>")
def deletar(id_cliente):
    ClienteService.deletar_cliente(id_cliente)
    return redirect(url_for("clientes"))


@app.route("/cliente/<int:cliente_id>")
def ficha_cliente(cliente_id):
    cliente = ClienteService.buscar_cliente_por_id(cliente_id)
    resumo = ClienteService.obter_resumo_cliente(cliente_id)
    return render_template("ficha_cliente.html", cliente=cliente, resumo=resumo)


@app.route("/cliente/baixa/<int:cliente_id>", methods=["POST"])
def dar_baixa(cliente_id):
    try:
        ClienteService.processar_pagamento(cliente_id)
        flash("Pagamento registrado com sucesso!", "success")

    except Exception as e:
        flash(f"Erro: {str(e)}", "error")
        
    return redirect(url_for('ficha_cliente', cliente_id=cliente_id))


# ---- MÓDULO DE ESTOQUE / PRODUTOS ----
@app.route('/produtos')
def visualizar_produtos():
    try: 
        produtos_estoque = ProdutoService.listar_produtos_estoque()
        return render_template('produtos.html', variacoes=produtos_estoque)
    except Exception as e:
        return f"Erro ao carregar a pagina de produtos: {e}", 500


@app.route('/produtos/salvar', methods=['POST'])
def salvar_produto():
    try:
        nome = request.form.get('nome_produto', '')
        cor = request.form.get('cor', '')
        tamanho = request.form.get('tamanho', '')

        nome_str = str(nome).strip().upper()
        cor_str = str(cor).strip().upper()
        tamanho_str = str(tamanho).strip().upper()

        nome_fmt = "-".join(nome_str.split())
        cor_fmt = "-".join(cor_str.split())
        sku_gerado = f"{nome_fmt}-{cor_fmt}-{tamanho_str}"

        dados_salvar = request.form.to_dict()
        dados_salvar['sku'] = sku_gerado
        dados_salvar.pop('nome_produto', None)

        ProdutoService.cadastrar_produto_com_grade(dados_salvar)
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect('/produtos')
    except Exception as e:
        return f"Erro ao salvar: {e}", 500


# ---- MODULO DE CONDICIONAIS ----
@app.route('/condicionais', methods=['GET', 'POST'])
def condicionais():
    if request.method == 'POST':
        nome_cliente = request.form.get('cliente_nome', '').upper().strip()
        sku = request.form.get('sku_produto', '').upper().strip()
        preco = request.form.get('preco_venda')
        quantidade = int(request.form.get('quantidade', 1))

        cliente_id = ClienteService.buscar_id_por_nome(nome_cliente)

        if cliente_id:
            try:
                ClienteService.adicionar_condicional({
                    "cliente_id": cliente_id,
                    "sku": sku,
                    "preco_venda": preco,
                    "quantidade": quantidade
                })
                flash('Item adicionado à condicional com sucesso!', 'success')
            except Exception as e:
                flash(str(e), 'error')
        else:
            flash('Erro: Cliente não encontrado.', 'error')
            
        return redirect('/condicionais')
    
    return render_template("condicionais.html", 
                           condicionais=ClienteService.listar_condicionais(), 
                           clientes=ClienteService.listar_clientes(), 
                           produtos=ProdutoService.listar_produtos_estoque())


@app.route("/condicionais/devolver/<int:id_item>/<sku>/<int:quantidade>")
@app.route("/condicionais/devolver/<int:id_item>/<sku>") # Rota de fallback

def devolver_condicional(id_item, sku, quantidade=1):
    ClienteService.processar_devolucao(id_item, sku, quantidade)
    flash('Item devolvido ao estoque com sucesso!', 'success')
    return redirect(url_for("condicionais"))


@app.route("/condicionais/vender/<int:id_item>")
def vender_condicional(id_item):
    """Apenas remove da condicional"""

    ClienteService.processar_venda(id_item)
    flash('Venda da condicional registrada com sucesso!', 'success')
    return redirect(url_for("condicionais"))

if __name__ == "__main__":
    app.run(debug=True)