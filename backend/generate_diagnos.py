import pymongo
import csv

print("connect to db")
myclient = pymongo.MongoClient(
    "mongodb://puskesmas:puskesmba@localhost:27017/puskesmas")
mydb = myclient["puskesmas"]
tabel = mydb["Kunjungan"]

pasien = tabel.find({})

print("reading data")
data = []
for p in pasien:
    data.append(p['no_mr']+' '+p['tanggal']+' X')

print("saving data")
print(data)
with open('files/diagnosa.txt', 'w') as file:
    writer = csv.writer(file)
    for d in data:
        writer.writerow([d])

print("done.")
