import sys
import cv2
import mediapipe as mp
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QBrush, QIcon, QPainterPath
from PyQt5.QtCore import Qt, QTimer, QSize

width = 800
height = 600
class RoundButton(QPushButton):
    def __init__(self, parent=None, hover_callback=None, icon_path=None):
        super().__init__(parent)
        self.setFixedSize(60, 60)
        self.animation_duration = 1500  # Gesamtdauer der Animation in Millisekunden
        self.hover_timer = QTimer(self)
        self.hover_progress = 0
        self.hover_timer.timeout.connect(self.update_hover_progress)
        self.hover_callback = hover_callback

        # Icon hinzufügen, falls ein Pfad angegeben wurde
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(40, 40))  # Größe des Icons anpassen

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
        button_rect=self.rect()
        # Zeichne das Icon
        if self.icon():
            icon_rect = button_rect.adjusted(10, 10, -10, -10)  # Hier kannst du die Größe des Icons anpassen
            self.icon().paint(painter, icon_rect, Qt.AlignCenter)

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

        self.is_blurred = False  # Zustandsvariable für Blur-Status


        # Buttons Links
        self.volUpButton = RoundButton(self, hover_callback=lambda:print("Volume Up"), icon_path="../GUI/images/volume-max-svgrepo-com.png")
        self.volUpButton.move(self.volUpButton.height() // 3, self.volUpButton.height() // 3)
        self.volDownButton = RoundButton(self, hover_callback=lambda: print("Volume Down"), icon_path="../GUI/images/volume-min-svgrepo-com.png")
        self.volDownButton.move(self.volDownButton.height() // 3, self.volDownButton.height() // 3 + self.volDownButton.height()+self.volDownButton.height()//3)
        self.muteButton = RoundButton(self, hover_callback=lambda: print("Muted"), icon_path="../GUI/images/volume-xmark-svgrepo-com.png")
        self.muteButton.move(self.muteButton.height() // 3, self.muteButton.height() // 3 + (self.muteButton.height() + self.muteButton.height() // 3)*2)

        # Buttons Rechts
        self.endCallButton = RoundButton(self, hover_callback=lambda:print("End Call"), icon_path="../GUI/images/call-cancel-svgrepo-com.png")
        self.endCallButton.move(width - self.endCallButton.height() - (self.endCallButton.height() // 3), self.endCallButton.height() // 3)

        self.blurButton = RoundButton(self, hover_callback=lambda: self.toggle_blur(), icon_path="../GUI/images/blur-svgrepo-com.png")
        self.blurButton.move(width - self.blurButton.height() - (self.blurButton.height() // 3), self.blurButton.height() // 3+ self.muteButton.height() + self.muteButton.height() // 3)

        self.gameButton = RoundButton(self, hover_callback=lambda: print("Gamingtime"), icon_path="../GUI/images/controller-svgrepo-com.png")
        self.gameButton.move(width - self.gameButton.height() - (self.gameButton.height() // 3), self.gameButton.height() // 3 + (self.muteButton.height() + self.muteButton.height() // 3)*2)



    def start(self):
        self.timer.start(30)

    def toggle_blur(self):
        # Umschalten des Blur-Status
        self.is_blurred = not self.is_blurred

    def update_image(self):
        ret, frame = self.cap.read()
        if ret:
            # Spiegle das Bild, um eine natürlichere Interaktion zu ermöglichen
            frame = cv2.flip(frame, 1)

            # Verarbeite das Frame für die Handerkennung
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            # Initialisiere Hover-Status für jeden Button
            vol_up_button_hovered = False
            vol_down_button_hovered = False
            mute_button_hovered = False
            end_call_button_hovered = False
            blur_button_hovered = False
            game_button_hovered = False

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
                                if self.volUpButton.contains_point(x, y):
                                    vol_up_button_hovered = True
                                if self.volDownButton.contains_point(x, y):
                                    vol_down_button_hovered = True
                                if self.muteButton.contains_point(x, y):
                                    mute_button_hovered = True
                                if self.endCallButton.contains_point(x, y):
                                    end_call_button_hovered = True
                                if self.blurButton.contains_point(x, y):
                                    blur_button_hovered = True
                                if self.gameButton.contains_point(x, y):
                                    game_button_hovered = True

            # Aktualisiere den Hover-Status der Buttons basierend auf der Fingerposition
            self.volUpButton.update_hover_status(vol_up_button_hovered)
            self.volDownButton.update_hover_status(vol_down_button_hovered)
            self.muteButton.update_hover_status(mute_button_hovered)
            self.endCallButton.update_hover_status(end_call_button_hovered)
            self.blurButton.update_hover_status(blur_button_hovered)
            self.gameButton.update_hover_status(game_button_hovered)

            # Erstelle eine Kopie des Frames für die Anzeige
            display_frame = frame.copy()

            # Wende den Blur-Effekt auf die Kopie an, falls aktiviert
            if self.is_blurred:
                display_frame = cv2.GaussianBlur(display_frame, (81, 81), 0)

            # Konvertiere das Display-Frame in ein QImage und setze es in das QLabel
            display_frame = cv2.resize(display_frame, (width, height))
            image = QImage(display_frame.data, display_frame.shape[1], display_frame.shape[0], QImage.Format_BGR888)
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
