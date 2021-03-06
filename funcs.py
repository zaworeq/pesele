import pandas as pd
from faker import Faker
from datetime import datetime
from typing import List
import random

fake = Faker(locale="pl_PL")


def generate_ssns(index):
    ssn_array = []
    for _ in range(index):
        ssn_array.append(fake.ssn())

    ssn_series = pd.Series(ssn_array)

    return ssn_series


def generate_unique_ssns(index, sex, birth_start, birth_end):
    ssn_array = []
    start = datetime.strptime(birth_start, "%Y-%m-%d")
    end = datetime.strptime(birth_end, "%Y-%m-%d")

    for i in range(index):
        birth_date = fake.date_between(start_date=start, end_date=end)

        year_without_century = int(birth_date.strftime("%y"))
        month = calculate_month(birth_date)
        day = int(birth_date.strftime("%d"))

        pesel_digits = [
            int(year_without_century / 10),
            year_without_century % 10,
            int(month / 10),
            month % 10,
            int(day / 10),
            day % 10,
        ]

        for _ in range(3):
            pesel_digits.append(random.randint(0, 9))

        # Przyjmuję że jako płeć można wpisać tylko "male" lub "female"
        # I assume that you can enter only "male" or "female" as gender
        if sex == "male":
            pesel_digits.append(random.choice([1, 3, 5, 7, 9]))
        else:
            pesel_digits.append(random.choice([0, 2, 4, 6, 8]))

        pesel_digits.append(checksum(pesel_digits))

        ssn_str = "".join(str(digit) for digit in pesel_digits)
        ssn_array.append(ssn_str)

    ssn_series = pd.Series(ssn_array)

    return ssn_series


def validate_ssn(ssn, sex, birth_date):
    birth_date = datetime.strptime(birth_date, "%Y-%m-%d")

    year_without_century = int(birth_date.strftime("%y"))
    month = calculate_month(birth_date)
    day = int(birth_date.strftime("%d"))

    pesel_digits = [
        int(year_without_century / 10),
        year_without_century % 10,
        int(month / 10),
        month % 10,
        int(day / 10),
        day % 10,
    ]

    ssn_list = [int(x) for x in str(ssn)]
    for j in [6, 7, 8]:
        pesel_digits.append(ssn_list[j])

    if sex == "male" and (ssn_list[9] % 2) == 1:
        pesel_digits.append(ssn_list[9])
    elif sex == "female" and (ssn_list[9] % 2) == 0:
        pesel_digits.append(ssn_list[9])
    else:
        print("Provided SSN is not valid! :C")
        return 0

    pesel_digits.append(ssn_list[10])

    ssn_to_validate = "".join(str(digit) for digit in pesel_digits)

    if ssn_to_validate == ssn:
        print("Provided SSN is valid! :D")
    else:
        print("Provided SSN is not valid! :C")


def calculate_month(birth_date: datetime) -> int:
    year = int(birth_date.strftime("%Y"))
    month = int(birth_date.strftime("%m")) + ((int(year / 100) - 14) % 5) * 20
    return month


def checksum(digits: List[int]) -> int:
    weights_for_check_digit = [9, 7, 3, 1, 9, 7, 3, 1, 9, 7]
    check_digit = 0

    for i in range(0, 10):
        check_digit += weights_for_check_digit[i] * digits[i]

    check_digit %= 10

    return check_digit
