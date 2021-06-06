import socket
import numpy as np


# Anzahl der Spieler
anzahl_spieler = 2

# Einrichten der Verbindung
host="25.71.80.22"
port = 443
print(host, ":", port)

# Blatt definieren
Zahlen = ["2","3", "4", "5", "6","7","8","9","10", "B", "D", "K", "A"]
Farben = ["\u2666", "\u2665", "\u2660", "\u2663"]


def print_cards(cards):
    for index, karte in enumerate(cards):
        zahl, farbe = convert_to_card(karte)
        print(index, ": ", zahl, farbe)

def convert_to_card(n):
    zahl = Zahlen[int((n - n % 4) / 4)]
    farbe = Farben[n % 4]
    return zahl, farbe

def Zahlprufen(input):
    try:
        int(input)
        return True
    except ValueError:
        return False
    
def check_for_four(my_cards):
    Handkarten = [[] for i in range(len(Zahlen))]
    for i in range(len(my_cards)):
        Zahl = int(my_cards[i]/4)
        Handkarten[Zahl].append(i)
    Handkarten = Handkarten[::-1]
    for irgendwas in Handkarten:
        if len(irgendwas) == 4:
            for i in irgendwas:
                my_cards.pop(irgendwas[0])
    return my_cards

if __name__ == '__main__':
    try:
        # Verbinden
        client_socket = socket.socket()
        client_socket.connect((host, port))

        my_cards = []

        while (True):
            data = client_socket.recv(1024).decode()
            if str(data) == "Du bist dran. Leg eine Karte:":
                print(str(data))
                my_cards = check_for_four(my_cards)
                print_cards(my_cards)
                
               
                while True:
                    message = input(" -> ")
                    if Zahlprufen(message) == True:
                        karte = str(my_cards[int(message)])
                        print(karte)
                        client_socket.send(karte.encode())
                        my_cards.pop(int(message))
                        print_cards(my_cards)
                        
                    elif (message == "a"):  
                        client_socket.send(message.encode())
                        break
                   
                    elif (message == "l"):
                        client_socket.send(message.encode())
                        break

                    else:
                        print("Auswahl geht nicht!!!")

            elif "Karten-start:" in str(data):
                data = str(data)
                data = data.split("\t")
                if len(data) >= 2:
                    my_cards.append(int(data[1]))

           
            elif "Um welche Zahl wird gespielt?" in str(data):
                print_cards(my_cards)
                while True:
                    Zahl = input(data + "\n")
                    if Zahl in Zahlen:
                        message = "s" + Zahl
                        client_socket.send(message.encode())
                        break
                    else:
                        print("Das hat nicht geklappt, bitte versuche es nochmal...")
            
            elif data.endswith(" Karten erhalten."):
                my_cards = np.sort(my_cards).tolist()
                print (data)
            
            elif data != "":
                print('Server: ' + data)  # show in terminal
   
    except KeyboardInterrupt:
        print("Bis bald!\n")
        client_socket.close()
