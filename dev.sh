#!/bin/bash
trap 'kill 0' EXIT

(cd client_web && python3 -m http.server 8000) &
(cd backoffice && python3 app.py) &

wait
