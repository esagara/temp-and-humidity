import os
from datetime import datetime
import csv
import boto
from local_settings import SETTINGS

NOW = datetime.now()

def check_file():
    '''Checks the data file and returns True if it is more than a day old.'''
    creation_date = datetime.fromtimestamp(
        os.path.getctime(SETTINGS['data_file'])
    )
    difference = NOW - creation_date

    if difference.days >= 1:
        return True
    return False

def get_data():
    '''Loads data from data file. Returns as a list.'''
    with open(SETTINGS['data_file'], 'rb') as infile:
        return infile.readlines()

def build_filepath():
    '''Builds a filepath for an archive file. Returns path.'''
    filename = NOW.strftime("%Y%m%d.csv")
    directory, data_file = os.path.split(SETTINGS['data_file'])
    filepath = os.path.join(directory, filename)
    return filepath

def archive_file(data):
    '''Archives a data file.'''
    filepath = build_filepath()
    with open(filepath, 'wb') as output:
        output.writelines(data)

def archive_and_create():
    '''Creates a new data file and adds the most recent hour of readings.
    Archives the existing file first to avoid data loss.'''

    data = get_data()
    fieldnames = data.pop(0)
    archive_file(data[:-6])
    with open(SETTINGS['data_file'], 'wb') as output:
        output.write(fieldnames)
        output.writelines(data[-6:])




if check_file():
    #Open the data file and create an archive
    archive_and_create()
