from automatas import Automata


class SimuladorAFD:

    def __init__(self, afd):
        self.afd = afd
<<<<<<< HEAD
        self.estado_actual = None
=======

>>>>>>> 0d75773174ba9944bdb0e0a0628d4ee225272967
    def simular(self, cadena):
        """
        Simula una cadena sobre el AFD.
        """
        if self.afd.estado_inicial is None:
            print("El AFD no tiene estado inicial.")
            return False
        estado_actual = self.afd.estado_inicial
<<<<<<< HEAD
        self.estado_actual = estado_actual 
=======

>>>>>>> 0d75773174ba9944bdb0e0a0628d4ee225272967
        print("\n========== SIMULACIÓN AFD ==========")
        print("Cadena:", cadena)
        print("\nEstado inicial:")
        print(estado_actual)
        # Procesar cada símbolo de la cadena
        for simbolo in cadena:
            print(f"\nProcesando símbolo: {simbolo}")
            # Verificar que el símbolo pertenece al alfabeto
            if simbolo not in self.afd.alfabeto:
                print(
                    f"El símbolo '{simbolo}' "
                    "no pertenece al alfabeto."
                )
                print("Resultado: RECHAZADA")
                print("====================================\n")

                return False

            # Verificar si existe una transición
            if estado_actual not in self.afd.transiciones:
                print("No existe una transición.")
                print("Resultado: RECHAZADA")
                print("====================================\n")

                return False

            if simbolo not in self.afd.transiciones[estado_actual]:
                print(
                    f"No existe transición para "
                    f"{estado_actual} con '{simbolo}'."
                )

                print("Resultado: RECHAZADA")
                print("====================================\n")

                return False

            # Obtener el siguiente estado
            destinos = self.afd.transiciones[
                estado_actual
            ][simbolo]

            # Como es un AFD, solamente existe un destino
            estado_actual = next(iter(destinos))

            print("Estado actual:")
            print(estado_actual)

        # Verificar si el estado final es aceptado
        print("\nEstado donde terminó:")
        print(estado_actual)

        print("\nEstados finales:")
        print(self.afd.estados_finales)

        if estado_actual in self.afd.estados_finales:

            print("\nResultado: ACEPTADA")

            print("====================================\n")

            return True

        else:

            print("\nResultado: RECHAZADA")

            print("====================================\n")

            return False
