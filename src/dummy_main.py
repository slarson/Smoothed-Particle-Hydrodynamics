"""
C elegans dummy model - will always return 0.3 or some such constant
"""

class muscle_simulation():

    def __init__(self,
                 k_fast_specific_gbar = 36.0,
                 k_slow_specific_gbar = 0.0,
                 ca_channel_specific_gbar = 120.0,
		 ca_h_A_F = 20.0,
                 k_tau_factor = 1.0,
                 ca_tau_factor = 1.0,
		 nocompile = True):

        pass

    def run(self):
        return 0.3
