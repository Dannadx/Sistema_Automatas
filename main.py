
import tkinter as tk
from tkinter import messagebox


class MenuPrincipal:
    def __init__(self, ventana):
        self.ventana = ventana

        self.ventana.title("Sistema de Autómatas Finitos")
        self.ventana.geometry("720x460")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f2f4f7")

        self.crear_interfaz()

    def crear_interfaz(self):
        contenedor = tk.Frame(
            self.ventana,
            bg="#f2f4f7"
        )
        contenedor.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=25
        )

        tk.Label(
            contenedor,
            text="SISTEMA DE AUTÓMATAS FINITOS",
            font=("Segoe UI", 19, "bold"),
            bg="#f2f4f7",
            fg="#26364a"
        ).pack(pady=(15, 8))

        tk.Label(
            contenedor,
            text="Seleccione el módulo que desea utilizar",
            font=("Segoe UI", 11),
            bg="#f2f4f7",
            fg="#667085"
        ).pack(pady=(0, 25))

        opciones = tk.Frame(
            contenedor,
            bg="#f2f4f7"
        )
        opciones.pack(fill="both", expand=True)

        # -----------------------------
        # OPCIÓN 1: AUTÓMATAS FINITOS
        # -----------------------------
        tarjeta_automatas = tk.Frame(
            opciones,
            bg="white",
            highlightbackground="#d5dce5",
            highlightthickness=1
        )
        tarjeta_automatas.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            tarjeta_automatas,
            text="AUTÓMATAS FINITOS",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg="#26364a"
        ).pack(pady=(28, 15))

        tk.Label(
            tarjeta_automatas,
            text=(
                "Crear y configurar autómatas.\n\n"
                "Simular cadenas mediante AFN y AFD.\n\n"
                "Convertir y minimizar autómatas."
            ),
            font=("Segoe UI", 10),
            bg="white",
            fg="#586477",
            justify="center"
        ).pack(padx=10, pady=(0, 20))

        tk.Button(
            tarjeta_automatas,
            text="Abrir autómatas",
            font=("Segoe UI", 10, "bold"),
            bg="#34495e",
            fg="white",
            activebackground="#263747",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.abrir_automatas
        ).pack(pady=(0, 25), ipadx=12, ipady=7)

        # -----------------------------
        # OPCIÓN 2: REGEX LAB
        # -----------------------------
        tarjeta_regex = tk.Frame(
            opciones,
            bg="white",
            highlightbackground="#d5dce5",
            highlightthickness=1
        )
        tarjeta_regex.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        tk.Label(
            tarjeta_regex,
            text="REGEX LAB",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg="#26364a"
        ).pack(pady=(28, 15))

        tk.Label(
            tarjeta_regex,
            text=(
                "Validar expresiones regulares.\n\n"
                "Buscar coincidencias en textos.\n\n"
                "Generar autómatas y consultar logs."
            ),
            font=("Segoe UI", 10),
            bg="white",
            fg="#586477",
            justify="center"
        ).pack(padx=10, pady=(0, 20))

        tk.Button(
            tarjeta_regex,
            text="Abrir Regex Lab",
            font=("Segoe UI", 10, "bold"),
            bg="#34495e",
            fg="white",
            activebackground="#263747",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.abrir_regex
        ).pack(pady=(0, 25), ipadx=12, ipady=7)

        # Línea divisoria inferior
        tk.Frame(
            contenedor,
            bg="#cbd3dd",
            height=1
        ).pack(fill="x", pady=(20, 10))

        tk.Label(
            contenedor,
            text="Sistema integrado de autómatas y expresiones regulares",
            font=("Segoe UI", 9),
            bg="#f2f4f7",
            fg="#7b8491"
        ).pack()

    def abrir_automatas(self):
        try:
            # Importar la interfaz original
            from automatas_finitos import InterfazAutomatas

            # Crear una nueva ventana para los autómatas
            nueva_ventana = tk.Tk()
            nueva_ventana.withdraw()

            try:
                aplicacion = InterfazAutomatas(nueva_ventana)

                self.ventana.destroy()
                nueva_ventana.deiconify()
                nueva_ventana.mainloop()

            except Exception:
                nueva_ventana.destroy()
                raise

        except Exception as error:
            messagebox.showerror(
                "Error al abrir autómatas",
                f"No se pudo abrir la interfaz original.\n\n{error}"
            )

    def abrir_regex(self):
        try:
            # Importar la interfaz de Regex Lab
            from interfaz import RegexLabApp

            # RegexLabApp ya hereda de tk.Tk
            self.ventana.destroy()

            aplicacion = RegexLabApp()
            aplicacion.mainloop()

        except Exception as error:
            messagebox.showerror(
                "Error al abrir Regex Lab",
                f"No se pudo abrir la interfaz de Regex Lab.\n\n{error}"
            )


if __name__ == "__main__":
    ventana = tk.Tk()
    aplicacion = MenuPrincipal(ventana)
    ventana.mainloop()
