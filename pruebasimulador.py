from afn import AFN
from simulador import SimuladorAFN


# Crear AFN
afn = AFN()


# ==========================
# ESTADOS
# ==========================

afn.agregar_estado("q0")
afn.agregar_estado("q1")
afn.agregar_estado("q2")
afn.agregar_estado("q3")


# ==========================
# ALFABETO
# ==========================

afn.agregar_simbolo("0")
afn.agregar_simbolo("1")


# ==========================
# ESTADO INICIAL
# ==========================

afn.establecer_inicial("q0")


# ==========================
# ESTADO FINAL
# ==========================

afn.agregar_final("q3")


# ==========================
# TRANSICIONES
# ==========================

afn.agregar_transicion("q0", "0", "q0")
afn.agregar_transicion("q0", "0", "q1")

afn.agregar_transicion("q1", "1", "q2")

afn.agregar_transicion("q2", "0", "q3")

# Transición epsilon
afn.agregar_transicion("q0", "ε", "q2")


# ==========================
# SIMULADOR
# ==========================

simulador = SimuladorAFN(afn)


# ==========================
# PROBAR CADENAS
# ==========================

simulador.simular("010")

simulador.simular("11")

simulador.simular("0010")
