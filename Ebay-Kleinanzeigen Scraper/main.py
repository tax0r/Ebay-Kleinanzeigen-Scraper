# Imports die Niemand wirklich verstehen muss...
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Nimmt sich das momentane Datum & formatiert es zu '[Stunde:Minute:Sekunde] - '.
now = datetime.now()
prefix = "[" + now.strftime("%H:%M:%S") + "] - "

# Eine Funktion um eine Text-Datei zu beschreiben.
def writeFile(response, name ,fileType):
    with open(name + fileType, "a", encoding="utf8") as f:
        f.write(response)

# Eine Funktion um den Durschnitt zu berechnen.
def calculateAverage(Sum, count):
    return Sum / count

# Eine Funktion um die Summe eines Arrays zu berechnen.
def calculateSum(arr):
    result = sum(arr)
    return result

# Fragt die Query ab die Später in den URL gegeben werden soll (der Suchbegriff)
query = input(prefix + "Bitte gebe deine Query an << ")

# Fügt die Query in den Ebay-Kleinanzeigen URL ein.
URL = "https://www.ebay-kleinanzeigen.de/s-" + query + "/k0"

# Gibt aus welche Query gewählt wurde.
print(prefix + "Es wird nach gesucht nach >> " + query)

# Setzt die Headers der Anfrage (Den User-Agent), damit Ebay-Kleinanzeigen die Anfrage nicht blockt.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59',
}

# Gibt den HTML text der Website in eine Variable wieder.
response = requests.get(url=URL, headers=headers)

# Setzt den Content der Website in eine Variable.
page = response.content

# Erstellt eine BeautifulSoup-Instanz mit dem Website-Content und einem passendem Parser.
soup = BeautifulSoup(page, "html.parser")

# Setzt die Search-Results-Content in eine Variable.
srchRsltsContent = soup.find("ul", id="srchrslt-adtable")

# Setzt die Einträge inheralb der Seach-Results und dem Table dortdrinn in eine Variable / Array.
srchRslts = srchRsltsContent.find_all("li")

# Setzt einen Counter.
counter = 0

# Setzt einen zweiten Counter.
vbCounter =  0

ePreise = []

# Looped durch alle Search-Results durch.
for srchRslt in srchRslts:
    #print(srchRslt.get_text())

    # Nimmt sich alles mit dem <strong> tag.
    preise = srchRslt.find_all("strong")

    # Geht durch jedes Element mit dem <strong> tag durch.
    for preis in preise:

        # Incrementiert einen Counter.
        counter = counter + 1

        # Gibt den Preis des Listings aus & fügt den Incrementierten Counter hinzu (+ formatierung).
        print("#" + str(counter) + " | " +  preis.text)

        # Zählt wieviele Listings mit 'VB' gekennzeichnet sind.
        if("VB" in preis.text):
            vbCounter = vbCounter + 1
            
            # Entfernt Chars, wenn das Euro-Zeichen vorhande ist.
            # Konvertiert außerdem den Preis in eine Int und speichert ihn in den Array 'ePreise'.
            if("€" in preis.text):
                if("." in preis.text):
                    if("VB" in preis.text):
                        ePreise.append(int(preis.text.replace(" ", "").replace("VB", "").replace("€", "").replace(".", "")))
                    else:
                        ePreise.append(int(preis.text.replace(" ", "").replace("€", "").replace(".", "")))
                    ePreise.append(int(preis.text.replace(" ", "").replace("VB", "").replace("€", "").replace(".", "")))
                else:
                    ePreise.append(int(preis.text.replace(" ", "").replace("VB", "").replace("€", "")))
        else:
            if("€" in preis.text):
                if("." in preis.text):
                    ePreise.append(int(preis.text.replace(" ", "").replace("€", "").replace(".", "")))
                else:
                    ePreise.append(int(preis.text.replace(" ", "").replace("€", "")))        

# Gibt verhandelbare Listings aus.
print(prefix + "Verhandelbare Listings >> " + str(vbCounter))

# Gibt die Anzahl aller Listings aus.
print(prefix + "Anzahl der Listings >> " + str(counter))

# Gibt den Durschnitspreis der Listings aus.
print(prefix + "Durschnitts-Preis der Listings >> " + str(calculateAverage(calculateSum(ePreise), counter)))
