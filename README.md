# pdf2ics
Wandelt Dienstpläne des LTH NÖ in ICS Kalender-Events um.

### Funktionsweise

**ICS-Dateien** sind Textdateien, die Kalender-Events mit Beginn, Ende, Datum, Beschreibung, etc darstellen. Sie können von allen gängigen Kalender-Apps und Services importiert und gelesen werden.
Das Python-Skript extrahiert Daten (zB Montag, 17.02.25) aus einem PDF, basierend auf der Formatvorlage, die im Landestheater NÖ verwendet wird.
Durch Texteingabe des gesuchten Namens ("Mustermann, Max") werden die Dienstzeiten der jeweiligen Woche aus der entsprechenden Zeile gelesen und in eine ICS-Datei geschrieben.

#### v1.0a
Erstellt ein ICS-File pro Kalenderwoche. Sinnvoll für manuelles Importieren, um doppelte Kalendereinträge zu vermeiden.

#### v1.0b
Erstellt ein ICS-File, zu dem neue Events stets angefügt werden. Sinnvoll für ICS-Kalender-Feeds, die über URLs eingebunden werden (zB über Google Drive + Google Calendar) und stetig synchronisiert werden.
