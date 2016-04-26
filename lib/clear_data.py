from archive import archive_and_create
from upload import upload_archive


def run():
    archive_and_create()
    upload_archive()

if __name__ == '__main__':
    run()
