# automate_ja.py
# ================================================
# directories
# ================================================
destination = '/home/vangogh/Downloads'
# destination = '/media/vanhs/084ad0f6-fe03-4469-aa8f-a69b6e9ec3ad/home/vangogh/Downloads'
server_path = '/var/www/html/dev'
video_path = '/home/vangogh/Downloads/Video'
# video_path = '/media/vanhs/084ad0f6-fe03-4469-aa8f-a69b6e9ec3ad/home/vangogh/Downloads/Video'

render_folder = 'render-to-mp3'
rename_folder = 'renamed-folder'

# ================================================
# words, formats
# ================================================
unwanted_words = ['for', 'trunk', 'v', 'pkg', 'stable', 'update', 'package', 'j2s']
wanted_formats = ['.jpg', '.jpeg', '.png', '.heic', '.mp4', '.mkv', '.mp3', '.zip']

video_formats = ['.mkv']  # , '.ts', '.mp4', '.mov', '.webm']  # , '.wmv', '.flv', '.avi']
mp3_unwanted_words = {'ytb', 'youtube', 'hd', 'official', 'best', 'full', 'album', 'albums', 'greatest', 'hit', 'music', 'video', 'mv'}

# ================================================
# credentials
# ================================================
host = 'localhost'
db_username = 'vangogh'
db_password = '#vanhs@xyz'
facl_user = 'vangogh'