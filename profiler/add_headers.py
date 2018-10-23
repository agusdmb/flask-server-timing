import flask

from .profile_manager import application


@application.after_request
def after_request(response):
    if flask.has_request_context() and flask.request.context:
        timing_list = [key.replace(' ', '-') + ';dur=' + str(val) + ';desc="' + key.replace(' ', '-') + '"' for key, val in flask.request.context.items()]
        response.headers.set('Server-Timing', ', '.join(timing_list))

    return response
