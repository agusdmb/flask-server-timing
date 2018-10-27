from flask import Flask, jsonify
import logging
import time

from server_timing import Timing


logging.basicConfig()
app = Flask(__name__)
t = Timing(app, force_debug=True)

from include import include # has to imported _after_ initialization


@app.route('/')
def root():
    # explicitly calling start and stop before and after - keys need to be identical
    t.start('done and done')
    time.sleep(0.3)
    t.stop('done and done')

    # context manager support to avoid having to call start and stop explicitly
    with t.time('context'):
        time.sleep(0.2)

    # decorated with name being the key
    named_decoration()
    # decorated without name so the function is the key
    unnamed_decoration()

    include()

    return jsonify("DONE")


@t.timer(name='named')
def named_decoration():
    time.sleep(0.4)

@t.timer
def unnamed_decoration():
    time.sleep(0.5)


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
