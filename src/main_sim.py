from neuron import h
import numpy
import pylab as pl
from matplotlib import pyplot as plt
import time
#from matplotlib import ion

def plot_voltage(voltage_plot,vectors_dict):
    pl.ion()
    voltage_plot.set_xdata(vectors_dict['t'])
    voltage_plot.set_ydata(vectors_dict['v_post'])
    pl.draw()
#     plot = plt.subplot(2,1,1)
#
#     plt1, = plot.plot(vectors_dict['t'],vectors_dict['v_post'])
#     plt2, = plot.plot(numpy.arange(0,len(vectors_dict['calcium_level'])*0.025,0.025),numpy.array(vectors_dict['calcium_level'])*60-60)
#     plt.legend([plt1, plt2], ["Post-synaptic voltage", "contraction instruction"])
#
#     plt.ylabel('Voltage in mV and contraction instruction(arbitrary units)')
#
#     plot = plt.subplot(2,1,2)
#
#     plot.plot(vectors_dict['t'],vectors_dict['v_pre'])
#     plt.ylabel('Voltage in mV')
#
#     plt.xlabel('Time in ms')
#     plt.draw()

class muscle_simulation():

    #simple simulation to test the principle

    def __init__(self,increment=1.0):
        #create pre- and post- synaptic sections

        self.increment = increment
        self.pre = h.Section()
        self.post = h.Section()

        for sec in self.pre,self.post:
            sec.insert('hh')

        #inject current in the pre-synaptic section
        self.stim = h.IClamp(0.5, sec=self.pre)
        self.stim.amp = 70.0
        self.stim.delay = 1500.0
        self.stim.dur = 500.0

        #create a synapse in the pre-synaptic section
        self.syn = h.ExpSyn(0.5,sec=self.post)

        #connect the pre-synaptic section to the synapse object:
        self.nc = h.NetCon(self.pre(0.5)._ref_v,
                           self.syn)
        self.nc.weight[0] = 10.0

        # record the membrane potentials and
        # synaptic currents
        vec = {}
        for var in 'v_pre', 'v_post', 'i_syn', 't':
            vec[var] = h.Vector()
        vec['v_pre'].record(self.pre(0.5)._ref_v )
        vec['v_post'].record(self.post(0.5)._ref_v )
        vec['i_syn'].record(self.syn._ref_i )
        vec['t'].record(h._ref_t)

        self.vector = vec

        #Initialize the simulation
        h.load_file ("stdrun.hoc")
        h.init()

        #let's do some manaical  experimentation of the most evil kind:
        self.calcium_level = 0
        self.vector['calcium_level']=[self.calcium_level]

        self.voltage_plot, = plt.plot([],[])
        #plt.show()

    def addition_rate(self):
        opening = abs(self.vector['v_post'][-1]+65)
        opening = (opening**2/(opening**2+opening))
        current = opening*(1-self.calcium_level)/100
        return current

    def removal_rate(self):
        opening = abs(20-self.vector['v_post'][-1])
        opening = (opening**2/(opening**2+opening))
        current = opening*(self.calcium_level)/100
        return -current


    def run(self,do_plot = True):
    #run and return resting potential
        t_now = h.t
        while h.t < t_now + self.increment:
            h.fadvance()
            self.calcium_level += self.addition_rate()+self.removal_rate()
            self.vector['calcium_level'].append(self.calcium_level)
        if do_plot:
            print len(self.vector['calcium_level'])
            plot_voltage(self.voltage_plot,self.vector)

        return self.calcium_level

#example use:
#a=muscle_simulation(increment=250)
#print a.run(do_plot=True)
#time.sleep(50)
#print a.run(do_plot=True)
#del(a) #delete the object
#print a.run(do_plot=True)
