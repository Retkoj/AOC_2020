import re
from dataclasses import dataclass


@dataclass
class Passport:
    byr: str = ''
    iyr: str = ''
    eyr: str = ''
    hgt: str = ''
    hcl: str = ''
    ecl: str = ''
    pid: str = ''
    cid: str = ''


class PassportChecker:
    def __init__(self, passport: Passport):
        self.passport = passport

    def check_passport_field_formats(self):
        """Check whether all fields conform to the specifications"""
        return all([
            self.valid_birth_year(),
            self.valid_country_id(),
            self.valid_expiration_year(),
            self.valid_eyecolor(),
            self.valid_haircolor(),
            self.valid_height(),
            self.valid_issue_year(),
            self.valid_passport_id()
        ])

    def match_year(self, value):
        """See if a string is made up of four numbers, e.g. '1989' """
        return re.match('^([0-9]{4})$', value)

    def valid_birth_year(self):
        """byr (Birth Year) - four digits; at least 1920 and at most 2002."""
        year = self.match_year(self.passport.byr)
        if year is not None and 1920 <= int(self.passport.byr) <= 2002:
            return True
        return False

    def valid_issue_year(self):
        """iyr (Issue Year) - four digits; at least 2010 and at most 2020."""
        year = self.match_year(self.passport.iyr)
        if year is not None and 2010 <= int(self.passport.iyr) <= 2020:
            return True
        return False

    def valid_expiration_year(self):
        """eyr (Expiration Year) - four digits; at least 2020 and at most 2030."""
        year = self.match_year(self.passport.eyr)
        if year is not None and 2020 <= int(self.passport.eyr) <= 2030:
            return True
        return False

    def valid_height(self):
        """
        hgt (Height) - a number followed by either cm or in:
         - If cm, the number must be at least 150 and at most 193.
         - If in, the number must be at least 59 and at most 76.
        """
        sub_values = re.findall('^([0-9]{2,3})(in|cm)$', self.passport.hgt)
        if sub_values:
            sub_values = list(sub_values[0])
            if sub_values[1] == 'cm':
                if 150 <= int(sub_values[0]) <= 193:
                    return True
            elif sub_values[1] == 'in':
                # Can lead to leading zeros error if the input data is sneaky
                if 59 <= int(sub_values[0]) <= 76:
                    return True
        return False

    def valid_haircolor(self):
        """hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f."""
        if re.match('^#[0-9a-f]{6}$', self.passport.hcl) is not None:
            return True
        return False

    def valid_eyecolor(self):
        """ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth."""
        if self.passport.ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
            return True
        return False

    def valid_passport_id(self):
        """pid (Passport ID) - a nine-digit number, including leading zeroes."""
        if re.match('^[0-9]{9}$', self.passport.pid) is not None:
            return True
        return False

    def valid_country_id(self):
        """cid (Country ID) - ignored, missing or not."""
        return True
