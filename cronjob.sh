#!/bin/bash
PATH=/home/pi/mt681-sml-ingest/myenv/bin:/home/pi/.autojump/bin:/home/pi/.autojump/bin:/home/pi/mt681-sml-ingest/myenv/bin:/home/pi/.autojump/bin:/home/pi/.autojump/bin:/home/pi/.cargo/bin:/usr/local/bin:/usr/bin:/bin:/usr/games
source /home/pi/mt681-sml-ingest/myenv/bin/activate
/home/pi/mt681-sml-ingest/myenv/bin/python /home/pi/mt681-sml-ingest/main.py
echo "Done"
