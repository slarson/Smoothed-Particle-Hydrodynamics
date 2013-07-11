import math
import numpy as np
from matplotlib import pyplot as plt

def parallel_waves(n=26, #26 for our first test?
                   time=0, 
                   phi=math.pi,
                   amplitude=1,
                   velocity=1):
    """
    Array of two travelling waves, second one starts
    half way through the array
    """

    if n % 2 != 0:
        raise NotImplementedError("Currently only supports even number of muscles!")

    j = n/2

    row_positions = np.linspace(0,1.5*2*math.pi,j)

    wave_1 = (map(math.sin,(row_positions - velocity*time)))
    wave_2 = (map(math.sin,(row_positions + (math.pi / 2) - velocity*time)))

    normalize_sine = lambda x : (x + 1)/2
    wave_1 = map(normalize_sine, wave_1)
    wave_2 = map(normalize_sine, wave_2)

    return wave_1 + wave_2

class muscle_simulation():

    def plot(self):
        n = len(self.contraction_array)
        plot_1, = plt.plot(np.array(self.contraction_array[0:n/2]))
        plot_2, = plt.plot(np.array(self.contraction_array[n/2:n]))
        plt.title("Muscle activation signal at time %f" % self.t)
        plt.xlabel("Muscle block number")
        plt.ylabel("Activation signal")
        plt.legend([plot_1,plot_2,],["RHS","LHS",])
        plt.show()

    def __init__(self,increment=1.0):
        self.increment = increment
        self.t = 0

    def run(self,do_plot = True):
        self.contraction_array =  parallel_waves(time = self.t)
        self.t += self.increment

a = muscle_simulation(increment=0.1)
for i in range(1,10):
    a.run()
    a.plot()
