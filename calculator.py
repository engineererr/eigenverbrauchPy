import csv

# das Elektroauto wird vollgeladen, sobald am aktuellen Tag keine überschüssige Energie mehr vorhanden ist. Die Ladeleistung wird nicht berücksichtigt.

class Simulator:
    # gibt aufsummierte Werte zurück
    def calculateYear(self, modulgrosse, batterieKapazitat=0, wirkungsgrad=0.14, verluste=0.75, elektroAuto=None, kmProTag=None):
        autoAnkunftszeit = 18
        autoAbfahrtszeit = 6

        batterieVorher = 0
        produktionTotal = 0
        verbrauchTotal = 0
        einspeisungTotal = 0

        netznutzungTotal = 0
        eigenverbrauchTotal = 0

        if(elektroAuto is not None):
            autoLadestandHeutigerTag = elektroAuto[0]

        autoNutzbarAlsBatterie = False
        with open('daten.csv', newline='') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=';')
            # für jede Zeile im CSV
            for row in datareader:
                einspeisung = 0
                netznutzung = 0

                if(elektroAuto is not None):
                    tagesStunde = int(row['Stunde']) % 24
                    # Auto parkiert um 18 Uhr
                    if(tagesStunde == autoAnkunftszeit):
                        autoLadestandHeutigerTag -= elektroAuto[1] / \
                            100 * kmProTag
                        autoNutzbarAlsBatterie = True
                    # Auto fährt weg um 6 Uhr
                    elif(tagesStunde == autoAbfahrtszeit):
                        netznutzung += elektroAuto[0] - \
                            autoLadestandHeutigerTag
                        autoLadestandHeutigerTag = elektroAuto[0]
                        autoNutzbarAlsBatterie = False

                produktion = float(row['Einstrahlung in Modulebene m2']
                                   ) * modulgrosse * wirkungsgrad * verluste

                verbrauch = float(row['Verbrauch 4 Pers'])
                remainingEnergy = produktion - verbrauch
                ubrigeEnergieMitBatterie = remainingEnergy + batterieVorher

                # Battery ist voll, Energie wird eingespiesen
                if(ubrigeEnergieMitBatterie >= batterieKapazitat):
                    remainingEnergyAfterFillingBattery = abs(
                        ubrigeEnergieMitBatterie - batterieKapazitat)
                    batterieJetzt = batterieKapazitat
                    if(autoNutzbarAlsBatterie and elektroAuto[0] > autoLadestandHeutigerTag + remainingEnergyAfterFillingBattery):
                        # Auto wird als Batterie genutzt
                        autoLadestandHeutigerTag += remainingEnergyAfterFillingBattery
                    else:
                        einspeisung += remainingEnergyAfterFillingBattery
                # zu wenige Energie vorhanden,  Netz wird genutzt
                elif(ubrigeEnergieMitBatterie < 0):
                    batterieJetzt = 0.0
                    netznutzung += abs(ubrigeEnergieMitBatterie)
                    # wenn Auto am System angeschlossen und nicht vollgeladen, dann bezieht das Auto Strom vom Netz
                    if(autoNutzbarAlsBatterie):
                        netznutzung += abs(elektroAuto[0] -
                                           autoLadestandHeutigerTag)
                        autoLadestandHeutigerTag = elektroAuto[0]
                else:
                    batterieJetzt = ubrigeEnergieMitBatterie

                # Eigenverbrauch
                eigenverbrauch = produktion - einspeisung

                # Totale
                produktionTotal += produktion
                einspeisungTotal += einspeisung
                netznutzungTotal += netznutzung
                eigenverbrauchTotal += eigenverbrauch
                verbrauchTotal += verbrauch

                # Variable, um den vorherigen Batteriestand zu merken, wird auf den aktuellen Wert gesetzt
                batterieVorher = batterieJetzt
        return {'produktionTotal': produktionTotal, 'verbrauchTotal': verbrauchTotal, 'einspeisungTotal': einspeisungTotal, 'netznutzungTotal': netznutzungTotal, 'eigenverbrauchTotal': eigenverbrauchTotal}

    # gibt eine Datenreihe für jeden Stunde zurück
    def calculateDays(self, modulgrosse, batterieKapazitat=0, wirkungsgrad=0.14, verluste=0.75, elektroAuto=None, kmProTag=None):
        batterieVorher = 0
        autoAnkunftszeit = 18
        autoAbfahrtszeit = 6
        resultat = []

        if(elektroAuto is not None):
            autoLadestandHeutigerTag = elektroAuto[0]

        autoNutzbarAlsBatterie = False
        with open('daten.csv', newline='') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=';')
            # für jede Zeile im CSV
            for row in datareader:

                einspeisung = 0
                netznutzung = 0

                if(elektroAuto is not None):
                    tagesStunde = int(row['Stunde']) % 24
                    # Auto parkiert um 18 Uhr
                    if(tagesStunde == autoAnkunftszeit):
                        autoLadestandHeutigerTag -= elektroAuto[1] / \
                            100 * kmProTag
                        autoNutzbarAlsBatterie = True
                    # Auto fährt weg um 18 Uhr
                    elif(tagesStunde == autoAbfahrtszeit):
                        netznutzung += elektroAuto[0] - \
                            autoLadestandHeutigerTag
                        autoLadestandHeutigerTag = elektroAuto[0]
                        autoNutzbarAlsBatterie = False

                produktion = float(row['Einstrahlung in Modulebene m2']
                                   ) * modulgrosse * wirkungsgrad * verluste

                verbrauch = float(row['Verbrauch 4 Pers'])
                remainingEnergy = produktion - verbrauch
                ubrigeEnergieMitBatterie = remainingEnergy + batterieVorher

                # Battery ist voll, Energie wird eingespiesen
                if(ubrigeEnergieMitBatterie >= batterieKapazitat):
                    remainingEnergyAfterFillingBattery = abs(
                        ubrigeEnergieMitBatterie - batterieKapazitat)
                    batterieJetzt = batterieKapazitat
                    if(autoNutzbarAlsBatterie and elektroAuto[0] > autoLadestandHeutigerTag + remainingEnergyAfterFillingBattery):
                        # Auto wird als Batterie genutzt
                        autoLadestandHeutigerTag += remainingEnergyAfterFillingBattery
                    else:
                        einspeisung += remainingEnergyAfterFillingBattery
                # zu wenige Energie vorhanden,  Netz wird genutzt
                elif(ubrigeEnergieMitBatterie < 0):
                    batterieJetzt = 0.0
                    netznutzung += abs(ubrigeEnergieMitBatterie)
                    # wenn Auto am System angeschlossen und nicht vollgeladen, dann bezieht das Auto Strom vom Netz
                    if(autoNutzbarAlsBatterie):
                        netznutzung += abs(elektroAuto[0] -
                                           autoLadestandHeutigerTag)
                        autoLadestandHeutigerTag = elektroAuto[0]
                else:
                    batterieJetzt = ubrigeEnergieMitBatterie

                # Eigenverbrauch
                eigenverbrauch = produktion - einspeisung

                # Variable, um den vorherigen Batteriestand zu merken, wird auf den aktuellen Wert gesetzt
                batterieVorher = batterieJetzt

                # Totale
                resultat.append({'stunde': row['Stunde'], 'produktion': produktion, 'verbrauch': verbrauch, 'einspeisung': einspeisung,
                                 'netznutzung': netznutzung, 'eigenverbrauch': eigenverbrauch})

        return resultat
