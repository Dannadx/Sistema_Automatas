"""
Conversión didáctica de Regex a AFN por Thompson y luego a AFD por subconjuntos.
Soporta: símbolos literales, concatenación, |, *, +, ?, paréntesis y escape con \\.
No soporta clases como [a-z], cuantificadores {m,n}, lookarounds ni clases \\d/\\w.
"""

EPSILON = "ε"
CONCAT = "·"

def tokenize(expression):
    if not expression:
        raise ValueError("Escribe una Regex para generar el autómata.")
    tokens = []
    i = 0
    while i < len(expression):
        ch = expression[i]
        if ch == "\\":
            i += 1
            if i >= len(expression):
                raise ValueError("La Regex termina con una barra invertida.")
            tokens.append(("LIT", expression[i]))
        elif ch.isspace():
            # Los espacios se consideran símbolos literales si se escapan;
            # los espacios sin escapar se ignoran para facilitar la escritura.
            pass
        elif ch in "()|*+?":
            tokens.append((ch, ch))
        else:
            tokens.append(("LIT", ch))
        i += 1
    return tokens

def to_postfix(expression):
    tokens = tokenize(expression)
    expanded = []
    atom_end = {"LIT", ")", "*", "+", "?"}
    atom_start = {"LIT", "("}
    for token in tokens:
        if expanded and expanded[-1][0] in atom_end and token[0] in atom_start:
            expanded.append((CONCAT, CONCAT))
        elif expanded and expanded[-1][0] in atom_end and token[0] == "(":
            expanded.append((CONCAT, CONCAT))
        elif expanded and expanded[-1][0] == ")" and token[0] in atom_start:
            expanded.append((CONCAT, CONCAT))
        expanded.append(token)

    output, stack = [], []
    precedence = {"|": 1, CONCAT: 2}
    for kind, value in expanded:
        if kind == "LIT":
            output.append(("LIT", value))
        elif kind == "(":
            stack.append(kind)
        elif kind == ")":
            while stack and stack[-1] != "(":
                output.append((stack.pop(), None))
            if not stack:
                raise ValueError("Paréntesis de cierre sin apertura.")
            stack.pop()
        elif kind in ("*", "+", "?"):
            output.append((kind, None))
        elif kind in ("|", CONCAT):
            while stack and stack[-1] != "(" and precedence.get(stack[-1], 0) >= precedence[kind]:
                output.append((stack.pop(), None))
            stack.append(kind)
        else:
            raise ValueError(f"Símbolo no reconocido: {value}")
    while stack:
        op = stack.pop()
        if op == "(":
            raise ValueError("Hay un paréntesis de apertura sin cerrar.")
        output.append((op, None))
    return output

class NFA:
    def __init__(self):
        self.transitions = {}
        self.start = None
        self.accept = None
        self.states = set()
        self.alphabet = set()

    def edge(self, src, symbol, dst):
        self.states.update((src, dst))
        self.transitions.setdefault((src, symbol), set()).add(dst)
        if symbol != EPSILON:
            self.alphabet.add(symbol)

def regex_to_nfa(expression):
    postfix = to_postfix(expression)
    nfa = NFA()
    stack = []
    next_state = 0

    def state():
        nonlocal next_state
        s = next_state
        next_state += 1
        nfa.states.add(s)
        return s

    for kind, value in postfix:
        if kind == "LIT":
            s, e = state(), state()
            nfa.edge(s, value, e)
            stack.append((s, e))
        elif kind == CONCAT:
            if len(stack) < 2:
                raise ValueError("Concatenación incompleta en la Regex.")
            b = stack.pop()
            a = stack.pop()
            nfa.edge(a[1], EPSILON, b[0])
            stack.append((a[0], b[1]))
        elif kind == "|":
            if len(stack) < 2:
                raise ValueError("Alternancia incompleta en la Regex.")
            b, a = stack.pop(), stack.pop()
            s, e = state(), state()
            nfa.edge(s, EPSILON, a[0])
            nfa.edge(s, EPSILON, b[0])
            nfa.edge(a[1], EPSILON, e)
            nfa.edge(b[1], EPSILON, e)
            stack.append((s, e))
        elif kind in ("*", "+", "?"):
            if not stack:
                raise ValueError(f"El operador {kind} no tiene un operando.")
            a = stack.pop()
            s, e = state(), state()
            nfa.edge(s, EPSILON, a[0])
            nfa.edge(a[1], EPSILON, e)
            if kind in ("*", "?"):
                nfa.edge(s, EPSILON, e)
            if kind in ("*", "+"):
                nfa.edge(a[1], EPSILON, a[0])
            stack.append((s, e))
    if len(stack) != 1:
        raise ValueError("La expresión no pudo interpretarse. Revisa operadores y paréntesis.")
    nfa.start, nfa.accept = stack[0]
    return nfa



def regex_to_core_afn(expression):
    """
    Construye el AFN de Thompson y lo adapta a la clase AFN de la Entrega 1.
    Así la conversión AFN->AFD y la minimización reutilizan los módulos existentes.
    """
    from afn import AFN

    construido = regex_to_nfa(expression)
    afn = AFN()
    nombres = {estado: f"r{estado}" for estado in construido.states}

    for estado in construido.states:
        afn.agregar_estado(nombres[estado])

    for simbolo in construido.alphabet:
        afn.agregar_simbolo(simbolo)

    afn.establecer_inicial(nombres[construido.start])
    afn.agregar_final(nombres[construido.accept])

    for (origen, simbolo), destinos in construido.transitions.items():
        for destino in destinos:
            afn.agregar_transicion(
                nombres[origen],
                simbolo,
                nombres[destino]
            )

    return construido, afn


def core_to_display_dfa(automata):
    """Adapta el AFD compartido a la estructura que dibuja REGEX LAB."""
    estados = sorted(automata.estados, key=lambda value: str(value))
    ids = {estado: indice for indice, estado in enumerate(estados)}
    transiciones = {}

    for origen, por_simbolo in automata.transiciones.items():
        for simbolo, destinos in por_simbolo.items():
            if destinos:
                destino = next(iter(destinos))
                if origen in ids and destino in ids:
                    transiciones[(ids[origen], simbolo)] = ids[destino]

    return {
        "states": list(range(len(estados))),
        "alphabet": sorted(automata.alfabeto),
        "start": ids.get(automata.estado_inicial, 0),
        "accepting": {ids[e] for e in automata.estados_finales if e in ids},
        "transitions": transiciones,
        "state_names": {ids[e]: str(e) for e in estados}
    }


def transition_lines(dfa):
    """Devuelve las transiciones del AFD para mostrarlas en la interfaz."""
    return [
        f"q{origen} -- {simbolo} --> q{destino}"
        for (origen, simbolo), destino in sorted(
            dfa["transitions"].items(),
            key=lambda item: (item[0][0], item[0][1])
        )
    ]
