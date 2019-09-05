import polyglot
from polyglot_adapters import as_js, as_ruby
from collections.abc import Iterable


js_func = polyglot.eval(language='js', string='(x) => x.toString()')

o = object()
assert js_func(as_js(o)) == str(o)


ruby_func = polyglot.eval(language='ruby', string='->(*args) { args.sort() }')

ruby_result = ruby_func(as_ruby([1, 3]), as_ruby([1, 2]), as_ruby([1, 4]))

assert [list(x) for x in ruby_result] == [[1, 2], [1, 3], [1, 4]]


def same_content(iterable1, iterable2):
    if len(iterable1) != len(iterable2):
        return False
    for value1, value2 in zip(iterable1, iterable2):
        if value1 != value2:
            if isinstance(value1, Iterable) and isinstance(value2, Iterable):
                return same_content(value1, value2)
            else:
                return False
    return True


assert same_content(ruby_result, [[1, 2], [1, 3], [1, 4]])

print('Polyglot adapters examples ran successfully!')
