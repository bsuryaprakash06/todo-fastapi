import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "your-project-url")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-client-key")

def get_supabase_client() -> Client:
    """Returns a configured Supabase client."""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase_client = get_supabase_client()
