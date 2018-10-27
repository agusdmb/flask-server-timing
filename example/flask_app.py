from flask import Flask, jsonify
import logging
import time

from profiler import Timing


logging.basicConfig()
app = Flask(__name__)
t = Timing(app, force_debug=True)

from include import include # has to imported _after_ initialization


@app.route('/')
def root():
    with t.time('root'):
        time.sleep(0.2)

    t.start('done and done')
    time.sleep(0.3)
    t.stop('done and done')

    r = to_be_timed()

    include()

    return jsonify("W00t!: {}".format(r))


@t.timer(name='decorated')
def to_be_timed():
    time.sleep(0.4)

    return True


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
