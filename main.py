import requests


ip_publico = requests.get('https://api.ipify.org').text
ip_atual = 'ip_publico'

if ip_publico == ip_atual:
    print('Ips são iguais, não será feita nenhuma mudança.')
else:
    print('Endereço de ip diferente, atualizando DNS Record para o novo ip.')
    print('Fake update API CF')
    print('DNS Record atualizado.')

