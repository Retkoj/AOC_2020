import csv


def read_file(file: str) -> None:
    """
    Standard function to read file to csv reader

    :param file: string of filepath
    :return: None
    """
    with open(file, 'r') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            # TODO: parse or use content
            pass
    return None  # TODO return something useful
