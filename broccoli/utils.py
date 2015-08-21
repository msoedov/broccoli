import types


def annotated_class(val):
    return isinstance(val, type) and hasattr(val, '__init__') and hasattr(
        val.__init__, '__annotations__') and val.__init__.__annotations__


def sub_modules(module):
    assert isinstance(module, types.ModuleType)
    modules = [module]
    package = module.__package__
    return modules + [
        m for m in module.__dict__.values()
        if isinstance(m, types.ModuleType) and m.__package__ == package
    ]
