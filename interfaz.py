import tkinter as tk
from tkinter import messagebox
from afn import AFN
from conversion import ConvertidorAFN_AFD
from minimizacion import MinimizadorAFD
from simulador import SimuladorAFN
from simulador_afd import SimuladorAFD
import math
#diseño de iinterfaz

class InterfazAutomatas:

    def __init__(self, ventana):

        self.ventana = ventana

        self.ventana.title(
            "Sistema de Autómatas Finitos"
        )

        # Abrir maximizada
        self.ventana.state(
            "zoomed"
        )

        # Permitir cambiar tamaño
        self.ventana.resizable(
            True,
            True
        )

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
            font=("Arial", 20, "bold")
        )

        titulo.pack(
            pady=15
        )

        subtitulo = tk.Label(
            self.ventana,
            text="Construcción, conversión, minimización y simulación",
            font=("Arial", 11)
        )

        subtitulo.pack()

        # ==================================
        # CONTENEDOR PRINCIPAL
        # ==================================

        contenedor = tk.Frame(
            self.ventana
        )

        contenedor.pack(
            pady=20,
            padx=20
        )

        # ==================================
        # PANEL IZQUIERDO
        # ==================================

        panel_izquierdo = tk.LabelFrame(
            contenedor,
            text="Configuración del AFN",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )

        panel_izquierdo.grid(
            row=0,
            column=0,
            padx=10,
            sticky="n"
        )

        # ==================================
        # ESTADOS
        # ==================================

        tk.Label(
            panel_izquierdo,
            text="Estados:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=5
        )

        self.txt_estados = tk.Entry(
            panel_izquierdo,
            width=35
        )

        self.txt_estados.grid(
            row=0,
            column=1,
            pady=5
        )

        # ==================================
        # ALFABETO
        # ==================================

        tk.Label(
            panel_izquierdo,
            text="Alfabeto:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=5
        )

        self.txt_alfabeto = tk.Entry(
            panel_izquierdo,
            width=35
        )

        self.txt_alfabeto.grid(
            row=1,
            column=1,
            pady=5
        )

        # ==================================
        # ESTADO INICIAL
        # ==================================

        tk.Label(
            panel_izquierdo,
            text="Estado inicial:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=5
        )

        self.txt_inicial = tk.Entry(
            panel_izquierdo,
            width=35
        )

        self.txt_inicial.grid(
            row=2,
            column=1,
            pady=5
        )

        # ==================================
        # ESTADOS FINALES
        # ==================================

        tk.Label(
            panel_izquierdo,
            text="Estados finales:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=5
        )

        self.txt_finales = tk.Entry(
            panel_izquierdo,
            width=35
        )

        self.txt_finales.grid(
            row=3,
            column=1,
            pady=5
        )

        # ==================================
        # CREAR AFN
        # ==================================

        boton_crear = tk.Button(
            panel_izquierdo,
            text="Crear AFN",
            width=25,
            command=self.crear_afn
        )

        boton_crear.grid(
            row=4,
            column=0,
            columnspan=2,
            pady=15
        )

        # ==================================
        # PANEL DE TRANSICIONES
        # ==================================

        panel_transiciones = tk.LabelFrame(
            contenedor,
            text="Agregar transición",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )

        panel_transiciones.grid(
            row=1,
            column=0,
            padx=10,
            pady=15,
            sticky="n"
        )

        # ==================================
        # ORIGEN
        # ==================================

        tk.Label(
            panel_transiciones,
            text="Origen:"
        ).grid(
            row=0,
            column=0,
            pady=5
        )

        self.txt_origen = tk.Entry(
            panel_transiciones,
            width=12
        )

        self.txt_origen.grid(
            row=0,
            column=1,
            pady=5
        )

        # ==================================
        # SÍMBOLO
        # ==================================

        tk.Label(
            panel_transiciones,
            text="Símbolo:"
        ).grid(
            row=1,
            column=0,
            pady=5
        )

        self.txt_simbolo = tk.Entry(
            panel_transiciones,
            width=12
        )

        self.txt_simbolo.grid(
            row=1,
            column=1,
            pady=5
        )

        # ==================================
        # DESTINO
        # ==================================

        tk.Label(
            panel_transiciones,
            text="Destino:"
        ).grid(
            row=2,
            column=0,
            pady=5
        )

        self.txt_destino = tk.Entry(
            panel_transiciones,
            width=12
        )

        self.txt_destino.grid(
            row=2,
            column=1,
            pady=5
        )

        # ==================================
        # AGREGAR TRANSICIÓN
        # ==================================

        boton_agregar = tk.Button(
            panel_transiciones,
            text="Agregar transición",
            width=20,
            command=self.agregar_transicion,
            
        )

        boton_agregar.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=10
        )

        # ==================================
        # PANEL CENTRAL
        # ==================================

        panel_operaciones = tk.LabelFrame(
            contenedor,
            text="Operaciones",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )

        panel_operaciones.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=10,
            sticky="n"
        )

        # ==================================
        # MOSTRAR AFN
        # ==================================

        tk.Button(
            panel_operaciones,
            text="Mostrar AFN",
            width=25,
            command=self.mostrar_afn
        ).pack(
            pady=5
        )

        # ==================================
        # CONVERTIR
        # ==================================

        tk.Button(
            panel_operaciones,
            text="Convertir AFN → AFD",
            width=25,
            command=self.convertir_afd
        ).pack(
            pady=5
        )

        # ==================================
        # MINIMIZAR
        # ==================================

        tk.Button(
            panel_operaciones,
            text="Minimizar AFD",
            width=25,
            command=self.minimizar_afd
        ).pack(
            pady=5
        )

        # ==================================
        # GRÁFICOS
        # ==================================

        tk.Label(
            panel_operaciones,
            text="GRÁFICOS",
            font=("Arial", 10, "bold")
        ).pack(
            pady=15
        )

        tk.Button(
            panel_operaciones,
            text="Dibujar AFN",
            width=25,
            command=self.dibujar_afn
        ).pack(
            pady=5
        )

        tk.Button(
            panel_operaciones,
            text="Dibujar AFD",
            width=25,
            command=self.dibujar_afd
        ).pack(
            pady=5
        )

        tk.Button(
            panel_operaciones,
            text="Dibujar AFD mínimo",
            width=25,
            command=self.dibujar_afd_minimo
        ).pack(
            pady=5
        )

        # ==================================
        # SIMULACIÓN
        # ==================================

        tk.Label(
            panel_operaciones,
            text="SIMULACIÓN",
            font=("Arial", 10, "bold")
        ).pack(
            pady=15
        )

        tk.Label(
            panel_operaciones,
            text="Cadena a evaluar:"
        ).pack()

        self.txt_cadena = tk.Entry(
            panel_operaciones,
            width=27
        )

        self.txt_cadena.pack(
            pady=5
        )

        # ==================================
        # SIMULAR AFN
        # ==================================

        tk.Button(
            panel_operaciones,
            text="Simular AFN",
            width=25,
            command=self.simular_afn
        ).pack(
            pady=5
        )

        # ==================================
        # SIMULAR AFD
        # ==================================

        tk.Button(
            panel_operaciones,
            text="Simular AFD",
            width=25,
            command=self.simular_afd
        ).pack(
            pady=5
        )

        # ==================================
        # SIMULAR AFD MÍNIMO
        # ==================================

        tk.Button(
            panel_operaciones,
            text="Simular AFD mínimo",
            width=25,
            command=self.simular_afd_minimo
        ).pack(
            pady=5
        )

        # ==================================
        # PANEL DERECHO - RESULTADOS
        # ==================================

        panel_resultado = tk.LabelFrame(
            contenedor,
            text="Resultados",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )

        panel_resultado.grid(
            row=0,
            column=2,
            rowspan=2,
            padx=10,
            sticky="n"
        )

        self.area_resultado = tk.Text(
            panel_resultado,
            width=48,
            height=30,
            font=("Consolas", 9)
        )

        self.area_resultado.pack()

     

        # ==================================
        # BOTONES INFERIORES
        # ==================================

        panel_inferior = tk.Frame(
            self.ventana
        )

        panel_inferior.pack(
            pady=10
        )

        # Limpiar

        tk.Button(
            panel_inferior,
            text="Limpiar",
            width=18,
            command=self.limpiar
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        # Salir

        tk.Button(
            panel_inferior,
            text="Salir",
            width=18,
            command=self.ventana.destroy
        ).grid(
            row=0,
            column=1,
            padx=5
        )

    # ==========================================
    # CREAR AFN
    # ==========================================

    def crear_afn(self):

        estados = self.txt_estados.get().split(",")

        alfabeto = self.txt_alfabeto.get().split(",")

        inicial = self.txt_inicial.get().strip()

        finales = self.txt_finales.get().split(",")

        estados = {
            estado.strip()
            for estado in estados
            if estado.strip()
        }

        alfabeto = {
            simbolo.strip()
            for simbolo in alfabeto
            if simbolo.strip()
        }

        finales = {
            estado.strip()
            for estado in finales
            if estado.strip()
        }

        if not estados:

            messagebox.showwarning(
                "Advertencia",
                "Debe ingresar los estados."
            )

            return

        if not alfabeto:

            messagebox.showwarning(
                "Advertencia",
                "Debe ingresar el alfabeto."
            )

            return

        if inicial not in estados:

            messagebox.showwarning(
                "Advertencia",
                "El estado inicial no existe."
            )

            return

        for estado in finales:

            if estado not in estados:

                messagebox.showwarning(
                    "Advertencia",
                    f"El estado final {estado} no existe."
                )

                return

        self.afn = AFN()

        for estado in estados:

            self.afn.agregar_estado(
                estado
            )

        for simbolo in alfabeto:

            self.afn.agregar_simbolo(
                simbolo
            )

        self.afn.establecer_inicial(
            inicial
        )

        for estado in finales:

            self.afn.agregar_final(
                estado
            )

        self.afd = None

        self.afd_minimo = None

        self.mostrar_afn()

        messagebox.showinfo(
            "AFN",
            "AFN creado correctamente."
        )

    # ==========================================
    # AGREGAR TRANSICIÓN
    # ==========================================

    def agregar_transicion(self):

        if self.afn is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero debe crear el AFN."
            )

            return

        origen = self.txt_origen.get().strip()

        simbolo = self.txt_simbolo.get().strip()

        destino = self.txt_destino.get().strip()

        if not origen or not simbolo or not destino:

            messagebox.showwarning(
                "Advertencia",
                "Complete todos los campos."
            )

            return

        if origen not in self.afn.estados:

            messagebox.showwarning(
                "Advertencia",
                f"El estado {origen} no existe."
            )

            return

        if destino not in self.afn.estados:

            messagebox.showwarning(
                "Advertencia",
                f"El estado {destino} no existe."
            )

            return

        if (
            simbolo not in self.afn.alfabeto
            and simbolo != "ε"
        ):

            messagebox.showwarning(
                "Advertencia",
                f"El símbolo {simbolo} "
                "no pertenece al alfabeto."
            )

            return

        self.afn.agregar_transicion(
            origen,
            simbolo,
            destino
        )

        self.afd = None

        self.afd_minimo = None

        self.txt_origen.delete(
            0,
            tk.END
        )

        self.txt_simbolo.delete(
            0,
            tk.END
        )

        self.txt_destino.delete(
            0,
            tk.END
        )

        self.mostrar_afn()

    # ==========================================
    # MOSTRAR AFN
    # ==========================================

    def mostrar_afn(self):

        if self.afn is None:
            return

        self.area_resultado.delete(
            "1.0",
            tk.END
        )

        self.area_resultado.insert(
            tk.END,
            "========== AFN ==========\n\n"
        )

        self.area_resultado.insert(
            tk.END,
            f"Estados:\n"
            f"{self.afn.estados}\n\n"
        )

        self.area_resultado.insert(
            tk.END,
            f"Alfabeto:\n"
            f"{self.afn.alfabeto}\n\n"
        )

        self.area_resultado.insert(
            tk.END,
            f"Estado inicial:\n"
            f"{self.afn.estado_inicial}\n\n"
        )

        self.area_resultado.insert(
            tk.END,
            f"Estados finales:\n"
            f"{self.afn.estados_finales}\n\n"
        )

        self.area_resultado.insert(
            tk.END,
            "Transiciones:\n"
        )

        for origen, simbolos in self.afn.transiciones.items():

            for simbolo, destinos in simbolos.items():

                for destino in destinos:

                    self.area_resultado.insert(
                        tk.END,
                        f"{origen} --{simbolo}--> "
                        f"{destino}\n"
                    )

        self.area_resultado.insert(
            tk.END,
            "\n=========================="
        )

    # ==========================================
    # CONVERTIR AFN → AFD
    # ==========================================

    def convertir_afd(self):

        if self.afn is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero debe crear un AFN."
            )

            return

        try:

            convertidor = ConvertidorAFN_AFD(
                self.afn
            )

            self.afd = convertidor.convertir()

            self.mostrar_afd()

            messagebox.showinfo(
                "Conversión",
                "AFN convertido a AFD correctamente."
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # ==========================================
    # MOSTRAR AFD
    # ==========================================

    def mostrar_afd(self):

        if self.afd is None:
            return

        self.area_resultado.delete(
            "1.0",
            tk.END
        )

        self.area_resultado.insert(
            tk.END,
            "========== AFD ==========\n\n"
        )

        estados_formateados = [
            self.nombre_estado(estado)
            for estado in self.afd.estados
        ]

        self.area_resultado.insert(
            tk.END,
            "Estados:\n"
            + ", ".join(estados_formateados)
            + "\n\n"
        )

        self.area_resultado.insert(
            tk.END,
            f"Alfabeto:\n"
            f"{self.afd.alfabeto}\n\n"
        )

        self.area_resultado.insert(
            tk.END,
            "Estado inicial:\n"
            + self.nombre_estado(
                self.afd.estado_inicial
            )
            + "\n\n"
        )

        finales_formateados = [
            self.nombre_estado(estado)
            for estado in self.afd.estados_finales
        ]

        self.area_resultado.insert(
            tk.END,
            "Estados finales:\n"
            + ", ".join(finales_formateados)
            + "\n\n"
        )

        self.area_resultado.insert(
            tk.END,
            "Transiciones:\n"
        )

        for origen, simbolos in self.afd.transiciones.items():

            for simbolo, destinos in simbolos.items():

                for destino in destinos:

                    self.area_resultado.insert(
                        tk.END,
                        f"{origen} --{simbolo}--> "
                        f"{destino}\n"
                    )

    # ==========================================
    # MINIMIZAR AFD
    # ==========================================

    def minimizar_afd(self):

        if self.afd is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero debe convertir el AFN a AFD."
            )

            return

        try:

            minimizador = MinimizadorAFD(
                self.afd
            )

            self.afd_minimo = (
                minimizador.minimizar()
            )

            self.mostrar_afd_minimo()

            messagebox.showinfo(
                "Minimización",
                "AFD minimizado correctamente."
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # ==========================================
    # MOSTRAR AFD MINIMIZADO
    # ==========================================

    def mostrar_afd_minimo(self):

        if self.afd_minimo is None:
            return

        self.area_resultado.delete(
            "1.0",
            tk.END
        )

        self.area_resultado.insert(
            tk.END,
            "======= AFD MINIMIZADO =======\n\n"
        )

        estados_formateados = [
            self.nombre_estado(estado)
            for estado in self.afd_minimo.estados
        ]

        self.area_resultado.insert(
            tk.END,
            "Estados:\n"
            + ", ".join(estados_formateados)
            + "\n\n"
        )

        self.area_resultado.insert(
            tk.END,
            f"Alfabeto:\n"
            f"{self.afd_minimo.alfabeto}\n\n"
        )

        self.area_resultado.insert(
            tk.END,
            f"Estado inicial:\n"
            f"{self.afd_minimo.estado_inicial}\n\n"
        )

        self.area_resultado.insert(
            tk.END,
            f"Estados finales:\n"
            f"{self.afd_minimo.estados_finales}\n\n"
        )

        self.area_resultado.insert(
            tk.END,
            "Transiciones:\n"
        )

        for origen, simbolos in self.afd_minimo.transiciones.items():

            for simbolo, destinos in simbolos.items():

                for destino in destinos:

                    self.area_resultado.insert(
                        tk.END,
                        f"{origen} --{simbolo}--> "
                        f"{destino}\n"
                    )

    # ==========================================
    # SIMULAR AFN
    # ==========================================

    def simular_afn(self):

        if self.afn is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero debe crear un AFN."
            )

            return

        cadena = self.txt_cadena.get()

        simulador = SimuladorAFN(
            self.afn
        )

        resultado = simulador.simular(
            cadena
        )

        self.area_resultado.insert(
            tk.END,
            "\n\n========== SIMULACIÓN AFN ==========\n"
        )

        self.area_resultado.insert(
            tk.END,
            f"Cadena: {cadena}\n"
        )

        if resultado:

            self.area_resultado.insert(
                tk.END,
                "RESULTADO: ACEPTADA\n"
            )

        else:

            self.area_resultado.insert(
                tk.END,
                "RESULTADO: RECHAZADA\n"
            )

    # ==========================================
    # SIMULAR AFD
    # ==========================================

    def simular_afd(self):

        if self.afd is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero debe convertir el AFN a AFD."
            )

            return

        cadena = self.txt_cadena.get()

        simulador = SimuladorAFD(
            self.afd
        )

        resultado = simulador.simular(
            cadena
        )

        self.area_resultado.insert(
            tk.END,
            "\n\n========== SIMULACIÓN AFD ==========\n"
        )

        self.area_resultado.insert(
            tk.END,
            f"Cadena: {cadena}\n"
        )

        if resultado:

            self.area_resultado.insert(
                tk.END,
                "RESULTADO: ACEPTADA\n"
            )

        else:

            self.area_resultado.insert(
                tk.END,
                "RESULTADO: RECHAZADA\n"
            )

    # ==========================================
    # SIMULAR AFD MINIMIZADO
    # ==========================================

    def simular_afd_minimo(self):

        if self.afd_minimo is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero debe minimizar el AFD."
            )

            return

        cadena = self.txt_cadena.get()

        simulador = SimuladorAFD(
            self.afd_minimo
        )

        resultado = simulador.simular(
            cadena
        )

        self.area_resultado.insert(
            tk.END,
            "\n\n===== SIMULACIÓN AFD MÍNIMO =====\n"
        )

        self.area_resultado.insert(
            tk.END,
            f"Cadena: {cadena}\n"
        )

        if resultado:

            self.area_resultado.insert(
                tk.END,
                "RESULTADO: ACEPTADA\n"
            )

        else:

            self.area_resultado.insert(
                tk.END,
                "RESULTADO: RECHAZADA\n"
            )
                # ==========================================
    # FORMATEAR NOMBRE DE ESTADO
    # ==========================================

    def nombre_estado(self, estado):

        if isinstance(estado, frozenset):

            if not estado:
                return "∅"

            return "{" + ", ".join(
                sorted(
                    str(elemento)
                    for elemento in estado
                )
            ) + "}"

        return str(estado)
        # ==========================================
    # FORMATEAR ESTADO PARA MOSTRAR
    # ==========================================

    def nombre_estado(self, estado):

        # Si es un estado generado por la conversión AFN → AFD
        if isinstance(estado, frozenset):

            # Estado vacío
            if not estado:
                return "∅"

            elementos = sorted(
                [str(elemento) for elemento in estado],
                key=self.orden_estado
            )

            # Si solamente contiene un estado
            if len(elementos) == 1:
                return elementos[0]

            # Si contiene varios estados
            return "{" + ", ".join(elementos) + "}"

        return str(estado)

    # ==========================================
    # ORDENAR ESTADOS
    # ==========================================

    def orden_estado(self, estado):

        texto = str(estado)

        # Buscar números dentro del nombre
        numero = ""

        for caracter in texto:

            if caracter.isdigit():
                numero += caracter

        if numero:
            return (
                texto.rstrip("0123456789"),
                int(numero)
            )

        return (
            texto,
            0
        )
    # ==========================================
    # DIBUJAR AUTÓMATA
    # ==========================================

        # ==========================================
    # DIBUJAR AUTÓMATA
    # ==========================================

    def dibujar_automata(self, automata):

        if automata is None:

            messagebox.showwarning(
                "Advertencia",
                "No existe un autómata para dibujar."
            )

            return

        if not automata.estados:

            messagebox.showwarning(
                "Advertencia",
                "No hay estados para dibujar."
            )

            return

        # ==================================
        # CREAR VENTANA
        # ==================================

        ventana_grafico = tk.Toplevel(
            self.ventana
        )

        ventana_grafico.title(
            "Diagrama del autómata"
        )

        ventana_grafico.state(
            "zoomed"
        )

        ventana_grafico.resizable(
            True,
            True
        )

        # ==================================
        # TÍTULO
        # ==================================

        titulo = tk.Label(
            ventana_grafico,
            text="REPRESENTACIÓN GRÁFICA DEL AUTÓMATA",
            font=("Arial", 18, "bold")
        )

        titulo.pack(
            pady=10
        )

        # ==================================
        # MARCO DEL CANVAS
        # ==================================

        marco = tk.Frame(
            ventana_grafico
        )

        marco.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        # ==================================
        # CANVAS
        # ==================================

        canvas = tk.Canvas(
            marco,
            bg="white"
        )

        canvas.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # ==================================
        # BARRAS DE DESPLAZAMIENTO
        # ==================================

        barra_horizontal = tk.Scrollbar(
            marco,
            orient="horizontal",
            command=canvas.xview
        )

        barra_horizontal.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        barra_vertical = tk.Scrollbar(
            marco,
            orient="vertical",
            command=canvas.yview
        )

        barra_vertical.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        canvas.configure(
            xscrollcommand=barra_horizontal.set,
            yscrollcommand=barra_vertical.set
        )

        marco.grid_rowconfigure(
            0,
            weight=1
        )

        marco.grid_columnconfigure(
            0,
            weight=1
        )

        # ==================================
        # ORDENAR ESTADOS
        # ==================================

        estados = sorted(
            list(automata.estados),
            key=lambda estado: (
                0 if estado == automata.estado_inicial else 1,
                self.orden_estado(
                    self.nombre_estado(estado)
                )
            )
        )

        # ==================================
        # CONFIGURACIÓN
        # ==================================

        radio = 38

        separacion_x = 230

        separacion_y = 170

        margen_x = 160

        margen_y = 130

        # Máximo 5 estados por fila

        columnas = min(
            5,
            max(1, len(estados))
        )

        filas = math.ceil(
            len(estados) / columnas
        )

        # ==================================
        # POSICIONES
        # ==================================

        posiciones = {}

        for indice, estado in enumerate(estados):

            fila = indice // columnas

            columna = indice % columnas

            x = (
                margen_x
                + columna * separacion_x
            )

            y = (
                margen_y
                + fila * separacion_y
            )

            posiciones[estado] = (
                x,
                y
            )

        # ==================================
        # TAMAÑO DEL CANVAS
        # ==================================

        ancho = (
            margen_x * 2
            + (columnas - 1) * separacion_x
            + 200
        )

        alto = (
            margen_y * 2
            + (filas - 1) * separacion_y
            + 180
        )

        canvas.config(
            scrollregion=(
                0,
                0,
                ancho,
                alto
            )
        )

        # ==================================
        # AGRUPAR TRANSICIONES
        # ==================================

        transiciones = {}

        for origen, simbolos in automata.transiciones.items():

            for simbolo, destinos in simbolos.items():
                destinos_lista = destinos if isinstance(destinos, (list, set, tuple, frozenset)) else [destinos]

                for destino in destinos:

                    clave = (
                        origen,
                        destino
                    )

                    if clave not in transiciones:

                        transiciones[clave] = []

                    transiciones[clave].append(
                        str(simbolo)
                    )

        # ==================================
        # DIBUJAR TRANSICIONES
        # ==================================

        for (origen, destino), simbolos in transiciones.items():

            if origen not in posiciones:
                continue

            if destino not in posiciones:
                continue

            x1, y1 = posiciones[origen]

            x2, y2 = posiciones[destino]

            etiqueta = ", ".join(
                sorted(simbolos)
            )

            # ==================================
            # BUCLE DEL MISMO ESTADO
            # ==================================

            if origen == destino:

                # Dibujar bucle (transición a sí mismo) usando una línea curva que sí acepta flecha
                canvas.create_line(
                    x1 - 25, y1 - 20,
                    x1, y1 - 55,
                    x1 + 25, y1 - 20,
                    smooth=True,
                    arrow=tk.LAST
                )

                canvas.create_text(
                    x1,
                    y1 - 100,
                    text=etiqueta,
                    font=(
                        "Arial",
                        12,
                        "bold"
                    )
                )

                continue

            # ==================================
            # DISTANCIA
            # ==================================

            dx = x2 - x1

            dy = y2 - y1

            distancia = math.sqrt(
                dx ** 2 + dy ** 2
            )

            if distancia == 0:
                continue

            # ==================================
            # PUNTOS DE ENTRADA Y SALIDA
            # ==================================

            inicio_x = (
                x1
                + dx / distancia * radio
            )

            inicio_y = (
                y1
                + dy / distancia * radio
            )

            final_x = (
                x2
                - dx / distancia * radio
            )

            final_y = (
                y2
                - dy / distancia * radio
            )

            # ==================================
            # COMPROBAR SI EXISTE TRANSICIÓN
            # EN SENTIDO CONTRARIO
            # ==================================

            existe_inversa = (
                (destino, origen)
                in transiciones
            )

            # ==================================
            # FLECHA CURVA PARA TRANSICIONES
            # DE IDA Y VUELTA
            # ==================================

            if existe_inversa:

                # Vector perpendicular
                perpendicular_x = (
                    -dy / distancia
                )

                perpendicular_y = (
                    dx / distancia
                )

                curvatura = 45

                control_x = (
                    (inicio_x + final_x) / 2
                    + perpendicular_x * curvatura
                )

                control_y = (
                    (inicio_y + final_y) / 2
                    + perpendicular_y * curvatura
                )

                canvas.create_line(
                    inicio_x,
                    inicio_y,
                    control_x,
                    control_y,
                    final_x,
                    final_y,
                    smooth=True,
                    arrow=tk.LAST,
                    width=2
                )

                # Etiqueta
                texto_x = (
                    control_x
                    + perpendicular_x * 10
                )

                texto_y = (
                    control_y
                    + perpendicular_y * 10
                )

            # ==================================
            # FLECHA RECTA
            # ==================================

            else:

                canvas.create_line(
                    inicio_x,
                    inicio_y,
                    final_x,
                    final_y,
                    arrow=tk.LAST,
                    width=2
                )

                texto_x = (
                    inicio_x + final_x
                ) / 2

                texto_y = (
                    inicio_y + final_y
                ) / 2 - 15

            # ==================================
            # SÍMBOLOS
            # ==================================

            canvas.create_text(
                texto_x,
                texto_y,
                text=etiqueta,
                font=(
                    "Arial",
                    12,
                    "bold"
                )
            )

        # ==================================
        # DIBUJAR ESTADOS
        # ==================================

        for estado in estados:

            x, y = posiciones[estado]

            # ==================================
            # COLOR DEL ESTADO
            # ==================================

            if estado == automata.estado_inicial:

                color_estado = "#DDEBFF"

            elif estado in automata.estados_finales:

                color_estado = "#DFF5E1"

            else:

                color_estado = "#F2F2F2"

            # ==================================
            # CÍRCULO EXTERIOR
            # ==================================

            canvas.create_oval(
                x - radio,
                y - radio,
                x + radio,
                y + radio,
                width=2,
                fill=color_estado
            )

            # ==================================
            # ESTADO FINAL
            # ==================================

            if estado in automata.estados_finales:

                canvas.create_oval(
                    x - radio + 7,
                    y - radio + 7,
                    x + radio - 7,
                    y + radio - 7,
                    width=2,
                    fill=color_estado
                )

            # ==================================
            # NOMBRE
            # ==================================

            canvas.create_text(
                x,
                y,
                text=self.nombre_estado(estado),
                font=(
                    "Arial",
                    13,
                    "bold"
                )
            )

        # ==================================
        # FLECHA DEL ESTADO INICIAL
        # ==================================

        if automata.estado_inicial in posiciones:

            x, y = posiciones[
                automata.estado_inicial
            ]

            canvas.create_line(
                x - 100,
                y,
                x - radio,
                y,
                arrow=tk.LAST,
                width=2
            )

        # ==================================
        # LEYENDA
        # ==================================

        canvas.create_text(
            160,
            alto - 50,
            text="Estado inicial",
            font=(
                "Arial",
                10
            )
        )

        canvas.create_oval(
            100,
            alto - 60,
            130,
            alto - 30,
            fill="#DDEBFF",
            width=2
        )

        canvas.create_text(
            340,
            alto - 50,
            text="Estado final",
            font=(
                "Arial",
                10
            )
        )

        canvas.create_oval(
            280,
            alto - 60,
            310,
            alto - 30,
            fill="#DFF5E1",
            width=2
        )

        # ==================================
        # BOTÓN CERRAR
        # ==================================

        tk.Button(
            ventana_grafico,
            text="Cerrar",
            width=18,
            command=ventana_grafico.destroy
        ).pack(
            pady=10
        )
       
    # DIBUJAR AFN
    # ==========================================

    def dibujar_afn(self):

        if self.afn is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero debe crear el AFN."
            )

            return

        self.dibujar_automata(
            self.afn
        )

    # ==========================================
    # DIBUJAR AFD
    # ==========================================

    def dibujar_afd(self):

        if self.afd is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero debe convertir el AFN a AFD."
            )

            return

        self.dibujar_automata(
            self.afd
        )

    # ==========================================
    # DIBUJAR AFD MÍNIMO
    # ==========================================

    def dibujar_afd_minimo(self):

        if self.afd_minimo is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero debe minimizar el AFD."
            )

            return
        if not self.afd_minimo.estados:
            self.afd_minimo.agregar_estado("q_trap")
            self.afd_minimo.establecer_inicial("q_trap")
            for simbolo in self.afd_minimo.alfabeto:
                self.afd_minimo.agregar_transicion("q_trap", simbolo, "q_trap")
                

        self.dibujar_automata(
            self.afd_minimo
        )

    # ==========================================
    # LIMPIAR
    # ==========================================

    def limpiar(self):

        self.txt_estados.delete(
            0,
            tk.END
        )

        self.txt_alfabeto.delete(
            0,
            tk.END
        )

        self.txt_inicial.delete(
            0,
            tk.END
        )

        self.txt_finales.delete(
            0,
            tk.END
        )

        self.txt_origen.delete(
            0,
            tk.END
        )

        self.txt_simbolo.delete(
            0,
            tk.END
        )

        self.txt_destino.delete(
            0,
            tk.END
        )

        self.txt_cadena.delete(
            0,
            tk.END
        )

        self.area_resultado.delete(
            "1.0",
            tk.END
        )

        

        

        self.afn = None

        self.afd = None

        self.afd_minimo = None


# ==============================================
# INICIAR APLICACIÓN
# ==============================================

if __name__ == "__main__":

    ventana = tk.Tk()

    aplicacion = InterfazAutomatas(
        ventana
    )

    ventana.mainloop()
