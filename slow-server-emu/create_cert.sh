#!/usr/bin/env bash
set -eu -o pipefail -x
cd "$(dirname "$0")"

mkcert -key-file key.pem -cert-file cert.pem slow-server
echo "Note: You will need to run mkcert -install to install the CA in your browsers."
