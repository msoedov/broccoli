from collections import namedtuple

Db = namedtuple('Db', '')
Session = namedtuple('Session', '')
Service = namedtuple('Service', '')


def new_app():
    return Db(), Session(), Service()


def request(request, db: Db, session: Session, service: Service):
    print(request, db, session, service)


def req(request, db=Db(), session=1):
    pass


def update_query(db: Db):
    print(db)


class Foo(object):
    def __init__(self, db: Db):
        self.db = db

# inject('__main__', *new_app())

# request('foo')
# update_query()
# update_query('MockDb')
# f = Foo()
