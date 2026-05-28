from database import supabase

class ClienteService:
    @staticmethod
    def listar_clientes():
        resposta = supabase.table("clientes").select("*").execute()
        return resposta.data if resposta.data else []


    @staticmethod
    def adicionar_cliente(dados):
        dados['nome'] = dados['nome'].upper().strip()
        supabase.table('clientes').insert(dados).execute()


    @staticmethod
    def deletar_cliente(id_cliente):
        supabase.table('clientes').delete().eq('id', id_cliente).execute()


    @staticmethod
    def buscar_id_por_nome(nome_cliente):
        nome_limpo = str(nome_cliente).strip()
        resposta = supabase.table('clientes').select('id').ilike('nome', nome_limpo).maybe_single().execute()
        return resposta.data['id'] if resposta and resposta.data else None


    @staticmethod
    def buscar_cliente_por_id(cliente_id):
        response = supabase.table("clientes").select("*").eq("id", cliente_id).single().execute()
        return response.data


    @staticmethod
    def formatar_dados(cliente):
        tel = str(cliente.get('telefone', ''))
        if len(tel) == 11:
            cliente['telefone'] = f"({tel[0:2]}) {tel[2:7]}-{tel[7:11]}"
        return cliente