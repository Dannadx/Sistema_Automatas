
from pathlib import Path
from regex_engine import compilar_regex


def analizar_logs(ruta_archivo, expresion):
    archivo = Path(ruta_archivo)

    if not archivo.is_file():
        raise FileNotFoundError("El archivo seleccionado no existe.")

    patron = compilar_regex(expresion)
    resultados = []

    with archivo.open("r", encoding="utf-8-sig", errors="replace") as archivo_log:
        for numero, linea in enumerate(archivo_log, start=1):
            linea = linea.rstrip("\r\n")

            coincidencias = list(patron.finditer(linea))

            if coincidencias:
                niveles = re_niveles(linea)

                resultados.append({
                    "linea": numero,
                    "nivel": niveles,
                    "contenido": linea,
                    "coincidencias": len(coincidencias)
                })

    return resultados


def re_niveles(linea):
    """Identifica el nivel habitual del registro."""
    import re

    niveles = re.findall(
        r"\b(CRITICAL|ERROR|WARNING|WARN|INFO|DEBUG)\b",
        linea,
        flags=re.IGNORECASE
    )

    if niveles:
        nivel = niveles[0].upper()
        return "WARNING" if nivel == "WARN" else nivel

    return "SIN CLASIFICAR"
