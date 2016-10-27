#! /usr/bin/env python3
#
# Copyright (c) 2016, Gabriel Linder <linder.gabriel@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#

import os
import json
import requests

# ~/.private_token.json
# {
#         "proto": "http(s)",
#         "host": "DAT_HOST",
#         "version": "DAT_VERSION",
#         "token": "DAT_TOKEN",
#         "ignore": [
#                 "path_A/repo_A",
#                 "path_A/repo_B",
#                 "path_X/repo_Z"
#         ],
#         "wiki": [
#                 "path_A/repo_A",
#                 "path_A/repo_B",
#                 "path_X/repo_Z"
#         ]
# }
# To get a token, go to /profile/account on your gitlab host.

with open(os.path.expanduser('~/.private_token.json')) as fd:
    conf = json.load(fd)

proto = conf['proto']
host = conf['host']
version = conf['version']
token = conf['token']
ignore = conf['ignore']
wiki = conf['wiki']

url = '{}://{}/api/{}/projects?private_token={}'.format(proto, host,
                                                        version, token)

while url is not None:

    req = requests.get(url)
    req.raise_for_status()
    rep = req.json()

    for r in rep:
        path = r['path_with_namespace']
        if path not in ignore:
            print('{}'.format(path))
            if path in wiki and r['wiki_enabled']:
                print('{}.wiki'.format(path))

    url = None
    for l in req.links:
        if l == 'next':
            url = req.links[l]['url']
            break
