import pymongo
import csv

print("connect to db")
myclient = pymongo.MongoClient(
    "mongodb://puskesmas:puskesmba@localhost:27017/puskesmas")
mydb = myclient["puskesmas"]
tabel = mydb["Pasien"]

pasien = tabel.find({})

print("reading data")
data = []
for p in pasien:
    data.append(p['nomor']+' '+p['tanggal_lahir']+' '+p['jenis_kelamin'])

print("saving data")
print(data)
with open('files/pasien.txt', 'w') as file:
    writer = csv.writer(file)
    for d in data:
        writer.writerow([d])

print("done.")
