import cv2
import numpy as np
import zmq
import mediapipe as mp
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from constants import WIDTH, HEIGHT
from round_button import RoundButton
import helpers
from game_menu_widget import GamesMenuWidget


class CameraWidget(QWidget):
    def __init__(self, parent=None, peer_ip='tcp://localhost:5556'):
        super().__init__(parent)
        self.is_blurred = False  # Zustandsvariable für Blur-Status
        self.setup_ui()
        self.initialize_camera()
        self.setup_buttons()
        self.setup_timer()
        self.setup_zmq(peer_ip)

    def setup_ui(self):
        self.image_label = QLabel(self)
        self.resize(WIDTH, HEIGHT)
        self.image_label.resize(WIDTH, HEIGHT)

    def initialize_camera(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)

    def setup_zmq(self, peer_ip):
        self.context = zmq.Context()
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind('tcp://*:5555')  # Dieser Peer bindet auf Port 5555
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.connect(peer_ip)  # Verbindet zum anderen Peer
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, '')

    def setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)  # Fix: do not call the method, just reference it
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Start the timer to update frame every 30 ms

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.stream_frame(self.process_streaming_frame(frame_rgb))
            self.display_frame()

    def stream_frame(self, frame):
        _, buffer = cv2.imencode('.jpg', frame)
        self.pub_socket.send(buffer.tobytes())

    def display_frame(self):
        try:
            frame_bytes = self.sub_socket.recv(zmq.NOBLOCK)  # Non-blocking receive
            npimg = np.frombuffer(frame_bytes, dtype=np.uint8)
            frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pix = QPixmap.fromImage(image)
            self.image_label.setPixmap(pix)
        except zmq.Again:
            pass  # No frame received

    def closeEvent(self, event):
        self.cap.release()
        self.pub_socket.close()
        self.sub_socket.close()
        self.context.term()
        super().closeEvent(event)  # Ensure the parent close event is also called




    def setup_buttons(self):
        # Buttons Links
        self.volUpButton = RoundButton(self, hover_callback=lambda: print("Volume Up"),
                                       icon_path="../GUI/images/volume-max-svgrepo-com.png")
        self.volUpButton.move(self.volUpButton.height() // 3, self.volUpButton.height() // 3)

        self.volDownButton = RoundButton(self, hover_callback=lambda: print("Volume Down"),
                                         icon_path="../GUI/images/volume-min-svgrepo-com.png")
        self.volDownButton.move(self.volDownButton.height() // 3,
                                self.volDownButton.height() // 3 + self.volDownButton.height() + self.volDownButton.height() // 3)

        self.muteButton = RoundButton(self, hover_callback=lambda: print("Muted"),
                                      icon_path="../GUI/images/volume-xmark-svgrepo-com.png")
        self.muteButton.move(self.muteButton.height() // 3, self.muteButton.height() // 3 + (
                    self.muteButton.height() + self.muteButton.height() // 3) * 2)

        # Buttons Rechts
        self.endCallButton = RoundButton(self, hover_callback=lambda: print("End Call"),
                                         icon_path="../GUI/images/call-cancel-svgrepo-com.png")
        self.endCallButton.move(WIDTH - self.endCallButton.height() - (self.endCallButton.height() // 3),
                                self.endCallButton.height() // 3)

        self.blurButton = RoundButton(self, hover_callback=lambda: self.toggle_blur(),
                                      icon_path="../GUI/images/blur-svgrepo-com.png")
        self.blurButton.move(WIDTH - self.blurButton.height() - (self.blurButton.height() // 3),
                             self.blurButton.height() // 3 + self.muteButton.height() + self.muteButton.height() // 3)

        self.gameButton = RoundButton(self, hover_callback=lambda: self.toggle_games_menu(),
                                      icon_path="../GUI/images/controller-svgrepo-com.png")
        self.gameButton.move(WIDTH - self.gameButton.height() - (self.gameButton.height() // 3),
                             self.gameButton.height() // 3 + (
                                         self.muteButton.height() + self.muteButton.height() // 3) * 2)

        self.closeMenuButton = RoundButton(self, hover_callback=self.toggle_games_menu,
                                           icon_path="../GUI/images/return-button-svgrepo-com.png")
        self.closeMenuButton.move(self.closeMenuButton.height() // 3,
                                  self.closeMenuButton.height() // 3)  # Position des Buttons anpassen
        self.closeMenuButton.hide()  # Anfangs versteckt

        self.gamesMenuWidget = GamesMenuWidget(self)  # Spiele-Menü-Widget erstellen
        self.gamesMenuWidget.setGeometry(0, 0, WIDTH, HEIGHT)  # Position und Größe des Menüs
        self.gamesMenuWidget.setVisible(False)

        #Buttons im GamesMenu

        # Button-Status-Dictionary
        self.buttons = {
            'vol_up': (self.volUpButton, False),
            'vol_down': (self.volDownButton, False),
            'mute': (self.muteButton, False),
            'end_call': (self.endCallButton, False),
            'blur': (self.blurButton, False),
            'game': (self.gameButton, False),
            'back': (self.closeMenuButton, False)
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
                # Process finger positions without drawing landmarks yet
                self.process_finger_position(results, frame)

            # Prepare display frame
            display_frame = frame.copy()  # Make a copy for drawing and blurring
            if hand_detected:
                self.draw_landmarks(display_frame, results)

            self.process_display_frame(display_frame)  # Pass the display frame with drawings
#HIER            stream_frame = self.process_streaming_frame(frame)
         #   self.image_label.setPixmap(QPixmap.fromImage(stream_frame))

    def process_finger_position(self, results, frame):
        finger_over_button = False
        for hand_landmarks in results.multi_hand_landmarks:
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

    def draw_landmarks(self, frame, results):
        # Draw landmarks on the frame that will be displayed
        for hand_landmarks in results.multi_hand_landmarks:
            self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

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
        # Apply any visual effects like blurring
        if self.is_blurred:
            frame = cv2.GaussianBlur(frame, (81, 81), 0)

        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
        self.image_label.setPixmap(QPixmap.fromImage(image))

    def process_streaming_frame(self, frame):
        # Apply any visual effects like blurring
        if self.is_blurred:
            frame = cv2.GaussianBlur(frame, (81, 81), 0)

        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
        return frame

    def closeEvent(self, event):
        self.cap.release()
        self.hands.close()
