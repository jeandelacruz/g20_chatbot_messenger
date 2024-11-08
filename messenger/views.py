from rest_framework import generics, status
from rest_framework.response import Response
from django.conf import settings
from time import sleep
from .utils.flows import FlowMethods

flow = FlowMethods()


class SetupView(generics.GenericAPIView):
    http_method_names = ['get']

    def get(self, request):
        response = flow.apigraph.setup()
        return Response(data=response, status=status.HTTP_200_OK)


class WebhookView(generics.GenericAPIView):
    http_method_names = ['get', 'post']

    def get(self, request):
        query_params = request.GET
        hub_mode = query_params.get('hub.mode')
        hub_challenge = query_params.get('hub.challenge')
        hub_verify_token = query_params.get('hub.verify_token')

        if hub_mode == 'subscribe' and hub_verify_token == settings.META_VERIFY:
            return Response(data=int(hub_challenge), status=status.HTTP_200_OK)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        data = request.data
        for entry in data['entry']:
            messaging = entry['messaging']
            for message in messaging:
                sender_id = message['sender']['id']
                postback = message.get('postback')
                messages = message.get('message')

                flow.apigraph.send_action(sender_id, 'mark_seen')
                sleep(1)
                flow.apigraph.send_action(sender_id, 'typing_on')
                sleep(1)

                if postback:
                    # TODO: Mensajes con accion
                    self.postback_event(sender_id, postback)
                else:
                    # TODO: Mensaje plano
                    self.message_event(sender_id, messages)
        return Response(status=status.HTTP_200_OK)

    def postback_event(self, sender_id, postback):
        flow.apigraph.send_action(sender_id, 'typing_off')
        payload = postback.get('payload')

        if payload == 'GET_STARTED_PAYLOAD':
            # TODO: Saludar al usuario
            return flow.welcome_message(sender_id)

    def message_event(self, sender_id, message):
        flow.apigraph.send_action(sender_id, 'typing_off')
        quick_reply = message.get('quick_reply')

        if quick_reply:
            # TODO: Respuestas rapidas
            return self.quick_reply_event(sender_id, quick_reply)

        # TODO: Capturar mensaje plano
        text = message.get('text')

        # TODO: Buscar la musica en Spotify
        flow.response_music(sender_id, text)

        # TODO: Reenviar las opciones al usuario
        return flow.retry_options_message(sender_id)

    def quick_reply_event(self, sender_id, quick_reply):
        payload = quick_reply.get('payload')

        if payload == 'SEARCH_MUSIC':
            return flow.search_music_message(sender_id)

        if payload == 'TALK_MESSAGE':
            flow.talk_chat_message(sender_id)

        # TODO: Reenviar las opciones al usuario
        return flow.retry_options_message(sender_id)


# sender_id, action
