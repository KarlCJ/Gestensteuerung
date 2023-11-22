# Notwendige Bibliotheken importieren: sys für Systemfunktionen, mediapipe für Handgestenerkennung und cv2 für Bildverarbeitung
import sys
import mediapipe
import cv2

# Mediapipe wird genutzt, um ein visuelles Modell der Hand zu erstellen
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

# Initialisierung der Kamera für Videoaufnahmen
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

# Einstellungen für die Handgestenerkennung: Modi, Vertrauenswerte und maximale Handanzahl
with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:

    # Endlosschleife für kontinuierliche Bildaufnahme und -verarbeitung
    while True:
        ret, frame = cap.read()

        # Anpassung der Bildgröße für optimale Verarbeitung
        frame1 = cv2.resize(frame, (640, 480))

        # Verarbeitung der Bildaufnahmen, um Handgesten zu erkennen
        results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))

        # Verarbeitung jeder erkannten Hand
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(frame1, handLandmarks, handsModule.HAND_CONNECTIONS)

                # Ausgabe der Koordinaten des Zeigefingers
                for point in handsModule.HandLandmark:

                    normalizedLandmark = handLandmarks.landmark[point]
                    pixelCoordinatesLandmark = drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, 640, 480)

                    if point == 8:  # Punkt 8 entspricht der Spitze des Zeigefingers
                        print(point)
                        print(pixelCoordinatesLandmark)
                        print(normalizedLandmark)
                        sys.stdout.flush()

        # Anzeigen des verarbeiteten Bildes
        cv2.imshow("Frame", frame1)
        key = cv2.waitKey(1) & 0xFF

        # Beenden des Programms bei Drücken der Taste 'q'
        if key == ord("q"):
            break
