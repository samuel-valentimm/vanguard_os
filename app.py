from flask import Flask, render_template, request, redirect, url_for
from database import ClienteService, ProdutoService

app = Flask(__name__)

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

        # Cadastra o cliente enviando o dicionário para o serviço do Supabase
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
        # IMPORTANTE: Mudamos de 'estoque=' para 'variacoes=' para conversar com o HTML novo
        return render_template('produtos.html', variacoes=produtos_estoque)
    
    except Exception as e:
        return f"Erro ao carregar a pagina de produtos: {e}", 500
    

@app.route('/produtos/salvar', methods=['POST'])
def salvar_produto():
    """Rota que recebe os dados do formulário HTML e salva no banco"""
    try:
        dados_formulario = request.form.to_dict()
        ProdutoService.cadastrar_produto_com_grade(dados_formulario)
        return redirect('/produtos')
    
    except Exception as e:
        return f"Erro ao salvar o produto no estoque: {e}", 500
    

if __name__ == "__main__":
    app.run(debug=True)