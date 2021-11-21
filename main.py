import json

class AutomatFinit():
    def __init__(self, stari, alfabet, tranziti, stare_initiala, stari_finale ):
        self.stari = stari
        self.alfabet = alfabet
        self.tranziti = {}
        for elem in tranziti:
            self.tranziti[(elem[0], elem[1])] = elem[2]
        self.stare_initiala = stare_initiala
        self.stari_finale = stari_finale

    def print_automat(self):
        print(f"Starile: {self.stari}")
        print(f"Alfabetul de intrare: {self.alfabet}")
        print("Functii de tranzitie: ")
        for key, value in self.tranziti.items():
            print(f"    {key} -> {value} ")
        print()
        print(f"Stare initiala: {self.stare_initiala}")
        print(f"Stari finale: {self.stari_finale}")

    def destinatie(self, stare, simbol):
        for tranzitie in self.tranziti:
            if tranzitie[0] == stare and tranzitie[1] == simbol:
                return self.tranziti[tranzitie]
        return None

    def este_secventa_valida(self, stare, secventa, poz, drum_parcurs):
        """
         Verifica in mod recursiv daca secventa este valida
        :param stare: Starea in care ne aflam
        :param secventa: Secventa pe care o validam
        :param poz: Pozitia simbolului curent din secventa
        :param drum_parcurs, o lista care va tine minte toate starile prin care am trecut
        :return: 1 Daca secventa este acceptata , 0 daca nu este acceptata
        """
        # Obtinem toate destinatile posibile din stare cu sinbolul cu pozitia poz din secenta data
        destinatii = self.destinatie(stare, secventa[poz])
        # print(destinatii)
        if destinatii is None:  # daca nu gasim nici o destinatie e clar ca nu mai putem continua pe drumul acesta
            return 0
        # Conditia de iesire: practim verificam daca la untima pozitie avem in destinatii un element care se afla in
        #       starile finale. Daca da returnam 1, daca nu inseamna ca drumul ales e gresit si ne intoarcem
        if poz == len(secventa)-1:
            for elem in destinatii:
                if elem in self.stari_finale:
                    return 1
            return 0
        # Partea recusiva: aici cautam un drum astfel incat sa validam secventa
        # O sa luat toate starile din destinatii si verificam daca pe una din ele pot ajunge cumva la o stare final
        # cu un ultimul simbol din secventa
        for elem in destinatii:
            print(drum_parcurs)
            aux = self.este_secventa_valida(elem, secventa, poz + 1, drum_parcurs + elem)
            if aux == 1:
                # print(drum_parcurs)
                return 1
        return 0

    def verificare_secventa(self, secventa):
        """
        Wraper pt functia este_secventa
        :param secventa: O adunatura de simboluri
        :return:
        """
        # aacd S a -> []
        return "Valid" if self.este_secventa_valida('S', secventa, 0, 'S') else "Invalid"


def main():
    with open("automat_finit.json") as f:
        data = dict(json.load(f))

    at = AutomatFinit(data['stari'], data['alfabet'], data['tranziti'],
                      data['stare_initiala'], data['stari_finale'])

    at.print_automat()
    simbol = "a"
    stare = "S"
    # aici primim un simbol si o stare . Cautam destinatia
    print(f"Tranzitile din starea {stare} cu simbolul {simbol} sunt {at.destinatie(stare, simbol)}")
    secventa = input("Dati secventa: ")
    print(at.verificare_secventa(secventa))


if __name__ == '__main__':
    main()