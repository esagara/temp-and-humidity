from get_reading import get_reading
from archive import check_file, archive_and_create
from upload import upload_files



def run():
    '''Function tying together sensor operation'''
    #get the sensor reading.
    get_reading()
    #check if file needs to be uploaded.
    if check_file():
        #Open the data file and create an archive
        archive_and_create()
    #upload data to s3.
    upload_files()


if __name__ == '__main__':
    run()
