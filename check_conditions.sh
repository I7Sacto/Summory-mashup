!/bin/bash

RESULT=$(cat /tmp/progress.txt)
NAME=$(cat /etc/mashup_user.txt)
EMAIL="annavorobey393@gmail.com"
TIMELEFT_SEC=$(cat /var/tmp/session_timeout.txt)   # залишок часу у хвилинах
TIMELEFT=$(( TIMELEFT_SEC /60 ))

# Умова 1: якщо результат = 100%
if [ "$RESULT" -eq 100 ]; then
    /usr/local/bin/end_mashup.sh "$RESULT" "$NAME" "$EMAIL"
    crontab -l | grep -v "/usr/local/bin/check_conditions.sh" | crontab -
fi

# Умова 2: якщо залишилося <= 5 хвилин
if [ "$TIMELEFT" -le 5 ]; then
    wall "УВАГА! До завершення сесії залишилося $TIMELEFT хвилин "
    /usr/local/bin/end_mashup.sh "$RESULT" "$NAME" "$EMAIL"
fi

if [ "$TIMELEFT" -eq 0 ]; then
    wall "Сессія мешапа закінчилась!!!"
    rm -rf /etc/mashup_user.txt
    crontab -l | grep -v "/usr/local/bin/check_conditions.sh" | crontab -
    /sbin/shutdown -h now
fi
