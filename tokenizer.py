UNLULER = "aeıioöuü"

def tokenize(dosya_adi="data.txt"):
    bitis = ".!?\n"
    noktalamalar = ",;:\"'()[]{}-_/#*"
    sonuc = []

    with open(dosya_adi, "r", encoding="utf-8") as dosya:
        metin = dosya.read()
    metin = metin.lower()

    for isaret in bitis:
        metin = metin.replace(isaret, "|")

    for isaret in noktalamalar:
        metin = metin.replace(isaret, " ")

    cumleler = metin.split("|")

    for cumle in cumleler:
        kelimeler = cumle.split()
        if kelimeler:
            sonuc.append(kelimeler)

    return sonuc

def hecele(kelime):
    if not kelime:
        return []

    heceler = []
    i = 0
    n = len(kelime)

    while i < n:
        unlu_index = -1
        for j in range(i, n):
            if kelime[j] in UNLULER:
                unlu_index = j
                break

        if unlu_index == -1:
            if heceler:
                heceler[-1] += kelime[i:]
            else:
                heceler.append(kelime[i:])
            break

        sonraki_unlu = -1
        for j in range(unlu_index + 1, n):
            if kelime[j] in UNLULER:
                sonraki_unlu = j
                break

        if sonraki_unlu == -1:
            heceler.append(kelime[i:])
            break

        aradaki_unsuz = sonraki_unlu - unlu_index - 1
        if aradaki_unsuz <= 1:
            kesim = unlu_index + 1
        else:
            kesim = unlu_index + 2

        heceler.append(kelime[i:kesim])
        i = kesim

    return [h for h in heceler if h]

def veri_setinden_ekleri_cikar(cumleler, min_frekans=3, min_govde_cesidi=3, max_ek_uzunlugu=5):
    ek_frekans = {}
    ek_govdeler = {}

    for satir in cumleler:
        for kelime in satir:
            if len(kelime) < 4:
                continue

            ust_sinir = min(max_ek_uzunlugu, len(kelime) - 2)
            for uzunluk in range(2, ust_sinir + 1):
                govde = kelime[:-uzunluk]
                ek = kelime[-uzunluk:]

                if len(govde) < 2:
                    continue
                if not any(harf in UNLULER for harf in ek):
                    continue

                ek_frekans[ek] = ek_frekans.get(ek, 0) + 1
                if ek not in ek_govdeler:
                    ek_govdeler[ek] = set()
                ek_govdeler[ek].add(govde)

    adaylar = []
    for ek, frekans in ek_frekans.items():
        if frekans < min_frekans:
            continue
        if len(ek_govdeler.get(ek, set())) < min_govde_cesidi:
            continue
        adaylar.append((ek, frekans))

    adaylar.sort(key=lambda x: (-len(x[0]), -x[1], x[0]))
    return [ek for ek, _ in adaylar]

def ekleri_ayir(kelime, ekler):
    govde = kelime
    bulunan_ekler = []

    while len(govde) > 2:
        eslesen = None
        for ek in ekler:
            if govde.endswith(ek) and len(govde) - len(ek) >= 2:
                eslesen = ek
                break

        if not eslesen:
            break

        bulunan_ekler.append(eslesen)
        govde = govde[: -len(eslesen)]

    bulunan_ekler.reverse()
    return govde, bulunan_ekler

def parcala(kelime, ekler):
    govde, bulunan_ekler = ekleri_ayir(kelime, ekler)
    parcaciklar = hecele(govde)
    parcaciklar.extend(f"+{ek}" for ek in bulunan_ekler)
    return parcaciklar if parcaciklar else [kelime]