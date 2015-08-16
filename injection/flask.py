from .core import bind


def BroccoliPlugin(app, *dependencies):
    errors = []
    for rule in app.url_map.iter_rules():
        view = app.view_functions[rule.endpoint]
        ok, deps = bind(view, *dependencies)
    return errors


BroccoliFlask = BroccoliPlugin
