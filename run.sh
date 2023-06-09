#!/bin/zsh

tmux new-session -d
tmux send-keys 'cd send_email/' C-m
tmux send-keys 'python send.py &' C-m