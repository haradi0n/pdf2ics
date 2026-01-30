# pdf2ics
Wandelt Dienstpläne des LTH NÖ in ICS Kalender-Events um.

### Funktionsweise

**ICS-Dateien** sind Textdateien, die Kalender-Events mit Beginn, Ende, Datum, Beschreibung, etc darstellen. Sie können von allen gängigen Kalender-Apps und Services importiert und gelesen werden.
Das Python-Skript extrahiert Daten (zB Montag, 17.02.25) aus einem PDF, basierend auf der Formatvorlage, die im Landestheater NÖ verwendet wird.
Durch Texteingabe des gesuchten Namens ("Mustermann, Max") werden die Dienstzeiten der jeweiligen Woche aus der entsprechenden Zeile gelesen und in eine ICS-Datei geschrieben.

#### v1.1
Einfaches GUI für Quelldatei, Textsuche und Speicherort. Option zum Überschreiben von ICS-Daten in bereits bestehenden Dateien.

#### v1.2
Package Import Optimierung für bessere Performance. MacOS .App File zum Release hinzugefügt.
