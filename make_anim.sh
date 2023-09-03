#!/usr/bin/bash

set -e
SCENES=("LinRegIntro" "LinRegTask" "LinRegMain")
LIST_FILE="vid_list.txt"

manim -qh main.py "${SCENES[@]}"
OUT=""
for SCENE in "${SCENES[@]}"
do
    OUT+="file 'media/videos/main/1080p60/$SCENE.mp4'\n"
done
echo -e $OUT > $LIST_FILE
ffmpeg -f concat -safe 0 -i $LIST_FILE -c copy out.mp4
