from collections import namedtuple

Db = namedtuple('Db', '')
Session = namedtuple('Session', '')
Service = namedtuple('Service', '')
Cache = namedtuple('Cache', '')


def new_app():
    return Db(), Session(), Service(), Cache()


def request(request, db: Db, session: Session, service: Service):
    return request, db, session, service


def update_query(db: Db):
    return db


def regular_function(a, b, c):
    return a, b, c
