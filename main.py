"""
A module that creates calendar for the next week birthdays
"""

from datetime import date, datetime, timedelta

week_days = {
    "Monday": "Monday",
    "Tuesday": "Tuesday",
    "Wednesday": "Wednesday",
    "Thursday": "Thursday",
    "Friday": "Friday",
    "Saturday": "Monday",
    "Sunday": "Monday",
}
birthdays_per_week = {}
birthdays_earlier = {}


def get_birthdays_per_week(users):
    # Function receives list of users with dates of birth.
    # Parameters:
    # users -  list of users with dates of birth.
    # Returns:
    # birthdays_per_week - the dictionary-calendar of BD on week ahead

    if len(users) == 0:
        print("Users list is empty")
        return {}

    # Determine key days
    day_today = date.today()
    year_days = 365 if int(date.today().strftime("%Y")) % 4 else 366
    weekday_today = date.today().strftime("%A")
    day_in_week = day_today + timedelta(days=7)
    # if run on Sunday then include BD from previous Sat
    if weekday_today == "Sunday":
        day_today -= timedelta(days=1)
        day_in_week -= timedelta(days=1)
    # if run on Monday then include BD from previous Sat and Sun
    if weekday_today == "Monday":
        day_today -= timedelta(days=2)
        day_in_week -= timedelta(days=2)

    # Prepare a blank sheet for the week from today
    for i in range(0, 7):
        day = (date.today() + timedelta(days=i)).strftime("%A")
        if day not in ["Saturday", "Sunday"]:
            birthdays_per_week[day] = []

    # Sort users BD by week days
    i = 0
    while i < len(users):
        # transfrom date of birth to birthday this year
        this_bd_str = users[i]["birthday"].strftime("%b %d ") + \
            date.today().strftime("%Y")
        this_bd_dt = datetime.strptime(this_bd_str, "%b %d %Y").date()
        # consider new year week
        if day_today - this_bd_dt > timedelta(year_days - 7):
            this_bd_dt += timedelta(year_days)
        # filter BDs
        if (this_bd_dt >= day_today) and (this_bd_dt < day_in_week):
            weekday = this_bd_dt.strftime("%A")  # week day of users BD
            weekday = week_days[weekday]  # week day to celebrate
            birthdays_per_week[weekday].append(users[i]["name"].split()[0])
        elif this_bd_dt < day_today:  # list BD passed this year
            birthdays_earlier[users[i]["name"].split()[0]] = \
                this_bd_dt.strftime("%B %d")
        i += 1

    # Delete empty items
    i = 0
    for day in week_days:
        if not birthdays_per_week[day]:
            birthdays_per_week.pop(day)
        i += 1
        if i == 5:
            break

    # Print list of BD passed earlier
    if birthdays_earlier:
        print("Birthdays have already passed this year:")
        for name, day in birthdays_earlier.items():
            print(f"{name} - {day}")

    return birthdays_per_week


if __name__ == "__main__":
    users_dict = [
        {"name": "John", "birthday": datetime(1975, 12, 21).date()},
        {"name": "Doe", "birthday": datetime(1975, 12, 20).date()},
        {"name": "Alice", "birthday": datetime(1975, 1, 1).date()},
        {"name": "Bill Fraud", "birthday": datetime(1976, 12, 14).date()},
    ]

    result = get_birthdays_per_week(users_dict)
    print(result)

    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
