from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QPainter, QColor, QBrush, QPainterPath
from PyQt5.QtCore import Qt, QTimer, QSize

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
