if [ ! -d "_site-packages" ]; then
  docker run -d --name=yt_dlp manologcode/yt_dlp /bin/ash
  sleep 2
  docker cp yt_dlp:/usr/local/lib/python3.10/site-packages ./_site-packages
  docker rm -f yt_dlp
fi

docker run -it --rm \
--name=yt_dlp \
-e FLASK_APP=app.py \
-e FLASK_ENV=development \
-p 5000:5000 \
-v $PWD/_site-packages:/usr/local/lib/python3.10/site-packages \
-v $PWD/app:/app \
-v $PWD/youtube_audios:/youtube_audios \
manologcode/yt_dlp \
/bin/ash