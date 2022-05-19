from flask import Flask, request, render_template
import yt_dlp
import os
import unidecode


app = Flask(__name__)
global background_thread
def download_video_mp3(url,folder):
    path = folder + '%(title)s' + '.%(ext)s'
    if folder!='/youtube_audios/':
        album=folder.split('/')[2]
    else:
        album="%(author)s"
    ydl_opts = {
        'outtmpl': path, 
        'format': 'm4a/bestaudio/best',
        'ignoreerrors': True,
        'writethumbnail': True,
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            },
            {'key': 'EmbedThumbnail'},
            {'key': 'FFmpegMetadata'},
            ],
        'postprocessor_args': ['-metadata', 'album='+album]    
        }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
    



@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == "POST":
        data = request.form
        print(data)
        folder = data['folder'] if 'folder' in data else None
        url = data['url'] if 'url' in data else None
        path_exit='/youtube_audios/'
        if url:
            if folder:
                folder = unidecode.unidecode(folder).replace(" ", "_")
                folder=f'/youtube_audios/'+folder
                if not os.path.exists(folder):
                   os.makedirs(folder)
                   os.chown(folder, 1000, 1000)
                   path_exit=folder+"/"
            download_video_mp3(url,path_exit)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
