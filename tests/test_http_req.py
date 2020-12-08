import sys
sys.path.append('..')
import sys
import socket
from requests.exceptions import ReadTimeout

from emrap.http import HttpRequest, HttpRequestRaw
from emrap import setup_logger

setup_logger(3)
TIMEOUT = 1

CONTENT = b'''POST /?q=foo#hash HTTP/1.1
Host: localhost:50001
Content-Length: 20
X-Foo: foo

bazfoobar
----------
'''

CONTENT_LEN_NONE = b'''POST /?q=foo#hash HTTP/1.1
Host: localhost:50001
X-Foo: foo

bazfoobar
----------
'''

CONTENT_LEN_SHORT = b'''POST /?q=foo#hash HTTP/1.1
Host: localhost:50001
Content-Length: 10
X-Foo: foo

bazfoobar
----------
'''

CONTENT_LEN_LONG = b'''POST /?q=foo#hash HTTP/1.1
Host: localhost:50001
Content-Length: 100
X-Foo: foo

bazfoobar
----------
'''

CONTENT_G = b'''GET /?q=google HTTP/1.1
Host: www.google.com

'''

CONTENT_SA = b'''GET / HTTP/1.1
Host: foo:443

'''
CONTENT_SB = b'''GET / HTTP/1.1
Host: foo:8443

'''
CONTENT_PA = b'''GET / HTTP/1.1
Host: foo

'''
CONTENT_PB = b'''GET / HTTP/1.1
Host: foo:8080

'''
hreq = HttpRequestRaw(CONTENT_SA)
assert hreq.origin == 'https://foo:443'
assert hreq.is_ssl
assert hreq.port == 443
assert hreq.hostname == 'foo'

hreq = HttpRequestRaw(CONTENT_SA, is_ssl=False)
assert hreq.origin == 'http://foo:443'
assert not hreq.is_ssl
assert hreq.port == 443
assert hreq.hostname == 'foo'

hreq = HttpRequestRaw(CONTENT_SA, origin='//foo:80')
assert hreq.origin == 'http://foo:80'
assert not hreq.is_ssl
assert hreq.port == 80
assert hreq.hostname == 'foo'


hreq = HttpRequestRaw(CONTENT_SB)
assert hreq.origin == 'https://foo:8443'
assert hreq.is_ssl
assert hreq.port == 8443
assert hreq.hostname == 'foo'

hreq = HttpRequestRaw(CONTENT_SB, is_ssl=False)
assert hreq.origin == 'http://foo:8443'
assert not hreq.is_ssl
assert hreq.port == 8443
assert hreq.hostname == 'foo'

hreq = HttpRequestRaw(CONTENT_SB, origin='//foo:80')
assert hreq.origin == 'http://foo:80'
assert not hreq.is_ssl
assert hreq.port == 80
assert hreq.hostname == 'foo'


hreq = HttpRequestRaw(CONTENT_PA)
assert hreq.origin == 'http://foo'
assert not hreq.is_ssl
assert hreq.port == 80
assert hreq.hostname == 'foo'

hreq = HttpRequestRaw(CONTENT_PA, is_ssl=True)
assert hreq.origin == 'https://foo'
assert hreq.is_ssl
assert hreq.port == 443
assert hreq.hostname == 'foo'

hreq = HttpRequestRaw(CONTENT_PA, origin='//foo:80')
assert hreq.origin == 'http://foo:80'
assert not hreq.is_ssl
assert hreq.port == 80
assert hreq.hostname == 'foo'


hreq = HttpRequestRaw(CONTENT_PB)
assert hreq.origin == 'http://foo:8080'
assert not hreq.is_ssl
assert hreq.port == 8080
assert hreq.hostname == 'foo'

hreq = HttpRequestRaw(CONTENT_PB, is_ssl=True)
assert hreq.origin == 'https://foo:8080'
assert hreq.is_ssl
assert hreq.port == 8080
assert hreq.hostname == 'foo'

hreq = HttpRequestRaw(CONTENT_PB, origin='//foo:80')
assert hreq.origin == 'http://foo:80'
assert not hreq.is_ssl
assert hreq.port == 80
assert hreq.hostname == 'foo'


print('~~~~~~~~~~ HttpRequestRaw G0 ~~~~~~~~~~')
hreq = HttpRequestRaw(CONTENT_G, timeout=TIMEOUT)
assert hreq.origin == 'http://www.google.com'
assert hreq.host == 'www.google.com'
assert hreq.port == 80
assert not hreq.is_ssl
resp = hreq.send()
print(resp.search(b'https?://[a-z0-9_.-]+', regex_flags='i'))

print('~~~~~~~~~~ HttpRequestRaw G1 ~~~~~~~~~~')
hreq = HttpRequestRaw(CONTENT_G, origin='https://google.com', timeout=TIMEOUT)
assert hreq.origin == 'https://google.com'
assert hreq.host == 'google.com'
assert hreq.port == 443
assert hreq.is_ssl
resp = hreq.send()

print('~~~~~~~~~~ HttpRequestRaw G3 ~~~~~~~~~~')
hreq = HttpRequestRaw(CONTENT_G, is_ssl=True, timeout=TIMEOUT)
assert hreq.origin == 'https://www.google.com'
assert hreq.host == 'www.google.com'
assert hreq.port == 443
assert hreq.is_ssl
resp = hreq.send()

print('~~~~~~~~~~ HttpRequestRaw L1 ~~~~~~~~~~')
hreq = HttpRequestRaw(CONTENT, timeout=TIMEOUT)
assert hreq.origin == 'http://localhost:50001'
assert hreq.hostname == 'localhost'
assert hreq.host == 'localhost:50001'
assert hreq.port == 50001
assert not hreq.is_ssl
try:
    resp = hreq.send()
except (socket.timeout, ConnectionRefusedError):
    pass


print('~~~~~~~~~~ HttpRequestRaw L2 ~~~~~~~~~~')
hreq = HttpRequestRaw(CONTENT,
                      origin='http://localhost:50002',
                      timeout=TIMEOUT)
assert hreq.origin == 'http://localhost:50002'
assert hreq.hostname == 'localhost'
assert hreq.host == 'localhost:50002'
assert hreq.port == 50002
assert not hreq.is_ssl
try:
    resp = hreq.send()
except (socket.timeout, ConnectionRefusedError):
    pass

print('~~~~~~~~~~ HttpRequest G1 ~~~~~~~~~~')
hreq = HttpRequest(CONTENT_G, timeout=TIMEOUT)
assert hreq.origin == 'http://www.google.com'
assert hreq.port == 80
assert not hreq.is_ssl
resp = hreq.send()


print('~~~~~~~~~~ HttpRequest G2 ~~~~~~~~~~')
hreq = HttpRequest(CONTENT_G, origin='https://google.com', timeout=TIMEOUT)
assert hreq.origin == 'https://google.com'
assert hreq.host == 'google.com'
assert hreq.port == 443
assert hreq.is_ssl
resp = hreq.send()


print('~~~~~~~~~~ HttpRequest G3 ~~~~~~~~~~')
hreq = HttpRequest(CONTENT_G, is_ssl=True, timeout=TIMEOUT)
assert hreq.origin == 'https://www.google.com'
assert hreq.host == 'www.google.com'
assert hreq.port == 443
assert hreq.is_ssl
resp = hreq.send()

print('~~~~~~~~~~ HttpRequest L1 ~~~~~~~~~~')
hreq = HttpRequest(CONTENT, timeout=TIMEOUT)
assert hreq.origin == 'http://localhost:50001'
assert hreq.hostname == 'localhost'
assert hreq.host == 'localhost:50001'
assert hreq.port == 50001
assert not hreq.is_ssl
assert hreq.base_href == '/?q=foo#hash'
hreq.hash = None
assert hreq.base_href == '/?q=foo'
try:
    resp = hreq.send()
except (ReadTimeout, socket.timeout, ConnectionRefusedError):
    pass


print('~~~~~~~~~~ HttpRequest L2 ~~~~~~~~~~')
hreq = HttpRequest(CONTENT, origin='http://localhost:50002', timeout=TIMEOUT)
assert hreq.origin == 'http://localhost:50002'
assert hreq.hostname == 'localhost'
assert hreq.host == 'localhost:50002'
assert hreq.port == 50002
assert not hreq.is_ssl
try:
    resp = hreq.send()
except (ReadTimeout, socket.timeout, ConnectionRefusedError):
    pass

print('~~~~~~~~~~ HttpRequest LLONG ~~~~~~~~~~')
hreq = HttpRequest(CONTENT_LEN_LONG, timeout=TIMEOUT)
assert hreq.headers['Content-Length'] == str(21)
assert len(hreq.content) == 21
assert hreq.raw == CONTENT_LEN_LONG
try:
    resp = hreq.send()
except (ReadTimeout, socket.timeout, ConnectionRefusedError):
    pass

print('~~~~~~~~~~ HttpRequestRaw LLONG ~~~~~~~~~~')
hreq = HttpRequestRaw(CONTENT_LEN_LONG, timeout=TIMEOUT)
assert hreq.headers['Content-Length'] == str(21)
assert len(hreq.content) == 21
assert hreq.raw == CONTENT_LEN_LONG
try:
    resp = hreq.send()
except (ReadTimeout, socket.timeout, ConnectionRefusedError):
    pass

print('~~~~~~~~~~ HttpRequest LSHORT ~~~~~~~~~~')
hreq = HttpRequest(CONTENT_LEN_SHORT, timeout=TIMEOUT)
assert hreq.headers['Content-Length'] == str(10)
assert len(hreq.content) == 10
assert hreq.raw == CONTENT_LEN_SHORT
try:
    resp = hreq.send()
except (ReadTimeout, socket.timeout, ConnectionRefusedError):
    pass

print('~~~~~~~~~~ HttpRequestRaw LSHORT ~~~~~~~~~~')
hreq = HttpRequestRaw(CONTENT_LEN_SHORT, timeout=TIMEOUT)
assert hreq.headers['Content-Length'] == str(10)
assert len(hreq.content) == 10
assert hreq.raw == CONTENT_LEN_SHORT
try:
    resp = hreq.send()
except (ReadTimeout, socket.timeout, ConnectionRefusedError):
    pass

print('~~~~~~~~~~ HttpRequest LNONE ~~~~~~~~~~')
hreq = HttpRequest(CONTENT_LEN_NONE, timeout=TIMEOUT)
assert hreq.headers['Content-Length'] == str(0)
assert len(hreq.content) == 0
assert hreq.raw == CONTENT_LEN_NONE
try:
    resp = hreq.send()
except (ReadTimeout, socket.timeout, ConnectionRefusedError):
    pass

print('~~~~~~~~~~ HttpRequestRaw LNONE ~~~~~~~~~~')
hreq = HttpRequestRaw(CONTENT_LEN_NONE, timeout=TIMEOUT)
assert hreq.headers['Content-Length'] == str(0)
assert len(hreq.content) == 0
assert hreq.raw == CONTENT_LEN_NONE
try:
    resp = hreq.send()
except (ReadTimeout, socket.timeout, ConnectionRefusedError):
    pass
