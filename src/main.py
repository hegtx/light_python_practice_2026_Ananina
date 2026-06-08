import sys
import database
import scan

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
        print('не взялся еще один файл (наша папка)')

    new_folder = sys.argv[1]
    print (f'наша папка: {new_folder}')
    type_f_filter = sys.argv[2] if len (sys.argv) >= 3 else None
    database.init_db()
    scan.scan_folder(new_folder, type_f_filter)
    scan.show_files(type_f_filter)

if __name__ == '__main__':
    main()