import csv
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# in kwh, kwh/100km
elektroautoTeslaKlein = 75, 18.5
elektroautoTeslaGross = 100, 18.9
elektroautoRenaultZoe = 22, 13.3
elektroautoBMWi3 = 18.8, 13.1
elektroautoNissanLeaf = 40, 17.4


def calculate(modulgrosse, batteryCapacity=0, wirkungsgrad=0.14, verluste=0.75, car=None, kmProTag=None):
    batteryBefore = 0
    produktionTotal = 0

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

            remainingEnergy = produktion - \
                float(row['Verbrauch 4 Pers'])
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

            # stuff
            batteryBefore = batteryNow
            # print('Stunde', row['Stunde'], 'Datum', row['Datum'], 'Produktion', row['Einstrahlung in Modulebene m2'], 'Verbrauch',
            #      row['Verbrauch 4 Pers'], 'Battery', batteryNow, 'Einspeisung', einspeisung, 'Netznutzung', netznutzung, 'Eigenverbrauch', eigenverbrauch)

    # print('produktionTotal', produktionTotal, 'einspeisungTotal', einspeisungTotal,
    #       'netznutzungTotal', netznutzungTotal, 'eigenverbrauchTotal', eigenverbrauchTotal)

    return {'produktionTotal': produktionTotal, 'einspeisungTotal': einspeisungTotal, 'netznutzungTotal': netznutzungTotal, 'eigenverbrauchTotal': eigenverbrauchTotal}


# resultatMitBatteryOhneAuto = calculate(batteryCapacity=13,
#                                        modulgrosse=25)

# resultatMitBatteryMitAuto = calculate(modulgrosse=25,
#                                       car=elektroautoTeslaKlein,
#                                       kmProTag=60)


# resultatOhneBatteryOhneAuto = calculate(modulgrosse=25)


# resultatOhneBatteryMitAuto = calculate(modulgrosse=25,
#                                        car=elektroautoTeslaKlein,
#                                        kmProTag=40)


# print('Eigenverbrauch mit Batterie um', resultMitBattery['eigenverbrauchTotal'] /
#       resultOhneBattery['eigenverbrauchTotal'], 'mal höher')

# print('Eigenverbrauch mit Batterie und mit Auto um', resultatMitBatteryMitAuto['eigenverbrauchTotal'] /
#       resultatMitBatteryOhneAuto['eigenverbrauchTotal'], 'mal höher als ohne Auto')

# eigenverbrauchNullBisHundert = []
# for x in range(0, 100):
#     # print('Modulgrösse', x)
#     resultatMitBatteryOhneAuto = calculate(batteryCapacity=13,
#                                            modulgrosse=x)
#     eigenverbrauchNullBisHundert.append(
#         resultatMitBatteryOhneAuto['eigenverbrauchTotal'])

def calculateModulgrosseRange(range):
    result = []
    for x in range:
        result.append(calculate(modulgrosse=x)[
                      'eigenverbrauchTotal'])
    return result


def calculateKmGefahrenRange(range, modulgrosse):
    result = []
    for x in range:
        result.append(calculate(modulgrosse=modulgrosse, car=elektroautoTeslaGross, kmProTag=x)[
                      'eigenverbrauchTotal'])
    return result


x = range(0, 100, 10)

plt.title('KM driven by different module sizes')

ax = plt.subplot(111)

ax.plot(x, calculateKmGefahrenRange(x, 10), label='10')
ax.plot(x, calculateKmGefahrenRange(x, 20), label='20')
# plt.plot(x, calculateKmGefahrenRange(x, 30), label='30')
# plt.plot(x, calculateKmGefahrenRange(x, 40), label='40')
# plt.plot(x, calculateKmGefahrenRange(x, 50), label='50')
ax.legend(loc='upper center', bbox_to_anchor=(
    0.5, -0.05),  shadow=True, ncol=2)
plt.show()
