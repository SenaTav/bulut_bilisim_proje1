# Mooduma Göre - Film,Müzik ve Aktivite Öneri Sistemi

Bu proje, kullanıcının anlık ruh haline göre(projede bunlar mutlu,melankolik,enerjik,aşık ve ürkütücü olarak belirtilmiştir) kişiselleştirilmiş film, şarkı ve aktivite önerileri sunan çift katmanlı (Frontend + API) bir web uygulamasıdır. 

Bu proje, modern Bulut Bilişim mimarileri göz önünde bulundurularak, ön yüz ve arka yüz servislerinin birbirinden tamamen bağımsız sunucularda barındırıldığı bir yapıda tasarlanmıştır.

# Canlı Proje Linkleri
Frontend (Arayüz): http://senatav-mooduma-gore-frontend.s3-website-us-east-1.amazonaws.com/
Backend (API): https://mooduma-gore.onrender.com

# Mimari Yapı ve Kullanılan Teknolojiler

Proje, iki ayrı sunucunun birbiriyle API üzerinden haberleştiği modern bir mimariye sahiptir:

# 1.Frontend- İstemci Katmanı
Teknolojiler:HTML5, CSS3, Vanilla JavaScript
Barındırma: Amazon Web Services (AWS) S3 - Static Website Hosting
Görev:Kullanıcı ile etkileşime geçer, seçilen duygu durumunu yakalar ve arka yüze HTTP `GET` isteği (Fetch API) gönderir. Gelen JSON verisini işleyerek ekranda dinamik olarak gösterir.

# 2.Backend - API Katmanı
Teknolojiler: Python, Flask, Flask-CORS, Gunicorn
Barındırma: Render.com 
Görev:Ön yüzden gelen istekleri karşılar. İstek yapılan ruh haline göre dış servislere bağlanarak veri çeker, bu verileri harmanlar ve JSON formatında ön yüze geri iletir. `Flask-CORS` eklentisi ile AWS S3 üzerinden gelen dış isteklere güvenli erişim izni verilmiştir.

# 3. Entegre Edilen Dış Servisler 
TMDB (The Movie Database) API: Ruh haline uygun film önerileri, film özetleri ve afişlerini dinamik olarak çekmek için kullanılmıştır.
Spotify API: Kullanıcının moduna uygun şarkı veya çalma listesi verilerini çekmek için sisteme entegre edilmiştir.


# Nasıl Çalışıyor? 
1. Kullanıcı, AWS S3 üzerindeki statik web sitesine giriş yapar.
2. Ekranda yer alan ruh hali butonlarından (Örn:Melankolik) birine tıklar.
3. İstemci tarafındaki JavaScript, Render üzerinde çalışan Flask API'sine bir istek atar: `GET /api/oneriler?mod=melankolik`
4. Flask sunucusu bu parametreyi alır, kendi içindeki algoritmayla uygun film türü ve müzik tarzını belirler.
5. Flask, TMDB ve Spotify API'lerine bağlanıp anlık verileri çeker.
6. Elde edilen veriler düzenlenip tek bir JSON paketi haline getirilir ve Frontend'e yollanır.
7. Frontend, gelen veriyi ayrıştırarak ekranda film afişi, şarkı linki ve kişiselleştirilmiş aktivite önerisi olarak kullanıcıya sunar.
