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

        # ==================================
        # PALETA DE COLORES VIVAS Y MODERNAS
        # ==================================
        self.COLOR_FONDO = "#0F172A"        # Slate 900 (Fondo principal)
        self.COLOR_PANEL = "#1E293B"        # Slate 800 (Fondo de tarjetas)
        self.COLOR_BORDE = "#334155"        # Slate 700 (Bordes)
        self.COLOR_BORDE_ACTIVE = "#3B82F6" # Blue 500 (Bordes destacados)
        
        # Textos
        self.COLOR_TEXTO_PRI = "#F8FAFC"    # Blanco brillante
        self.COLOR_TEXTO_SEC = "#94A3B8"    # Gris claro
        self.COLOR_TEXTO_MUTED = "#38BDF8"  # Cyan 400 (Categorías)

        # Botones Vívidos
        self.COLOR_BTN_PRIMARY = "#4F46E5"   # Indigo vívido
        self.COLOR_BTN_PRIMARY_HOVER = "#4338CA"
        self.COLOR_BTN_SUCCESS = "#10B981"   # Esmeralda vívido
        self.COLOR_BTN_ACTION = "#8B5CF6"    # Púrpura vívido
        self.COLOR_BTN_INFO = "#0284C7"      # Cyan vívido
        self.COLOR_BTN_NEUTRAL = "#334155"   # Slate 700
        self.COLOR_BTN_DANGER = "#EF4444"    # Rojo vívido

        self.ventana.configure(bg=self.COLOR_FONDO)

        # FUENTES AMPLIADAS Y ENFÁTICAS
        self.FONT_TITLE = ("Segoe UI", 22, "bold")
        self.FONT_SUBTITLE = ("Segoe UI", 11)
        self.FONT_HEADER = ("Segoe UI", 13, "bold")
        self.FONT_BODY = ("Segoe UI", 11)
        self.FONT_BOLD = ("Segoe UI", 11, "bold")
        self.FONT_MONO = ("Consolas", 11)

        # ==================================
        # VARIABLES
        # ==================================
        self.afn = None
        self.afd = None
        self.afd_minimo = None

        # ==================================
        # CABECERA PRINCIPAL
        # ==================================
        header_frame = tk.Frame(self.ventana, bg=self.COLOR_FONDO)
        header_frame.pack(fill="x", padx=30, pady=(20, 10))

        titulo = tk.Label(
            header_frame,
            text="SISTEMA DE AUTÓMATAS FINITOS",
            font=self.FONT_TITLE,
            bg=self.COLOR_FONDO,
            fg="#38BDF8"
        )
        titulo.pack(anchor="w")

        subtitulo = tk.Label(
            header_frame,
            text="Análisis, conversión, minimización y simulación de autómatas",
            font=self.FONT_SUBTITLE,
            bg=self.COLOR_FONDO,
            fg=self.COLOR_TEXTO_SEC
        )
        subtitulo.pack(anchor="w", pady=(2, 0))

       
        contenedor = tk.Frame(self.ventana, bg=self.COLOR_FONDO)
        contenedor.pack(fill="both", expand=True, padx=25, pady=10)

        # Configuración proporcional de columnas expandibles
        contenedor.columnconfigure(0, weight=3)
        contenedor.columnconfigure(1, weight=3)
        contenedor.columnconfigure(2, weight=4)
        contenedor.rowconfigure(0, weight=1)

        # Estilos visuales para paneles amplios
        estilo_frame = {
            "bg": self.COLOR_PANEL,
            "fg": "#38BDF8",
            "font": self.FONT_HEADER,
            "padx": 20,
            "pady": 20,
            "bd": 2,
            "relief": "solid",
            "highlightthickness": 0
        }

        # Estilo de campos de texto amplios
        self.estilo_entry = {
            "bg": "#0F172A",
            "fg": "#FFFFFF",
            "insertbackground": "#FFFFFF",
            "relief": "flat",
            "highlightbackground": self.COLOR_BORDE_ACTIVE,
            "highlightthickness": 1.5,
            "font": ("Segoe UI", 12)
        }

        # ==================================
        # COLUMNA 1: CONFIGURACIÓN Y TRANSICIONES
        # ==================================
        col1 = tk.Frame(contenedor, bg=self.COLOR_FONDO)
        col1.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        # PANEL CONFIGURACIÓN AFN
        panel_izquierdo = tk.LabelFrame(col1, text=" Configuración del AFN ", **estilo_frame)
        panel_izquierdo.pack(fill="x", pady=(0, 15))

        fields = [
            ("Estados:", "txt_estados"),
            ("Alfabeto:", "txt_alfabeto"),
            ("Estado inicial:", "txt_inicial"),
            ("Estados finales:", "txt_finales")
        ]

        for idx, (label_text, var_name) in enumerate(fields):
            tk.Label(panel_izquierdo, text=label_text, font=self.FONT_BODY, bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO_PRI).grid(row=idx, column=0, sticky="w", pady=8)
            entry = tk.Entry(panel_izquierdo, width=22, **self.estilo_entry)
            entry.grid(row=idx, column=1, pady=8, padx=(10, 0), sticky="ew")
            setattr(self, var_name, entry)
        
        panel_izquierdo.columnconfigure(1, weight=1)

        boton_crear = tk.Button(
            panel_izquierdo,
            text="CREAR AUTÓMATA",
            command=self.crear_afn,
            bg=self.COLOR_BTN_PRIMARY,
            fg="white",
            activebackground=self.COLOR_BTN_PRIMARY_HOVER,
            activeforeground="white",
            font=self.FONT_BOLD,
            bd=0,
            cursor="hand2",
            pady=10
        )
        boton_crear.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(15, 0))

        # PANEL TRANSICIONES
        panel_transiciones = tk.LabelFrame(col1, text=" Agregar Transición ", **estilo_frame)
        panel_transiciones.pack(fill="x")

        trans_fields = [
            ("Origen:", "txt_origen"),
            ("Símbolo:", "txt_simbolo"),
            ("Destino:", "txt_destino")
        ]

        for idx, (label_text, var_name) in enumerate(trans_fields):
            tk.Label(panel_transiciones, text=label_text, font=self.FONT_BODY, bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO_PRI).grid(row=idx, column=0, sticky="w", pady=6)
            entry = tk.Entry(panel_transiciones, width=15, **self.estilo_entry)
            entry.grid(row=idx, column=1, pady=6, padx=(10, 0), sticky="ew")
            setattr(self, var_name, entry)

        panel_transiciones.columnconfigure(1, weight=1)

        boton_agregar = tk.Button(
            panel_transiciones,
            text="+ AÑADIR TRANSICIÓN",
            command=self.agregar_transicion,
            bg=self.COLOR_BTN_INFO,
            fg="white",
            activebackground="#0369A1",
            font=self.FONT_BOLD,
            bd=0,
            cursor="hand2",
            pady=8
        )
        boton_agregar.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        # ==================================
        # COLUMNA 2: OPERACIONES Y SIMULACIÓN
        # ==================================
        col2 = tk.Frame(contenedor, bg=self.COLOR_FONDO)
        col2.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        panel_operaciones = tk.LabelFrame(col2, text=" Operaciones & Análisis ", **estilo_frame)
        panel_operaciones.pack(fill="both", expand=True)

        def crear_btn_op(parent, texto, comando, color_bg=self.COLOR_BTN_NEUTRAL, color_fg="white"):
            return tk.Button(
                parent,
                text=texto,
                command=comando,
                bg=color_bg,
                fg=color_fg,
                activebackground=self.COLOR_BORDE,
                font=self.FONT_BOLD,
                bd=0,
                cursor="hand2",
                pady=8
            )

        tk.Label(panel_operaciones, text="PROCESAMIENTO", font=("Segoe UI", 9, "bold"), bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO_MUTED).pack(anchor="w", pady=(0, 4))
        crear_btn_op(panel_operaciones, "Mostrar Estructura AFN", self.mostrar_afn).pack(fill="x", pady=4)
        crear_btn_op(panel_operaciones, "Convertir AFN → AFD", self.convertir_afd, self.COLOR_BTN_ACTION, "white").pack(fill="x", pady=4)
        crear_btn_op(panel_operaciones, "Minimizar AFD", self.minimizar_afd, self.COLOR_BTN_ACTION, "white").pack(fill="x", pady=4)

        tk.Label(panel_operaciones, text="VISUALIZACIÓN GRÁFICA", font=("Segoe UI", 9, "bold"), bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO_MUTED).pack(anchor="w", pady=(15, 4))
        crear_btn_op(panel_operaciones, "Ver Diagrama AFN", self.dibujar_afn, self.COLOR_BTN_INFO, "white").pack(fill="x", pady=4)
        crear_btn_op(panel_operaciones, "Ver Diagrama AFD", self.dibujar_afd, self.COLOR_BTN_INFO, "white").pack(fill="x", pady=4)
        crear_btn_op(panel_operaciones, "Ver Diagrama AFD Mínimo", self.dibujar_afd_minimo, self.COLOR_BTN_INFO, "white").pack(fill="x", pady=4)

        tk.Label(panel_operaciones, text="PRUEBA DE CADENAS", font=("Segoe UI", 9, "bold"), bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO_MUTED).pack(anchor="w", pady=(15, 4))
        
        frame_cadena = tk.Frame(panel_operaciones, bg=self.COLOR_PANEL)
        frame_cadena.pack(fill="x", pady=4)
        tk.Label(frame_cadena, text="Cadena:", font=self.FONT_BODY, bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO_PRI).pack(side="left")
        self.txt_cadena = tk.Entry(frame_cadena, **self.estilo_entry)
        self.txt_cadena.pack(side="right", fill="x", expand=True, padx=(10, 0))

        crear_btn_op(panel_operaciones, "Simular en AFN", self.simular_afn, self.COLOR_BTN_SUCCESS).pack(fill="x", pady=(10, 3))
        crear_btn_op(panel_operaciones, "Simular en AFD", self.simular_afd, self.COLOR_BTN_SUCCESS).pack(fill="x", pady=3)
        crear_btn_op(panel_operaciones, "Simular en AFD Mínimo", self.simular_afd_minimo, self.COLOR_BTN_SUCCESS).pack(fill="x", pady=3)

        # ==================================
        # COLUMNA 3: CONSOLA DE RESULTADOS
        # ==================================
        col3 = tk.Frame(contenedor, bg=self.COLOR_FONDO)
        col3.grid(row=0, column=2, sticky="nsew", padx=10, pady=5)

        panel_resultado = tk.LabelFrame(col3, text=" Terminal de Salida ", **estilo_frame)
        panel_resultado.pack(fill="both", expand=True)

        self.area_resultado = tk.Text(
            panel_resultado,
            font=self.FONT_MONO,
            bg="#0B0F19",
            fg="#38BDF8",
            insertbackground="white",
            relief="flat",
            bd=0,
            padx=16,
            pady=16
        )
        self.area_resultado.pack(fill="both", expand=True)

        # ==================================
        # PANEL INFERIOR / ACCIONES
        # ==================================
        panel_inferior = tk.Frame(self.ventana, bg=self.COLOR_FONDO)
        panel_inferior.pack(fill="x", padx=35, pady=(10, 20))

        tk.Button(
            panel_inferior,
            text="Limpiar Todo",
            command=self.limpiar,
            bg=self.COLOR_BTN_NEUTRAL,
            fg="white",
            font=self.FONT_BOLD,
            bd=0,
            cursor="hand2",
            padx=25,
            pady=10
        ).pack(side="left")

        tk.Button(
            panel_inferior,
            text="Cerrar Aplicación",
            command=self.ventana.destroy,
            bg=self.COLOR_BTN_DANGER,
            fg="white",
            font=self.FONT_BOLD,
            bd=0,
            cursor="hand2",
            padx=25,
            pady=10
        ).pack(side="right")

    # ==========================================
    # LÓGICA DE DIBUJO DEL AUTÓMATA (GRÁFICOS VÍVIDOS)
    # ==========================================

    def dibujar_automata(self, automata):

        if automata is None or not automata.estados:
            messagebox.showwarning("Advertencia", "No hay autómata o estados para dibujar.")
            return

        ventana_grafico = tk.Toplevel(self.ventana)
        ventana_grafico.title("Visor de Diagramas — Estado de Transiciones")
        ventana_grafico.state("zoomed")
        ventana_grafico.configure(bg=self.COLOR_FONDO)

        header = tk.Frame(ventana_grafico, bg=self.COLOR_FONDO)
        header.pack(fill="x", padx=30, pady=15)

        tk.Label(
            header,
            text="DIAGRAMA DE TRANSICIONES DE ESTADOS",
            font=self.FONT_TITLE,
            bg=self.COLOR_FONDO,
            fg="#38BDF8"
        ).pack(anchor="w")

        marco = tk.Frame(ventana_grafico, bg=self.COLOR_FONDO)
        marco.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        canvas = tk.Canvas(marco, bg="#0F172A", highlightthickness=1, highlightbackground=self.COLOR_BORDE_ACTIVE)
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

        radio = 45
        separacion_x = 280
        separacion_y = 220
        margen_x = 180
        margen_y = 160

        columnas = min(5, max(1, len(estados)))
        filas = math.ceil(len(estados) / columnas)

        posiciones = {}
        for indice, estado in enumerate(estados):
            fila = indice // columnas
            columna = indice % columnas
            x = margen_x + columna * separacion_x
            y = margen_y + fila * separacion_y
            posiciones[estado] = (x, y)

        ancho = margen_x * 2 + (columnas - 1) * separacion_x + 250
        alto = margen_y * 2 + (filas - 1) * separacion_y + 200
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

        # LÍNEAS Y FLECHAS VÍVIDAS
        COLOR_FLECHA = "#94A3B8"

        for (origen, destino), simbolos in transiciones.items():
            if origen not in posiciones or destino not in posiciones:
                continue

            x1, y1 = posiciones[origen]
            x2, y2 = posiciones[destino]
            etiqueta = ", ".join(sorted(simbolos))

            if origen == destino:
                canvas.create_line(
                    x1 - 30, y1 - 25,
                    x1, y1 - 70,
                    x1 + 30, y1 - 25,
                    smooth=True,
                    arrow=tk.LAST,
                    fill="#F59E0B",
                    width=3
                )
                canvas.create_text(x1, y1 - 82, text=etiqueta, font=("Segoe UI", 12, "bold"), fill="#F59E0B")
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
                curvatura = 55

                control_x = (inicio_x + final_x) / 2 + perpendicular_x * curvatura
                control_y = (inicio_y + final_y) / 2 + perpendicular_y * curvatura

                canvas.create_line(
                    inicio_x, inicio_y,
                    control_x, control_y,
                    final_x, final_y,
                    smooth=True, arrow=tk.LAST, width=2.5, fill=COLOR_FLECHA
                )
                texto_x = control_x + perpendicular_x * 12
                texto_y = control_y + perpendicular_y * 12
            else:
                canvas.create_line(
                    inicio_x, inicio_y, final_x, final_y,
                    arrow=tk.LAST, width=2.5, fill=COLOR_FLECHA
                )
                texto_x = (inicio_x + final_x) / 2
                texto_y = (inicio_y + final_y) / 2 - 18

            canvas.create_text(texto_x, texto_y, text=etiqueta, font=("Segoe UI", 12, "bold"), fill="#38BDF8")

        # NODOS CON COLORES SATURADOS Y VÍVIDOS
        for estado in estados:
            x, y = posiciones[estado]

            if estado == automata.estado_inicial:
                color_estado = "#0284C7"  # Cyan vívido
                color_borde = "#38BDF8"
            elif estado in automata.estados_finales:
                color_estado = "#10B981"  # Verde vívido
                color_borde = "#34D399"
            else:
                color_estado = "#3B82F6"  # Azul vívido
                color_borde = "#60A5FA"

            canvas.create_oval(
                x - radio, y - radio, x + radio, y + radio,
                width=3, fill=color_estado, outline=color_borde
            )

            if estado in automata.estados_finales:
                canvas.create_oval(
                    x - radio + 6, y - radio + 6, x + radio - 6, y + radio - 6,
                    width=2, fill=color_estado, outline="#FFFFFF"
                )

            canvas.create_text(x, y, text=self.nombre_estado(estado), font=("Segoe UI", 12, "bold"), fill="#FFFFFF")

        if automata.estado_inicial in posiciones:
            x, y = posiciones[automata.estado_inicial]
            canvas.create_line(x - 110, y, x - radio, y, arrow=tk.LAST, width=3, fill="#38BDF8")

        # LEYENDA DEL DIAGRAMA
        canvas.create_oval(50, alto - 50, 80, alto - 20, fill="#0284C7", outline="#38BDF8", width=2)
        canvas.create_text(130, alto - 35, text="Estado Inicial", font=self.FONT_BODY, fill="#FFFFFF")

        canvas.create_oval(220, alto - 50, 250, alto - 20, fill="#10B981", outline="#34D399", width=2)
        canvas.create_text(300, alto - 35, text="Estado Final", font=self.FONT_BODY, fill="#FFFFFF")

        tk.Button(
            ventana_grafico,
            text="Cerrar Vista",
            command=ventana_grafico.destroy,
            bg=self.COLOR_BTN_NEUTRAL,
            fg="white",
            font=self.FONT_BOLD,
            bd=0,
            cursor="hand2",
            padx=25,
            pady=8
        ).pack(pady=10)

    # ==========================================
    # MÉTODOS DEL SISTEMA
    # ==========================================

    def crear_afn(self):
        estados = self.txt_estados.get().split(",")
        alfabeto = self.txt_alfabeto.get().split(",")
        inicial = self.txt_inicial.get().strip()
        finales = self.txt_finales.get().split(",")

        estados = {estado.strip() for estado in estados if estado.strip()}
        alfabeto = {simbolo.strip() for simbolo in alfabeto if simbolo.strip()}
        finales = {estado.strip() for estado in finales if estado.strip()}

        if not estados or not alfabeto or inicial not in estados:
            messagebox.showwarning("Advertencia", "Verifique los datos ingresados para el AFN.")
            return

        for estado in finales:
            if estado not in estados:
                messagebox.showwarning("Advertencia", f"El estado final '{estado}' no está registrado en la lista de estados.")
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
        messagebox.showinfo("Éxito", "Estructura del AFN creada correctamente.")

    def agregar_transicion(self):
        if self.afn is None:
            messagebox.showwarning("Advertencia", "Primero debe crear la estructura del AFN.")
            return

        origen = self.txt_origen.get().strip()
        simbolo = self.txt_simbolo.get().strip()
        destino = self.txt_destino.get().strip()

        if not origen or not simbolo or not destino:
            messagebox.showwarning("Advertencia", "Complete todos los campos de la transición.")
            return

        if origen not in self.afn.estados or destino not in self.afn.estados:
            messagebox.showwarning("Advertencia", "El estado de origen o destino no existe.")
            return

        if simbolo not in self.afn.alfabeto and simbolo != "ε":
            messagebox.showwarning("Advertencia", f"El símbolo '{simbolo}' no pertenece al alfabeto asignado.")
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
        self.area_resultado.insert(tk.END, "=== CONFIGURACIÓN AFN ===\n\n")
        self.area_resultado.insert(tk.END, f"Estados:         {self.afn.estados}\n")
        self.area_resultado.insert(tk.END, f"Alfabeto:        {self.afn.alfabeto}\n")
        self.area_resultado.insert(tk.END, f"Estado Inicial:  {self.afn.estado_inicial}\n")
        self.area_resultado.insert(tk.END, f"Estados Finales: {self.afn.estados_finales}\n\n")
        self.area_resultado.insert(tk.END, "Transiciones:\n")
        for origen, simbolos in self.afn.transiciones.items():
            for simbolo, destinos in simbolos.items():
                for destino in destinos:
                    self.area_resultado.insert(tk.END, f"  {origen} --({simbolo})--> {destino}\n")

    def convertir_afd(self):
        if self.afn is None:
            messagebox.showwarning("Advertencia", "Primero debe definir un AFN.")
            return
        try:
            convertidor = ConvertidorAFN_AFD(self.afn)
            self.afd = convertidor.convertir()
            self.mostrar_afd()
            messagebox.showinfo("Conversión", "AFN convertido a AFD con éxito.")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def mostrar_afd(self):
        if self.afd is None:
            return
        self.area_resultado.delete("1.0", tk.END)
        self.area_resultado.insert(tk.END, "=== ESTRUCTURA AFD CONVERTIDO ===\n\n")
        estados_formateados = [self.nombre_estado(estado) for estado in self.afd.estados]
        self.area_resultado.insert(tk.END, "Estados:\n  " + ", ".join(estados_formateados) + "\n\n")
        self.area_resultado.insert(tk.END, f"Alfabeto:\n  {self.afd.alfabeto}\n\n")
        self.area_resultado.insert(tk.END, "Estado Inicial:\n  " + self.nombre_estado(self.afd.estado_inicial) + "\n\n")
        finales_formateados = [self.nombre_estado(estado) for estado in self.afd.estados_finales]
        self.area_resultado.insert(tk.END, "Estados Finales:\n  " + ", ".join(finales_formateados) + "\n\n")
        self.area_resultado.insert(tk.END, "Transiciones:\n")
        for origen, simbolos in self.afd.transiciones.items():
            for simbolo, destinos in simbolos.items():
                for destino in destinos:
                    self.area_resultado.insert(tk.END, f"  {origen} --({simbolo})--> {destino}\n")

    def minimizar_afd(self):
        if self.afd is None:
            messagebox.showwarning("Advertencia", "Primero debe realizar la conversión a AFD.")
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
        self.area_resultado.insert(tk.END, "=== ESTRUCTURA AFD MINIMIZADO ===\n\n")
        estados_formateados = [self.nombre_estado(estado) for estado in self.afd_minimo.estados]
        self.area_resultado.insert(tk.END, "Estados:\n  " + ", ".join(estados_formateados) + "\n\n")
        self.area_resultado.insert(tk.END, f"Alfabeto:\n  {self.afd_minimo.alfabeto}\n\n")
        self.area_resultado.insert(tk.END, f"Estado Inicial:\n  {self.afd_minimo.estado_inicial}\n\n")
        self.area_resultado.insert(tk.END, f"Estados Finales:\n  {self.afd_minimo.estados_finales}\n\n")
        self.area_resultado.insert(tk.END, "Transiciones:\n")
        for origen, simbolos in self.afd_minimo.transiciones.items():
            for simbolo, destinos in simbolos.items():
                for destino in destinos:
                    self.area_resultado.insert(tk.END, f"  {origen} --({simbolo})--> {destino}\n")

    def simular_afn(self):
        if self.afn is None:
            messagebox.showwarning("Advertencia", "Primero debe crear un AFN.")
            return
        cadena = self.txt_cadena.get()
        simulador = SimuladorAFN(self.afn)
        resultado = simulador.simular(cadena)
        self.area_resultado.insert(tk.END, "\n\n> SIMULACIÓN EN AFN\n")
        self.area_resultado.insert(tk.END, f"  Cadena Evaluada: '{cadena}'\n")
        self.area_resultado.insert(tk.END, f"  Resultado:       {'ACEPTADA' if resultado else 'RECHAZADA'}\n")

    def simular_afd(self):
        if self.afd is None:
            messagebox.showwarning("Advertencia", "Primero debe convertir el AFN a AFD.")
            return
        cadena = self.txt_cadena.get()
        simulador = SimuladorAFD(self.afd)
        resultado = simulador.simular(cadena)
        self.area_resultado.insert(tk.END, "\n\n> SIMULACIÓN EN AFD\n")
        self.area_resultado.insert(tk.END, f"  Cadena Evaluada: '{cadena}'\n")
        self.area_resultado.insert(tk.END, f"  Resultado:       {'ACEPTADA' if resultado else 'RECHAZADA'}\n")

    def simular_afd_minimo(self):
        if self.afd_minimo is None:
            messagebox.showwarning("Advertencia", "Primero debe minimizar el AFD.")
            return
        cadena = self.txt_cadena.get()
        simulador = SimuladorAFD(self.afd_minimo)
        resultado = simulador.simular(cadena)
        self.area_resultado.insert(tk.END, "\n\n> SIMULACIÓN EN AFD MÍNIMO\n")
        self.area_resultado.insert(tk.END, f"  Cadena Evaluada: '{cadena}'\n")
        self.area_resultado.insert(tk.END, f"  Resultado:       {'ACEPTADA' if resultado else 'RECHAZADA'}\n")

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
