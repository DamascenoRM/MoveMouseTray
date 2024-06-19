import random
import time
import json
import os
from threading import Thread, Event
import ctypes
import tkinter as tk
from tkinter import ttk

import pyautogui
import pystray
from PIL import Image, ImageDraw
from pynput import mouse, keyboard

# Caminho do arquivo de configuração
CONFIG_FILE = 'config.json'

# Configurações padrão
DEFAULT_CONFIG = {
    'INACTIVITY_TIMEOUT': 60,  # Tempo limite de inatividade em segundos
    'MOVE_INTERVAL': 10,  # Intervalo para verificar inatividade e mover o mouse
    'MULTI_MOVE_COUNT': 2,  # Quantidade de movimentos múltiplos do mouse
    'ALLOW_SCREEN_LOCK': False,  # Permitir tela de bloqueio
    'ALLOW_HIBERNATION': False,  # Permitir hibernação
    'ALLOW_SLEEP': False,  # Permitir suspensão
    'ENABLE_MOUSE_MOVEMENT': True,  # Ativar movimento do mouse
    'ENABLE_MULTI_MOVE': True  # Ativar movimentos múltiplos do mouse
}


# Carregar configurações
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        return DEFAULT_CONFIG


# Salvar configurações
def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)


# Carrega as configurações atuais
config = load_config()

# Descompacta as configurações carregadas
INACTIVITY_TIMEOUT = config['INACTIVITY_TIMEOUT']
MOVE_INTERVAL = config['MOVE_INTERVAL']
MULTI_MOVE_COUNT = config['MULTI_MOVE_COUNT']
ALLOW_SCREEN_LOCK = config['ALLOW_SCREEN_LOCK']
ALLOW_HIBERNATION = config['ALLOW_HIBERNATION']
ALLOW_SLEEP = config['ALLOW_SLEEP']
ENABLE_MOUSE_MOVEMENT = config['ENABLE_MOUSE_MOVEMENT']
ENABLE_MULTI_MOVE = config['ENABLE_MULTI_MOVE']

# Estado do programa
running = True
last_activity_time = time.time()
mouse_moving = False

# Evento para controlar a pausa e retomada do movimento
stop_event = Event()

# Definição das constantes
ES_CONTINUOUS = 0x80000000
ES_DISPLAY_REQUIRED = 0x00000002
ES_SYSTEM_REQUIRED = 0x00000001


def set_thread_execution_state():
    flags = ES_CONTINUOUS
    if not ALLOW_SCREEN_LOCK:
        flags |= ES_DISPLAY_REQUIRED
    if not ALLOW_HIBERNATION or not ALLOW_SLEEP:
        flags |= ES_SYSTEM_REQUIRED
    ctypes.windll.kernel32.SetThreadExecutionState(flags)


# Previne o sistema de entrar em suspensão inicial
set_thread_execution_state()


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
        if not running or not ENABLE_MOUSE_MOVEMENT:
            break

        for _ in range(MULTI_MOVE_COUNT if ENABLE_MULTI_MOVE else 1):
            if not running or not ENABLE_MOUSE_MOVEMENT:
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
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)  # Reseta o estado do sistema


def open_configurator(icon, item):
    def save_config_and_close():
        global INACTIVITY_TIMEOUT, MOVE_INTERVAL, MULTI_MOVE_COUNT, ALLOW_SCREEN_LOCK, ALLOW_HIBERNATION, ALLOW_SLEEP, ENABLE_MOUSE_MOVEMENT, ENABLE_MULTI_MOVE

        INACTIVITY_TIMEOUT = int(inactivity_timeout_var.get())
        MOVE_INTERVAL = int(move_interval_var.get())
        MULTI_MOVE_COUNT = int(multi_move_count_var.get())
        ALLOW_SCREEN_LOCK = allow_screen_lock_var.get()
        ALLOW_HIBERNATION = allow_hibernation_var.get()
        ALLOW_SLEEP = allow_sleep_var.get()
        ENABLE_MOUSE_MOVEMENT = enable_mouse_movement_var.get()
        ENABLE_MULTI_MOVE = enable_multi_move_var.get()

        # Salva as configurações no arquivo
        current_config = {
            'INACTIVITY_TIMEOUT': INACTIVITY_TIMEOUT,
            'MOVE_INTERVAL': MOVE_INTERVAL,
            'MULTI_MOVE_COUNT': MULTI_MOVE_COUNT,
            'ALLOW_SCREEN_LOCK': ALLOW_SCREEN_LOCK,
            'ALLOW_HIBERNATION': ALLOW_HIBERNATION,
            'ALLOW_SLEEP': ALLOW_SLEEP,
            'ENABLE_MOUSE_MOVEMENT': ENABLE_MOUSE_MOVEMENT,
            'ENABLE_MULTI_MOVE': ENABLE_MULTI_MOVE
        }
        save_config(current_config)

        # Atualiza o estado do sistema com as novas configurações
        set_thread_execution_state()

        config_window.destroy()

    config_window = tk.Tk()
    config_window.title("Configurador")

    ttk.Label(config_window, text="Tempo de inatividade (segundos):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    inactivity_timeout_var = tk.StringVar(value=str(INACTIVITY_TIMEOUT))
    ttk.Entry(config_window, textvariable=inactivity_timeout_var).grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(config_window, text="Intervalo entre movimentos (segundos):").grid(row=1, column=0, padx=10, pady=5,
                                                                                 sticky="w")
    move_interval_var = tk.StringVar(value=str(MOVE_INTERVAL))
    ttk.Entry(config_window, textvariable=move_interval_var).grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(config_window, text="Quantidade de movimentos múltiplos do mouse:").grid(row=2, column=0, padx=10, pady=5,
                                                                                       sticky="w")
    multi_move_count_var = tk.StringVar(value=str(MULTI_MOVE_COUNT))
    ttk.Entry(config_window, textvariable=multi_move_count_var).grid(row=2, column=1, padx=10, pady=5)

    allow_screen_lock_var = tk.BooleanVar(value=ALLOW_SCREEN_LOCK)
    ttk.Checkbutton(config_window, text="Permitir tela de bloqueio", variable=allow_screen_lock_var).grid(row=3,
                                                                                                          column=0,
                                                                                                          padx=10,
                                                                                                          pady=5,
                                                                                                          sticky="w")

    allow_hibernation_var = tk.BooleanVar(value=ALLOW_HIBERNATION)
    ttk.Checkbutton(config_window, text="Permitir hibernação", variable=allow_hibernation_var).grid(row=4, column=0,
                                                                                                    padx=10, pady=5,
                                                                                                    sticky="w")

    allow_sleep_var = tk.BooleanVar(value=ALLOW_SLEEP)
    ttk.Checkbutton(config_window, text="Permitir suspensão", variable=allow_sleep_var).grid(row=5, column=0, padx=10,
                                                                                             pady=5, sticky="w")

    enable_mouse_movement_var = tk.BooleanVar(value=ENABLE_MOUSE_MOVEMENT)
    ttk.Checkbutton(config_window, text="Ativar movimento do mouse", variable=enable_mouse_movement_var).grid(row=6,
                                                                                                              column=0,
                                                                                                              padx=10,
                                                                                                              pady=5,
                                                                                                              sticky="w")

    enable_multi_move_var = tk.BooleanVar(value=ENABLE_MULTI_MOVE)
    ttk.Checkbutton(config_window, text="Ativar movimentos múltiplos do mouse", variable=enable_multi_move_var).grid(
        row=7, column=0, padx=10, pady=5, sticky="w")

    ttk.Button(config_window, text="Salvar", command=save_config_and_close).grid(row=8, column=0, columnspan=2, padx=10,
                                                                                 pady=10)

    config_window.mainloop()


def setup_tray_icon():
    image = create_image()
    menu = pystray.Menu(
        pystray.MenuItem('Start', start_program),
        pystray.MenuItem('Stop', stop_program),
        pystray.MenuItem('Configurador', open_configurator),
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
