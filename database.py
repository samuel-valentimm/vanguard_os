import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv() # Carrega as variaveis do .env

# Pega as chaves direto do sistema, sem expor elas
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Conexao com a nuvem
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class ClienteService:

    @classmethod
    def listar_clientes(cls):
        resposta = supabase.table('clientes').select('*').execute() # Busca os clientes salvos na tabela do supabase
        return resposta.data # Retorna a lista de dados
    
    @classmethod
    def adicionar_cliente(cls, nome, telefone):
        if nome and telefone: # Insere o novo cliente ja na nuvem
            supabase.table('clientes').insert({"nome": nome, "telefone": telefone}).execute()

    @classmethod
    def deletar_cliente(cls, id_cliente): # Deleta o cliente na nuvem pelo ID unico
        supabase.table('clientes').delete().eq('id', id_cliente).execute()


class ProdutoService:

    @classmethod
    def cadastrar_produto_com_grade(cls, dados):
        """
        CORRIGIDA: Cria o produto PAI apenas uma vez e distribui todos os 
        tamanhos preenchidos na tabela de variações.
        """

        nome_produto = dados.get("nome").upper().strip()
        categoria_produto = dados.get("categoria")
        cor_produto = dados.get("cor").upper().strip()

        produto_existente = supabase.table("produtos")\
            .select("id")\
            .eq("nome", nome_produto)\
            .eq("categoria", categoria_produto)\
            .execute()

        if produto_existente.data:
            produto_id = produto_existente.data[0]["id"]
        else:
            novo_produto = {
                "nome": nome_produto,
                "categoria": categoria_produto
            }

            resultado = supabase.table("produtos").insert(novo_produto).execute()
            
            if not resultado.data:
                raise Exception("Erro ao criar o produto principal no banco.")
            
            produto_id = resultado.data[0]["id"]

        nome_slug = nome_produto.replace(" ", "-")
        cor_slug = cor_produto.replace(" ", "-")
        
        tamanhos = ['p', 'm', 'g', 'gg']
        variacoes_para_salvar = []
        
        for t in tamanhos:
     
            qtd = int(dados.get(f"qtd_{t}", 0))
            custo = float(dados.get(f"custo_{t}", 0.0))
            venda = float(dados.get(f"venda_{t}", 0.0))
            
            if qtd > 0 or custo > 0 or venda > 0:
                sku_gerado = f"{nome_slug}-{cor_slug}-{t.upper()}"
                
                variacoes_para_salvar.append({
                    "sku": sku_gerado,
                    "produto_id": produto_id,
                    "cor": cor_produto,
                    "tamanho": t.upper(),
                    "preco_custo": custo,
                    "preco_venda": venda,
                    "quantidade": qtd
                })
        

        if variacoes_para_salvar:
            supabase.table("estoque_variacoes").upsert(variacoes_para_salvar).execute()
            
        return produto_id
            

    @classmethod
    def listar_produtos_estoque(cls):
        """
        Faz uma juncao com JOIN, para trazert o produtos e seus detalhes de estoque juntos.
        """

        resultado = supabase.table("estoque_variacoes").select("*, produtos(nome, categoria)").execute()

        return resultado.data
    