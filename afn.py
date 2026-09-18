from automatas import Automata


class AFN(Automata):

    def __init__(self):
        super().__init__()

    def agregar_transicion(self, origen, simbolo, destino):
        """
        Agrega una transición al AFN.

        Un AFN puede tener varias transiciones:
        - Desde el mismo estado
        - Con el mismo símbolo
        - Hacia diferentes estados
        """

        super().agregar_transicion(origen, simbolo, destino)

    def obtener_destinos(self, estado, simbolo):
        """
        Obtiene todos los estados destino desde un estado
        utilizando un determinado símbolo.
        """

        if estado in self.transiciones:
            if simbolo in self.transiciones[estado]:
                return self.transiciones[estado][simbolo]

        return set()

    def mostrar_transiciones(self):
        """Muestra únicamente las transiciones del AFN."""

        print("\n========== TRANSICIONES DEL AFN ==========")

        if not self.transiciones:
            print("No existen transiciones.")
            return

        for origen, simbolos in self.transiciones.items():

            for simbolo, destinos in simbolos.items():

                for destino in destinos:
                    print(f"{origen} --{simbolo}--> {destino}")

        print("==========================================")
