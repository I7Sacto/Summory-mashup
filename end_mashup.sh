#!/bin/bash

RESULT=$(cat /tmp/progress.txt 2>/dev/null)
NAME=$(cat /etc/mashup_user.txt 2>/dev/null)
TIME_LEFT=$(cat /var/tmp/session_timeout.txt 2>/dev/null)
HOURS=$((TIME_LEFT / 3600))
MINUTES=$(((TIME_LEFT % 3600) / 60))
SECONDS=$((TIME_LEFT % 60))

TIME_FORMATTED=$(printf "%02d:%02d:%02d" "$HOURS" "$MINUTES" "$SECONDS")

EMAIL="annavorobey393@gmail.com"

cat <<EOF | sendmail "$EMAIL"
Subject: Звіт про проходження завдання
To: $EMAIL
Content-Type: text/plain; charset=UTF-8

Користувач: $NAME

Прогрес: $RESULT%

Час сесії: $TIME_FORMATTED

Дата: $(date '+%d.%m.%Y %H:%M:%S')
EOF

