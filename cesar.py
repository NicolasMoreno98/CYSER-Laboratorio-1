import sys

def cifrado_cesar(texto, desplazamiento):
    resultado = ""
    for caracter in texto:
        # Verifica si el caracter es una letra
        if caracter.isalpha():
            # Manejo de letras minúsculas (basado en tu ejemplo)
            if caracter.islower():
                # Calcula la nueva posición en el alfabeto (0-25) y vuelve a ASCII
                resultado += chr((ord(caracter) - ord('a') + desplazamiento) % 26 + ord('a'))
            # Manejo de letras mayúsculas (por si acaso)
            elif caracter.isupper():
                resultado += chr((ord(caracter) - ord('A') + desplazamiento) % 26 + ord('A'))
        else:
            # Si no es letra (como los espacios), lo deja igual
            resultado += caracter
    return resultado

if __name__ == "__main__":
    # Verifica que se entreguen exactamente 2 argumentos (+ el nombre del script)
    if len(sys.argv) != 3:
        print("Uso: sudo python3 cesar.py \"<texto_a_cifrar>\" <desplazamiento>")
        sys.exit(1)

    texto_ingresado = sys.argv[1]
    
    try:
        desplazamiento_ingresado = int(sys.argv[2])
    except ValueError:
        print("Error: El desplazamiento debe ser un número entero.")
        sys.exit(1)

    # Llama a la función e imprime el resultado
    texto_cifrado = cifrado_cesar(texto_ingresado, desplazamiento_ingresado)
    print(texto_cifrado)