# Mooduma Göre - Film,Müzik ve Aktivite Öneri Sistemi

Bu proje, kullanıcının anlık ruh haline göre(projede bunlar mutlu,melankolik,enerjik,aşık ve ürkütücü olarak belirtilmiştir) kişiselleştirilmiş film, şarkı ve aktivite önerileri sunan çift katmanlı (Frontend + API) bir web uygulamasıdır. 

Bulut bilişim mimarisi prensiplerine uygun olarak, uygulamanın ön yüzü ve arka yüzü farklı sunucularda barındırılmaktadır.

# Canlı Proje Linkleri
Frontend (Arayüz): http://senatav-mooduma-gore-frontend.s3-website-us-east-1.amazonaws.com/
Backend (API): https://mooduma-gore.onrender.com

# Kullanılan Teknolojiler
Frontend: HTML, CSS, JavaScript
Backend: Python, Flask, Flask-CORS
API'ler: TMDB API , Spotify API
Dağıtım: Git, GitHub, AWS, Render

# Mimari Yapı
Proje iki ana bileşenden oluşur:
1. İstemci (S3): Kullanıcı arayüzünü sunar ve kullanıcının seçtiği ruh haline göre Backend'e istek atar.
2. Sunucu (Render): İstemciden gelen isteği alır, harici API'lerle haberleşir, verileri işler ve JSON formatında istemciye geri gönderir. CORS ayarları sayesinde iki farklı origin arasında güvenli iletişim sağlanmıştır.
