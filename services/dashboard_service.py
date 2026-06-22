from database import supabase

class DashboardService:
    @staticmethod
    def get_dashboard_metrics():

        try:

            clientes = supabase.table('clientes').select('*', count='exact').execute().count
            total_clientes = clientes.bit_count

            vendas = supabase.table('vendas').select('*', count='exact').execute().count
            total_vendas = vendas.count

            vendas_data = supabase.table('vendas').select('valor').execute().data
            if vendas_data:
                faturamento = sum(item.get('valor', 0) for item in vendas_data)
            else:
                faturamento = 0

            return {
                'total_clientes': total_clientes,
                'total_vendas': total_vendas,
                'faturamento': faturamento
            }
        
        except Exception as e:
            print(f'Erro ao buscar métricas: {e}')
            return {'total_clientes': 0, 'total_vendas': 0, 'faturamento': 0}