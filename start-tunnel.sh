#!/data/data/com.termux/files/usr/bin/env bash
cd "$HOME/tekno1n" || exit 1
mkdir -p logs
# Stream terus: simpan log mentah, dan setiap kali ada URL, tulis/overwrite ke ~/tunnel_url.txt
exec ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -o ServerAliveCountMax=2 \
  -R 80:localhost:8081 nokey@localhost.run 2>&1 \
  | stdbuf -oL tr -d '\r' \
  | tee logs/localhostrun.raw.log \
  | awk '
      match($0, /https:\/\/[A-Za-z0-9.-]+\.(lhr\.life|localhost\.run)/) {
        url = substr($0, RSTART, RLENGTH);
        system("printf \"" url "\" > " ENVIRON["HOME"] "/tunnel_url.txt");
        print "[URL] " url > "/dev/stderr";
      }
      { fflush(); }
    '
