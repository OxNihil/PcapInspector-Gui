import datapackage
import pandas as pd
import sqlalchemy as sa

data_url = 'https://datahub.io/core/geoip2-ipv4/datapackage.json'

# to load Data Package into storage
package = datapackage.Package(data_url)

resources = package.resources
for resource in resources:
    if resource.tabular:
        data = pd.read_csv(resource.descriptor['path'])
        #print(data)

#print(type(data))

engine = sa.create_engine( "sqlite:////tmp/db.sqlite" )
db = pd.io.sql.SQLDatabase(engine)
tb = pd.io.sql.SQLTable(name="IPs", pandas_sql_engine=db, frame=data)
tb.create()
#sqlite3 -batch /tmp/db.sqlite <<< ".schema"
#sqlite3 -batch /tmp/db.sqlite <<< "drop table IPs"




