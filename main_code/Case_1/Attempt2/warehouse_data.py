#####################
# Kevin Gu
# gukailia@msu.edu
# 2018-2-20
#####################


##################
# import
##################

from tools import open_file_on_desktop
from tools import goto_cell, goto_sheet, create_sheet, delete_cols, goto_term, read_cell, repeated_press
from tools import grab_clipboard
import pyautogui


def send_email(email_address, total):
    print('I had send an email to email_address ', email_address, 'about the missing total of ', total, ' .')


def main():
    open_file_on_desktop("ex_1.xlsx")

    create_sheet('cals')
    pyautogui.hotkey('ctrl', '`')
    goto_sheet("Warehouse")
    goto_term("Part")
    pyautogui.hotkey('ctrl', 'space')
    pyautogui.hotkey('ctrl', 'c')
    goto_sheet("cals")
    goto_cell('a', 1)
    pyautogui.hotkey('ctrl', 'v')
    goto_cell('b', 1)
    pyautogui.typewrite('=COUNTA(A1:A1000)')
    pyautogui.press('enter')
    pyautogui.press('up')
    total_items = int(read_cell())

    pyautogui.press('alt')
    pyautogui.press('e')
    pyautogui.press('l')
    pyautogui.press('enter')

    goto_sheet("Warehouse")
    goto_term('open')
    pyautogui.press('right')
    pyautogui.typewrite('calculation')
    pyautogui.press('down')
    for _ in range(total_items-1):
        pyautogui.typewrite('=')
        repeated_press('left', 2)
        pyautogui.typewrite('-')
        pyautogui.press('left')
        pyautogui.press('enter')

    goto_term('calculation')
    pyautogui.press('right')
    pyautogui.typewrite('total')
    goto_term('part')
    count = 1
    pyautogui.press('down')
    pyautogui.hotkey('ctrl', 'c')
    part_next = str(grab_clipboard())
    for _ in range(total_items-1):
        part = str(part_next)

        pyautogui.press('down')
        pyautogui.hotkey('ctrl', 'c')
        part_next = str(grab_clipboard())

        if part == part_next:
            count = count + 1
        else:
            pyautogui.press('up')
            repeated_press('right', 9)
            pyautogui.typewrite('=')
            # pyautogui.press('left')
            if count == 1:
                pyautogui.press('left')
            else:
                pyautogui.press('left')
                for _ in range(1, count):
                    pyautogui.typewrite('+')
                    pyautogui.press('left')
                    repeated_press('up', _)
            pyautogui.press('enter')

            repeated_press('left', 9)
            count = 1

    goto_term('total')
    for _ in range(total_items-1):
        pyautogui.press('down')
        # pyautogui.hotkey('ctrl', 'c')
        try:
            total = int(read_cell())
            if total > 0:
                repeated_press('left', 9)
                pyautogui.hotkey('ctrl', 'c')
                part_id = str(grab_clipboard())
                goto_sheet('Contact')
                pyautogui.hotkey('ctrl', 'f')
                pyautogui.typewrite(part_id)
                pyautogui.PAUSE = 0.5
                pyautogui.press('esc')
                repeated_press('right', 4)
                pyautogui.hotkey('ctrl', 'c')
                email = str(grab_clipboard())
                send_email(email, total)
                goto_sheet('Warehouse')
                goto_term('total')
                repeated_press('down', _+1)

        except Exception as e:
            pass




















main()