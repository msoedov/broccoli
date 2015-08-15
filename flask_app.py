from flask import Flask
from injection import BrocolliPlugin

from inject import *

app = Flask(__name__)


@app.route('/')
def hello_world(s: Service):
    print(s)
    return 'Hello World! {}'.format(s)


if __name__ == '__main__':
    BrocolliPlugin(app, *new_app())
    app.run()
