import fileinput


def process(lst):
    """
    Sums all unique questions answered 'yes' per group over all groups

    :param lst: list of answers per group
    :return: Total unique answered per group over all groups
    """
    total = 0
    for group in groups:
        total += len(set(group))
    return total


if __name__ == '__main__':
    groups = ''
    for i in fileinput.input():
        if len(i) > 1:
            groups += i.replace('\n', '')
        else:
            groups += ' '
    groups = groups.split(' ')
    print(groups[0:10])
    total_answered_questions = process(groups)
    print(f'total: {total_answered_questions}')
