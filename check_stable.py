#!/usr/bin/env python
# check_stable.py
#
# Retrieve latest stable version from static.rust-lang.org
# Compare the stable version to ensure we have a corresponding docker tag
#
# If we have not built it, print the version we need to build and exit 0
# If we have built it, exit 1

import urllib.request as urllib
import json
import toml
import sys

# Dockerhub repo to compare rust-lang release with
DOCKERHUB_REPO="clux/muslrust"

def rust_stable_version():
    """Retrieve the latest rust stable version from static.rust-lang.org"""
    url = 'https://static.rust-lang.org/dist/channel-rust-stable.toml'
    req = urllib.urlopen(url)
    data = toml.loads(req.read().decode("utf-8"))
    req.close()
    return data['pkg']['rust']['version'].split()[0]

def stable_tag_exists(stable_ver):
    """Retrieve our built tags and check we have built a given one"""
    url = f'https://registry.hub.docker.com/v1/repositories/{DOCKERHUB_REPO}/tags'
    req = urllib.urlopen(url)
    data = json.loads(req.read())
    req.close()
    for x in data:
        if x['name'] == stable_ver:
            return True
    return False


if __name__ == '__main__':
    latest_stable = rust_stable_version()
    tag = f'{latest_stable}-stable'
    exists = stable_tag_exists(tag)
    if not exists:
        print(latest_stable)
        sys.exit(0)
    else:
        sys.exit(1)
