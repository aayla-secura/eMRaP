#!/bin/bash

./demo.py \
  -c credentials.json \
  -t token.pickle \
  -C cache.pickle \
  -E name:cookie regex:'Set-Cookie: ([^\r\n]*)' regex_group:1 regex_flags:'I' stages:pre,post where:raw_headers default:'Foo=bar' \
  -E name:token regex:'token: ([a-zA-Z0-9]{16})' regex_group:1 stages:post where:content default:'' \
  -E name:from_domain regex:'.+@([a-zA-Z0-9._-]+)' regex_group:1 stages:fetch where:from_address default:'localhost' \
  --latest \
  -O http://localhost:50001 \
  --pre-search pre_request.txt \
  --post-search post_request.txt \
  --repeat 2 \
  -o - \
  "${@}"
