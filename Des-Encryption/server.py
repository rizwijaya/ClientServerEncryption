import socket
import des
import call

# Berfungsi sebagai "server" untuk implementasi

def Main():
    host = "127.0.0.1"
    port = 5001
    # Diperlukan untuk menginisiasi server
    socketKu = socket.socket()
    socketKu.bind((host,port))

    print("Menunggu sambungan .....")
    # Mendengarkan user untuk terhubung
    socketKu.listen(2)
    # Mendapatkan informasi koneksi user
    conn, addr = socketKu.accept()
    print ("Sambungan dari : " + str(addr))

    while True:
            # Menerima respon dari user lain
            data = conn.recv(1024).decode()
            print("Pesan yang diterima dari klien  = " + data)
            # Men-dekripsi pesan user lain
            pesanTerdekrip = call.decrypt(data)
            if not data:
                    break
            print ("Pesan yang telah di dekripsi = " + str(pesanTerdekrip))
            print("\n")
            pesan = input("Silahkan masukan pesan yang akan di enkripsi -> ")
            # Meng-enkripsi pesan menggunakan DES
            pesanTerenkrip = call.encrypt(pesan)
            print("Pesan yang dienkripsi = " + pesanTerenkrip)
            # Print loading bar
            call.sending()
            # Mengirim pesan
            conn.send(pesanTerenkrip.encode())
 
    conn.close()
     
if __name__ == '__main__':
    Main()





