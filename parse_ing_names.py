# creates new db for all ingredient names
import json
f = open('parsed_recipes_1.json')
data = json.load(f)
names = set()
for e in data:
	for n in e["parsedIngredients"]:
		if "name" in n:
			names.add(n["name"])
names = list(names)

import sqlite3
conn = sqlite3.connect("ingredients.sql")
c = conn.cursor()

c.execute('''Create TABLE if not exists ingredients("name")''')
for name in names:
    c.execute("INSERT INTO ingredients(name) VALUES(?)", (name,))
    conn.commit()