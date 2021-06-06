# luge_Kartenspiel

Remote Lügespiel von Niklas und Tobi

Installation:

Es wird ein laufendes Python benötigt. Eine Möglichkeit ist Miniconda zu
installieren:
- Miniconda:
  https://docs.conda.io/en/latest/miniconda.html

Außerdem wird numpy benötigt. Wenn miniconda installiert ist, kann das
installiert werden indem man in der Miniconda Konsole den Befehl

            pip install numpy --user

eingibt.

- Programmdatei heruntergeladen (Dateipfad merken)

- LogMeIn Hamachi:
  installieren zum Beispiel von hier

  https://www.computerbild.de/download/LogMeIn-Hamachi-2017878.html

  Da muss man einen Account machen und dem Netzwerk ..... beitreten.
  Passwort weiß der Niklas

Spielen:

Spieler:

- In der Miniconda Konsole zum Spiel navigieren. Dazu können Befehle wie
  dir (Windows) / ls (Linux/Mac) # Anzeigen dder Inhalte eines Ordner
  cd Name-des-Ordners # Wechseln in einen Unterordner

- IP adresse abgleichen:
  Es muss am Anfang des Programms die IP adresse der Person, die den
  Server laufen lässt eingetragen werden.
  Beispiel:
  host="25.47.246.219"
  (Nur das in "" muss geändert werden)

- Programm starten:
  In Miniconda den Befehl:
  python luge_client.py
  eingeben.

Tasten:
- a -> Abschließen des Kartenlegen
- Karten legen -> Zahl vor der angezeigten Karte eingeben
                  (Vorsicht bei mehreren Eingaben nacheinander)
- l -> Aufdecken
- Strg-c -> Beenden


Server: (nicht vollständig ausgetestet)

- Verbindung freigeben:
  In der Firewall der Port 443 freigeben (eingehende Verbindungen erlauben)

- Eigene IP in Server Programm einfügen und an Mitspieler weitergeben
  1. in Hamachi nach der IPv4 Addresse suchen
  2. per Konsole mit Befehlen, wie
  ip config (Windows) / ip a (Linux, Mac?)

- Anzahl der Spieler im Programm anpassen

- Als Admin Ausführen
  In Linux:
  sudo luge_sever.py
  In Windows:
  keine Ahnung
