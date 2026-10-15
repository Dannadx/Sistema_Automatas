from automatas import Automata


automata = Automata()

# Agregar estados
automata.agregar_estado("q0")
automata.agregar_estado("q1")
automata.agregar_estado("q2")

# Agregar símbolos
automata.agregar_simbolo("0")
automata.agregar_simbolo("1")

# Establecer estado inicial
automata.establecer_inicial("q0")

# Agregar estado final
automata.agregar_final("q2")

# Agregar transiciones
automata.agregar_transicion("q0", "0", "q1")
automata.agregar_transicion("q1", "1", "q2")

# Mostrar el autómata
automata.mostrar()
