# fix_signal_photos_metadata

## Fotos aus Signal exportieren
- jedes Foto muss einzeln heruntergeladen werden, weil sonst teilweise der Dateiname nicht das gewünschte Empfangsdatum, sondern nur einen generischen Wert enthält
- scrcpy ausführen und als Fenster maximieren (ggf. müssen Koordinaten der Klicks angepasst werden)
- erstes Foto öffnen und Skript `download_photos.py` ausführen (Anzahl bei `repeats` festlegen → mit "select all" lässt sich Gesamtanzahl der Fotos im Chat herausfinden), innerhalb von 5 Sekunden ins scrcpy-Fenster klicken

## Metadaten aus Dateiname extrahieren
- Fotos in Ordner `input` speichern
- `extract_metadata.py`ausführen
- Fotos mit aktualisiertem Erstelldatum werden im Ordner `output` gespeichert