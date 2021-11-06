import socket
import des
import sys
from time import sleep
import call


# Pada fungsi ini akan bekerja sebagai client side
def Main():
        host = "127.0.0.1"
        port = 5001

        # melakukan penyambungan dengan socket menuju host dan port yang telah didefinisikan
        socketKu = socket.socket()
        socketKu.connect((host,port))
        
        pesan = input("Silahkan masukan pesan yang akan di enkripsi -> ")

        # Enkripsi pesan dengan DES
        pesanTerenkrip = call.encrypt(pesan)
        print("Pesan yang terenkripsi = " + pesanTerenkrip)

        # Perulangan infinite agar terus terhubung
        while pesan != 'q':

                # Menampilkan loading bar 
                call.sending()

                # Enkripsi pesan DES
                pesanTerenkrip = call.encrypt(pesan)
                # Mengirimkan pesan
                socketKu.send(pesanTerenkrip.encode())
                # Mendapatkan response dari user lain
                data = socketKu.recv(1024).decode()
                print("Received from server = " + data)
                #Melakukan decrypt pesan dari user lain
                pesanTerdekrip = call.decrypt(data)
                if not data:
                        break
                print ("Decrypted pesan = " + str(pesanTerdekrip))
                print("\n")
                # Persiapan untuk meminta pesan kepada user yang akan di enkripsi.
                pesan = input("Silahkan masukan pesan yang akan di enkripsi -> ")
                pesanTerenkrip = call.encrypt(pesan)
                print("Pesan yang dienkripsi = " + pesanTerenkrip)
                 
        socketKu.close()
 
if __name__ == '__main__':
    Main()
