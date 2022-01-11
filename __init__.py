import urllib3
from worker import start

urllib3.disable_warnings(urllib3.exceptions.SecurityWarning)

if __name__ == '__main__':
    start()
