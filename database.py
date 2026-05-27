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