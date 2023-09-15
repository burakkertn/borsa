import subprocess
import pymongo

import os

dosyalar = ['datache.csv', 'datajpy.csv', 'dataeur.csv', 'datagbp.csv', 'datausd.csv']

# Her dosyayı sırayla silin
for dosya in dosyalar:
    if os.path.exists(dosya):
        os.remove(dosya)
        print(f"{dosya} başarıyla silindi.")
    else:
        print(f"{dosya} dosyası mevcut değil, silinemedi.")

# Diğer işlemlere devam edin
client = pymongo.MongoClient("mongodb://localhost:27017/")  # MongoDB sunucu bağlantısı
database = client["borsadb"]  # Veritabanı adı



# Diğer beş dosyayı çalıştırma
files_to_run = ['connectionche.py', 'connectionjpy.py', 'connectioneur.py', 'connectiongbp.py', 'connectionusd.py']

for file in files_to_run:
    subprocess.call(['python', file])






# Silmek istediğiniz koleksiyonların adlarını listeye ekleyin
koleksiyonlar = ["usd", "eur", "jpy", "gbp", "che"]

# Her koleksiyonu sırayla silin
for koleksiyon_adı in koleksiyonlar:
    database.drop_collection(koleksiyon_adı)
    print(f"{koleksiyon_adı} koleksiyonu başarıyla silindi.")

print("Mevcut koleksiyonlar başarıyla silindi.")



files_to_run = ['tahminche.py', 'tahmineur.py', 'tahmingbp.py', 'tahminjpy.py', 'tahminusd.py']

for file in files_to_run:
    subprocess.call(['python', file])