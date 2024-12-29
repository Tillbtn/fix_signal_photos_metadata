import pyautogui
import time

time.sleep(5)

repeats = 3518
for i in range(repeats):
    # print(pyautogui.position())

    # pyautogui.click(3592,97)
    # time.sleep(1)
    # pyautogui.click(3461, 196)
    # time.sleep(1)
    # pyautogui.click(3533, 554)
    # time.sleep(2)
    # pyautogui.click(3479, 802)
    # time.sleep(1)

    pyautogui.moveTo(3592, 97)  # Bewege den Mauszeiger zur Position
    pyautogui.mouseDown()  # Maus "drücken"
    time.sleep(0.1)  # Haltezeit in Sekunden
    pyautogui.mouseUp()
    time.sleep(0.5)

    pyautogui.moveTo(3461, 196)  # Bewege den Mauszeiger zur Position
    pyautogui.mouseDown()  # Maus "drücken"
    time.sleep(0.1)  # Haltezeit in Sekunden
    pyautogui.mouseUp()
    time.sleep(0.5)

    pyautogui.moveTo(3533, 554)  # Bewege den Mauszeiger zur Position
    pyautogui.mouseDown()  # Maus "drücken"
    time.sleep(0.1)  # Haltezeit in Sekunden
    pyautogui.mouseUp()
    time.sleep(1)

    pyautogui.moveTo(3479, 802)  # Bewege den Mauszeiger zur Position
    pyautogui.mouseDown()  # Maus "drücken"
    time.sleep(0.1)  # Haltezeit in Sekunden
    pyautogui.mouseUp()
    time.sleep(0.5)

    print(f"Foto {i+1} von {repeats} gesichert")

