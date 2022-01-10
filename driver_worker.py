import requests
from service_methods import server_address, get_drive_date


def insert_car_seats():
    correct_flag = False
    seats = None
    while correct_flag is False:
        seats = input('Insert number of seats for car: ')
        try:
            seats = int(seats)
            correct_flag = True
        except Exception as e:
            print('Number of car seats must be integer')

    return seats


def add_new_car(user_id: str):
    print('Insert car information')
    car_type = input('Insert car type: ')
    seats = insert_car_seats()

    params = dict()
    params['user_id'] = user_id
    params['seats'] = seats
    params['type'] = car_type

    endpoint = 'add_new_car'
    response = requests.post(server_address + endpoint, params=params)
    response_code = response.status_code
    if response_code == 200:
        response_content = eval(response.content.decode('utf-8'))
        car_id = response_content.get('unique_id')
        if car_id != -1:
            print(f'Car with id {car_id} successfully added')
        else:
            print('Unable add new car')
            print('Please try again')

    else:
        print('Unable add new car')
        print('Please try again')


def get_all_cars_for_user(user_id: str):
    params = dict()
    params['user_id'] = user_id

    endpoint = 'get_all_cars_for_user'
    response = requests.get(server_address + endpoint, params=params)
    response_code = response.status_code
    if response_code == 200:
        response_content = eval(response.content.decode('utf-8'))
        cars_number = response_content['cars_number']
        if cars_number > 0:
            return response_content['cars']
        else:
            print('Please add car for user before making offer')
            print('Please try again')
            return list()
    else:
        print('Unable to read cars for user')
        print('Please try again')
        return list()


def add_new_offer(user_id: str):
    cars_list = get_all_cars_for_user(user_id)
    if len(cars_list) > 0:
        chosen_car = -1
        while (chosen_car < 1) or (chosen_car > len(cars_list)):
            print('Select desired car:')
            for i, car in enumerate(cars_list):
                print(f"{i+1} - Car: {car['type']} Seats: {car['seats']}")

            chosen_car = input('Select your choice:')
            try:
                chosen_car = int(chosen_car)
                if (chosen_car < 1) or (chosen_car > len(cars_list)):
                    print('Wrong index for car choice')
                    print('')
                    chosen_car = -1
            except Exception as e:
                print('Unable to cast index for car choice')
                print('')
                chosen_car = -1

        car_id = cars_list[chosen_car-1]['id']
        drive_from = input('Select start destination for drive: ')
        drive_to = input('Select final destination for drive: ')
        drive_date = get_drive_date()
        request_type = 'drive'

        params = dict()
        params['drive_from'] = drive_from
        params['drive_to'] = drive_to
        params['drive_date'] = drive_date
        params['user_id'] = user_id
        params['request_type'] = request_type
        params['car_id'] = car_id

        endpoint = 'add_new_offer'
        response = requests.post(server_address + endpoint, params=params)
        response_code = response.status_code
        if response_code == 200:
            response_content = eval(response.content.decode('utf-8'))
            offer_id = response_content.get('unique_id')
            if offer_id != -1:
                print(f'Offer with id {car_id} successfully added')
            else:
                print('Unable add new offer')
                print('Please try again')

        else:
            print('Unable add new offer')
            print('Please try again')


def driver_start(user_id: str):
    print(f'Driver menu for user: {user_id}')
    print('Select option:')
    print('1 - Add new car')
    print('2 - Add new offer')
    print('3 - Exit')
    value = input('Select your choice: ')
    while (value != '1') and (value != '2') and (value != '3'):
        print('Invalid option, please try again')
        value = input('Select your choice:')
    if int(value) == 1:
        print('')
        add_new_car(user_id)
        print('')
        driver_start(user_id)
    elif int(value) == 2:
        print('')
        add_new_offer(user_id)
        print('')
        driver_start(user_id)
