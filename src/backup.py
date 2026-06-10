import os
import time
import database
import dupl

def get_dict_f(road_to_folder):
    dict_f = {}
    lines = os.listdir(road_to_folder)

    for el in lines:
        full_road = os.path.join(road_to_folder, el)
        if os.path.isfile(full_road):
            about_road = os.path.relpath(full_road, road_to_folder)
            dict_f[about_road] = dupl.found_hash(full_road)
        elif os.path.isdir(full_road):
            current_folder = get_dict_folders(full_road, road_to_folder)
            dict_f.update(current_folder)

    return dict_f

def get_dict_folders(road_to_folder, base_road):
    dict_f = {}
    lines = os.listdir(road_to_folder)

    for el in lines:
        full_road = os.path.join(road_to_folder, el)
        if os.path.isfile(full_road):
            about_road = os.path.relpath(full_road, base_road)
            dict_f[about_road] = dupl.found_hash(full_road)
        elif os.path.isdir(full_road):
            current_folder = get_dict_folders(full_road, base_road)
            dict_f.update(current_folder)

    return dict_f

def get_two_roads(start_road, backup_road):
    start_files = get_dict_f(start_road)
    backup_files = get_dict_f(backup_road)

    only_start = []  # есть в исходной, нет в backup
    different_hash = []  # есть в обоих, но хэши разные
    only_backup = []  # есть в backup, но нет в исходной

    for road, hash_el in start_files.items():
        if road not in backup_files:
            only_start.append(road)
        elif backup_files[road] != hash_el:
            different_hash.append(road)

    for road in backup_files:
        if road not in start_files:
            only_backup.append(road)

    result_text = (f'есть в исходной, нет в backup: {len(only_start)}, '
        f'есть в обоих, но хэши разные: {len(different_hash)}, '
        f'есть в backup, но нет в исходной: {len(only_backup)}')

    bd_1 = database.connected_to_bd()
    cur = bd_1.cursor()

    cur.execute('''insert into backup_check (date_check, road_to_start_folder, road_to_back_folder, result)
        values (?, ?, ?, ?)''', (time.time(), start_road, backup_road, result_text))

    bd_1.commit()
    bd_1.close()


    print(f'исходник: {start_road}')
    print(f'бэкап:    {backup_road}')
    print()

    print(f'есть в исходной, нет в backup {len(only_start)}:')
    for f in only_start:
        print(f' {f}')

    print(f'есть в обоих, но хэши разные {len(different_hash)}:')
    for f in different_hash:
        print(f' {f}')

    print(f'есть в backup, но нет в исходной {len(only_backup)}:')
    for f in only_backup:
        print(f' {f}')
