import random
import tokenizer

SON = "SON"
KELIME_SON = "KELIME_SON"

liste = tokenizer.tokenize()
ekler = tokenizer.veri_setinden_ekleri_cikar(liste)

kelime_sayi = {}
sayi_kelime = {}
sayac = 0

for satir in liste:
    for kelime in satir:
        if kelime not in kelime_sayi:
            kelime_sayi[kelime] = sayac
            sayi_kelime[sayac] = kelime
            sayac += 1

kelime_sayi[SON] = sayac
sayi_kelime[sayac] = SON
SON_SAYI = sayac

sayi_listesi = [[kelime_sayi[k] for k in satir] for satir in liste]

ikili_sayac = {}
uclu_sayac = {}

for satir in sayi_listesi:
    uzatilmis = satir + [SON_SAYI]
    for i in range(len(uzatilmis) - 1):
        ikili = (uzatilmis[i], uzatilmis[i + 1])
        ikili_sayac[ikili] = ikili_sayac.get(ikili, 0) + 1

    for i in range(len(uzatilmis) - 2):
        uclu = (uzatilmis[i], uzatilmis[i + 1], uzatilmis[i + 2])
        uclu_sayac[uclu] = uclu_sayac.get(uclu, 0) + 1

parca_baslangic_sayac = {}
parca_ikili_sayac = {}
parca_uclu_sayac = {}

for satir in liste:
    for kelime in satir:
        parcaciklar = tokenizer.parcala(kelime, ekler)
        if not parcaciklar:
            continue

        ilk = parcaciklar[0]
        parca_baslangic_sayac[ilk] = parca_baslangic_sayac.get(ilk, 0) + 1

        uzatilmis_parca = parcaciklar + [KELIME_SON]
        for i in range(len(uzatilmis_parca) - 1):
            ikili = (uzatilmis_parca[i], uzatilmis_parca[i + 1])
            parca_ikili_sayac[ikili] = parca_ikili_sayac.get(ikili, 0) + 1

        for i in range(len(uzatilmis_parca) - 2):
            uclu = (uzatilmis_parca[i], uzatilmis_parca[i + 1], uzatilmis_parca[i + 2])
            parca_uclu_sayac[uclu] = parca_uclu_sayac.get(uclu, 0) + 1


def agirlikli_secim(sozluk):
    if not sozluk:
        return None
    return random.choices(list(sozluk.keys()), weights=sozluk.values(), k=1)[0]

def sonraki_ikili(mevcut):
    bulunanlar = {ikili: miktar for ikili, miktar in ikili_sayac.items() if ikili[0] == mevcut}
    if not bulunanlar:
        return None
    secim = agirlikli_secim(bulunanlar)
    return secim[1]

def sonraki_uclu(mevcut1, mevcut2):
    bulunanlar = {
        uclu: miktar
        for uclu, miktar in uclu_sayac.items()
        if uclu[0] == mevcut1 and uclu[1] == mevcut2
    }
    if not bulunanlar:
        return None
    secim = agirlikli_secim(bulunanlar)
    return secim[2]

def parcadan_sonraki_ikili(mevcut_parca):
    bulunanlar = {
        ikili: miktar
        for ikili, miktar in parca_ikili_sayac.items()
        if ikili[0] == mevcut_parca
    }
    if not bulunanlar:
        return None
    secim = agirlikli_secim(bulunanlar)
    return secim[1]

def parcadan_sonraki_uclu(mevcut1, mevcut2):
    bulunanlar = {
        uclu: miktar
        for uclu, miktar in parca_uclu_sayac.items()
        if uclu[0] == mevcut1 and uclu[1] == mevcut2
    }
    if not bulunanlar:
        return None
    secim = agirlikli_secim(bulunanlar)
    return secim[2]

def parcaciklardan_kelime_uret(tohum_kelime=None, max_adim=8):
    if not parca_baslangic_sayac:
        return None

    if tohum_kelime:
        tohum_parcalar = tokenizer.parcala(tohum_kelime, ekler)
        ilk_parca = tohum_parcalar[0] if tohum_parcalar else None
        if ilk_parca not in parca_baslangic_sayac:
            ilk_parca = agirlikli_secim(parca_baslangic_sayac)
    else:
        ilk_parca = agirlikli_secim(parca_baslangic_sayac)

    if not ilk_parca:
        return None

    parcalar = [ilk_parca]

    ikinci = parcadan_sonraki_ikili(ilk_parca)
    if not ikinci or ikinci == KELIME_SON:
        kelime = ""
        for parca in parcalar:
            if parca.startswith("+"):
                kelime += parca[1:]
            else:
                kelime += parca
        return kelime if kelime else None

    parcalar.append(ikinci)
    mevcut1 = ilk_parca
    mevcut2 = ikinci

    for _ in range(max_adim - 1):
        sonraki = parcadan_sonraki_uclu(mevcut1, mevcut2)
        if not sonraki:
            sonraki = parcadan_sonraki_ikili(mevcut2)
        if not sonraki or sonraki == KELIME_SON:
            break
        parcalar.append(sonraki)
        mevcut1 = mevcut2
        mevcut2 = sonraki

    kelime = ""
    for parca in parcalar:
        if parca.startswith("+"):
            kelime += parca[1:]
        else:
            kelime += parca
    return kelime if kelime else None

def modele_uygun_kelime(kelime):
    if kelime in kelime_sayi:
        return kelime

    for _ in range(12):
        aday = parcaciklardan_kelime_uret(kelime)
        if aday in kelime_sayi:
            return aday

    bilinenler = [k for k in kelime_sayi.keys() if k != SON]
    return random.choice(bilinenler)

def cumle_uret(baslangiclar, max_uzunluk=20):
    if not baslangiclar:
        return []

    sonuc = baslangiclar[:]

    if len(baslangiclar) == 1:
        ikinci_kelime = sonraki_ikili(sonuc[-1])
        if ikinci_kelime is None or ikinci_kelime == SON_SAYI:
            return sonuc
        sonuc.append(ikinci_kelime)

    elif len(baslangiclar) == 2:
        ucuncu_kelime = sonraki_ikili(sonuc[-1])
        if ucuncu_kelime is None or ucuncu_kelime == SON_SAYI:
            return sonuc
        sonuc.append(ucuncu_kelime)

    mevcut1 = sonuc[-2]
    mevcut2 = sonuc[-1]

    while len(sonuc) < max_uzunluk:
        tahmin = sonraki_uclu(mevcut1, mevcut2)
        if tahmin is None or tahmin == SON_SAYI:
            break
        sonuc.append(tahmin)
        mevcut1 = mevcut2
        mevcut2 = tahmin

    return sonuc

print("Bilinen kelime sayisi:", len(kelime_sayi) - 1)
print("Veriden ogrenilen ek sayisi:", len(ekler))

girdi = input("Kelime girin: ").strip().lower().split()
if not girdi:
    raise SystemExit

cozulen_girdi = [modele_uygun_kelime(k) for k in girdi]

bas_sayilar = [kelime_sayi[kelime] for kelime in cozulen_girdi]
sonuc_sayilar = cumle_uret(bas_sayilar)
sonuc_kelimeler = [sayi_kelime[s] for s in sonuc_sayilar]

print(f"\nTahmin cumlesi: {' '.join(sonuc_kelimeler)}")