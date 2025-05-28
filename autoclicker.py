import sys
import threading
import time
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QSpinBox, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import pyautogui
from pynput import keyboard

clicking = False
click_interval = 100  # ms
click_count = 0

def log(message):
    with open("clicker_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")

def click_loop():
    global clicking, click_count
    while True:
        if clicking:
            pyautogui.click()
            click_count += 1
            log(f"Tıklama #{click_count}")
            time.sleep(click_interval / 1000.0)
        else:
            time.sleep(0.1)

def start_listener(app):
    def on_press(key):
        global clicking
        try:
            if key == keyboard.Key.f6:
                clicking = not clicking
                status = "Başladı" if clicking else "Durdu"
                log(f"Tıklama {status}")
            elif key == keyboard.Key.f9:
                log("Uygulama kapatıldı.")
                app.quit()
        except:
            pass
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

class AutoClicker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gelişmiş Autoclicker")
        self.setFixedSize(300, 200)
        self.setStyleSheet("background-color: #2d2d2d; color: white;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Autoclicker by Python")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.spin = QSpinBox()
        self.spin.setRange(10, 1000)
        self.spin.setValue(click_interval)
        self.spin.setSuffix(" ms")
        self.spin.setStyleSheet("background-color: #444; color: white; padding: 5px;")
        self.spin.valueChanged.connect(self.update_interval)

        start_label = QLabel("F6: Başlat / Durdur\nF9: Çıkış")
        start_label.setAlignment(Qt.AlignCenter)

        exit_button = QPushButton("Çıkış")
        exit_button.clicked.connect(self.close_app)
        exit_button.setStyleSheet("background-color: #b00020; color: white; padding: 5px;")

        layout.addWidget(title)
        layout.addWidget(QLabel("Tıklama Aralığı:"))
        layout.addWidget(self.spin)
        layout.addWidget(start_label)
        layout.addWidget(exit_button)

        self.setLayout(layout)

    def update_interval(self):
        global click_interval
        click_interval = self.spin.value()
        log(f"Tıklama aralığı güncellendi: {click_interval} ms")

    def close_app(self):
        log("Uygulama manuel olarak kapatıldı.")
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoClicker()
    window.show()

    # Başlatma
    log("Uygulama başlatıldı.")
    threading.Thread(target=click_loop, daemon=True).start()
    start_listener(app)

    sys.exit(app.exec_())
