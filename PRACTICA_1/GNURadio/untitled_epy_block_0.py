import numpy as np
from gnuradio import gr


class blk(gr.sync_block):

    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='Promedios_de_tiempos',
            in_sig=[np.float32],
            out_sig=[np.float32, np.float32, np.float32, np.float32, np.float32]
        )

        self.acum_anterior = 0
        self.acum_anterior1 = 0
        self.Ntotales = 0

    def work(self, input_items, output_items):
        x = input_items[0]

        y0 = output_items[0]   # Media
        y1 = output_items[1]   # Media cuadrática
        y2 = output_items[2]   # RMS
        y3 = output_items[3]   # Potencia promedio
        y4 = output_items[4]   # Desviación estándar

        N = len(x)
        self.Ntotales += N

        # ===== MEDIA =====
        acumulado = self.acum_anterior + np.cumsum(x)
        self.acum_anterior = acumulado[-1]
        y0[:] = acumulado / self.Ntotales

        # ===== MEDIA CUADRATICA =====
        x2 = x**2
        acumulado1 = self.acum_anterior1 + np.cumsum(x2)
        self.acum_anterior1 = acumulado1[-1]
        y1[:] = acumulado1 / self.Ntotales

        # ===== RMS =====
        y2[:] = np.sqrt(y1)

        # ===== POTENCIA PROMEDIO =====
        y3[:] = y1

        # ===== DESVIACION ESTANDAR (forma correcta en streaming) =====
        y4[:] = np.sqrt(y1 - y0**2)

        return len(x)