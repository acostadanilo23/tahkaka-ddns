# tahkaka-ddns-service

Este projeto é um **serviço de DDNS (Dynamic DNS)** que atualiza automaticamente o registro DNS de um domínio no Cloudflare com o IP público atual da máquina.  
Ideal para ambientes onde o IP muda frequentemente e é necessário manter o domínio sempre atualizado.

## ✨ Funcionalidades

- Consulta o IP público atual da máquina.
- Verifica se o IP já registrado no Cloudflare é diferente.
- Atualiza o registro DNS automaticamente se necessário.
- Utiliza API Token para segurança reforçada.
- Configuração simples via `.env`.

## 🛠️ Pré-requisitos

- Python 3.7+
- Conta no [Cloudflare](https://www.cloudflare.com/)
- Um **API Token** do Cloudflare com permissão de **Zone.DNS:Read** e **Zone.DNS:Edit**

## 📦 Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/tahkaka-ddns-service.git
cd tahkaka-ddns-service
```

Instale as dependências:
```
pip install -r requirements.txt
```

## ⚙️ Configuração

Crie um arquivo .env na raiz do projeto com as seguintes variáveis:

```bash
CLOUDFLARE_TOKEN='seu_token_cloudflare'
CLOUDFLARE_ZONE_ID='seu_zone_id'
DDNS_RECORD_NAME='seu_dominio.exemplo.com'
DDNS_RECORD_TYPE='A' # ou 'AAAA' para IPv6
```

> Atenção: As variáveis CLOUDFLARE_TOKEN, CLOUDFLARE_ZONE_ID e DDNS_RECORD_NAME são obrigatórias!

## 🚀 Uso

Execute o script manualmente:
```bash
python tahkaka_ddns_service.py
```
Se desejar, agende a execução periódica usando cron no Linux ou o Agendador de Tarefas no Windows.

Exemplo de agendamento no crontab para rodar a cada 5 minutos:
```bash
*/5 * * * * /usr/bin/python3 /caminho/para/tahkaka_ddns_service.py
```

## 📁 Estrutura do Projeto

```text
tahkaka-ddns-service/
├── tahkaka_ddns_service.py
├── .env
├── requirements.txt
└── README.md
```

## 📝 Licença

Este projeto está sob a licença MIT.

Feito com ☁️ por *acostadanilo23*