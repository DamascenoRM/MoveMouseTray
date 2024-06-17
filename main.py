import random
import time
from threading import Thread, Event

import pyautogui
import pystray
from PIL import Image, ImageDraw
from pynput import mouse, keyboard

# Configurações de inatividade
INACTIVITY_TIMEOUT = 60  # Tempo limite de inatividade em segundos
MOVE_INTERVAL = 10  # Intervalo para verificar inatividade e mover o mouse

# Estado do programa
running = True
last_activity_time = time.time()
mouse_moving = False

# Evento para controlar a pausa e retomada do movimento
stop_event = Event()


def on_activity(x=None, y=None, button=None, pressed=None, key=None):
    global last_activity_time, mouse_moving
    last_activity_time = time.time()
    if mouse_moving:
        mouse_moving = False
        stop_event.clear()


def move_mouse():
    global mouse_moving
    while running:
        stop_event.wait()  # Aguarda até que stop_event seja sinalizado para continuar
        if not running:
            break

        # Pega a posição atual do mouse
        current_position = pyautogui.position()

        # Gera uma nova posição aleatória para mover o mouse
        x_random = random.randint(-100, 100)
        y_random = random.randint(-100, 100)
        new_position = (current_position[0] + x_random, current_position[1] + y_random)

        # Move o mouse para a nova posição aleatória
        pyautogui.moveTo(new_position, duration=0.25)
        time.sleep(0.25)

        # Gera outra posição aleatória para mover o mouse de volta
        x_random = random.randint(-100, 100)
        y_random = random.randint(-100, 100)
        final_position = (new_position[0] + x_random, new_position[1] + y_random)

        # Move o mouse para a posição final aleatória
        pyautogui.moveTo(final_position, duration=0.25)
        time.sleep(MOVE_INTERVAL)


def check_inactivity():
    global mouse_moving
    while running:
        if time.time() - last_activity_time > INACTIVITY_TIMEOUT:
            mouse_moving = True
            stop_event.set()  # Permite que o movimento do mouse continue
        else:
            stop_event.clear()  # Pausa o movimento do mouse
        time.sleep(1)


def create_image():
    width, height = 64, 64
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((width // 2 - 10, height // 2 - 10, width // 2 + 10, height // 2 + 10), fill=(0, 0, 0))
    return image


def start_program(icon, item):
    global running
    running = True
    stop_event.clear()


def stop_program(icon, item):
    global running
    running = False
    stop_event.set()


def quit_program(icon, item):
    icon.stop()
    global running
    running = False
    stop_event.set()


def setup_tray_icon():
    image = create_image()
    menu = pystray.Menu(
        pystray.MenuItem('Start', start_program),
        pystray.MenuItem('Stop', stop_program),
        pystray.MenuItem('Quit', quit_program)
    )
    icon = pystray.Icon("mouse_mover", image, "Mouse Mover", menu)
    icon.run()


if __name__ == "__main__":
    mouse_listener = mouse.Listener(on_move=on_activity, on_click=on_activity, on_scroll=on_activity)
    keyboard_listener = keyboard.Listener(on_press=on_activity, on_release=on_activity)

    mouse_listener.start()
    keyboard_listener.start()

    Thread(target=check_inactivity, daemon=True).start()
    Thread(target=move_mouse, daemon=True).start()

    setup_tray_icon()

    mouse_listener.stop()
    keyboard_listener.stop()
