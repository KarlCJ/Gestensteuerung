plugins {
    kotlin("jvm") version "1.7.10" // Verwenden Sie die aktuellste stabile Kotlin-Version
}

group = "com.yourproject"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    implementation(kotlin("stdlib"))

    // JavaCV (OpenCV für Java/Kotlin)
    implementation("org.bytedeco:javacv:1.5.7") // Ersetzen Sie dies durch die neueste Version
    implementation("org.bytedeco:javacv-platform:1.5.7") // Plattformübergreifende Unterstützung

    // WebRTC-Abhängigkeit (abhängig von Ihrer spezifischen Implementierung oder Bibliothek)
    // Beachten Sie, dass Sie die richtige Abhängigkeit für Ihre WebRTC-Implementierung finden müssen.
}

tasks.compileKotlin {
    kotlinOptions {
        jvmTarget = "1.8" // oder '11' oder höher, je nach Ihrer JDK-Version
    }
}

tasks.compileTestKotlin {
    kotlinOptions {
        jvmTarget = "1.8"
    }
}
