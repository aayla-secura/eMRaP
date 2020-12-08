import sys
sys.path.append('..')
from emrap.common import Searchable
from emrap.extracts import OrderedExtracts, \
    ExtractDirectives, ExtractDirectivesContainer

from emrap import setup_logger


setup_logger(3)


SOURCE_TEXT_A = '''A Title with Some Words of Various CaSeS'''
SOURCE_TEXT_B = '''Foo Bar'''

TARGET_TEXT = ('1: {%test%} 2: {%test_2%} 1: {%test_1%} '
               '3: {%test_3%} 40: {%test_40%}')


class Source(Searchable):
    _extract_type = OrderedExtracts

    def __init__(self, data):
        self.data = data


ed = ExtractDirectives(name='test',
                       where='data',
                       regex='([A-Z])([\w]+)',
                       regex_flags='',
                       regex_group=1,
                       default='?')

sourceA = Source(SOURCE_TEXT_A)
sourceB = Source(SOURCE_TEXT_B)
res = ed.apply(TARGET_TEXT, sourceB, sourceA)
print(res)
assert res == '1: F 2: B 1: F 3: T 40: ?'

res = ed.apply(TARGET_TEXT)
print(res)
assert res == '1: F 2: B 1: F 3: T 40: ?'

ed.extracts.clear()
res = ed.apply(TARGET_TEXT)
print(res)
assert res == '1: ? 2: ? 1: ? 3: ? 40: ?'

ed.search_sources(sourceA)
res = ed.apply(TARGET_TEXT)
print(res)
assert res == '1: T 2: S 1: T 3: W 40: ?'

ed.search_sources(sourceB)
res = ed.apply(TARGET_TEXT)
print(res)
assert res == '1: F 2: B 1: F 3: T 40: ?'

ed.search_sources(sourceA)
res = ed.apply(TARGET_TEXT)
print(res)
assert res == '1: T 2: S 1: T 3: W 40: ?'

res = ed.apply(TARGET_TEXT, only_found=True)
print(res)
assert res == '1: T 2: S 1: T 3: W 40: {%test_40%}'

ec = ExtractDirectivesContainer(
    dict(name='foo', stages='1', where='data', regex='bar'),
    dict(name='bar', stages='2', where='data', regex='foo'),
    dict(name='baz', stages='2,3', where='data', regex='foobar'))
print(ec)
assert len(ec) == 3
assert len(ec.get()) == 3
assert len(ec.get(stages='1')) == 1
assert len(ec.get(stages='2')) == 2
assert len(ec.get(stages='3')) == 1
assert len(ec.get(stages='1,2')) == 3
assert len(ec.get(stages='2,3')) == 2
