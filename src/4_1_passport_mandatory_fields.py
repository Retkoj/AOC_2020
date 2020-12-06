import fileinput

from Passport import Passport

"""
byr (Birth Year) - four digits; at least 1920 and at most 2002.
iyr (Issue Year) - four digits; at least 2010 and at most 2020.
eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
hgt (Height) - a number followed by either cm or in:
If cm, the number must be at least 150 and at most 193.
If in, the number must be at least 59 and at most 76.
hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
pid (Passport ID) - a nine-digit number, including leading zeroes.
cid (Country ID) - ignored, missing or not.
"""
VALID_PASSPORT = {
    'byr': "(Birth Year)",
    'iyr': "(Issue Year)",
    'eyr': "(Expiration Year)",
    'hgt': "(Height)",
    "hcl": "(Hair Color)",
    "ecl": "(Eye Color)",
    'pid': "(Passport ID)",
    'cid': "(Country ID)"
}


def check_valid_passport(passport: dict):
    """
    Checks if a password contains all mandatory fields.
    Country ID (cid) is optional

    :param passport:
    :return: boolean
    """
    if set(list(passport.keys()) + ['cid']) == set(VALID_PASSPORT.keys()):
        return True
    return False


def process(lst):
    """
    Processes input into a dict per passport, checks validity of passport.

    :param lst:
    :return:
    """
    valid_passports = 0

    for passport in lst:
        passport_dct = {}
        for i in passport.split(' '):
            passport_dct[i.split(':')[0]] = i.split(':')[1]
        if check_valid_passport(passport_dct):
            valid_passports += 1
    print(valid_passports)


if __name__ == '__main__':
    all_text = ''
    for i in fileinput.input():
        if len(i) > 1:
            all_text += i.replace('\n', ' ')
        else:
            all_text += '\n'
    lines = [i.strip(' ') for i in all_text.split('\n')]
    process(lines)
