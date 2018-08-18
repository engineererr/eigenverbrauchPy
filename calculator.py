import csv

# vars


class Simulator:
    def calculateYear(self, modulgrosse, batteryCapacity=0, wirkungsgrad=0.14, verluste=0.75, car=None, kmProTag=None):
        batteryBefore = 0
        produktionTotal = 0
        verbrauchTotal = 0
        einspeisungTotal = 0

        netznutzungTotal = 0
        eigenverbrauchTotal = 0

        if(car is not None):
            carBatteryLevelCurrentDay = car[0]

        carUsableAsBattery = False
        with open('daten.csv', newline='') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=';')
            for row in datareader:

                # basic data
                einspeisung = 0
                netznutzung = 0

                if(car is not None):
                    hourOfTheDay = int(row['Stunde']) % 24
                    # car parks at home at 18 Uhr
                    if(hourOfTheDay == 12):
                        carBatteryLevelCurrentDay -= car[1] / 100 * kmProTag
                        carUsableAsBattery = True
                    # car leaves home at 6 Uhr
                    elif(hourOfTheDay == 6):
                        netznutzung += car[0] - carBatteryLevelCurrentDay
                        carBatteryLevelCurrentDay = car[0]
                        carUsableAsBattery = False

                produktion = float(row['Einstrahlung in Modulebene m2']
                                   ) * modulgrosse * wirkungsgrad * verluste

                verbrauch = float(row['Verbrauch 4 Pers'])
                remainingEnergy = produktion - verbrauch
                remainingEnergyWithBattery = remainingEnergy + batteryBefore

                if(remainingEnergyWithBattery >= batteryCapacity):
                    remainingEnergyAfterFillingBattery = abs(
                        remainingEnergyWithBattery - batteryCapacity)
                    batteryNow = batteryCapacity
                    if(carUsableAsBattery and car[0] > carBatteryLevelCurrentDay + remainingEnergyAfterFillingBattery):
                        # we use the car as a battery
                        carBatteryLevelCurrentDay += remainingEnergyAfterFillingBattery
                    else:
                        einspeisung += remainingEnergyAfterFillingBattery
                elif(remainingEnergyWithBattery < 0):
                    batteryNow = 0.0
                    netznutzung += abs(remainingEnergyWithBattery)
                else:
                    batteryNow = remainingEnergyWithBattery

                # eigenverbrauch
                eigenverbrauch = produktion - einspeisung

                # totale
                produktionTotal += produktion
                einspeisungTotal += einspeisung
                netznutzungTotal += netznutzung
                eigenverbrauchTotal += eigenverbrauch
                verbrauchTotal += verbrauch

                # stuff
                batteryBefore = batteryNow
                # print('Stunde', row['Stunde'], 'Datum', row['Datum'], 'Produktion', row['Einstrahlung in Modulebene m2'], 'Verbrauch',
                #      row['Verbrauch 4 Pers'], 'Battery', batteryNow, 'Einspeisung', einspeisung, 'Netznutzung', netznutzung, 'Eigenverbrauch', eigenverbrauch)

        print('produktionTotal', produktionTotal, 'verbrauchTotal', verbrauchTotal, 'einspeisungTotal', einspeisungTotal,
              'netznutzungTotal', netznutzungTotal, 'eigenverbrauchTotal', eigenverbrauchTotal)

        return {'produktionTotal': produktionTotal, 'verbrauchTotal': verbrauchTotal, 'einspeisungTotal': einspeisungTotal, 'netznutzungTotal': netznutzungTotal, 'eigenverbrauchTotal': eigenverbrauchTotal}

    def calculateDays(self, modulgrosse, batteryCapacity=0, wirkungsgrad=0.14, verluste=0.75, car=None, kmProTag=None):
        batteryBefore = 0

        result = []

        if(car is not None):
            carBatteryLevelCurrentDay = car[0]

        carUsableAsBattery = False
        with open('daten.csv', newline='') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=';')
            for row in datareader:

                # basic data
                einspeisung = 0
                netznutzung = 0

                if(car is not None):
                    hourOfTheDay = int(row['Stunde']) % 24
                    # car parks at home at 18 Uhr
                    if(hourOfTheDay == 12):
                        carBatteryLevelCurrentDay -= car[1] / 100 * kmProTag
                        carUsableAsBattery = True
                    # car leaves home at 6 Uhr
                    elif(hourOfTheDay == 6):
                        netznutzung += car[0] - carBatteryLevelCurrentDay
                        carBatteryLevelCurrentDay = car[0]
                        carUsableAsBattery = False

                produktion = float(row['Einstrahlung in Modulebene m2']
                                   ) * modulgrosse * wirkungsgrad * verluste

                verbrauch = float(row['Verbrauch 4 Pers'])
                remainingEnergy = produktion - verbrauch
                remainingEnergyWithBattery = remainingEnergy + batteryBefore

                if(remainingEnergyWithBattery >= batteryCapacity):
                    remainingEnergyAfterFillingBattery = abs(
                        remainingEnergyWithBattery - batteryCapacity)
                    batteryNow = batteryCapacity
                    if(carUsableAsBattery and car[0] > carBatteryLevelCurrentDay + remainingEnergyAfterFillingBattery):
                        # we use the car as a battery
                        carBatteryLevelCurrentDay += remainingEnergyAfterFillingBattery
                    else:
                        einspeisung += remainingEnergyAfterFillingBattery
                elif(remainingEnergyWithBattery < 0):
                    batteryNow = 0.0
                    netznutzung += abs(remainingEnergyWithBattery)
                else:
                    batteryNow = remainingEnergyWithBattery

                # eigenverbrauch
                eigenverbrauch = produktion - einspeisung

                # stuff
                batteryBefore = batteryNow

                # totale
                result.append({'stunde': row['Stunde'], 'produktion': produktion, 'verbrauch': verbrauch, 'einspeisung': einspeisung,
                               'netznutzung': netznutzung, 'eigenverbrauch': eigenverbrauch})

        return result
