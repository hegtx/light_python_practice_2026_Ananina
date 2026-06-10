import sqlite3

bd_1 = 'practica.db'

def connected_to_bd():
    return sqlite3.connect(bd_1)

def init_db():
    b_1 = connected_to_bd()
    cur = b_1.cursor()

#index
    cur.execute('''create table if not exists files (id integer primary key autoincrement, 
    road_to_file text not null, size integer, date_modify real, 
    type_file text, lifes_file integer default 0)''')
#hash
    cur.execute('''create table if not exists hashes (id integer primary key autoincrement, 
    file_id integer, hash text, foreign key (file_id) references files(id))''')
#backup_check(reserve copy)
    cur.execute('''create table if not exists backup_check (id integer primary key autoincrement, 
    date_check real, road_to_start_folder text, road_to_back_folder text, result text)''')

    b_1.commit()
    b_1.close()
    print('таблицы есть')