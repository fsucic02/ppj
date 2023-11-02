import sys
spec = [
        'OP_PRIDRUZI',
        'OP_PLUS',
        'OP_MINUS',
        'OP_PUTA',
        'OP_DIJELI',
        'L_ZAGRADA',
        'D_ZAGRADA', 
        'KR_ZA', 
        'KR_OD', 
        'KR_DO', 
        'KR_AZ',
        'IDN'
        ]

tablica = {
    ("<program>", "IDN"): 1,
    ("<program>", "KR_ZA"): 1,
    ("<program>", "!"): 1,
    ("<lista_naredbi>", "IDN"): 2,
    ("<lista_naredbi>", "KR_ZA"): 2,
    ("<lista_naredbi>", "KR_AZ"): 3,
    ("<lista_naredbi>", "!"): 3,
    ("<naredba>", "IDN"): 4,
    ("<naredba>", "KR_ZA"): 5,
    ("<naredba_pridruzivanja>", "IDN"): 6,
    ("<za_petlja>", "KR_ZA"): 7,
    ("<E>", "IDN"): 8,
    ("<E>", "BROJ"): 8,
    ("<E>", "OP_PLUS"): 8,
    ("<E>", "OP_MINUS"): 8,
    ("<E>", "L_ZAGRADA"): 8,
    ("<E_lista>", "IDN"): 3,
    ("<E_lista>", "OP_PLUS"): 9,
    ("<E_lista>", "OP_MINUS"): 9,
    ("<E_lista>", "D_ZAGRADA"): 3,
    ("<E_lista>", "KR_ZA"): 3,
    ("<E_lista>", "KR_DO"): 3,
    ("<E_lista>", "KR_AZ"): 3,
    ("<E_lista>", "!"): 3,
    ("<T>", "IDN"): 10,
    ("<T>", "BROJ"): 10,
    ("<T>", "OP_PLUS"): 10,
    ("<T>", "OP_MINUS"): 10,
    ("<T>", "L_ZAGRADA"): 10,
    ("<T_lista>", "IDN"): 3,
    ("<T_lista>", "OP_PLUS"): 3,
    ("<T_lista>", "OP_MINUS"): 3,
    ("<T_lista>", "OP_PUTA"): 11,
    ("<T_lista>", "OP_DIJELI"): 11,
    ("<T_lista>", "D_ZAGRADA"): 3,
    ("<T_lista>", "KR_ZA"): 3,
    ("<T_lista>", "KR_DO"): 3,
    ("<T_lista>", "KR_AZ"): 3,
    ("<T_lista>", "!"): 3,
    ("<P>", "IDN"): 14,
    ("<P>", "BROJ"): 14,
    ("<P>", "OP_PLUS"): 12,
    ("<P>", "OP_MINUS"): 12,
    ("<P>", "L_ZAGRADA"): 13,
    ("IDN", "IDN"): 14,
    ("OP_PRIDRUZI", "OP_PRIDRUZI"): 14,
    ("KR_OD", "KR_OD"): 14,
    ("KR_DO", "KR_DO"): 14,
    ("KR_AZ", "KR_AZ"): 14,
    ("D_ZAGRADA", "D_ZAGRADA"): 14,
    ("#", "!"): 15
}

def zamijeni_zadrzi(lista, stog, indent, ispis):
    temp = stog.pop()
    ispis.append(f"{indent * ' '}{temp}")
    indent += temp.startswith('<')
    for arg in lista:
        stog.append(arg)
    return stog, indent, ispis
    
def izvuci_zadrzi(stog, indent, ispis):
    temp = stog.pop()
    ispis.append(f"{indent * ' '}{temp}")
    indent += temp.startswith('<')
    stog.append("minus")
    ispis.append(f"{indent * ' '}$")
    return stog, indent, ispis

def zamijeni_pomakni(lista, stog, indent, ispis, redak):
    temp = stog.pop()
    ispis.append(f"{indent * ' '}{temp}")
    indent += temp.startswith('<')
    for arg in lista:
        stog.append(arg)
    redak += 1
    return stog, indent, ispis, redak

def izvuci_pomakni(stog, indent, ispis, redak):
    temp = stog.pop()
    if temp not in spec:
        ispis.append(f"{indent * ' '}{temp}")
    indent += temp.startswith('<')
    redak += 1
    return stog, indent, ispis, redak

def prihvati(ispis):
    for line in ispis:
        print(line)
    sys.exit(0)

def kraj(redak, n, linije):
    if redak == n-1:
        print("err kraj")
    else:
        print(f"err {linije[redak]}")
    sys.exit(0)

def main():
    stog = ["#", "<program>"]
    redak = 0
    indent = 0
    ispis = []
    linije = []
    for linija in sys.stdin:
        linija = linija.strip()
        linije.append(linija)
    linije.append("!")
    n = len(linije)

    while redak < n:
        top = stog[-1]
        if top == "minus":
            stog.pop()
            indent -= 1
            continue
        identifikator = linije[redak].split(" ")[0]
        funkcija = tablica.get((top, identifikator), [])
        if funkcija == 1:
            stog, indent, ispis = zamijeni_zadrzi(["minus", "<lista_naredbi>"], stog, indent, ispis)
        elif funkcija == 2:
            stog, indent, ispis = zamijeni_zadrzi(["minus", "<lista_naredbi>", "<naredba>"], stog, indent, ispis)
        elif funkcija == 3:
            stog, indent, ispis = izvuci_zadrzi(stog, indent, ispis)
        elif funkcija == 4:
            stog, indent, ispis = zamijeni_zadrzi(["minus", "<naredba_pridruzivanja>"], stog, indent, ispis)
        elif funkcija == 5:
            stog, indent, ispis = zamijeni_zadrzi(["minus", "<za_petlja>"], stog, indent, ispis)
        elif funkcija == 6:
            stog, indent, ispis, redak = zamijeni_pomakni(["minus", "<E>", "OP_PRIDRUZI"], stog, indent, ispis, redak)
            ispis.append(f"{indent * ' '}{linije[redak-1]}")
        elif funkcija == 7:
            stog, indent, ispis, redak = zamijeni_pomakni(["minus", "KR_AZ", "<lista_naredbi>", "<E>", "KR_DO", "<E>", "KR_OD", "IDN"], stog, indent, ispis, redak)
            ispis.append(f"{indent * ' '}{linije[redak-1]}")
        elif funkcija == 8:
            stog, indent, ispis = zamijeni_zadrzi(["minus", "<E_lista>", "<T>"], stog, indent, ispis)
        elif funkcija == 9:
            stog, indent, ispis, redak = zamijeni_pomakni(["minus", "<E>"], stog, indent, ispis, redak)
            ispis.append(f"{indent * ' '}{linije[redak-1]}")
        elif funkcija == 10:
            stog, indent, ispis = zamijeni_zadrzi(["minus", "<T_lista>", "<P>"], stog, indent, ispis)
        elif funkcija == 11:
            stog, indent, ispis, redak = zamijeni_pomakni(["minus", "<T>"], stog, indent, ispis, redak)
            ispis.append(f"{indent * ' '}{linije[redak-1]}")
        elif funkcija == 12:
            stog, indent, ispis, redak = zamijeni_pomakni(["minus", "<P>"], stog, indent, ispis, redak)
            ispis.append(f"{indent * ' '}{linije[redak-1]}")
        elif funkcija == 13:
            stog, indent, ispis, redak = zamijeni_pomakni(["minus", "D_ZAGRADA", "<E>"], stog, indent, ispis, redak)
            ispis.append(f"{indent * ' '}{linije[redak-1]}")
        elif funkcija == 14:
            stog, indent, ispis, redak = izvuci_pomakni(stog, indent, ispis, redak)
            ispis.append(f"{indent * ' '}{linije[redak-1]}")
            if top == "<P>":
                indent -= 1
        elif funkcija == 15:
            prihvati(ispis)
        else:
            kraj(redak, n, linije)

if __name__ == "__main__":
    main()