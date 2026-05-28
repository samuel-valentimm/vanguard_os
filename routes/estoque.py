from flask import Blueprint, render_template, request, redirect, flash
from services.estoque_service import ProdutoService

estoque_bp = Blueprint('estoque', __name__)

@estoque_bp.route('/produtos')
def visualizar_produtos():

    try:
        variacoes = ProdutoService.listar_produtos_estoque()
        return render_template('produtos.html', variacoes=variacoes)
    except Exception as e:
        return f"Erro ao carregar produtos: {e}", 500


@estoque_bp.route('/produtos/salvar', methods=['POST'])
def salvar_produto():

    try:
        dados = request.form.to_dict()
        # Lógica de SKU
        nome = str(dados.get('nome_produto', '')).strip().upper()
        cor = str(dados.get('cor', '')).strip().upper()
        tamanho = str(dados.get('tamanho', '')).strip().upper()
        
        sku_gerado = f"{'-'.join(nome.split())}-{'-'.join(cor.split())}-{tamanho}"
        dados['sku'] = sku_gerado
        dados.pop('nome_produto', None)
        
        ProdutoService.cadastrar_produto_com_grade(dados)
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect('/produtos')
    
    except Exception as e:
        return f"Erro ao salvar: {e}", 500