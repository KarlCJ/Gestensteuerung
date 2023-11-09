import org.bytedeco.opencv.global.opencv_highgui.*
import org.bytedeco.opencv.opencv_core.*
import org.bytedeco.opencv.opencv_videoio.VideoCapture

fun main() {
    // Kamera initialisieren
    val capture = VideoCapture(0)
    if (!capture.isOpened) {
        println("Kamera konnte nicht geöffnet werden.")
        return
    }

    // Fenster für die Anzeige erstellen
    namedWindow("Webcam")

    // Frame-Objekt für das Einlesen der Bilder
    val frame = Mat()

    while (true) {
        // Bild von der Kamera einlesen
        capture.read(frame)
        if (!frame.empty()) {
            // Bild anzeigen
            imshow("Webcam", frame)
        } else {
            println("Kein Frame erfasst.")
            break
        }

        // Schleife beenden, wenn 'q' gedrückt wird
        if (waitKey(30) == 'q'.toInt()) {
            break
        }
    }

    // Ressourcen freigeben
    capture.release()
    destroyAllWindows()
}
