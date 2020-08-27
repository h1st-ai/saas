#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [ -f "$DIR/.env" ]; then
    set -a
    . "$DIR/.env"
    set +a
fi

# virtualenv
if [ -f "$DIR/venv" ]; then
    export PATH=$DIR/venv/bin:$PATH
fi

export PORT=${PORT-8999}
export ENVIRONMENT=${ENVIRONMENT:-"development"}

if [[ "$ENVIRONMENT" == "production" ]]; then
    exec gunicorn -w 4 -b "0.0.0.0:$PORT" --log-level info --access-logfile - server:app 2>&1
else
    FLASK_ENV=development FLASK_APP=server.py exec python -m flask run --port $PORT
fi
