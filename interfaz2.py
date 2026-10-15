import tkinter as tk
from tkinter import messagebox
from afn import AFN
from conversion import ConvertidorAFN_AFD
from minimizacion import MinimizadorAFD
from simulador import SimuladorAFN
from simulador_afd import SimuladorAFD
import math


class InterfazAutomatas:

    def __init__(self, ventana):

        self.ventana = ventana
        self.ventana.title("Sistema de Autómatas Finitos")
        self.ventana.state("zoomed")
        self.ventana.resizable(True, True)

        # Configuración de Fondo General (Azul Frío Pastel)
        self.COLOR_FONDO = "#F0F4F8"
        self.COLOR_PANEL = "#FFFFFF"
        self.COLOR_TEXTO = "#2C3E50"
        self.COLOR_BTN_PRIMARIO = "#7091E6"
        self.COLOR_BTN_SECUNDARIO = "#86A7FC"
        self.COLOR_BTN_ACCION = "#A3B7D8"
        self.COLOR_BTN_SALIR = "#E57373"

        self.ventana.configure(bg=self.COLOR_FONDO)

        # ==================================
        # VARIABLES
        # ==================================

        self.afn = None
        self.afd = None
        self.afd_minimo = None

        # ==================================
        # TÍTULO
        # ==================================

        titulo = tk.Label(
            self.ventana,
            text="SISTEMA DE AUTÓMATAS FINITOS",
            font=("Arial", 20, "bold"),
            bg=self.COLOR_FONDO,
            fg=self.COLOR_TEXTO
        )
        titulo.pack(pady=15)

        subtitulo = tk.Label(
            self.ventana,
            text="Construcción, conversión, minimización y simulación",
            font=("Arial", 11),
            bg=self.COLOR_FONDO,
            fg="#64748B"
        )
        subtitulo.pack()

        # ==================================
        # CONTENEDOR PRINCIPAL
        # ==================================

        contenedor = tk.Frame(self.ventana, bg=self.COLOR_FONDO)
        contenedor.pack(pady=20, padx=20)

        # Estilos comunes de LabelFrame
        estilo_frame = {
            "bg": self.COLOR_PANEL,
            "fg": self.COLOR_TEXTO,
            "font": ("Arial", 11, "bold"),
            "padx": 15,
            "pady": 15,
            "bd": 1,
            "relief": "solid"
        }

        # Estilos comunes para botones
        self.estilo_btn = {
            "font": ("Arial", 9, "bold"),
            "fg": "white",
            "bd": 0,
            "cursor": "hand2",
            "activeforeground": "white"
        }

        # ==================================
        # PANEL IZQUIERDO
        # ==================================

        panel_izquierdo = tk.LabelFrame(contenedor, text="Configuración del AFN", **estilo_frame)
        panel_izquierdo.grid(row=0, column=0, padx=10, sticky="n")

        # ESTADOS
        tk.Label(panel_izquierdo, text="Estados:", bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO).grid(row=0, column=0, sticky="w", pady=5)
        self.txt_estados = tk.Entry(panel_izquierdo, width=35, bg="#F8FAFC", relief="groove")
        self.txt_estados.grid(row=0, column=1, pady=5)

        # ALFABETO
        tk.Label(panel_izquierdo, text="Alfabeto:", bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO).grid(row=1, column=0, sticky="w", pady=5)
        self.txt_alfabeto = tk.Entry(panel_izquierdo, width=35, bg="#F8FAFC", relief="groove")
        self.txt_alfabeto.grid(row=1, column=1, pady=5)

        # ESTADO INICIAL
        tk.Label(panel_izquierdo, text="Estado inicial:", bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO).grid(row=2, column=0, sticky="w", pady=5)
        self.txt_inicial = tk.Entry(panel_izquierdo, width=35, bg="#F8FAFC", relief="groove")
        self.txt_inicial.grid(row=2, column=1, pady=5)

        # ESTADOS FINALES
        tk.Label(panel_izquierdo, text="Estados finales:", bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO).grid(row=3, column=0, sticky="w", pady=5)
        self.txt_finales = tk.Entry(panel_izquierdo, width=35, bg="#F8FAFC", relief="groove")
        self.txt_finales.grid(row=3, column=1, pady=5)

        # CREAR AFN
        boton_crear = tk.Button(
            panel_izquierdo,
            text="Crear AFN",
            width=25,
            command=self.crear_afn,
            bg=self.COLOR_BTN_PRIMARIO,
            activebackground="#5A7AD2",
            **self.estilo_btn
        )
        boton_crear.grid(row=4, column=0, columnspan=2, pady=15)

        # ==================================
        # PANEL DE TRANSICIONES
        # ==================================

        panel_transiciones = tk.LabelFrame(contenedor, text="Agregar transición", **estilo_frame)
        panel_transiciones.grid(row=1, column=0, padx=10, pady=15, sticky="n")

        # ORIGEN
        tk.Label(panel_transiciones, text="Origen:", bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO).grid(row=0, column=0, pady=5)
        self.txt_origen = tk.Entry(panel_transiciones, width=12, bg="#F8FAFC", relief="groove")
        self.txt_origen.grid(row=0, column=1, pady=5)

        # SÍMBOLO
        tk.Label(panel_transiciones, text="Símbolo:", bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO).grid(row=1, column=0, pady=5)
        self.txt_simbolo = tk.Entry(panel_transiciones, width=12, bg="#F8FAFC", relief="groove")
        self.txt_simbolo.grid(row=1, column=1, pady=5)

        # DESTINO
        tk.Label(panel_transiciones, text="Destino:", bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO).grid(row=2, column=0, pady=5)
        self.txt_destino = tk.Entry(panel_transiciones, width=12, bg="#F8FAFC", relief="groove")
        self.txt_destino.grid(row=2, column=1, pady=5)

        # AGREGAR TRANSICIÓN
        boton_agregar = tk.Button(
            panel_transiciones,
            text="Agregar transición",
            width=20,
            command=self.agregar_transicion,
            bg=self.COLOR_BTN_SECUNDARIO,
            activebackground="#6F92E5",
            **self.estilo_btn
        )
        boton_agregar.grid(row=3, column=0, columnspan=2, pady=10)

        # ==================================
        # PANEL CENTRAL
        # ==================================

        panel_operaciones = tk.LabelFrame(contenedor, text="Operaciones", **estilo_frame)
        panel_operaciones.grid(row=0, column=1, rowspan=2, padx=10, sticky="n")

        def crear_btn_op(texto, comando, color=self.COLOR_BTN_SECUNDARIO):
            return tk.Button(
                panel_operaciones,
                text=texto,
                width=25,
                command=comando,
                bg=color,
                activebackground="#6F92E5",
                **self.estilo_btn
            )

        crear_btn_op("Mostrar AFN", self.mostrar_afn).pack(pady=4)
        crear_btn_op("Convertir AFN → AFD", self.convertir_afd).pack(pady=4)
        crear_btn_op("Minimizar AFD", self.minimizar_afd).pack(pady=4)

        tk.Label(panel_operaciones, text="GRÁFICOS", font=("Arial", 10, "bold"), bg=self.COLOR_PANEL, fg="#475569").pack(pady=10)

        crear_btn_op("Dibujar AFN", self.dibujar_afn, "#93C5FD").pack(pady=4)
        crear_btn_op("Dibujar AFD", self.dibujar_afd, "#93C5FD").pack(pady=4)
        crear_btn_op("Dibujar AFD mínimo", self.dibujar_afd_minimo, "#93C5FD").pack(pady=4)

        tk.Label(panel_operaciones, text="SIMULACIÓN", font=("Arial", 10, "bold"), bg=self.COLOR_PANEL, fg="#475569").pack(pady=10)

        tk.Label(panel_operaciones, text="Cadena a evaluar:", bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO).pack()
        self.txt_cadena = tk.Entry(panel_operaciones, width=27, bg="#F8FAFC", relief="groove")
        self.txt_cadena.pack(pady=5)

        crear_btn_op("Simular AFN", self.simular_afn, "#A5B4FC").pack(pady=4)
        crear_btn_op("Simular AFD", self.simular_afd, "#A5B4FC").pack(pady=4)
        crear_btn_op("Simular AFD mínimo", self.simular_afd_minimo, "#A5B4FC").pack(pady=4)

        # ==================================
        # PANEL DERECHO - RESULTADOS
        # ==================================

        panel_resultado = tk.LabelFrame(contenedor, text="Resultados", **estilo_frame)
        panel_resultado.grid(row=0, column=2, rowspan=2, padx=10, sticky="n")

        self.area_resultado = tk.Text(
            panel_resultado,
            width=48,
            height=30,
            font=("Consolas", 9),
            bg="#F8FAFC",
            fg="#1E293B",
            relief="groove",
            bd=1
        )
        self.area_resultado.pack()

        # ==================================
        # BOTONES INFERIORES
        # ==================================

        panel_inferior = tk.Frame(self.ventana, bg=self.COLOR_FONDO)
        panel_inferior.pack(pady=10)

        tk.Button(
            panel_inferior,
            text="Limpiar",
            width=18,
            command=self.limpiar,
            bg=self.COLOR_BTN_ACCION,
            activebackground="#8B9FC1",
            **self.estilo_btn
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            panel_inferior,
            text="Salir",
            width=18,
            command=self.ventana.destroy,
            bg=self.COLOR_BTN_SALIR,
            activebackground="#D32F2F",
            **self.estilo_btn
        ).grid(row=0, column=1, padx=5)

    # ==========================================
    # LÓGICA DE DIBUJO DEL AUTÓMATA CON COLORES
    # ==========================================

    def dibujar_automata(self, automata):

        if automata is None or not automata.estados:
            messagebox.showwarning("Advertencia", "No hay autómata o estados para dibujar.")
            return

        ventana_grafico = tk.Toplevel(self.ventana)
        ventana_grafico.title("Diagrama del autómata")
        ventana_grafico.state("zoomed")
        ventana_grafico.configure(bg=self.COLOR_FONDO)

        titulo = tk.Label(
            ventana_grafico,
            text="REPRESENTACIÓN GRÁFICA DEL AUTÓMATA",
            font=("Arial", 18, "bold"),
            bg=self.COLOR_FONDO,
            fg=self.COLOR_TEXTO
        )
        titulo.pack(pady=10)

        marco = tk.Frame(ventana_grafico, bg=self.COLOR_FONDO)
        marco.pack(fill="both", expand=True, padx=15, pady=10)

        # Canvas con color pastel frío claro
        canvas = tk.Canvas(marco, bg="#F7FAFC", highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        barra_horizontal = tk.Scrollbar(marco, orient="horizontal", command=canvas.xview)
        barra_horizontal.grid(row=1, column=0, sticky="ew")

        barra_vertical = tk.Scrollbar(marco, orient="vertical", command=canvas.yview)
        barra_vertical.grid(row=0, column=1, sticky="ns")

        canvas.configure(xscrollcommand=barra_horizontal.set, yscrollcommand=barra_vertical.set)
        marco.grid_rowconfigure(0, weight=1)
        marco.grid_columnconfigure(0, weight=1)

        estados = sorted(
            list(automata.estados),
            key=lambda estado: (
                0 if estado == automata.estado_inicial else 1,
                self.orden_estado(self.nombre_estado(estado))
            )
        )

        radio = 38
        separacion_x = 230
        separacion_y = 170
        margen_x = 160
        margen_y = 130

        columnas = min(5, max(1, len(estados)))
        filas = math.ceil(len(estados) / columnas)

        posiciones = {}
        for indice, estado in enumerate(estados):
            fila = indice // columnas
            columna = indice % columnas
            x = margen_x + columna * separacion_x
            y = margen_y + fila * separacion_y
            posiciones[estado] = (x, y)

        ancho = margen_x * 2 + (columnas - 1) * separacion_x + 200
        alto = margen_y * 2 + (filas - 1) * separacion_y + 180
        canvas.config(scrollregion=(0, 0, ancho, alto))

        transiciones = {}
        for origen, simbolos in automata.transiciones.items():
            for simbolo, destinos in simbolos.items():
                destinos_lista = destinos if isinstance(destinos, (list, set, tuple, frozenset)) else [destinos]
                for destino in destinos_lista:
                    clave = (origen, destino)
                    if clave not in transiciones:
                        transiciones[clave] = []
                    transiciones[clave].append(str(simbolo))

        # DIBUJAR TRANSICIONES Y FLECHAS
        COLOR_FLECHA = "#475569"

        for (origen, destino), simbolos in transiciones.items():
            if origen not in posiciones or destino not in posiciones:
                continue

            x1, y1 = posiciones[origen]
            x2, y2 = posiciones[destino]
            etiqueta = ", ".join(sorted(simbolos))

            if origen == destino:
                canvas.create_line(
                    x1 - 25, y1 - 20,
                    x1, y1 - 55,
                    x1 + 25, y1 - 20,
                    smooth=True,
                    arrow=tk.LAST,
                    fill=COLOR_FLECHA,
                    width=2
                )
                canvas.create_text(x1, y1 - 65, text=etiqueta, font=("Arial", 11, "bold"), fill="#1E293B")
                continue

            dx = x2 - x1
            dy = y2 - y1
            distancia = math.sqrt(dx ** 2 + dy ** 2)
            if distancia == 0:
                continue

            inicio_x = x1 + dx / distancia * radio
            inicio_y = y1 + dy / distancia * radio
            final_x = x2 - dx / distancia * radio
            final_y = y2 - dy / distancia * radio

            existe_inversa = (destino, origen) in transiciones

            if existe_inversa:
                perpendicular_x = -dy / distancia
                perpendicular_y = dx / distancia
                curvatura = 45

                control_x = (inicio_x + final_x) / 2 + perpendicular_x * curvatura
                control_y = (inicio_y + final_y) / 2 + perpendicular_y * curvatura

                canvas.create_line(
                    inicio_x, inicio_y,
                    control_x, control_y,
                    final_x, final_y,
                    smooth=True, arrow=tk.LAST, width=2, fill=COLOR_FLECHA
                )
                texto_x = control_x + perpendicular_x * 10
                texto_y = control_y + perpendicular_y * 10
            else:
                canvas.create_line(
                    inicio_x, inicio_y, final_x, final_y,
                    arrow=tk.LAST, width=2, fill=COLOR_FLECHA
                )
                texto_x = (inicio_x + final_x) / 2
                texto_y = (inicio_y + final_y) / 2 - 15

            canvas.create_text(texto_x, texto_y, text=etiqueta, font=("Arial", 11, "bold"), fill="#1E293B")

        # DIBUJAR NODOS / ESTADOS
        for estado in estados:
            x, y = posiciones[estado]

            # Colores Pastel Fríos para los estados
            if estado == automata.estado_inicial:
                color_estado = "#BAE6FD"  # Azul Hielo
                color_borde = "#0284C7"
            elif estado in automata.estados_finales:
                color_estado = "#A7F3D0"  # Menta Pastel
                color_borde = "#059669"
            else:
                color_estado = "#E2E8F0"  # Gris Frío Pastel
                color_borde = "#64748B"

            canvas.create_oval(
                x - radio, y - radio, x + radio, y + radio,
                width=2, fill=color_estado, outline=color_borde
            )

            if estado in automata.estados_finales:
                canvas.create_oval(
                    x - radio + 6, y - radio + 6, x + radio - 6, y + radio - 6,
                    width=2, fill=color_estado, outline=color_borde
                )

            canvas.create_text(x, y, text=self.nombre_estado(estado), font=("Arial", 12, "bold"), fill="#0F172A")

        if automata.estado_inicial in posiciones:
            x, y = posiciones[automata.estado_inicial]
            canvas.create_line(x - 100, y, x - radio, y, arrow=tk.LAST, width=2, fill=COLOR_FLECHA)

        # LEYENDA EN LENGUAJE GRÁFICO
        canvas.create_oval(100, alto - 60, 130, alto - 30, fill="#BAE6FD", outline="#0284C7", width=2)
        canvas.create_text(160, alto - 45, text="Estado inicial", font=("Arial", 10), fill="#334155")

        canvas.create_oval(280, alto - 60, 310, alto - 30, fill="#A7F3D0", outline="#059669", width=2)
        canvas.create_text(340, alto - 45, text="Estado final", font=("Arial", 10), fill="#334155")

        tk.Button(
            ventana_grafico,
            text="Cerrar",
            width=18,
            command=ventana_grafico.destroy,
            bg=self.COLOR_BTN_ACCION,
            activebackground="#8B9FC1",
            **self.estilo_btn
        ).pack(pady=10)

    # Resto de métodos del sistema (sin modificaciones lógicas)
    def crear_afn(self):
        estados = self.txt_estados.get().split(",")
        alfabeto = self.txt_alfabeto.get().split(",")
        inicial = self.txt_inicial.get().strip()
        finales = self.txt_finales.get().split(",")

        estados = {estado.strip() for estado in estados if estado.strip()}
        alfabeto = {simbolo.strip() for simbolo in alfabeto if simbolo.strip()}
        finales = {estado.strip() for estado in finales if estado.strip()}

        if not estados or not alfabeto or inicial not in estados:
            messagebox.showwarning("Advertencia", "Verifique los datos del AFN.")
            return

        for estado in finales:
            if estado not in estados:
                messagebox.showwarning("Advertencia", f"El estado final {estado} no existe.")
                return

        self.afn = AFN()
        for estado in estados:
            self.afn.agregar_estado(estado)
        for simbolo in alfabeto:
            self.afn.agregar_simbolo(simbolo)
        self.afn.establecer_inicial(inicial)
        for estado in finales:
            self.afn.agregar_final(estado)

        self.afd = None
        self.afd_minimo = None
        self.mostrar_afn()
        messagebox.showinfo("AFN", "AFN creado correctamente.")

    def agregar_transicion(self):
        if self.afn is None:
            messagebox.showwarning("Advertencia", "Primero debe crear el AFN.")
            return

        origen = self.txt_origen.get().strip()
        simbolo = self.txt_simbolo.get().strip()
        destino = self.txt_destino.get().strip()

        if not origen or not simbolo or not destino:
            messagebox.showwarning("Advertencia", "Complete todos los campos.")
            return

        if origen not in self.afn.estados or destino not in self.afn.estados:
            messagebox.showwarning("Advertencia", "Estado de origen o destino no existe.")
            return

        if simbolo not in self.afn.alfabeto and simbolo != "ε":
            messagebox.showwarning("Advertencia", f"El símbolo {simbolo} no pertenece al alfabeto.")
            return

        self.afn.agregar_transicion(origen, simbolo, destino)
        self.afd = None
        self.afd_minimo = None

        self.txt_origen.delete(0, tk.END)
        self.txt_simbolo.delete(0, tk.END)
        self.txt_destino.delete(0, tk.END)
        self.mostrar_afn()

    def mostrar_afn(self):
        if self.afn is None:
            return
        self.area_resultado.delete("1.0", tk.END)
        self.area_resultado.insert(tk.END, "========== AFN ==========\n\n")
        self.area_resultado.insert(tk.END, f"Estados:\n{self.afn.estados}\n\n")
        self.area_resultado.insert(tk.END, f"Alfabeto:\n{self.afn.alfabeto}\n\n")
        self.area_resultado.insert(tk.END, f"Estado inicial:\n{self.afn.estado_inicial}\n\n")
        self.area_resultado.insert(tk.END, f"Estados finales:\n{self.afn.estados_finales}\n\n")
        self.area_resultado.insert(tk.END, "Transiciones:\n")
        for origen, simbolos in self.afn.transiciones.items():
            for simbolo, destinos in simbolos.items():
                for destino in destinos:
                    self.area_resultado.insert(tk.END, f"{origen} --{simbolo}--> {destino}\n")
        self.area_resultado.insert(tk.END, "\n==========================")

    def convertir_afd(self):
        if self.afn is None:
            messagebox.showwarning("Advertencia", "Primero debe crear un AFN.")
            return
        try:
            convertidor = ConvertidorAFN_AFD(self.afn)
            self.afd = convertidor.convertir()
            self.mostrar_afd()
            messagebox.showinfo("Conversión", "AFN convertido a AFD correctamente.")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def mostrar_afd(self):
        if self.afd is None:
            return
        self.area_resultado.delete("1.0", tk.END)
        self.area_resultado.insert(tk.END, "========== AFD ==========\n\n")
        estados_formateados = [self.nombre_estado(estado) for estado in self.afd.estados]
        self.area_resultado.insert(tk.END, "Estados:\n" + ", ".join(estados_formateados) + "\n\n")
        self.area_resultado.insert(tk.END, f"Alfabeto:\n{self.afd.alfabeto}\n\n")
        self.area_resultado.insert(tk.END, "Estado inicial:\n" + self.nombre_estado(self.afd.estado_inicial) + "\n\n")
        finales_formateados = [self.nombre_estado(estado) for estado in self.afd.estados_finales]
        self.area_resultado.insert(tk.END, "Estados finales:\n" + ", ".join(finales_formateados) + "\n\n")
        self.area_resultado.insert(tk.END, "Transiciones:\n")
        for origen, simbolos in self.afd.transiciones.items():
            for simbolo, destinos in simbolos.items():
                for destino in destinos:
                    self.area_resultado.insert(tk.END, f"{origen} --{simbolo}--> {destino}\n")

    def minimizar_afd(self):
        if self.afd is None:
            messagebox.showwarning("Advertencia", "Primero debe convertir el AFN a AFD.")
            return
        try:
            minimizador = MinimizadorAFD(self.afd)
            self.afd_minimo = minimizador.minimizar()
            self.mostrar_afd_minimo()
            messagebox.showinfo("Minimización", "AFD minimizado correctamente.")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def mostrar_afd_minimo(self):
        if self.afd_minimo is None:
            return
        self.area_resultado.delete("1.0", tk.END)
        self.area_resultado.insert(tk.END, "======= AFD MINIMIZADO =======\n\n")
        estados_formateados = [self.nombre_estado(estado) for estado in self.afd_minimo.estados]
        self.area_resultado.insert(tk.END, "Estados:\n" + ", ".join(estados_formateados) + "\n\n")
        self.area_resultado.insert(tk.END, f"Alfabeto:\n{self.afd_minimo.alfabeto}\n\n")
        self.area_resultado.insert(tk.END, f"Estado inicial:\n{self.afd_minimo.estado_inicial}\n\n")
        self.area_resultado.insert(tk.END, f"Estados finales:\n{self.afd_minimo.estados_finales}\n\n")
        self.area_resultado.insert(tk.END, "Transiciones:\n")
        for origen, simbolos in self.afd_minimo.transiciones.items():
            for simbolo, destinos in simbolos.items():
                for destino in destinos:
                    self.area_resultado.insert(tk.END, f"{origen} --{simbolo}--> {destino}\n")

    def simular_afn(self):
        if self.afn is None:
            messagebox.showwarning("Advertencia", "Primero debe crear un AFN.")
            return
        cadena = self.txt_cadena.get()
        simulador = SimuladorAFN(self.afn)
        resultado = simulador.simular(cadena)
        self.area_resultado.insert(tk.END, "\n\n========== SIMULACIÓN AFN ==========\n")
        self.area_resultado.insert(tk.END, f"Cadena: {cadena}\n")
        self.area_resultado.insert(tk.END, f"RESULTADO: {'ACEPTADA' if resultado else 'RECHAZADA'}\n")

    def simular_afd(self):
        if self.afd is None:
            messagebox.showwarning("Advertencia", "Primero debe convertir el AFN a AFD.")
            return
        cadena = self.txt_cadena.get()
        simulador = SimuladorAFD(self.afd)
        resultado = simulador.simular(cadena)
        self.area_resultado.insert(tk.END, "\n\n========== SIMULACIÓN AFD ==========\n")
        self.area_resultado.insert(tk.END, f"Cadena: {cadena}\n")
        self.area_resultado.insert(tk.END, f"RESULTADO: {'ACEPTADA' if resultado else 'RECHAZADA'}\n")

    def simular_afd_minimo(self):
        if self.afd_minimo is None:
            messagebox.showwarning("Advertencia", "Primero debe minimizar el AFD.")
            return
        cadena = self.txt_cadena.get()
        simulador = SimuladorAFD(self.afd_minimo)
        resultado = simulador.simular(cadena)
        self.area_resultado.insert(tk.END, "\n\n===== SIMULACIÓN AFD MÍNIMO =====\n")
        self.area_resultado.insert(tk.END, f"Cadena: {cadena}\n")
        self.area_resultado.insert(tk.END, f"RESULTADO: {'ACEPTADA' if resultado else 'RECHAZADA'}\n")

    def nombre_estado(self, estado):
        if isinstance(estado, frozenset):
            if not estado:
                return "∅"
            elementos = sorted([str(elemento) for elemento in estado], key=self.orden_estado)
            if len(elementos) == 1:
                return elementos[0]
            return "{" + ", ".join(elementos) + "}"
        return str(estado)

    def orden_estado(self, estado):
        texto = str(estado)
        numero = "".join(caracter for caracter in texto if caracter.isdigit())
        return (texto.rstrip("0123456789"), int(numero)) if numero else (texto, 0)

    def dibujar_afn(self):
        if self.afn is None:
            messagebox.showwarning("Advertencia", "Primero debe crear el AFN.")
            return
        self.dibujar_automata(self.afn)

    def dibujar_afd(self):
        if self.afd is None:
            messagebox.showwarning("Advertencia", "Primero debe convertir el AFN a AFD.")
            return
        self.dibujar_automata(self.afd)

    def dibujar_afd_minimo(self):
        if self.afd_minimo is None:
            messagebox.showwarning("Advertencia", "Primero debe minimizar el AFD.")
            return
        if not self.afd_minimo.estados:
            self.afd_minimo.agregar_estado("q_trap")
            self.afd_minimo.establecer_inicial("q_trap")
            for simbolo in self.afd_minimo.alfabeto:
                self.afd_minimo.agregar_transicion("q_trap", simbolo, "q_trap")

        self.dibujar_automata(self.afd_minimo)

    def limpiar(self):
        self.txt_estados.delete(0, tk.END)
        self.txt_alfabeto.delete(0, tk.END)
        self.txt_inicial.delete(0, tk.END)
        self.txt_finales.delete(0, tk.END)
        self.txt_origen.delete(0, tk.END)
        self.txt_simbolo.delete(0, tk.END)
        self.txt_destino.delete(0, tk.END)
        self.txt_cadena.delete(0, tk.END)
        self.area_resultado.delete("1.0", tk.END)
        self.afn = None
        self.afd = None
        self.afd_minimo = None


if __name__ == "__main__":
    ventana = tk.Tk()
    aplicacion = InterfazAutomatas(ventana)
    ventana.mainloop()
