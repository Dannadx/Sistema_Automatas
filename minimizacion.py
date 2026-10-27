from automatas import Automata


class MinimizadorAFD:

    def __init__(self, afd):
        self.afd = afd

    def obtener_destino(self, estado, simbolo):
        """
        Obtiene el estado destino de una transición.
        Si no existe, devuelve 'TRAP' (estado sumidero virtual).
        """
        if estado == "TRAP":
            return "TRAP"

        if estado not in self.afd.transiciones:
            return "TRAP"

        if simbolo not in self.afd.transiciones[estado]:
            return "TRAP"

        destinos = self.afd.transiciones[estado][simbolo]

        if not destinos:
            return "TRAP"

        return next(iter(destinos))

    def minimizar(self):

        # Copiar los estados
        estados = list(self.afd.estados)

        # Si el AFD no tiene estados finales alcanzables (lenguaje vacío)
        if not self.afd.estados_finales:
            afd_minimo = Automata()
            for simbolo in self.afd.alfabeto:
                afd_minimo.agregar_simbolo(simbolo)

            estado_unico = "Q0"
            afd_minimo.agregar_estado(estado_unico)
            afd_minimo.establecer_inicial(estado_unico)

            for simbolo in self.afd.alfabeto:
                afd_minimo.agregar_transicion(estado_unico, simbolo, estado_unico)

            return afd_minimo

        if len(estados) <= 1:
            return self.afd

        # -----------------------------------------
        # PASO 1: Crear pares de estados
        # -----------------------------------------

        pares = []

        for i in range(len(estados)):
            for j in range(i + 1, len(estados)):
                pares.append((estados[i], estados[j]))

        # -----------------------------------------
        # PASO 2: Marcar pares donde uno es final y otro no
        # -----------------------------------------

        marcados = set()

        for estado1, estado2 in pares:
            final1 = estado1 in self.afd.estados_finales
            final2 = estado2 in self.afd.estados_finales

            if final1 != final2:
                marcados.add(frozenset([estado1, estado2]))

        # -----------------------------------------
        # PASO 3: Repetir hasta que no haya nuevos pares marcados
        # -----------------------------------------

        cambio = True

        while cambio:
            cambio = False

            for estado1, estado2 in pares:
                par = frozenset([estado1, estado2])

                if par in marcados:
                    continue

                for simbolo in self.afd.alfabeto:
                    destino1 = self.obtener_destino(estado1, simbolo)
                    destino2 = self.obtener_destino(estado2, simbolo)

                    if destino1 != destino2:
                        par_destinos = frozenset([destino1, destino2])

                        if par_destinos in marcados:
                            marcados.add(par)
                            cambio = True
                            break

        # -----------------------------------------
        # PASO 4: Crear grupos de estados equivalentes
        # -----------------------------------------

        grupos = []
        usados = set()

        for estado in estados:
            if estado in usados:
                continue

            grupo = {estado}

            for otro in estados:
                if otro == estado:
                    continue

                par = frozenset([estado, otro])

                if par not in marcados:
                    grupo.add(otro)

            grupos.append(grupo)
            usados.update(grupo)

        # -----------------------------------------
        # PASO 5: Crear nuevo AFD
        # -----------------------------------------

        afd_minimo = Automata()

        for simbolo in self.afd.alfabeto:
            afd_minimo.agregar_simbolo(simbolo)

        mapa_estado_a_nombre = {}

        for indice, grupo in enumerate(grupos):
            nombre_estado = f"Q{indice}"
            afd_minimo.agregar_estado(nombre_estado)

            for est in grupo:
                mapa_estado_a_nombre[est] = nombre_estado

        # -----------------------------------------
        # PASO 6: Estado inicial y finales
        # -----------------------------------------

        if self.afd.estado_inicial in mapa_estado_a_nombre:
            afd_minimo.establecer_inicial(mapa_estado_a_nombre[self.afd.estado_inicial])

        for estado in self.afd.estados_finales:
            if estado in mapa_estado_a_nombre:
                afd_minimo.agregar_final(mapa_estado_a_nombre[estado])

        # -----------------------------------------
        # PASO 7: Transiciones
        # -----------------------------------------

        for grupo in grupos:
            estado_rep = next(iter(grupo))
            origen_min = mapa_estado_a_nombre[estado_rep]

            for simbolo in self.afd.alfabeto:
                destino = self.obtener_destino(estado_rep, simbolo)

                if destino in mapa_estado_a_nombre:
                    destino_min = mapa_estado_a_nombre[destino]
                    afd_minimo.agregar_transicion(origen_min, simbolo, destino_min)

        return afd_minimo
