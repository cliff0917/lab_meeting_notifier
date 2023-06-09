#!/bin/zsh

ps -ef | grep send.py | awk '{print $2}' | xargs kill -9 2> /dev/null
tmux kill-server 2> /dev/null