import cv2
import mediapipe as mp
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from constants import WIDTH, HEIGHT
from round_button import RoundButton
import helpers
from game_menu_widget import GamesMenuWidget

class CameraWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_blurred = False  # Zustandsvariable für Blur-Status
        self.setup_ui()
        self.initialize_camera()
        self.setup_buttons()
        self.setup_timer()

    def initialize_camera(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)

    def setup_ui(self):
        self.image_label = QLabel(self)
        self.resize(WIDTH, HEIGHT)
        self.image_label.resize(WIDTH, HEIGHT)

    def setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)


    def setup_buttons(self):
        # Buttons Links
        self.volUpButton = RoundButton(self, hover_callback=lambda: print("Volume Up"), icon_path="../GUI/images/volume-max-svgrepo-com.png")
        self.volUpButton.move(self.volUpButton.height() // 3, self.volUpButton.height() // 3)

        self.volDownButton = RoundButton(self, hover_callback=lambda: print("Volume Down"), icon_path="../GUI/images/volume-min-svgrepo-com.png")
        self.volDownButton.move(self.volDownButton.height() // 3, self.volDownButton.height() // 3 + self.volDownButton.height() + self.volDownButton.height() // 3)

        self.muteButton = RoundButton(self, hover_callback=lambda: print("Muted"), icon_path="../GUI/images/volume-xmark-svgrepo-com.png")
        self.muteButton.move(self.muteButton.height() // 3, self.muteButton.height() // 3 + (self.muteButton.height() + self.muteButton.height() // 3) * 2)

        # Buttons Rechts
        self.endCallButton = RoundButton(self, hover_callback=lambda: print("End Call"), icon_path="../GUI/images/call-cancel-svgrepo-com.png")
        self.endCallButton.move(WIDTH - self.endCallButton.height() - (self.endCallButton.height() // 3), self.endCallButton.height() // 3)

        self.blurButton = RoundButton(self, hover_callback=lambda: self.toggle_blur(), icon_path="../GUI/images/blur-svgrepo-com.png")
        self.blurButton.move(WIDTH - self.blurButton.height() - (self.blurButton.height() // 3), self.blurButton.height() // 3 + self.muteButton.height() + self.muteButton.height() // 3)

        self.gameButton = RoundButton(self, hover_callback=lambda :self.toggle_games_menu(), icon_path="../GUI/images/controller-svgrepo-com.png")
        self.gameButton.move(WIDTH - self.gameButton.height() - (self.gameButton.height() // 3), self.gameButton.height() // 3 + (self.muteButton.height() + self.muteButton.height() // 3) * 2)

        self.closeMenuButton = RoundButton(self, hover_callback=self.toggle_games_menu, icon_path="../GUI/images/return-button-svgrepo-com.png")
        self.closeMenuButton.move(self.closeMenuButton.height()//3, self.closeMenuButton.height()//3)  # Position des Buttons anpassen
        self.closeMenuButton.hide()  # Anfangs versteckt

        self.gamesMenuWidget = GamesMenuWidget(self)  # Spiele-Menü-Widget erstellen
        self.gamesMenuWidget.setGeometry(100, 100, 300, 400)  # Position und Größe des Menüs
        self.gamesMenuWidget.setVisible(False)

        # Button-Status-Dictionary
        self.buttons = {
            'vol_up': (self.volUpButton, False),
            'vol_down': (self.volDownButton, False),
            'mute': (self.muteButton, False),
            'end_call': (self.endCallButton, False),
            'blur': (self.blurButton, False),
            'game': (self.gameButton, False),
            'back': (self.closeMenuButton,False)
        }

    def toggle_games_menu(self):
        if self.gamesMenuWidget.isVisible():
            self.gamesMenuWidget.hide()
            self.toggle_buttons_visibility(True)  # Ursprüngliche Buttons anzeigen
            self.closeMenuButton.hide()
        else:
            self.gamesMenuWidget.show()
            self.toggle_buttons_visibility(False)  # Ursprüngliche Buttons verstecken
            self.closeMenuButton.show()

    def toggle_buttons_visibility(self, visible):
        self.volUpButton.setVisible(visible)
        self.volDownButton.setVisible(visible)
        self.muteButton.setVisible(visible)
        self.endCallButton.setVisible(visible)
        self.blurButton.setVisible(visible)
        self.gameButton.setVisible(visible)

    def start(self):
        self.timer.start(30)

    def toggle_blur(self):
        self.is_blurred = helpers.toggle_blur(self.is_blurred)

    def update_image(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            hand_detected = False

            if results.multi_hand_landmarks:
                hand_detected = True
                self.process_finger_position(results, frame)

            if not hand_detected:
                self.reset_buttons_hover_status()

            self.process_display_frame(frame)

    def process_finger_position(self, results, frame):
        finger_over_button = False

        for hand_landmarks in results.multi_hand_landmarks:
            self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            for point in self.mp_hands.HandLandmark:
                if point == self.mp_hands.HandLandmark.INDEX_FINGER_TIP:
                    normalizedLandmark = hand_landmarks.landmark[point]
                    pixelCoordinatesLandmark = self.mp_drawing._normalized_to_pixel_coordinates(
                        normalizedLandmark.x, normalizedLandmark.y, WIDTH, HEIGHT)

                    if pixelCoordinatesLandmark:
                        x, y = pixelCoordinatesLandmark
                        if self.gamesMenuWidget.isVisible():
                            # Überprüfe nur den closeMenuButton, wenn das Spiele-Menü sichtbar ist
                            finger_over_button = self.update_single_button_hover_status(self.closeMenuButton, x, y)
                        else:
                            # Überprüfe alle anderen Buttons, wenn das Spiele-Menü nicht sichtbar ist
                            finger_over_button = self.update_button_hover_status(x, y)

        if not finger_over_button:
            self.reset_buttons_hover_status()

    def update_single_button_hover_status(self, button, x, y):
        if button.contains_point(x, y):
            if not button.hover_timer.isActive():
                button.start_hover_animation()
            return True
        return False

    def update_button_hover_status(self, x, y):
        for key, (button, hovered) in self.buttons.items():
            if button.contains_point(x, y):
                if not button.hover_timer.isActive():
                    button.start_hover_animation()
                return True
        return False

    def reset_buttons_hover_status(self):
        for key, (button, _) in self.buttons.items():
            button.hover_timer.stop()
            button.hover_progress = 0
            button.update()

    def process_display_frame(self, frame):
        display_frame = frame.copy()
        if self.is_blurred:
            display_frame = cv2.GaussianBlur(display_frame, (81, 81), 0)

        display_frame = cv2.resize(display_frame, (WIDTH, HEIGHT))
        image = QImage(display_frame.data, display_frame.shape[1], display_frame.shape[0], QImage.Format_BGR888)
        self.image_label.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        self.cap.release()
        self.hands.close()
