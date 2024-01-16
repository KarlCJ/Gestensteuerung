import sys
import cv2
import mediapipe as mp
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QTimer
width = 800
height = 600
class RoundButton(QPushButton):
    def __init__(self, parent=None, hover_callback=None):
        super().__init__(parent)
        self.setFixedSize(60, 60)
        self.animation_duration = 1500  # Gesamtdauer der Animation in Millisekunden
        self.hover_timer = QTimer(self)
        self.hover_progress = 0
        self.hover_timer.timeout.connect(self.update_hover_progress)
        self.hover_callback = hover_callback

    def contains_point(self, x, y):
        # Überprüfen, ob der Punkt (x, y) innerhalb des Buttons liegt
        button_rect = self.geometry()
        return button_rect.contains(x, y)

    def start_hover_animation(self):
        if not self.hover_timer.isActive():
            self.hover_timer.start(30)
            self.hover_progress = 0

    def update_hover_status(self, is_hovering):
        if is_hovering:
            if not self.hover_timer.isActive():
                self.start_hover_animation()
        else:
            if self.hover_timer.isActive():
                self.hover_timer.stop()
                self.hover_progress = 0
                self.update()

    def set_hover_callback(self, callback):
        self.hover_callback = callback

    def update_hover_progress(self):
        increment = self.hover_timer.interval() / self.animation_duration
        self.hover_progress += increment
        if self.hover_progress >= 1:
            self.hover_timer.stop()
            self.hover_progress = 1
            self.hover_callback()  # Aufrufen der Callback-Funktion
            self.update()  # Aktualisiert das Aussehen des Buttons

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Grundlegender grauer Button
        painter.setBrush(QBrush(QColor(200, 200, 200, 128)))  # Grauer Hintergrund
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())

        # Heller blauer Hover-Effekt
        if self.hover_progress > 0:
            painter.setBrush(QBrush(QColor(30, 144, 255, int(128 * self.hover_progress))))  # Hellblau mit Transparenz
            painter.setPen(Qt.NoPen)
            radius = int(self.width() / 2 * self.hover_progress)
            painter.drawEllipse(self.width() // 2 - radius, self.height() // 2 - radius, radius * 2, radius * 2)

    def enterEvent(self, event):
        self.hover_timer.start(40)  # Du kannst hier ein anderes Intervall einstellen, falls nötig
        self.hover_progress = 0

    def leaveEvent(self, event):
        self.hover_timer.stop()
        self.hover_progress = 0
        self.update()  # Setzt den Button auf den ursprünglichen Zustand zurück


class CameraWidget(QWidget):
    def __init__(self, parent=None):


        super().__init__(parent)
        self.image_label = QLabel(self)
        self.resize(width, height)
        self.image_label.resize(width, height)

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.cap = cv2.VideoCapture(0)

        self.button1 = RoundButton(self, hover_callback=lambda:print("Button 1 Aktiviert"))
        self.button1.move(self.button1.height()//3, self.button1.height()//3)
        self.button2 = RoundButton(self,hover_callback=lambda:print("Button 2 Aktiviert"))
        self.button2.move(width-self.button2.height()-(self.button2.height()//3), self.button2.height()//3)



    def start(self):
        self.timer.start(30)

    def update_image(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)
            button1_hovered = False
            button2_hovered = False

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                    # Koordinaten des Zeigefingers erfassen
                    for point in self.mp_hands.HandLandmark:
                        if point == self.mp_hands.HandLandmark.INDEX_FINGER_TIP:
                            normalizedLandmark = hand_landmarks.landmark[point]
                            pixelCoordinatesLandmark = self.mp_drawing._normalized_to_pixel_coordinates(
                                normalizedLandmark.x, normalizedLandmark.y, width, height)

                            if pixelCoordinatesLandmark:
                                x, y = pixelCoordinatesLandmark
                                # Überprüfe die Kollision mit Buttons
                                if self.button1.contains_point(x, y):
                                    button1_hovered = True
                                if self.button2.contains_point(x, y):
                                    button2_hovered = True
                # Aktualisiere den Hover-Status der Buttons basierend auf der Fingerposition
            self.button1.update_hover_status(button1_hovered)
            self.button2.update_hover_status(button2_hovered)

            frame = cv2.resize(frame, (width, height))
            image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
            self.image_label.setPixmap(QPixmap.fromImage(image))


    def closeEvent(self, event):
        self.cap.release()
        self.hands.close()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, width, height)
        self.setWindowTitle('Python Camera UI')
        self.camera_widget = CameraWidget(self)
        self.camera_widget.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
