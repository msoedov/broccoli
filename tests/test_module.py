from collections import namedtuple

Db = namedtuple('Db', '')
Session = namedtuple('Session', '')
Service = namedtuple('Service', '')
Cache = namedtuple('Cache', '')
UselessManager = namedtuple('Manger', '')


def new_app():
    return Db(), Session(), Service(), Cache()


def request(request, db: Db, session: Session, service: Service):
    return request, db, session, service


def update_query(db: Db):
    return db


def utility(a, b, c):
    return a, b, c


def do_stuff(session: Session, mgr: UselessManager):
    return session, mgr


def validation(mgr: UselessManager, service: Service):
    return mgr, service


class Foo(object):
    def __init__(self, db: Db):
        self.db = db
