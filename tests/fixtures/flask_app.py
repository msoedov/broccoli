from flask import Flask
from broccoli import BroccoliPlugin

app = Flask(__name__)


class Service(object):

    def __init__(self, arg):
        super(Service, self).__init__()
        self.arg = arg


@app.route('/')
def hello_world(s: Service):
    return 'Hello World! {}'.format(s.arg)


def web_app():
    service = Service('foo')
    BroccoliPlugin(app, service)
    return app


if __name__ == '__main__':
    web_app().run()
