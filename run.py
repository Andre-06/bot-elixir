from keep_alive import keep_alive
from key import get_token
from start import client

print("Iniciando...")

TOKEN = get_token()
keep_alive()
client.run(TOKEN)
