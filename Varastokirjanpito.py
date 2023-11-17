"""
Projekti: Varastokirjanpito. Ohjelma ylläpitää tuotevaraston kirjanpitoa,
jossa jokainen tuote on identifioitu spesifisellä tuotekoodilla.
Ohjelman käyttöliittymä mahdollistaa tuotevaraston kaikkien tuotteiden
sekä tuotekoodikohtaisten tuotteiden tulostamisen että kriittisen varastosaldo-
rajan alle pudonneiden tuotteiden tarkastelun, tuotteiden varastosaldon
ja hinnan muokkauksen sekä mahdollisuuden yhdistää että poistaa tuotteita.
"""

# Globaali vakio kriittiselle varastosaldolle.
LOW_STOCK_LIMIT = 30

class Product:
    """
    Luokassa määritellään varastokirjanpidon tuotteille oliokohtaisesti
    rakentajassa määritellyt ominaisuudet sekä ohjelman käyttöliittymän
    toiminnallisuuksia vastaavat metodit.
    """

    def __init__(self, code, name, category, price, stock):
        self.__code = code # Tuotekoodi.
        self.__name = name # Tuotteen nimi.
        self.__category = category # Tuotekategoria.
        self.__price = price # Tuotehinta.
        self.__stock = stock # Varastosaldo.
        self.__original_price = price # Tuotteen alkuperäinen hinta.

    def __str__(self):
        """
        Yhteydessä automaattisiin testeihin.
        """

        lines = [
            f"Code:     {self.__code}",
            f"Name:     {self.__name}",
            f"Category: {self.__category}",
            f"Price:    {self.__price:.2f}€",
            f"Stock:    {self.__stock} units",
        ]

        longest_line = len(max(lines, key=len))

        for i in range(len(lines)):
            lines[i] = f"| {lines[i]:{longest_line}} |"

        solid_line = "+" + "-" * (longest_line + 2) + "+"
        lines.insert(0, solid_line)
        lines.append(solid_line)

        return "\n".join(lines)

    def __eq__(self, other):
        """
        Yhteydessä automaattisiin testeihin (read_database -function)
        """

        return self.__code == other.__code and \
               self.__name == other.__name and \
               self.__category == other.__category and \
               self.__price == other.__price

    def modify_stock_size(self, amount):
        """
        Muuttaa oliokohtaisesti tuotteen varastosaldoa
        parametrin <amount> määräämän kappalemäärän verran.

        :param amount: int, käyttäjän syöttämä lukuarvo,
                       joka voi olla positiivinen
                       tai negatiivinen.
        """

        self.__stock += amount

    def print_products(self):
        """
        Tulostaa tuotetiedot oliokohtaisesti.
        """

        print(self)

    def delete_product(self):
        """
        Poistaa oliokohtaisen tuotteen varastokirjanpidosta
        palauttamalla paluuarvon True kutsuvalle funktiolle.

        Tuotetta ei voi poistaa varastokirjanpidosta mikäli sitä on jäljellä,
        tällöin metodi palauttaa False ja tulostuu virheilmoitus.
        Mikäli tuotteen varastosaldo on nolla tai negatiivinen luku,
        tuote voidaan poistaa ja metodi palauttaa True.

        :return: bool: True, mikäli tuote voidaan poistaa.
                       False, mikäli tuotetta ei voi poistaa.
        """

        if self.__stock > 0: # Varastosaldon tarkistus.
            print(f"Error: product '{self.__code}' can not be", end=" ")
            print("deleted as stock remains.")
            # Tuotetta oli jäljellä.
            return False

        elif self.__stock <= 0:
            # Tuote voidaan poistaa.
            return True

    def critical_product_balance(self):
        """
        Tulostaa oliokohtaisesti tuotetiedot mikäli
        tuotteen varastosaldo on pudonnut alle
        kriittisen 30 kappaleen rajan.
        """

        if self.__stock < LOW_STOCK_LIMIT: # Kriittisen rajan tarkitus.
            print(self)

    def combine_same_products(self, product_2):
        """
        Yhdistää kaksi samaan tuotekategoriaan ja hintaluokkaan
        kuuluvaa tuotetta yhdeksi tuotteeksi.

        Mikäli tuotteiden tuotekategoria tai hintaluokka ei ole
        yhteneväinen, yhdistäminen estetään ja tulostuu virheilmoitus.
        Muussa tapauksessa suoritetaan tuotteiden yhdistäminen ja
        palautetaan True, joka sallii kutsuvan funktion poistaa
        2. tuote <product_2> varastokirjanpidosta.

        :param product_2: int, tuotekoodi 2. tuotteelle.
        :return: bool: True, mikäli yhdistäminen onnistui.
                       False, muussa tapauksessa.
        """

        # Samaan kategoriaan kuuluvia tuotteita ei voi yhdistää.
        if self.__category != product_2.__category:
            print(f"Error: combining items of different categories", end=" ")
            print(f"'{self.__category}' and '{product_2.__category}'.")
            return False

        # Samaan hintaluokkaan kuuluvia tuotteita ei voi yhdistää.
        elif self.__price != product_2.__price:
            print(f"Error: combining items with different prices", end=" ")
            print(f"{self.__price}€ and {product_2.__price}€.")
            return False

        # Samassa tuote- ja hintaluokassa olevat tuotteet voidaan yhdistää.
        elif (self.__price.__eq__(product_2.__price) and
              self.__category.__eq__(product_2.__category)):

            self.__stock += product_2.__stock # Tuotteiden yhdistäminen.
            return True

    def set_category_discount(self, category, percentage):
        """
        Laskee kaikille parametrina annetun kategorian <category>
        tuotteille alennetun hinnan parametrina saadun alennusprosentin
        <percentage> mukaisesti.

        Mikäli alennusprosentti on yhtä suuri kuin 0.0, palautetaan
        kaikille kyseessä olevan kategorian tuotteille niiden
        alkuperäinen hinta. Mikäli alennusprosentti on eri suuri kuin 0.0,
        alennettu hinta realisoidaan uudeksi listahinnaksi
        alennusprosentin mukaisesti tuotteen alkuperäisestä hinnasta.

        :param category: str, käyttäjän syöttämä tuotekategoria.
        :param percentage: float, käyttäjän syöttämä alennusprosentti.
        :return: bool: True, mikäli tuotteelle asetettiin uusi hinta.
        """

        if self.__category == category: # Kategorian tarkistus.
            if percentage != float(0.0):
                # Alennusprosentin asettaminen.
                self.__price = self.__original_price * ((100 - percentage) / 100)
                return True

            elif percentage == float(0.0):
                # Alkuperäisen hinnan asettaminen.
                self.__price = self.__original_price
                return True

def error_check_to_print_products(warehouse, parameters):
    """
    Tuotekoodin <parameters> tietotyypin ja olemassaolon
    tarkistus.

    Mikäli tuotekoodi ei ole kokonaisluku tai sitä ei löydy
    varastokirjanpidosta, metodi palauttaa False ja tulostuu
    virheilmoitus.

    :param warehouse: dict, tuotetiedot sisältävä tietorakenne.
    :param parameters: int, käyttäjän syöttämä tuotekoodi.
    :return: bool: True, mikäli tarkistukset onnistuivat.
                   False, muussa tapauksessa.
    """

    try:
        code = int(parameters) # Tuotekoodin tietotyypin tarkistus.
        if code not in warehouse: # Tuotteen olemassaolon tarkistus.
            raise ValueError

        elif code in warehouse:
            # Tuote löytyy kirjanpidosta.
            return True

    # Tuotekoodin ollessa muu kuin kokonaisluku,
    # tai mikäli tuotetta ei löydy kirjanpidosta.
    except ValueError:
        print(f"Error: product '{parameters}' can not be", end=" ")
        print("printed as it does not exist.")

def error_check_to_modify_stock_size(warehouse, parameters):
    """
    Tarkistaa käyttäjän antaman tuotekoodin tietotyypin
    ja varmistaa että tuotekoodi löytyy varastokirjanpidosta.
    Lisäksi tarkistaa käyttäjän antaman lukumäärän tietotyypin.

    Mikäli tuotekoodi ole kokonaisluku tai sitä ei löydy varasto-
    kirjanpidosta, palautuu False ja tulostuu virheilmoitus.
    Lisäksi mikäli lukumäärä ei ole kokonaisluku, palautuu False
    ja tulostuu virheilmoitus.

    :param warehouse: dict, tuotetiedot sisältävä tietorakenne.
    :param parameters: int, tuotekoodi <code> ja lukumäärä <amount>
                       samassa merkkijonossa <parameters>.
    :return: bool: True, mikäli tuotemäärää voidaan muuttaa.
                   False, muussa tapauksessa.
    """

    try:
        code, amount = parameters.split()
        code = int(code) # Tuotekoodi.
        amount = int(amount) # Lukumäärä.

        if code not in warehouse: # Tuotteen olemassaolon tarkistus.
            raise KeyError

        elif code in warehouse:
            # Tuotteen varastosaldoa voidaan muuttaa.
            return True

    # Tuotekoodin tai lukumäärän ollessa muu kuin kokonaisluku.
    except ValueError:
        print(f"Error: bad parameters '{parameters}' for", end=" ")
        print("change command.")

    # Mikäli tuotetta ei löydy varastokirjanpidosta.
    except KeyError:
        print(f"Error: stock for '{code}' can not be changed", end=" ")
        print("as it does not exist.")

def error_check_to_delete_product(warehouse, parameters):
    """
    Tuotekoodin <parameters> tietotyypin tarkistus,
    sekä tuotteen olemassaolon tarkistus.

    Mikäli tuotekoodi ei ole kokonaisluku tai tuotetta ei löydy
    varastokirjanpidosta, metodi palauttaa False ja tulostaa
    virheilmoituksen.

    :param warehouse: dict, tuotetiedot sisältävä tietorakenne.
    :param parameters: int, käyttäjän syöttämä tuotekoodi.
    :return: bool: True, mikäli tuotteen poisto on sallittu.
                   False, mikäli havaitaan virhetilanne.
    """

    try:
        code = int(parameters) # Tuotekoodin tietotyypin tarkistus.

        if code not in warehouse: # Tuotteen olemassaolon tarkistus.
            raise ValueError

        elif code in warehouse:
            # Tuote löytyy kirjanpidosta.
            return True

    # Tuotekoodin ollessa muu kuin kokonaisluku,
    # tai mikäli tuotetta ei löydy kirjanpidosta.
    except ValueError:
        print(f"Error: product '{parameters}' can not be", end=" ")
        print("deleted as it does not exist.")

def error_check_to_combine_same_products(warehouse, parameters):
    """
    Tuotteiden 1. ja 2. tuotekoodien tietotyyppien tarkistus.
    Lisäksi tarkistaa löytyvätkö annetut tuotteet kirjanpidosta.

    Mikäli tuotteiden tietotyyppi ei ole kokonaisluku tai
    tuotteita ei löydy varastokirjanpidosta, tuotteiden yhdistäminen
    estetään ja tulostuu virheilmoitus.

    :param warehouse: dict, tuotetiedot sisältävä tietorakenne.
    :param parameters: int, 1. tuotteen tuotekoodi <code_1>
                       ja 2. tuotteen tuotekoodi <code_2>
                       samassa merkkijonossa <parameters>.
    :return: bool: True, mikäli tarkistusoperaatiot onnistuivat.
                   False, muussa tapauksessa.
    """

    try:
        # Soveltumattoman käyttäjäsyötteen tarkistus.
        if len(parameters.split()) > 2:
            raise KeyError

        # Parametrin <parameters> viipalointi muuttujiksi.
        code_1, code_2 = parameters.split()
        code_1 = int(code_1) # 1. tuotteen tuotekoodi.
        code_2 = int(code_2) # 2. tuotteen tuotekoodi.

        # Tuotteiden olemassaolon tarkistus.
        if code_1 not in warehouse or code_2 not in warehouse:
            raise ValueError

        elif code_1 == code_2: # Samoja tuotteita ei voi yhdistää.
            raise ValueError

        else:
            return True

    # Tuotekoodien ollessa muu kuin kokonaisluku
    # tai toisen puuttuessa kirjanpidosta.
    except ValueError:
        print(f"Error: bad parameters '{parameters}' for combine command.")

    # Soveltumaton käyttäjäsyöte.
    except KeyError:
        print(f"Error: bad command line 'combine {parameters}'.")

def error_check_to_category_discount(parameters):
    """
    Alennusprosentin tietotyypin tarkistus.

    Mikäli alennusprosentti on reaaliluku, metodi palauttaa True.
    Muussa tapauksessa palautuu False, ja tulostuu virheilmoitus.

    :param parameters: str, tuotteen kategoria <category> ja
                       float, kategorian alennusprosentti <sale_percentage>
                       samassa merkkijonossa <parameters>.
    :return: bool: True, mikäli tarkistusoperaatiot onnistuivat.
                   False, muussa tapauksessa.
    """

    try:
        # Määritetään muuttujat viipaloimalla parametri.
        category, sale_percentage = parameters.split()
        sale_percentage = float(sale_percentage) # Alennusprosentti.
        return True

    # Alennusprosentin ollessa muu kuin reaaliluku.
    except ValueError:
        print(f"Error: bad parameters '{parameters}' for sale command.")

def _read_lines_until(fd, last_line):
    """
    read_database -function relies on it's behaviour on this one.

    Reads lines from <fd> until the <last_line> is found.
    Returns a list of all the lines before the <last_line>
    which is not included in the list. Return None if
    file ends bofore <last_line> is found.
    Skips empty lines and comments (i.e. characeter '#'
    and everything after it on a line).

    :param fd: file, file descriptor the input is read from.
    :param last_line: str, reads lines until <last_line> is found.
    :return: list[str] | None
    """

    lines = []

    while True:
        line = fd.readline()

        if line == "":
            return None

        hashtag_position = line.find("#")
        if hashtag_position != -1:
            line = line[:hashtag_position]

        line = line.strip()

        if line == "":
            continue

        elif line == last_line:
            return lines

        else:
            lines.append(line)

def read_database(filename):
    """
    This function reads an input file which must be in the format
    explained in the assignment. Returns a dict containing
    the product code as the key and the corresponding Product
    object as the payload. If an error happens, the return value will be None.

    :param filename: str, name of the file to be read.
    :return: dict[int, Product] | None
    """

    data = {}

    try:
        with open(filename, mode="r", encoding="utf-8") as fd:

            while True:
                lines = _read_lines_until(fd, "BEGIN PRODUCT")
                if lines is None:
                    return data

                lines = _read_lines_until(fd, "END PRODUCT")
                if lines is None:
                    print(f"Error: premature end of file while reading '{filename}'.")
                    return None

                collected_product_info = {}

                for line in lines:
                    keyword, value = line.split(maxsplit=1)  # ValueError possible

                    if keyword in ("CODE", "STOCK"):
                        value = int(value)  # ValueError possible

                    elif keyword in ("NAME", "CATEGORY"):
                        pass  # No conversion is required for string values.

                    elif keyword == "PRICE":
                        value = float(value)  # ValueError possible

                    else:
                        print(f"Error: an unknown data identifier '{keyword}'.")
                        return None

                    collected_product_info[keyword] = value

                if len(collected_product_info) < 5:
                    print(f"Error: a product block is missing one or more data lines.")
                    return None

                product_code = collected_product_info["CODE"]
                product_name = collected_product_info["NAME"]
                product_category = collected_product_info["CATEGORY"]
                product_price = collected_product_info["PRICE"]
                product_stock = collected_product_info["STOCK"]

                product = Product(code=product_code,
                                  name=product_name,
                                  category=product_category,
                                  price=product_price,
                                  stock=product_stock)

                if product_code in data:
                    if product == data[product_code]:
                        data[product_code].modify_stock_size(product_stock)

                    else:
                        print(f"Error: product code '{product_code}' conflicting data.")
                        return None

                else:
                    data[product_code] = product

    except OSError:
        print(f"Error: opening the file '{filename}' failed.")
        return None

    except ValueError:
        print(f"Error: something wrong on line '{line}'.")
        return None

def main():
    # Ohjelma käynnistyy kysymällä syötetiedoston nimen.
    filename = input("Enter database name: ")

    warehouse = read_database(filename) # Syötetiedosto luetaan sanakirjaan.
    if warehouse is None:
        return

    while True:
        # Käyttäjä valitsee ohjelman toiminnallisuuden.
        command_line = input("Enter command: ").strip()

        if command_line == "":
            return

        # Toiminnallisuutta koskevat lisätiedot tallennetaan
        # muuttujaan <parameters> yhdeksi merkkijonoksi.
        command, *parameters = command_line.split(maxsplit=1)

        command = command.lower()

        if len(parameters) == 0:
            parameters = ""
        else:
            parameters = parameters[0]

        if "print".startswith(command) and parameters == "":
            # Kaikkien tuotteiden tuotetietojen tulostus.
            for code in sorted(warehouse):
                warehouse[code].print_products()

        elif "print".startswith(command) and parameters != "":
            # Parametrin tarkistus.
            if error_check_to_print_products(warehouse, parameters):
                code = int(parameters) # Tuotekoodi.
                warehouse[code].print_products() # Tuotetietojen tulostus.

        elif "delete".startswith(command) and parameters != "":
            # Parametrin tarkistus.
            if error_check_to_delete_product(warehouse, parameters):
                code = int(parameters) # Tuotekoodi.

                # Tuotteen olemassaolon tarkistus.
                if warehouse[code].delete_product():
                    del warehouse[code] # Tuotteen poisto.

        elif "change".startswith(command) and parameters != "":
            # Parametrin viipalointi ja tarkistus.
            if error_check_to_modify_stock_size(warehouse, parameters):
                code, amount = parameters.split()
                code = int(code) # Tuotekoodi.
                amount = int(amount) # Tuotemäärä.

                # Varastosaldon muutos.
                warehouse[code].modify_stock_size(amount)

        elif "low".startswith(command) and parameters == "":
            # Kriittisen varastosaldorajan alle pudonneiden
            # tuotteiden tulostus.
            for product_code in sorted(warehouse):
                warehouse[product_code].critical_product_balance()

        elif "combine".startswith(command) and parameters != "":
            # Syötetietojen <parameters> tarkistus.
            if error_check_to_combine_same_products(warehouse, parameters):
                code_1, code_2 = parameters.split()
                code_1 = int(code_1) # 1. tuotekoodi.
                code_2 = int(code_2) # 2. tuotekoodi.

                # Tuotetietojen tarkistus.
                if warehouse[code_1].combine_same_products(warehouse[code_2]):
                    # Tuotteiden yhdistämisen onnistuessa jälkimmäinen
                    # tuote poistetaan kirjanpidosta.
                    del warehouse[code_2]

        elif "sale".startswith(command) and parameters != "":
            n = 0 # Alennettujen tuotteiden lkm.

            # Syötetietojen <parameters> tarkistus.
            if error_check_to_category_discount(parameters):
                category, percentage = parameters.split()
                category = str(category) # Tuotekategoria.
                percentage = float(percentage) # Alennusprosentti.

                for code in warehouse:
                    # Uuden tuotehinnan asettaminen.
                    if warehouse[code].set_category_discount(category,
                                                             percentage):
                        n += 1

                # Tuotemäärälle <n> asetettiin uusi hinta.
                print(f"Sale price set for {n} items.")

        else:
            print(f"Error: bad command line '{command_line}'.")


if __name__ == "__main__":
    main()
