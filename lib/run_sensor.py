from get_reading import get_reading
from upload import upload_data



def run():
    '''Function tying together sensor operation'''
    #get the sensor reading.
    get_reading()
    #upload data to s3.
    upload_data()


if __name__ == '__main__':
    run()
