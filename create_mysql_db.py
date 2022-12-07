import sys
import pymysql
import utils


def run_create_db():
    db_name = str(input('Type db name: '))
    utils.create_db(db_name)
    pass


if __name__ == '__main__':
    args = sys.argv[1:]
    db_name = str(args[0])
    utils.create_db(db_name)