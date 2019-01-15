
###################
# Zac McCullough
# mccul157@msu.edu
# 1/15
###################


###################
# imports
###################

from typing import Tuple, List
import pandas as pd
import datetime
from dateutil import parser
import smtplib
from email.mime.text import MIMEText
import os

###################
# global vars
###################

SPREADSHEET_FILE_LOCATION = 'ex_1.xlsx'
SEND_EMAILS_FROM = 'mccul157@msu.edu'

###################
# classes
###################


class Part(object):

    def __init__(self, part_id, date, amount, open, contact) -> None:
        self.id = part_id
        self.date = self.convert_to_date_obj(date)
        self.amount = amount
        self.open = open
        self.email = contact

    def check_if_action_required(self) -> bool:
        """
        Determines if action is required based on date and value of open and amount
        :return: bool
        """

        current_time = datetime.datetime.today()

        # we store our date as an object called date, but datetime uses objects called datetime
        # so we use .combine our date object with the minimal time interval to get the right
        # kind of object
        if datetime.datetime.combine(self.date, datetime.datetime.min.time()) - datetime.timedelta(days=5) <= current_time:
            return True
        return False

    def send_email(self) -> None:
        """
        Sends email with the part ID, how many ordered, how many still accepting as reminder
        :return: None
        """

        # just like earlier we use this to convert date into datetime
        days_between_deadline_and_now = datetime.datetime.combine(self.date, datetime.datetime.min.time()) - datetime.datetime.today()

        static_email_text = '''
        Hello,
        \tThis is an automated email reminder about ordering part {part_id}.  At this time only {amount}
        have been recieved and {open} are currently on route.  As of now there are less than {days} left
        before the deadline on {date} has passed.
        '''.format(open=self.open, part_id=self.id, amount=self.amount, date=str(self.date),
                   days=int(days_between_deadline_and_now.days))

        if os.path.isfile('temp_email.txt'):
            os.remove('temp_email.txt')
        with open('temp_email.txt', 'w+') as f:
            f.write(static_email_text)
            msg = MIMEText(f.read())

        msg['Subject'] = 'AUTOMATED Part Order Reminder'
        msg['From'] = SEND_EMAILS_FROM
        msg['To'] = self.email

        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()

    @staticmethod
    def convert_to_date_obj(date_str: str) -> datetime.date:
        """
        attempts to convert date string into a usable date object
        :param date_str: date string grabbed
        :return: datetime.date object
        """
        try:
            dt = parser.parse(date_str)
        except Exception as e:
            print('Unable to parse date string: %s' % date_str)
            raise

        return dt

###################
# function definitions
###################


def load_spreadsheet(file_name: str) -> pd.ExcelFile:
    """
    Loads excel spreadsheet and returns the panda excel object
    :param file_name: location of file to load in
    :return: the resulting loaded excel object
    """

    try:
        loaded_file = pd.ExcelFile(file_name)
    except Exception as e:
        print('Unable to load excel file!')
        raise

    return loaded_file


def verify_correct_sheets(excel_file: pd.ExcelFile) -> bool:
    """
    verifies we have the right sheets in our spreadsheet
    :param excel_file: loaded excel file from pandas
    :return: boolean if we have warehouse and contact
    """

    sheets = excel_file.sheet_names

    return 'Warehouse' in sheets and 'Contact' in sheets


def parse_spreadsheet(excel_file: pd.ExcelFile) -> List[Part]:
    """
    Reads the pandas excel file and extracts the relevant portions to construct
    our list of part objects
    :param excel_file: pandas excel file
    :return: list of part
    """
    pass


def __main__() -> None:
    loaded_spreadsheet = load_spreadsheet(SPREADSHEET_FILE_LOCATION)
    if not verify_correct_sheets(loaded_spreadsheet):
        print('Spreadsheet does not have requisite sheets!')
        exit(1)


__main__()
