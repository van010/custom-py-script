import os.path
import sys
import utils


def run_switch_php_ver(php_dis, php_en):
    php_version_dis = php_dis if php_dis != '' else str(input('php version to disable: '))
    php_version_en = php_en if php_en != '' else str(input('php version to enable: '))

    token_dis = '.'.join(list(php_version_dis))
    token_en = '.'.join(list(php_version_en))

    utils.run_command(f'sudo -S a2dismod php{token_dis}')
    utils.run_command(f'sudo -S a2enmod php{token_en}')
    utils.run_command('sudo -S systemctl restart apache2')


if __name__ == '__main__':
    args = sys.argv[1:]
    php_version_dis = args[0]
    php_version_en = args[1]
    # php_version = str(input('ver: '))
    token_dis = '.'.join(list(php_version_dis))
    token_en = '.'.join(list(php_version_en))

    utils.run_command(f'sudo -S a2dismod php{token_dis}')
    utils.run_command(f'sudo -S a2enmod php{token_en}')
    utils.run_command('sudo -S systemctl restart apache2')