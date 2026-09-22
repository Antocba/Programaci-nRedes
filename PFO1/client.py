import socket

def main():
    # se conecta al servidor
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 5000))
    print("Conectado. Escribí 'éxito' para salir.")

    while True:
        mensaje = input("Mensaje: ")
        s.send(mensaje.encode("utf-8"))
        if mensaje.lower() == "éxito":  # corta conexión
            break
        print("Servidor:", s.recv(1024).decode("utf-8"))

    s.close()

if __name__ == "__main__":
    main()