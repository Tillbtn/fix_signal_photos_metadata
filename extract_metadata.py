from PIL import Image
import piexif
from datetime import datetime
import os
import shutil
import re


def show_exif_dates(image_path):
    """
    Zeigt alle Datums-relevanten EXIF-Daten eines Fotos an.
    """
    exif_dict = piexif.load(image_path)

    if "Exif" in exif_dict:
        exif = exif_dict["Exif"]
        if piexif.ExifIFD.DateTimeOriginal in exif:
            print(f"Original Date: {exif[piexif.ExifIFD.DateTimeOriginal].decode()}")
        if piexif.ExifIFD.DateTimeDigitized in exif:
            print(f"Digitized Date: {exif[piexif.ExifIFD.DateTimeDigitized].decode()}")

    if "0th" in exif_dict:
        zeroth = exif_dict["0th"]
        if piexif.ImageIFD.DateTime in zeroth:
            print(f"Modify Date: {zeroth[piexif.ImageIFD.DateTime].decode()}")


def modify_create_date(image_path, new_date):
    """
    Ändert die Datums-Metadaten eines Fotos.

    Args:
        image_path (str): Pfad zum Foto
        new_date (datetime): Neues Datum für das Foto
    Returns:
        bool: True wenn erfolgreich, False wenn ein Fehler auftrat
    """
    try:
        # Datum im EXIF-Format formatieren (YYYY:MM:DD HH:MM:SS)
        date_str = new_date.strftime("%Y:%m:%d %H:%M:%S")

        # EXIF-Daten auslesen
        exif_dict = piexif.load(image_path)

        # Stelle sicher, dass die EXIF-Bereiche existieren
        if "Exif" not in exif_dict:
            exif_dict["Exif"] = {}
        if "0th" not in exif_dict:
            exif_dict["0th"] = {}

        # Setze die Datums-Tags
        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = date_str.encode('ascii')
        exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = date_str.encode('ascii')
        exif_dict["0th"][piexif.ImageIFD.DateTime] = date_str.encode('ascii')

        # Wenn SubSecTime-Tags existieren, diese auch aktualisieren
        subsec_time = "00"
        if piexif.ExifIFD.SubSecTimeOriginal in exif_dict["Exif"]:
            exif_dict["Exif"][piexif.ExifIFD.SubSecTimeOriginal] = subsec_time.encode('ascii')
        if piexif.ExifIFD.SubSecTimeDigitized in exif_dict["Exif"]:
            exif_dict["Exif"][piexif.ExifIFD.SubSecTimeDigitized] = subsec_time.encode('ascii')

        # Neue EXIF-Daten speichern
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, image_path)

        return True

    except Exception as e:
        print(f"Fehler beim Ändern der Metadaten von {image_path}: {str(e)}")
        return False


def extract_datetime_from_filename(filename):
    """
    Extrahiert Datum und Zeit aus einem Dateinamen im Format 'signal-YYYY-MM-DD-HH-MM-SS-xxx(-n).jpg'

    :param filename: Der Dateiname (ohne Pfad)
    :return: Ein datetime-Objekt oder None, falls das Format nicht stimmt
    """
    # Extrahiere nur den Dateinamen ohne Pfad
    base_filename = os.path.basename(filename)

    # Angepasstes Pattern für beide Formatvarianten
    pattern = r"signal-(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-\d{3}(?:-\d+)?\.jpg"

    match = re.match(pattern, base_filename)
    if match:
        try:
            # Extrahiere die Gruppen (Jahr, Monat, Tag, Stunde, Minute, Sekunde)
            year, month, day, hour, minute, second = map(int, match.groups())

            # Erstelle ein datetime-Objekt
            return datetime(year, month, day, hour, minute, second)
        except ValueError as e:
            print(f"Fehler beim Parsen des Datums aus {base_filename}: {e}")
            return None
    else:
        print(f"Fehler: Dateiname '{base_filename}' passt nicht zum erwarteten Format.")
        return None


def process_directory(input_dir, output_dir):
    """
    Verarbeitet alle JPG-Dateien in einem Ordner und verschiebt sie nach der Bearbeitung.

    Args:
        input_dir (str): Quellordner mit den zu bearbeitenden Fotos
        output_dir (str): Zielordner für bearbeitete Fotos
    """
    # Stelle sicher, dass der Zielordner existiert
    os.makedirs(output_dir, exist_ok=True)

    # Zähler für die Statistik
    erfolgreiche = 0
    fehlgeschlagene = 0

    # Alle JPG-Dateien im Quellordner verarbeiten
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.jpg'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            print(f"\nVerarbeite: {filename}")

            # Extrahiere das Datum aus dem Dateinamen
            new_date = extract_datetime_from_filename(filename)

            if new_date is None:
                print(f"Überspringe {filename} - Konnte kein Datum aus dem Namen extrahieren")
                fehlgeschlagene += 1
                continue

            # print(f"Extrahiertes Datum: {new_date}")
            # print("Ursprüngliche Metadaten:")
            # show_exif_dates(input_path)

            if modify_create_date(input_path, new_date):
                # Verschiebe die Datei in den Zielordner
                shutil.move(input_path, output_path)
                # print(f"Erfolgreich bearbeitet und verschoben nach: {output_path}")
                # print("Neue Metadaten:")
                # show_exif_dates(output_path)
                erfolgreiche += 1
            else:
                print(f"Fehler bei der Bearbeitung von: {filename}")
                fehlgeschlagene += 1

    # Abschlussbericht
    print(f"\nVerarbeitung abgeschlossen:")
    print(f"Erfolgreich bearbeitet: {erfolgreiche}")
    print(f"Fehlgeschlagen: {fehlgeschlagene}")


# Beispiel für die Verwendung
if __name__ == "__main__":

    process_directory("input", "output")