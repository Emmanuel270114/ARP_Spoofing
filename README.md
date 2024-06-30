# ARP_Spoofing
Ataque a otra máquina virtual, por medio de ARP Spoofing.
Utilizando un programa, desarrollado en Python, realizamos la suplantación en la dirección MAC de nuestra victima
a la que le realizamos el ataque.

1.- Para realizar la ejecución, primero verificamos en ambas máquinas que direcciones IP hay con el comando:
                              arp -n o arp -a(Windows)

2.- Después, en la máquina principal, ejecutamos el programa de Python: arp_spoof.py
Ingresamos la IP de la máquina que será la victima y también la IP del Router

3.- Cuando se este ejecutando, verificamos en la maquina que esta siendo atacada si se realizó el cambio de dirección MAC,
con el comando:   arp -n o arp -a(Windows)

4.- En la máquina atacada, realizamos la ejecuación del segundo programa de Python: arp_detection.py
Para verificar si hay algun cambio.
