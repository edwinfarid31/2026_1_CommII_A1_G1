import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='Monitor de Ruido', # Nombre más descriptivo
            in_sig=[np.float32],
            out_sig=[np.float32, np.float32, np.float32, np.float32, np.float32]
        )
        self.acum_anterior = 0.0
        self.acum_anterior1 = 0.0
        self.Ntotales = 0

    def work(self, input_items, output_items):
        x = input_items[0]
        
        # Si no hay muestras, no hace nada
        if len(x) == 0:
            return 0

        y0, y1, y2, y3, y4 = output_items

        N = len(x)
        self.Ntotales += N

        # MEDIA (y0)
        acumulado = self.acum_anterior + np.cumsum(x)
        self.acum_anterior = acumulado[-1]
        y0[:] = acumulado / self.Ntotales

        # MEDIA CUADRÁTICA (y1)
        x2 = x**2
        acumulado1 = self.acum_anterior1 + np.cumsum(x2)
        self.acum_anterior1 = acumulado1[-1]
        y1[:] = acumulado1 / self.Ntotales

        # RMS (y2) y POTENCIA (y3)
        y2[:] = np.sqrt(np.maximum(y1, 0)) # Protege contra valores negativos mínimos
        y3[:] = y1

        # DESVIACIÓN ESTÁNDAR (y4) - El nivel de ruido ambiental
        # Usamos clip para evitar errores matemáticos por precisión decimal
        varianza = np.maximum(y1 - y0**2, 0)
        y4[:] = np.sqrt(varianza)

        return len(x)