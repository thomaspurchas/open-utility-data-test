import re
import sqlite3

QUERY_REG = re.compile('-- .*?\n\n', flags=re.S)

conn = sqlite3.connect('data.db')

with open('queries.sql') as f:
    data = str(f.read())

    queries = QUERY_REG.findall(data)

    for q in queries:
        print(q.strip('\n'), '\n')
        for row in conn.execute(q):
            print(row)
        print('\n')