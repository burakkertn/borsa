import requests
import csv
from bs4 import BeautifulSoup

# API URL'si
api_url = "https://localhost:44317/api/Borsa/Dolar?daysAgo=500"

# Güvensiz bağlantı uyarılarını devre dışı bırakma
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Güvensiz bağlantı ile istek yapma
response = requests.get(api_url, verify=False)

# API yanıtını XML'den çözümleme
soup = BeautifulSoup(response.text, 'xml')

# CSV dosyasını aç ve başlık satırını yaz
with open('datausd.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['date', 'usd'])  

    # Her bir <items> öğesini işle
    for item in soup.find_all('items'):
        date = item.find('date').text
        usd = item.find('usd').text

        # Tarih formatını düzenle (dd-mm-yyyy veya d/m/yyyy)
        date_parts = date.split('-')
        if len(date_parts) == 3:
            date = f"{date_parts[0]}/{date_parts[1]}/{date_parts[2]}"
        
        # Verileri CSV dosyasına yaz
        writer.writerow([date, usd])

print("Veriler datausd.csv dosyasına yazıldı.")
