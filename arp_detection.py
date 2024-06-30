from scapy.all import ARP, Ether, srp  # Importa las funciones necesarias de Scapy para enviar y recibir paquetes ARP y Ethernet
import os  # Importa el módulo os para ejecutar comandos del sistema

def get_true_mac(ip):
    # Crea un paquete ARP para la IP de destino (router)
    arp_request = ARP(pdst=ip)
    # Crea un paquete Ethernet broadcast (envía a todas las MACs)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    # Combina los paquetes ARP y Ethernet
    arp_request_broadcast = broadcast / arp_request
    # Envía el paquete y recibe las respuestas
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    # Verifica si hay alguna respuesta
    if answered_list:
        # Retorna la dirección MAC de la primera respuesta
        return answered_list[0][1].hwsrc
    else:
        # Lanza una excepción si no hay respuestas
        raise Exception(f"No se recibió respuesta ARP para la IP {ip}")

def get_arp_table_entry(ip):
    # Ejecuta el comando 'arp -a' y lee la salida
    arp_table = os.popen("arp -a").read()
    # Recorre cada línea de la tabla ARP
    for line in arp_table.split('\n'):
        # Si la línea contiene la IP del router
        if ip in line:
            # Retorna la dirección MAC de la segunda columna
            return line.split()[1]
    # Retorna None si no se encuentra la IP en la tabla ARP
    return None

def main():
    # Pedir la IP del router al usuario
    gateway_ip = input("Introduce la IP del router: ")

    try:
        # Obtener la dirección MAC verdadera del router
        true_mac = get_true_mac(gateway_ip)
        print(f"Dirección MAC verdadera del router: {true_mac}")

        # Obtener la dirección MAC registrada en la tabla ARP
        arp_table_mac = get_arp_table_entry(gateway_ip)
        print(f"Dirección MAC en la tabla ARP: {arp_table_mac}")

        # Comparar las direcciones MAC
        if arp_table_mac is None:
            # No se encontró una entrada para el router en la tabla ARP
            print("No se encontró una entrada para el router en la tabla ARP.")
        elif true_mac == arp_table_mac:
            # La tabla ARP no ha sido modificada
            print("La tabla ARP no ha sido modificada. La dirección MAC del router es correcta.")
        else:
            # La tabla ARP ha sido modificada
            print("¡ALERTA! La tabla ARP ha sido modificada. La dirección MAC del router ha sido falsificada.")
    except Exception as e:
        # Maneja cualquier excepción que ocurra y la imprime
        print(f"Error: {e}")

if __name__ == "__main__":
    main()  # Llama a la función main() cuando se ejecuta el script
