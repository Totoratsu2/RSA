import numpy as np
from cryptoRSA import *


def continuar() -> bool:
    flag = input("\nDesea continuar? [S,n]: ")

    return False if flag.lower() == "n" else True


def menu() -> int:
    opt = 0
    while opt not in range(1, 6):
        print("\n===== MENU DE OPCIONES =====")
        print("1. Generar par de llaves")
        print("2. Encriptar mensaje")
        print("3. Desencriptar mensaje")
        print("4. Salir")

        try:
            opt = int(input("\nIngrese una opción: "))

            if opt not in range(1, 6):
                print("\nERROR: OPCIÓN NO VÁLIDA")
        except:
            print("\nERROR: OPCIÓN NO VÁLIDA")

    return opt


def main():
    opcion = 0
    while opcion != 4:
        opcion = menu()

        if opcion == 1:
            llaves = genParLlaves()
            print("Privada: ", *llaves[0], "\nPublica:", *llaves[1], "\n")

            if not continuar():
                break

            print("\n")
        elif opcion == 2:
            mensaje = input("Ingresa mensaje: ")
            n, e = list(map(np.int64, input(
                "Ingrese n y e separados por espacios: ").rstrip().split()))

            print("Mensaje encriptado:", *encriptar(mensaje, e, n))

            if not continuar():
                break

            print("\n")
        elif opcion == 3:
            mensaje = np.array(list(map(np.int64, input(
                "Ingrese lista de letras encriptadas separadas por espacios: ").rstrip().split())))
            n, d = list(map(np.int64, input(
                "Ingrese n y d separados por espacios: ").rstrip().split()))

            print(f"Mensaje encriptado:", desencriptar(mensaje, d, n), "\n")
            if not continuar():
                break

            print("\n")


if __name__ == '__main__':
    main()
