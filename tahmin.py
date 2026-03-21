import random
import tokenizer

SON = "SON"

liste = tokenizer.tokenize()

kelime_sayı = {}
sayı_kelime = {}
sayac = 0

for satir in liste:
    for kelime in satir:
        if kelime not in kelime_sayı:
            kelime_sayı[kelime] = sayac
            sayı_kelime[sayac] = kelime
            sayac += 1

kelime_sayı[SON] = sayac
sayı_kelime[sayac] = SON
SON_SAYI = sayac
sayac += 1

sayı_listesi = [[kelime_sayı[k] for k in satir] for satir in liste]

ikili_sayac = {}
uclu_sayac = {}

for satir in sayı_listesi:
    uzatilmis = satir + [SON_SAYI]
    for i in range(len(uzatilmis) - 1):
        ikili = (uzatilmis[i], uzatilmis[i+1])
        ikili_sayac[ikili] = ikili_sayac.get(ikili, 0) + 1

    for i in range(len(uzatilmis) - 2):
        uclu = (uzatilmis[i], uzatilmis[i+1], uzatilmis[i+2])
        uclu_sayac[uclu] = uclu_sayac.get(uclu, 0) + 1

def sonraki_ikili(mevcut):
    bulunanlar = {ikili: miktar for ikili, miktar in ikili_sayac.items() if ikili[0] == mevcut}
    if not bulunanlar:
        return None
    return random.choices(list(bulunanlar.keys()), weights=bulunanlar.values(), k=1)[0][1]

def sonraki_uclu(mevcut1, mevcut2):
    bulunanlar = {uclu: miktar for uclu, miktar in uclu_sayac.items() if uclu[0] == mevcut1 and uclu[1] == mevcut2}
    if not bulunanlar:
        return None
    return random.choices(list(bulunanlar.keys()), weights=bulunanlar.values(), k=1)[0][2]

def dizi(baslangic):
    sonuc = [baslangic]
    ikinci_kelime = sonraki_ikili(baslangic)
    if ikinci_kelime is None or ikinci_kelime == SON_SAYI:
        return sonuc
        
    sonuc.append(ikinci_kelime)
    mevcut1 = baslangic
    mevcut2 = ikinci_kelime
    
    while True:
        tahmin = sonraki_uclu(mevcut1, mevcut2)
        if tahmin is None or tahmin == SON_SAYI:
            break
        sonuc.append(tahmin)
        mevcut1 = mevcut2
        mevcut2 = tahmin
        
    return sonuc

print("Bilinen kelimeler:", list(kelime_sayı.keys()))

girdi = input("Kelime girin: ").strip().lower()

bas_sayi = kelime_sayı[girdi]
sonuc_sayilar = dizi(bas_sayi)
sonuc_kelimeler = [sayı_kelime[s] for s in sonuc_sayilar]
print(f"\nTahmin: {' '.join(sonuc_kelimeler)}")