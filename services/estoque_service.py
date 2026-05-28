from database import supabase

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
    def deletar_variacao(cls, id_variacao):
        return supabase.table("estoque_variacoes").delete().eq("id", id_variacao).execute()


    @staticmethod
    def listar_produtos_estoque():
        resultado = supabase.table("estoque_variacoes").select("*, produtos(nome, categoria)").execute()
        return resultado.data