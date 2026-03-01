import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='Diferenciador Python',   # Nombre que verás en GRC
            in_sig=[np.float32],           # Tipo de entrada: float
            out_sig=[np.float32]           # Tipo de salida: float
        )
        # Variable para guardar el último valor de la ráfaga anterior
        self.last_sample = 0.0

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        
        # Creamos un vector desplazado que incluya la última muestra del bloque anterior
        # Esto evita picos de error entre ráfagas de datos
        temp_input = np.insert(in0, 0, self.last_sample)
        
        # Calculamos la diferencia: out[n] = in[n] - in[n-1]
        out[:] = np.diff(temp_input)
        
        # Guardamos la última muestra actual para el próximo ciclo
        self.last_sample = in0[-1]
        
        return len(out)
