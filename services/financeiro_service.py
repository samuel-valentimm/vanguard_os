from database import supabase

class FinanceiroService:

    @staticmethod
    def obter_resumo_cliente(cliente_id):
        condicionais = supabase.table("condicionais").select("*").eq("cliente_id", cliente_id).execute().data
        total_devido = sum(float(item.get('valor_total', 0)) for item in condicionais)
        total_pecas = sum(int(item.get('quantidade', 0)) for item in condicionais)
        return {"itens": condicionais, "total_devido": total_devido, "total_pecas": total_pecas}


    @staticmethod
    def processar_pagamento(cliente_id):
        supabase.table("condicionais").delete().eq("cliente_id", cliente_id).execute()
        return True


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
