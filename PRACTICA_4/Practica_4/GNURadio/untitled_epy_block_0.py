

import numpy as np
from gnuradio import gr

class blk(gr.sync_block):  
    """This block is a Complex Exponential (CE) Voltage-Controlled Oscillator (VCO) or Baseband VCO. 
    It works by generating a complex exponential signal with amplitude and phase modulation.
    """

    def __init__(self,):  
        # Initialize the sync block with the specified input and output signal types
        gr.sync_block.__init__(
            self,
            name='VCO Complex',  # Name of the block
            in_sig=[np.float32, np.float32],  # Input: two float32 arrays (amplitude and phase)
            out_sig=[np.complex64]  # Output: one complex64 array (modulated signal in complex form)
        )
        
    def work(self, input_items, output_items):
        # Get the amplitude (A) and phase (Q) from the input items
        A = input_items[0]  # Amplitude input signal
        Q = input_items[1]  # Phase input signal
        Sec = output_items[0]  # Output signal array (modulated complex signal)

        
        # Generate the complex exponential output signal using the formula:
        # y = A * exp(j*Q)
        Sec[:] = A * np.exp(1j * Q)  # complex exponential signal
        
        
        return len(Sec)