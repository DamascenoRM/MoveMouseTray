import pyautogui
import time
from threading import Thread, Event
from pynput import mouse, keyboard
import pystray
from PIL import Image, ImageDraw

# Configurações de inatividade
INACTIVITY_TIMEOUT = 60  # Tempo limite de inatividade em segundos
MOVE_INTERVAL = 10  # Intervalo para verificar inatividade e mover o mouse

# Estado do programa
running = True
last_activity_time = time.time()
mouse_moving = False

# Evento para controlar a pausa e retomada do movimento
stop_event = Event()


def on_move(x, y):
    global last_activity_time
    last_activity_time = time.time()


def on_click(x, y, button, pressed):
    global last_activity_time
    last_activity_time = time.time()


def on_scroll(x, y, dx, dy):
    global last_activity_time
    last_activity_time = time.time()


def on_press(key):
    global last_activity_time
    last_activity_time = time.time()


def on_release(key):
    global last_activity_time
    last_activity_time = time.time()


def move_mouse():
    global mouse_moving
    while running:
        stop_event.wait()  # Aguarda até que stop_event seja sinalizado para continuar
        if not running:
            break
        current_position = pyautogui.position()
        new_position = (current_position[0] + 10, current_position[1])

        pyautogui.moveTo(new_position, duration=0.25)
        time.sleep(0.25)
        pyautogui.moveTo(current_position, duration=0.25)
        time.sleep(MOVE_INTERVAL)


def check_inactivity():
    global mouse_moving
    while running:
        current_time = time.time()
        if current_time - last_activity_time > INACTIVITY_TIMEOUT and not mouse_moving:
            mouse_moving = True
            stop_event.set()  # Permite que o movimento do mouse continue
        else:
            mouse_moving = False
            stop_event.clear()  # Pausa o movimento do mouse
        time.sleep(1)


def create_image():
    # Cria uma imagem para o ícone da bandeja
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle(
        (width // 2 - 10, height // 2 - 10, width // 2 + 10, height // 2 + 10),
        fill=(0, 0, 0))
    return image


def start_program(icon, item):
    global running, last_activity_time
    running = True
    last_activity_time = time.time()
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
    # Configura os ouvintes para mouse e teclado
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

    mouse_listener.start()
    keyboard_listener.start()

    # Inicia as threads para monitorar inatividade e mover o mouse
    Thread(target=check_inactivity, daemon=True).start()
    Thread(target=move_mouse, daemon=True).start()

    # Configura o ícone da bandeja
    setup_tray_icon()

    # Para ouvintes ao encerrar
    mouse_listener.stop()
    keyboard_listener.stop()
