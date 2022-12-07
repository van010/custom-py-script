import os
import re
import datetime
import pymysql
import config as cfg
from zipfile import ZipFile
from time import sleep


current_path = os.getcwd()
destination = cfg.destination
server_path = cfg.server_path
unwanted_words = cfg.unwanted_words
host = cfg.host
username = cfg.db_username
password = cfg.db_password


def color(arg):
    colors = {
        'header': '\033[95m',
        'okblue': '\033[94m',
        'okcyan': '\033[96m',
        'okgreen': '\033[92m',
        'warning': '\033[93m',
        'fail': '\033[91m',
        'endc': '\033[0m',
        'bold': '\033[1m',
        'underline': '\033[4m',
        'normal': ''
    }
    return colors.get(arg, 'normal')


def get_all_compressed_files(path):
    if not check_path_exist(path): return
    all_files = os.listdir(path)
    compressed_files = {
        'zip': [],
        'jpa': [],
        'all': []
    }
    file_formats = list(compressed_files.keys())
    for format_ in file_formats:
        compressed_files[format_] = [file for file in all_files if format_ in file.lower()]
        compressed_files['all'] = [file for file in all_files]

    for file in all_files:
        if '.j01' in file:
            compressed_files['jpa'].append(file)

    return compressed_files


# get all file formats
# return array of formats
def get_formats(path, format_needed=''):
    if not check_path_exist(path): return
    all_treasures = os.listdir(path)
    all_files = [file for file in all_treasures if os.path.isfile(f'{path}/{file}')]
    all_folders = [folder for folder in all_treasures if os.path.isdir(f'{path}/{folder}')]
    all_formats = [format.split('.')[-1].lower() for format in all_files]
    all_formats = unique_list(all_formats)

    files_with_format = {}
    # get all files with specific format
    for format_ in all_formats:
        files_with_format[format_] = [file for file in all_files if format_ in file]
    if format_needed:
        return [all_formats, files_with_format]
    return all_formats


def check_path_exist(path):
    if not os.path.exists(path):
        msg('The Path not Exist! Kindly check again!', 'fail')
        return False
    return True


def unique_list(_list):
    return list(set(_list))


# get_formats('/home/vangogh/Downloads')
# get_all_compressed_files('/home/vangogh/Downloads')
# exit()


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    # else:
    #     print(f"========================================================")
    #     option = str(input(f'{color("warning")}Remove folder: {folder_name}?{color("endc")} y/n: '))
    #     if option == 'y':
    #         os.system(f"sudo rm -r {folder_name}")
    #         print(f"""{color('okgreen')}Removing success!{color('endc')}
    #         ========================================================
    #         """)
    #         sleep(.5)


def clear_special_chars(sentence, unwanted_words=[]):
    clean = re.compile('<.*?>')
    clear_html_tags = re.sub(clean, '', sentence)
    clear_html_tags = re.sub('[\@\#]\w+', ' ', clear_html_tags)
    clear_html_tags = re.sub('[\/\#]\w+', ' ', clear_html_tags)
    clear_special_char = re.sub('[^A-Za-z0-9]+', ' ', clear_html_tags)
    lower_word = ' '.join([word.lower() for word in clear_special_char.split(' ')]).strip()
    if unwanted_words:
        return ' '.join([word for word in lower_word.split(' ') if word not in unwanted_words]).strip()
    return lower_word


def remove_small_word(words, char):
    split_words = words.lower().split(' ')
    split_words = [ele for ele in split_words if ele not in unwanted_words]
    return char.join(split_words).strip()


def extract_zip(file, name_folder, file_type='zip'):
    """extract and create database"""
    to_path = ''

    if file_type == 'jpa':
        to_path = f"{server_path}/fix-bugs/fix/"
        path_to_extract = os.path.join(to_path, name_folder)
        create_folder(path_to_extract)
        for _file in file:
            os.system(f"cp -v {destination}/{_file} {path_to_extract}")
        os.system(f"cp -v {server_path}/fix-bugs/backup/kickstart/* {path_to_extract}")
        run_command(f"sudo -S chown -R www-data.vangogh {path_to_extract}/")
        if create_db('fixbugs_' + name_folder.replace('-', '_')):
            for _file in file:
                run_command(f"mv {destination}/{_file} {destination}/Compressed/site-user-backup/")
            show_ref(to_path, name_folder, 'jpa')
            print(f"""\nif catch the Error
            {color('warning')}Url not found on server{color('endc')}\n
            Backend > System > global config > Site > SEO > Search Engine Friendly URLs > NO
            Frontend > F12 > Network > Disable cache checks
            """)
        exit()
        # set other user permission to this folder
        # run_command(f"sudo -S setfacl -R -m u:vangogh:wxr {path_to_extract}/")

    if 'j3' in name_folder:
        to_path = f"{server_path}/j3-templates/"
    elif 'j4' in name_folder:
        to_path = f"{server_path}/j4-templates/"

    create_folder(os.path.join(to_path, name_folder))
    path_to_extract = os.path.join(to_path, name_folder)

    with ZipFile(f"{destination}/{file}", 'r') as zip_ref:
        print(f'Extracting files to {path_to_extract}/')
        zip_ref.printdir()
        try:
            zip_ref.extractall(path_to_extract)
        except RuntimeError as err:
            print(err)
    # set folder owner
    run_command(f"sudo -S chown -R www-data.vangogh {path_to_extract}/")
    # set other user permission to this folder
    run_command(f"sudo -S setfacl -R -m u:vangogh:wxr {path_to_extract}/")

    if create_db(name_folder.replace('-', '_')):
        run_command(f"mv {destination}/{file} {destination}/Compressed/Temps/")
        show_ref(to_path, name_folder)


def run_command(command):
    return os.system(command)


def show_ref(to_path, name_folder, file_type=''):
    if file_type == 'jpa':
        print(
            f"Local folder path: {color('okgreen')} {to_path}{name_folder}/ {color('endc')}")
        print(
            f"Installation link: {color('okgreen')} {to_path.replace('/var/www/html', host)}{name_folder}/kickstart.php {color('endc')}")
    else:
        print(
            f"Installation link: {color('okgreen')} {to_path.replace('/var/www/html', host)}{name_folder} {color('endc')}")
    print(f'Mysql: {color("okgreen")} {username} - {password} {color("endc")}')
    print(f'Site: {name_folder}.com\nAdmin: admin\nPassword: #bacclone@123 ')


def msg(message, type='success'):
    notify = {
        'success': color('okgreen'),
        'fail': color('fail'),
        'warning': color('warning'),
        'notice': color('header'),
        'end': color('endc'),
        'no': color('normal')
    }
    print(f"{notify[type]}{message}{notify['end']}")


def search_str_in_file(file_path, word, target_file='configuration.php'):
    if not os.path.isfile(os.path.join(file_path, target_file)): return False
    with open(os.path.join(file_path, 'configuration.php'), 'r') as file:
        lines = file.readlines()
        for line in lines:
            if word in line:
                return re.findall(r"'(\w+)'", line)[0]
    return False


# ================================================
# all main functions
# ================================================


def create_db(db_name):
    """create mysql db"""
    mydb = pymysql.connect(
        host=host,
        user=username,
        password=password
    )
    my_cursor = mydb.cursor()
    try:
        drop_db(db_name)
        my_cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db_name} COLLATE utf8mb4_unicode_ci')
        mydb.close()
        msg(f'Successfully Created db: {db_name}')
        return True
    except pymysql.connect.Error as err:
        msg(f'Something went wrong: {err}', 'fail')
        return False


def drop_db(db_name):
    mydb = pymysql.connect(
        host=host,
        user=username,
        password=password
    )
    my_cursor = mydb.cursor()
    query = f'DROP DATABASE IF EXISTS `{db_name}`;'

    try:
        my_cursor.execute(query)
        mydb.close()
        msg(f"Dropped db: {db_name}")
        return True
    except pymysql.connect.Error as err:
        msg(f'Something went wrong: {err}', 'fail')
        return False


def _exit(option):
    if option == 'n':
        msg('Good Bye!', 'notice')
        exit()


# the path to install site fixbug is wrong,
# it route to the j3-templates or j4-templates folder
def run_install_fixbug_site():
    jpa_files = get_all_compressed_files(destination)['jpa']
    # jpa_files = get_all_compressed_files(destination)['all']

    if len(jpa_files) == 0:
        print(f"{color('warning')}Nothing to Install!{color('endc')}")
        exit()

    print(f"{color('header')}All JPA files below: {color('endc')}")
    [msg(f"{i}. {jpa_files[i]}", 'no') for i in range(len(jpa_files))]

    msg("""
            + n or Empty: cancel
            + choose folders to DO!
            """, 'warning')

    _option = str(input('option: '))  # empty => delete all, if 0, 1 => keep
    _exit(_option)
    _option = [] if _option.strip() == '' else _option.split(' ')

    if len(_option) == 0: exit('Nothing to do!')

    try:
        name_folder = str(input(f'\n{color("okcyan")}Type folder name {color("endc")}: '))
        jpa_files_target = [jpa_files[int(opt)] for opt in _option]
        extract_zip(jpa_files_target, name_folder, 'jpa')
    except ValueError as err:
        print(f"{err}")


def remove_installed_sites(_name_folder):
    name_folder = _name_folder if _name_folder != '' else str(input('Type site folder: '))
    server_path = cfg.server_path
    # target_folder = [to_path + folder for folder in os.listdir(to_path) if name_folder in folder]
    target_folder = []
    paths = [f'{server_path}/j4-templates/', f'{server_path}/fix-bugs/fix/', f'{server_path}/j3-templates/']
    for path in paths:
        if not os.path.isdir(path):
            msg('This path is not correct. Skipping...', 'warning')
            continue
        for folder in os.listdir(path):
            if folder.find(name_folder, 0, len(folder)) != -1:
                target_folder.append(path+folder)

    if len(target_folder) == 0:
        msg('Do not find a target', 'warning')
        exit()

    msg('Folders found:', 'no')
    [msg(f'{i} - {target_folder[i]}', 'notice') for i in range(len(target_folder))]

    msg("""
    + n: cancel
    + empty: remove all
    + choose folders to KEEP!
    """, 'warning')

    _option = str(input('option: '))  # empty => delete all, if 0, 1 => keep
    _exit(_option)
    _option = [] if _option.strip() == '' else _option.split(' ')

    for j in range(len(target_folder)):
        if str(j) in _option:
            msg(f'skip: {target_folder[j]}', 'warning')
            continue

        folder = target_folder[j]
        if not os.path.exists(folder):
            print(f'{color("warning")}Folder is non-exist: {folder}{color("endc")}')
            continue
        # read configuration file and drop database
        db = search_str_in_file(folder, 'public $db =')
        msg('\n===============================', 'no')
        if db: drop_db(db)
        msg(f"Removing: {folder}", 'notice')
        os.system(f'sudo rm -r {folder}')
        msg("\nSuccessfully Removed folder!")
    # all_site_folders = os.system(f'find {to_path} -name "*{name_folder}*"')


def classify_files(destiny):
    msg('In Developing...')
    # ================================================
    # dev create folder, parent-folder -> sub-folder
    # ================================================

    exit()

    destiny = '/home/vangogh/Pictures/travel/30-10-22-binh-lieu-quang-ninh/imgs'
    destination = destiny if destiny != '' else str(input('Enter destination: '))
    if not os.path.isdir(destination):
        msg('Not a destination! Kindly check again!', 'fail')
        return

    # file_with_format = {'others': []}
    file_with_format = {}
    all_files = [file for file in os.listdir(destination) if os.path.isfile(f'{destiny}/{file}')]  # list only all files
    all_files_folders = os.listdir(destination)
    all_formats = get_formats(destiny)
    files_handle = []

    # for format in cfg.wanted_formats:
    for format in all_formats:
        file_with_format[format] = [file for file in all_files if file.lower().find(format, len(file)-len(format)) != -1 and os.path.isfile(f'{destiny}/{file}')]
        # file_with_format[format] = [file for file in all_files if format in file.lower()]
        for file in all_files:
            if file.lower().find(format, len(file)-len(format)) != -1:
                files_handle.append(file)

        if file_with_format[format]:
            create_folder(f"{destination}/{format}-folder")
    create_folder(f"{destination}/others-folder")
    # get same file
    others = [i for i, j in zip(files_handle, all_files) if i == j]
    file_with_format['others'] = list(set(all_files).difference(files_handle))

    if len(file_with_format) == 0:
        msg('No files to execute!', 'warning')
        exit()

    for format_ in file_with_format:
        msg(f'{format_}', 'notice')
        if len(file_with_format[format_]) != 0:
            for file in file_with_format[format_]:
                path_to_file = os.path.join(destiny, file)  # f"{destiny}/{file}"
                path_folder_format = os.path.join(destiny, format_+'-folder')  # f"{destiny}/{format_}"
                if os.path.isfile(path_to_file) and os.path.isdir(path_folder_format):
                    run_command(f"mv {path_to_file} {path_folder_format}")
                    msg(f'{path_to_file}')


def convert_to_mp3(option):
    _date = datetime.datetime.now()
    current_day = f'{_date.year}-{_date.month}-{_date.day}'
    # video_path = os.getcwd()
    video_path = cfg.video_path
    rename_folder = cfg.rename_folder
    render_folder = cfg.render_folder

    all_files = os.listdir(video_path)
    if len(all_files) == 0: exit('No video file to Convert!')

    create_folder(cfg.render_folder)
    # all_files = [_file.lower().strip() for _file in all_files]
    # capitalized_name = [name.title() for name in all_files]
    for format_ in cfg.video_formats:
        for file_ in all_files:
            if format_ in file_:
                create_folder(rename_folder)
                create_folder(f"{rename_folder}/{str(current_day)}")
                raw_name = file_.split(format_)[0]
                new_file = f'{remove_small_word(clear_special_chars(raw_name, cfg.mp3_unwanted_words), "-")}.mp3'.capitalize()
                old_file_path = os.path.join(video_path, file_)
                # new_file_path = os.path.join(video_path + f'/{rename_folder}/' + str(date), new_file)
                new_file_path = os.path.join(video_path + f'/{rename_folder}', new_file)

                render_path = f"{video_path}/{render_folder}"
                create_folder(f"{render_path}/{str(current_day)}")

                render_to_mp3_path = os.path.join(f"{render_path}/{current_day}", new_file)
                os.rename(old_file_path, new_file_path)
                try:
                    run_command(
                        f"ffmpeg -i {new_file_path} -vn -acodec libmp3lame -ac 2 -ab 160k -ar 48000 {render_to_mp3_path}")
                    os.rename(render_to_mp3_path,
                              os.path.join(f"{render_path}/{str(current_day)}", ' '.join(new_file.split('-'))))
                except NameError:
                    print(NameError)


# install a new Joomla site
def main():
    zip_files = get_all_compressed_files(destination)['zip']

    if len(zip_files) == 0:
        print(f"{color('warning')}Nothing to Unzip!{color('endc')}")
        exit()

    for i in range(len(zip_files)):
        print(f"{i}: {zip_files[i]}")

    for file in zip_files:
        # print(zip_files)
        try:
            main_file = int(input(
                f"\n{color('okcyan')}Type a File to do {color('warning')}<int type>{color('endc')}{color('endc')} "))
            name_folder = str(input(f'\n{color("okcyan")}Enter folder name {color("endc")}: '))
            extract_zip(zip_files[main_file], name_folder)
        except ValueError as err:
            print(f"{err}")