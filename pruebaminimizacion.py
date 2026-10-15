from automatas import Automata
from minimizacion import MinimizadorAFD


# ==========================================
# CREAR AFD
# ==========================================

afd = Automata()


# Estados
afd.agregar_estado("A")
afd.agregar_estado("B")
afd.agregar_estado("C")
afd.agregar_estado("D")


# Alfabeto
afd.agregar_simbolo("0")
afd.agregar_simbolo("1")


# Estado inicial
afd.establecer_inicial("A")


# Estado final
afd.agregar_final("D")


# ==========================================
# TRANSICIONES
# ==========================================

afd.agregar_transicion("A", "0", "B")
afd.agregar_transicion("A", "1", "C")

afd.agregar_transicion("B", "0", "B")
afd.agregar_transicion("B", "1", "D")

afd.agregar_transicion("C", "0", "B")
afd.agregar_transicion("C", "1", "D")

afd.agregar_transicion("D", "0", "D")
afd.agregar_transicion("D", "1", "D")


# ==========================================
# MOSTRAR AFD ORIGINAL
# ==========================================

print("\n")
print("########################################")
print("#          AFD ORIGINAL                #")
print("########################################")

afd.mostrar()


# ==========================================
# MINIMIZAR
# ==========================================

minimizador = MinimizadorAFD(afd)

afd_minimo = minimizador.minimizar()


# ==========================================
# MOSTRAR AFD MINIMIZADO
# ==========================================

print("\n")
print("########################################")
print("#          AFD MINIMIZADO              #")
print("########################################")

afd_minimo.mostrar()
