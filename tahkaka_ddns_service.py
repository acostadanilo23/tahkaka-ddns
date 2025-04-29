import os
import requests
import sys
from dotenv import load_dotenv # Importa a função necessária

# Carrega as variáveis do arquivo .env para o ambiente do script
# Faça isso ANTES de tentar acessar as variáveis com os.environ.get()
load_dotenv()

print("Variáveis do .env carregadas.") # Mensagem de confirmação (opcional)

# 1. Configuração e Verificação Inicial (agora lê do ambiente populado pelo dotenv)
TOKEN = os.environ.get("CF_API_TOKEN")
ZONE_ID = os.environ.get("CF_ZONE_ID")
RECORD_NAME = os.environ.get("DDNS_RECORD_NAME")
REC_TYPE = os.environ.get("DDNS_RECORD_TYPE", "A").upper()

if not all([TOKEN, ZONE_ID, RECORD_NAME]):
    print("Erro: Variáveis CF_API_TOKEN, CF_ZONE_ID, DDNS_RECORD_NAME são obrigatórias (verifique o .env)!")
    sys.exit(1)

print(f"Iniciando DDNS check para {RECORD_NAME} ({REC_TYPE})")

# 2. Obter IP Público Atual
ip_resp = requests.get('https://api.ipify.org')
if ip_resp.status_code != 200:
    print(f"Erro ao obter IP público: Status {ip_resp.status_code}")
    sys.exit(1)
public_ip = ip_resp.text.strip()
print(f"IP Público Atual: {public_ip}")

# 3. Obter Info do Cloudflare
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
cf_url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
params = {"name": RECORD_NAME, "type": REC_TYPE}
cf_resp = requests.get(cf_url, headers=headers, params=params)

if cf_resp.status_code != 200:
    print(f"Erro ao buscar registro no Cloudflare: Status {cf_resp.status_code}")
    sys.exit(1)

cf_data = cf_resp.json()
if not cf_data.get("success") or not cf_data.get("result"):
    print(f"Erro na resposta da API Cloudflare ao buscar registro: {cf_data.get('errors')}")
    sys.exit(1)
if len(cf_data["result"]) == 0:
     print(f"Erro: Registro {RECORD_NAME} ({REC_TYPE}) não encontrado no Cloudflare.")
     sys.exit(1)

record_info = cf_data["result"][0]
cloudflare_ip = record_info["content"]
record_id = record_info["id"]
print(f"IP Atual no Cloudflare: {cloudflare_ip}")

# 4. Comparar e Atualizar (se necessário)
if public_ip == cloudflare_ip:
    print("IPs são iguais. Nenhuma atualização necessária.")
    sys.exit(0)

print(f"IPs diferentes ({public_ip} != {cloudflare_ip}). Atualizando Cloudflare...")
update_url = f"{cf_url}/{record_id}"
payload = {
    "type": REC_TYPE, "name": RECORD_NAME, "content": public_ip,
    "ttl": 1, "proxied": record_info["proxied"]
}
update_resp = requests.put(update_url, headers=headers, json=payload)

if update_resp.status_code != 200:
     print(f"Erro ao atualizar registro no Cloudflare: Status {update_resp.status_code}")
     sys.exit(1)

update_data = update_resp.json()
if update_data.get("success"):
    print("Sucesso! Registro DNS atualizado no Cloudflare.")
    sys.exit(0)
else:
    print(f"Falha na atualização: {update_data.get('errors')}")
    sys.exit(1)

