class WordParser:
    SPECIAL = "{}[]():,.'\"-+=/"

    def __str__(self):
        return str([self.words, self.ind])

    def __init__(self, text):
        self.text = text
        self.state = None
        self.words = self._get_words()
        self.ind = self._get_ind()
        self.word_inds = self._get_word_ind()

    def _get_words(self):
        word = ""
        words = []
        for char in self.text:
            state = self._get_state(char)
            if state != self.state:
                words += [word]
                word = ""

            self.state = state
            word += char

        words += [word]  # Clean up any remaining word

        if len(words) > 1:
            words = words[1:]  # Remove first word which is an empty string

        return words

    def _get_ind(self):
        n = 0
        ind = []
        for word in self.words:
            ind += [n] * len(word)
            n += 1

        return ind

    def _get_word_ind(self):
        inds = []
        i = 0
        for n, word in enumerate(self.words):
            ind = list(range(i, i + len(word)))
            inds += [ind]
            i += len(word)

        return inds

    def _get_state(self, char):
        if char == " ":
            return "space"

        if char in WordParser.SPECIAL:
            return "special"

        if char.isprintable():
            return "printable"

    def next_word_start(self, ind):
        for word, inds in zip(self.words, self.word_inds):
            if inds[0] > ind and word.strip():
                return inds[0]

    def next_word_end(self, ind):
        for word, inds in zip(self.words, self.word_inds):
            if inds[-1] > ind and word.strip():
                return inds[-1]

    def prev_word_start(self, ind):
        for word, inds in zip(reversed(self.words), reversed(self.word_inds)):
            print(word, inds)
            if inds[0] < ind and word.strip():
                return inds[0]


if __name__ == "__main__":
    wp = WordParser("def foo(x, y=[1,2,3]):")
    wp = WordParser("class Foo:    def foo(self, x):      return self.x + 1")
    print(wp.words)
    print(wp.word_inds)
    print(wp.ind)

    # for n, char in enumerate(wp.text):
    #     print("main", n, char, wp.next_word_start(n), wp.next_word_end(n))

    for n, char in enumerate(wp.text):
        print("main", n, char, wp.prev_word_start(n))
