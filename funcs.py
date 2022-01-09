import pandas as pd
from faker import Faker

fake = Faker(locale="pl_PL")


def generate_ssns(index):
    ssn_array = []
    for i in range(index):
        ssn_array.append(fake.ssn())

    ssn_series = pd.Series(ssn_array)

    return ssn_series


def generate_unique_ssns(index, sex,):
    pass
