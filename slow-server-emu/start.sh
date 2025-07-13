#!/usr/bin/env bash
set -eu -o pipefail -x
cd "$(dirname "$0")"
engine="${ENGINE:-docker}"

"$engine" start slow-server
ip=$("$engine" inspect --format '{{.NetworkSettings.IPAddress}}' slow-server)
sed -i '/ slow-server$/d' /etc/hosts
echo "$ip slow-server" >>/etc/hosts