#!/bin/bash

USER_FILE="/etc/mashup_user.txt"
PROGRESS_FILE="/var/tmp/progress.txt"
ADMIN_EMAIL="annavorobey393@gmail.com"
TIMEOUT_FILE="/var/tmp/session_timeout.txt"

USER_INFO=$(cat "$USER_FILE" 2>/dev/null)
PROGRESS=$(cat "$PROGRESS_FILE" 2>/dev/null)

SERVICE="mashup.service"

# Умова 1: якщо 100% → надсилаємо результат, але НЕ вимикаємо VM
if grep -q "100" "$PROGRESS_FILE"; then
    echo "Учасник: $USER_INFO, результат: $PROGRESS" \
    | mail -s "Mashup результати (100%)" "$ADMIN_EMAIL"
   systemctl stop "$SERVICE"
   systemctl disable "$SERVICE"
fi

# Умова 2: таймер доходить до нуля → надсилаємо результат і вимикаємо VM
if [[ -f "$TIMEOUT_FILE" ]]; then
    remaining=$(< "$TIMEOUT_FILE")

    if (( remaining <= 60 )); then
        echo "Учасник: $USER_INFO, результат: $PROGRESS" \
        | mail -s "Mashup результати (таймаут)" "$ADMIN_EMAIL"
        systemctl stop "$SERVICE"
        systemctl disable "$SERVICE"
fi
        # Оновлюємо залишок і час старту
        remaining=$(( remaining - 1 ))
        echo "$remaining" > "$TIMEOUT_FILE"
fi
