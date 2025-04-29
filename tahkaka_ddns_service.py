import os
import sys
import requests
import logging
from dotenv import load_dotenv

# Configurar Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Log para arquivo
file_handler = logging.FileHandler('ddns_update.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Log para console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(stream_handler)

# Mensagem inicial
logger.info("Iniciando script DDNS Service")

# Carrega variáveis do .env
load_dotenv()
logger.info(".env carregado.")

# Carrega as variáveis de ambiente
TOKEN = os.environ.get("CF_API_TOKEN")
ZONE_ID = os.environ.get("CF_ZONE_ID")
RECORD_NAME = os.environ.get("DDNS_RECORD_NAME")
REC_TYPE = os.environ.get("DDNS_RECORD_TYPE", "A").upper()

if not all([TOKEN, ZONE_ID, RECORD_NAME]):
    logger.error("Erro: Variáveis CF_API_TOKEN, CF_ZONE_ID, DDNS_RECORD_NAME são obrigatórias (verifique o .env)!")
    sys.exit(1)

logger.info(f"Iniciando DDNS check para {RECORD_NAME} ({REC_TYPE})")

# Obtém IP Público Atual
try:
    ip_resp = requests.get('https://api.ipify.org')
    ip_resp.raise_for_status()
    public_ip = ip_resp.text.strip()
    logger.info(f"IP Público Atual: {public_ip}")
except Exception as e:
    logger.error(f"Erro ao obter IP público: {e}")
    sys.exit(1)

# Obtém informações atuais do registro no Cloudflare
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
cf_url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
params = {
    "name": RECORD_NAME,
    "type": REC_TYPE
}

try:
    cf_resp = requests.get(cf_url, headers=headers, params=params)
    cf_resp.raise_for_status()
except Exception as e:
    logger.error(f"Erro ao buscar registro no Cloudflare: {e}")
    sys.exit(1)

cf_data = cf_resp.json()
if not cf_data.get("success") or not cf_data.get("result"):
    logger.error(f"Erro na resposta da API Cloudflare ao buscar registro: {cf_data.get('errors')}")
    sys.exit(1)

if len(cf_data["result"]) == 0:
    logger.error(f"Erro: Registro {RECORD_NAME} ({REC_TYPE}) não encontrado no Cloudflare.")
    sys.exit(1)

record_info = cf_data["result"][0]
cloudflare_ip = record_info["content"]
record_id = record_info["id"]

logger.info(f"IP Atual no Cloudflare: {cloudflare_ip}")

# Comparar IPs e atualizar se necessário
if public_ip == cloudflare_ip:
    logger.info("IPs são iguais. Nenhuma atualização necessária.")
    sys.exit(0)

logger.info(f"IPs diferentes ({public_ip} != {cloudflare_ip}). Atualizando Cloudflare...")

update_url = f"{cf_url}/{record_id}"
payload = {
    "type": REC_TYPE,
    "name": RECORD_NAME,
    "content": public_ip,
    "ttl": 1,
    "proxied": record_info["proxied"]
}

try:
    update_resp = requests.put(update_url, headers=headers, json=payload)
    update_resp.raise_for_status()
except Exception as e:
    logger.error(f"Erro ao atualizar registro no Cloudflare: {e}")
    sys.exit(1)

update_data = update_resp.json()
if update_data.get("success"):
    logger.info("Sucesso! Registro DNS atualizado no Cloudflare.")
    sys.exit(0)
else:
    logger.error(f"Falha na atualização: {update_data.get('errors')}")
    sys.exit(1)
