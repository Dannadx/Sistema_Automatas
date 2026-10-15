from automatas import Automata


class ConvertidorAFN_AFD:

    def __init__(self, afn):
        self.afn = afn

    def convertir(self):
        afd = Automata()

        # Copiar el alfabeto
        for simbolo in self.afn.alfabeto:
            afd.agregar_simbolo(simbolo)

        # Estado inicial del AFN
        estado_inicial_set = frozenset([self.afn.estado_inicial])

        # Mapeo de conjuntos (frozenset) a nombres amigables ("Q0", "Q1", ...)
        mapa_nombres = {}
        contador = 0

        nombre_inicial = f"Q{contador}"
        mapa_nombres[estado_inicial_set] = nombre_inicial
        contador += 1

        afd.agregar_estado(nombre_inicial)
        afd.establecer_inicial(nombre_inicial)

        pendientes = [estado_inicial_set]
        procesados = set()

        while pendientes:
            conjunto_actual = pendientes.pop()

            if conjunto_actual in procesados:
                continue

            procesados.add(conjunto_actual)
            nombre_origen = mapa_nombres[conjunto_actual]

            # Verificar si es estado final
            for estado in conjunto_actual:
                if estado in self.afn.estados_finales:
                    afd.agregar_final(nombre_origen)
                    break

            # Procesar transiciones para cada símbolo
            for simbolo in self.afn.alfabeto:
                destinos_set = set()

                for estado in conjunto_actual:
                    destinos = self.afn.obtener_destinos(estado, simbolo)
                    destinos_set.update(destinos)

                nuevo_conjunto = frozenset(destinos_set)

                # Si el conjunto no está en el mapa, le asignamos un nuevo nombre Q_n
                if nuevo_conjunto not in mapa_nombres:
                    nombre_nuevo = f"Q{contador}"
                    mapa_nombres[nuevo_conjunto] = nombre_nuevo
                    contador += 1
                    afd.agregar_estado(nombre_nuevo)

                nombre_destino = mapa_nombres[nuevo_conjunto]

                # Agregar transición en el AFD
                afd.agregar_transicion(nombre_origen, simbolo, nombre_destino)

                if nuevo_conjunto not in procesados:
                    pendientes.append(nuevo_conjunto)

        return afd
