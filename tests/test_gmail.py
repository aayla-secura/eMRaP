import sys
sys.path.append('..')
import re
from time import time

from emrap import setup_logger
from emrap.gmail import Gmail

setup_logger(3)
QUERY = lambda in_last: '' if in_last is None else (
    ' after:{:.0f}'.format(time() - in_last))
REGEX = '/auth/reset-password/([a-f0-9]+)'
REGEX_GROUP = 1
CLIENT_CREDS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'

gmail = Gmail(CLIENT_CREDS_FILE, TOKEN_FILE)
msgs = gmail.fetch(id_range=1)

print('--------------------')
msgs = gmail.fetch(preferred_mime_type='text/plain',
                   query=QUERY(None),
                   id_range=1)
assert len(msgs) == 1
print('Time = {}'.format(msgs[0].time))
prev_ts = msgs[0].timestamp

print('--------------------')
msgs = gmail.fetch(preferred_mime_type='text/plain',
                   query=QUERY(None),
                   id_range=-1)
assert len(msgs) == 1
print('Time = {}'.format(msgs[0].time))
assert prev_ts > msgs[0].timestamp

print('--------------------')
msgs = gmail.fetch(preferred_mime_type='text/plain',
                   query=QUERY(None),
                   id_range=(-1, -5))
assert len(msgs) == 5

msg = msgs[0]
ex = msg.search('https?://[^ \r\n]+')
print(ex)

print('--------------------')
msgs = gmail.fetch(preferred_mime_type='text/plain',
                   query=QUERY(None),
                   id_range=(1, 10),
                   regex=REGEX,
                   regex_group=REGEX_GROUP,
                   regex_flags=re.I,
                   where=['body'])
for m in msgs:
    print(m.last_search)
