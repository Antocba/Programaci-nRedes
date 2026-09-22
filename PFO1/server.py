import socket
import sqlite3
import sys
from datetime import datetime

def inicializar_db():
    # Crea la tabla si no existe
    conexion = sqlite3.connect("chat.db")
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenido TEXT NOT NULL,
            fecha_envio TEXT NOT NULL,
            ip_cliente TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

def guardar_mensaje(contenido, ip):
    # coloca el mensaje en la BD (con manejo de errores) 
    try:
        conexion = sqlite3.connect("chat.db")
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conexion.execute("INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)", (contenido, fecha, ip))
        conexion.commit()
        conexion.close()
    except sqlite3.Error as e:
        print(f"Error DB: {e}")

def iniciar_socket():
    # Configuración del socket TCP/IP (IPv4 + TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # socket en localhost:5000
        s.bind(("localhost", 5000))
    except OSError as e:
        # Manejo de error: puerto ocupado
        print(f"Puerto ocupado: {e}")
        sys.exit(1)
    s.listen(3)  # cola de espera
    print("Servidor escuchando en localhost:5000...")
    return s

def main():
    inicializar_db()
    s = iniciar_socket()

    while True:
        # accept() espera hasta que cliente se conecte
        conn, addr = s.accept()
        ip = addr[0]
        print(f"Cliente conectado: {ip}")

        while True:
            try:
                datos = conn.recv(1024)
            except ConnectionError:
                # cliente cortó conexión
                break
            if not datos:
                break
            mensaje = datos.decode("utf-8")
            guardar_mensaje(mensaje, ip)
            conn.send(f"Mensaje recibido: {mensaje}".encode("utf-8"))

        conn.close()
        print(f"Cliente desconectado: {ip}")

if __name__ == "__main__":
    main()