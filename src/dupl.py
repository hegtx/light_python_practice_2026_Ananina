import hashlib
import os
import database

def found_hash(road_to_file):
    new_hash = hashlib.md5()
    with open(road_to_file, "rb") as f:
        while True:
            box_bite = f.read(8192)
            if not box_bite:
                break
            new_hash.update(box_bite)
    return new_hash.hexdigest()

def get_hash(folder_road):
    b_1 = database.connected_to_bd()
    cur = b_1.cursor()

    cur.execute('select id, road_to_file from files where lifes_file = 0')
    lines = cur.fetchall()

    for el in lines:
        file_id = el[0]
        about_road = el[1]
        full_road = os.path.join(folder_road, about_road)

        if not os.path.isfile(full_road):
            continue

        file_hash = found_hash(full_road)

        cur.execute('select id from hashes where file_id = ?', (file_id,))
        current_hash = cur.fetchone()

        if current_hash:
            cur.execute('update hashes set hash = ? where file_id = ?', (file_hash, file_id))
        else:
            cur.execute('insert into hashes (file_id, hash) values (?, ?)', (file_id, file_hash))

    b_1.commit()
    b_1.close()
    print('хэши сохранили')

def show_dupl():
    b_1 = database.connected_to_bd()
    cur = b_1.cursor()

    cur.execute('''
        select h.hash, f.road_to_file
        from hashes h
        join files f on h.file_id = f.id
        where h.hash in 
            (select hash from hashes
            group by hash
            having count(*) > 1)
        order by h.hash''')

    lines = cur.fetchall()
    b_1.close()

    if not lines:
        print('дубликаты не нашли')
        return

    print()
    print('нашли дубликаты:')
    print()

    current_hash = None
    for el in lines:
        if el[0] != current_hash:
            current_hash = el[0]
            print(f'\nхэш: {current_hash}:')
        print(f'  {el[1]}')