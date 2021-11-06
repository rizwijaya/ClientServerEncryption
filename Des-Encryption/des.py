import sys


class DES:
    def __init__(self):

        self.key = "1001100111"
        # provided sbox 0
        self.s0 = [[1, 0, 3, 2],
                   [3, 2, 1, 0],
                   [0, 2, 1, 3],
                   [3, 1, 3, 2]]
        # provided sbox 1
        self.s1 = [[0, 1, 2, 3],
                   [2, 0, 1, 3],
                   [3, 0, 1, 0],
                   [2, 1, 0, 3]]
    
    def getSboxEntry(self, binary, sbox):

        # 1 dan indeks terakhir menunjukkan indeks baris sbox
        row = binary[0] + binary[3]
        # 2 dan indeks ke-3 menunjukkan indeks kolom dari sbox
        col = binary[1] + binary[2]
        # mengonversi dari string biner menjadi integer untuk keduanya
        row = int(row, 2)
        col = int(col, 2)
        if sbox == 0:
            binary = bin(self.s0[row][col])[2:]
            # pastikan itu bukan biner panjang 1
            if len(binary) == 1:
                binary = "0" + binary
            return binary
        else:
            binary = bin(self.s1[row][col])[2:]
            # pastikan itu bukan biner panjang 1y
            if len(binary) == 1:
                binary = "0" + binary
            return binary

    # mengembangkan kunci mereka dari 4 bit menjadi 8 bit
    def fFunction(self, key, k):
        # Perubahan dari 32 bit jadi 48 bit 
        expansion = key[3]+key[0]+key[1]+key[2]+key[1]+key[2]+key[3]+key[0]

        # XOR dengan key 8 bit 
        XOR = bin((int(expansion, 2) ^ int(k, 2)))[2:]
        XOR = self.padding(XOR, 8)

        left = XOR[:4]
        right = XOR[4:]

        # Lakukan pencocokan kembali terhadap sbox masing-masing
        S0 = self.getSboxEntry(left, 0)
        S1 = self.getSboxEntry(right, 1)

        # Penggabungan setelah sbox
        p4 = S0 + S1

        # Lakukan permutasi terhadap tabel P dari sbox tadi
        p4 = p4[1]+p4[3]+p4[2]+p4[0]

        return p4


    def kValueGenerator(self, key):
        # initial permuation
		# Permutasi awal
        newKey = key[2] + key[4] + key[1] + key[6] + \
            key[3] + key[9] + key[0] + key[8] + key[7] + key[5]

		# Membagi dua dari K awal menjadi C dan D
        left = newKey[0:5]
        right = newKey[5:]
        # Lakukan pergeseran shift ke kiri untuk key pertama
        leftShift = left[1:] + left[0]
        # Lakukan pergeseran shift ke kiri untuk key kedua
        rightShift = right[1:] + right[0]

        # Pembuatan K1 dengan menggabungkan antara pergeseran shift dengan permutassi
        k1 = leftShift + rightShift
        k1Permuted = k1[5] + k1[2] + k1[6] + \
            k1[3] + k1[7] + k1[4] + k1[9] + k1[8]

        # Menampilkan pergeseran kedua pada key pertama
        leftShiftTwice = leftShift[1:] + leftShift[0]
        # performing a second left shift on the second key
        rightShiftTwice = rightShift[1:] + rightShift[0]

        # Pembuatan K2 dengan menggabungkan antara pergeseran shift dengan permutasi
        k2 = leftShiftTwice + rightShiftTwice
        k2Permuted = k2[5] + k2[2] + k2[6] + \
            k2[3] + k2[7] + k2[4] + k2[9] + k2[8]

        # Meminta balikan K1 dan K2
        return(k1Permuted, k2Permuted)

    # Permutasi dari key asli 
    def initialPermutation(self, key):
        newKey = key[1] + key[5] + key[2] + \
            key[0] + key[3] + key[7] + key[4] + key[6]
        return newKey

    # Permutasi enkripsi kembali menuju permutasi asli
    def reversePermutation(self, key):
        newKey = key[3] + key[0] + key[2] + \
            key[4] + key[6] + key[1] + key[7] + key[5]
        return newKey

    # Fungsi yang berfungsi untuk menambahkan 0 di depan untuk melengkapi panjang dari biner
    # Contoh jika ada 4 biner yang diinginkan dan kita mendapat 101, maka seharusnya 0101
    def padding(self, string, length):
        if len(string) == length:
            return string
        while(len(string) < length):
            string = "0" + string
        return string

    # Fungsi yang menjalankan satu ronde enkripsi
    # Dengan keynya adalah 8 bit
    def Encryption(self, string):
        # Lakukan permutasi awal
        permString = self.initialPermutation(string)
        # Membagi dua dari K agar menjadi C dan D
        left = permString[0:4]
        right = permString[4:]
        k1, k2 = self.kValueGenerator(self.key)

        firstFOutput = self.fFunction(right, k1)

        # Melakukan XOR untuk C dan F(D,K1)
        firstXOR = bin((int(left, 2) ^ int(firstFOutput, 2)))[2:]
        firstXOR = self.padding(firstXOR, 4)
        secondFOutput = self.fFunction(firstXOR, k2)

        # Melakukan XOR untuk D dan F(XOR(C,F(D,K1)),K2)
        secondXOR = bin((int(right, 2) ^ int(secondFOutput, 2)))[2:]
        secondXOR = self.padding(secondXOR, 4)
        output = secondXOR + firstXOR

        # Permutasi berdasarkan tabel IP^-1
        output = self.reversePermutation(output)
        return output

    # Funsi untuk melakukan dekripsi
    def Decryption(self, string):
        # initial permutation
        permString = self.initialPermutation(string)
        # Membagi 2 strings 4 bit, A dan B
        left = permString[0:4]
        right = permString[4:]
        k1, k2 = self.kValueGenerator(self.key)

        firstFOutput = self.fFunction(right, k2)

        # Melakukan XORS A dan F(B,K1)
        firstXOR = bin((int(left, 2) ^ int(firstFOutput, 2)))[2:]
        firstXOR = self.padding(firstXOR, 4)
        secondFOutput = self.fFunction(firstXOR, k1)

        # Melakukan XORS B dan F(XOR(A,F(B,K1)),K2)
        secondXOR = bin((int(right, 2) ^ int(secondFOutput, 2)))[2:]
        secondXOR = self.padding(secondXOR, 4)
        output = secondXOR + firstXOR

        # Melakukan reverse the initial permutation
        output = self.reversePermutation(output)
        return output
