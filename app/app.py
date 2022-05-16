from flask import Flask, request, render_template
import yt_dlp
import os
import unidecode
from threading import Thread
from threading import active_count


app = Flask(__name__)
global background_thread
def download_video_mp3(url,folder):
    path = folder + '%(title)s' + '.%(ext)s'
    if folder!='/youtube_audios/':
        album=folder.split('/')[2]
    else:
        album="youtube"
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
            process_1=active_count()
            background_thread = Thread(target=download_video_mp3, kwargs={"url": url, "folder": path_exit})
            background_thread.start()
            process_2=active_count()
            # download_video_mp3(url,path)
            return render_template('loading.html', p_1=process_1, p_2=process_2, p_s="DESCARGANDO." )
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/loading/', methods = ['GET'])
def loading():
    process_string = request.args.get('ps') + "."
    return render_template('loading.html', p_1=request.args.get('p1'), p_2=active_count(), p_s=process_string )    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
