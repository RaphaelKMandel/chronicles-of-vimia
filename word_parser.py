class WordParser:
    SPECIAL = "{}[]():,.'\"-+/"

    def __str__(self):
        return str([self.words, self.ind])

    def __init__(self, text):
        self.text = text
        self.state = None
        self.words = self.get_words()
        self.ind = self.get_ind()

    def get_words(self):
        word = ""
        words = []
        for char in self.text:
            state = self.get_state(char)
            if (
                    (self.state == "space" and state != "space")
                    or (self.state == "printable" and state == "special")
                    or (self.state == "special" and state == "printable")):
                words += [word]
                word = ""

            self.state = state
            word += char

        words += [word]  # Clean up any remaining word

        return words

    def get_ind(self):
        n = 0
        ind = []
        for word in self.words:
            ind += [n] * len(word)
            n += 1

        return ind

    def get_state(self, char):
        if char == " ":
            return "space"

        if char in WordParser.SPECIAL:
            return "special"

        if char.isprintable():
            return "printable"


if __name__ == "__main__":
    wp = WordParser("This is (a) test phrase.")
    print(wp.words)
    print(wp.ind)

    wp = WordParser("")
    print(wp)
