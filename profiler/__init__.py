import logging

from .profile_manager import ProfileManager as Timing


def timing(app=None, force_debug=False):
    log = logging.getLogger()
    if app.debug or force_debug:
        log.info("Setting up after-request handler to add server timing header")
        app.after_request(Timing._add_header)

    return Timing(app, 'None')
