import os

def jatek_letrehozas():
    szervezo = input("Ki a szervező?: ")
    jatek_neve = input("Mi a játék megnevezése? (egyedinek kell lennie): ")
    resztvevok_szama = int(input("Hány résztvevő van?: "))
    
    resztvevok = []
    for i in range(resztvevok_szama):
        resztvevo_neve = input(f"{i + 1}. játékos neve: ")
        resztvevok.append(resztvevo_neve)

    esemenyek_szama = int(input("Hány esemény van?: "))
    
    esemenyek = []
    for i in range(esemenyek_szama):
        esemeny_neve = input(f"{i + 1}. esemény neve: ")
        esemenyek.append(esemeny_neve)

    with open("jatekok.txt", "a") as file:
        file.write(f"{szervezo};{jatek_neve};{resztvevok_szama};{esemenyek_szama};")
        file.write(";".join(resztvevok + esemenyek) + "\n")

    print("\nJáték sikeresen létrehozva!\n")

def fogadas_leadasa():
    resztvevo_neve = input("Felhasználó neve: ")
    jatek_neve = input("Játék megnevezése: ")
    
    # Ellenőrizze, hogy létezik-e a játék
    with open("jatekok.txt", "r") as file:
        jatekok = [sor.strip().split(";") for sor in file]

    jatek_letezik = False
    for jatek in jatekok:
        if jatek[1] == jatek_neve:
            jatek_letezik = True
            break

    if not jatek_letezik:
        print("A megadott játék nem található.")
        return

    # Ellenőrizze a játékos pontjait
    jatekos_pontok = 100  # Cserélje le a valódi pontlekérési logikával
    print(f"{resztvevo_neve} jelenleg {jatekos_pontok} ponttal rendelkezik.")

    # Fogadás leadása
    resztvevo_fogadasa = input("Mire fogadsz? (alany, esemény, érték): ").split(',')
    fogadas_osszeg = int(input("Mennyit fogadsz?: "))

    # Ellenőrizze, hogy a játékosnak van-e elég pontja
    if fogadas_osszeg > jatekos_pontok:
        print("Nincs elegendő pontod a fogadáshoz.")
        return

    # Mentse el a fogadást a fájlba
    with open("fogadasok.txt", "a") as file:
        file.write(f"{resztvevo_neve};{jatek_neve};{fogadas_osszeg};{';'.join(resztvevo_fogadasa)}\n")

    print("A fogadás sikeresen rögzítve!\n")

def jatek_lezarasa():
    szervezo = input("Add meg a szervező nevét: ")
    jatek_neve = input("Add meg a játék nevét, amit le szeretnél zárni: ")

    # Ellenőrizze, hogy a szervező helyes-e
    with open("jatekok.txt", "r") as file:
        jatekok = [sor.strip().split(";") for sor in file]

    jatek_talalt = False
    for jatek in jatekok:
        if jatek[0] == szervezo and jatek[1] == jatek_neve:
            jatek_talalt = True
            break

    if not jatek_talalt:
        print("A megadott játék nem található vagy nincs jogosultságod lezárni.")
        return

    # Gyűjtse össze az eredményeket
    eredmenyek = []
    for i in range(int(jatek[2])):
        resztvevo_neve = input(f"{i + 1}. játékos neve: ")
        esemeny_eredmenye = input(f"{i + 1}. esemény eredménye: ")
        eredmenyek.append((resztvevo_neve, esemeny_eredmenye))

    # Számolja ki és mentse el a pontszámokat
    with open("eredmenyek.txt", "a") as file:
        file.write(f"{jatek_neve}\n")
        for eredmeny in eredmenyek:
            resztvevo_neve, esemeny_eredmeny = eredmeny
            fogadas_eredmenyek = fogadas_eredmenyek_megkapasa(resztvevo_neve, jatek_neve, esemeny_eredmeny)
            osszpontszam = pontszam_szamolasa(fogadas_eredmenyek)
            file.write(f"{resztvevo_neve};{esemeny_eredmeny};{osszpontszam}\n")

    print("A játék eredményei sikeresen rögzítve!\n")

def fogadas_eredmenyek_megkapasa(resztvevo_neve, jatek_neve, esemeny_eredmeny):
    with open("fogadasok.txt", "r") as file:
        fogadasok = [sor.strip().split(";") for sor in file]

    fogadas_eredmenyek = []
    for fogadas in fogadasok:
        if fogadas[0] == resztvevo_neve and fogadas[1] == jatek_neve:
            resztvevo_fogadasa = fogadas[3].split(',')
            if esemeny_eredmeny in resztvevo_fogadasa:
                fogadas_eredmenyek.append((int(fogadas[2]), float(resztvevo_fogadasa[2])))

    return fogadas_eredmenyek

def pontszam_szamolasa(fogadas_eredmenyek):
    if not fogadas_eredmenyek:
        return 0

    osszpontszam = 0
    for fogadas in fogadas_eredmenyek:
        fogadas_osszeg, esemeny_ertek = fogadas
        pontszam = fogadas_osszeg * esemeny_ertek
        osszpontszam += pontszam

    return round(osszpontszam, 2)

def ranglista_megjelenitese():
    pontszamok = {}
    with open("eredmenyek.txt", "r") as file:
        eredmenyek = [sor.strip().split(";") for sor in file]

    for eredmeny in eredmenyek:
        resztvevo_neve, esemeny_eredmeny, osszpontszam = eredmeny
        if resztvevo_neve not in pontszamok:
            pontszamok[resztvevo_neve] = 0
        pontszamok[resztvevo_neve] += float(osszpontszam)

    rendezett_pontszamok = sorted(pontszamok.items(), key=lambda x: x[1], reverse=True)

    print("\nRanglista:")
    for i, (resztvevo, pontszam) in enumerate(rendezett_pontszamok, start=1):
        print(f"{i}. {resztvevo}: {int(pontszam)} pont")

def main():
    while True:
        print("1. Játék létrehozása")
        print("2. Fogadás leadása")
        print("3. Játék lezárása")
        print("4. Ranglista megjelenítése")
        print("5. Kilépés")

        valasztas = input("Válassz egy menüpontot (1-5): ")

        if valasztas == "1":
            jatek_letrehozas()
        elif valasztas == "2":
            fogadas_leadasa()
        elif valasztas == "3":
            jatek_lezarasa()
        elif valasztas == "4":
            ranglista_megjelenitese()
        elif valasztas == "5":
            print("Viszlát!")
            break
        else:
            print("Hibás választás, kérlek válassz újra.")

if __name__ == "__main__":
    main()
