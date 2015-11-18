# Broccoli

Broccoli is a simple dependency injection package based on type annotations

[![PyPI](https://img.shields.io/pypi/v/broccoli.svg)]()
[![Supported versions](https://img.shields.io/pypi/pyversions/broccoli.svg)]()
[![Build Status](https://travis-ci.org/msoedov/brocolli.svg)](https://travis-ci.org/msoedov/brocolli)

Installation
-----------
```shell
pip install broccoli

```

Features
--------
- **Simple** - less than 100 lines of code without external dependencies
- **Error check** - Function signature check on start up - less errors during refactoring
- **Fast** - Designed to have zero runtime overhead, all dependencies injected either on module load or application start up.
- **Powerful** - Auto-discovery of dependencies by package and by module
- **Convenient** - Hackable and elegant programmatic API. Really easy to start using it.


Python 2 support?
-----------------
Oups, sorry


Basic Usage
-----------

Inject dependency to function with type annotations

```python
from broccoli import bind

class Dependency:
    pass

def foo(a, bar:Dependency):
    print(a, bar)

bind(foo, Dependency())
foo(1)  # prints 1 <__main__.Dependency object at 0x11111b7b8>
```

Inject dependency to module/package
```python
# module foo.py

def foo(a, b:DependencyA):
    print(a, b)


def bar(a, b:DependencyB):
    print(a, b)

# main.py
from broccoli import inject
from package import foo

inject(foo, DependencyA(), DependencyB())

# or
inject('package.foo', DependencyA(), DependencyB())

```

Example with decorator wich inject deps on demand
```python
from brocolli.fixtures.types import *
from broccoli import Dependency


def dependecies():
    return Db(), Service(), Cache()


default_dependencies = Dependency(dependecies)


@default_dependencies
def a(db: Db):
    return db.query('User').all()
```

Inject deps on application entry point
```python
...

default_dependencies = Dependency()


@default_dependencies
def a(db: Db):
    return db.query('User').all()

if __name__ == '__main__':
    default_dependencies << dependecies
    # or even
    default_dependencies << dependecies()

```

Test examples
--------
[examples](https://github.com/msoedov/brocolli/tree/master/tests)


This looks as dirty hack why should use it?
---------------------------------------------
No reason, you can keep using module level variables and singleton objects. But if you know a good example of unit tests for such code don't hesitate to share it.


Getting Help
------------

For **feature requests** and **bug reports** [submit an issue
](https://github.com/msoedov/brocolli/issues) to the GitHub issue tracker for
Broccoli.

