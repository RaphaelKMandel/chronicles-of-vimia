from difflib import SequenceMatcher


def replace(string):
    return string.replace(" ", "\u2423")

def get_diff(current, target):
    words = []
    x = SequenceMatcher(a=current, b=target).get_opcodes()
    for op, s1, f1, s2, f2 in x:
        print(op, s1, f1, s2, f2)
        if op == "replace":
            words.append(
                ("delete", replace(current[s1:f1]))
            )
            words.append(
                ("insert", target[s2:f2])
            )
        elif op == "insert":
            words.append(
                (op, target[s2:f2])
            )

        elif op == "delete":
            words.append(
                (op, replace(current[s1:f1]))
            )

        else:
            words.append(
                (op, current[s1:f1])
            )

    return words


if __name__ == "__main__":
    current = "def foo(self, x): "
    target = "def foo(self):"
    print(get_diff(current, target))
