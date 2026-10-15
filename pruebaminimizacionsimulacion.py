from automatas import Automata
from minimizacion import MinimizadorAFD
from simulador_afd import SimuladorAFD


# ==========================================
# CREAR AFD ORIGINAL
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
# MINIMIZAR
# ==========================================

minimizador = MinimizadorAFD(afd)

afd_minimo = minimizador.minimizar()


# ==========================================
# CREAR SIMULADORES
# ==========================================

simulador_original = SimuladorAFD(afd)

simulador_minimo = SimuladorAFD(afd_minimo)


# ==========================================
# CADENAS DE PRUEBA
# ==========================================

cadenas = [
    "",
    "0",
    "1",
    "00",
    "01",
    "10",
    "11",
    "000",
    "001",
    "010",
    "011",
    "100",
    "101",
    "110",
    "111"
]


# ==========================================
# COMPARAR RESULTADOS
# ==========================================

print("\n")
print("############################################")
print("#     COMPARACIÓN AFD ORIGINAL / MÍNIMO    #")
print("############################################")


for cadena in cadenas:

    print("\n============================================")

    if cadena == "":
        print("Cadena: ε")
    else:
        print("Cadena:", cadena)

    print("\n--- AFD ORIGINAL ---")

    resultado_original = simulador_original.simular(
        cadena
    )

    print("\n--- AFD MINIMIZADO ---")

    resultado_minimo = simulador_minimo.simular(
        cadena
    )

    print("\n--------------------------------------------")

    if resultado_original == resultado_minimo:

        print("✓ RESULTADO IGUAL")

    else:

        print("✗ RESULTADO DIFERENTE")

    print("--------------------------------------------")
