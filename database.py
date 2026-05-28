import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class ClienteService:
    @classmethod
    def listar_clientes(cls):
        resposta = supabase.table("clientes").select("*").execute()
        return resposta.data if resposta.data else []


    @classmethod
    def adicionar_cliente(cls, dados):
        dados['nome'] = dados['nome'].upper().strip()
        supabase.table('clientes').insert(dados).execute()


    @staticmethod
    def formatar_dados(cliente):
        tel = str(cliente.get('telefone', ''))
        if len(tel) == 11:
            cliente['telefone'] = f"({tel[0:2]}) {tel[2:7]}-{tel[7:11]}"
        return cliente


    @classmethod
    def deletar_cliente(cls, id_cliente):
        supabase.table('clientes').delete().eq('id', id_cliente).execute()


    @classmethod
    def buscar_id_por_nome(cls, nome_cliente):
        nome_limpo = str(nome_cliente).strip()
        resposta = supabase.table('clientes').select('id').ilike('nome', nome_limpo).maybe_single().execute()
        return resposta.data['id'] if resposta and resposta.data else None


    @classmethod
    def adicionar_condicional(cls, dados):

        dados['sku'] = dados['sku'].upper().strip()
        quantidade_solicitada = int(dados['quantidade'])

        produto = supabase.table("estoque_variacoes") \
            .select("quantidade, preco_venda") \
            .eq("sku", dados['sku']) \
            .single() \
            .execute().data

        if not produto:
            raise Exception("Produto não encontrado.")

        if produto['quantidade'] < quantidade_solicitada:
            raise Exception(f"Estoque insuficiente! Disponível: {produto['quantidade']}")

        preco_unitario = float(dados.get('preco_venda', produto.get('preco_venda', 0)))
        dados['valor_total'] = preco_unitario * quantidade_solicitada

        supabase.table("condicionais").insert(dados).execute()

        nova_qtd = produto['quantidade'] - quantidade_solicitada
        supabase.table("estoque_variacoes") \
            .update({"quantidade": nova_qtd}) \
            .eq("sku", dados['sku']) \
            .execute()


    @classmethod
    def listar_condicionais(cls):
        resposta = supabase.table("condicionais").select("*, clientes(nome)").execute()
        condicionais = resposta.data if resposta.data else []

        for c in condicionais:
            c['cliente_nome'] = c['clientes']['nome'] if c.get('clientes') else 'DESCONHECIDO'
        return condicionais


    @classmethod
    def processar_devolucao(cls, id_item, sku, quantidade):
        supabase.table("condicionais").delete().eq("id", id_item).execute()
        produto = supabase.table("estoque_variacoes").select("quantidade").eq("sku", sku).single().execute().data
        if produto:
            nova_qtd = produto['quantidade'] + int(quantidade)
            supabase.table("estoque_variacoes").update({"quantidade": nova_qtd}).eq("sku", sku).execute()


    @classmethod
    def processar_venda(cls, id_item):
        supabase.table("condicionais").delete().eq("id", id_item).execute()


    @staticmethod
    def buscar_debito_cliente(cliente_id):
        """Essa funcao sera chamada pela rota que soma todos os valores do cliente"""

        response = supabase.table("condicionais")\
            .select("valor_total.sum()")\
            .eq("cliente_id", cliente_id)\
            .execute()
        
        return response.data[0]['sum'] or 0


    @staticmethod
    def obter_resumo_cliente(cliente_id):
        condicionais = supabase.table("condicionais")\
            .select("*")\
            .eq("cliente_id", cliente_id)\
            .execute().data
      
        total_devido = sum(float(item.get('valor_total', 0)) for item in condicionais)
        total_pecas = sum(int(item.get('quantidade', 0)) for item in condicionais)     
        return {
            "itens": condicionais,
            "total_devido": total_devido,
            "total_pecas": total_pecas
        }

    @staticmethod
    def dar_baixa_pagamento(cliente_id, valor_pago):
        pass

    # No ClienteService
    @staticmethod
    def processar_pagamento_total(cliente_id):
        """
        Remove os itens da condicional (baixa) e 
        poderia salvar em uma tabela de 'historico_vendas'
        """

        itens = supabase.table("condicionais").select("*").eq("cliente_id", cliente_id).execute().data
        if itens:
            supabase.table("condicionais").delete().eq("cliente_id", cliente_id).execute()
        return True
        
    @staticmethod
    def processar_pagamento(cliente_id):
        supabase.table("condicionais").delete().eq("cliente_id", cliente_id).execute()
        return True
    
    
    @staticmethod
    def buscar_cliente_por_id(cliente_id):
        response = supabase.table("clientes").select("*").eq("id", cliente_id).single().execute()
        return response.data


class ProdutoService:

    @classmethod
    def cadastrar_produto_com_grade(cls, dados):
        nome_produto = str(dados.get("nome_produto", "PRODUTO")).upper().strip()
        cor_produto = str(dados.get("cor", "UNICA")).upper().strip()
        tamanho = str(dados.get("tamanho", "U")).upper().strip()
        produto_existente = supabase.table("produtos").select("id").eq("nome", nome_produto).execute()

        if produto_existente.data:
            produto_id = produto_existente.data[0]["id"]
        else:
            novo_produto = {"nome": nome_produto, "categoria": "GERAL"}
            resultado = supabase.table("produtos").insert(novo_produto).execute()
            produto_id = resultado.data[0]["id"]

        variacao = {
            "sku": dados.get("sku"),
            "produto_id": produto_id,
            "cor": cor_produto,
            "tamanho": tamanho,
            "preco_custo": float(dados.get("preco_custo", 0)),
            "preco_venda": float(dados.get("preco_venda", 0)),
            "quantidade": int(dados.get("quantidade", 0))
        }
        supabase.table("estoque_variacoes").insert(variacao).execute()
        return produto_id

    @classmethod
    def listar_produtos_estoque(cls):
        resultado = supabase.table("estoque_variacoes").select("*, produtos(nome, categoria)").execute()
        return resultado.data