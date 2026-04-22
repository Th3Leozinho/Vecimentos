import datetime
import requests

# CONFIGURAÇÕES
# Datas de renovação (formato: AAAA-MM-DD)
spotify_renovacao = datetime.date(2026, 4, 21)
iptv_renovacao = datetime.date(2026, 4, 21)

# Frequências
spotify_frequencia = datetime.timedelta(days=365)  # 1 ano
iptv_frequencia = datetime.timedelta(days=30)      # 30 dias

# Telegram
TELEGRAM_TOKEN = '8245354299:AAEinGrrz-OE8-cufO0BOGZkVNXhBkUiBgM'
TELEGRAM_CHAT_ID = '-5133616689'

# Quantos dias antes avisar
AVISO_ANTES_DIAS_SPOTIFY = 3  # Spotify avisa 3 dias antes
AVISO_ANTES_DIAS_IPTV = 1     # IPTV avisa 1 dia antes

def proximo_vencimento(data_renovacao, frequencia):
    hoje = datetime.date.today()
    proxima = data_renovacao
    while proxima < hoje:
        proxima += frequencia
    return proxima

def enviar_telegram(mensagem):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': mensagem}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f'Erro ao enviar mensagem: {e}')

def checar_e_avisar():
    print(f"[LOG] Executando checagem em {datetime.datetime.now()}")
    hoje = datetime.date.today()
    agora = datetime.datetime.now()
    venc_spotify = proximo_vencimento(spotify_renovacao, spotify_frequencia)
    venc_iptv = proximo_vencimento(iptv_renovacao, iptv_frequencia)

    # Spotify: avisa somente no dia do vencimento anual, e apenas uma vez às 09h00
    print(f"[LOG] Próximo vencimento Spotify: {venc_spotify}")
    print(f"[LOG] Próximo vencimento IPTV: {venc_iptv}")
    if hoje == venc_spotify:
        if agora.hour == 9 and agora.minute == 0:
            print("[LOG] Enviando aviso do Spotify para o Telegram")
            enviar_telegram(f'Spotify: RENOVE AGORA SEU SPOTIFY! Vence hoje ({venc_spotify.strftime("%d/%m/%Y")})')

    # IPTV: avisa 1 dia antes (qualquer hora)
    if (venc_iptv - hoje).days == AVISO_ANTES_DIAS_IPTV:
        print("[LOG] Enviando aviso de IPTV para o Telegram (vence amanhã)")
        enviar_telegram(f'IPTV vence amanhã ({venc_iptv.strftime("%d/%m/%Y")})!')
    # IPTV: envia mensagem todo dia 22 às 09h00
    if hoje.day == 22 and agora.hour == 9 and agora.minute == 0:
        # Controle para não enviar várias vezes no mesmo dia
        try:
            with open('controle_envio_iptv.txt', 'r') as f:
                ultima_data = f.read().strip()
        except FileNotFoundError:
            ultima_data = ''
        data_envio = hoje.strftime('%Y-%m-%d')
        if ultima_data != data_envio:
            print("[LOG] Enviando aviso recorrente de IPTV para o Telegram")
            enviar_telegram('IPTV: RENOVE AGORA SEU IPTV por R$10,00')
            with open('controle_envio_iptv.txt', 'w') as f:
                f.write(data_envio)

if __name__ == '__main__':
    import time
    print("[LOG] Iniciando loop principal do aviso de vencimentos...")
    while True:
        checar_e_avisar()
        time.sleep(5)  # Espera 5 segundos
