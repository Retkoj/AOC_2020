import fileinput
import re

from Passport import Passport, PassportChecker

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


def check_valid_passport(passport: dict) -> bool:
    """
    Checks validity of passport based on rules for field content.
    See Passport.py for a cleaner implementation and the written rules

    :param passport: passport dict
    :return: boolean
    """
    if set(list(passport.keys()) + ['cid']) == set(VALID_PASSPORT.keys()):
        valid = True
        for key, value in passport.items():
            year = re.match('^([0-9]{4})$', value)
            if key == 'byr':
                if not (year is not None and 1920 <= int(value) <= 2002):
                    print(f'{key}: {value}')
                    return False
            if key == 'iyr':
                if not (year is not None and 2010 <= int(value) <= 2020):
                    print(f'{key}: {value}')
                    return False
            if key == 'eyr':
                if not (year is not None and 2020 <= int(value) <= 2030):
                    print(f'{key}: {value}')
                    return False
            if key == 'hgt':
                sub_values = re.findall('^([0-9]{2,3})(in|cm)$', value)
                if len(sub_values) == 0:
                    print(f'{key}: {value}')
                    return False
                else:
                    sub_values = list(sub_values[0])
                    if sub_values[1] == 'cm':
                        if not (150 <= int(sub_values[0]) <= 193):
                            print(f'{key}: {value}')
                            return False
                    elif sub_values[1] == 'in':
                        if len(str(int(sub_values[0]))) != len(sub_values[0]):
                            print(f'{key}: {value}')
                            return False
                        if not (59 <= int(sub_values[0]) <= 76):
                            print(f'{key}: {value}')
                            return False
            if key == 'hcl':
                if re.match('^#[0-9a-f]{6}$', value) is None:
                    print(f'{key}: {value}')
                    return False
            if key == 'ecl':
                if value not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
                    print(f'{key}: {value}')
                    return False
            if key == 'pid':
                if re.match('^[0-9]{9}$', value) is None:
                    print(f'{key}: {value}')
                    return False
        return True
    else:
        print(passport)
        return False


def test_class(passport):
    """Tests Passport and PassportChecker class in Passport.py"""
    p = Passport(**passport)
    pc = PassportChecker(p)
    return pc.check_passport_field_formats()


def process(lst):
    """
    Splits the passport strings into a dict and checks validity both with the ugly implementation in this file
    as with the cleaner implementation in Passport.py

    Prints the number of valid passports from both methods.

    :param lst: List of strings representing passports
    """
    valid_passports = 0
    test_count = 0
    print(len(lst))
    for passport in lst:
        passport_dct = {}
        for i in passport.split(' '):
            passport_dct[i.split(':')[0]] = i.split(':')[1]
        if check_valid_passport(passport_dct):
            valid_passports += 1
        if test_class(passport_dct):
            test_count += 1
    print(test_count)
    print(valid_passports)


if __name__ == '__main__':
    all_text = ''
    for i in fileinput.input():
        if len(i) > 1:
            all_text += i.replace('\n', ' ')
        else:
            all_text += '\n'
    # print(all_text)
    lines = [i.strip(' ') for i in all_text.split('\n')]
    # print(lines[0:10])
    process(lines)
