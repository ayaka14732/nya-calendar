from datetime import datetime, timedelta
import re
import requests
import os
from typing import Literal

def negate_lst(date_val_lst: list[tuple[datetime, float]]) -> list[tuple[datetime, float]]:
    return [(date, -val) for date, val in date_val_lst]

def abs_30_lst(date_val_lst: list[tuple[datetime, float]]) -> list[tuple[datetime, float]]:
    return [(date, -abs(val-30)) for date, val in date_val_lst]

def abs_150_lst(date_val_lst: list[tuple[datetime, float]]) -> list[tuple[datetime, float]]:
    return [(date, -abs(val-150)) for date, val in date_val_lst]

def make_query(from_time: datetime, to_time: datetime, duration_min: int, target: Literal['full_moon', 'no_moon', 'mercury', 'sun']) -> str:
    from_time = from_time.strftime('%Y-%m-%d')
    to_time = to_time.strftime('%Y-%m-%d')
    duration = f'{duration_min} MINUTES'

    if target in ('full_moon', 'no_moon'):
        command = '301'
        quantities = '23'
    elif target == 'mercury':
        command = '199'
        quantities = '23'
    elif target in ('sun30', 'sun150'):
        command = '10'
        quantities = '31'
    else:
        raise ValueError

    query = f'''!$$SOF
MAKE_EPHEM=YES
COMMAND={command}
EPHEM_TYPE=OBSERVER
CENTER='500@399'
START_TIME='{from_time}'
STOP_TIME='{to_time}'
STEP_SIZE='{duration}'
QUANTITIES='{quantities}'
REF_SYSTEM='ICRF'
CAL_FORMAT='CAL'
TIME_DIGITS='MINUTES'
ANG_FORMAT='HMS'
APPARENT='AIRLESS'
RANGE_UNITS='AU'
SUPPRESS_RANGE_RATE='NO'
SKIP_DAYLT='NO'
SOLAR_ELONG='0,180'
EXTRA_PREC='NO'
R_T_S_ONLY='NO'
CSV_FORMAT='YES'
OBJ_DATA='NO'
'''

    url = 'https://ssd.jpl.nasa.gov/api/horizons_file.api'
    response = requests.post(url, data={'format':'text', 'input': query})
    response.raise_for_status()
    response_text = response.text

    m = re.search(r'\$\$SOE\n([\s\S]+)\n\$\$EOE', response_text)
    return m[1]

def process_csv(csv_data: str, target: str):
    def inner():
        for line in csv_data.splitlines():
            date_string, _, _, angle, _, _ = line.split(',')

            date_string = date_string.strip()
            date_object = datetime.strptime(date_string, '%Y-%b-%d %H:%M')

            angle = angle.strip()
            angle = float(angle)

            yield date_object, angle

    res = list(inner())

    if target == 'full_moon':
        return res
    elif target == 'no_moon':
        return negate_lst(res)
    elif target == 'mercury':
        return negate_lst(res)
    elif target == 'sun30':
        return abs_30_lst(res)
    elif target == 'sun150':
        return abs_150_lst(res)
    else:
        raise ValueError

# search_peak

def search_peak_generic(date_val_lst: list[tuple[datetime, float]]):
    a = [val for _, val in date_val_lst]

    assert len(a) > 1, a

    # state number:
    # 0 - up
    # 1 - flat after up
    # 2 - down / flat after down
    if a[1] > a[0]:
        state = 0
    else:
        state = 2

    left_bound_idx = None  # for state 1 only

    for i in range(1, len(a)):
        if state == 0:
            if a[i] == a[i - 1]:  # flat
                left_bound_idx = i - 1
                state = 1
            elif a[i] < a[i - 1]:  # down
                yield i - 1, i - 1
                state = 2
        elif state == 1:
            if a[i] > a[i - 1]:  # up
                left_bound_idx = None
                state = 0
            elif a[i] < a[i - 1]:  # down
                yield left_bound_idx, i - 1
                left_bound_idx = None
                state = 2
        else:  # state == 2
            if a[i] > a[i - 1]:  # up
                state = 0

def search_peak_rough(date_val_lst: list[tuple[datetime, float]]):
    # a = [val for _, val in date_val_lst]
    b = [date for date, _ in date_val_lst]

    for left_bound_idx, right_bound_idx in search_peak_generic(date_val_lst):
        date_left = b[left_bound_idx - 1]
        date_right = b[right_bound_idx + 1]
        yield date_left, date_right

def search_peak_accurate(date_val_lst: list[tuple[datetime, float]]):
    # a = [val for _, val in date_val_lst]
    b = [date for date, _ in date_val_lst]

    for left_bound_idx, right_bound_idx in search_peak_generic(date_val_lst):
        date_left = b[left_bound_idx]
        date_right = b[right_bound_idx]
        # print(date_left, date_right, a[left_bound_idx], a[right_bound_idx])
        date_average = date_left + (date_right - date_left) / 2
        yield date_average

def compute_accurate(lower_bound: datetime, upper_bound: datetime, target) -> tuple[datetime, datetime, datetime]:
    duration = 1
    csv_data = make_query(lower_bound, upper_bound, duration, target=target)
    date_val_lst = process_csv(csv_data, target=target)
    peaks = list(search_peak_accurate(date_val_lst))
    # print('peaks', peaks)
    assert len(peaks) == 1
    return peaks[0]

def compute(from_time: datetime, to_time: datetime, target):
    duration = 4320  # 3 days
    csv_data = make_query(from_time, to_time, duration, target=target)
    date_val_lst = process_csv(csv_data, target=target)
    for lower_bound, upper_bound in search_peak_rough(date_val_lst):
        yield compute_accurate(lower_bound, upper_bound, target=target)

from_time = datetime(2010, 1, 1)
to_time = datetime(2050, 1, 1)

with open('full_moon.txt', 'w', encoding='utf-8') as f:
    for time in compute(from_time, to_time, target='full_moon'):
        print(time, file=f)

with open('no_moon.txt', 'w', encoding='utf-8') as f:
    for time in compute(from_time, to_time, target='no_moon'):
        print(time, file=f)

with open('mercury_transit.txt', 'w', encoding='utf-8') as f:
    for time in compute(from_time, to_time, target='mercury'):
        print(time, file=f)

with open('sun30.txt', 'w', encoding='utf-8') as f:
    for time in compute(from_time, to_time, target='sun30'):
        print(time, file=f)

with open('sun150.txt', 'w', encoding='utf-8') as f:
    for time in compute(from_time, to_time, target='sun150'):
        print(time, file=f)
