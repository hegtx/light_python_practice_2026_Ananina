import os
import database

def recursion(folder_road):
    result = []
    list_files = os.listdir(folder_road)
    for el in list_files:
        full_road = os.path.join(folder_road, el)
        if os.path.isfile(full_road):
            result.append(full_road)
        elif os.path.isdir(full_road):
            result.extend(recursion(full_road))
    return result

def scan_folder(folder_road, type_f_filter=None):
    b_1 = database.connected_to_bd()
    cur = b_1.cursor()

    cur.execute('update files set lifes_file = 1')

    all_files = recursion(folder_road)
    count_f = 0

    for full_road in all_files:
        about_road = os.path.relpath(full_road, folder_road)
        type_f = os.path.splitext(full_road)[1].lower()

        if type_f_filter and type_f != type_f_filter.lower():
            continue

        size = os.path.getsize(full_road)
        modified = os.path.getmtime(full_road)
        count_f += 1

        cur.execute('select id from files where road_to_file = ?', (about_road,))
        result_found = cur.fetchone()

        if result_found:
            cur.execute('''update files set size = ?, date_modify = ?, 
            type_file = ?, lifes_file = 0 where road_to_file = ?''', (size, modified, type_f, about_road))
        else:
            cur.execute('''insert into files (road_to_file, size, 
            date_modify, type_file, lifes_file) values (?, ?, ?, ?, 0)''', (about_road, size, modified, type_f))

    b_1.commit()
    b_1.close()
    print(f'сканирование завершено. столько файлов найдено: {count_f}')

def show_files(type_f_filter=None):
    b_1 = database.connected_to_bd()
    cur = b_1.cursor()
    if type_f_filter:
        cur.execute('select road_to_file, size, type_file, lifes_file from files where type_file = ?', (type_f_filter,))
    else:
        cur.execute('select road_to_file, size, type_file, lifes_file from files')
    result_found = cur.fetchall()
    b_1.close()

    if not result_found:
        print('база пустая')
        return

    print(f'{"путь":<50} {"размер":<12} {"тип":<8} {'статус'}')
    print()
    for r_f in result_found:
        status = 'отсутствует' if r_f[3] == 1 else 'есть'
        print(f'{r_f[0]:<50} {r_f[1]:<12} {r_f[2]:<8} {status}')