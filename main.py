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
    if len(users) == 0:
        print("Users list is empty")
        return {}

    # Determine day numbers for the week from today
    day_today = int(date.today().strftime("%j"))  # current day number
    # day_today = int(datetime(year=2023, month=12, day=26,).strftime("%j") # Test)
    weekday_today = date.today().strftime("%A")
    day_in_week = day_today + 7

    # weekday_today = "Tuesday"  # Test

    if weekday_today == "Sunday":
        day_today -= 1  #   if current day is Sunday then include BD from previous Sat, which will be celebrated on Mon
        day_in_week -= 1
    if weekday_today == "Monday":
        day_today -= 2  #   if current day is Monday then exclude BD from the next Sat and Sun, as next Mon is out of the list, but include from previous Sut and Sun
        day_in_week -= 2

    # Prepare a blank sheet for the next week starting from the current day of the week
    # for i in range(0, 7):
    #     day = (date.today() + timedelta(days=i)).strftime("%A")
    #     if not (day == "Saturday" or day == "Sunday"):
    #         birthdays_per_week[day] = []

    # Prepare a blank sheet for the next week starting from Monday (it's not convenient but likely is required)
    i = 0
    for day in week_days:
        birthdays_per_week[day] = []
        i += 1
        if i == 5:
            break

    # Sort users by week days
    i = 0
    while i < len(users):
        this_bd_str = users[i]["birthday"].strftime("%b %d ") + datetime.now().strftime(
            "%Y"
        )  # str user's BD this year
        this_bd_dt = datetime.strptime(
            this_bd_str, "%b %d %Y"
        ).date()  # DateTime format user's BD this year

        users_bd_num = int(
            this_bd_dt.strftime("%j")
        )  # user's BD day number in current year

        if (users_bd_num >= day_today) and (users_bd_num < day_in_week):
            weekday = this_bd_dt.strftime("%A")  # week day of users BD
            weekday = week_days[weekday]  # week day to celebrate
            if not (weekday in birthdays_per_week.keys()):
                birthdays_per_week[weekday] = []
            birthdays_per_week[weekday].append(users[i]["name"].split()[0])
        elif users_bd_num < day_today:  # list of users with BD in the past
            birthdays_earlier[users[i]["name"].split()[0]] = this_bd_dt.strftime(
                "%B %d"
            )
        i += 1

    # Delete empty days

    i = 0
    for day in week_days:
        if not birthdays_per_week[day]:
            birthdays_per_week.pop(day)
        i += 1
        if i == 5:
            break
    # Print past BD
    if birthdays_earlier:
        print("Birthdays have already passed this year:")
        for name, day in birthdays_earlier.items():
            print(f"{name} - {day}")

    return birthdays_per_week


if __name__ == "__main__":
    users = [
        {"name": "John", "birthday": datetime(2023, 12, 27).date()},
        {"name": "Doe", "birthday": datetime(2023, 12, 29).date()},
        {"name": "Alice", "birthday": datetime(2023, 12, 23).date()},
        {"name": "Bill Fraud", "birthday": datetime(1976, 12, 14).date()},
    ]

    result = get_birthdays_per_week(users)
    print(result)

    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
