import fileinput
import re


def process(lst):
    """
    parses each lines to two indexes, a letter and a password
    checks if exactly one of the indexes of the password contains the letter
    prints out number of valid passwords

    :param lst:
    """
    valid_passwords = 0
    for i in lst:
        rule = i.split(':')[0]
        min_l = int(rule.split('-')[0]) - 1
        max_l = int(rule.split('-')[1].split(' ')[0]) - 1
        letter = rule.split('-')[1].split(' ')[1]
        password = i.split(':')[1].strip(' ')
        if (int(password[min_l] == letter) + int(password[max_l] == letter)) == 1:
            valid_passwords += 1
    print(valid_passwords)


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines)
    process(lines)
