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

ikili_sayac = {}

for satir in sayı_listesi:
    uzatilmis = satir + [SON]
    for i in range(len(uzatilmis) - 1):
        ikili = (uzatilmis[i], uzatilmis[i+1])
        ikili_sayac[ikili] = ikili_sayac.get(ikili, 0) + 1

def sonraki(mevcut):
    bulunanlar = {ikili: miktar for ikili, miktar in ikili_sayac.items() if ikili[0] == mevcut}
    if not bulunanlar:
        return None
    return random.choices(list(bulunanlar.keys()), weights=bulunanlar.values(), k=1)[0][1]

def dizi(baslangic):
    sonuc = [baslangic]
    mevcut = baslangic
    while True:
        tahmin = sonraki(mevcut)
        if tahmin is None or tahmin == SON:
            break
        sonuc.append(tahmin)
        mevcut = tahmin
    return sonuc

print("Bilinen kelimeler:", list(kelime_sayı.keys()))
girdi = input("Kelime girin: ").strip()

baslangic_sayi = kelime_sayı[girdi]
sonuc_sayilar = dizi(baslangic_sayi)
sonuc_kelimeler = [sayı_kelime[s] for s in sonuc_sayilar]
print(f"Tahmin: {sonuc_kelimeler}")