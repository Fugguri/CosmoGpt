#!/bin/bash

set -e

exec python3 main.py &
exec python3 server.py 