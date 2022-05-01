import socket
import sys
import time
from threading import Thread

from essential_generators import DocumentGenerator


def client(client_socket, addr):
    word_generator = DocumentGenerator()
    try:
        while True:
            data = word_generator.sentence() + "\n"
            client_socket.send(data.encode())
            time.sleep(0.5)
    except:
        conn.close()


if __name__ == "__main__":

    s = socket.socket()
    s.bind(("", 9999))
    s.listen(5)

    print("Servidor rodando..." + str(time.time()))

    while True:
        try:
            conn, addr = s.accept()
            print("Conexao estabelecida com: ", addr)
            t = Thread(target=client, args=(conn, addr))
            t.start()

        except KeyboardInterrupt:
            s.close()

        except:
            e = sys.exc_info()[0]
            print("Erro: %s" % e)
