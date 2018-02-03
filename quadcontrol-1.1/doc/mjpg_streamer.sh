
#/opt/mjpg-streamer/mjpg-streamer-experimental/mjpg_streamer -i "input_raspicam.so -fps 15 -q 50 -x 640 -y 480" -o "output_http.so -p 9000 -w /opt/mjpg-streamer/www" > /dev/null 2>&1&

LD_LIBRARY_PATH=/opt/mjpg-streamer/mjpg-streamer-experimental/ /opt/mjpg-streamer/mjpg-streamer-experimental/mjpg_streamer -i "input_raspicam.so -fps 15 -q 50 -x 640 -y 480" -o "output_http.so -p 9000 -w /opt/mjpg-streamer/www">/dev/null 2>&1  &

