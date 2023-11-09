import org.bytedeco.opencv.global.opencv_imgproc.*
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
    val zoomedFrame = Mat()

    while (true) {
        // Bild von der Kamera einlesen
        capture.read(frame)
        if (!frame.empty()) {
            // Zoom anwenden
            val center = Point(frame.cols() / 2, frame.rows() / 2)
            val newSize = Size(frame.cols() / 2, frame.rows() / 2)
            val roi = Rect(center.x() - newSize.width() / 2, center.y() - newSize.height() / 2, newSize.width(), newSize.height())

            // Bild beschneiden und skalieren
            resize(frame.apply(roi), zoomedFrame, frame.size())

            // Bild anzeigen
            imshow("Webcam", zoomedFrame)
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
