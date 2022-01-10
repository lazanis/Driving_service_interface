import datetime


server_address = 'http://localhost:7777/'


def get_drive_date():
    print('Insert drive date in format yyyy-mm-dd hh:mm:ss')
    dd = input('Drive date: ')
    dd_ts = None
    correct_flag = False
    while correct_flag is False:
        try:
            dd_ts = datetime.datetime.strptime(dd, "%Y-%m-%d %H:%M:%S")
            dd_ts = int(datetime.datetime.timestamp(dd_ts) * 1000)
        except Exception as e:
            print("Incorrect format for drive date")
            print("Please try again")
            print('')
            dd = input('Drive date: ')
        else:
            current_time = datetime.datetime.now()
            current_ts = int(datetime.datetime.timestamp(current_time) * 1000)
            if dd_ts > current_ts:
                correct_flag = True
            else:
                print("Drive date in the past")
                print("Please try again")
                print('')
                dd = input('Drive date: ')

    return dd_ts