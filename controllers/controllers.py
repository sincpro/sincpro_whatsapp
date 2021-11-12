# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.http import Response
import logging

_logger = logging.getLogger(__name__)


class ControllerWebhookMessenger(http.Controller):

    @http.route('/webhook_messenger', methods=['POST'], type='json', auth='public', csrf=False)
    def webhook(self, **kw):
        data = request.jsonrequest
        _logger.info(data)
        if data['object'] == 'page':
            test = http.request.env['handler.messenger'].sudo()
            test.handler_body(data)

            # data_processor = http.request.env['data.processor'].sudo()
            # try:
            #     data_processor.data_checker(data)
            # except:
            #     pass
            return 'EVENT_RECEIVED'
        else:
            return Response(status=404)

    @http.route('/webhook_messenger', methods=['GET'], auth='public')
    def verificacion_webhook(self, **kw):
        VERIFY_TOKEN = 'Hola_mundo'

        data = request
        mode = data.params['hub.mode']
        token = data.params['hub.verify_token']
        challenge = data.params['hub.challenge']

        if mode and token:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                _logger.info('WEBHOOK_VERIFIED')
                return challenge
            else:
                return Response(status=403)
