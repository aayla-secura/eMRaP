import sys
sys.path.append('..')
from collections import UserString
from emrap.common import Cacheable, Sortable, \
    SortedUniqueContainer, ReverseOrderedContainer, \
    ReverseOrderedUniqueContainer

class C(Cacheable):
    _holds = list

class S(Sortable, UserString):
    @property
    def _comparables(self):
        return (len(self.data), self.data)

class SUC(SortedUniqueContainer):
    _holds = S


class RUC(ReverseOrderedUniqueContainer):
    _holds = int

class RC(ReverseOrderedContainer):
    _holds = int


c = C()
prev_ts = c.new_cache('foo')
c.new_cache('bar')
ts = c.add_cache_item('foo', 'bar')
assert ts > prev_ts
assert c['foo'] == ['bar']
prev_ts = ts
ts = c.add_cache_item('foo', 'baz')
assert ts > prev_ts
assert c['foo'] == ['bar', 'baz']
prev_ts = ts
ts = c.reset_cache('foo')
assert ts > prev_ts
assert c['foo'] == []
assert list(c) == ['foo', 'bar']
assert 'foo' in c
assert 'foobar' not in c

suc = SUC()
suc.new('foobar')
suc.new('foo')
suc.new('bar')
suc.new('foo')
suc.add(S('baz'))
assert [s.data for s in suc] == ['bar', 'baz', 'foo', 'foobar']

rc = RC()
rc.add(1)
rc.add(2)
rc.extend([3, 4])
rc += [5, 6]
rc.add(1)
assert list(rc) == [1, 5, 6, 3, 4, 2, 1]

ruc = RUC()
ruc.add(1)
ruc.add(2)
ruc.extend([3, 4])
ruc += [5, 6]
ruc.add(1)
assert list(ruc) == [1, 5, 6, 3, 4, 2]
