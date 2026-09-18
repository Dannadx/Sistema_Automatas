class Automata:

    def __init__(self):
        # Conjunto de estados
        self.estados = set()

        # Alfabeto del autómata
        self.alfabeto = set()

        # Estado inicial
        self.estado_inicial = None

        # Estados finales
        self.estados_finales = set()

        # Transiciones
        self.transiciones = {}


    def agregar_estado(self, estado):
        """Agrega un estado al autómata."""
        self.estados.add(estado)


    def agregar_simbolo(self, simbolo):
        """Agrega un símbolo al alfabeto."""
        self.alfabeto.add(simbolo)


    def establecer_inicial(self, estado):
        """Establece el estado inicial."""
        if estado in self.estados:
            self.estado_inicial = estado
        else:
            print("El estado no existe.")


    def agregar_final(self, estado):
        """Agrega un estado final."""
        if estado in self.estados:
            self.estados_finales.add(estado)
        else:
            print("El estado no existe.")


    def agregar_transicion(self, origen, simbolo, destino):
        """Agrega una transición."""
        if origen not in self.estados:
            print(f"El estado {origen} no existe.")
            return

        if destino not in self.estados:
            print(f"El estado {destino} no existe.")
            return

        if simbolo not in self.alfabeto and simbolo != "ε":
            print(f"El símbolo {simbolo} no pertenece al alfabeto.")
            return

        if origen not in self.transiciones:
            self.transiciones[origen] = {}

        if simbolo not in self.transiciones[origen]:
            self.transiciones[origen][simbolo] = set()

        self.transiciones[origen][simbolo].add(destino)


    def mostrar(self):
        """Muestra la información del autómata."""

        print("\n========== AUTÓMATA ==========")

        print("Estados:", self.estados)

        print("Alfabeto:", self.alfabeto)

        print("Estado inicial:", self.estado_inicial)

        print("Estados finales:", self.estados_finales)

        print("\nTransiciones:")

        for origen, simbolos in self.transiciones.items():
            for simbolo, destinos in simbolos.items():
                for destino in destinos:
                    print(f"  {origen} --{simbolo}--> {destino}")

        print("===============================\n")
