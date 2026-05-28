from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.financeiro_service import FinanceiroService
from services.cliente_service import ClienteService
from services.estoque_service import ProdutoService

financeiro_bp = Blueprint('financeiro', __name__)


@financeiro_bp.route('/condicionais', methods=['GET', 'POST'])
def condicionais():

    if request.method == 'POST':

        try:
            nome_cliente = request.form.get('cliente_nome', '').upper().strip()
            cliente_id = ClienteService.buscar_id_por_nome(nome_cliente)
            
            if not cliente_id:
                flash('Erro: Cliente não encontrado.', 'error')
                return redirect(url_for('financeiro.condicionais'))
                
            FinanceiroService.adicionar_condicional({
                "cliente_id": cliente_id,
                "sku": request.form.get('sku_produto'),
                "preco_venda": request.form.get('preco_venda'),
                "quantidade": int(request.form.get('quantidade', 1))
            })

            flash('Item adicionado à condicional!', 'success')

        except Exception as e:
            flash(str(e), 'error')

        return redirect(url_for('financeiro.condicionais'))
    
    return render_template("condicionais.html", 
                           condicionais=FinanceiroService.listar_condicionais(),
                           clientes=ClienteService.listar_clientes(),
                           produtos=ProdutoService.listar_produtos_estoque())


@financeiro_bp.route("/condicionais/devolver/<int:id_item>/<sku>/<int:quantidade>")
def devolver(id_item, sku, quantidade):

    FinanceiroService.processar_devolucao(id_item, sku, quantidade)
    flash('Item devolvido ao estoque!', 'success')
    return redirect(url_for("financeiro.condicionais"))

@financeiro_bp.route("/condicionais/vender/<int:id_item>")
def vender(id_item):
    
    FinanceiroService.processar_venda(id_item)
    flash('Venda registrada!', 'success')
    return redirect(url_for("financeiro.condicionais"))