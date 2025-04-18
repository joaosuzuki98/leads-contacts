import requests


class SendPulseService:
    def __init__(self, client_id, client_secret):
        self.token_url = 'https://api.sendpulse.com/oauth/access_token'
        self.token = self._authenticate(client_id, client_secret)

    def _authenticate(self, client_id, client_secret):
        """Autentica na API do SendPulse."""
        response = requests.post(self.token_url, {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        })
        response.raise_for_status()
        return response.json().get('access_token')

    def get_source_url(self, contact_id):
        """Obtém a campanha ou não da qual o lead veio"""
        url = 'https://api.sendpulse.com/whatsapp/' \
            f'chats/messages?contact_id={contact_id}'
        response = requests.get(
            url, headers={'Authorization': f'Bearer {self.token}'}
        )
        try:
            return response.json().get('data')[-1]['data'
                                                   ]['referral']['source_url']
        except Exception:
            return 'Nenhum'

    def insert_campaign(self, df):
        """
        Para preencher o campo 'campanha' de todos os contatos no dataframe,
        usado ao exportar CSV diretamente do SendPulse.
        """
        print("Preenchendo campanhas para todos os contatos...")
        source_urls = []
        for contact_id in df.iloc[:, 0]:
            source = self.get_source_url(contact_id)
            print(source)
            source_urls.append(source)

        df['campanha'] = source_urls
        return df
