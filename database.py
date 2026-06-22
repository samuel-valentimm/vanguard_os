import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv(override=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print(f"DEBUG: URL={SUPABASE_URL}")
print(f"DEBUG: KEY={SUPABASE_KEY}")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Variáveis de ambiente não carregadas! Verifique o arquivo .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)