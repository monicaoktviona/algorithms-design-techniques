# Nama: Monica Oktaviona
# NPM: 2106701210
# Kode Asdos: 4
# Kelas: C
# Desain dan Analisis Algoritma
# Semester Ganjil 2023/2024

import random
import os.path

def generate_data(num):
    """
    Fungsi untuk men-generate dataset secara random pasangan weight dan value 
    yang dipisahkann dengan spasi dan menyimpannya dalam file .txt.

    Baris pertama dalam file yang digenerate adalah header.
    """
    file_path = os.path.join("./dataset/", str(num) + ".txt")         
    file = open(file_path, "a")
    file.write("{:<10}{:<10}\n".format("Weight", "Value"))  # dataset header
    for i in range(0, num):
        weight = random.randint(1, 100)
        value = random.randint(1, 100)
        file.write("{:>6}{:<4}{:<10}".format(weight, "", value))
        if i != (num - 1):
            file.write("\n")
    file.close()
    print(str(num) + " data succesfully generated.")

if __name__ == '__main__':
    size = [100, 1000, 10000]     # list of size dari dataset yang ingin digenerate

    for i in range(0, len(size)):
        generate_data(size[i])

