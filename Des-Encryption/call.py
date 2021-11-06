import des
from time import sleep
import sys 

# fungsi yang mengkonveri biner ke ASCII
def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

# fungsi yang mengkonveri ASCII ke biner
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

# fungsi yang diberi string dengan panjang n dan panjang tertentu m
# dan mengembalikan sebuah list substring panjang m
def splitIntoGroups(string,length):
    results = []
    loc = 0
    temp = ""
    while(loc < len(string)):
        temp += string[loc]
        loc += 1
        if loc % length == 0:
            results.append(temp)
            temp = ""
    return results

# fungsi yang mengambil biner ter-enkripsi dan mengubahnya menjadi teks didekripsi
def decrypt(message):
    # memanggil class DES
    toy = des.DES()
    # membagi biner menjadi potongan 8-bit (diperlukan untuk class DES) 
    entries = splitIntoGroups(message,8)
    decryptedMessages = []
    # men-dekripsi masing-masing potongan 
    for i in range(len(entries)):
        decryption = toy.Decryption(entries[i])
        decryptedMessages.append(decryption)
    # menggabungkan dekripsi
    decryptedMessage ="".join(decryptedMessages)
    # mengubah dari biner ke ASCII
    decryptedMessage = text_from_bits(decryptedMessage)
    return decryptedMessage

# fungsi yang mengambil teks ASCII dan mengubahnya menjadi biner terenkripsi
def encrypt(message):
    # memanggil class DES
    toy = des.DES()
    # mengubah ASCII ke biner
    binary = text_to_bits(message)
    # membagi biner menjadi potongan 8-bit (diperlukan untuk class DES) 

    entries = splitIntoGroups(binary,8)

    encryptedEntries = []
    # meng-enkripsi masing-masing potongan
    for i in range(len(entries)):
        encryptedMessage = toy.Encryption(entries[i])
        encryptedEntries.append(encryptedMessage)
    # menggabungkan enkripsi
    finalEncryptedMessage = "".join(encryptedEntries)
    return finalEncryptedMessage

#fungsi yang mecetak loading bar untuk mengirim pesan
def sending():
    print("\nSending ",end = "")
    for j in range(5):
        sleep(0.4)
        print(".", end = "")
        sys.stdout.flush()
    print(' SENT')