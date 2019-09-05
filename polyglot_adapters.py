class _AbstractAdapter():
    def __init__(self, _wrapped_value, extended_behavior=None):
        self._polyglot_mapping = {}
        self._wrapped_value = _wrapped_value
        self._polyglot_mapping.update(self.__default_polyglot__mapping___())
        if isinstance(extended_behavior, dict):
            for identifier in extended_behavior:
                target = extended_behavior[identifier]
                if isinstance(target, str):
                    if not hasattr(self._wrapped_value, target):
                        raise PolyglotAdapterError(
                            'Value "%s" does not have attribute named "%s"' % (
                                self._wrapped_value, target))
                    attr = getattr(self._wrapped_value, target)
                    if callable(attr):
                        self._polyglot_mapping[identifier] = attr
                    else:
                        raise PolyglotAdapterError(
                            'Target "%s" not callable, is "%s"' % (
                                target, attr))
                elif callable(target):
                    def _wrap_func(*args):
                        return target(self._wrapped_value, *args)
                    self._polyglot_mapping[identifier] = _wrap_func
                else:
                    raise PolyglotAdapterError(
                        'Unsupported target "%s"' % target)
        elif isinstance(extended_behavior, type):
            import inspect
            for identifier, target in inspect.getmembers(
                    extended_behavior, predicate=inspect.isfunction):
                def _wrap_func(*args):
                    return target(self._wrapped_value, *args)
                self._polyglot_mapping[identifier] = _wrap_func

    def __str__(self):
        return str(self._wrapped_value)

    def __repr__(self):
        return str(self._wrapped_value)

    def __iter__(self):
        return iter(self._wrapped_value)

    def __len__(self):
        return len(self._wrapped_value)

    def __default_polyglot__mapping___(self, *args):
        raise PolyglotAdapterError('Must be implemented by subclass')

    def __getattribute__(self, name):
        if name.startswith('_'):
            return object.__getattribute__(self, name)
        try:
            return object.__getattribute__(self, '_polyglot_mapping')[name]
        except KeyError:
            raise AttributeError("%r object has no attribute2 %r" %
                                 (self.__class__.__name__, name))


class _RubyObjectAdapter(_AbstractAdapter):

    def __default_polyglot__mapping___(self):
        def identical(x):
            if isinstance(x, _AbstractAdapter):
                return identical(x._wrapped_value)
            else:
                if self._wrapped_value == x:
                    return 0
                elif self._wrapped_value > x:
                    return 1
                else:
                    return -1

        return {
            'to_s': lambda: str(self._wrapped_value),
            '<=>': identical,
            '>': lambda x: self._wrapped_value > x
        }


class _JavaScriptObjectAdapter(_AbstractAdapter):

    def __default_polyglot__mapping___(self):
        return {
            'length': lambda: len(self._wrapped_value),
            'toString': lambda: str(self._wrapped_value)
        }


class _JavaScriptListAdapter(_JavaScriptObjectAdapter):

    def __default_polyglot__mapping___(self):

        def indexOf(x):
            try:
                return self._wrapped_value.index(x)
            except ValueError:
                return -1

        mapping = super().__default_polyglot__mapping___()
        mapping.update({
            'concat': lambda o: self._wrapped_value + o,
            'copyWithin': lambda: str(self._wrapped_value),
            'entries': lambda: str(self._wrapped_value),
            'every': lambda: str(self._wrapped_value),
            'fill': lambda: str(self._wrapped_value),
            'filter': lambda: str(self._wrapped_value),
            'find': lambda: str(self._wrapped_value),
            'findIndex': lambda: str(self._wrapped_value),
            'flat': lambda: str(self._wrapped_value),
            'flatMap': lambda: str(self._wrapped_value),
            'forEach': lambda: str(self._wrapped_value),
            'includes': lambda o: o in self._wrapped_value,
            'indexOf': indexOf,
            'join': lambda: str(self._wrapped_value),
            'keys': lambda: str(self._wrapped_value),
            'lastIndexOf': lambda: str(self._wrapped_value),
            'map': lambda: str(self._wrapped_value),
            'pop': lambda: self._wrapped_value.pop(),
            'push': lambda x: self._wrapped_value.append(x),
            'reduce': lambda: str(self._wrapped_value),
            'reduceRight': lambda: str(self._wrapped_value),
            'reverse': lambda: self._wrapped_value.reverse(),
            'shift': lambda: str(self._wrapped_value),
            'slice': lambda: str(self._wrapped_value),
            'some': lambda: str(self._wrapped_value),
            'sort': lambda: self._wrapped_value.sort(),
            'splice': lambda: str(self._wrapped_value),
            'toLocaleString': lambda: str(self._wrapped_value),
            'toSource': lambda: str(self._wrapped_value),
            'toString': lambda: str(self._wrapped_value),
            'unshift': lambda: str(self._wrapped_value),
            'values': lambda: str(self._wrapped_value),
        })
        return mapping


""" PUBLIC API """


class PolyglotAdapterError(Exception):
    pass


def as_js(value, extended_behavior=None):
    if isinstance(value, list):
        return _JavaScriptListAdapter(
            value, extended_behavior=extended_behavior)
    else:
        return _JavaScriptObjectAdapter(
            value, extended_behavior=extended_behavior)


def as_ruby(value, extended_behavior=None):
    return _RubyObjectAdapter(value, extended_behavior=extended_behavior)


# from collections.abc import Iterable
#
# def as_python(value):
#     if isinstance(value, Iterable):
#         return [as_python(x) for x in value]
#     else:
#         return x
