import flask
import datetime
import logging
from flask import request

from contextlib import contextmanager


class ProfileManager():
    def __init__(self, app, mode):
        self.log = logging.getLogger()
        if mode.lower() == 'debug':
            self.log.info("Setting up after-request handler to add server timing header")
            app.after_request(ProfileManager._add_header)

    def start(self, key):
        if not flask.has_request_context():
            self.log.debug("No request context available - start timing ignored")
            return

        if not hasattr(request, 'context'):
            request.context = {}

        request.context[key.replace(' ', '-')] = {'start': datetime.datetime.now()}

    def stop(self, key):
        if not flask.has_request_context() or not hasattr(request, 'context'):
            self.log.debug("No request context available - stop timing ignored")
            return

        _key = key.replace(' ', '-')
        if not _key in request.context:
            self.log.warn("Key '{}' not found in request context".format(key))
            return

        stop_time = datetime.datetime.now()
        start_time = request.context.get(_key, {}).get('start')
        if start_time:
            request.context[_key] = (stop_time - start_time).total_seconds() * 1000
        else:
            self.log.warn("No start time found for key '{}'".format(key))

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
