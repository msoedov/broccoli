def annotated_class(val):
    return isinstance(val, type) and hasattr(val, '__init__') and hasattr(
        val.__init__, '__annotations__') and val.__init__.__annotations__
