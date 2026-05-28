from flask import Blueprint, render_template, request, redirect, flash
from services.estoque_service import ProdutoService
from database import supabase

estoque_bp = Blueprint('estoque', __name__)

@estoque_bp.route('/produtos')
def visualizar_produtos():
    try:
        variacoes = ProdutoService.listar_produtos_estoque()
        return render_template('estoque/produtos.html', variacoes=variacoes)
    except Exception as e:
        return f"Erro ao carregar produtos: {e}", 500


@estoque_bp.route('/produtos/salvar', methods=['POST'])
def salvar_produto():

    try:
        dados = request.form.to_dict()
        nome = str(dados.get('nome_produto', '')).strip().upper()
        cor = str(dados.get('cor', '')).strip().upper()
        tamanho = str(dados.get('tamanho', '')).strip().upper()
        sku_gerado = f"{'-'.join(nome.split())}-{'-'.join(cor.split())}-{tamanho}"
        dados['sku'] = sku_gerado
        
        if not dados.get('produto_id'):
            dados['produto_id'] = None 
        
        dados.pop('nome_produto', None)
        
        ProdutoService.cadastrar_produto_com_grade(dados)
        flash('Produto cadastrado com sucesso!', 'success')
        
        return redirect('/produtos') 
    
    except Exception as e:
        return f"Erro ao salvar: {e}", 500
    

@estoque_bp.route('/produtos/deletar/<int:id_variacao>', methods=['POST'])
def deletar_produto(id_variacao):

    try:
        ProdutoService.deletar_variacao(id_variacao)
        flash('Item removido do estoque!', 'success')
        return redirect('/produtos')
    
    except Exception as e:
        return f"Erro ao deletar: {e}", 500
    

@estoque_bp.route('/produtos/editar/<int:id_produto>', methods=['POST'])
def editar_produto(id_produto):

    try:
        novo_nome = request.form.get('nome_produto')
        
        if not novo_nome:
            flash('Erro: Nome vazio', 'error')
            return redirect('/produtos')

        supabase.table("produtos").update({"nome": novo_nome.upper().strip()}).eq("id", id_produto).execute()
        
        flash('Nome do modelo atualizado com sucesso!', 'success')
        return redirect('/produtos')
    
    except Exception as e:
        return f"Erro ao editar: {e}", 500