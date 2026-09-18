class SimuladorAFN:

    def __init__(self, afn):
        self.afn = afn

    def clausura_epsilon(self, estados):
        """
        Obtiene todos los estados que se pueden alcanzar
        utilizando únicamente transiciones epsilon.
        """

        resultado = set(estados)
        pendientes = list(estados)

        while pendientes:

            estado_actual = pendientes.pop()

            destinos = self.afn.obtener_destinos(
                estado_actual,
                "ε"
            )

            for destino in destinos:

                if destino not in resultado:
                    resultado.add(destino)
                    pendientes.append(destino)

        return resultado


    def mover(self, estados, simbolo):
        """
        Obtiene los estados a los que se puede llegar
        utilizando un determinado símbolo.
        """

        resultado = set()

        for estado in estados:

            destinos = self.afn.obtener_destinos(
                estado,
                simbolo
            )

            resultado.update(destinos)

        return resultado


    def simular(self, cadena):
        """
        Simula una cadena completa sobre el AFN.
        """

        if self.afn.estado_inicial is None:
            print("El AFN no tiene estado inicial.")
            return False

        # Comenzamos desde el estado inicial
        estados_actuales = {
            self.afn.estado_inicial
        }

        # Consideramos las transiciones epsilon iniciales
        estados_actuales = self.clausura_epsilon(
            estados_actuales
        )

        print("\n========== SIMULACIÓN ==========")

        print("Cadena:", cadena)

        print("Estado inicial:")
        print(estados_actuales)

        # Procesar cada símbolo
        for simbolo in cadena:

            print(f"\nProcesando símbolo: {simbolo}")

            # Verificar que el símbolo pertenece al alfabeto
            if simbolo not in self.afn.alfabeto:
                print(
                    f"El símbolo '{simbolo}' "
                    "no pertenece al alfabeto."
                )

                return False

            # Moverse utilizando el símbolo
            estados_actuales = self.mover(
                estados_actuales,
                simbolo
            )

            # Después del movimiento,
            # volvemos a aplicar clausura epsilon
            estados_actuales = self.clausura_epsilon(
                estados_actuales
            )

            print("Estados actuales:")
            print(estados_actuales)

            # Si no existen estados posibles,
            # la cadena ya no puede continuar
            if not estados_actuales:
                print("\nLa cadena no puede continuar.")
                print("Resultado: RECHAZADA")
                print("===============================\n")

                return False

        # Verificar si alguno de los estados actuales
        # es un estado final
        aceptada = bool(
            estados_actuales.intersection(
                self.afn.estados_finales
            )
        )

        print("\nEstados finales:")
        print(self.afn.estados_finales)

        if aceptada:
            print("\nResultado: ACEPTADA")
        else:
            print("\nResultado: RECHAZADA")

        print("===============================\n")

        return aceptada
