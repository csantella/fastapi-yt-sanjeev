#!/bin/bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $SCRIPTDIR
export GIT_COMMIT_HASH=$(git rev-parse --short HEAD)

if [ -z $BUILD_TYPE]; then
  BUILD_TYPE='dev'
fi

DEVTAG=""

if [[ "$BUILD_TYPE" != "release" ]]; then
  DEVTAG="_${BUILD_TYPE}_${GIT_COMMIT_HASH}.d$(date +"%Y%m%d")"
fi

VERSION="$(grep '^version =' pyproject.toml | cut -d '"' -f 2)$DEVTAG"

echo "__version__ = $VERSION" > $SCRIPTDIR/api/_version.py

#python -c "from api.version import get_version; open('api/_version.py', 'w').write(f'__version__ = \"{get_version()}\"')"
docker compose build
if [[ $? -ne 0 ]]; then
  echo "ERROR: Docker Compose Build failed."
fi

exit 0
