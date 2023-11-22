import java.io.BufferedReader
import java.io.InputStreamReader

fun main() {
    try {
        // Pfad zum Python-Skript
        val pythonScriptPath = "src/main/python/gestureRecongnition.py"

        // Starten des Python-Skripts als externen Prozess
        val process = Runtime.getRuntime().exec("python $pythonScriptPath")

        // Lesen der Standard- und Fehlerausgabe des Python-Skripts
        val stdInput = BufferedReader(InputStreamReader(process.inputStream))
        val stdError = BufferedReader(InputStreamReader(process.errorStream))

        // Ausgabe der Standardausgabe
        println("Standardausgabe:")
        stdInput.forEachLine { println(it) }

        // Ausgabe der Fehlerausgabe
        println("Fehlerausgabe:")
        stdError.forEachLine { println(it) }

        // Warten, bis der Prozess beendet ist
        process.waitFor()
    } catch (e: Exception) {
        e.printStackTrace()
    }
}

