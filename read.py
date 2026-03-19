import sys
try:
    from scapy.all import rdpcap, ICMP, Raw
except ImportError:
    print("Error: La librería 'scapy' no está instalada.")
    sys.exit(1)

# Códigos ANSI para imprimir en color verde en la consola
COLOR_VERDE = '\033[92m'
COLOR_RESET = '\033[0m'

def extraer_mensaje_pcap(archivo_pcap):
    """Lee el archivo pcapng y extrae el primer byte del campo Data de los ICMP request."""
    print(f"[*] Leyendo el archivo {archivo_pcap}...")
    try:
        paquetes = rdpcap(archivo_pcap)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        sys.exit(1)

    mensaje_extraido = ""
    for paquete in paquetes:
        # Buscamos paquetes ICMP tipo 8 (Echo Request) que contengan datos crudos (Raw)
        if paquete.haslayer(ICMP) and paquete[ICMP].type == 8 and paquete.haslayer(Raw):
            datos = paquete[Raw].load
            if len(datos) > 0:
                # Extraemos el primer byte y lo convertimos a carácter
                caracter = chr(datos[0])
                mensaje_extraido += caracter
                
    return mensaje_extraido

def descifrar_cesar(texto, desplazamiento):
    """Aplica la operación inversa del cifrado César."""
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():
            if caracter.islower():
                resultado += chr((ord(caracter) - ord('a') - desplazamiento) % 26 + ord('a'))
            elif caracter.isupper():
                resultado += chr((ord(caracter) - ord('A') - desplazamiento) % 26 + ord('A'))
        else:
            resultado += caracter
    return resultado

def evaluar_probabilidad(texto):
    """
    Evalúa qué tan probable es que el texto sea el mensaje en claro,
    buscando palabras comunes en español o relacionadas al contexto.
    """
    # Diccionario de palabras esperadas
    palabras_clave = ["y", "en", "de", "el", "la", "criptografia", "seguridad", "redes", "informacion"]
    puntaje = 0
    palabras_en_texto = texto.lower().split()
    
    for palabra in palabras_en_texto:
        if palabra in palabras_clave:
            puntaje += 1
    return puntaje

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: py readv2.py <archivo.pcapng>")
        sys.exit(1)

    archivo = sys.argv[1]
    
    # 1. Extraer el mensaje interceptado
    mensaje_cifrado = extraer_mensaje_pcap(archivo)
    
    if not mensaje_cifrado:
        print("No se encontraron paquetes ICMP con datos en el archivo.")
        sys.exit(1)
        
    print(f"[*] Mensaje interceptado: {mensaje_cifrado}\n")

    # Variables para identificar la mejor opción
    mejor_puntaje = 0
    mejor_desplazamiento = 0
    resultados = []

    # 2. Generar todas las combinaciones posibles (desplazamientos del 1 al 25)
    for i in range(1, 26):
        texto_prueba = descifrar_cesar(mensaje_cifrado, i)
        puntaje = evaluar_probabilidad(texto_prueba)
        
        resultados.append((i, texto_prueba, puntaje))
        
        # Actualizamos cuál es el mensaje con más sentido
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_desplazamiento = i

    # 3. Imprimir resultados resaltando la opción más probable
    for desplazamiento, texto, puntaje in resultados:
        # El formato imita la salida solicitada en el laboratorio: texto desplazamiento
        linea_salida = f"{texto} {desplazamiento}"
        
        if desplazamiento == mejor_desplazamiento and mejor_puntaje > 0:
            # Imprime en verde si es la opción ganadora
            print(f"{COLOR_VERDE}{linea_salida}{COLOR_RESET}")
        else:
            print(linea_salida)