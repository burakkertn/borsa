import requests
import csv

# API URL'si
api_url = "https://localhost:44317/api/Borsa/Dolar?daysAgo=23"

# API'den veri çekme
response = requests.get(api_url)

# Yanıtı kontrol etme
if response.status_code == 200:
    # JSON verisini alın
    json_data = response.json()

    # CSV dosyasına yazma
    with open("data.csv", "w", newline="") as csvfile:
        # CSV dosyası yazma işlemi için writer oluşturun
        csv_writer = csv.writer(csvfile)

        # Başlık satırını yazın
        csv_writer.writerow(["date", "usd"])

        # Verileri CSV dosyasına yazın
        for data_point in json_data:
            # Verileri CSV satırına dönüştürün ve yazın
            csv_writer.writerow([data_point["date"], data_point["usd"]])

    print("Veriler başarıyla data.csv dosyasına yazıldı.")
else:
    print("API'den veri çekme başarısız. Hata kodu:", response.status_code)