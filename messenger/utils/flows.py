from .apigraph import ApiGraph
from random import choice


class FlowMethods:
    def __init__(self):
        self.apigraph = ApiGraph()
        self.options = [
            {
                'content_type': 'text',
                'title': 'Buscar Musica',
                'payload': 'SEARCH_MUSIC'
            },
            {
                'content_type': 'text',
                'title': 'Conversar',
                'payload': 'TALK_MESSAGE'
            }
        ]

    def welcome_message(self, recipient_id):
        return self.apigraph.send_quick_replies(
            recipient_id,
            'Hola, ¿Qué deseas hacer?',
            self.options
        )

    def retry_options_message(self, recipient_id):
        return self.apigraph.send_quick_replies(
            recipient_id,
            'Ahora, que deseas hacer?',
            self.options
        )

    def talk_chat_message(self, recipient_id):
        messages = [
            'Estas bien?',
            'Se quema la comida',
            'Cuidado'
        ]
        return self.apigraph.send_message(
            recipient_id,
            {
                'text': choice(messages)
            }
        )

    def search_music_message(self, recipient_id):
        return self.apigraph.send_message(
            recipient_id,
            {
                'text': 'Escriba el nombre de la canción o del artista que deseas buscar:'
            }
        )
