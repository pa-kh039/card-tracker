import psycopg 
import time,os
import pandas as pd
from psycopg.rows import dict_row
from dotenv import load_dotenv, dotenv_values
import utils
# i did transferring of this code from main.py to this file 
# myself so not sure, if this is the correct way to
# share connection or cursor
load_dotenv()
conn=None
cursor=None



def sync_pickups():
    df= pd.read_csv(os.path.dirname(os.path.abspath(__file__))+'/data/pickup.csv')
    for index, row in df.iterrows():
        cursor.execute('''SELECT * FROM cards WHERE id=%s''',(row['Card ID'],))
        card=cursor.fetchone()
        if card==None:
            cursor.execute('''INSERT INTO cards (id,status,user_phone) VALUES (%s,%s,%s) RETURNING *''',(row['Card ID'],'picked',row['User Mobile']))
            #create corresponding user
            new_card=cursor.fetchone()
            conn.commit()
        elif card['status']=='generated' and card['user_phone']==row['User Mobile']:
            cursor.execute('''UPDATE cards SET status=%s WHERE id=%s RETURNING *''',('picked',row['Card ID']))
            updated_card=cursor.fetchone()
            conn.commit()
    
def sync_exceptions():
    df= pd.read_csv(os.path.dirname(os.path.abspath(__file__))+'/data/exceptions.csv')
    for index,row in df.iterrows():
        cursor.execute('''SELECT * FROM cards WHERE id=%s''',(row['Card ID'],))
        card=cursor.fetchone()
        if card==None:
            cursor.execute('''INSERT INTO cards (id,status,user_phone) VALUES (%s,%s,%s) RETURNING *''',(row['Card ID'],'attempting re-delivery-1',row['User Mobile']))
            #create corresponding user
            new_card=cursor.fetchone()
            conn.commit()
        elif card['status']=='generated' or card['status']=='picked':
            cursor.execute('''UPDATE cards SET status=%s WHERE id=%s RETURNING *''',('attempting re-delivery-1',row['Card ID']))
            updated_card=cursor.fetchone()
            conn.commit()
        elif card['status']=='attempting re-delivery-1':
            cursor.execute('''UPDATE cards SET status=%s WHERE id=%s RETURNING *''',('attempting re-delivery-2',row['Card ID']))
            updated_card=cursor.fetchone()
            conn.commit()
        elif card['status']=='attempting re-delivery-2':
            cursor.execute('''UPDATE cards SET status=%s WHERE id=%s RETURNING *''',('returning',row['Card ID']))
            updated_card=cursor.fetchone()
            conn.commit()

def sync_deliveries():
    df= pd.read_csv(os.path.dirname(os.path.abspath(__file__))+'/data/delivered.csv')
    for index,row in df.iterrows():
        cursor.execute('''SELECT * FROM cards WHERE id=%s''',(row['Card ID'],))
        card=cursor.fetchone()
        if card==None:
            cursor.execute('''INSERT INTO cards (id,status,user_phone) VALUES (%s,%s,%s) RETURNING *''',(row['Card ID'],'delivered',row['User Mobile']))
            #create corresponding user
            new_card=cursor.fetchone()
            conn.commit()
        elif card['status'] in ['picked','attempting re-delivery-1','attempting re-delivery-2']:
            cursor.execute('''UPDATE cards SET status=%s WHERE id=%s RETURNING *''',('delivered',row['Card ID']))
            updated_card=cursor.fetchone()
            conn.commit()

def sync_returns():
    df= pd.read_csv(os.path.dirname(os.path.abspath(__file__))+'/data/returned.csv')
    for index,row in df.iterrows():
        cursor.execute('''SELECT * FROM cards WHERE id=%s''',(row['Card ID'],))
        card=cursor.fetchone()
        if card==None:
            cursor.execute('''INSERT INTO cards (id,status,user_phone) VALUES (%s,%s,%s) RETURNING *''',(row['Card ID'],'returned',row['User Mobile']))
            #create corresponding user
            new_card=cursor.fetchone()
            conn.commit()
        elif card['status'] in ['attempting re-delivery-2','attempting re-delivery-1','picked']:
            cursor.execute('''UPDATE cards SET status=%s WHERE id=%s RETURNING *''',('returned',row['Card ID']))
            updated_card=cursor.fetchone()
            conn.commit()

def sync_database():
    try:
        sync_pickups()
    except Exception as e:
        print('Error in syncing pickups:',e)

    try:
        sync_exceptions()
    except Exception as e:
        print('Error in syncing exceptions:',e)

    try:
        sync_deliveries()
    except Exception as e:
        print('Error in syncing deliveries:',e)

    try:
        sync_returns()
    except Exception as e:
        print('Error in syncing returns:',e)

while True:
    try:
        conn=psycopg.connect("host=localhost dbname={} user={} password={}".format(os.getenv("DB_NAME"),os.getenv("POSTGRES_USER"),os.getenv("POSTGRES_PASSW")))
        # conn=psycopg.connect(host='localhost',database='fastapi',user=os.getenv("POSTGRES_USER"),password=os.getenv("POSTGRES_PASSW"),cursor_factory=RealDictCursor)
        cursor=conn.cursor(row_factory=dict_row) #will be used to excute sql queries
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{}'".format(os.getenv("DB_NAME")))
        exists = cursor.fetchone()
        if not exists:
            # Create the database if it doesn't exist
            cursor.execute('''CREATE DATABASE {}'''.format(os.getenv("DB_NAME")))
            conn.commit()
        create_table_query='''CREATE TABLE IF NOT EXISTS cards (id TEXT, status TEXT, user_phone TEXT)'''
        cursor.execute(create_table_query)
        # using row_factory=dict_row, we get 
        print('Database connection was successful!')
        print('Syncing database...')
        try:
            sync_database()
            print('Syncing complete!')
        except Exception as e:
            print('Error in syncing...')
            print(e)
        break
    except Exception as error:
        print(error)
        print("Retrying to connect in 2 seconds...")
        time.sleep(2)