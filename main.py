from afn import AFN
from conversion import ConvertidorAFN_AFD
from minimizacion import MinimizadorAFD
from simulador import SimuladorAFN
from simulador_afd import SimuladorAFD


def mostrar_menu():

    print("\n")
    print("==========================================")
    print("       SISTEMA DE AUTÓMATAS FINITOS       ")
    print("==========================================")
    print("1. Crear AFN")
    print("2. Mostrar AFN")
    print("3. Convertir AFN → AFD")
    print("4. Minimizar AFD")
    print("5. Simular cadena en AFN")
    print("6. Simular cadena en AFD")
    print("7. Mostrar AFD")
    print("8. Mostrar AFD minimizado")
    print("9. Salir")
    print("==========================================")


# Variables principales

afn = None
afd = None
afd_minimo = None


# Programa principal

while True:

    mostrar_menu()

    opcion = input("Seleccione una opción: ")

    # --------------------------------------
    # OPCIÓN 1
    # --------------------------------------

    if opcion == "1":

        afn = AFN()

        print("\nAFN creado correctamente.")

    # --------------------------------------
    # OPCIÓN 2
    # --------------------------------------

    elif opcion == "2":

        if afn is None:

            print("\nPrimero debe crear un AFN.")

        else:

            afn.mostrar()

    # --------------------------------------
    # OPCIÓN 3
    # --------------------------------------

    elif opcion == "3":

        if afn is None:

            print("\nPrimero debe crear un AFN.")

        else:

            convertidor = ConvertidorAFN_AFD(afn)

            afd = convertidor.convertir()

            print("\nAFN convertido correctamente a AFD.")

    # --------------------------------------
    # OPCIÓN 4
    # --------------------------------------

    elif opcion == "4":

        if afd is None:

            print("\nPrimero debe convertir un AFN a AFD.")

        else:

            minimizador = MinimizadorAFD(afd)

            afd_minimo = minimizador.minimizar()

            print("\nAFD minimizado correctamente.")

    # --------------------------------------
    # OPCIÓN 5
    # --------------------------------------

    elif opcion == "5":

        if afn is None:

            print("\nPrimero debe crear un AFN.")

        else:

            cadena = input(
                "\nIngrese la cadena a simular: "
            )

            simulador = SimuladorAFN(afn)

            simulador.simular(cadena)

    # --------------------------------------
    # OPCIÓN 6
    # --------------------------------------

    elif opcion == "6":

        if afd is None:

            print("\nPrimero debe convertir el AFN a AFD.")

        else:

            cadena = input(
                "\nIngrese la cadena a simular: "
            )

            simulador = SimuladorAFD(afd)

            simulador.simular(cadena)

    # --------------------------------------
    # OPCIÓN 7
    # --------------------------------------

    elif opcion == "7":

        if afd is None:

            print("\nPrimero debe convertir el AFN a AFD.")

        else:

            afd.mostrar()

    # --------------------------------------
    # OPCIÓN 8
    # --------------------------------------

    elif opcion == "8":

        if afd_minimo is None:

            print("\nPrimero debe minimizar el AFD.")

        else:

            afd_minimo.mostrar()

    # --------------------------------------
    # OPCIÓN 9
    # --------------------------------------

    elif opcion == "9":

        print("\nPrograma finalizado.")

        break

    # --------------------------------------
    # OPCIÓN INCORRECTA
    # --------------------------------------

    else:

        print("\nOpción no válida.")
