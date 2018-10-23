import flask
import datetime
from flask import request

application = None


class ProfileManager():
    def __init__(self, app, mode):
        global application
        self.app = app
        application = app
        if mode.lower() == 'debug':
            from .add_headers import after_request

    def start(self, key):
        if not flask.has_request_context():
            return

        if not hasattr(request, 'context'):
            request.context = {}

        request.context[key.replace(' ', '-')] = {'start': datetime.datetime.now()}

    def stop(self, key):
        if not flask.has_request_context() or not hasattr(request, 'context'):
            return

        key = key.replace(' ', '-')
        if not key in request.context:
            return

        stop_time = datetime.datetime.now()
        start_time = request.context.get(key, {}).get('start')
        if start_time:
            request.context[key] = (stop_time - start_time).total_seconds() * 1000
