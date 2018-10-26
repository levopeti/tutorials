import copy
import itertools


class Camel(object):
    def __init__(self, color):
        self.color = color
        self.place = 0
        self.active = True
        self.under = None
        self.top = None
        self.position = 0


class Table(object):
    def __init__(self, size):
        self.camels = {"red": Camel("red"),
                       "blue": Camel("blue"),
                       "yellow": Camel("yellow"),
                       "green": Camel("green"),
                       "white": Camel("white")}

        self.places = []
        for i in range(size + 1):
            self.places.append(Place(i))

    def pop_unit(self, number, color):
        place = self.places[number]

        for i in range(len(place.camel_unit)):
            if place.camel_unit[i].color == color:
                c_u = place.camel_unit[i:]
                place.camel_unit = place.camel_unit[:i]
                return c_u
        print("This place doesn't have this camel.")

    def add_unit(self, number, camel_unit, direction=None):
        place = self.places[number]

        if place.forward:
            self.add_unit(number + 1, camel_unit, direction="for")
        elif place.backward:
            self.add_unit(number - 1, camel_unit, direction="back")
        else:
            if direction == "back":
                place.camel_unit = camel_unit + place.camel_unit
                place.set()
            else:
                place.camel_unit = place.camel_unit + camel_unit
                place.set()

    def rank(self):
        rank_camels = []
        for place in self.places:
            if place.camel_unit:
                for camel in place.camel_unit:
                    rank_camels.append(camel.color)
        return rank_camels[::-1]


class Place(object):
    def __init__(self, number):
        self.number = number
        self.forward = False
        self.backward = False
        self.camel_unit = []  # index 0 - lowermost

    def set(self):
        for camel in self.camel_unit[::-1]:
            camel.place = self.number


class Game(object):
    def __init__(self):
        self.round = 0

        self.table = Table(30)

        self.commands = {"dice": self.dice,
                         "card": self.card,
                         "print": self.print,
                         "exit": self.exit}

        self.run_ind = True

        while not self.init():
            pass

    def init(self):
        colors = ["red", "blue", "yellow", 'green', "white"]
        for color in colors:
            number = input("Init of " + color + ' :')
            try:
                number = int(number)
            except ValueError:
                print("Index must be a number!")
                return False
            if 1 > number or 3 < number:
                print("Number must be between 1 and 3!")
                return False
            self.table.add_unit(number, [self.table.camels[color]])

        self.predict()
        return True

    def run(self):
        while self.run_ind:
            inp = input("\nType command: ")
            try:
                self.commands[inp]()
            except KeyError:
                print("Bad command. Type 'help' for the optional commands!")

    def dice(self):
        color = input("Color: ")
        number = int(input("Number: "))
        if number not in [1, 2, 3]:
            print("Number must be 1, 2 or 3!")
            return

        if color not in ["red", "blue", "green", "white", "yellow"]:
            print("Bad color!")
            return

        if not self.table.camels[color].active:
            print("This camel has stepped in this round!")
            return

        table_index = self.table.camels[color].place
        camel_unit = self.table.pop_unit(table_index, color)

        if table_index + number > 20:
            print("The", camel_unit[::-1][0].color, "camel win!")
            self.run_ind = False
            return

        self.table.add_unit(table_index + number, camel_unit)
        self.table.camels[color].active = False

        for color in ["red", "blue", "green", "white", "yellow"]:
            if self.table.camels[color].active:
                break
        else:
            print("End of round!")
            self.round += 1
            for color in ["red", "blue", "green", "white", "yellow"]:
                self.table.camels[color].active = True

            for place in self.table.places:
                place.forward = False
                place.backward = False

        self.predict()

    def card(self):
        direction = input("Direction (for/back/clear): ")
        number = input("Number: ")

        try:
            number = int(number)
        except ValueError:
            print("Index must be a number!")
            return

        if 0 > number or 20 < number:
            print("Number must be between 0 and 20!")
            return

        if self.table.places[number].camel_unit:
            print("This place has minimum 1 camel.")
            return

        if self.table.places[number + 1].backward or self.table.places[number + 1].forward or self.table.places[number - 1].backward or self.table.places[number - 1].forward:
            print("There is a card in the neighborhood of this place.")
            return

        if direction == "for":
            self.table.places[number].forward = True
            self.table.places[number].backward = False
        elif direction == "back":
            self.table.places[number].forward = False
            self.table.places[number].backward = True
        elif direction == "clear":
            self.table.places[number].forward = False
            self.table.places[number].backward = False
        else:
            print("Bad direction!")
            return

        self.predict()

    def predict(self):
        result = {"red": [0, 0, 0, 0, 0],
                  "blue": [0, 0, 0, 0, 0],
                  "yellow": [0, 0, 0, 0, 0],
                  "green": [0, 0, 0, 0, 0],
                  "white": [0, 0, 0, 0, 0]}

        sequences = []

        active_colors = []
        for color in ["red", "blue", "green", "white", "yellow"]:
            if self.table.camels[color].active:
                active_colors.append(color)

        print("Computing the prediction...")
        number_of_dice = len(active_colors)
        for dice_combo in itertools.product([1, 2, 3], repeat=number_of_dice):
            for color_combo in itertools.permutations(active_colors):
                table = copy.deepcopy(self.table)
                for i in range(number_of_dice):
                    table_index = table.camels[color_combo[i]].place
                    color = table.camels[color_combo[i]].color
                    camel_unit = table.pop_unit(table_index, color)
                    table.add_unit(table_index + dice_combo[i], camel_unit)
                    if table_index + dice_combo[i] > 20:
                        break
                sequences.append(table.rank())

        for i in range(5):
            for seq in sequences:
                for color in ["red", "blue", "green", "white", "yellow"]:
                    if seq[i] == color:
                        result[color][i] += 1 / len(sequences) * 100

        print("color\tno.1\tno.2\tno.3\tno.4\tno.5")
        for color in ["red", "blue", "green", "white", "yellow"]:
            print(color, "\t", int(result[color][0]), "% \t", int(result[color][1]), "% \t", int(result[color][2]), "% \t", int(result[color][3]), "% \t", int(result[color][4]), "%")

    def print(self):
        for place in self.table.places:
            if place.camel_unit:
                print(place.number, ':')
                for camel in place.camel_unit[::-1]:
                    print(camel.color)
                print()
            if place.forward:
                print(place.number, 'for')
            if place.backward:
                print(place.number, 'back')

    def exit(self):
        self.run_ind = False


if __name__ == "__main__":
    camel_cup = Game()
    camel_cup.run()



