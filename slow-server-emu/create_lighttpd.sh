#!/usr/bin/env bash
set -eu -o pipefail -x
cd "$(dirname "$0")"
engine="${ENGINE:-docker}"

# Create sslkey.log if it doesn't exist.
# Give it the same ownership as this directory so that the repo doesn't get
# polluted with root-owned files.
if [[ ! -f sslkey.log ]]; then
  uid="$(stat . --format='%u')"
  gid="$(stat . --format='%g')"
  touch sslkey.log
  chown "$uid:$gid" sslkey.log
fi

"$engine" build -f lighttpd.Dockerfile . --tag slow-server
"$engine" rm -f slow-server || : 2>/dev/null
"$engine" create \
  -v ..:/var/www/html:ro \
  -v ./cert.pem:/cert.pem:ro \
  -v ./key.pem:/key.pem:ro \
  -v ./lighttpd.conf:/etc/lighttpd/conf.d/100-my.conf \
  --name slow-server \
  --hostname slow-server \
  --privileged \
  slow-server
./start.sh
