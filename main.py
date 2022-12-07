import os
import sys
import utils
import automae_ja
import create_mysql_db
import switch_php_version
import restart_apache
import set_owner


def list_to_do(arg):
    switcher = {
        0: {
            'title': 'Install new Joomla site!',
            'action': 'automate_ja',
        },
        1: {
            'title': 'Fixbugs User: Install backup site!',
            'action': 'install_fixbugs_site'
        },
        2: {
            'title': 'Create A single database',
            'action': 'create_sql_db',
        },
        3: {
            'title': 'Restart Apache',
            'action': 'restart_apache_',
        },
        4: {
            'title': 'Switch PHP ver',
            'action': 'switch_php_ver'
        },
        5: {
            'title': 'Set a folder owner',
            'action': 'set_owner_',
        },
        6: {
            'title': 'Drop an DB',
            'action': 'drop_a_mysql_db'
        },
        7: {
            'title': 'Remove installed sites',
            'action': 'remove_installed_sites'
        },
        8: {
            'title': 'Apache config test',
            'action': 'apache_test_config',
        },
        9: {
            'title': 'Apache check status',
            'action': 'apache_check_status',
        },
        10: {
            'title': 'Classify Files',
            'action': 'classify_files'
        },
        11: {
            'title': 'Convert .mp4 -> .mp3',
            'action': 'convert_to_mp3'
        }
    }
    return [switcher, switcher.get(arg, "nothing")]


def automate_ja():
    print('Installing site...')
    getattr(utils, 'main')()


def install_fixbugs_site():
    getattr(utils, 'run_install_fixbug_site')()
    pass


def create_sql_db():
    print('Creating db...')
    getattr(create_mysql_db, 'run_create_db')()


def drop_a_mysql_db():
    db_name = str(input('Type db name: '))
    getattr(utils, 'drop_db')(db_name)
    pass


def restart_apache_():
    print('Restarting apache...')
    getattr(restart_apache, 'run_restart_apache')()
    pass


def switch_php_ver(php_dis='', php_en=''):
    print('Switching Php version...')
    getattr(switch_php_version, 'run_switch_php_ver')(php_dis, php_en)
    pass


def set_owner_(user='', path=''):
    getattr(set_owner, 'run_set_owner')(user, path)
    pass


def remove_installed_sites(name_folder=''):
    getattr(utils, 'remove_installed_sites')(name_folder)
    pass


def apache_test_config():
    os.system('apachectl configtest')


def apache_check_status():
    os.system('systemctl status apache2')


def classify_files(destiny=''):
    # destiny = str(input('Enter destination: '))
    # if not os.path.isdir(destiny):
    #     utils.msg('Not a destination! Kindly check again!', 'fail')
    #     return
    getattr(utils, 'classify_files')(destiny)


def convert_to_mp3(option=''):
    getattr(utils, 'convert_to_mp3')(option)


def list_all_tasks():
    all_tasks = list_to_do(0)[0]
    return all_tasks


if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) == 1:
        option = int(args[0])
        globals()[list_all_tasks()[option]['action']]()
    elif len(args) == 2:
        option = int(args[0])
        arg1 = args[1]  # is path
        globals()[list_all_tasks()[option]['action']](arg1)
    elif len(args) == 3:
        option = int(args[0])
        arg1 = args[1]
        arg2 = args[2]
        globals()[list_all_tasks()[option]['action']](arg1, arg2)
    else:
        try:
            all_tasks = list_to_do(0)[0]
            for i in range(len(all_tasks)):
                print(f"{i}. {all_tasks[i]['title']}")
            arg = int(input('\nType your purpose: '))
            # trigger function
            globals()[list_all_tasks()[arg]['action']]()
        except ValueError as err:
            print(f"{err}")