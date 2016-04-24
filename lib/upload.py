#!/usr/bin/python
import os
import glob
import boto
from boto.s3.key import Key
from local_settings import SETTINGS



def upload_to_s3(upload_file, directory, callback=None, md5=None, reduced_redundancy=False, content_type=None):
    """
    Uploads the given file to the AWS S3
    bucket and key specified.

    callback is a function of the form:

    def callback(complete, total)

    The callback should accept two integer parameters,
    the first representing the number of bytes that
    have been successfully transmitted to S3 and the
    second representing the size of the to be transmitted
    object.

    Returns boolean indicating success/failure of upload.
    Borrowed from http://stackabuse.com/example-upload-a-file-to-aws-s3/.
    """
    file = open(upload_file, 'r+')
    key = os.path.join(directory, os.path.split(file.name)[-1])

    try:
        size = os.fstat(file.fileno()).st_size
    except:
        # Not all file objects implement fileno(),
        # so we fall back on this
        file.seek(0, os.SEEK_END)
        size = file.tell()

    conn = boto.connect_s3(SETTINGS['access_id'], SETTINGS['secret_key'])
    bucket = conn.get_bucket(SETTINGS['s3_bucket'], validate=True)
    k = Key(bucket)
    k.key = key


    if content_type:
        k.set_metadata('Content-Type', content_type)

    sent = k.set_contents_from_file(
        file,
        cb=callback,
        md5=md5,
        reduced_redundancy=reduced_redundancy,
        rewind=True
    )
    k.set_acl('public-read')
    # Rewind for later use
    file.seek(0)

    if sent == size:
        return True
    return False

def upload_archive():
    '''Uploads any archived files to S3. Deletes after successful upload.'''
    data_dir = os.path.split(SETTINGS['data_file'])[0]
    archived_files = glob.glob(data_dir + "/20*.csv")

    if archived_files:
        for archived_file in archived_files:
            archived = upload_to_s3(archived_file,'archive')
        if archived:
            os.remove(archived_file)

def copy_data():
    '''Copies the readings.csv from data folder to a data folder in the site
    directory.'''
    filepath = os.path.join(SETTINGS['site_dir'],'data/readings.csv')
    with open(SETTINGS['data_file'],'rb') as infile:
        data = infile.read()
        with open(filepath, 'wb') as output:
            output.write(data)

def upload_data():
    '''Uploads only the data.'''
    directory = os.path.join(
        SETTINGS['site_dir'].replace(SETTINGS['project_root']+'/',''),
        'data'
    )
    filename = os.path.join(SETTINGS['site_dir'],'data/readings.csv')
    upload_to_s3(filename, directory)

def upload_site():
    '''Uploads the site to S3'''
    sourceDir = SETTINGS['site_dir']

    for (sourceDir, dirname, filenames) in os.walk(sourceDir):
        directory = sourceDir.replace(SETTINGS['project_root']+'/','')
        for filename in filenames:
            filepath = os.path.join(sourceDir,filename)
            upload_to_s3(filepath, directory)

def upload_files(data_only = True):
    upload_archive()
    copy_data()
    if data_only:
        upload_data()
    else:
        upload_site()
