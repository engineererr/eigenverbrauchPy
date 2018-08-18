import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.widgets import Slider
import calculator as calc
sim = calc.Simulator()

# battery capacity in kwh, kwh/100km
elektroautoTeslaKlein = 75, 18.5
elektroautoTeslaGross = 100, 18.9
elektroautoRenaultZoe = 22, 13.3
elektroautoBMWi3 = 18.8, 13.1
elektroautoNissanLeaf = 40, 17.4

# variables
simulationResult = 0
eigenverbrauchProH = 0
eigenverbrauchProJ = 0
produktionProJ = 0
EVA = 0
nth = 24
modulgrosse = 10
batterygrosse = 6


# simulates the year and saves result in simulationResult
def simulate(modulgrosse, battery=0):
    global simulationResult
    simulationResult = sim.calculateDays(modulgrosse, batteryCapacity=battery)


# calculates based on simulationResults the Eigenverbrauch per hour
def calculateEV():
    global eigenverbrauchProH
    eigenverbrauchProH = [v['eigenverbrauch'] for v in simulationResult]


# calculates based on simulationResults the EVA per year
def calculateEVA():
    global EVA
    global produktionProH
    global produktionProJ
    produktionProH = [v['produktion'] for v in simulationResult]

    produktionProJ = 0
    for val in enumerate(produktionProH):
        produktionProJ += val

    eva = eigenverbrauchProJ / produktionProJ


def calcY():
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


def update(val):
    global modulgrosse
    global batterygrosse
    modulgrosse = slidersqm.val
    batterygrosse = sliderbattery.val
    simulate(modulgrosse, batterygrosse)
    calculateEV()
    yData = calcY()
    l.set_ydata(yData)
    ax.set_title(
        f'EVA over the year with {int(round(modulgrosse))} qm solar panels and {int(round(batterygrosse))} kWh battery - Total EVA={round(EVA, 2)}')
    fig.canvas.draw_idle()


# plot init
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.25)
x = range(0, int(8760/nth))

# plot
simulate(modulgrosse, batterygrosse)
calculateEV()
yData = calcY()
l, = ax.plot(x, yData, label='EVA')

ax.set_title(
    f'EVA over the year with {int(round(modulgrosse))} qm solar panels and {int(round(batterygrosse))} kWh battery - Total EV={round(eigenverbrauchProJ, 2)} - EVA={EVA}')

ax.set_ylim(0, 30)
# squaremeter slider
axcolor = 'lightblue'
axqm = plt.axes([0.1, 0.05, 0.8, 0.03], facecolor=axcolor)
f0 = 50
delta_f = 5
slidersqm = Slider(axqm, 'QM', 10, 100, valinit=f0, valstep=delta_f)

slidersqm.on_changed(update)

# battery size slider
axcolor = 'lightblue'
axbatt = plt.axes([0.1, 0.1, 0.8, 0.03], facecolor=axcolor)
g0 = 6
delta_g = 1
sliderbattery = Slider(axbatt, 'Battery', 0, 13, valinit=g0, valstep=delta_g)

sliderbattery.on_changed(update)

# legendary
ax.legend(loc='upper center', bbox_to_anchor=(
    0.5, -0.05),  shadow=True, ncol=2)
plt.show()
