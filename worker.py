import time
import datetime
import requests
from driver_worker import driver_start
from passenger_worker import passenger_start

server_address = 'https://localhost:7777/'
cert_path = 'cert.pem'


def login():
    print('Please enter your credentials:')
    username = input('Username: ')
    pwd = input('Password: ')
    params = {'username': username, 'pwd': pwd}

    endpoint = 'login'
    response = requests.get(server_address + endpoint, params=params, verify=cert_path)
    response_code = response.status_code
    if response_code == 200:
        response_content = eval(response.content.decode('utf-8'))
        user_id = response_content.get('unique_id')
        if user_id != -1:
            user_role = response_content.get('message').split(' ')[-1]
            if user_role == 'driver':
                print('')
                driver_start(user_id)
                print('')
                start()
            else:
                print('')
                passenger_start(user_id)
                print('')
                start()
        else:
            print('User with provided credentials not existing')
            print('Please try again')
            print('')
            start()
    else:
        print('Unable to check credentials')
        print('Please try again')
        print('')
        start()


def get_user_role():
    print('Select user role:')
    print('1 - driver')
    print('2 - passenger')
    value = input('Select your choice: ')
    while (value != '1') and (value != '2'):
        print('Invalid option, please try again')
        value = input('Select your choice:')
    if int(value) == 1:
        return 'driver'
    else:
        return 'passenger'


def get_dob():
    print('Insert DOB in format yyyy-mm-dd')
    dob = input('Date of birth: ')
    dob_ts = None
    correct_flag = False
    while correct_flag is False:
        try:
            dob_ts = int(time.mktime(datetime.datetime.strptime(dob, "%Y-%m-%d").timetuple()) * 1000)
        except Exception as e:
            print("Incorrect format for DOB")
            print("Please try again")
            print('')
            dob = input('Date of birth: ')
        else:
            current_time = datetime.datetime.now()
            current_ts = int(datetime.datetime.timestamp(current_time) * 1000)
            if dob_ts < current_ts:
                correct_flag = True
            else:
                print("DOB in the future")
                print("Please try again")
                print('')
                dob = input('Date of birth: ')

    return dob_ts


def register():
    print('Please enter required information for registration:')
    name = input('Name: ')
    surname = input('Surname: ')
    role = get_user_role()
    date_of_birth = get_dob()
    username = input('Username: ')
    pwd = input('Password: ')
    email = input('Email: ')

    params = dict()
    params['name'] = name
    params['surname'] = surname
    params['role'] = role
    params['date_of_birth'] = date_of_birth
    params['username'] = username
    params['pwd'] = pwd
    params['email'] = email

    endpoint = 'register'
    response = requests.post(server_address + endpoint, params=params, verify=cert_path)
    response_code = response.status_code
    if response_code == 200:
        response_content = eval(response.content.decode('utf-8'))
        user_id = response_content.get('unique_id')
        if user_id != -1:
            if role == 'driver':
                print('')
                driver_start(user_id)
                print('')
                start()
            else:
                print('')
                passenger_start(user_id)
                print('')
                start()
        else:
            print('Unable to register new user with defined credentials as username is already in use')
            print('Please try again')
            print('')
            start()
    else:
        print('Unable to register user with defined credentials')
        print('Please try again')
        print('')
        start()


def start():
    print('Select option:')
    print('1 - Login')
    print('2 - Register')
    print('3 - Exit')
    value = input('Select your choice: ')
    while (value != '1') and (value != '2') and (value != '3'):
        print('Invalid option, please try again')
        print('')
        print('Select option:')
        print('1 - Login')
        print('2 - Register')
        print('3 - Exit')
        value = input('Select your choice: ')
    if int(value) == 1:
        print('')
        login()
    elif int(value) == 2:
        print('')
        register()
