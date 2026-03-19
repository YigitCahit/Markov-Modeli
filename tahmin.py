import random

SON = "SON"

liste = [
    ["merhaba", "bugün", "nasılsın", "umarım", "iyisindir"],
    ["merhaba", "bugün", "hava", "çok", "güzel"],
    ["selam", "bugün", "neler", "yapacaksın"],
    ["selam", "ne", "haber", "görüşmeyeli", "uzun", "zaman", "oldu"],
    ["günaydın", "bugün", "hava", "yağmurlu", "olacakmış"],
    ["günaydın", "sabah", "erken", "kalktım", "ve", "kahve", "içtim"],
    ["bugün", "hava", "çok", "soğuk", "dikkatli", "ol"],
    ["yarın", "hava", "güneşli", "olacak", "dışarı", "çıkalım"],
    ["dün", "hava", "çok", "kötüydü", "evde", "kaldım"],
    ["bugün", "hava", "sıcak", "denize", "gidelim"],
    ["dışarı", "çıkalım", "çünkü", "hava", "çok", "güzel"],
    ["evde", "kaldım", "çünkü", "hava", "çok", "soğuk"],
    ["sabah", "erken", "kalktım", "spor", "yaptım", "ve", "yoruldum"],
    ["akşam", "eve", "geldim", "kitap", "okudum", "ve", "uyudum"],
    ["akşam", "eve", "geldim", "film", "izledim", "çok", "güzeldi"],
    ["öğlen", "yemekte", "döner", "yedim", "çok", "lezzetliydi"],
    ["akşam", "yemekte", "çorba", "içtim", "ve", "salata", "yedim"],
    ["sabah", "kahvaltıda", "yumurta", "yedim", "ve", "çay", "içtim"],
    ["bugün", "işte", "çok", "yoruldum", "hemen", "uyuyacağım"],
    ["yarın", "okulda", "önemli", "bir", "sınav", "var"],
    ["yarın", "işte", "önemli", "bir", "toplantı", "var"],
    ["yeni", "bir", "bilgisayar", "aldım", "çok", "hızlı", "çalışıyor"],
    ["yeni", "bir", "telefon", "aldım", "kamerası", "çok", "güzel"],
    ["python", "ile", "kod", "yazmak", "çok", "zevkli", "ve", "eğlenceli"],
    ["yapay", "zeka", "ile", "yeni", "projeler", "geliştiriyorum"],
    ["kitap", "okudum", "ve", "sonra", "hemen", "uyudum"],
    ["film", "izledim", "ve", "sonra", "arkadaşımla", "konuştum"],
    ["çok", "çalıştım", "çünkü", "sınav", "çok", "zor"]
]

kelime_sayı = {}
sayı_kelime = {}
sayac = 0

for satir in liste:
    for kelime in satir:
        if kelime not in kelime_sayı:
            kelime_sayı[kelime] = sayac
            sayı_kelime[sayac] = kelime
            sayac += 1

sayı_listesi = [[kelime_sayı[k] for k in satir] for satir in liste]

uclu_sayac = {}

for satir in sayı_listesi:
    uzatilmis = satir + [SON]
    for i in range(len(uzatilmis) - 2):
        uclu = (uzatilmis[i], uzatilmis[i+1], uzatilmis[i+2])
        uclu_sayac[uclu] = uclu_sayac.get(uclu, 0) + 1

def sonraki(mevcut1, mevcut2):
    bulunanlar = {uclu: miktar for uclu, miktar in uclu_sayac.items() if uclu[0] == mevcut1 and uclu[1] == mevcut2}
    if not bulunanlar:
        return None
    return random.choices(list(bulunanlar.keys()), weights=bulunanlar.values(), k=1)[0][2]

def dizi(baslangic1, baslangic2):
    sonuc = [baslangic1, baslangic2]
    mevcut1 = baslangic1
    mevcut2 = baslangic2
    while True:
        tahmin = sonraki(mevcut1, mevcut2)
        if tahmin is None or tahmin == SON:
            break
        sonuc.append(tahmin)
        mevcut1 = mevcut2
        mevcut2 = tahmin
    return sonuc

print("Bilinen kelimeler:", list(kelime_sayı.keys()))

girdi1 = input("Kelime girin: ").strip()
girdi2 = input("2. Kelimeyi girin: ").strip()

bas1_sayi = kelime_sayı[girdi1]
bas2_sayi = kelime_sayı[girdi2]

sonuc_sayilar = dizi(bas1_sayi, bas2_sayi)
sonuc_kelimeler = [sayı_kelime[s] if s != SON else "" for s in sonuc_sayilar]
print(f"Tahmin: {' '.join(sonuc_kelimeler)}")