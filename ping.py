import sys
import time
import logging

# Suprimimos las advertencias de Scapy para mantener la consola limpia
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

try:
    from scapy.all import IP, ICMP, send
except ImportError:
    print("Error: La librería 'scapy' no está instalada.")
    print("Por favor, instálela ejecutando: pip install scapy")
    sys.exit(1)

def cifrado_cesar(texto, desplazamiento):
    """Aplica el cifrado César manteniendo los espacios."""
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():
            if caracter.islower():
                resultado += chr((ord(caracter) - ord('a') + desplazamiento) % 26 + ord('a'))
            elif caracter.isupper():
                resultado += chr((ord(caracter) - ord('A') + desplazamiento) % 26 + ord('A'))
        else:
            resultado += caracter
    return resultado

def send_stealth_ping(mensaje_cifrado, destino="8.8.8.8"):
    """
    Envía caracteres individuales en paquetes ICMP Request de 48 bytes de Data.
    El caracter oculto se inserta en el primer byte del payload.
    """
    # Relleno de 47 bytes para simular el resto de un ping real de Linux.
    padding_base = b'\x60\x09\x00\x00\x00\x00\x00' + bytes(range(0x10, 0x38))
    
    for caracter in mensaje_cifrado:
        # El payload total será de 48 bytes: Nuestro carácter (1 byte) al inicio + el relleno (47 bytes)
        payload = caracter.encode('utf-8') + padding_base
        
        # Armamos el paquete IP y el ICMP (Type 8 es Echo Request)
        paquete = IP(dst=destino)/ICMP(type=8)/payload
        
        try:
            # Enviamos el paquete de forma silenciosa
            send(paquete, verbose=0)
            print("Sent 1 packets.")
            time.sleep(1)
        except PermissionError:
            print("\nError: Permisos insuficientes para enviar paquetes ICMP crudos.")
            print("Por favor, ejecute la consola (CMD o PowerShell) como Administrador.")
            sys.exit(1)

if __name__ == "__main__":
    # Verifica que se entreguen exactamente 2 argumentos (+ el nombre del script)
    if len(sys.argv) != 3:
        print("Uso: py ping.py \"<texto_en_claro>\" <desplazamiento>")
        sys.exit(1)

    texto_ingresado = sys.argv[1]
    
    try:
        desplazamiento_ingresado = int(sys.argv[2])
    except ValueError:
        print("Error: El desplazamiento debe ser un número entero.")
        sys.exit(1)

    # 1. Cifra el mensaje
    texto_cifrado = cifrado_cesar(texto_ingresado, desplazamiento_ingresado)
    print(f"Texto cifrado a enviar: {texto_cifrado}")
    
    # 2. Envía los pings sigilosos
    send_stealth_ping(texto_cifrado)