from afn import AFN
from conversion import ConvertidorAFN_AFD
from simulador_afd import SimuladorAFD


# ==========================================
# CREAR AFN
# ==========================================

afn = AFN()

# Estados
afn.agregar_estado("q0")
afn.agregar_estado("q1")

# Alfabeto
afn.agregar_simbolo("a")
afn.agregar_simbolo("b")

# Estado inicial
afn.establecer_inicial("q0")

# Estado final
afn.agregar_final("q1")


# ==========================================
# TRANSICIONES DEL AFN
# ==========================================

afn.agregar_transicion("q0", "a", "q0")
afn.agregar_transicion("q0", "a", "q1")

afn.agregar_transicion("q0", "b", "q0")

afn.agregar_transicion("q1", "a", "q1")
afn.agregar_transicion("q1", "b", "q1")


# ==========================================
# CONVERTIR AFN → AFD
# ==========================================

convertidor = ConvertidorAFN_AFD(afn)

afd = convertidor.convertir()


# ==========================================
# MOSTRAR AFD
# ==========================================

print("\n")
print("########################################")
print("#        AFD GENERADO                  #")
print("########################################")

afd.mostrar()


# ==========================================
# CREAR SIMULADOR DEL AFD
# ==========================================

simulador = SimuladorAFD(afd)


# ==========================================
# PROBAR CADENAS
# ==========================================

simulador.simular("a")

simulador.simular("aa")

simulador.simular("ab")

simulador.simular("bbb")

simulador.simular("aab")
