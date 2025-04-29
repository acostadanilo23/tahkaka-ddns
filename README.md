# tahkaka-ddns-service

Este projeto é um **serviço de DDNS (Dynamic DNS)** que atualiza automaticamente o registro DNS de um domínio no Cloudflare com o IP público atual da máquina.  
Ideal para ambientes onde o IP muda frequentemente e é necessário manter o domínio sempre atualizado.

## ✨ Funcionalidades

- Consulta o IP público atual da máquina.
- Verifica se o IP já registrado no Cloudflare é diferente.
- Atualiza o registro DNS automaticamente se necessário.
- Utiliza API Token para segurança reforçada.
- Gera arquivos de log com histórico completo de execução.

## 🛠️ Pré-requisitos

- Python 3.7+
- Conta no [Cloudflare](https://www.cloudflare.com/)
- Um **API Token** do Cloudflare com permissões:
  - **Zone.DNS:Read**
  - **Zone.DNS:Edit**

## 📦 Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/tahkaka-ddns-service.git
cd tahkaka-ddns-service
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

Crie um arquivo .env na raiz do projeto com as seguintes variáveis:

```bash
CF_API_TOKEN='seu_token_cloudflare'
CF_ZONE_ID='sua_zone_id'
DDNS_RECORD_NAME='seu_dominio.exemplo.com'
DDNS_RECORD_TYPE='A' # ou 'AAAA' para IPv6
```

> Atenção: As variáveis CF_API_TOKEN, CF_ZONE_ID e DDNS_RECORD_NAME são obrigatórias!

## 🚀 Uso

Execute o script manualmente:

```bash
python tahkaka_ddns_service.py
```

Se quiser, agende a execução automática:

    Linux: via cron

    Windows: via Agendador de Tarefas

Exemplo de agendamento no crontab para rodar a cada 5 minutos:

```text
*/5 * * * * /usr/bin/python3 /caminho/para/tahkaka_ddns_service.py
```

## 🧩 Logs

O script gera um arquivo de log chamado ddns_update.log, contendo todas as operações realizadas com data e hora.
As mensagens também são exibidas no console em tempo real.

## 📁 Estrutura do Projeto

```text
tahkaka-ddns-service/
├── tahkaka_ddns_service.py
├── .env
├── requirements.txt
├── README.md
└── ddns_update.log   # (gerado automaticamente após a execução)
```

## 📝 Licença

Este projeto está sob a licença MIT.

Feito com ☁️ por *acostadanilo23*
