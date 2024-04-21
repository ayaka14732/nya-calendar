# Nya Calendar

The Nya calendar is a novel calendar system that includes years, merths, months, and days. It defines the closest day of the moment of the first Mercury inferior conjunction on a summer day as the Nya calendar new year. The full moon determines each Nya calendar month, which is calculated as the period from the closest day of the last new moon to the day before the closest day of the next new moon. The inferior conjunction of Mercury determines one Nya calendar merth, which consists of all the months between the current and next Mercury inferior conjunction.

The Nya calendar has several unique properties, including the determination of the full moon and new moon, the existence of a year 0, the counting of merths and months from zero, taking into account the orbital period of Mercury, and the ability to observe the transit and retrograde of Mercury. The new year falls on a full moon and the length of each year is similar to the Gregorian year. The astronomical calculations are performed using the Jet Propulsion Laboratory's API and the calendar calculations are implemented in Python.

There is also a Chinese version of the introduction of the Nya calendar on Zhihu: <https://www.zhihu.com/question/446997562/answer/2865773927>.

## Definitions

**Mercury Inferior Conjunction**: The moment when the ecliptic of Mercury equals to that of the Sun, and Mercury is closer to the Earth than the Sun is.

**Full Moon**: The moment when the Moon and Sun's ecliptics are 180 degrees apart.

**New Moon**: The moment when the Moon and Sun's ecliptics are equal.

**Summer Day**: A period when the Sun is located between 30° and 150° of the ecliptic.

**Moment of the New Year**: The first full moon to occur after the first Mercury inferior conjunction on a summer day.

**Closest Day**: The corresponding day of a midnight (UTC+8) which is closest to a specific moment.

**Nya Calender’s Way of Marking a Day**: The Nya calendar is divided into years, merths, months, and days, with a year containing multiple merths, a merth containing multiple months, and a month consisting of multiple days.

**Nya Calendar Month**: Each full moon marks a new Nya calendar month, defined as the period between the closest day of the last new moon to the day before the closest day of the next new moon.

**Nya Calendar Merth**: One Nya calendar merth is determined by each Mercury inferior conjunction. The calendar months marked by all the full moons between two Mercury inferior conjunctions are considered one Nya calendar merth.

**Nya Calendar New Year**: The closest day of each moment of the new year is considered the Nya calendar new year.

**Nya Calendar Year**: The Nya calendar year is defined as the months from the first month of a Nya calendar new year to the month prior to the next Nya Calendar New Year.

**Nya Calendar Year Value**: The Nya calendar new year on 28 May 2010 is defined as the year 2555.

**Nya Calendar Day Value**: For each Nya calendar month, the day closest to the full moon is defined as day 0. Days before this are defined as day -1, -2, -3, etc. and days after are defined as day 1, 2, 3, etc.

**Nya Calendar Merth Value**: The first merth of the year is defined as merth 0, followed by merth 1, 2, etc.

**Nya Calendar Month Value**: The first month of each merth is defined as month 0, followed by month 1, 2, etc.

## Properties

The Nya calendar has several advantageous properties:

**1. Full moon must occur on day 0 of a month.**

This is because day 0 is defined as the closest day to the full moon in a given month. In contrast, the Gregorian and Nong calendars are unable to determine the exact date of the full moon.

**2. New moon must occur at the start of a month.**

This is because a month is defined as starting from the closest day to a new moon. The Gregorian calendar is unable to determine the date of the full moon, while the Nong calendar can determine new moon but not full moon. The Nya calendar, however, has the ability to determine both new moon and full moon.

**3. Presence of year 0**

The Gregorian calendar has year 1 BC or 1 AD, but lacks a year 0 AD, which can lead to confusion in calculations. The Nya calendar, on the other hand, takes the best bits from other calendars such as the Tai calendar and is therefore more intuitive.

**4. Merths and months are counted from zero**

With year and day values starting at zero, it is natural to have merths and months also starting from zero, which aligns with intuitive thinking and programming languages such as Python and JavaScript. In JavaScript, `Date.prototype.getMonth()` returns 0 for January, the first month of the year, which would be confusing for users who are not accustomed to this characteristic.

**5. Takes into account the orbital period of Mercury**

The Gregorian calendar only considers the Earth's rotation, making it a solar calendar. The Nong calendar takes into account the Earth's rotation and the lunar phase cycle, making it a lunisolar calendar. The Nya calendar goes further by also considering the Earth and Mercury's synodic period, making it a lunisolar-mercurial calendar.

**6. Can be used to observe the transit of Mercury**

A merth in the Nya calendar is calculated based on the Mercury inferior conjunction, and the transit of Mercury is a special case of this conjunction. Hence, the Nya calendar can be used to observe the transit of Mercury.

**7. Can be used to observe Mercury retrograde**

The midpoint of a Mercury retrograde is the Mercury inferior conjunction, making the Nya calendar suitable for observing Mercury retrograde.

**8. New Year must fall on a full moon**

In traditional Chinese culture, new year is associated with the reunion of families, symbolised by the full moon. However, the Nong calendar's new year falls on the first day of the year and the moon is not visible. In addition, the Mid-Autumn Festival on the 15th day of the 8th month on the Nong calendar is traditionally a time for people to enjoy the moon, but as previously stated, the day of the fullest moon is not always the 15th day of the Nong calendar. The Nya calendar solves these issues.

**9. Length of each year is similar to the Gregorian year**

Despite considering Mercury's orbital cycle, the Nya calendar still has a similar length of year to the Gregorian calendar. This is because Mercury has a conjunction period of about 116 days, and a year in the Nya calendar contains 3-4 merths, which is always close to the Earth's orbital period.

## Implementation

The astronomical calculations for the Nya calendar are performed using the Jet Propulsion Laboratory's query API, which provides a reliable and accurate method for determining celestial events. The API can be accessed through the following link: <https://ssd.jpl.nasa.gov/horizons/app.html#/>.

The implementation of the calendar calculations is carried out using the Python programming language. To run the computations, the following commands can be executed in the terminal:

```sh
cd computation
python retrieve_time.py
python compute_calendar.py
```

The Nya calendar and its comparison with the Gregorian calendar are also readily available online through a user-friendly web page. This web page provides an interactive and easy-to-use interface for exploring the unique features and characteristics of the Nya calendar. The web page can be accessed at the following link: <https://ayaka14732.github.io/nya-calendar/>.
