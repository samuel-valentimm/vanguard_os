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
        resposta = supabase.table('clientes').select('*').execute()
        return resposta.data
    
    @classmethod
    def adicionar_cliente(cls, dados):
        supabase.table('clientes').insert(dados).execute()

    @classmethod
    def deletar_cliente(cls, id_cliente):
        supabase.table('clientes').delete().eq('id', id_cliente).execute()


class ProdutoService:
    @classmethod
    def cadastrar_produto_com_grade(cls, dados):
        """
        Cadastro unificado: busca ou cria o produto PAI e insere a variação.
        """

        nome_produto = str(dados.get("nome_produto", "PRODUTO")).upper().strip()
        cor_produto = str(dados.get("cor", "UNICA")).upper().strip()
        tamanho = str(dados.get("tamanho", "U")).upper().strip()

        produto_existente = supabase.table("produtos")\
            .select("id")\
            .eq("nome", nome_produto)\
            .execute()

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