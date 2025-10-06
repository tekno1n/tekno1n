#!/data/data/com.termux/files/usr/bin/env bash
cd "$HOME/tekno1n" || exit 1
exec python -m http.server 8081 --bind 127.0.0.1
