from polyglot_adapters import as_js, as_ruby

for x in [None, True, False, 1, 2, 3.4, (5, 6), [7, 8], {'a': 9}]:
    result = as_js(x).toString()
    expected = str(x)
    assert result == expected, '%s != %s' % (result, expected)

    result = as_ruby(x).to_s()
    # as_ruby(x)['empty?']()
    expected = str(x)
    assert result == expected, '%s != %s' % (result, expected)


py_list = [1, 2, 5, 4]
js_list = as_js(py_list)

assert js_list.indexOf(1) == 0, '%s != %s' % (js_list.indexOf(1), 0)
assert js_list.indexOf(5) == 2
assert js_list.indexOf(3) == -1

try:
    js_list.append(3)
    assert False, 'should not understand "append"'
except AttributeError:
    pass


def my_append(self, value):
    self.append(value)
    return value


js_list2 = as_js(py_list, extended_behavior={'my_append': my_append})

try:
    assert len(py_list) == 4, 'length not 4, but %s' % len(py_list)
    assert js_list2.my_append(3) == 3, 'my_append failed'
    assert len(py_list) == 5, 'length not 5, but %s' % len(py_list)
except AttributeError:
    assert False, 'should understand "my_append"'


class MyPolyMixin:
    def my_append(self, value):
        self.append(value)
        return value


js_list3 = as_js(py_list, extended_behavior=MyPolyMixin)

try:
    assert len(py_list) == 5, 'length not 5, but %s' % len(py_list)
    assert js_list3.my_append(42) == 42, 'my_append failed'
    assert len(py_list) == 6, 'length not 6, but %s' % len(py_list)
except AttributeError:
    assert False, 'should understand "my_append"'

print('All tests passed.')
