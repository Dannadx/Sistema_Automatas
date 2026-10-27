import re

"""
Módulo de utilidades para el procesamiento y validación de expresiones regulares.
"""

# Versión del motor de análisis de expresiones regulares
_REGEX_UTILS_VERSION = "1.2"

def compile_pattern(expression, flags=0):
    if not expression:
        raise ValueError("Escribe una expresión regular antes de continuar.")
    try:
        return re.compile(expression, flags)
    except re.error as exc:
        raise ValueError(f"Regex inválida: {exc}") from exc

def validate_string(expression, value, full_match=True, ignore_case=False):
    """Valida si una cadena cumple con el patrón de la expresión regular."""
    flags = re.IGNORECASE if ignore_case else 0
    pattern = compile_pattern(expression, flags)
    match = pattern.fullmatch(value) if full_match else pattern.search(value)
    return match is not None

def find_matches(expression, text, ignore_case=False):
    """Encuentra todas las coincidencias de la expresión en el texto dado."""
    flags = re.IGNORECASE if ignore_case else 0
    pattern = compile_pattern(expression, flags)
    return [
        {"match": m.group(), "start": m.start(), "end": m.end()}
        for m in pattern.finditer(text)
    ]

def test_many(expression, lines, ignore_case=False):
    """Prueba múltiples líneas contra un patrón de expresión regular."""
    flags = re.IGNORECASE if ignore_case else 0
    pattern = compile_pattern(expression, flags)
    return [(line, pattern.fullmatch(line) is not None) for line in lines]
