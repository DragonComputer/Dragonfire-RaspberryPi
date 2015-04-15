#sudo apt-get install vlc-nox

cvlc v4l2:///dev/video0 --sout '#transcode{vcodec=x264{keyint=60,idrint=2},vcodec=h264,vb=200,ab=32,fps=25,width=1280,height=720,acodec=mp3,samplerate=44100}:duplicate{dst=std{access=http{mime=video/x-flv},mux=ffmpeg{mux=flv},dst=:8082/stream.flv}' &
