# Broccoli

Broccoli is a simple dependency injection package based on type annotations

[![Build Status](https://travis-ci.org/msoedov/brocolli.svg)](https://travis-ci.org/msoedov/brocolli)
[![Py3 support](https://caniusepython3.com/check/f332c1e2-d31f-4e5c-b0af-0a85bf7f00cd.svg?style=flat)]()

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


Examples
--------
[/examples](https://github.com/)

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

This looks as dirty hack why should use it?
---------------------------------------------
No reason, you can keep using module level variables and singleton objects. But if you know a good example of unit tests for such code don't hesitate to share it.


Getting Help
------------

For **feature requests** and **bug reports** [submit an issue
](https://github.com/msoedov/brocolli/issues) to the GitHub issue tracker for
Broccoli.

