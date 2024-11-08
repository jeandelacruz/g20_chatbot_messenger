from .apigraph import ApiGraph
from .spotify import SpotifyClient
from random import choice


class FlowMethods:
    def __init__(self):
        self.apigraph = ApiGraph()
        self.spotify = SpotifyClient()
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

    def response_music(self, recipient_id, text):
        results = self.spotify.search_track_or_artist(text)
        tracks = results['tracks']['items']
        return self.apigraph.send_message(
            recipient_id,
            {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'generic',
                        'elements': self.__serializer_elements(tracks)
                    }
                }
            }
        )

    def __serializer_elements(self, items):
        elements = []
        for item in items:
            track_name = item['name']
            artist_name = item['artists'][0]['name']
            track_album = item['album']
            album_name = track_album['name']
            album_image = track_album['images'][0]['url']
            track_url = item['external_urls']['spotify']
            elements.append({
                'title': f'{artist_name} - {track_name}',
                'image_url': album_image,
                'subtitle': album_name,
                'default_action': {
                    'type': 'web_url',
                    'url': track_url,
                    'webview_height_ratio': 'tall'
                },
                'buttons': [
                    {
                        'type': 'web_url',
                        'url': track_url,
                        'title': 'Play Spotify'
                    }
                ]
            })
        return elements
