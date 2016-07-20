#!/bin/bash

set -e

ARCHIVE=elk-butler.tar.bz2

pushd ../

[ ! -e elk-butler/releases ] && mkdir releases
[ -e elk-butler/releases/$ARCHIVE ] && rm elk-butler/releases/$ARCHIVE

echo "working dir: $(pwd)"
tar --exclude=releases --exclude=logs --exclude=.idea \
 --exclude=.cache --exclude=.env --exclude=.git* \
 -cvjf elk-butler/releases/$ARCHIVE elk-butler
popd
