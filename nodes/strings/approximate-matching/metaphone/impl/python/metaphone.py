# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/metaphone/. The authors are listed in prov/SN7VAT.jsonl.

"""Original Metaphone code of an English word, by the rules stated on the page.

Implementations of Metaphone differ in details. This one follows the rule
list of the page exactly and does not cut the code to a fixed length.
"""

VOWELS = "AEIOU"


def metaphone(word: str) -> str:
    """Return the Metaphone code of word, for example "K0RN" for "Catherine".

    Characters that are not ASCII letters are ignored, and case does not
    matter. A word without letters gives "". Cost: O(len(word)) time.
    """
    s = [c for c in word.upper() if "A" <= c <= "Z"]  # @line L1
    w: list[str] = []
    for c in s:  # @line L2
        if not w or c != w[-1] or c == "C":
            w.append(c)
    if "".join(w[:2]) in ("KN", "GN", "PN", "AE", "WR"):  # @line L3
        w = w[1:]
    n = len(w)

    def at(j: int) -> str:
        return w[j] if 0 <= j < n else ""

    def vowel(j: int) -> bool:
        return at(j) != "" and at(j) in VOWELS

    out: list[str] = []
    for i in range(n):  # @line L4
        c, nx, pv = w[i], at(i + 1), at(i - 1)
        if c in VOWELS:  # @line L5
            if i == 0:
                out.append(c)
        elif c == "B":  # @line L6
            if not (i == n - 1 and pv == "M"):
                out.append("B")
        elif c == "C":
            if nx == "I" and at(i + 2) == "A":
                out.append("X")
            elif nx == "H":
                out.append("K" if pv == "S" else "X")
            elif nx in ("I", "E", "Y"):
                out.append("S")
            else:
                out.append("K")
        elif c == "D":
            out.append("J" if nx == "G" and at(i + 2) in ("E", "Y", "I") else "T")
        elif c == "G":
            if nx == "H" and not (i + 1 == n - 1 or vowel(i + 2)):
                pass
            elif nx == "N" and (i + 1 == n - 1 or "".join(w[i + 1 :]) == "NED"):
                pass
            elif pv == "D" and nx in ("E", "I", "Y"):
                pass
            elif nx in ("I", "E", "Y"):
                out.append("J")
            else:
                out.append("K")
        elif c == "H":
            if pv in ("C", "G", "P", "S", "T") or (i == 1 and pv == "W"):
                pass
            elif vowel(i - 1) and not vowel(i + 1):
                pass
            else:
                out.append("H")
        elif c == "K":
            if pv != "C":
                out.append("K")
        elif c == "P":
            out.append("F" if nx == "H" else "P")
        elif c == "Q":
            out.append("K")
        elif c == "S":
            if nx == "H" or (nx == "I" and at(i + 2) in ("O", "A")):
                out.append("X")
            else:
                out.append("S")
        elif c == "T":
            if nx == "I" and at(i + 2) in ("A", "O"):
                out.append("X")
            elif nx == "H":
                out.append("0")
            elif nx == "C" and at(i + 2) == "H":
                pass
            else:
                out.append("T")
        elif c == "V":
            out.append("F")
        elif c == "W":
            if i == 0 and nx == "H":
                out.append("W")
            elif vowel(i + 1):
                out.append("W")
        elif c == "X":
            out.append("S" if i == 0 else "KS")
        elif c == "Y":
            if vowel(i + 1):
                out.append("Y")
        elif c == "Z":
            out.append("S")
        else:  # @line L7
            out.append(c)  # F, J, L, M, N, R
    return "".join(out)  # @line L8
