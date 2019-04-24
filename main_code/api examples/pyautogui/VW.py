import pyautogui as p
import pandas as pd
import win32clipboard as clip





def open_sample_file():
    """
    opne sample.xlsx file
    :return: None
    """

    p.press('win')
    p.typewrite('sample.xlsx', interval=0.35)
    p.PAUSE = 3
    p.press('enter')

    # get the screen coordinates
    warehouse_location = p.locateOnScreen('warehousetab.png')

    # get the X and Y coordinates at the center of this region.
    p.click(p.center(warehouse_location))

    p.PAUSE = 1
    p.hotkey('ctrl', 'a')
    p.hotkey('ctrl', 'c')

# def load_xl():
# #     """
# #         opne sample.xlsx file
# #         :return: None
# #         """
# #     xl_file = pd.ExcelFile('C:/Users/Maryam/Desktop/sample.xlsx')
# #
# #     if not xl_file:
# #         print("File not found!")
# #
# #     Warehouse_sheet = xl_file.parse('Warehouse') # pars the Warehouse sheet from sample.xlsx file
# #
# # open_sample_file()

def clipboard_():
    clip.OpenClipboard()
    clip.EmptyClipboard()


