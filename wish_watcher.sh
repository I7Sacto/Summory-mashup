#!/bin/bash

while true; do
    PROGRESS=$(cat /tmp/progress.txt 2>/dev/null)

    if [ "$PROGRESS" = "100" ]; then

        for tty in $(who | awk '{print $2}'); do
            {
                echo -e "\033[2J\033[H"
                cat /usr/bin/wish.md
            } > "/dev/$tty"
        done

        exit 0
    fi

    sleep 10
done
