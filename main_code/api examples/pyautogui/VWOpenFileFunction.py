import pyautogui as p

p.press('win')

p.typewrite('sample.xlsx',interval=0.35)
p.PAUSE = 5
p.press('enter')





b = p.locateOnScreen('k5.pnp')
p.click(p.center(b))

