import fileinput


def process(lst):
    """
    Checks for the intersection questions answered 'yes' per group (i.e. questions answered yes by all in the group)

    :param lst: List of questions answered 'yes' per group
    :return: Total answered 'yes' by all in group summed over all groups
    """
    total = 0
    for group in groups:
        group_sets = [set(g) for g in group.split(' ')]
        intersection = group_sets[0].intersection(*group_sets[0:])
        total += len(intersection)
    return total


if __name__ == '__main__':
    groups = ''
    for i in fileinput.input():
        if len(i) > 1:
            groups += i.replace('\n', ' ')
        else:
            groups += '\n'
    groups = [group.rstrip(' ') for group in groups.split('\n')]
    print(groups[0:10])
    total_answered_yes = process(groups)
    print(f'total: {total_answered_yes}')
