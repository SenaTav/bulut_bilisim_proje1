from flask import Flask, jsonify, request, render_template
import requests
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.json.ensure_ascii = False 

TMDB_API_KEY = '6fc0f84971f7fd4e876f776405805c1d'
SPOTIFY_CLIENT_ID = '6ae4a1ec60564456aafac6679a26d42f'
SPOTIFY_CLIENT_SECRET = '058987c73fc64eb1b51dba6bcb9b710b'

MOOD_MAP_TMDB = {
    'mutlu': '35',      
    'melankolik': '18', 
    'heyecanli': '28',   
    'urkutucu': '27', 
    'asik': '10749',    
}

MOOD_MAP_SPOTIFY = {
    'mutlu': 'happy upbeat pop',
    'melankolik': 'sad',
    'heyecanli': 'workout edm dance',
    'asik': 'türkçe aşk şarkıları',
    'urkutucu': 'dark creepy goth'
}

MOOD_MAP_AKTIVITE = {
    'mutlu': [
        'Dışarı çıkıp temiz hava al ve güneşin tadını çıkar', 
        'Sevdiğin bir arkadaşını kahveye davet et', 
        'Yeni bir yemek tarifi dene ',
        'Sokakta gördüğün ilk kedi veya köpeği sev',
        'Hiçbir sebep yokken eski bir dostunu arayıp halini hatırını sor',
        'Kendine küçük bir hediye al, bunu hak ettin! ',
        'Kişisel bakım yap kendinle uğraş',
        'Bağırarak karoke yapmaya ne dersin',
        'Bir topluluğa katılıp sosyalleşmeye başla yeni insanlarla tanıştıkça neşen artacak',
        'Spontane bir şekilde arkadaşlarınla küçük bir bulışma yapmaya ne dersin',
        'Yaşadığın şehri hiç bir turist gibi gezdin mi? Daha önce fark etmediğin detayları bu sefer fark edince mutluluğun katlanacak!',
        'Bir standup,komedi gösterisi izle',
        'Hava uygunsa uçurtma uçur'
    ],
    'melankolik': [
        'Sıcak bir içecek alıp camdan dışarıyı izle', 
        'Duygularını bir günlüğe veya kağıda dök',
        'Spotifyda podcast dinlemeye ne dersin?',
        'Odanı hafifçe toplayarak zihnini rahatlat',
        'Seni rahatlatacak şeyleri düşün',
        'Telefonu sessize al ve 1 saat boyunca hiçbir ekrana bakma',
        'Eski fotoğraflara bakıp nostalji yap(Uyarı)',
        'Gözlerini kapat ve sadece nefes alışverişine odaklan ',
        'Zihnini dinlendirecek ama elini çalıştıracak şeyler dene: Örgü örmek,boyama yapmak,boncuk işlemek...',
        'Sokak hayvanları için kapının önüne bir kap mama ve su bırak.Başkasına iyi gelmek, hüznü hafifletir.',
        'Çocukken yapmayı en sevdiğin şeyleri yap'
    ],
    'enerjik': [
        'Hemen 15 dakikalık bir ev egzersizi yap', 
        'Kulaklığını takıp tempolu bir yürüyüşe/koşuya çık', 
        'Uzun zamandır ertelediğin o sıkıcı işi bugün bitir!',
        'Odanın şeklini değiştir, eşyaların yerini yenile',
        'İnternetten hiç bilmediğin bir dili öğrenmeye çalış',
        'Sesi son ses açıp odada çılgınlar gibi zıpla',
        'Evi baştan aşağı süpürüp temizlik terapisine gir',
        'Şehrin hiç gitmediğin bir sokağını veya kafesini keşfet', 
        'Yakındaki bir ormana/parka gidip doğa yürüyüşü yap', 
        'Daha önce yemekten çekindiğin o yemeği sipariş et',
        'Haritayı aç, gözünü kapat ve parmağının geldiği yeri araştır',
        'Yakın gelecekte yapacağın bir kamp veya gezi planı tasarla',
        'Arkadaşlarınla kaçış evine veya Lunaparka git',
        'Bisiklet sür'
        'Spontane yaşamaya ne dersin?Küçük bir sırt çantasıyla hafta sonu için yakın bir lokasyona gidebilirsin'

    ],
    'asik': [
        'Sevdiğin kişiye içinden gelen tatlı bir mesaj at', 
        'Gelecek için heyecan verici bir plan/hayal kur', 
        'Kendini şımartıp en sevdiğin tatlıyı ısmarla',
        'Romantik bir komedi filmi açıp mısır patlat',
        'Birlikte dinlediğiniz "o" şarkıyı açıp anılara dal',
        'Kağıda seni en çok mutlu eden 3 şeyi yaz',
        'Partnerinle bir yemek veya tatlı hazırla',
        'Partlerinle birbirinizin resmini çizmeye çalışın',
        'Sevdiğin kişiyle fotoğraflarınıza bakın ve geçmişteki tatlı anılarınızdan konuşun',
        'Partnerinize elinizle hediye hazırlayın: Bir mektup,çiçek,kalp,origami...',
        'Partnerinizle lego yapın',
        'Size özel şeyler bulun:Sizin şarkınız,sizin mekanınız,sizin filminiz...',
        'Beraber ortak bir hobi bulun.Bulmaya çalışırken zaten birçok aktivite deneyeceksiniz',
        'Çiftlere özel tasarlanmış, birbirini daha iyi tanımayı sağlayan soru-cevap kutu oyunları oynamak.',
        'Manzara ya da gün batımını beraber izleyin',
        'Birlikte gidilecek tatiller, izlenecek filmler veya yapılacak aktiviteler için dijital bir (vision board) hazırlamak.',
        'Bugun bir bilet almanın tam sırası: Tiyatro,sinema,konser belki de otobüs...'
    ],

    'urkutucu': [
        'Işıkları kapatıp gizemli/korkunç bir hikaye oku veya dinle', 
        'İnternetten çözülmemiş tarihi sırları veya gizemleri araştır', 
        'Karanlıkta oturup sadece dışarıdaki sesleri dinle',
        'Bir korku oyunu oyna',
        'Uzaylılar veya paralel evrenler hakkında komplo teorileri izle',
        'Tüm perdeleri kapatıp kült bir korku filmi aç',
        'Paronormal hikayeler oku',
        'Sanal Gerçeklik gözlüğü bulup veya kiralayıp karanlıkta hayatta kalma temalı bir korku deneyimi yaşamak.'
    ]
}

def get_spotify_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(auth_url, data={
        'grant_type': 'client_credentials'
    }, auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET))
    
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

@app.route('/')
def ana_sayfa():
    return render_template('index.html')

@app.route('/api/oneriler', methods=['GET'])
def oneri_getir():
    gelen_mod = request.args.get('mod', 'mutlu').lower() 
    
    # 1. FİLM BULMA BÖLÜMÜ (TMDB)
    tmdb_tur_id = MOOD_MAP_TMDB.get(gelen_mod, '35')
    tmdb_url = f"https://api.themoviedb.org/3/discover/movie"

    rastgele_sayfa = random.randint(1, 5)

    tmdb_response = requests.get(tmdb_url, params={
        'api_key': TMDB_API_KEY,
        'with_genres': tmdb_tur_id,
        'language': 'tr-TR',
        'sort_by': 'popularity.desc',
        'with_original_language': 'en',
        'page': rastgele_sayfa
    })
    
    film_verisi = {}
    if tmdb_response.status_code == 200:
        filmler = tmdb_response.json().get('results', [])
        if filmler:
            secilen_film = random.choice(filmler) 
            film_verisi = {
                'adi': secilen_film['title'],
                'ozeti': secilen_film['overview'],
                'poster': f"https://image.tmdb.org/t/p/w500{secilen_film['poster_path']}"
            }

        spotify_kelime = MOOD_MAP_SPOTIFY.get(gelen_mod, 'pop')
        spotify_token = get_spotify_token()
        
        rastgele_atlama = random.randint(0, 10) 
        
        spotify_url = "https://api.spotify.com/v1/search"
        params = {
            "q": spotify_kelime, 
            "type": "track",
            "limit": 10,  
            "offset": rastgele_atlama
        }
        
        headers = {
            "Authorization": f"Bearer {spotify_token}"
        }
        
        spotify_response = requests.get(spotify_url, headers=headers, params=params)
        
        sarki_verisi = {}
        if spotify_response.status_code == 200:
            sarkilar = spotify_response.json().get('tracks', {}).get('items', [])
            if sarkilar:
                secilen_sarki = random.choice(sarkilar)
                
                kapak_resmi = ""
                if secilen_sarki.get('album') and secilen_sarki['album'].get('images'):
                    kapak_resmi = secilen_sarki['album']['images'][0]['url']
                    
                sarki_verisi = {
                    'sarki_adi': secilen_sarki['name'],
                    'sanatci': secilen_sarki['artists'][0]['name'],
                    'kapak_resmi': kapak_resmi,
                    'spotify_linki': secilen_sarki['external_urls']['spotify']
                }
        else:
            print("SPOTIFY API HATASI:", spotify_response.json())

    

    aktiviteler = MOOD_MAP_AKTIVITE.get(gelen_mod, ['Derin bir nefes al ve anın tadını çıkar '])
    secilen_aktivite = random.choice(aktiviteler)
    return jsonify({
        'algilanan_mod': gelen_mod,
        'film_onerisi': film_verisi,
        'sarki_onerisi': sarki_verisi,
        'aktivite_onerisi': secilen_aktivite
    })

if __name__ == '__main__':
    app.run(debug=True)

