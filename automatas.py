class Automata:

    def __init__(self):

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

    def es_estado_final(self, estado):
        """Comprueba si un estado pertenece al conjunto de estados finales."""
        return estado in self.estados_finales

    def existe_estado(self, estado):
        """Comprueba si un estado pertenece al autómata."""
        return estado in self.estados

    def es_estado_inicial(self, estado):
        """Comprueba si un estado es el estado inicial."""
        return estado == self.estado_inicial

    def obtener_estado_inicial(self):
        """Devuelve el estado inicial del autómata."""
        return self.estado_inicial

    def existe_transicion(self, origen, simbolo):
        """Comprueba si existe una transición desde un estado con un símbolo."""
        return simbolo in self.transiciones.get(origen, {})
    
    def obtener_alfabeto(self):
        """Devuelve una copia del alfabeto del autómata."""
        return self.alfabeto.copy()

    def obtener_transiciones(self, estado):
        """Devuelve las transiciones que salen de un estado."""
        return self.transiciones.get(estado, {}).copy()

    def obtener_estados_finales(self):
        """Devuelve una copia de los estados finales del autómata."""
        return self.estados_finales.copy()

    def obtener_estados(self):
        """Devuelve una copia de los estados del autómata."""
        return self.estados.copy()

    
    def tiene_estados(self):
        """Comprueba si el autómata tiene estados definidos."""
        return bool(self.estados)

    
    def tiene_alfabeto(self):
        """Comprueba si el autómata tiene símbolos definidos."""
        return bool(self.alfabeto)

    
    def tiene_estado_inicial(self):
        """Comprueba si el autómata tiene un estado inicial."""
        return self.estado_inicial is not None
    
    def existe_simbolo(self, simbolo):
        """Comprueba si un símbolo pertenece al alfabeto."""
        return simbolo in self.alfabeto

    
    def contar_simbolos(self):
        """Devuelve la cantidad de símbolos del alfabeto."""
        return len(self.alfabeto)
    
    def contar_estados_no_finales(self):
        """Devuelve la cantidad de estados que no son finales."""
        return len(self.estados - self.estados_finales)


