import os
import datetime
import yt_dlp
from moviepy.editor import VideoFileClip

def download_video(url, file_format, title):
    today = datetime.datetime.today().strftime("%d-%m-%Y")
    folder_name = f"{today}-{title}"
    output_folder = os.path.join(os.getcwd(), folder_name)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ydl_opts = {
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'noplaylist': True
    }

    if file_format == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
    elif file_format in ['mp4', 'gif']:
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'merge_output_format': 'mp4'
        })
    else:
        print("Format not supported. Use 'mp3', 'mp4' or 'gif'.")
        return

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_title = info_dict.get('title', 'Unknown Title')
        video_filename = ydl.prepare_filename(info_dict)

    if file_format == 'gif' and video_filename.endswith(".mp4"):
        gif_filename = video_filename.replace(".mp4", ".gif")
        try:
            clip = VideoFileClip(video_filename)
            clip.write_gif(gif_filename, fps=10)
            clip.close()
            os.remove(video_filename)
        except Exception as e:
            print(f"Error converting {video_filename} to GIF: {e}")

    print(f"{video_title} : Download completed! Files saved in: {output_folder}")

urls = [
    "",
]

for url in urls:
    download_video(url, "mp3", "Title")
