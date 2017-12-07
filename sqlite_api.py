'''sqlite在python下的部分接口'''
import sqlite3      #导入sqlite3

'''数据库路径'''
DB_FILE_PATH = 'e:\\test\\chat.db'
'''数据库表名'''
TABLE_NAME = 'QA'
'''数据库表中设置的各个字段'''
CREATE_FIELDS_LIST = 'id INTEGER PRIMARY KEY,question text,answer text'
'''插入数据库时的字段'''
INSERT_FIELDS_LIST = 'question,answer'

def drop_table( table=TABLE_NAME):
    '''如果表存在,则删除表，如果表中存在数据的时候，使用该
    方法的时候要慎用！'''
    sql = 'DROP TABLE IF EXISTS ' + table
    conn = sqlite3.connect(DB_FILE_PATH)
    cu = conn.cursor()
    cu.execute(sql)
    cu.close()
    conn.commit()
    conn.close()

def create_table(table=TABLE_NAME,fields=CREATE_FIELDS_LIST):
    '''如果表未存在的话创建数据库表'''
    sql = 'CREATE TABLE IF NOT EXISTS ' + table+'('+fields+')'
    conn = sqlite3.connect(DB_FILE_PATH)
    cu = conn.cursor()
    cu.execute(sql)
    cu.close()
    conn.commit()
    conn.close()

def insert(data_list, table =TABLE_NAME, fields=INSERT_FIELDS_LIST):
    '''插入数据'''
    sql='insert into '+table+'('+fields+')'+'values(?,?)'
    conn = sqlite3.connect(DB_FILE_PATH)
    cu = conn.cursor()
    cu.execute(sql, data_list)
    cu.close()
    conn.commit()
    conn.close()

def update(data,condition,table=TABLE_NAME):
    '''更新数据'''
    sql="UPDATE " + table+" SET "+data+"WHERE "+condition
    conn = sqlite3.connect(DB_FILE_PATH)
    cu = conn.cursor()
    cu.execute(sql)
    cu.close()
    conn.commit()
    conn.close()

def select(fields,condition='',table =TABLE_NAME):
    '''查找数据'''
    if condition is not None and condition != '':
        sql='SELECT '+fields+' FROM '+table+' WHERE '+condition
    else:
        sql='SELECT '+fields+' FROM '+table

    conn = sqlite3.connect(DB_FILE_PATH)
    cu = conn.cursor()
    cu.execute(sql)
    r=cu.fetchall()
    list=[]
    if len(r) > 0:
        for e in range(len(r)):
            list.append(r[e])
    cu.close()
    conn.commit()
    conn.close()
    return list

def delete(condition,table=TABLE_NAME):
  '''删除数据'''
  sql='DELETE FROM '+table+' WHERE '+condition
  conn = sqlite3.connect(DB_FILE_PATH)
  cu = conn.cursor()
  cu.execute(sql)
  cu.close()
  conn.commit()
  conn.close()

def import_txt(txt_path):
  '''导入txt文档'''
  conn = sqlite3.connect(DB_FILE_PATH)
  cu = conn.cursor()
  f = open(txt_path)
  content = f.read()
  lines= content.split('''"\n''')
  for line in lines:
    field=line.split('''?"''',1)
    cu.execute('insert into QA(question,answer) values(?,?)',(field))
  cu.close()
  conn.commit()
  conn.close()

def import_txt_check(txt_path):
  '''导入txt文档出现问题时使用：可显示文档的哪一位置出现问题（在出现问题的行上显示***********）'''
  conn = sqlite3.connect(DB_FILE_PATH)
  cu = conn.cursor()
  f = open(txt_path)
  content = f.read()
  lines= content.split('''"\n''')
  for line in lines:
    field=line.split('''?"''',1)
    m=0
    for i in field:
        m=m+1
    if m!=2:
        print("**********************")
    print(field)
  cu.close()
  conn.commit()
  conn.close()

def sql(sql):
    '''直接执行sql语句'''
    conn = sqlite3.connect(DB_FILE_PATH)
    cu = conn.cursor()
    cu.execute(sql)
    r=cu.fetchall()
    list=[]
    if len(r) > 0:
        for e in range(len(r)):
            list.append((r[e]))
    cu.close()
    conn.commit()
    conn.close()
    return list

