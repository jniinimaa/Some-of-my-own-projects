"""
Projekti: Matkareitin optimoija. Ohjelma lukee syötetiedostosta kaupunkien
välisiä reittejä ja niiden välisiä etäisyyksiä, joista luodaan
dict-in-dict -tietorakenteeseen reittiopas. Käyttäjä voi halutessaan muuttaa
reittioppaassa olevia reittitietoja poistamalla tai lisäämällä kaupunkien
välisiä reittejä, sekä tarkastella kaikkia reittioppaassa olevia reittitietoja
että yksittäisiä kaupunkeja ja niiden välisiä etäisyyksiä.
"""

def remove_route(distance_data):
    """
    Funktio poistaa etäisyystietorakenteesta käyttäjän antaman
    lähtö- ja kohdekaupungin mukaisen reitin. Reitti poistuu tietorakenteesta
    käyttäjän antamaan suuntaan ja funktio palauttaa päivitetyn etäisyystieto-
    rakenteen.

    Lisäksi funktio tulostaa virheilmoituksen mikäli lähtökaupunki on
    tuntematon, tai jos kohdekaupunki on tuntematon tai lähtökaupungista
    ei ole suoraa yhteyttä kohdekaupunkiin.

    :param distance_data: dict[dict], etäisyystietorakenne
    :return: distance_data: dict[dict], päivitetty etäisyystietorakenne
    """
    departure = input("Enter departure city: ")

    # try-except-rakenteessa varmistetaan että lähtökaupunki löytyy
    # etäisyystietorakenteesta, ja varaudutaan ennalta suunniteltuun
    # virhetilanteeseen mikäli  lähtökaupunki on tuntematon.
    try:
        if departure not in distance_data:
            raise KeyError
    except KeyError:
        print(f"Error: '{departure}' is unknown.")
        return

    destination = input("Enter destination city: ")

    # if-rakenteessa poissuljetaan tilanne, jossa lähtökaupunki löytyy
    # etäisyystietorakenteesta mutta kohdekaupunki on tuntematon.
    # Tällöin ohjaudutaan if-rakenteen sisällä olevaan try-except-rakenteeseen
    # jossa nostetaan ennalta suunniteltu virhetilanne ja tulostetaan virheilmoitus.
    if departure in distance_data and destination not in distance_data[departure]:
        try:
            del distance_data[departure][destination]
        except KeyError:
            print(f"Error: missing road segment between '{departure}' and '{destination}'.")

    # Mikäli lähtö- että kohdekaupunki löytyy etäisyystietorakenteesta
    # mahdollisena reittinä, ohjaudutaan if-rakenteeseen jossa haluttu reitti
    # poistetaan etäisyystietorakenteesta. Päivitetty tietorakenne palautetaan.
    if departure in distance_data and destination in distance_data[departure]:
        del distance_data[departure][destination]
        return distance_data

def display_routes(distance_data):
    """
    Funktio tulostaa aakkosjärjestyksessä kaikki sellaiset reittioppaassa olevat
    etäisyystiedot, jossa kaupunkien välillä on määritelty suora yhteys.

    :param distance_data: dict[dict], etäisyystietorakenne
    :return:
    """
    # for-silmukka käy läpi lähtökaupungit aakkosjärjestetyssä etäisyystiedot
    # sisältävässä yhdistetyn sanakirjan ulommassa sanakirjassa.
    for departure in sorted(distance_data):
        # for-silmukka käy läpi kohdekaupungit aakkosjärjestetyssä sisemmässä
        # sanakirjassa, josta samalla valikoituu käytettäväksi kyseisen reitin etäisyys.
        for destination in sorted(distance_data[departure]):
            print(f"{departure:<14}{destination:<14}{distance_data[departure][destination]:>5}")

def add_route(distance_data):
    """
    Funktio lisää kaupunkien väliseen etäisyystietorakenteeseen käyttäjän
    määräämän lähtö- ja kohdekaupungin välisen yksisuuntaisen reitin
    ja palauttaa päivitetyn etäisyystietorakenteen ohjelman käyttöön.

    :param distance_data: dict[dict], etäisyystietorakenne.
    :return: distance_data: dict[dict], päivitetty etäisyystietorakenne.
    """
    departure = input("Enter departure city: ")
    destination = input("Enter destination city: ")
    distance = input(f"Distance: ")

    try:
        # try-except-rakenteen if-ehdossa tarkistetaan onko käyttäjän antamaa
        # reittiä jo ennalta etäisyystietorakenteessa, jolloin kyseisen reitin
        # etäisyystieto vain päivitetään.
        if departure in distance_data:
            distance_data[departure][destination] = int(distance)

        # Mikäli reittiä ei ennalta ole etäisyystiedoissa, muodostetaan
        # elif-ehtorakenteessa uusi reitti ja se lisätään etäisyystietorakenteeseen.
        elif departure not in distance_data:
            data = {}
            data[destination] = int(distance)
            distance_data[departure] = data

        return distance_data

    # except-osassa varaudutaan virhetilanteeseen, mikäli etäisyytenä syötetään
    # kokonaisluvusta poikkeava arvo.
    except ValueError:
        print(f"Error: '{distance}' is not an integer.")

def find_route(data, departure, destination):
    """
    This function tries to find a route between <departure>
    and <destination> cities. It assumes the existence of
    the two functions fetch_neighbours and distance_to_neighbour
    (see the assignment and the function templates below).
    They are used to get the relevant information from the data
    structure <data> for find_route to be able to do the search.

    The return value is a list of cities one must travel through
    to get from <departure> to <destination>. If for any
    reason the route does not exist, the return value is
    an empty list [].

    :param data: dict[dict], etäisyystietorakenne.
    :param departure: str, lähtökaupungin nimi.
    :param destination: str, kohdekaupungin nimi.
    :return: list[str], lista jonka alkioina ovat reitin muodostamat
             kaupungit. Funktio palauttaa tyhjän listan mikäli haettua reittiä
             ei ole olemassa. Lisäksi mikäli lähtö- että kohdepaunki ovat samat,
             funktio palauttaa listan jonka ainoat kaksi alkiota ovat
             lähtökaupunki kahdesti.
    """

    if departure not in data:
        return []

    elif departure == destination:
        return [departure, destination]

    greens = {departure}
    deltas = {departure: 0}
    came_from = {departure: None}

    while True:
        if destination in greens:
            break

        red_neighbours = []
        for city in greens:
            for neighbour in fetch_neighbours(data, city):
                if neighbour not in greens:
                    delta = deltas[city] + distance_to_neighbour(data, city, neighbour)
                    red_neighbours.append((city, neighbour, delta))

        if not red_neighbours:
            return []

        current_city, next_city, delta = min(red_neighbours, key=lambda x: x[2])

        greens.add(next_city)
        deltas[next_city] = delta
        came_from[next_city] = current_city

    route = []
    while True:
        route.append(destination)
        if destination == departure:
            break
        destination = came_from.get(destination)

    return list(reversed(route))

def read_distance_file(input_file):
    """
    Funktio lukee käyttäjän syötteen mukaisen tiedoston <input_file>
    ja tallentaa tiedoston sisältämät etäisyystiedot yhdistettyyn sanakirjaan niin,
    että ulompi sanakirja sisältää avaimena lähtökaupungin ja puolestaan sisempi
    sanakirja sisältää toisena avaimena lähtökaupunkia vastaavan kohdekaupungin.
    Lopullinen hyötykuorma vastaa tätä lähtö- ja kohdekaupungin mukaista suoran
    reitin etäisyyttä. Lopullinen etäisyystietorakenne palautetaan ohjelman
    käyttöön, mikäli tiedoston käsittelyssä ei esiinny virhetilannetta.

    :param input_file: str, syötetiedoston nimi.
    :return: dict[dict] | None: <index>, etäisyystiedot sisältävä tietorakenne,
             tai None mikäli tiedoston käsittelyssä esiintyy virhe.
    """
    try:
        file = open(input_file, mode="r", encoding="utf-8")

        # Sanakirjan alustus
        index = {}

        # for-silmukka käy läpi syötetiedoston riveittäin.
        for row in file:
            # Poistetaan for-silmukan kierroksella olevasta merkkijonosta
            # sanavälejä esittävät merkit.
            row = row.rstrip()
            # Luodaan muuttujat lähtö- ja kohdekaupungille sekä etäisyydelle
            # viipaloimalla rivi halutun merkin kohdalta.
            departure, destination, distance = row.split(";")

            # if-ehtorakenteessa tarkistetaan löytyykö aiemmin alustetusta
            # sanakirjasta käsiteltävänä olevaa lähtökaupunkia, ja jos, niin
            # muodostetaan sisemmän sanakirjan avaimeksi tätä vastaava kohdekaupunki
            # ja hyötykuormaksi kyseisen suoran reitin etäisyys.
            if departure in index:
                data = {}
                data[destination] = distance
                index[departure].update(data)

            # Mikäli käsiteltävänä olevaa lähtökaupunkia ei ole ennestään
            # ulommassa sanakirjassa, lisätään kyseinen lähtökaupunki
            # uutena avaimena ulompaan sanakirjaan ja tätä vastaava kohde-
            # kaupunki toisena avaimena sisempään sanakirjaan, hyötykuorman
            # ollessa kyseisen reitin etäisyys.
            elif departure not in index:
                data = {}
                data[destination] = distance
                index[departure] = data

        file.close()
        return index

    except FileNotFoundError:
        return None

    except NameError:
        return None

def fetch_neighbours(distance_data, city):
    """
    Funktio käsittelee etäisyystietorakenteessa olevat parametrina annetun
    lähtökaupungin kaikki naapurikaupungit ja palauttaa listan,
    jonka alkiot koostuvat kaikista näistä naapurikaupungeista. Mikäli
    lähtökaupunki on tuntematon tai lähtökaupungista ei ole yhteyksiä
    naapurikaupunkeihin, palautetaan tyhjä lista.

    :param distance_data: dict[dict], etäisyystietorakenne
    :param city: str, lähtökaupunki jonka naapurikaupunkeja
           halutaan tarkastella
    :return: list[str] | []: parametrina annetun lähtökaupungin
             kaikki naapurikaupungit listamuodossa, tai tyhjä lista mikäli
             lähtökaupunki on tuntematon/lähtökaupungista ei ole
             yhteyksiä naapurikaupunkeihin
    """
    try:
        # if-ehtorakenne tarkistaa löytyykö parametrina annettua
        # lähtökaupunkia etäisyystietorakenteesta.
        if city not in distance_data:
            empty_list = []
            return empty_list
        else:
            # Mikäli lähtökaupunki on etäisyystietorakenteessa, muodostetaan
            # tyhjä lista johon lisätään alkioina kaikki naapurikaupungit.
            list = []
            for destination in sorted(distance_data[city]):
                neighbours = destination
                list.append(neighbours)
            return list

    # Varaudutaan virhetilanteeseen mikäli lähtökaupunki on tuntematon.
    except KeyError:
        print(f"Error: '{city}' is unknown.")


def distance_to_neighbour(data, departure, destination):
    """
    Funktio palauttaa kahden naapurikaupungin välisen etäisyyden.
    Palauttaa None, mikäli lähtökaupungista <departure> ei ole
    suoraa yhteyttä kohdekaupungiin <destination>.

    :param data: dict[dict], etäisyystietorakenne
    :param departure: str, lähtökaupunki
    :param destination: str, kohdekaupunki
    :return: int | None, etäisyys kahden naapurikaupungin
             <departure> ja <destination> välillä. None mikäli
             suoraa yhteyttä ei ole annettujen kaupunkien välillä.
    """
    if departure not in data:
        return None
    elif departure == destination:
        return 0
    elif destination not in data[departure]:
        return None
    else:
        return int(data[departure][destination])

def routes_whole_distance(distance_data, departure, destination):
    """
    Funktio tulostaa lähtökaupungin <departure> ja kohdekaupungin
    <destination> välisen reitin sekä sen kokonaispituuden. Funktion
    toiminnallisuus on jaettu myös poikkeustilanteita varten, mikäli
    lähtö- että kohdekaupunki on sama tai annettua reittiä ei ole olemassa.

    :param distance_data: dict[dict], etäisyystietorakenne
    :param departure: str, lähtökaupunki
    :param destination: str, kohdekaupunki
    :return:
    """
    # find_route-funktio palauttaa muuttujalle <route> listan kaupungeista
    # joista varsinainen reitti muodostuu.
    route = find_route(distance_data, departure, destination)

    if len(route) == 2 and departure == destination:
        print(f"{departure}-{departure} (0 km)")
    elif route == []:
        print(f"No route found between '{departure}' and '{destination}'.")
    else:
        sum = 0
        # Listan alkioina olevat kaupungit yhdistetään yhdeksi
        # merkkijonoksi väliviivalla eroteltuina.
        route = "-".join(find_route(distance_data, departure, destination))

        # Merkkijono viipaloidaan yksittäisiksi kaupungeiksi.
        route_slice = route.split("-")

        # for-silmukka laskee annetun reitin kokonaispituuden viipaleiden avulla.
        for i in range(route.count("-")):
            lenght = int(distance_data[route_slice[i]][route_slice[i + 1]])
            sum += lenght

        print(f"{route} ({sum} km)")

def neighbours(distance_data):
    """
    Funktio tulostaa käyttäjän antaman lähtökaupungin <city> kaikki
    suorat yhteydet naapurikaupunkeihin aakkosjärjestyksessä. Mikäli syötetty
    lähtökaupunki on tuntematon, funktio tulostaa virheilmoituksen. Lisäksi
    mikäli suoria reittejä naapurikaupunkeihin ei ole olemassa,
    yhteyksiä ei tulostu.

    :param distance_data: dict[dict], etäisyystietorakenne
    :return:
    """
    try:
        city = input("Enter departure city: ")

        # Alustetaan tarkistuslista.
        lista = []

        # Koska tunnettu lähtökaupunki on sellainen kaupunki, johon on koskaan
        # viitattu lähtö- tai kohdekaupunkina, muodostetaan kaksi sisäkkäistä
        # for-silmukkaa yhdistetylle sanakirjalle ja kerätään kaupungit listaan.
        for depart in distance_data:
            lista.append(depart)
            for dest in distance_data[depart]:
                lista.append(dest)

        # Mikäli lähtökaupunki on tuntematon, tulostuu virheilmoitus, muussa
        # tapauksessa funktion suoritus jatkuu.
        if city not in lista:
            raise KeyError

        # fetch_neighbours-funktio palauttaa listan annetun lähtökaupungin
        # kaikista naapurikaupungeista muuttujalle <list_of_neighbours>.
        # Mikäli reittiä ei ole olemassa, palautuu tyhjä lista.
        list_of_neighbours = fetch_neighbours(distance_data, city)

        # for-silmukka käsittelee listassa olevat naapurikaupungit
        # ja tulostaa yhteydet naapurikaupunkeihin aakkosjärjestyksessä.
        for i in sorted(list_of_neighbours):
            print(f"{city:<14}{i:<14}{distance_data[city][i]:>5}")

    except KeyError:
        print(f"Error: '{city}' is unknown.")

def route(distance_data):
    """
    Funktion avulla kutsutaan routes_whole_distance-funktiota, joka tulostaa
    lähtökaupungin <departure> ja kohdekaupungin <destination> välisen
    reitin sekä kyseisen reitin kokonaispituuden. Tämä funktio kuitenkin
    jo varautuu mahdolliseen virhetilanteeseen, ja tulostaa virheilmoituksen
    mikäli annettu lähtökaupunki on tuntematon.

    :param distance_data: dict[dict], etäisyystietorakenne
    :return:
    """
    # try-except-rakenteessa poissuljetaan tuntemattoman
    # lähtökaupungin mahdollisuus.
    try:
        departure = input("Enter departure city: ")

        # Alustetaan tarkistuslista.
        lista = []

        # Koska tunnettu lähtökaupunki on sellainen kaupunki, johon on koskaan
        # viitattu lähtö- tai kohdekaupunkina, muodostetaan kaksi sisäkkäistä
        # for-silmukkaa yhdistetylle sanakirjalle ja kerätään kaupungit listaan.
        for depart in distance_data:
            lista.append(depart)
            for dest in distance_data[depart]:
                lista.append(dest)

        # Mikäli lähtökaupunki on tuntematon, syntyy virhetilanne, muussa
        # tapauksessa ohjelman suoritus jatkuu.
        if departure not in lista:
            raise KeyError

        destination = input("Enter destination city: ")

        # Varsinaisen reitin tulostaminen tapahtuu routes_whole_distance-funktiossa.
        routes_whole_distance(distance_data, departure, destination)

    except KeyError:
        print(f"Error: '{departure}' is unknown.")

def main():
    # Ohjelma käynnistyy kysymällä syötetiedoston nimeä.
    input_file = input("Enter input file name: ")

    # Etäisyystietorakenne luodaan muuttujaan <distance_data>.
    distance_data = read_distance_file(input_file)

    # Mikäli syötetiedostoa käsittelevä funktio palauttaa arvon None,
    # tulostuu virheilmoitus ja ohjelman suoritus keskeytyy.
    if distance_data is None:
        print(f"Error: '{input_file}' can not be read.")
        return

    while True:
        # Käyttäjän valitsema toiminnallisuus.
        action = input("Enter action> ")

        # Ohjelman suoritus keskeytyy välilyönnillä.
        if action == "":
            print("Done and done!")
            return

        # display-komennolla tulostetaan kaikki etäisyystiedot.
        elif "display".startswith(action):
            display_routes(distance_data)

        # add-komennolla lisätään etäisyystietoihin uusi yhteys.
        elif "add".startswith(action):
            add_route(distance_data)

        # remove-komennolla poistetaan etäisyystiedoista haluttu yhteys.
        elif "remove".startswith(action):
            remove_route(distance_data)

        # neighbours-komennolla tulostetaan halutusta kaupungista kaikki
        # suorat yhteydet naapurikaupunkeihin.
        elif "neighbours".startswith(action):
            neighbours(distance_data)

        # route-komennolla tulostetaan kahden kaupungin välinen reitti
        # sekä reitin kokonaispituus.
        elif "route".startswith(action):
            route(distance_data)

        else:
            print(f"Error: unknown action '{action}'.")

if __name__ == "__main__":
    main()
