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
        
        if len(kelimeler) > 0:
            sonuc.append(kelimeler)

    return sonuc