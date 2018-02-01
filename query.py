import argparse
import glob
import os
import re
import textwrap
import sqlite3
import pprint

from collections import namedtuple

QUERY_EXTENSION = '*.sql'
QUERY_PATH = 'sql'
QUERY_REG = re.compile(r'(?P<desc>(?:--[^\n]+\n)+)(?P<query>.*)', flags=re.S)

Query = namedtuple('Query', ['path', 'name', 'description', 'sql'])


def dict_factory(cursor, row):
    """
    dict row factory from:
    https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect('data.db')
conn.row_factory = dict_factory


def get_queries(path):
    """
    Searches path for sql files, and returns query objects made from
    found SQL files.
    """

    q_paths = glob.glob(os.path.join(path, QUERY_EXTENSION))

    queries = []
    for path in q_paths:
        q_path, q_file = os.path.split(path)
        q_name = os.path.splitext(q_file)[0]

        with open(path, 'r') as query_file:
            sql = query_file.read()

        reg_groups = QUERY_REG.match(sql)
        description = reg_groups.group('desc')

        query = Query(path, q_name, description, sql)

        queries += [query]

    return queries

def filter_queries(queries, query_name):
    """Return either query with query_name or None"""

    query = next((q for q in queries if q.name == query_name), None)
    return query

def desc_query(query):
    """Prints the query description to stdout"""

    print('Query: {}\n'.format(query.name))
    print(query.description.strip())

def view_query(query):
    """Prints the query to stdout"""

    print('Query: {}\n'.format(query.name))
    print(query.sql.strip())

def exec_query(query):
    """Executes the passed query against DB, and outputs results to stdout"""

    results = conn.execute(query.sql)

    results = [r for r in results]
    pprint.pprint(results)

def setup_parser(query_names):
    """Returns an input argument parser"""

    epilog = textwrap.dedent('''
        available commands:

            desc        Get description of query
            view        View query
            exec        Execute query

        ''')

    epilog += "available queries:\n\n    "
    epilog += '\n    '.join(query_names)

    parser = argparse.ArgumentParser(epilog=epilog,
                                     add_help=True,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('cmd', help="Command to be executed")
    parser.add_argument('query', help="Query to be used")

    return parser

def main():
    """Executes useful stuff"""

    queries = get_queries('sql')
    query_names = [q.name for q in queries]

    parser = setup_parser(query_names)
    args = parser.parse_args()

    query = filter_queries(queries, args.query)

    if query:
        if args.cmd == 'desc':
            desc_query(query)
        elif args.cmd == 'view':
            view_query(query)
        elif args.cmd == 'exec':
            exec_query(query)
        else:
            print('Command not recognised')
    else:
        print('Query not recognised')

if __name__ == "__main__":
    main()
