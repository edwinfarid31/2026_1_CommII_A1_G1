import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='Acumulador',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.suma = 0.0

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        for i in range(len(in0)):
            self.suma += in0[i]
            out[i] = self.suma

        return len(out)