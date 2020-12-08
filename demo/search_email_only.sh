#!/bin/bash

./demo.py \
  -c credentials.json \
  -t token.pickle \
  -C cache.pickle \
  -E name:from regex:'[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+' stages:fetch where:from_address default:'unknown' \
  -E name:subject regex:'.+' stages:fetch where:subject default:'' \
  --latest \
  -o - \
  "${@}"
