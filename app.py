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
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')


        ClienteService.adicionar_cliente({"nome": nome, "telefone": telefone})
        return redirect('/clientes')
    
    dados_clientes = ClienteService.listar_clientes()
    return render_template("clientes.html", clientes=dados_clientes)


@app.route("/clientes/excluir/<int:id_cliente>")
def deletar(id_cliente):
    """Rota ajustada para bater com o link 'Excluir' do novo clientes.html"""
    ClienteService.deletar_cliente(id_cliente)
    return redirect(url_for("clientes"))


# ---- MÓDULO DE ESTOQUE / PRODUTOS ----
@app.route('/produtos')
def visualizar_produtos():
    """Rota para exibir a página de cadastro e a grade de variações do estoque"""
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
        print(f" ERRO DETALHADO: {e}")
        return f"Erro ao salvar: {e}", 500


# ---- MODULO DE CONDICIONAIS ----
@app.route('/condicionais', methods = ['GET', 'POST'])
def condicionais():
    if request.method == 'POST':

        nome_cliente = request.form.get('cliente_nome')
        sku = request.form.get('sku_produto')
        preco = request.form.get('preco_venda')

        cliente_id = ClienteService.buscar_id_por_nome(nome_cliente)
        
        ClienteService.adicionar_condicional({
            "cliente_id": cliente_id,
            "sku": sku,
            "preco_venda": preco
        })
        return redirect('/condicionais')
    
    dados_condicional = ClienteService.listar_condicionais()
    return render_template("condicionais.html", condicionais = dados_condicional)


if __name__ == "__main__":
    app.run(debug=True)