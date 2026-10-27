from automatas import Automata


class ConvertidorAFN_AFD:
    """Convierte un AFN en AFD mediante construcción por subconjuntos.
    Incluye clausura-ε para admitir transiciones epsilon correctamente.
    """

    def __init__(self, afn):
        self.afn = afn

    def clausura_epsilon(self, estados):
        resultado = set(estados)
        pendientes = list(estados)

        while pendientes:
            actual = pendientes.pop()
            destinos = self.afn.obtener_destinos(actual, "ε")
            for destino in destinos:
                if destino not in resultado:
                    resultado.add(destino)
                    pendientes.append(destino)

        return resultado

    def convertir(self):
        afd = Automata()

        for simbolo in self.afn.alfabeto:
            afd.agregar_simbolo(simbolo)

        if self.afn.estado_inicial is None:
            raise ValueError("El AFN no tiene un estado inicial.")

        estado_inicial_set = frozenset(
            self.clausura_epsilon({self.afn.estado_inicial})
        )

        mapa_nombres = {estado_inicial_set: "Q0"}
        afd.agregar_estado("Q0")
        afd.establecer_inicial("Q0")

        pendientes = [estado_inicial_set]
        procesados = set()
        contador = 1

        while pendientes:
            conjunto_actual = pendientes.pop(0)

            if conjunto_actual in procesados:
                continue
            procesados.add(conjunto_actual)

            nombre_origen = mapa_nombres[conjunto_actual]

            if any(
                estado in self.afn.estados_finales
                for estado in conjunto_actual
            ):
                afd.agregar_final(nombre_origen)

            for simbolo in sorted(self.afn.alfabeto):
                destinos = set()

                for estado in conjunto_actual:
                    destinos.update(
                        self.afn.obtener_destinos(estado, simbolo)
                    )

                nuevo_conjunto = frozenset(
                    self.clausura_epsilon(destinos)
                )

                if nuevo_conjunto not in mapa_nombres:
                    nombre_nuevo = f"Q{contador}"
                    contador += 1
                    mapa_nombres[nuevo_conjunto] = nombre_nuevo
                    afd.agregar_estado(nombre_nuevo)
                    pendientes.append(nuevo_conjunto)

                afd.agregar_transicion(
                    nombre_origen,
                    simbolo,
                    mapa_nombres[nuevo_conjunto]
                )

        return afd
