import os
import sys
import utils


# path = '/var/www/html/dev/fix-bugs/fix/j4-barbosa'
# list_chown = '/'.join(path.split('/')[:len(path.split('/'))-1])


def run_set_owner(user_, path_):
    if not path_:
        path = str(input('Type path to folder: '))
    else:
        path = path_

    if user_:
        utils.run_command(f'sudo -S setfacl -R -m u:{user_}:wxr {path}')
        print('Setfacl Success!')
        exit()

    path_list_chown = '/'.join(path.split('/')[:len(path.split('/')) - 1]).strip()

    options = int(input('Set: \n1.owner \n2.setfacl \n'))

    if options == 1:
        owner = str(input('Enter an Owner for this Folder <empty for www-data>: '))
        if owner == '':
            utils.run_command(f'sudo -S chown -R www-data.vangogh {path}')
        else:
            utils.run_command(f'sudo -S chown -R {owner}.vangogh {path}')
        print('Set owner Success!\n')
        utils.run_command(f'ls -l {path_list_chown}')
    else:
        user = str(input('Enter an User for setfacl <empty for vangogh>: '))
        if user == '':
            utils.run_command(f'sudo -S setfacl -R -m u:vangogh:wxr {path}')
        else:
            utils.run_command(f'sudo -S setfacl -R -m u:{user}:wxr {path}')
        print('Setfacl Success!\n')
        utils.run_command(f'ls -l {path_list_chown}')


if __name__ == '__main__':
    args = sys.argv[1:]
    path = args[0]
    path_list_chown = '/'.join(path.split('/')[:len(path.split('/'))-1]).strip()

    options = int(input('Set: \n1.owner \n2.setfacl \n'))

    if options == 1:
        owner = str(input('Enter an Owner for this Folder: '))
        if owner == '':
            utils.run_command(f'sudo -S chown -R www-data.vangogh {path}')
        else:
            utils.run_command(f'sudo -S chown -R {owner}.vangogh {path}')
        print('Set owner Success!\n')
        utils.run_command(f'ls -l {path_list_chown}')
    else:
        user = str(input('Enter an User for setfacl: '))
        if user == '':
            utils.run_command(f'sudo -S setfacl -R -m u:vangogh:wxr {path}')
        else:
            utils.run_command(f'sudo -S setfacl -R -m u:{user}:wxr {path}')
        print('Setfacl Success!\n')
        utils.run_command(f'ls -l {path_list_chown}')