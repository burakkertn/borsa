import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from datetime import datetime, timedelta
import pymongo

# Veriyi yükleyin veya oluşturun (örneğin, data.csv'den)
veri = pd.read_csv("dataeur.csv")

# Tarihleri günlük sıralamalı sayılara dönüştürün
veri["date"] = veri["date"].apply(lambda x: datetime.strptime(x, "%d/%m/%Y").strftime('%d/%m/%Y'))

x = veri["date"]  # Tarihleri kullanın
y = veri["eur"]

# Polinom Regresyon modelini eğitin
tahminpolinom = PolynomialFeatures(degree=3)
Xyeni = tahminpolinom.fit_transform(np.array(range(len(x))).reshape(-1, 1))

polinommodel = LinearRegression()
polinommodel.fit(Xyeni, y.values.reshape(-1, 1))

# Gelecekteki günleri tahmin edin
gelecekteki_gun_sayisi = 50  # Kaç gün sonrasını tahmin etmek istediğinizi belirtin
son_tarih = datetime.strptime(x.iloc[-1], '%d/%m/%Y')  # Veri setindeki en son tarihi alın ve datetime türüne dönüştürün

gelecekteki_tarihler = []
for i in range(1, gelecekteki_gun_sayisi + 1):
    son_tarih += timedelta(days=1)
    gelecekteki_tarihler.append(son_tarih.strftime('%d/%m/%Y'))

gelecekteki_tarihler_sirali = [datetime.strptime(tarih, '%d/%m/%Y').strftime('%d/%m/%Y') for tarih in gelecekteki_tarihler]
Xgelecek = tahminpolinom.transform(np.array(range(len(x), len(x) + gelecekteki_gun_sayisi)).reshape(-1, 1))
gelecekteki_eur_tahmini = polinommodel.predict(Xgelecek)

# MongoDB'ye bağlanın
client = pymongo.MongoClient("mongodb://localhost:27017/")  # MongoDB sunucu bağlantısı
database = client["borsadb"]  # Veritabanı adı
collection = database["eur"]  # Koleksiyon adı

# Geçmiş verileri MongoDB'ye ekleyin
veri_dict = veri.to_dict(orient="records")  # DataFrame'i sözlük listesine dönüştürün
collection.insert_many(veri_dict)

# Gelecekteki tahminleri MongoDB'ye ekleyin
for tarih, tahmin in zip(gelecekteki_tarihler_sirali, gelecekteki_eur_tahmini):
    tahmin_verisi = {
        "date": tarih,
        "eur": tahmin[0]
    }
    collection.insert_one(tahmin_verisi)

print("Veriler ve tahminler yeni veritabanına başarıyla kaydedildi.")
