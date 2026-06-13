#!/bin/bash
SESSION="/var/tmp/session_timeout.txt"
OUTPUT="/var/tmp/prompt_timeout.txt"

# якщо файл порожній — 2 години
if [[ ! -s "$SESSION" ]]; then
    echo 7200 > "$SESSION"
fi
REM=$(<"$SESSION")
echo  "rem" $(( REM ))
while (( REM > 0 )); do
        printf "Time: %02d:%02d:%02d\n" \
            $((REM/3600)) $(((REM%3600)/60)) $((REM%60)) > "$OUTPUT"
        REM=$(( REM - 1 ))
        echo $(( REM )) > "$SESSION"
    sleep 1
done

rm $SESSION
