import tkinter as tk

from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time

# PARÁMETROS TÉCNICOS DEL SISTEMA (Unidad 3)
BITS_DATOS = 8                 
BITS_TRAMA = BITS_DATOS + 1    
FRECUENCIA_PORTADORA = 5       
MUESTRAS_POR_BIT = 120         
MUESTRAS_POR_CARACTER = MUESTRAS_POR_BIT * BITS_TRAMA  
NIVELES_ASK = 2                
UMBRAL_DETECCION = 0.35        
FS_EFECTIVA = MUESTRAS_POR_BIT

CAPAS_OSI = [
    "1. APLICACIÓN",
    "2. PRESENTACIÓN",
    "3. SESIÓN",
    "4. TRANSPORTE",
    "5. RED",
    "6. ENLACE DE DATOS",
    "7. FÍSICA",
]

class SimuladorContextoRealUNEMI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("PROYECTO: Transmisión de Datos con Contexto Real - UNEMI")
        try:
            self.root.state('zoomed')          
        except tk.TclError:
            try:
                self.root.attributes('-zoomed', True)  
            except tk.TclError:
                self.root.geometry("1280x800")          
        self.root.configure(bg="#1e1e2f")

        # BASE DE DATOS DE CONTEXTO REAL (Basado en el material de clase)
        self.detalles_reales = [
            {
                "ejemplo": "WHATSAPP (WI-FI)",
                "explicacion": "Los bits de tu mensaje se modulan en ondas de radio de 2.4GHz. Aquí se aplica el Subtema 1: Datos digitales viajando en señales analógicas.",
                "teoria": "Teorema de Nyquist: Define la tasa máxima de bits en el aire."
            },
            {
                "ejemplo": "NETFLIX (FIBRA ÓPTICA)",
                "explicacion": "La luz se enciende y apaga (bits) para viajar por el vidrio. Es una señal periódica se relaciona con el Subtema 2 de altísima frecuencia.",
                "teoria": "Ancho de Banda: Es masivo, permitiendo video en 4K sin retrasos."
            },
            {
                "ejemplo": "LLAMADA CELULAR",
                "explicacion": "Tu voz es una señaal analógica se digitaliza para procesarse y luego vuelve a ser onda para salir por la antena.",
                "teoria": "Relación Señal/Ruido (SNR): Si hay interferencia, la calidad de voz baja."
            },
            {
                "ejemplo": "CONTROL DE TV (INFRARROJO)",
                "explicacion": "Pulsas un botón representando un dato discreto y un LED emite ráfagas de luz invisible que el TV interpreta.",
                "teoria": "Codificación: Cada botón tiene una secuencia de bits única."
            },
            {
                "ejemplo": "TRANSACCIÓN CAJERO (ATM)",
                "explicacion": "Tus datos bancarios viajan encriptados por cables de cobre usando módems DSL.",
                "teoria": "Ciberseguridad: Es una vulnerabilidad compartida en redes públicas."
            }
        ]

        # ESTADÍSTICAS GLOBALES DE LA TRANSMISIÓN 
        self.bits_totales = 0
        self.bits_con_error = 0
        self.mensaje_recibido = ""

        # DISEÑO RESPONSIVO 
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(4, weight=1)

        # 1. Encabezado
        header = tk.Frame(root, bg="#002147", pady=8)
        header.grid(row=0, column=0, sticky="ew")
        tk.Label(header, text="UNIVERSIDAD ESTATAL DE MILAGRO (UNEMI)", font=("Helvetica", 16, "bold"), bg="#002147", fg="white").pack()
        tk.Label(header, text="Materia: Comunicación de Datos | Docente: Ing. Alex Armando Ávila Coello, Mgtr.", font=("Helvetica", 10), bg="#002147", fg="#ffcc00").pack()

        # 2. Conceptos clave + Panel Nyquist (dinámico)
        diff_frame = tk.Frame(root, bg="#2a2a40", pady=6, bd=1, relief=tk.RIDGE)
        diff_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=4)
        tk.Label(diff_frame, text="CONCEPTOS CLAVE DE LA UNIDAD 3", font=("Helvetica", 10, "bold"), bg="#2a2a40", fg="#00d2ff").pack()
        info_txt = "Señal Digital: Discreta (0,1) | Señal Analógica: Continua (Ondas) | Teorema de Nyquist: C = 2 * B * log2(L)"
        tk.Label(diff_frame, text=info_txt, font=("Helvetica", 9), bg="#2a2a40", fg="white").pack()

        self.lbl_nyquist = tk.Label(diff_frame, text=self._texto_nyquist_estatico(),
                                     font=("Consolas", 9, "bold"), bg="#2a2a40", fg="#33ff33")
        self.lbl_nyquist.pack(pady=(4, 0))

        # 2.5 Animación de Codificación ASCII (carácter -> decimal -> 8 bits, en vivo)
        ascii_frame = tk.Frame(root, bg="#2a2a40", pady=6, bd=1, relief=tk.RIDGE)
        ascii_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=4)
        tk.Label(ascii_frame, text="ANIMACIÓN DE CODIFICACIÓN ASCII", font=("Helvetica", 10, "bold"),
                 bg="#2a2a40", fg="#00d2ff").pack(pady=(0, 4))

        fila_ascii = tk.Frame(ascii_frame, bg="#2a2a40")
        fila_ascii.pack()

        tk.Label(fila_ascii, text="Carácter:", font=("Arial", 9), bg="#2a2a40", fg="white").pack(side=tk.LEFT, padx=(0, 4))
        self.lbl_ascii_char = tk.Label(fila_ascii, text="-", font=("Consolas", 12, "bold"),
                                        bg="#1e1e2f", fg="#ffcc00", width=3, relief=tk.SUNKEN)
        self.lbl_ascii_char.pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(fila_ascii, text="Código ASCII (dec):", font=("Arial", 9), bg="#2a2a40", fg="white").pack(side=tk.LEFT, padx=(0, 4))
        self.lbl_ascii_dec = tk.Label(fila_ascii, text="-", font=("Consolas", 12, "bold"),
                                       bg="#1e1e2f", fg="#ffcc00", width=4, relief=tk.SUNKEN)
        self.lbl_ascii_dec.pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(fila_ascii, text="Binario (8 bits):", font=("Arial", 9), bg="#2a2a40", fg="white").pack(side=tk.LEFT, padx=(0, 6))
        self.lbls_ascii_bits = []
        for _ in range(BITS_DATOS):
            b = tk.Label(fila_ascii, text="0", font=("Consolas", 11, "bold"), bg="#3a3a55", fg="white",
                         width=2, relief=tk.RIDGE, bd=1)
            b.pack(side=tk.LEFT, padx=2)
            self.lbls_ascii_bits.append(b)

        # 3. Panel de Capas OSI (se ilumina capa por capa durante la transmisión)
        osi_frame = tk.Frame(root, bg="#1e1e2f", pady=4)
        osi_frame.grid(row=3, column=0, sticky="ew", padx=20)
        tk.Label(osi_frame, text="ENCAPSULADO - MODELO OSI (el Entry de texto recorre estas capas)",
                 font=("Helvetica", 9, "bold"), bg="#1e1e2f", fg="#ffcc00").pack()
        capas_bar = tk.Frame(osi_frame, bg="#1e1e2f")
        capas_bar.pack(fill=tk.X, pady=4)
        self.layer_labels = []
        for capa in CAPAS_OSI:
            lbl = tk.Label(capas_bar, text=capa, font=("Consolas", 8, "bold"),
                            bg="#3a3a55", fg="white", padx=6, pady=4, relief=tk.GROOVE, bd=1)
            lbl.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
            self.layer_labels.append(lbl)

        # 4. Área de Gráficos (3 etapas: digital, canal/portadora, receptor)
        self.main = tk.Frame(root, bg="#1e1e2f")
        self.main.grid(row=4, column=0, sticky="nsew", padx=20)
        self.main.columnconfigure(0, weight=1)

        # Indicador en vivo: muestra el carácter que se está transportando
        # en este instante, arriba de las gráficas.
        self.lbl_transmision = tk.Label(self.main, text="📡 Esperando transmisión...",
                                         font=("Consolas", 11, "bold"), bg="#1e1e2f", fg="#00d2ff")
        self.lbl_transmision.pack(fill=tk.X, padx=40, pady=(4, 0))

        self.fig, (self.ax_dig, self.ax_ana, self.ax_rx) = plt.subplots(3, 1, figsize=(6, 5.2))
        self.fig.patch.set_facecolor('#2a2a40')
        self.fig.subplots_adjust(hspace=0.9)
        for ax in [self.ax_dig, self.ax_ana, self.ax_rx]:
            ax.set_facecolor('#1e1e2f')
            ax.tick_params(colors='white', labelsize=7)
            ax.title.set_color('white')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=40)

        # Títulos descriptivos fijos: explican qué representa cada gráfico,
        # visibles incluso antes de presionar "Transmitir".
        self.ax_dig.set_title("① TRANSMISOR — Bits Digitales de la Trama (8 datos + 1 paridad)", fontsize=8)
        self.ax_ana.set_title("② CANAL — Señal Analógica Modulada en ASK (Amplitude Shift Keying)", fontsize=8)
        self.ax_rx.set_title("③ RECEPTOR — Señal Recibida (con/sin ruido) y Bits Demodulados", fontsize=8)
        for ax in [self.ax_dig, self.ax_ana, self.ax_rx]:
            ax.set_ylim(-1.2, 1.2)
        self.canvas.draw()

        # 5. Consola de Vida Real
        self.consola = tk.Text(self.main, height=12, bg="#0d0d0d", fg="#33ff33", font=("Consolas", 10), padx=15, pady=10)
        self.consola.pack(fill=tk.X, padx=40, pady=8)

        # 6. Controles
        footer = tk.Frame(root, bg="#1e1e2f", pady=10)
        footer.grid(row=5, column=0, sticky="ew")

        self.entry_msg = tk.Entry(footer, font=("Arial", 14), width=15, justify='center')
        self.entry_msg.pack(side=tk.LEFT, padx=20)
        self.entry_msg.insert(0, "UNEMI")

        self.btn_tx = tk.Button(footer, text="⚡ TRANSMITIR Y ANALIZAR", command=self.transmitir, bg="#00d2ff", width=22, font=("bold", 10))
        self.btn_tx.pack(side=tk.LEFT, padx=5)
        tk.Button(footer, text="🔄 RESET", command=self.reset, bg="#ff4b2b", fg="white", width=10).pack(side=tk.LEFT, padx=5)

        tk.Label(footer, text="Ruido del canal (SNR):", bg="#1e1e2f", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=(20, 2))
        self.var_ruido = tk.IntVar(value=0)
        self.slider_ruido = tk.Scale(footer, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.var_ruido,
                                      bg="#1e1e2f", fg="white", troughcolor="#2a2a40", highlightthickness=0, length=160)
        self.slider_ruido.pack(side=tk.LEFT)
        tk.Label(footer, text="%", bg="#1e1e2f", fg="white").pack(side=tk.LEFT)

    # CÁLCULOS TEÓRICOS (Teorema de Nyquist / Capacidad de canal)
    def _texto_nyquist_estatico(self):

        cumple = FS_EFECTIVA >= 2 * FRECUENCIA_PORTADORA
        capacidad = 2 * FRECUENCIA_PORTADORA * np.log2(NIVELES_ASK)
        estado = "CUMPLE ✔" if cumple else "NO CUMPLE ✘ (habría aliasing)"
        return (f"f_portadora = {FRECUENCIA_PORTADORA} Hz | "
                f"f_muestreo ≈ {FS_EFECTIVA:.2f} Hz | "
                f"Nyquist (fs ≥ 2·f): {estado} | "
                f"Capacidad C = 2·{FRECUENCIA_PORTADORA}·log2({NIVELES_ASK}) = {capacidad:.1f} bps")

    # ANIMACIÓN DEL PANEL DE CODIFICACIÓN ASCII (Carácter -> Decimal -> 8 bits)
    def animar_ascii(self, letra, bits_datos):
        """Actualiza en vivo el panel 'ANIMACIÓN DE CODIFICACIÓN ASCII':
        muestra el carácter, su código decimal y enciende cada casilla de bit
        una por una (verde = 1, gris = 0), imitando el efecto de la imagen de referencia."""
        self.lbl_ascii_char.config(text=letra)
        self.lbl_ascii_dec.config(text=str(ord(letra)))

        # Apaga todas las casillas antes de animar el nuevo carácter
        for b in self.lbls_ascii_bits:
            b.config(bg="#3a3a55", fg="white", text="0")
        self.root.update()
        time.sleep(0.1)

        # Enciende bit por bit, de izquierda a derecha
        for i, bit in enumerate(bits_datos):
            if bit == 1:
                self.lbls_ascii_bits[i].config(bg="#33cc33", fg="white", text="1")
            else:
                self.lbls_ascii_bits[i].config(bg="#3a3a55", fg="white", text="0")
            self.root.update()
            time.sleep(0.08)

    # CAPA DE ENLACE DE DATOS: Paridad real (paridad par)
    def construir_trama(self, letra):

        """Convierte un carácter en una trama: 8 bits de datos + 1 bit de paridad par."""
        bits_datos = [int(b) for b in format(ord(letra), '08b')]
        bit_paridad = sum(bits_datos) % 2  # Paridad PAR: hace que la suma total sea par
        trama = bits_datos + [bit_paridad]
        return trama

    # CAPA FÍSICA: Modulación ASK (Amplitude Shift Keying)
    def modular_ask(self, trama):

        """Genera la onda portadora y la modula en amplitud según los bits de la trama (ASK)."""
        total_muestras = MUESTRAS_POR_BIT * len(trama)  # Siempre exacto, sin residuos
        t = np.linspace(0, len(trama), total_muestras)
        portadora = np.sin(2 * np.pi * FRECUENCIA_PORTADORA * t)
        envolvente = np.repeat(trama, MUESTRAS_POR_BIT)
        señal = portadora * envolvente
        return t, señal

    def aplicar_ruido_canal(self, señal, porcentaje):

        """Ruido VISUAL sobre la onda (efecto gráfico de interferencia en el medio).
        Se mantiene acotado para no destruir por completo la energía de la señal."""
        if porcentaje <= 0:
            return señal.copy()
        sigma = (porcentaje / 100.0) * 0.3
        ruido = np.random.normal(0, sigma, size=señal.shape)
        return señal + ruido

    def aplicar_errores_canal(self, trama_rx, porcentaje, prob_max=0.12):

        """Modelo de Canal Binario Simétrico (BSC): cada bit tiene una probabilidad
        de invertirse proporcional al nivel de ruido configurado (a mayor ruido,
        menor Relación Señal/Ruido y mayor probabilidad de error). Esto es lo que
        realmente demuestra el efecto del ruido sobre la Tasa de Error de Bits (BER),
        de forma gradual y controlable (a diferencia del ruido físico puro, que con
        muchas muestras por bit es extremadamente robusto y no falla "poco a poco")."""
        if porcentaje <= 0:
            return list(trama_rx)
        p = (porcentaje / 100.0) * prob_max
        return [(1 - b) if np.random.random() < p else b for b in trama_rx]

    # RECEPTOR: Demodulación ASK (detección de envolvente + umbral)
    def demodular_ask(self, señal_recibida, num_bits):

        bits_rx = []
        for i in range(num_bits):
            segmento = señal_recibida[i * MUESTRAS_POR_BIT:(i + 1) * MUESTRAS_POR_BIT]
            amplitud_rms = np.sqrt(np.mean(segmento ** 2))  # Detección de envolvente (RMS)
            bits_rx.append(1 if amplitud_rms > UMBRAL_DETECCION else 0)
        return bits_rx

    def verificar_y_decodificar(self, trama_rx):
        
        """Verifica el bit de paridad y reconstruye el carácter recibido."""
        bits_datos_rx = trama_rx[:BITS_DATOS]
        paridad_rx = trama_rx[BITS_DATOS]
        paridad_calculada = sum(bits_datos_rx) % 2
        paridad_ok = (paridad_calculada == paridad_rx)
        valor = int(''.join(map(str, bits_datos_rx)), 2)
        try:
            caracter = chr(valor)
        except ValueError:
            caracter = "?"
        return caracter, paridad_ok

    # UTILIDADES DE INTERFAZ GRÁFICA
    def log(self, tag, msg, color="#33ff33"):
        self.consola.insert(tk.END, f"[{tag}] ", "bold")
        self.consola.insert(tk.END, f"{msg}\n")
        self.consola.see(tk.END)
        self.root.update()

    def resaltar_capa(self, indice, color="#ffcc00"):
        for i, lbl in enumerate(self.layer_labels):
            lbl.config(bg=color if i == indice else "#3a3a55",
                       fg="#1e1e2f" if i == indice else "white")
        self.root.update()

    def apagar_capas(self):
        for lbl in self.layer_labels:
            lbl.config(bg="#3a3a55", fg="white")

    def reset(self):
        
        self.ax_dig.clear()
        self.ax_ana.clear()
        self.ax_rx.clear()
        self.canvas.draw()
        self.consola.delete(1.0, tk.END)
        self.apagar_capas()
        self.lbl_ascii_char.config(text="-")
        self.lbl_ascii_dec.config(text="-")
        for b in self.lbls_ascii_bits:
            b.config(bg="#3a3a55", fg="white", text="0")
        self.lbl_transmision.config(text="📡 Esperando transmisión...")
        self.btn_tx.config(state=tk.NORMAL)
        self.bits_totales = 0
        self.bits_con_error = 0
        self.mensaje_recibido = ""

    # PROCESO PRINCIPAL DE TRANSMISIÓN
    def transmitir(self):
        
        texto = self.entry_msg.get().upper()
        if not texto:
            messagebox.showwarning(
                "Campo vacío",
                 "Por favor, ingrese un mensaje antes de iniciar la transmisión."
            )
            self.entry_msg.focus_set()  # Regresa el cursor al cuadro de texto
            return
        self.btn_tx.config(state=tk.DISABLED)
        self.consola.delete(1.0, tk.END)
        self.bits_totales = 0
        self.bits_con_error = 0
        self.mensaje_recibido = ""
        nivel_ruido = self.var_ruido.get()

        self.consola.insert(tk.END, "=" * 125 + "\n")
        self.log("SISTEMA", self._texto_nyquist_estatico())
        if nivel_ruido > 0:
            p_bit = (nivel_ruido / 100.0) * 0.12
            self.log("CANAL", f"Ruido activo: {nivel_ruido}% -> Modelo de Canal Binario Simétrico "
                               f"(BSC): cada bit tiene ~{p_bit*100:.1f}% de prob. de invertirse")
        self.consola.insert(tk.END, "=" * 125 + "\n")

        for i, letra in enumerate(texto):
            # Indicador en vivo arriba de la gráfica: qué carácter se transporta ahora
            self.lbl_transmision.config(
                text=f"📡 Transmitiendo carácter {i+1}/{len(texto)}: '{letra}'  (ASCII {ord(letra)})"
            )
            self.root.update_idletasks()

            # CAPA 7: APLICACIÓN 
            self.resaltar_capa(0)
            self.log("OSI-1 APP", f"Usuario ingresa el carácter '{letra}' en el Entry")
            time.sleep(0.25)

            # CAPA 6: PRESENTACIÓN (codificación ASCII) 
            self.resaltar_capa(1)
            bits_datos = [int(b) for b in format(ord(letra), '08b')]
            self.animar_ascii(letra, bits_datos)
            self.log("OSI-2 PRES", f"Codificación ASCII: '{letra}' = {ord(letra)} = {''.join(map(str, bits_datos))}")
            time.sleep(0.25)

            # CAPA 3: SESIÓN 
            self.resaltar_capa(2)
            self.log("OSI-3 SESION", "Diálogo de transmisión establecido con el receptor")
            time.sleep(0.2)

            # CAPA 4: TRANSPORTE 
            self.resaltar_capa(3)
            self.log("OSI-4 TRANS", f"Segmento de 8 bits preparado para envío fiable")
            time.sleep(0.2)

            # CAPA 5: RED 
            self.resaltar_capa(4)
            self.log("OSI-5 RED", "Trama direccionada hacia el medio de transmisión")
            time.sleep(0.2)

            # CAPA 6: ENLACE DE DATOS (trama + paridad real)
            self.resaltar_capa(5)
            trama = self.construir_trama(letra)
            self.log("OSI-6 ENLACE", f"Trama armada (datos+paridad): {''.join(map(str, trama))} "
                                      f"(bit de paridad par = {trama[-1]})")
            time.sleep(0.25)

            # CAPA 7: FÍSICA (modulación ASK) 
            self.resaltar_capa(6)
            t, señal_tx = self.modular_ask(trama)
            self.log("OSI-7 FÍSICA", f"Modulación ASK con portadora de {FRECUENCIA_PORTADORA} Hz")

            # Gráfico 1: bits digitales (Tx)
            self.ax_dig.clear()
            self.ax_dig.step(range(len(trama)), trama, where='post', color='#00d2ff', lw=2)
            self.ax_dig.set_title(f"① TX DIGITAL: '{letra}' -> trama {''.join(map(str, trama))} (8 datos + 1 paridad)", fontsize=8)
            self.ax_dig.set_ylim(-0.2, 1.2)

            # Gráfico 2: señal analógica transmitida (canal)
            self.ax_ana.clear()
            self.ax_ana.plot(t, señal_tx, color='#ff4b2b', lw=1)
            self.ax_ana.set_title("② CANAL: Onda ASK transmitida (medio físico)", fontsize=8)

            self.canvas.draw()
            self.root.update_idletasks()
            time.sleep(0.6)

            # CANAL: posible ruido 
            señal_rx = self.aplicar_ruido_canal(señal_tx, nivel_ruido)

            # RECEPTOR: demodulación 
            trama_rx = self.demodular_ask(señal_rx, len(trama))
            # Modelo de Canal Binario Simétrico: errores de bit graduales según el ruido
            trama_rx = self.aplicar_errores_canal(trama_rx, nivel_ruido)
            caracter_rx, paridad_ok = self.verificar_y_decodificar(trama_rx)

            # Conteo de BER
            errores_bit = sum(1 for a, b in zip(trama, trama_rx) if a != b)
            self.bits_totales += len(trama)
            self.bits_con_error += errores_bit

            # Gráfico 3: señal recibida + bits reconstruidos
            self.ax_rx.clear()
            self.ax_rx.plot(t, señal_rx, color='#a0a0ff', lw=1, alpha=0.6, label="Señal recibida")
            self.ax_rx.step(np.linspace(0, len(trama_rx), len(trama_rx)), trama_rx,
                             where='post', color='#33ff33', lw=2, label="Bits demodulados")
            color_titulo = "#33ff33" if paridad_ok and caracter_rx == letra else "#ff4b2b"
            self.ax_rx.set_title(f"③ RX: demodulado='{caracter_rx}' | paridad {'OK' if paridad_ok else 'ERROR'}", fontsize=8)
            self.canvas.draw()
            self.root.update_idletasks()

            self.mensaje_recibido += caracter_rx
            if paridad_ok and caracter_rx == letra:
                self.log("RECEPTOR", f"Carácter recibido: '{caracter_rx}' -> coincide con el original. Paridad OK ✔")
            else:
                self.log("RECEPTOR", f"Carácter recibido: '{caracter_rx}' (esperado '{letra}') -> "
                                      f"{'paridad ERROR' if not paridad_ok else 'no coincide'} ✘", color="#ff4b2b")

            # DETALLE DE VIDA REAL
            detalle = self.detalles_reales[i % len(self.detalles_reales)]
            self.log("ESCENARIO", detalle['ejemplo'])
            self.log("APLICACIÓN", detalle['explicacion'])
            self.log("TEORÍA U3", detalle['teoria'])
            self.consola.insert(tk.END, "=" * 125 + "\n")

            self.apagar_capas()
            time.sleep(1.0)

        # RESUMEN FINAL 
        self.lbl_transmision.config(text=f"✅ Transmisión completa: '{texto}' -> recibido: '{self.mensaje_recibido}'")
        ber = (self.bits_con_error / self.bits_totales * 100) if self.bits_totales else 0
        self.log("SISTEMA", f"Mensaje original : '{texto}'")
        color_resumen = "#33ff33" if self.mensaje_recibido == texto else "#ff4b2b"
        self.log("SISTEMA", f"Mensaje recibido : '{self.mensaje_recibido}'", color=color_resumen)
        self.log("SISTEMA", f"Bits transmitidos: {self.bits_totales} | Bits con error: {self.bits_con_error} | BER: {ber:.2f}%")
        if self.mensaje_recibido == texto:
            self.log("SISTEMA", "Verificación de paridad e integridad: ÉXITO TOTAL ✔")
        else:
            self.log("SISTEMA", "Se detectaron errores de transmisión (ver bits/paridad arriba). Aumente la SNR (reduzca el ruido).", color="#ff4b2b")
        self.consola.insert(tk.END, "=" * 125 + "\n")
        self.btn_tx.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorContextoRealUNEMI(root)
    root.mainloop()