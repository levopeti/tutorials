import os
import json
from random import shuffle


class Dictionary(object):
    def __init__(self, path):
        self.path = path
        if self.path:
            with open(self.path) as fin:
                self.dictionary = json.load(fin)
        elif os.path.isfile("dictionary.json"):
            with open("dictionary.json") as fin:
                self.dictionary = json.load(fin)
        else:
            self.dictionary = []

        self.commands = {"add": self.add,
                         "example": self.example,
                         "sentence": self.sentence,
                         "del": self.delete,
                         "correct": self.correct,
                         "meaning": self.meaning,
                         "test": self.test,
                         "print": self.print,
                         "clear": self.clear,
                         "save": self.save,
                         "reload": self.reload,
                         "help": self.help,
                         "exit": self.exit}

        self.run_ind = True

    def __del__(self):
        print("Good bye!")

    def run(self):
        while self.run_ind:
            inp = input("Type command: ")
            try:
                self.commands[inp]()
            except KeyError:
                print("Bad command. Type 'help' for the optional commands!")

    def add(self):
        english = input("english: ")
        hungarian = input("hungarian: ")
        new_dict = {"english": english,
                    "hungarian": hungarian,
                    "id": len(self.dictionary)}
        self.dictionary.append(new_dict)
        self.save()

    def example(self):
        index = int(input("index: "))
        if 0 > index or index > len(self.dictionary) - 1:
            print("Index out of range.")
            return
        english = input("english sentence: ")
        hungarian = input("hungarian sentence: ")
        self.dictionary[index]["e_sentence"] = english
        self.dictionary[index]["h_sentence"] = hungarian
        self.save()

    def sentence(self):
        index = self.index()
        if index == -1:
            return

        try:
            print(self.dictionary[index]["english"], '\t-->\t', self.dictionary[index]["hungarian"])
            print(self.dictionary[index]["e_sentence"], '\t-->\t', self.dictionary[index]["h_sentence"])
        except KeyError:
            print("This word doesn't have example sentence.\n")

    def delete(self):
        index = self.index()
        if index == -1:
            return

        d = self.dictionary[index]
        print("(id:", d["id"], '\t', d["english"], '\t-->\t', d["hungarian"], ") WAS DELETED.\n")

        self.dictionary.pop(index)
        self.save()

    def correct(self):
        index = int(input("index: "))
        if 0 > index or index > len(self.dictionary) - 1:
            print("Index out of range.")
            return

        d = self.dictionary[index]
        print("id:", d["id"], '\t', d["english"], '\t-->\t', d["hungarian"])
        print("Type only ENTER if any part does not change.")
        english = input("english: ")
        hungarian = input("hungarian: ")

        if english:
            d["english"] = english
        if hungarian:
            d["hungarian"] = hungarian
        self.save()

    def test(self):
        start = input("Start of range (ENTER -> first): ")

        if start == '':
            start = 0
        else:
            try:
                start = int(start)
            except ValueError:
                print("Start index is not correct!")
                return
            if start not in range(0, len(self.dictionary)):
                print("Start index is not correct!")
                return

        end = input("End of range (ENTER -> last): ")

        if end == '':
            end = len(self.dictionary)
        else:
            try:
                end = int(end)
            except ValueError:
                print("End index is not correct!")
                return
            if end not in range(0, len(self.dictionary)) or end < start:
                print("End index is not correct!")
                return

        test = self.dictionary[start:end]

        shuffle(test)
        print("You can leave the test with 'quit!'.")
        for d in test:
            print("hungarian: ", d["hungarian"])
            attempt = input("english: ")
            if attempt == "quit!":
                return

            if self.match(attempt, d["english"]):
                print("Right\n")
                try:
                    print("Example sentence:")
                    print(d["e_sentence"], '\t-->\t', d["h_sentence"], '\n')
                except KeyError:
                    print("This word doesn't have example sentence.\n")
            elif self.lev_dist(attempt, d["english"]) < 4:
                print("Do you think", d["english"], "?\n")
            else:
                print("Wrong")
                print(d["english"], '\n')

    def meaning(self):
        english = input("english: ")
        for d in self.dictionary:
            word = d["english"]
            if self.match(word, english):
                print(d["hungarian"])
                return

        prob_var = []
        for d in self.dictionary:
            word = d["english"]
            if self.lev_dist(word, english) < 4:
                prob_var.append(word)

        if prob_var:
            print("Do you think this/these?")
            for w in prob_var:
                print(w)
            return

        print("No match.")

    @staticmethod
    def match(w1, w2):
        if w1 == w2:
            return True
        else:
            return False

    @staticmethod
    def lev_dist(w1, w2):
        """Return the Levenshtein edit distance between two strings *w1* and *w2*."""
        if w1 == w2:
            return 0
        if len(w1) < len(w2):
            w1, w2 = w2, w1
        if not w1:
            return len(w2)
        previous_row = range(len(w2) + 1)
        for i, column1 in enumerate(w1):
            current_row = [i + 1]
            for j, column2 in enumerate(w2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (column1 != column2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    def save(self):
        if self.path:
            with open(self.path, 'w') as fout:
                json.dump(self.dictionary, fout)
        else:
            with open("dictionary.json", 'w') as fout:
                json.dump(self.dictionary, fout)

    def reload(self):
        if self.path:
            with open(self.path) as fin:
                self.dictionary = json.load(fin)
        elif os.path.isfile("dictionary.json"):
            with open("dictionary.json") as fin:
                self.dictionary = json.load(fin)

    def print(self):
        for d in self.dictionary:
            print("id:", d["id"], '\t',  d["english"], '\t-->\t', d["hungarian"])

    def clear(self):
        self.dictionary = []

    def help(self):
        print("Optional commands:")
        for c, _ in self.commands.items():
            print(c)

    def index(self):
        index = input("index: ")
        try:
            index = int(index)
        except ValueError:
            print("Index must be a number!")
            return -1
        if 0 > index or index > len(self.dictionary) - 1:
            print("Index out of range.")
            return -1
        return index

    def exit(self):
        self.run_ind = False


if __name__ == "__main__":
    def add_arguments(parser):
        parser.add_argument('--path', type=str)

    path = None
    dictionary = Dictionary(path)
    dictionary.run()



