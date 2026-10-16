#!/bin/bash
# usage: encode.sh out.mp4 [ass]
OUT=$1; ASS=$2
VF="[0:v][1:v]xfade=transition=fade:duration=0.2:offset=145.766667,settb=1/30,setpts=N/30/TB"
[ -n "$ASS" ] && VF="$VF,ass=$ASS:fontsdir=/home/user/desi-store/edit/work/fonts"
VF="$VF,format=yuv420p[v]"
ffmpeg -v error -y -i A.mp4 -i B.mp4 -i song_norm.wav -filter_complex "$VF" -map "[v]" -map 2:a \
  -c:v libx264 -profile:v high -preset slow -crf 18 -pix_fmt yuv420p -r 30 -frames:v 7201 \
  -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUT" && echo "ENCODED $OUT"
