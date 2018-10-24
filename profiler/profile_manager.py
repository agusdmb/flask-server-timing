import flask
import datetime
from flask import request

from contextlib import contextmanager


class ProfileManager():
    def __init__(self, app, mode):
        if mode.lower() == 'debug':
            app.after_request(ProfileManager._add_header)

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

    @contextmanager
    def time(self, key):
        self.start(key)
        yield key
        self.stop(key)

    @staticmethod
    def _add_header(response):
        if flask.has_request_context() and flask.request.context:
            timing_list = [key + ';dur=' + str(val) + ';desc="' + key + '"' for key, val in flask.request.context.items()]
            response.headers.set('Server-Timing', ', '.join(timing_list))

        return response
