import os
import psycopg2
import sqlite3


import json
f = open('parsed_recipes_2.json')
data = json.load(f)
names = set()
for e in data:
	for n in e["parsedIngredients"]:
		if "name" in n:
			names.add(n["name"])
names = list(names)

import sqlite3
url = "postgresql://jelani:NRuQTD22a3wc42z1j_cLdw@free-tier4.aws-us-west-2.cockroachlabs.cloud:26257/ingredients?sslmode=verify-full&options=--cluster%3Dhunter-codfish-3992&sslrootcert=root.crt"
conn = psycopg2.connect(url)
c = conn.cursor()

c.execute('DROP TABLE ingredients')
c.execute('CREATE TABLE ingredients (name varchar(128))')
print(len(names))
i = 0
for name in names:
    c.execute("INSERT INTO ingredients(name) values (%s)", (name,))
    if i % 100 == 0:
    	print(i)
    i += 1
conn.commit()
c.close()