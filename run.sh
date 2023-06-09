#!/bin/zsh

tmux new-session -d
tmux send-keys 'cd lab_meeting_notifier/' C-m
tmux send-keys 'python send.py &' C-m