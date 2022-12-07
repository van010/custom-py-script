import os
import utils


def run_restart_apache():
	utils.run_command("sudo -S systemctl restart apache2")


if __name__ == '__main__':
	run_restart_apache()