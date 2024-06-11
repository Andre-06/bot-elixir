from key import get_token
from main import client

print("Iniciando...")

TOKEN = get_token()

client.run(TOKEN)
