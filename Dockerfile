FROM python:3.10-alpine

RUN apk add --update --no-cache --virtual .build-deps gcc musl-dev \
&& pip install --upgrade pip \
&& apk add ffmpeg \
&& mkdir /youtube_audios \
&& chmod o+w /youtube_audios \
&& adduser -D yt-dlp
COPY ./app /app
RUN chown -R 1000:1000 /app 
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements.txt
RUN rm -rf ~/.cache/pip && apk del .build-deps 

USER yt-dlp
CMD ["gunicorn", "-b", "0.0.0.0:80", "wsgi:app"]