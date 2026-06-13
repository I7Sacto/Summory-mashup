"Промт для відображення прогрес бар відсотків та таймаута"
progress_file="/tmp/progress.txt"

show_progress() {
    local p=0
    [ -f "$progress_file" ] && p=$(cat "$progress_file")
    printf "Progress:%s%%" "$p"
}

show_timeout() {
    if [[ -f /var/tmp/prompt_timeout.txt ]]; then
        cat /var/tmp/prompt_timeout.txt
    else
        printf "Time: N/A"
    fi
}

PS1='\[\e[38;2;255;255;255m\e[48;2;20;50;110m\]$(show_timeout) \[\e[0m\]'\
'\[\e[38;2;255;255;255m\e[48;2;140;40;110m\]$(show_progress) \[\e[0m\]'\
'\[\e[38;2;255;255;255m\e[48;2;20;50;110m\][\u@\h \W]\[\e[0m\] \$ '
