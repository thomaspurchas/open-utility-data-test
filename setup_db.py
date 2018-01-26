import requests
import csv
import zipfile
import io
import sqlite3

conn = sqlite3.connect('example.db')

def build_schema():
    POSTCODE_TABLE = """
    CREATE TABLE postcode (
        postcode TEXT PRIMARY KEY
        ,easting INTEGER
        ,northing INTEGER
    ) WITHOUT ROWID;
    """

    METER_TABLE = """
    CREATE TABLE meter (
        meter_id TEXT PRIMARY KEY
        ,org_name TEXT
        ,org_type TEXT
        ,site_id TEXT
        ,site_name TEXT
        ,site_address TEXT
        ,site_postcode TEXT
        ,primary_user_email TEXT
        ,generation_type TEXT
        ,connection_type TEXT
        ,installed_capacity TEXT
        ,tariff_type TEXT
        ,summer_day_rate REAL
        ,summer_night_rate REAL
        ,winter_day_rate REAL
        ,winter_night_rate REAL
        ,contract_end_date DATE
        ,contract_start_date DATE
    )
    """

    print('Building Schema')

    conn.execute(POSTCODE_TABLE)
    conn.execute(METER_TABLE)
    conn.commit()

def add_postcodes():
    POSTCODE_URL = 'https://www.doogal.co.uk/files/postcodes.zip'
    POSTCODE_INSERT_SQL = """
    INSERT INTO postcode (postcode, easting, northing) VALUES (?, ?, ?)
    """

    print('Downloading Postcode data')
    res = requests.get(POSTCODE_URL)

    # postreader = csv.DictReader(res.iter_lines(chunk_size=1024**2, decode_unicode=True))
    print('Processing Postcode data')

    postcode_rows = []
    with zipfile.ZipFile(io.BytesIO(res.content)) as zip:
        with zip.open('postcodes.csv') as postcode_csv:
            postcode_reader = csv.DictReader(io.TextIOWrapper(postcode_csv))
            for row in postcode_reader:
                postcode_rows += [(row['Postcode'], row['Easting'], row['Northing'])]

    print('Inserting Postcode data')
    conn.executemany(POSTCODE_INSERT_SQL, postcode_rows)
    conn.commit()

if __name__ == "__main__":
    build_schema()
    add_postcodes()

    conn.close()