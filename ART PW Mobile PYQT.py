import sys
import random
import string
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QComboBox, QPushButton, QCheckBox, QVBoxLayout, QMessageBox, QFileDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPoint
from playwright.sync_api import sync_playwright
import os
import time

def resource_path(relative_path):
    """Ottieni il percorso delle risorse, compatibile con PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Funzione per chiedere il percorso di chrome.exe
def chiedi_chrome_path():
    file_dialog = QFileDialog()
    file_dialog.setWindowTitle("Seleziona il percorso di chrome.exe")
    file_dialog.setNameFilter("Executable Files (*.exe)")
    file_path, _ = file_dialog.getOpenFileName(
        None, "Seleziona il percorso di chrome.exe", os.path.expanduser("~"), "Executable Files (*.exe)"
    )
    if file_path:
        with open('chrome_path.txt', 'w') as file:
            file.write(file_path)
        return file_path
    else:
        QMessageBox.critical(None, "Errore", "Devi selezionare un file chrome.exe valido.")
        sys.exit()

# Funzione per ottenere il percorso di chrome.exe
def get_chrome_path():
    if os.path.exists('chrome_path.txt'):
        with open('chrome_path.txt', 'r') as file:
            return file.read().strip()
    else:
        return chiedi_chrome_path()


# Lista di user-agent mobili
mobile_user_agents = [
    "Mozilla/5.0 (Linux; Android 12; SM-G991B Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36",  # Galaxy S22
    "Mozilla/5.0 (Linux; Android 13; SM-S908B Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36",  # Galaxy S24 Ultra
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",  # iPhone 15 Pro Max
    "Mozilla/5.0 (Linux; Android 12; 2201123C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36",  # Xiaomi 12
    "Mozilla/5.0 (Linux; Android 13; 23013RK75C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36",  # Xiaomi 14
    "Mozilla/5.0 (Linux; Android 13; HUAWEI Pura 70) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36",  # Huawei Pura 70
    "Mozilla/5.0 (Linux; Android 12; LE2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36",  # OnePlus 9 Pro
    "Mozilla/5.0 (Linux; Android 13; NE2211) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36",  # OnePlus 10
    "Mozilla/5.0 (Linux; Android 13; PHN110) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36",  # OnePlus 12 Pro
]

def random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def start_registration(number_of_registrations, intervallo, email_domain, username_length_min, username_length_max, fixed_password, use_random_password, selected_language, invitation_code):
    chrome_path = get_chrome_path()
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome_path, headless=False)
        
        with open("accounts.txt", "w") as file:
            for i in range(number_of_registrations):
                if selected_language == "it":
                    url = f"https://it.bidoo.com/Invito.php?fr={invitation_code}"
                else:
                    url = f"https://es.bidoo.com/Invito.php?fr={invitation_code}"
                
                email = f"{random_string(15)}{email_domain}"
                username = random_string(random.randint(username_length_min, username_length_max))
                password = random_string(10) if use_random_password else fixed_password

                # Scrivi l'account nel file
                file.write(f"Email: {email}, Username: {username}, Password: {password}\n")

                user_agent = random.choice(mobile_user_agents)
                context = browser.new_context(
                    user_agent=user_agent,
                    viewport={"width": 375, "height": 812},  # Dimensioni di iPhone X come esempio
                    is_mobile=True,
                    has_touch=True,
                    device_scale_factor=3.0
                )
                page = context.new_page()

                try:
                    page.goto(url)
                    page.fill('xpath=//*[@id="email_signup"]', email)
                    page.fill('xpath=/html/body/div[1]/div/form/div[2]/input', username)
                    page.fill('xpath=//*[@id="password_signup"]', password)
                    page.check('xpath=/html/body/div[1]/div/form/div[4]/div/label/input')
                    page.click('xpath=/html/body/div[1]/div/form/div[4]/button/b')
                    page.wait_for_url("**/home_alt.php?onboard=false&nu=true&fr=digita qui il tuo codice d'invito", timeout=50000)
                except Exception as e:
                    QMessageBox.critical(None, "Errore", f"Errore durante la registrazione: {e}")
                
                context.close()
                if i < number_of_registrations - 1:
                    time.sleep(intervallo)
        
        browser.close()

class RegistrationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        # Variabili per tracciare il trascinamento della finestra
        self._is_dragging = False
        self._start_pos = QPoint()

        # Centra la finestra al centro dello schermo
        self.center()

    def init_ui(self):
        self.setWindowTitle("ART 0.0.1")
        self.setGeometry(200, 200, 200, 450)
        self.setWindowFlags(Qt.FramelessWindowHint)  # Rimuove i bordi della finestra
        self.setStyleSheet("background-color: rgb(230, 228, 221);")

        # Percorso relativo dell'icona
        icon_path = os.path.join(os.path.dirname(__file__), "resources", "PNG.png")
        self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout()

        # Numero di account da creare
        self.registration_count = QLineEdit(self)
        self.registration_count.setPlaceholderText("Numero di Account")
        layout.addWidget(self.registration_count)

        # Intervallo tra le registrazioni
        self.interval = QLineEdit(self)
        self.interval.setPlaceholderText("Intervallo in Secondi")
        layout.addWidget(self.interval)

        # Menu a tendina per dominio email
        self.email_domain = QComboBox(self)
        self.email_domain.addItems(["@gmail.com", "@yahoo.com", "@outlook.com"])
        layout.addWidget(self.email_domain)

        # Menu a tendina per lunghezza username
        self.username_length_min = QComboBox(self)
        self.username_length_min.addItems([str(i) for i in range(4, 9)])
        layout.addWidget(self.username_length_min)

        self.username_length_max = QComboBox(self)
        self.username_length_max.addItems([str(i) for i in range(5, 10)])
        layout.addWidget(self.username_length_max)

        # Menu a tendina per password fissa
        self.fixed_password = QLineEdit(self)
        self.fixed_password.setPlaceholderText("Password Fissa")
        layout.addWidget(self.fixed_password)

        # Checkbox per password random
        self.use_random_password = QCheckBox("Usa password casuale", self)
        layout.addWidget(self.use_random_password)

        # Selezione della lingua (it/es)
        self.selected_language = QComboBox(self)
        self.selected_language.addItems(["it", "es"])
        layout.addWidget(self.selected_language)

        # Campo di input per il codice d'invito
        self.invitation_code = QLineEdit(self)
        self.invitation_code.setPlaceholderText("Codice d'invito")
        layout.addWidget(self.invitation_code)

        # Bottone per avviare la registrazione
        start_button = QPushButton("Inizia Registrazione", self)
        start_button.clicked.connect(self.on_start_button_click)
        start_button.setStyleSheet("background-color: black; color: white;")
        layout.addWidget(start_button)

        # Bottone "X" per chiudere la finestra
        close_button = QPushButton("X", self)
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("background-color: red; color: white;")
        layout.addWidget(close_button)

        self.setLayout(layout)

    def mousePressEvent(self, event):
        """Inizia il trascinamento della finestra se si clicca su una parte vuota della GUI."""
        if event.button() == Qt.LeftButton:
            self._is_dragging = True
            self._start_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Sposta la finestra durante il trascinamento."""
        if self._is_dragging:
            self.move(event.globalPos() - self._start_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Termina il trascinamento della finestra."""
        self._is_dragging = False

    def center(self):
        """Centra la finestra al centro dello schermo."""
        screen_geometry = QApplication.desktop().screenGeometry()
        window_geometry = self.frameGeometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)

    def on_start_button_click(self):
        try:
            count = int(self.registration_count.text()) if self.registration_count.text() else 1
            intervallo = int(self.interval.text()) if self.interval.text() else 60
            email_domain = self.email_domain.currentText()
            username_length_min = int(self.username_length_min.currentText())
            username_length_max = int(self.username_length_max.currentText())
            fixed_password = self.fixed_password.text() if self.fixed_password.text() else "inserisci la tua password fissa"
            use_random_password = self.use_random_password.isChecked()
            selected_language = self.selected_language.currentText()
            invitation_code = self.invitation_code.text() if self.invitation_code.text() else "digita qui il tuo codice d'invito"

            start_registration(count, intervallo, email_domain, username_length_min, username_length_max, fixed_password, use_random_password, selected_language, invitation_code)
            QMessageBox.information(self, "Successo", f"{count} registrazioni completate.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore imprevisto: {e}")

def main():
    app = QApplication(sys.argv)
    ex = RegistrationApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
