import requests
import csv
from bs4 import BeautifulSoup

# API URL'si
api_url = "https://localhost:44317/api/Borsa/IsvicreFrangi?daysAgo=500"

# Güvensiz bağlantı uyarılarını devre dışı bırakma
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Güvensiz bağlantı ile istek yapma
response = requests.get(api_url, verify=False)

# API yanıtını XML'den çözümleme
soup = BeautifulSoup(response.text, 'xml')

# CSV dosyasını aç ve başlık satırını yaz
with open('datache.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['date', 'che'])

    # Her bir <items> öğesini işleme
    for item in soup.find_all('items'):
        date = item.find('date').text
        che = item.find('che').text

        # Tarih formatını düzenlemer
        date_parts = date.split('-')
        if len(date_parts) == 3:
            date = f"{date_parts[0]}/{date_parts[1]}/{date_parts[2]}"
        
        # Verileri CSV dosyasına yazma
        writer.writerow([date, che])

print("Veriler datache.csv dosyasına yazıldı.")
