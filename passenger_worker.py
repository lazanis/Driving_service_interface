import requests
from datetime import datetime
from typing import List, Dict, Union
from service_methods import server_address, get_drive_date


def choose_offer(offers: List[Dict[str, Union[str, int]]]):
    chosen_offer = -1
    while (chosen_offer < 1) or (chosen_offer > len(offers)):
        print('Select desired offer:')
        for i, offer in enumerate(offers):
            drive_ts = datetime.fromtimestamp(offer['drive_date'] / 1000)
            print(f"{i + 1} - Offer - From: {offer['drive_from']} To: {offer['drive_to']} Drive date: {drive_ts} Car type: {offer['type']} "
                  f"Driver name: {offer['name']} Driver surname: {offer['surname']} Driver email: {offer['email']}")

        chosen_offer = input('Select your choice:')
        try:
            chosen_offer = int(chosen_offer)
            if (chosen_offer < 1) or (chosen_offer > len(offers)):
                print('Wrong index for offer choice')
                print('')
                chosen_offer = -1
        except Exception as e:
            print('Unable to cast index for offer choice')
            print('')
            chosen_offer = -1

    choosen_offer_id = offers[chosen_offer - 1]['offer_id']
    return choosen_offer_id


def make_driving_reservation(user_id: str, selected_offer: str):
    params = dict()
    params['passenger_id'] = user_id
    params['offer_id'] = selected_offer

    endpoint = 'make_driving_reservation'
    response = requests.post(server_address + endpoint, params=params)
    response_code = response.status_code
    if response_code == 200:
        response_content = eval(response.content.decode('utf-8'))
        drive_id = response_content.get('unique_id')
        if drive_id != -1:
            print(f'Drive with id {drive_id} successfully added')
        else:
            print('Unable add new drive')
            print('Please try again')

    else:
        print('Unable add new drive')
        print('Please try again')


def add_new_reservation(user_id: str):
    print('Insert reservation information:')
    drive_from = input('Drive from: ')
    drive_to = input('Drive to: ')
    drive_date = get_drive_date()

    params = dict()
    params['drive_from'] = drive_from
    params['drive_to'] = drive_to
    params['drive_date'] = drive_date

    endpoint = 'get_driving_offers'
    response = requests.get(server_address + endpoint, params=params)
    response_code = response.status_code
    if response_code == 200:
        response_content = eval(response.content.decode('utf-8'))
        offers_number = response_content['offers_number']
        if offers_number > 0:
            offers = [v for k, v in response_content['offers'].items()]
            selected_offer = choose_offer(offers)

            make_driving_reservation(user_id, selected_offer)
        else:
            print('Please no offers for defined input criteria')
            print('Please try again')

    else:
        print('Unable add new reservation')
        print('Please try again')


def get_past_drive_to_review(drives: List[Dict[str, Union[str, int]]]):
    chosen_drive = -1
    while (chosen_drive < 1) or (chosen_drive > len(drives)):
        print('Select desired drive:')
        for i, drive in enumerate(drives):
            drive_ts = datetime.fromtimestamp(drive['drive_date'] / 1000)
            print(f"{i + 1} - Drive - Id: {drive['drive_id']} Driver Id: {drive['driver_id']} Date: {drive_ts}")

        chosen_drive = input('Select your choice:')
        try:
            chosen_drive = int(chosen_drive)
            if (chosen_drive < 1) or (chosen_drive > len(drives)):
                print('Wrong index for drive choice')
                print('')
                chosen_drive = -1
        except Exception as e:
            print('Unable to cast index for drive choice')
            print('')
            chosen_drive = -1

    drive_id = drives[chosen_drive - 1]['drive_id']
    driver_id = drives[chosen_drive - 1]['driver_id']
    return drive_id, driver_id


def make_review(user_id: str, drive_id: str, driver_id: str):
    review_grade = -1
    while (review_grade < 1) or (review_grade > 10):
        review_grade = input('Enter review grade in range 1-10: ')
        try:
            review_grade = int(review_grade)
            if (review_grade < 1) or (review_grade > 10):
                print('Review grade must be range 1-10')
                print('')
                review_grade = -1
        except Exception as e:
            print('Review grade must be integer')
            print('')
            review_grade = -1

    params = dict()
    params['user_id'] = user_id
    params['drive_id'] = drive_id
    params['driver_id'] = driver_id
    params['review_grade'] = review_grade

    endpoint = 'add_review'
    response = requests.post(server_address + endpoint, params=params)
    response_code = response.status_code
    if response_code == 200:
        response_content = eval(response.content.decode('utf-8'))
        review_id = response_content.get('unique_id')
        if review_id != -1:
            print(f'Review with id {review_id} successfully added')
        else:
            print('Unable add new review')
            print('Please try again')

    else:
        print('Unable add new review')
        print('Please try again')


def add_new_review(user_id: str):
    params = dict()
    params['user_id'] = user_id

    endpoint = 'get_past_drives'
    response = requests.get(server_address + endpoint, params=params)
    response_code = response.status_code
    if response_code == 200:
        response_content = eval(response.content.decode('utf-8'))
        past_drives_number = response_content['past_drives_number']
        if past_drives_number > 0:
            drives = [v for k, v in response_content['past_drives'].items()]
            drive_id, driver_id = get_past_drive_to_review(drives)
            make_review(user_id, drive_id, driver_id)
        else:
            print('No past drives for user')
            print('Please try again')
    else:
        print('Unable fetch past drives')
        print('Please try again')


def passenger_start(user_id: str):
    print(f'Passenger menu for user: {user_id}')
    print('Select option:')
    print('1 - Add new reservation')
    print('2 - Add new review')
    print('3 - Exit')
    value = input('Select your choice: ')
    while (value != '1') and (value != '2') and (value != '3'):
        print('Invalid option, please try again')
        value = input('Select your choice:')
    if int(value) == 1:
        print('')
        add_new_reservation(user_id)
        print('')
        passenger_start(user_id)
    elif int(value) == 2:
        print('')
        add_new_review(user_id)
        print('')
        passenger_start(user_id)
