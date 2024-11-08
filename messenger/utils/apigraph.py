from django.conf import settings
from requests import post


class ApiGraph:
    def __init__(self):
        self.host = 'https://graph.facebook.com'
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.access_token = settings.META_TOKEN

    def setup(self):
        # https://developers.facebook.com/docs/messenger-platform/discovery/welcome-screen
        response = post(
            f'{self.host}/v18.0/me/messenger_profile',
            params={
                'access_token': self.access_token
            },
            headers=self.headers,
            json={
                'get_started': {
                    'payload': 'GET_STARTED_PAYLOAD'
                },
                'greeting': [
                    {
                        'locale': 'default',
                        'text': 'Hola, {{user_full_name}}'
                    }
                ]
            }
        )
        return response.json()

    def send_message(self, recipient_id, body):
        response = post(
            f'{self.host}/v21.0/me/messages',
            params={
                'access_token': self.access_token
            },
            headers=self.headers,
            json={
                'recipient': {
                    'id': recipient_id
                },
                'messaging_type': 'RESPONSE',
                'message': body
            }
        )
        return response.json()
