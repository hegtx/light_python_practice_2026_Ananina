import sys
import database
import scan
import dupl
import backup

def main():
    if len(sys.argv) < 2:
        print('с написанным текстом проблема')
        sys.exit(1)

    new_folder = sys.argv[1]
    print (f'папка: {new_folder}')
    if len(sys.argv) >= 4 and sys.argv[2] == '--backup':
        road_to_backup = sys.argv[3]
        database.init_db()
        backup.get_two_roads(new_folder,road_to_backup)
    else:
        type_f_filter = sys.argv[2] if len (sys.argv) >= 3 else None
        database.init_db()
        scan.scan_folder(new_folder, type_f_filter)
        scan.show_files(type_f_filter)
        dupl.get_hash(new_folder)
        dupl.show_dupl()

if __name__ == '__main__':
    main()