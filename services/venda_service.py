from database import supabase

class VendaService:
    @staticmethod
    def registrar_venda_direta(dados):
        """
        dados deve conter: sku, quantidade, valor_total, valor_recebido, troco
        """
  
        produto = supabase.table("estoque_variacoes") \
            .select("quantidade") \
            .eq("sku", dados['sku']) \
            .single() \
            .execute().data
        
        if not produto or produto['quantidade'] < int(dados['quantidade']):
            raise Exception("Estoque insuficiente para esta venda.")

        supabase.table("vendas").insert({
            "sku": dados['sku'],
            "quantidade": int(dados['quantidade']),
            "valor_total": float(dados['valor_total']),
            "valor_recebido": float(dados['valor_recebido']),
            "troco": float(dados['troco']),
            "tipo_pagamento": "dinheiro"
        }).execute()

        nova_qtd = produto['quantidade'] - int(dados['quantidade'])
        supabase.table("estoque_variacoes") \
            .update({"quantidade": nova_qtd}) \
            .eq("sku", dados['sku']) \
            .execute()
        
        return True


    @staticmethod
    def obter_historico_vendas(data_inicio, data_fim):
        """
        Busca vendas filtrando pelo período (para o seu dashboard)
        """
        return supabase.table("vendas") \
            .select("*") \
            .gte("data_venda", data_inicio) \
            .lte("data_venda", data_fim) \
            .execute().data