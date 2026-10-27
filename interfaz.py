import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import re

from database import initialize_database, query_logs, get_stats
from log_manager import log_event, export_logs
from regex_engine import validate_string, find_matches, test_many
from regex_automata import regex_to_core_afn, core_to_display_dfa, transition_lines
from conversion import ConvertidorAFN_AFD
from minimizacion import MinimizadorAFD
from simulador_afd import SimuladorAFD

BG = "#0F172A"
PANEL = "#1E293B"
PANEL2 = "#334155"
TEXT = "#F1F5F9"
MUTED = "#CBD5E1"
ACCENT = "#38BDF8"
RED = "#F43F5E"
YELLOW = "#FBBF24"

class RegexLabApp(tk.Tk):
    def __init__(self):
        super().__init__()
        initialize_database()
        self.title("Sistema de autómatas y expresiones regulares")
        self.geometry("1180x780")
        self.minsize(980, 650)
        self.configure(bg=BG)
        self.current_dfa = None
        self.current_core_dfa = None
        self.log_event("INFO", "SISTEMA", "Aplicación iniciada")
        self._style()
        self._build()

    def log_event(self, level, category, message, details=""):
        log_event(level, category, message, details)

    def _style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 10))
        style.configure("TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("TLabel", background=BG, foreground=TEXT)
        style.configure("Muted.TLabel", background=BG, foreground=MUTED)
        style.configure("Title.TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 19, "bold"))
        style.configure("Sub.TLabel", background=BG, foreground=MUTED, font=("Segoe UI", 10))
        style.configure("TButton", padding=8, background=PANEL2, foreground=TEXT)
        style.map("TButton", background=[("active", "#475569")])
        style.configure("TEntry", fieldbackground=PANEL2, foreground=TEXT, insertcolor=TEXT)
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", padding=(16, 10), background=PANEL2, foreground=TEXT)
        style.map("TNotebook.Tab", background=[("selected", "#475569")])
        style.configure("Treeview", background=PANEL, fieldbackground=PANEL, foreground=TEXT, rowheight=27)
        style.configure("Treeview.Heading", background=PANEL2, foreground=TEXT, font=("Segoe UI", 9, "bold"))
        style.map("Treeview", background=[("selected", "#075985")])

    def _build(self):
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=22, pady=(14, 6))
        tk.Label(header, text="Sistema de autómatas y expresiones regulares", bg=BG, fg=TEXT,
                 font=("Segoe UI", 17, "bold")).pack(side="left")
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=22, pady=(0, 8))

        self.stats_frame = tk.Frame(self, bg=BG)
        self.stats_frame.pack(fill="x", padx=22, pady=8)
        self.stats_labels = {}
        for key, label in [("total", "EVENTOS REGISTRADOS"), ("errors", "ERRORES CRÍTICOS"), ("warnings", "ADVERTENCIAS"), ("info", "INFORMACIÓN")]:
            card = tk.Frame(self.stats_frame, bg=PANEL, padx=15, pady=10)
            card.pack(side="left", fill="x", expand=True, padx=(0, 10))
            tk.Label(card, text=label, bg=PANEL, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w")
            value = tk.Label(card, text="0", bg=PANEL, fg=ACCENT, font=("Segoe UI", 21, "bold"))
            value.pack(anchor="w", pady=(3, 0))
            self.stats_labels[key] = value

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=22, pady=(8, 18))
        self.tab_regex = ttk.Frame(self.notebook, padding=16)
        self.tab_automata = ttk.Frame(self.notebook, padding=16)
        self.tab_logs = ttk.Frame(self.notebook, padding=16)
        self.notebook.add(self.tab_regex, text="  Regex Lab  ")
        self.notebook.add(self.tab_automata, text="  Generador de autómatas  ")
        self.notebook.add(self.tab_logs, text="  Centro de logs  ")
        self._build_regex()
        self._build_automata()
        self._build_logs()
        self.refresh_stats()
        self.refresh_logs()

    def label(self, parent, text, **kwargs):
        return ttk.Label(parent, text=text, **kwargs)

    def _build_regex(self):
        tab = self.tab_regex
        self.label(tab, "Validación y búsqueda de patrones", style="Title.TLabel").pack(anchor="w")
        self.label(tab, "Usa la sintaxis de expresiones regulares. Cada acción importante se guarda automáticamente en el historial.",
                   style="Sub.TLabel").pack(anchor="w", pady=(3, 14))

        row = ttk.Frame(tab)
        row.pack(fill="x")
        self.regex_entry = ttk.Entry(row, width=58)
        self.regex_entry.insert(0, r"^[A-Z]{3}\d{4}$")
        self.regex_entry.pack(side="left", ipady=5)
        ttk.Button(row, text="Comprobar expresión", command=self.regex_info).pack(side="left", padx=(8, 0))
        ttk.Separator(tab, orient="horizontal").pack(fill="x", pady=(12, 2))

        columns = ttk.Frame(tab)
        columns.pack(fill="both", expand=True, pady=(14, 0))
        left = ttk.Frame(columns)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        right = ttk.Frame(columns)
        right.pack(side="left", fill="both", expand=True)

        self.label(left, "Validación de cadena completa").pack(anchor="w", pady=(0, 5))
        self.string_entry = ttk.Entry(left)
        self.string_entry.insert(0, "ABC1234")
        self.string_entry.pack(fill="x", ipady=5)
        ttk.Button(left, text="Validar cadena", command=self.validate_one).pack(anchor="w", pady=8)

        self.label(left, "Prueba múltiple (una cadena por línea)").pack(anchor="w", pady=(12, 5))
        self.multi_text = tk.Text(left, height=9, bg=PANEL2, fg=TEXT, insertbackground=TEXT,
                                  relief="flat", padx=10, pady=8, font=("Consolas", 10))
        self.multi_text.pack(fill="both", expand=True)
        self.multi_text.insert("1.0", "ABC1234\nXYZ9876\nAB1234\nDEF5678")

        ttk.Button(left, text="Validar todas las cadenas", command=self.validate_many).pack(anchor="w", pady=8)

        self.label(right, "Buscar coincidencias dentro de un texto").pack(anchor="w", pady=(0, 5))
        self.search_text = tk.Text(right, height=8, bg=PANEL2, fg=TEXT, insertbackground=TEXT,
                                   relief="flat", padx=10, pady=8, font=("Consolas", 10))
        self.search_text.pack(fill="x")
        self.search_text.insert("1.0", "Eventos: ABC1234, XYZ9876 y AB1234. Código DEF5678.")
        ttk.Button(right, text="Buscar coincidencias", command=self.search_matches).pack(anchor="w", pady=8)
        self.regex_output = tk.Text(right, height=12, bg="#0B1120", fg=ACCENT, insertbackground=TEXT,
                                    relief="flat", padx=10, pady=8, font=("Consolas", 10), wrap="word")
        self.regex_output.pack(fill="both", expand=True)
        self.regex_output.insert("1.0", "Los resultados aparecerán aquí.")
        self.regex_output.configure(state="disabled")

    def set_output(self, widget, text):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    def regex_info(self):
        expr = self.regex_entry.get()
        try:
            compiled = re.compile(expr)
            msg = f"Regex válida\nLongitud: {len(expr)} caracteres\nFlags: {compiled.flags}\n\nPatrón:\n{expr}"
            self.log_event("INFO", "REGEX", "Expresión regular compilada correctamente", expr)
            self.set_output(self.regex_output, msg)
        except re.error as exc:
            self.log_event("ERROR", "REGEX", "Error de sintaxis en Regex", f"{expr} | {exc}")
            messagebox.showerror("Regex inválida", str(exc))
        self.refresh_stats()
        self.refresh_logs()

    def validate_one(self):
        expr, value = self.regex_entry.get(), self.string_entry.get()
        try:
            ok = validate_string(expr, value)
            level = "INFO" if ok else "WARNING"
            result = "VÁLIDA" if ok else "NO VÁLIDA"
            self.log_event(level, "VALIDACIÓN", f"Cadena {result.lower()}", f"Regex={expr} | Cadena={value}")
            self.set_output(self.regex_output, f"RESULTADO: {result}\n\nCadena: {value}\nExpresión: {expr}\n\nLa cadena {'cumple' if ok else 'no cumple'} completamente el patrón.")
        except ValueError as exc:
            self.log_event("ERROR", "REGEX", "No se pudo validar la cadena", str(exc))
            messagebox.showerror("Error", str(exc))
        self.refresh_stats()
        self.refresh_logs()

    def validate_many(self):
        expr = self.regex_entry.get()
        lines = self.multi_text.get("1.0", "end-1c").splitlines()
        try:
            results = test_many(expr, lines)
            valid = sum(ok for _, ok in results)
            output = [f"Resumen: {valid} válidas de {len(results)} cadenas\n"]
            output.extend([f"[{'OK' if ok else 'NO'}] {line}" for line, ok in results])
            self.set_output(self.regex_output, "\n".join(output))
            self.log_event("INFO", "VALIDACIÓN", "Validación múltiple ejecutada",
                           f"Total={len(results)} | Válidas={valid} | Regex={expr}")
        except ValueError as exc:
            self.log_event("ERROR", "REGEX", "Falló la validación múltiple", str(exc))
            messagebox.showerror("Error", str(exc))
        self.refresh_stats()
        self.refresh_logs()

    def search_matches(self):
        expr, text = self.regex_entry.get(), self.search_text.get("1.0", "end-1c")
        try:
            matches = find_matches(expr, text)
            output = [f"Coincidencias encontradas: {len(matches)}\n"]
            output.extend([f"{i}. {m['match']!r} | posiciones {m['start']}–{m['end']}" for i, m in enumerate(matches, 1)])
            if not matches:
                output.append("No se encontraron coincidencias.")
            self.set_output(self.regex_output, "\n".join(output))
            self.log_event("INFO", "BÚSQUEDA", "Búsqueda de coincidencias ejecutada",
                           f"Coincidencias={len(matches)} | Regex={expr}")
        except ValueError as exc:
            self.log_event("ERROR", "REGEX", "Falló la búsqueda de coincidencias", str(exc))
            messagebox.showerror("Error", str(exc))
        self.refresh_stats()
        self.refresh_logs()

    def _build_automata(self):
        tab = self.tab_automata
        self.label(tab, "Conversión de expresión regular a autómatas", style="Title.TLabel").pack(anchor="w")
        self.label(tab, "Convierte la expresión en AFN, AFD y AFD mínimo. Puedes revisar las transiciones y probar una cadena.",
                   style="Sub.TLabel").pack(anchor="w", pady=(3, 10))
        ttk.Separator(tab, orient="horizontal").pack(fill="x", pady=(0, 10))
        row = ttk.Frame(tab)
        row.pack(fill="x", anchor="w")
        self.automata_entry = ttk.Entry(row, width=42)
        self.automata_entry.insert(0, "(a|b)*abb")
        self.automata_entry.pack(side="left", ipady=5)
        ttk.Button(row, text="Generar AFD mínimo", command=self.generate_automaton).pack(side="left", padx=(8, 0))
        ttk.Button(row, text="Validar con AFD", command=self.validate_automaton).pack(side="left", padx=(8, 0))

        ttk.Separator(tab, orient="horizontal").pack(fill="x", pady=(12, 8))
        self.label(tab, "Cadena que deseas probar").pack(anchor="w", pady=(0, 4))
        self.automata_test = ttk.Entry(tab, width=42)
        self.automata_test.insert(0, "aabb")
        self.automata_test.pack(anchor="w", pady=(0, 8), ipady=4)
        ttk.Separator(tab, orient="horizontal").pack(fill="x", pady=(0, 10))

        body = ttk.Frame(tab)
        body.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(body, bg="#0B1120", highlightthickness=0, height=350)
        self.canvas.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.automata_output = tk.Text(body, width=35, bg=PANEL, fg=TEXT, relief="flat",
                                       padx=10, pady=8, font=("Consolas", 9), wrap="word")
        self.automata_output.pack(side="left", fill="y")
        self.automata_output.insert("1.0", "Genera un autómata para ver sus transiciones.")
        self.automata_output.configure(state="disabled")

    def generate_automaton(self):
        expr = self.automata_entry.get()
        try:
            nfa_original, afn_compartido = regex_to_core_afn(expr)
            afd_compartido = ConvertidorAFN_AFD(afn_compartido).convertir()
            afd_minimo_compartido = MinimizadorAFD(afd_compartido).minimizar()

            # Mantener el objeto real del AFD para validar con el simulador de la Entrega 1.
            self.current_core_dfa = afd_minimo_compartido
            minimized = core_to_display_dfa(afd_minimo_compartido)
            self.current_dfa = minimized

            lineas_afn = [
                f"r{origen} -- {simbolo} --> r{destino}"
                for (origen, simbolo), destinos in sorted(
                    nfa_original.transitions.items(),
                    key=lambda item: (item[0][0], item[0][1])
                )
                for destino in sorted(destinos)
            ]
            lines = [
                f"Regex: {expr}",
                f"Estados AFN: {len(nfa_original.states)}",
                f"Estados AFD: {len(afd_compartido.estados)}",
                f"Estados AFD mínimo: {len(afd_minimo_compartido.estados)}",
                f"Alfabeto: {sorted(afd_minimo_compartido.alfabeto)}",
                f"Estado inicial: {afd_minimo_compartido.estado_inicial}",
                f"Estados finales: {sorted(afd_minimo_compartido.estados_finales, key=str)}",
                "", "TRANSICIONES DEL AFN (Thompson):"
            ] + lineas_afn + ["", "TRANSICIONES DEL AFD MÍNIMO:"] + transition_lines(minimized)
            self.set_output(self.automata_output, "\n".join(lines))
            self.draw_automaton(minimized)
            self.log_event(
                "INFO", "AUTÓMATA", "AFN, AFD y AFD mínimo generados",
                f"Regex={expr} | AFN={len(nfa_original.states)} | "
                f"AFD={len(afd_compartido.estados)} | "
                f"Mínimo={len(afd_minimo_compartido.estados)}"
            )
        except Exception as exc:
            self.log_event("ERROR", "AUTÓMATA", "No se pudo generar el autómata", f"{expr} | {exc}")
            messagebox.showerror("Error al generar autómata", str(exc))
        self.refresh_stats()
        self.refresh_logs()

    def validate_automaton(self):
        if self.current_dfa is None:
            messagebox.showwarning("Autómata requerido", "Primero genera el AFD mínimo.")
            return
        value = self.automata_test.get()
        # La validación se realiza con el simulador de AFD que ya usa la Entrega 1.
        from contextlib import redirect_stdout
        import io
        salida_simulador = io.StringIO()
        with redirect_stdout(salida_simulador):
            ok = SimuladorAFD(self.current_core_dfa).simular(value)
        self.set_output(
            self.automata_output,
            f"Cadena: {value}\nResultado: {'ACEPTADA' if ok else 'RECHAZADA'}"
            + "\n\n" + "\n".join(transition_lines(self.current_dfa))
        )
        self.log_event("INFO" if ok else "WARNING", "AUTÓMATA",
                       f"Cadena {'aceptada' if ok else 'rechazada'} por el AFD",
                       f"Cadena={value}")
        self.refresh_stats()
        self.refresh_logs()

    def draw_automaton(self, dfa):
        self.canvas.delete("all")
        states = dfa["states"]
        if len(states) > 14:
            self.canvas.create_text(20, 20, anchor="nw", fill=YELLOW,
                                    text=f"El AFD tiene {len(states)} estados. Se muestra la tabla de transiciones a la derecha.")
            return
        width = max(self.canvas.winfo_width(), 600)
        height = max(self.canvas.winfo_height(), 330)
        n = len(states)
        positions = {}
        cx, cy = width / 2, height / 2
        import math
        radius = min(width, height) * 0.34
        for i, state in enumerate(states):
            angle = -math.pi / 2 + (2 * math.pi * i / max(n, 1))
            positions[state] = (cx + radius * math.cos(angle), cy + radius * math.sin(angle))

        # Dibujar transiciones antes de los estados
        for (src, symbol), dst in dfa["transitions"].items():
            x1, y1 = positions[src]
            x2, y2 = positions[dst]
            if src == dst:
                self.canvas.create_arc(x1-22, y1-38, x1+22, y1+4, start=20, extent=320,
                                       style="arc", outline=ACCENT, width=2)
                self.canvas.create_text(x1, y1-39, text=symbol, fill=TEXT, font=("Consolas", 9))
            else:
                self.canvas.create_line(x1, y1, x2, y2, fill="#64748B", width=1.5,
                                        arrow=tk.LAST, arrowshape=(8, 10, 4))
                mx, my = (x1+x2)/2, (y1+y2)/2
                self.canvas.create_text(mx, my-8, text=symbol, fill=ACCENT, font=("Consolas", 9))
        sx, sy = positions[dfa["start"]]
        self.canvas.create_line(sx-55, sy, sx-24, sy, fill=ACCENT, width=2, arrow=tk.LAST)
        for state, (x, y) in positions.items():
            fill = "#064E3B" if state in dfa["accepting"] else PANEL2
            self.canvas.create_oval(x-22, y-22, x+22, y+22, fill=fill, outline=ACCENT if state in dfa["accepting"] else "#94A3B8", width=2)
            if state in dfa["accepting"]:
                self.canvas.create_oval(x-17, y-17, x+17, y+17, outline=ACCENT, width=1)
            self.canvas.create_text(x, y, text=f"q{state}", fill=TEXT, font=("Segoe UI", 9, "bold"))

    def _build_logs(self):
        tab = self.tab_logs
        self.label(tab, "Centro de auditoría de eventos", style="Title.TLabel").pack(anchor="w")
        self.label(tab, "Los registros se guardan automáticamente en SQLite. Puedes filtrarlos y exportar el resultado.",
                   style="Sub.TLabel").pack(anchor="w", pady=(3, 12))

        filters = ttk.Frame(tab)
        filters.pack(fill="x", pady=(0, 8))
        self.level_var = tk.StringVar(value="Todos")
        self.category_var = tk.StringVar(value="Todos")
        self.log_search_var = tk.StringVar()
        ttk.Label(filters, text="Nivel:").pack(side="left", padx=(0, 5))
        ttk.Combobox(filters, textvariable=self.level_var, values=["Todos", "INFO", "WARNING", "ERROR", "CRITICAL"],
                     state="readonly", width=12).pack(side="left", padx=(0, 12))
        ttk.Label(filters, text="Categoría:").pack(side="left", padx=(0, 5))
        ttk.Combobox(filters, textvariable=self.category_var,
                     values=["Todos", "SISTEMA", "REGEX", "VALIDACIÓN", "BÚSQUEDA", "AUTÓMATA"],
                     state="readonly", width=14).pack(side="left", padx=(0, 12))
        ttk.Entry(filters, textvariable=self.log_search_var).pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=4)
        ttk.Button(filters, text="Filtrar", command=self.refresh_logs).pack(side="left")

        actions = ttk.Frame(tab)
        actions.pack(fill="x", pady=(0, 8))
        ttk.Button(actions, text="Exportar CSV", command=lambda: self.export("csv")).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Exportar TXT", command=lambda: self.export("txt")).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Actualizar", command=self.refresh_logs).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Probar error CRÍTICO", command=self.simulate_critical_error).pack(side="left")

        cols = ("id", "timestamp", "level", "category", "message", "details")
        self.logs_tree = ttk.Treeview(tab, columns=cols, show="headings")
        labels = {"id": "ID", "timestamp": "Fecha y hora", "level": "Nivel",
                  "category": "Categoría", "message": "Evento", "details": "Detalles"}
        widths = {"id": 55, "timestamp": 175, "level": 90, "category": 105, "message": 240, "details": 330}
        for col in cols:
            self.logs_tree.heading(col, text=labels[col])
            self.logs_tree.column(col, width=widths[col], anchor="w")
        self.logs_tree.tag_configure("CRITICAL", foreground="#F43F5E", font=("Segoe UI", 10, "bold"))
        self.logs_tree.tag_configure("ERROR", foreground=RED, font=("Segoe UI", 10, "bold"))
        self.logs_tree.tag_configure("WARNING", foreground=YELLOW)
        self.logs_tree.tag_configure("INFO", foreground=ACCENT)
        scroll_y = ttk.Scrollbar(tab, orient="vertical", command=self.logs_tree.yview)
        scroll_x = ttk.Scrollbar(tab, orient="horizontal", command=self.logs_tree.xview)
        self.logs_tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.logs_tree.pack(fill="both", expand=True, side="top")
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(fill="x")

    def simulate_critical_error(self):
        """Registra un evento crítico de prueba sin dañar archivos ni datos."""
        confirmed = messagebox.askyesno(
            "Simulación de error crítico",
            "Se registrará un evento CRITICAL de prueba para comprobar el sistema de logs.\n\n"
            "No se borrarán datos ni se dañará la aplicación. ¿Continuar?"
        )
        if not confirmed:
            return
        self.log_event(
            "CRITICAL", "SISTEMA",
            "SIMULACIÓN: componente esencial no disponible",
            "Evento de prueba controlado; no representa una falla real del equipo."
        )
        self.refresh_stats()
        self.refresh_logs()
        messagebox.showerror(
            "ERROR CRÍTICO DE PRUEBA",
            "Se registró un evento CRITICAL.\nAbre el Centro de logs y filtra por CRITICAL para comprobarlo."
        )

    def refresh_logs(self):
        if not hasattr(self, "logs_tree"):
            return
        rows = query_logs(
            level=self.level_var.get(),
            category=self.category_var.get(),
            search=self.log_search_var.get().strip(),
            limit=3000
        )
        for item in self.logs_tree.get_children():
            self.logs_tree.delete(item)
        for row in rows:
            self.logs_tree.insert("", "end", values=tuple(row[c] for c in
                ("id", "timestamp", "level", "category", "message", "details")),
                tags=(row["level"],))

    def refresh_stats(self):
        stats = get_stats()
        for key, value in stats.items():
            if key in self.stats_labels:
                self.stats_labels[key].configure(text=str(value))

    def export(self, format_name):
        rows = query_logs(
            level=self.level_var.get(),
            category=self.category_var.get(),
            search=self.log_search_var.get().strip(),
            limit=10000
        )
        if not rows:
            messagebox.showinfo("Sin datos", "No hay registros que exportar con los filtros actuales.")
            return
        ext = ".csv" if format_name == "csv" else ".txt"
        path = filedialog.asksaveasfilename(
            title="Guardar reporte de logs",
            defaultextension=ext,
            filetypes=[("CSV", "*.csv")] if format_name == "csv" else [("Texto", "*.txt")]
        )
        if not path:
            return
        try:
            export_logs(rows, path, format_name)
            self.log_event("INFO", "SISTEMA", "Reporte de logs exportado", f"Archivo={path} | Filas={len(rows)}")
            messagebox.showinfo("Exportación completada", f"Se exportaron {len(rows)} registros.")
            self.refresh_stats()
            self.refresh_logs()
        except OSError as exc:
            self.log_event("ERROR", "SISTEMA", "Falló la exportación de logs", str(exc))
            messagebox.showerror("Error de exportación", str(exc))

if __name__ == "__main__":
    app = RegexLabApp()
    app.mainloop()
