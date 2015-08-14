from .core import bind


def BrocolliPlugin(app, *dependencies):
    errors = []
    for rule in app.url_map.iter_rules():
        ok, deps = bin(rule.endpoint, dependencies)
    return errors
