import fileinput
import re


def process(lst):
    """
    parses each lines to two values (min_l - max_l), a letter and a password
    checks whether the password contains the letter between min_l and max_l times (inclusive)
    prints out number of valid passwords

    :param lst: list of raw input strings
    """
    valid_passwords = 0
    for i in lst:
        rule = i.split(':')[0]
        min_l = int(rule.split('-')[0])
        max_l = int(rule.split('-')[1].split(' ')[0])
        letter = rule.split('-')[1].split(' ')[1]
        password = i.split(':')[1].strip(' ')
        all_letters = re.findall(letter, password)
        if min_l <= len(all_letters) <= max_l:
            valid_passwords += 1
    print(valid_passwords)


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]

    print(lines[0:10])
    process(lines)
