# Das Elektroauto muss im Code bei der Methode simulate konfiguriert werden.
# Die gefahrenen km pro Tag müssen im Code bei der Methode simulate konfiguriert werden.

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.widgets import Slider
import calculator as calc
sim = calc.Simulator()

# Autos (Kapazität, Verbrauch pro 100km)
elektroautoTeslaKlein = 75, 18.5
elektroautoTeslaGross = 100, 18.9
elektroautoRenaultZoe = 22, 13.3
elektroautoBMWi3 = 18.8, 13.1
elektroautoNissanLeaf = 40, 17.4

# Variablen
simulationsResultate = 0
eigenverbrauchProH = 0
eigenverbrauchProJ = 0
produktionProJ = 0
EVA = 0
nth = 24
modulgrosse = 50
batterieKapazitat = 6

# simulates the year and saves result in simulationsResultate


def simulate(modulgrosse, batterieKapazitat=0, elektroAuto=elektroautoTeslaKlein, kmProTag=50):
    global simulationsResultate
    simulationsResultate = sim.calculateDays(
        modulgrosse, batterieKapazitat=batterieKapazitat, elektroAuto=elektroAuto, kmProTag=kmProTag)


# calculates based on simulationResults the Eigenverbrauch per hour
def calculateEV():
    global eigenverbrauchProH
    # selektiert eine einzelne Spalte aus dem Datensatz
    eigenverbrauchProH = [v['eigenverbrauch'] for v in simulationsResultate]


# calculates based on simulationResults the EVA per year
def calculateEVA():
    global EVA
    global produktionProH
    global produktionProJ
    # selektiert eine einzelne Spalte aus dem Datensatz
    produktionProH = [v['produktion'] for v in simulationsResultate]

    produktionProJ = 0
    for _, val in enumerate(produktionProH):
        produktionProJ += val

    EVA = eigenverbrauchProJ / produktionProJ

# sums up eigenverbrauch every nth value to fit in plot form


def transformiereInYform():
    global nth
    global eigenverbrauchProJ
    y = []
    currSum = 0
    eigenverbrauchProJ = 0
    for idx, val in enumerate(eigenverbrauchProH):
        if(idx % nth == 0):
            y.append(currSum)
            eigenverbrauchProJ += currSum
            currSum = 0
        else:
            currSum += val
    return y

# updates the calculation based on slider values


def update(val):
    global modulgrosse
    global batterieKapazitat
    modulgrosse = slidersqm.val
    batterieKapazitat = sliderbattery.val
    simulate(modulgrosse, batterieKapazitat)
    calculateEV()
    yData = transformiereInYform()
    calculateEVA()
    l.set_ydata(yData)
    ax.set_title(
        f'EV über ein Jahr mit {int(round(modulgrosse))} qm PV Anlage und {int(round(batterieKapazitat))} kWh Batterie-Kapazität - Total Produktion={round(produktionProJ, 2)} - Total EV={round(eigenverbrauchProJ, 2)} - EVA={round(EVA * 100, 2)}%')
    fig.canvas.draw_idle()


# plot init
fig, ax = plt.subplots()
# adjusts the plot itself
plt.subplots_adjust(left=0.1, bottom=0.25)

# creates x axis values
x = range(0, int(8760/nth))

# calculates everything
simulate(modulgrosse, batterieKapazitat)
calculateEV()
yData = transformiereInYform()
calculateEVA()

# sets axis limits
ax.set_ylim(0, 30)

# plot
l, = ax.plot(x, yData, label='EVA')

# sets title
ax.set_title(
    f'EVA over the year with {int(round(modulgrosse))} qm solar panels and {int(round(batterieKapazitat))} kWh batterieKapazität - Total Produktion={round(produktionProJ, 2)} - Total EV={round(eigenverbrauchProJ, 2)} - EVA={round(EVA * 100, 2)}%')

# square meter slider
axcolor = 'lightblue'
axqm = plt.axes([0.2, 0.05, 0.7, 0.03], facecolor=axcolor)
f0 = modulgrosse
delta_f = 5
slidersqm = Slider(axqm, 'QM', 10, 100, valinit=f0, valstep=delta_f)

slidersqm.on_changed(update)

# batterieKapazität size slider
axcolor = 'lightblue'
axbatt = plt.axes([0.2, 0.1, 0.7, 0.03], facecolor=axcolor)
g0 = batterieKapazitat
delta_g = 1
sliderbattery = Slider(
    axbatt, 'Kapazität Batterie [kWh]', 0, 13, valinit=g0, valstep=delta_g)

sliderbattery.on_changed(update)

# creates a legend
ax.legend(loc='upper center', bbox_to_anchor=(
    0.5, -0.05),  shadow=True, ncol=2)

# displays the plot
plt.show()
