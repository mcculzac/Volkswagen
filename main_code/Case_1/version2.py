
###################
# Zac McCullough
# mccul157@msu.edu

# Maryam Irannejadnajafabdi
# irannej1@msu.edu
# 1/15
###################


###################
# imports
###################

from typing import Tuple, List, Any
import pandas as pd
import datetime
from dateutil import parser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging
import pyautogui as p
# import pandas as pd
import win32clipboard as clip
###################
# global vars
###################

SPREADSHEET_FILE_LOCATION = 'ex_1.xlsx'
SEND_EMAILS_FROM = 'kevin694026728@gmail.com'
DEBUG_VAR = True


###################
# classes
###################


class Part(object):

    def __init__(self, part_id, date, amount, open, contact, from_email, server) -> None:
        self.id = part_id
        self.date = self.convert_to_date_obj(date)
        self.amount = amount
        self.open = open
        self.email = contact
        self.from_email = from_email
        self.server = server

    def __repr__(self):
        return('ID: {id}, Due: {date}, Recieved: {amount}, '
              'In-Shipping: {open}, Contact: {email}, Send From: {from_email}'.format(
               id=self.id, date=self.date, amount=self.amount, open=self.open, email=self.email,
               from_email=self.from_email
        ))

    def check_if_action_required(self) -> bool:
        """
        Determines if action is required based on date and value of open and amount
        :return: bool
        """

        current_time = datetime.datetime.today()

        # we store our date as an object called date, but datetime uses objects called datetime
        # so we use .combine our date object with the minimal time interval to get the right
        # kind of object
        if datetime.datetime.combine(self.date,
                                     datetime.datetime.min.time()) - datetime.timedelta(days=5) <= current_time:
            return True
        return False

    def send_email(self) -> None:
        """
        Sends email with the part ID, how many ordered, how many still accepting as reminder
        :return: None
        """

        # just like earlier we use this to convert date into datetime
        days_between_deadline_and_now = datetime.datetime.combine(
            self.date, datetime.datetime.min.time()) - datetime.datetime.today()

        static_email_text = '''
        Hello,
        \tThis is an automated email reminder about ordering part {part_id}.  At this time only {amount}
        have been recieved and {open} are currently on route.  As of now there are less than {days} left
        before the deadline on {date} has passed.
        '''.format(open=self.open, part_id=self.id, amount=self.amount, date=str(self.date),
                   days=int(days_between_deadline_and_now.days))

        msg = MIMEMultipart()
        msg['Subject'] = 'AUTOMATED Part Order Reminder'
        msg['From'] = self.from_email
        msg['To'] = self.email
        # msg.attach(static_email_text)
        body = MIMEText(static_email_text)
        msg.attach(body)

        self.server.sendmail(self.from_email, self.email, msg.as_string())

    @staticmethod
    def convert_to_date_obj(date_str: Any) -> datetime.date:
        """
        attempts to convert date string into a usable date object
        :param date_str: date string grabbed
        :return: datetime.date object
        """

        if type(date_str) is datetime.datetime:
            return date_str
        try:
            dt = parser.parse(date_str)
        except Exception as e:
            print('Unable to parse date string: %s' % date_str)
            logging.exception('Unable to convert date!')
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
        logging.exception('Unable to load spreadsheet!')
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


def parse_spreadsheet(warehouse_sheet, contact_sheet, send_from_email: str, server, DEBUG: bool=False) -> List[Part]:
    """
    Reads the pandas excel file and extracts the relevant portions to construct
    our list of part objects
    :param excel_file: pandas excel file
    :return: list of part
    """



    # var def
    part_col = None
    date_col = None
    amount_col = None
    open_col = None
    contact_part_id = None
    contact_email = None

    # print(warehouse_sheet)

    # separate sheet into the corresponding columns we care about
    # for col in warehouse_sheet:
    #     for val in warehouse_sheet[col]:
    #         if val == 'Part':
    #             part_col = warehouse_sheet[col]
    #             break
    #         elif val == 'date':
    #             date_col = warehouse_sheet[col]
    #             break
    #         elif val == 'amount':
    #             amount_col = warehouse_sheet[col]
    #             break
    #         elif val == 'open':
    #             open_col = warehouse_sheet[col]
    #             break
    part_col = warehouse_sheet[0]
    date_col = warehouse_sheet[6]
    amount_col = warehouse_sheet[7]
    open_col = warehouse_sheet[8]
    # do the same as above but for the contact sheet
    # for col in contact_sheet:
    #     if contact_sheet[col][0] == 'Part-ID':
    #         contact_part_id = contact_sheet[col]
    #         continue
    #     elif contact_sheet[col][0] == 'email':
    #         contact_email = contact_sheet[col]
    #         continue
    contact_part_id = contact_sheet[0]
    contact_email = contact_sheet[4]


    # find first actual part stripping out other things
    first_actual_val = 0
    part_vals = part_col.values
    for val in part_vals:
        first_actual_val += 1
        if val == 'Part':
            break
    # print('first_actual_val: ' + str(first_actual_val))

    # # find first actual part stripping out other things
    # first_contact_val = 0
    # contact_vals = contact_part_id.values
    # for val in contact_vals:
    #     first_contact_val += 1
    #     if val == 'Part-ID':
    #         break
    

    # construct a dictionary that has every part id corresponding to an email address
    part_to_email_dict = {}
    for i in range(0, len(contact_part_id)):
        part_to_email_dict[contact_part_id[i]] = contact_email[i]

    # check if debug is defined above
    # by doing this we make this function independent of our gloval variable

    # if we are debugging, then set our output email to be the same as our source email.
    if DEBUG:
        keys = part_to_email_dict.keys()
        for key in keys:
            part_to_email_dict[key] = send_from_email

    # construct our part list
    part_list = []
    for i in range(first_actual_val, len(part_col)):
        try:
            part_list.append(Part(part_col.iloc[i], date_col.iloc[i], amount_col.iloc[i], open_col.iloc[i], part_to_email_dict[part_col.iloc[i]],
                             send_from_email, server))
        except KeyError as e:
            print('Error: ' + str(e) + ' was not found!')
            logging.exception('Error: ' + str(e) + ' was not found!')

    return part_list


def start_mail_server():
    server = smtplib.SMTP('smtp.gmail.com', 587)  # port 465 or 587
    server.ehlo()
    server.starttls()
    server.ehlo()
    logging.info('Starting SMTP server...')
    try:
        server.login('kevin694026728@gmail.com', 'fjydklnsatjiwfcr')
    except Exception as e:
        logging.exception('Failed!')
        raise

    return server

######################33

def open_sample_file(file_name):
    """
    opne sample.xlsx file
    :return: None
    """

    p.press('win')
    p.typewrite(file_name, interval=0.35)
    p.PAUSE = 2.5
    p.press('enter')

def select_sheet_data(pic_name):

    pic_location = p.locateOnScreen(pic_name)
    p.click(p.center(pic_location))

    p.PAUSE = 0.8
    p.hotkey('ctrl', 'a')
    p.hotkey('ctrl', 'c')




def clipboard_():

    clip.OpenClipboard()
    data = clip.GetClipboardData()
    clip.CloseClipboard()

    temp = []
    temp2 = []

    temp = data.split('\n')
    for val in temp:
        temp2.append(val.split('\t'))

    temp2.pop()
    df = pd.DataFrame(temp2)
    return (df)







####################################
def __main__() -> None:
    # enable logging
    logging.basicConfig(filename='reminder.log', level=logging.DEBUG)

    # loaded_spreadsheet = load_spreadsheet(SPREADSHEET_FILE_LOCATION)
    # if not verify_correct_sheets(loaded_spreadsheet):
    #     print('Spreadsheet does not have requisite sheets!')
    #     exit(1)
    open_sample_file('sample.xlsx')
    select_sheet_data('warehousetab.png')
    warehouse_file = clipboard_()
    select_sheet_data('contactTab.PNG')
    contact_file = clipboard_()
    print(contact_file)
    print("Here is email: ",contact_file[4][0])
    for col in contact_file:
        print("Here is col number: ",col)

    server = start_mail_server()
    part_list = parse_spreadsheet(warehouse_file,contact_file,SEND_EMAILS_FROM, server, DEBUG_VAR)

    # print(warehouse_file[2][2])
    # for col in warehouse_file:
    #     print(col)
    for p in part_list:
        print(p)
    email_count = 1
    logging.info('Sending out emails:')
    for i, part in enumerate(part_list):
        if part.check_if_action_required():
            logging.info('Sending email #{i}'.format(i=email_count))
            part.send_email()
            email_count += 1

    logging.info('Shutting down SMTP server.')
    server.close()


__main__()
