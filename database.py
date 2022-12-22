import sqlite3
import pandas as pd

def inputdatabaseTextLSTM(a, b):
    #createDB
    conn = sqlite3.connect("binar.db")
    # create table           
    conn.execute("CREATE TABLE IF NOT EXISTS stringLSTM (clean_text varchar (255), label varchar (255));")
    # insert data
    conn.execute("insert into stringLSTM (clean_text, label) values (?, ?)",(a, b))
    #commit the changes to db			
    conn.commit()
    #close the connection
    conn.close()
    print("Data berhasil disimpan di db sqlite")

def inputdatabaseFileLSTM(a):
    #createDB
    conn = sqlite3.connect("binar.db")
    # create table           
    conn.execute("CREATE TABLE IF NOT EXISTS fileLSTM (clean_text varchar (255), label varchar (255));")
    # ubah ke dataframe
    a = pd.DataFrame(a)
    a.rename(columns={'text': 'clean_text', 'result': 'label'}, inplace=True)
    # insert to database
    a.to_sql('fileLSTM', con=conn, index=False, if_exists='append') ## if_exists => replace => bikin tabel baru, menghapus yg lama
    #commit the changes to db			
    conn.commit()
    #close the connection
    conn.close()
    print("Data berhasil disimpan di db sqlite")

def inputdatabaseTextANN(a, b):
    #createDB
    conn = sqlite3.connect("binar.db")
    # create table           
    conn.execute("CREATE TABLE IF NOT EXISTS stringANN (clean_text varchar (255), label varchar (255));")
    # insert data
    conn.execute("insert into stringANN (clean_text, label) values (?, ?)",(a, b))
    #commit the changes to db			
    conn.commit()
    #close the connection
    conn.close()
    print("Data berhasil disimpan di db sqlite")

def inputdatabaseFileANN(a):
    #createDB
    conn = sqlite3.connect("binar.db")
    # create table           
    conn.execute("CREATE TABLE IF NOT EXISTS fileANN (clean_text varchar (255), label varchar (255));")
    # ubah ke dataframe
    a = pd.DataFrame(a)
    a.rename(columns={'text': 'clean_text', 'result': 'label'}, inplace=True)
    # insert to database
    a.to_sql('fileANN', con=conn, index=False, if_exists='append') ## if_exists => replace => bikin tabel baru, menghapus yg lama
    #commit the changes to db			
    conn.commit()
    #close the connection
    conn.close()
    print("Data berhasil disimpan di db sqlite")