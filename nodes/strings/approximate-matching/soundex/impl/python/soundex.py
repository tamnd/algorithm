# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/soundex/. The authors are listed in prov/8WZ6WZ.jsonl.

"""American Soundex code of a name: one letter and three digits."""

_CODE = {}
for _letters, _digit in (("BFPV", "1"), ("CGJKQSXZ", "2"), ("DT", "3"), ("L", "4"), ("MN", "5"), ("R", "6")):
    for _ch in _letters:
        _CODE[_ch] = _digit


def code(ch: str) -> str:
    """Digit of an upper-case letter; "0" for A, E, I, O, U, Y, H and W."""
    return _CODE.get(ch, "0")


def soundex(name: str) -> str:
    """Return the Soundex code of name, for example "R163" for "Robert".

    Characters that are not ASCII letters are ignored, and case does not
    matter. Precondition: name holds at least one ASCII letter, else
    ValueError. Cost: O(len(name)) time.
    """
    s = [c for c in name.upper() if "A" <= c <= "Z"]  # @line L1
    if not s:
        raise ValueError("the name holds no letter")
    out = [s[0]]  # @line L2
    last = code(s[0])
    for ch in s[1:]:  # @line L3
        c = code(ch)  # @line L4
        if ch in "HW":  # @line L5
            continue
        if c != "0" and c != last:  # @line L6
            out.append(c)
            if len(out) == 4:  # @line L8
                break
        last = c  # @line L7
    return "".join(out).ljust(4, "0")  # @line L9
