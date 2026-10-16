
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from regex_engine import (
    validar_cadena,
    buscar_coincidencias,
    obtener_informacion
)
from log_analyzer import analizar_logs


class AplicacionRegex:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Expresiones Regulares y Logs")
        self.ventana.geometry("1000x680")
        self.ventana.minsize(800, 550)

        self.crear_interfaz()

    def crear_interfaz(self):
        titulo = ttk.Label(
            self.ventana,
            text="ANÁLISIS DE EXPRESIONES REGULARES Y LOGS",
            font=("Arial", 15, "bold")
        )
        titulo.pack(pady=12)

        self.pestanas = ttk.Notebook(self.ventana)
        self.pestanas.pack(fill="both", expand=True, padx=12, pady=8)

        self.pestana_regex = ttk.Frame(self.pestanas, padding=12)
        self.pestana_logs = ttk.Frame(self.pestanas, padding=12)

        self.pestanas.add(
            self.pestana_regex,
            text="Expresiones regulares"
        )
        self.pestanas.add(
            self.pestana_logs,
            text="Validación de logs"
        )

        self.crear_pestana_regex()
        self.crear_pestana_logs()

    def crear_pestana_regex(self):
        marco = self.pestana_regex

        ttk.Label(
            marco, text="Expresión regular:"
        ).pack(anchor="w")

        self.regex_var = tk.StringVar(value=r"^[A-Z]{3}\d{4}$")

        ttk.Entry(
            marco, textvariable=self.regex_var
        ).pack(fill="x", pady=5)

        ttk.Label(
            marco, text="Cadena que deseas validar:"
        ).pack(anchor="w", pady=(10, 0))

        self.cadena_var = tk.StringVar(value="ABC1234")

        ttk.Entry(
            marco, textvariable=self.cadena_var
        ).pack(fill="x", pady=5)

        botones = ttk.Frame(marco)
        botones.pack(fill="x", pady=8)

        ttk.Button(
            botones,
            text="Validar cadena",
            command=self.validar
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            botones,
            text="Información de Regex",
            command=self.informacion
        ).pack(side="left")

        ttk.Label(
            marco, text="Texto para buscar coincidencias:"
        ).pack(anchor="w", pady=(10, 0))

        self.texto_busqueda = tk.Text(marco, height=6)
        self.texto_busqueda.pack(fill="x", pady=5)
        self.texto_busqueda.insert(
            "1.0",
            "ABC1234, XYZ9876, AB1234, DEF5678"
        )

        ttk.Button(
            marco,
            text="Buscar coincidencias",
            command=self.buscar
        ).pack(anchor="w", pady=5)

        ttk.Label(
            marco, text="Resultados:"
        ).pack(anchor="w", pady=(8, 0))

        self.resultado_regex = tk.Text(
            marco, height=9, state="disabled", wrap="word"
        )
        self.resultado_regex.pack(fill="both", expand=True, pady=5)

    def mostrar_resultado(self, widget, mensaje):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", mensaje)
        widget.config(state="disabled")

    def validar(self):
        expresion = self.regex_var.get()
        cadena = self.cadena_var.get()

        try:
            resultado = validar_cadena(expresion, cadena)

            if resultado:
                mensaje = f"CADENA VÁLIDA\n\nLa cadena '{cadena}' cumple la Regex."
            else:
                mensaje = f"CADENA NO VÁLIDA\n\nLa cadena '{cadena}' no cumple la Regex."

            self.mostrar_resultado(self.resultado_regex, mensaje)

        except ValueError as error:
            messagebox.showerror("Error de Regex", str(error))

    def informacion(self):
        try:
            datos = obtener_informacion(self.regex_var.get())

            mensaje = (
                f"Expresión: {datos['expresion']}\n"
                f"Longitud: {datos['longitud']} caracteres\n"
                f"Compilación: correcta"
            )

            self.mostrar_resultado(self.resultado_regex, mensaje)

        except ValueError as error:
            messagebox.showerror("Error de Regex", str(error))

    def buscar(self):
        try:
            expresion = self.regex_var.get()
            texto = self.texto_busqueda.get("1.0", "end-1c")

            coincidencias = buscar_coincidencias(expresion, texto)

            if not coincidencias:
                mensaje = "No se encontraron coincidencias."
            else:
                lineas = [
                    f"{i}. '{c['texto']}' "
                    f"(posición {c['inicio']} a {c['fin']})"
                    for i, c in enumerate(coincidencias, start=1)
                ]
                mensaje = (
                    f"Coincidencias encontradas: {len(coincidencias)}\n\n"
                    + "\n".join(lineas)
                )

            self.mostrar_resultado(self.resultado_regex, mensaje)

        except ValueError as error:
            messagebox.showerror("Error de Regex", str(error))

    def crear_pestana_logs(self):
        marco = self.pestana_logs

        ttk.Label(
            marco, text="Expresión regular para filtrar logs:"
        ).pack(anchor="w")

        self.regex_logs_var = tk.StringVar(
            value=r"\b(ERROR|CRITICAL)\b"
        )

        ttk.Entry(
            marco, textvariable=self.regex_logs_var
        ).pack(fill="x", pady=5)

        botones = ttk.Frame(marco)
        botones.pack(fill="x", pady=8)

        ttk.Button(
            botones,
            text="Seleccionar archivo",
            command=self.seleccionar_logs
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            botones,
            text="Analizar logs",
            command=self.analizar
        ).pack(side="left")

        self.ruta_logs_var = tk.StringVar(
            value="Ningún archivo seleccionado"
        )

        ttk.Label(
            marco,
            textvariable=self.ruta_logs_var,
            wraplength=850
        ).pack(anchor="w", pady=5)

        columnas = ("linea", "nivel", "coincidencias", "contenido")

        self.tabla = ttk.Treeview(
            marco, columns=columnas, show="headings"
        )

        self.tabla.heading("linea", text="Línea")
        self.tabla.heading("nivel", text="Nivel")
        self.tabla.heading("coincidencias", text="Coincidencias")
        self.tabla.heading("contenido", text="Contenido del registro")

        self.tabla.column("linea", width=60, anchor="center")
        self.tabla.column("nivel", width=120, anchor="center")
        self.tabla.column("coincidencias", width=110, anchor="center")
        self.tabla.column("contenido", width=570)

        scroll = ttk.Scrollbar(
            marco, orient="vertical", command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.pack(
            side="left", fill="both", expand=True, pady=8
        )
        scroll.pack(side="right", fill="y", pady=8)

        self.resumen_logs_var = tk.StringVar(
            value="Selecciona un archivo para comenzar."
        )

        ttk.Label(
            marco, textvariable=self.resumen_logs_var
        ).pack(side="bottom", anchor="w", pady=5)

    def seleccionar_logs(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de logs",
            filetypes=[
                ("Archivos de registro", "*.log *.txt"),
                ("Todos los archivos", "*.*")
            ]
        )

        if ruta:
            self.ruta_logs_var.set(ruta)

    def analizar(self):
        ruta = self.ruta_logs_var.get()

        if ruta == "Ningún archivo seleccionado":
            messagebox.showwarning(
                "Archivo requerido",
                "Selecciona un archivo .log o .txt."
            )
            return

        try:
            resultados = analizar_logs(
                ruta, self.regex_logs_var.get()
            )

            for elemento in self.tabla.get_children():
                self.tabla.delete(elemento)

            for registro in resultados:
                self.tabla.insert(
                    "",
                    "end",
                    values=(
                        registro["linea"],
                        registro["nivel"],
                        registro["coincidencias"],
                        registro["contenido"]
                    )
                )

            self.resumen_logs_var.set(
                f"Registros coincidentes: {len(resultados)}"
            )

        except (ValueError, OSError) as error:
            messagebox.showerror("Error de análisis", str(error))


def iniciar():
    ventana = tk.Tk()
    AplicacionRegex(ventana)
    ventana.mainloop()
