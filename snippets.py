

# def calculateModulgrosseRange(range):
#     result = []

#     preisProKwhBezogen = 27.65 / 100  # chf
#     preisProKwhEingespiesen = 9.19 / 100  # chf

#     preisProQmModul = 700.0  # chf

#     anzahlJahre = 25

#     for x in range:
#         print('anzahl qm', x)
#         preisOhneAnlage = 0
#         preisMitAnlage = 0
#         kwhPreisProduzierte = 0
#         eingespiesenPreisTotal = 0
#         nichtBezogenPreisTotal = 0
#         bezogenPreisTotal = 0

#         res = sim.calculate(modulgrosse=x)
#         result.append(res['eigenverbrauchTotal'])

#         preisOhneAnlage = res['verbrauchTotal'] * preisProKwhBezogen

#         kwhPreisProduzierte = x * preisProQmModul / \
#             anzahlJahre / res['produktionTotal']

#         eingespiesenPreisTotal = res['einspeisungTotal'] * \
#             preisProKwhEingespiesen
#         bezogenPreisTotal = res['netznutzungTotal'] * preisProKwhBezogen

#         preisMitAnlage = res['eigenverbrauchTotal'] * \
#             kwhPreisProduzierte + bezogenPreisTotal - eingespiesenPreisTotal

#         print('preisOhneAnlage', preisOhneAnlage,
#               'preisMitAnlage', preisMitAnlage)

#     return result


# def calculateKmGefahrenRange(range, modulgrosse):
#     result = []
#     for x in range:
#         result.append(sim.calculate(modulgrosse=modulgrosse, car=elektroautoTeslaGross, kmProTag=x)[
#                       'eigenverbrauchTotal'])
#     return result


# x=range(1, 102, 10)
# plt.title('KM driven by different module sizes')

# ax = plt.subplot(111)

# ax.plot(x, calculateKmGefahrenRange(x, 10), label='10')
# ax.plot(x, calculateKmGefahrenRange(x, 20), label='20')
# # plt.plot(x, calculateKmGefahrenRange(x, 30), label='30')
# # plt.plot(x, calculateKmGefahrenRange(x, 40), label='40')
# # plt.plot(x, calculateKmGefahrenRange(x, 50), label='50')
# ax.legend(loc='upper center', bbox_to_anchor=(
#     0.5, -0.05),  shadow=True, ncol=2)
# plt.show()


# resultatMitBatteryOhneAuto = sim.calculate(batteryCapacity=13,
#                                        modulgrosse=25)

# resultatMitBatteryMitAuto = sim.calculate(modulgrosse=25,
#                                       car=elektroautoTeslaKlein,
#                                       kmProTag=60)


# resultatOhneBatteryOhneAuto = sim.calculate(modulgrosse=25)


# resultatOhneBatteryMitAuto = sim.calculate(modulgrosse=25,
#                                        car=elektroautoTeslaKlein,
#                                        kmProTag=40)


# print('Eigenverbrauch mit Batterie um', resultMitBattery['eigenverbrauchTotal'] /
#       resultOhneBattery['eigenverbrauchTotal'], 'mal höher')

# print('Eigenverbrauch mit Batterie und mit Auto um', resultatMitBatteryMitAuto['eigenverbrauchTotal'] /
#       resultatMitBatteryOhneAuto['eigenverbrauchTotal'], 'mal höher als ohne Auto')

# eigenverbrauchNullBisHundert = []
# for x in range(0, 100):
#     # print('Modulgrösse', x)
#     resultatMitBatteryOhneAuto = sim.calculate(batteryCapacity=13,
#                                            modulgrosse=x)
#     eigenverbrauchNullBisHundert.append(
#         resultatMitBatteryOhneAuto['eigenverbrauchTotal'])
