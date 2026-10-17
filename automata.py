"""
Conversión didáctica de Regex a AFN por Thompson y luego a AFD por subconjuntos.
Soporta: símbolos literales, concatenación, |, *, +, ?, paréntesis y escape con \\.
No soporta clases como [a-z], cuantificadores {m,n}, lookarounds ni clases \\d/\\w.
"""
#CODIGO INICIAL 
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

def epsilon_closure(nfa, states):
    result = set(states)
    pending = list(states)
    while pending:
        current = pending.pop()
        for nxt in nfa.transitions.get((current, EPSILON), set()):
            if nxt not in result:
                result.add(nxt)
                pending.append(nxt)
    return frozenset(result)

def move(nfa, states, symbol):
    result = set()
    for s in states:
        result.update(nfa.transitions.get((s, symbol), set()))
    return result
#funcion alfabeto
def nfa_to_dfa(nfa):
    alphabet = sorted(nfa.alphabet)
    start = epsilon_closure(nfa, {nfa.start})
    states = [start]
    ids = {start: 0}
    transitions = {}
    pending = [start]
    accepting = set()

    while pending:
        current = pending.pop(0)
        cid = ids[current]
        if nfa.accept in current:
            accepting.add(cid)
        for symbol in alphabet:
            target = epsilon_closure(nfa, move(nfa, current, symbol))
            if not target:
                continue
            if target not in ids:
                ids[target] = len(states)
                states.append(target)
                pending.append(target)
            transitions[(cid, symbol)] = ids[target]

    return {
        "states": list(range(len(states))),
        "alphabet": alphabet,
        "start": 0,
        "accepting": accepting,
        "transitions": transitions,
        "subsets": states
    }

def minimize_dfa(dfa):
    """Minimización por refinamiento de particiones; conserva estados alcanzables."""
    states = set(dfa["states"])
    alphabet = dfa["alphabet"]
    accepting = set(dfa["accepting"])
    nonaccepting = states - accepting
    partitions = [p for p in (accepting, nonaccepting) if p]
    changed = True

    while changed:
        changed = False
        new_partitions = []
        for group in partitions:
            buckets = {}
            for state in group:
                signature = []
                for symbol in alphabet:
                    target = dfa["transitions"].get((state, symbol))
                    target_group = next(
                        (i for i, part in enumerate(partitions) if target in part),
                        -1
                    )
                    signature.append(target_group)
                buckets.setdefault(tuple(signature), set()).add(state)
            new_partitions.extend(buckets.values())
            if len(buckets) > 1:
                changed = True
        partitions = new_partitions

    state_to_group = {}
    for i, group in enumerate(partitions):
        for state in group:
            state_to_group[state] = i

    transitions = {}
    for i, group in enumerate(partitions):
        representative = next(iter(group))
        for symbol in alphabet:
            target = dfa["transitions"].get((representative, symbol))
            if target is not None:
                transitions[(i, symbol)] = state_to_group[target]

    return {
        "states": list(range(len(partitions))),
        "alphabet": alphabet,
        "start": state_to_group[dfa["start"]],
        "accepting": {state_to_group[s] for s in accepting},
        "transitions": transitions,
        "subsets": [sorted(group) for group in partitions]
    }

def validate_with_dfa(dfa, text):
    state = dfa["start"]
    for symbol in text:
        target = dfa["transitions"].get((state, symbol))
        if target is None:
            return False
        state = target
    return state in dfa["accepting"]

def transition_lines(dfa):
    lines = []
    for (src, symbol), dst in sorted(dfa["transitions"].items()):
        lines.append(f"q{src} -- {symbol} --> q{dst}")
    return lines
