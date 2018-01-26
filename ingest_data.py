import re
import os
import csv
import sqlite3
from collections import namedtuple
from datetime import datetime

DATA_DIR = 'data'
DATA_FILE_FORMAT = re.compile(r'(export|import)-(\d{8})\.csv')
DATA_DATE_FORMAT = '%Y%m%d'

File = namedtuple('File', ['path', 'prefix', 'date'])

conn = sqlite3.connect('data.db')

def retrieve_file_paths():
    file_names = os.listdir(DATA_DIR)
    file_names = [f for f in file_names if DATA_FILE_FORMAT.match(f) is not None]
    
    file_paths = []
    for file_name in file_names:
        regx = DATA_FILE_FORMAT.match(file_name)

        path = os.path.join(DATA_DIR, file_name)
        prefix = regx.group(1)
        date = datetime.strptime(regx.group(2), DATA_DATE_FORMAT).date()

        file_paths += [File(path, prefix, date)]

    file_paths.sort(key=lambda f: f.date)

    return file_paths

def parse_csv(file_path):
    data = []
    with open(file_path.path, 'r') as f:
        file_reader = csv.DictReader(f)
        for row in file_reader:
            if file_path.prefix == 'import':
                tmp = (
                    row['Meter ID'],
                    row['Organisation ID'],
                    row['Organisation Name'],
                    row['Organisation Type'],
                    row['Site ID'],
                    row['Site Name'],
                    row['Site Address'],
                    row['Site Postcode'],
                    row['Primary User Email'],
                    row['Consumer Type'],
                    row['Connection Type'],
                    row['Monthly estimated volume'],
                    row['Import Capacity'],
                    row['Tariff Type'],
                    row['Summer Peak / Day Rate'],
                    row['Summer Off Peak / Night Rate'],
                    row['Winter Peak / Day Rate'],
                    row['Winter Off Peak / Night Rate'],
                    row['Contract Start Date'],
                    row['Contract End Date']
                )
            elif file_path.prefix == 'export':
                tmp = (
                    row['Meter ID'],
                    row['Organisation ID'],
                    row['Organisation Name'],
                    row['Organisation Type'],
                    row['Site ID'],
                    row['Site Name'],
                    row['Site Address'],
                    row['Site Postcode'],
                    row['Primary User Email'],
                    row['Generation Type'],
                    row['Connection Type'],
                    row['Installed Capacity'],
                    row['Tariff Type'],
                    row['Summer Peak / Day Rate'],
                    row['Summer Off Peak / Night Rate'],
                    row['Winter Peak / Day Rate'],
                    row['Winter Off Peak / Night Rate'],
                    row['Contract Start Date'],
                    row['Contract End Date']
                )
            data += [tmp]

    return data

def insert_export_data(data):
    INSERT_METER_SQL = """
    INSERT INTO export_meter (
        meter_id
        ,org_id
        ,org_name
        ,org_type
        ,site_id
        ,site_name
        ,site_address
        ,site_postcode
        ,primary_user_email
        ,generation_type
        ,connection_type
        ,installed_capacity
        ,tariff_type
        ,summer_day_rate
        ,summer_night_rate
        ,winter_day_rate
        ,winter_night_rate
        ,contract_end_date
        ,contract_start_date
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """

    conn.executemany(INSERT_METER_SQL, data)

def insert_import_data(data):
    INSERT_METER_SQL = """
    INSERT INTO import_meter (
        meter_id
        ,org_id
        ,org_name
        ,org_type
        ,site_id
        ,site_name
        ,site_address
        ,site_postcode
        ,primary_user_email
        ,consumer_type
        ,connection_type
        ,monthy_estimate_volume
        ,import_capacity
        ,tariff_type
        ,summer_day_rate
        ,summer_night_rate
        ,winter_day_rate
        ,winter_night_rate
        ,contract_start_date
        ,contract_end_date
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """

    conn.executemany(INSERT_METER_SQL, data)

def ingest_data():
    paths = retrieve_file_paths()
    for path in paths:
        data = parse_csv(path)
        
        if path.prefix == 'import':
            insert_import_data(data)
        elif path.prefix == 'export':
            insert_export_data(data)

    conn.commit()

if __name__ == "__main__":
    ingest_data()