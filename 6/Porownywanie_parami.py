import csv


def parametry_na_podstawie_witryny(witryna):

    if witryna == "geneid":
        #parametry = (plik, separator, numery_pozycji, czy_same_exony)
        parametry = ("geneid_predictions.txt", "\t", [3, 4, 6], 1)
    elif witryna == "augustus":
        parametry = ("augustus_predictions.txt", "\t", [3, 4, 6], 0)
    elif witryna == "genemark":
        parametry = ("genemark_predictions.txt", "\t", [3, 4, 6], 0)
    else:
        parametry = (f"{witryna}.txt", "\t", [3, 4, 6], 0)
        print(f"Nienznana witryna, zastosowano parametry {parametry}")

    return parametry


def pobieranie_danych(parametry):
    (plik, separator, numery_pozycji, czy_same_exony) = (parametry[0], parametry[1], parametry[2], parametry[3])
    witryna = plik.split("_")[0]

    # Tworzymy listy na zbieranie danych
    start = []
    end = []
    znak = []  # +/- polarnosc nici
    [poz_start, poz_end, poz_znak] = numery_pozycji

    with open(plik, newline='') as f:
        reader = csv.reader(f, delimiter=separator, quoting=csv.QUOTE_NONE)
        for row in reader:
            if row[0][0] != "#":    #Dzieki temu pomijamy nieistotne linijki bez separatorow
                if czy_same_exony == 1:
                    start.append(row[poz_start])
                    end.append(row[poz_end])
                    znak.append(row[poz_znak])
                elif czy_same_exony == 0 and ("exon" in row):
                    start.append(row[poz_start])
                    end.append(row[poz_end])
                    znak.append(row[poz_znak])


    lista_robocza = [witryna, start, end, znak]

    #Tworzymy slownik, zeby potem latwo bylo przeksztalcic to w tabele (uczylem sie na tym tez "pandas")
    slownik_dict= {
                 "algorytm": lista_robocza[0],
                 "start": tuple(lista_robocza[1]),
                 "end": tuple(lista_robocza[2]),
                 "znak": tuple(lista_robocza[3])
    }

    return slownik_dict     # type:dict

# stara funkcja
"""
def szukanie_konsensusu(slowniki, zakres_tolerancji):

    "@@@@@@@@@"''''
    #pobieranie_danych(zrodlo, plik, separator, numery_pozycji, czy_same_exony)
    slowniki[0] = pobieranie_danych("geneid", "geneid_predictions.txt", "\t", [3, 4, 6], 1)
    slowniki[1] = pobieranie_danych("augustus", "Oflankowane.txt", "\t", [3, 4, 6], 0)
    slowniki[2] = pobieranie_danych("genemark", "genemark_predictions.txt", "\t", [3, 4, 6], 0)
    '''
    wszystkie_exony_slowniki0 = []
    wszystkie_exony_slowniki1 = []
    wszystkie_exony_slowniki2 = []
    for k in range(len(slowniki[0]["znak"])):
        for l in range(len(slowniki[1]["znak"])):
            for m in range(len(slowniki[2]["znak"])):
                #Jezeli znaki (polarnosc nici) sa te same
                if (slowniki[0]["znak"][k]) == (slowniki[1]["znak"][l]) == (slowniki[2]["znak"][m]):
                    #Sprawdzamy czy poczatki i konce exonow roznia sie mniej niz o 100 miejsc
                    if (
                        abs(int(slowniki[0]["start"][k])  - int(slowniki[1]["start"][l])) < zakres_tolerancji and
                        abs(int(slowniki[0]["start"][k]) - int(slowniki[2]["start"][m])) < zakres_tolerancji and

                        abs(int(slowniki[0]["end"][k]) - int(slowniki[1]["end"][l])) < zakres_tolerancji and
                        abs(int(slowniki[0]["end"][k]) - int(slowniki[2]["end"][m])) < zakres_tolerancji
                    ):

                        pojedyncze_exony_geneid = [k, slowniki[0]["znak"][k], slowniki[0]["start"][k], slowniki[0]["end"][k]]
                        wszystkie_exony_slowniki0.append(pojedyncze_exony_geneid)

                        pojedyncze_exony_augustus = [l, slowniki[1]["znak"][l], slowniki[1]["start"][l], slowniki[1]["end"][l]]
                        wszystkie_exony_slowniki1.append(pojedyncze_exony_augustus)

                        pojedyncze_exony_genemark = [m, slowniki[2]["znak"][m], slowniki[2]["start"][m], slowniki[2]["end"][m]]
                        wszystkie_exony_slowniki2.append(pojedyncze_exony_genemark)

    return [wszystkie_exony_slowniki0, wszystkie_exony_slowniki1, wszystkie_exony_slowniki2]
"""
# koniec jej

def porownywanie(lista_slownikow, zakres_tolerancji, typ_porownywanego_elementu):

    #typ_porownywanego_elementu = [start, end, znak, ...]
    pierwsza = list(map(int, lista_slownikow[0][f"{typ_porownywanego_elementu}"]))
    druga = list(map(int, lista_slownikow[1][f"{typ_porownywanego_elementu}"]))

    wspolne_elementy = {f"{typ_porownywanego_elementu}": list()}

    if len(pierwsza) == min(len(pierwsza), len(druga)):

        for k in range(len(pierwsza)):
            # Skad wiemy ktora jest krotsza
            # if (pierwsza[k]-zakres_tolerancji in druga) or (pierwsza[k]+zakres_tolerancji in druga):
            # pierwsza[k] - 100

            liczby_z_przedzialu = list(range(pierwsza[k]-zakres_tolerancji, pierwsza[k]+zakres_tolerancji+1))

            for liczba in liczby_z_przedzialu:
                # jesli liczba z przedzialu jest w drugiej liscie oraz
                # znak odpowiadajacy liczbie z 1 listy oraz znak odpowiadajacy liczbie z drugiej listy sa te same
                if liczba in druga:
                    if lista_slownikow[0]["znak"][k] == lista_slownikow[1]["znak"][lista_slownikow[1][f"{typ_porownywanego_elementu}"].index(f"{liczba}")]:

                        # appendujemy mniejsza liczbe jesli END
                        # appendujemy wieksza liczbe jesli START
                        if typ_porownywanego_elementu == "start":
                            wspolne_elementy[typ_porownywanego_elementu].append((k, max(liczba, pierwsza[k])))  # starty
                            break
                        elif typ_porownywanego_elementu =="end":
                            wspolne_elementy[typ_porownywanego_elementu].append((k, min(liczba, pierwsza[k])))  # endy
                            break
                        else:
                            wspolne_elementy[typ_porownywanego_elementu].append((k, liczba))
                            break
    else:
        for k in range(len(druga)):
            liczby_z_przedzialu = list(range(pierwsza[k]-zakres_tolerancji, pierwsza[k]+zakres_tolerancji+1))

            for liczba in liczby_z_przedzialu:
                if liczba in druga:
                    if lista_slownikow[0]["znak"][k] == lista_slownikow[1]["znak"][lista_slownikow[1][f"{typ_porownywanego_elementu}"].index(f"{liczba}")]:

                        if typ_porownywanego_elementu == "start":
                            wspolne_elementy[typ_porownywanego_elementu].append((k, max(liczba, pierwsza[k])))  # starty
                            break
                        elif typ_porownywanego_elementu =="end":
                            wspolne_elementy[typ_porownywanego_elementu].append((k, min(liczba, pierwsza[k])))  # endy
                            break
                        else:
                            wspolne_elementy[typ_porownywanego_elementu].append((k, liczba))
                            break

    return wspolne_elementy #type:dict


def wez_znaki(slownik_startow, slownik_bazowy):

    znaki_wspolne = []

    for krotka in range(len(slownik_startow["start"])):
        indeks = slownik_startow["start"][krotka][0] #integer
        znak = slownik_bazowy["znak"][indeks]

        znaki_wspolne.append(znak)

    return tuple(znaki_wspolne)

# nie uzywam - proba przejscia na Pandy bedzie.
"""
def tworzenie_csv(lista_wszystkich_exonow):
    #Tworzenie Pliku CSV

    naglowek = ['NR', 'znak', 'start', 'end']

    with open("Wersja_ladniejsza.csv", 'w', newline="") as myfile:
        writer = csv.writer(myfile, delimiter=",")

        for i in range(len(lista_wszystkich_exonow)):

            #   Zapisujemy GENEID
            writer.writerow([f"Witryna {i}"])
            writer.writerow(naglowek)
            for skladnik in lista_wszystkich_exonow[i]:
                writer.writerow(skladnik)
            #   Pusty wiersz
            writer.writerow([])

        return "Utworzono plik CSV: \"Wersja_ladniejsza\""
        
"""


def slownik_z_pary(aaa, bbb, ccc):

    slownik_uzyskany_z_pary = {
        "algorytm": "Przez_porownanie",
        "start": tuple(aaa["start"][k][1] for k in range(len(aaa["start"]))),
        "end": tuple(bbb["end"][k][1] for k in range(len(bbb["end"]))),
        "znak": tuple(ccc),
        }

    return slownik_uzyskany_z_pary


def nazwa_nazwa(strony):

    slownik_uzyskany_z_pary = {}

    iteracja = 1
    while iteracja < len(strony):

        if len(slownik_uzyskany_z_pary) == 0:
            # Pobierz pierwsze dwa elementy z listy
            lista_parametrow = [parametry_na_podstawie_witryny(x) for x in [strony[0], strony[1]]]
            slowniki = [pobieranie_danych(x) for x in lista_parametrow]  # lista_slownikow

            lista_wszystkich_startow = porownywanie(lista_slownikow=slowniki, zakres_tolerancji=100, typ_porownywanego_elementu="start")
            lista_wszystkich_endow = porownywanie(lista_slownikow=slowniki, zakres_tolerancji=100, typ_porownywanego_elementu="end")
            lista_wszystkich_znakow = wez_znaki(lista_wszystkich_startow, slowniki[0])  # bierzemy z pierwszego slownika
            slownik_uzyskany_z_pary = slownik_z_pary(lista_wszystkich_startow, lista_wszystkich_endow, lista_wszystkich_znakow)

            iteracja += 1

        else:
            # Porownaj kolejny element z listy ze slownikiem

            parametry = parametry_na_podstawie_witryny(strony[iteracja])

            slowniki = [slownik_uzyskany_z_pary, pobieranie_danych(parametry)]

            # Dla sprawdzenia, czy dziala
            #print(slownik_uzyskany_z_pary)
            #print("###############")
            #print(pobieranie_danych(parametry))

            # Tworzenie slownika do porownania
            lista_wszystkich_startow = porownywanie(lista_slownikow=slowniki, zakres_tolerancji=100, typ_porownywanego_elementu="start")
            lista_wszystkich_endow = porownywanie(lista_slownikow=slowniki, zakres_tolerancji=100, typ_porownywanego_elementu="end")
            lista_wszystkich_znakow = wez_znaki(lista_wszystkich_startow, slowniki[0])  # bierzemy z pierwszego slownika

            slownik_uzyskany_z_pary = slownik_z_pary(lista_wszystkich_startow, lista_wszystkich_endow, lista_wszystkich_znakow)

            iteracja += 1

    return slownik_uzyskany_z_pary


def main():

    return nazwa_nazwa(["geneid", "augustus", "genemark"])

    #tworzenie_csv(lista_wszystkich_exonow)

    #return tworzenie_csv(lista_wszystkich_exonow)


print(
    main()
)
