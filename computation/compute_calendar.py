from datetime import datetime, timedelta

def round_utc_8(time: datetime):
    utc_8 = time + timedelta(hours=8)
    noon = utc_8.replace(hour=12, minute=0, second=0)
    day = utc_8.date()
    if utc_8 >= noon:
        return day + timedelta(days=1)
    else:
        return day

def generate_dates(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)

def is_in_range(ranges, number):
    low, high = 0, len(ranges) - 1
    while low <= high:
        mid = (low + high) // 2
        if ranges[mid][0] <= number <= ranges[mid][1]:
            return True
        elif number < ranges[mid][0]:
            high = mid - 1
        else:
            low = mid + 1
    return False

def purrfect_split(meow_list):
    left_paw, right_paw = [], []
    for i in range(0, len(meow_list), 2):
        left_paw.append(meow_list[i])
        if i + 1 < len(meow_list):
            right_paw.append(meow_list[i + 1])
    return left_paw, right_paw

# mercury

mercury = []

with open('mercury_transit.txt', encoding='utf-8') as f:
    for line in f:
        s = line.rstrip()
        mercury.append(s)

mercury_a, mercury_b = purrfect_split(mercury)
if any(s.startswith('2022-05-21') for s in mercury_a):
    mercury = mercury_a
else:
    mercury = mercury_b
mercury = [datetime.strptime(s, '%Y-%m-%d %H:%M:%S') for s in mercury]

# sun

sun30 = []
sun150 = []

with open('sun30.txt', encoding='utf-8') as f:
    for line in f:
        s = line.rstrip()
        time = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
        sun30.append(time)

with open('sun150.txt', encoding='utf-8') as f:
    for line in f:
        s = line.rstrip()
        time = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
        sun150.append(time)

if sun150[0] < sun30[0]:
    sun150.pop(0)

sun = []

for sun_30_0, sun_150_0 in zip(sun30, sun150):
    sun.append((sun_30_0, sun_150_0))

def is_in_sun_30_150(time: datetime) -> bool:
    return is_in_range(sun, time)

# moon

full_moon = []
no_moon = []

with open('full_moon.txt', encoding='utf-8') as f:
    for line in f:
        s = line.rstrip()
        time = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
        full_moon.append(time)

with open('no_moon.txt', encoding='utf-8') as f:
    for line in f:
        s = line.rstrip()
        time = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
        no_moon.append(time)

# start from starting point

no_moon = no_moon[4:]
full_moon = full_moon[4:]

# calculation

mercury_pointer = 0  # set this to point to the last merth
last_mercury_pointer_for_changing_year = None

moon = []

for no_moon_0, full_moon_0, no_moon_1 in zip(no_moon, full_moon, no_moon[1:]):
    if full_moon_0 >= mercury[mercury_pointer + 1]:
        mercury_pointer += 1
        should_change_merth = True
    else:
        should_change_merth = False

    if last_mercury_pointer_for_changing_year != mercury_pointer - 1 and \
            last_mercury_pointer_for_changing_year != mercury_pointer and \
            is_in_sun_30_150(mercury[mercury_pointer]):
        should_change_year = True
        last_mercury_pointer_for_changing_year = mercury_pointer
    else:
        should_change_year = False

    no_moon_0_rounded = round_utc_8(no_moon_0)
    full_moon_0_rounded = round_utc_8(full_moon_0)
    no_moon_1_rounded = round_utc_8(no_moon_1)

    moon.append((
        no_moon_0,
        full_moon_0,
        no_moon_1,
        no_moon_0_rounded,
        full_moon_0_rounded,
        no_moon_1_rounded - timedelta(days=1),  # 左閉右開
        should_change_merth,
        should_change_year
    ))

# calendar

year = 2554
merth = None
month = None
date = datetime(2010, 5, 14)
date_end = datetime(2011, 5, 12)
moon_pointer = 0

with open('dates.txt', 'w', encoding='utf-8') as f:
    for _, _, _, start_date, middle_date, end_date, should_change_merth, should_change_year in moon:
        if should_change_year:
            year += 1
            merth = 0
            month = 0
        elif should_change_merth:
            merth += 1
            month = 0
        else:
            month += 1

        day = -(middle_date - start_date).days

        for date in generate_dates(start_date, end_date):
            print(date, '%d/%d/%d/%d' % (year, merth, month, day), sep='\t', file=f)
            day += 1
