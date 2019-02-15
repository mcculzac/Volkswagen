import pyautogui as pg

stuff = 'hello_world'


def main():
    pg.hotkey('command', 'space')

    pg.typewrite('word')
    pg.PAUSE = 1.0
    pg.keyDown('enter')
    pg.keyDown('enter')
    pg.typewrite(stuff)




main()