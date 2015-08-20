from collections import namedtuple
import inspect


Db = namedtuple('Db', '')
Session = namedtuple('Session', '')
Service = namedtuple('Service', '')


def new_app():
    return Db(), Session(), Service()


def request(request, db: Db, session: Session, service: Service):
    print(request, db, session, service)


def inject(fn):
    deps = new_app()
    type_to_dependency = {type(d): d for d in deps}
    detected_dependecies = {}
    signature = inspect.signature(fn)
    for val, _type in fn.__annotations__.items():
        dep = type_to_dependency.get(_type)
        if dep is None:
            continue
        detected_dependecies[val] = dep
    defaults = []
    for param in signature.parameters:
        if param in detected_dependecies:
            defaults.append(detected_dependecies[param])
    fn.__defaults__ = tuple(defaults)
    return fn


inject(request)

request('foo')

print(self)
