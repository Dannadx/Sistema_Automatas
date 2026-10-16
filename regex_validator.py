import re


def compilar_regex(expresion):
    """Compila la expresión regular y detecta errores."""
    try:
        return re.compile(expresion)
    except re.error as error:
        raise ValueError(f"Expresión regular inválida: {error}")


def validar_cadena(expresion, cadena):
    """Valida si toda la cadena cumple la expresión regular."""
    patron = compilar_regex(expresion)
    return patron.fullmatch(cadena) is not None


def buscar_coincidencias(expresion, texto):
    """Busca todas las coincidencias dentro de un texto."""
    patron = compilar_regex(expresion)
    return [
        {
            "texto": coincidencia.group(),
            "inicio": coincidencia.start(),
            "fin": coincidencia.end()
        }
        for coincidencia in patron.finditer(texto)
    ]


def obtener_informacion(expresion):
    """Devuelve información básica de la expresión."""
    patron = compilar_regex(expresion)

    return {
        "expresion": expresion,
        "longitud": len(expresion),
        "flags": patron.flags
    }

