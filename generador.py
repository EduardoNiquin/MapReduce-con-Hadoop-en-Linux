import random

string = ""
while 10000 > len(string):
    frutas = ["manzana", "platano", "cereza", "durazno", "pera", "uva", "melon", "naranja", "kiwi", "limon"]
    # selecciona al azar un número entre 0 y 9 incluyendo 9.
    numero = random.randint(0, 9)
    # añade la fruta al string y salto de línea.
    string += frutas[numero]
    string += "\n"
print(string)
string = string[:-1]

# guardar el string en un archivo llamado frutas.txt.
with open("frutas.txt", "w") as f:
    f.write(string)