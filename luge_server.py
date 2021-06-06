import numpy as np
import socket
import time as t

# Anzahl der Spieler
anzahl_spieler = 5

# Einrichten der Verbindung
host="25.73.125.219"
port = 443
print(host, ":", port)

# Blatt definieren
kleinste_Zahl = 1
Zahlen = ["2","3", "4", "5", "6","7","8","9","10", "B", "D", "K", "A"]
Farben = ["\u2666", "\u2665", "\u2660", "\u2663"]

# Globale Variablen
i = 0
stack = []
stack2 = [] 
stack3 = []

# Funktion zum Erzeugen der Karten
def Karten_erzeugen(low_limit, player):
    # Karten erzeugen und mischen
    karten = np.arange((low_limit-1)*4 , 52)
    np.random.shuffle(karten)

    # Karten verteilen
    player_karten = []
    i = 0
    j = 0
    for p in range(player):
        i = p * int(len(karten)/player)
        j = (p+1) * int(len(karten)/player)
        player_karten.append([karten[i:j]])

    player_karten.append([karten[j:]])
    return player_karten

# Nachricht an alle schicken
def message_to_all(message):
    global player
    for conn in player:
        conn.send(message.encode())
    t.sleep(0.3)


# Karten an eine Person verschicken
def Karten_senden(karten, spieler, wait=0.3, numpy_arr=False):
    print("Karten werden versendet.")
    if numpy_arr:
        karten=karten[0]
    for karte in karten:
        message = "Karten-start:\t" + str(karte)
        spieler.send(message.encode())
        t.sleep(wait)
    message = "Du hast " + str(len(karten))+ " Karten erhalten."
    spieler.send(message.encode())
   
# Auswählen, was gespielt wird
def Wahl_des_Spiels(spieler):
    global i
    message = "Spieler "+str(i%anzahl_spieler)+" wählt Zahl. Bitte warten."
    message_to_all(message)
    message = "Um welche Zahl wird gespielt?"
    spieler.send(message.encode())
    while True:
        answer = spieler.recv(1024).decode()
        if(answer.startswith("s")):
            answer = answer.strip("s")
            message = "Gespielt wird: " + answer
            message_to_all(message)
            return answer
        t.sleep(0.1)
        i -= 1

def close_connections(player):
    for conn in player:
         conn.close()

def Zahlprufen(input):
    try:
        int(input)
        return True
    except ValueError:
        return False

def reih_um(player):
    global i
    global gespielt_wird
    global stack
    global stack2
    global stack3
    conn = player[i%anzahl_spieler]
    message = "Du bist dran. Leg eine Karte:"
    conn.send(message.encode())
    
    stack3=stack2
    stack2 = []
    while True:
        data = conn.recv(1024).decode()
        if data == "l":
            luge = luge_prufen(stack3, gespielt_wird)
            if luge:
                Karten_senden(stack, player[(i-1)%anzahl_spieler])
                gespielt_wird = Wahl_des_Spiels(player[(i)%anzahl_spieler])
                i -= 1
                print("Lüge!")
            else:
                Karten_senden(stack, player[i%anzahl_spieler])
                gespielt_wird = Wahl_des_Spiels(player[(i+1)%anzahl_spieler])
                print("Keine Lüge!")
    
            stack = []
            break
       
        elif (data=="a"):
            break
        
        elif Zahlprufen(data):
            stack.append(int(data))
            stack2.append(int(data))
    
        elif not data:
            close_connections(player)
    
        else:
            message = "Das hat nicht funktioniert, versuche es nochmal"
            conn.send(message.encode())
            reih_um(player, i, stack)
    
    message = "Es wurden "+str(len(stack2))+" Karten gelegt"
    message_to_all (message)

def luge_prufen(stack, gespielt_wird):
    
    luge=False
    for Karte in stack:
        num = int(Karte/4)
        if(Zahlen[num] != gespielt_wird):
            luge = True
        print("gelegt: ", Zahlen [num],"gespielt:", gespielt_wird)
        message = "gelegt: "+ Zahlen [num]+"gespielt:"+ gespielt_wird
        message_to_all (message)
    return luge
    




############### Vorbereitung #################

# Aufsetzen des Server mit angegebenen Daten
server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(anzahl_spieler)

# Auf Spieler warten
player = []
spieler = 0
while (len(player) < anzahl_spieler):
    try:
        conn, address = server_socket.accept()
        player.append(conn)
        print("Connection from: " + " at " + str(address))
        welcome = "Hi, schön dass du da bist! Du bist Spieler " + str(spieler)
        conn.send(welcome.encode())
        spieler += 1
        
    except KeyboardInterrupt:
        close_connections(player)
        quit()


######### Spielbeginn ##################

message_to_all("Los geht's ... ")

# Karten erzeugen und verteilen
Spieler_Karten = Karten_erzeugen(kleinste_Zahl, spieler)
len_Karten = len(Spieler_Karten)
for j, spieler in enumerate(player):
    Karten_senden(Spieler_Karten[j], spieler, numpy_arr=True)
    Spieler_Karten[j].pop()

# Rest der Karten kommen in die Mitte
#if len_Karten%anzahl_spieler > 0:
#    for karte in Spieler_Karten[anzahl_spieler]:
#        stack.append(karte)

# Der erste Spieler wählt worum gespielt wird

gespielt_wird = Wahl_des_Spiels(player[0])


while True:
    try:
        # Reih um Aktion abfragen
        data = reih_um(player)
        i += 1
        message = "Spieler " + str(i%anzahl_spieler) + " hat gespielt!"
        message_to_all(message)

    except ConnectionResetError:
        break
    except KeyboardInterrupt:
        print("Bis bald\n")
        message_to_all("Bis zum nächsten Mal!")
        break
close_connections(player)
