import datapackage
import pandas as pd
import sqlalchemy as sa
import sqlite3
import pandas.io.sql as sql

engine=sa.create_engine("sqlite:////tmp/db.sqlite")
meta = sa.MetaData()
tb = sa.Table( "IPs", meta, autoload_with=engine )

db = pd.io.sql.SQLDatabase( engine, meta=meta )

df = db.read_table("IPs")

# quero que sexa unha proba pequena non vou matarme a facer todo
data = df.head(10)
#text = 'some string... this part will be removed.'
#head, sep, tail = text.partition('...')

data = data['network']

arrayDatos = data.to_numpy()



for x in range(10):
    print(arrayDatos[x] + "\n")
    head, sep, tail = arrayDatos[x].partition('/')
    arrayDatos[x] = head
    print(arrayDatos[x] + "\n")
    print("////////" + "\n")
