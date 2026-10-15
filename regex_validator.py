
import re


def validar_regex(expresion):
    """Comprueba si la expresión regular tiene una sintaxis válida."""
    try:
        re.compile(expresion)
        return True, "Expresión regular válida."
    except re.error as error:
        return False, f"Error en la expresión regular: {error}"


def validar_cadena(expresion, cadena):
    """Valida toda la cadena, no solamente una parte."""
    try:
        patron = re.compile(expresion)
        return patron.fullmatch(cadena) is not None
    except re.error:
        return False


def probar_cadenas(expresion, cadenas):
    """Devuelve el resultado de cada cadena."""
    resultados = []

    for cadena in cadenas:
        resultados.append({
            "cadena": cadena,
            "valida": validar_cadena(expresion, cadena)
        })

    return resultados
