from flask import Flask, request, render_template
import yt_dlp
import os
import unidecode
from mutagen.mp4 import MP4

app = Flask(__name__)

folder_base="youtube_audios"

def download_video_mp3(url,folder):
    folder1 = folder
    path = folder1 + '%(title)s' + '.%(ext)s'
    ydl_opts = {
        'outtmpl': path, 
        'format': 'm4a/bestaudio/best',
        'ignoreerrors': True,
        'writethumbnail': True,
        # 'postprocessor_args': ['-metadata', "album= '%(title)s'"],    
        'postprocessors': [{ 
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            },
            {'key': 'EmbedThumbnail'},
            {'key': 'FFmpegMetadata'},
            ],
        }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        ydl.download(url)
        print("----------------")
        name=info['title'].replace("|", "_")
        folder2 = folder
        path2 = folder2 + name + '.'+info['ext'] 
        if "audiobooks" in folder: 
            folder2 = folder  + name + "/" 
            os.makedirs(folder2)
            os.chown(folder2, 1000, 1000) 
            new_path2 = folder2 + name + '.'+info['ext']  
            os.rename(path2, new_path2)
            path2=new_path2

        tags = MP4(path2)
        album=tags['©ART'][0]
        if "audiobooks" in folder: 
            album=tags['©nam'][0] 
        tags['\xa9alb'] = f"{album}"
        tags.save()    



@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == "POST":
        data = request.form
        folder = data['folder'] if 'folder' in data else None
        url = data['url'] if 'url' in data else None
        type_sound = data['type_sound'] if 'type_sound' in data else None
        path_exit=f"/{folder_base}/{type_sound}/"
        if url:
            if folder:
                folder = unidecode.unidecode(folder).replace(" ", "_")
                folder= path_exit + folder
                if not os.path.exists(folder):
                   os.makedirs(folder)
                   os.chown(folder, 1000, 1000)
                   path_exit=folder+"/"
            download_video_mp3(url,path_exit)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
