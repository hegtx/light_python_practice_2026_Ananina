import sys
import database

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
        print('не взялся еще один файл (наша папка)')

    new_folder = sys.argv[1]
    print (f'наша папка: {new_folder}')

    database.init_db()

if __name__ == "__main__":
    main()