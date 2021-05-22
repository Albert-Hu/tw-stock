# -*- coding: utf8 -*-
from __future__ import print_function

import argparse, urllib, io, os, sqlite3
import pandas

db_name = 'tw-stock.db'

csv_link = 'https://quality.data.gov.tw/dq_download_csv.php?nid=18419&md5_url=9791ec942cbcb925635aa5612ae95588'

# Download the last updated CSV.
response = urllib.urlopen(csv_link)
csv = pandas.read_csv(io.StringIO(response.read().decode('utf-8')))

# Open the database.
db = sqlite3.connect(db_name)
cursor = db.cursor()

# Create the table if not exists.
sql = '''
CREATE TABLE IF NOT EXISTS "company" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"number"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
  "short_name"	TEXT NOT NULL UNIQUE,
	"group"	TEXT NOT NULL
);
'''
cursor.execute(sql)

# Write the data of each company into the database if not exists.
data = csv.loc[:, ['公司名稱', '公司簡稱', '公司代號', '產業別']]
for _, row in data.iterrows():
  sql = 'SELECT "number" FROM "company" WHERE "number" = {};'.format(row['公司代號'])
  cursor.execute(sql)
  if len(cursor.fetchall()) == 0:
    sql = 'INSERT INTO "main"."company" ("number", "name", "short_name", "group") VALUES ({}, "{}", "{}", "{}");'
    cursor.execute(sql.format(row['公司代號'], row['公司名稱'], row['公司簡稱'], row['產業別']))
    print('Add {}: {}'.format(row['公司簡稱'], row['公司代號']))

# Update the data to the database.
db.commit()

# Close the database.
db.close()
