# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/check-digit-computation/. The authors are listed in prov/CAQC35.jsonl.

"""Weighted check digits: ISBN-10, ISBN-13 / EAN-13 / UPC-A, ISO/IEC 7064 MOD 11-2 and MOD 97-10.

All of them compute a weighted sum of the digits and choose the check
character that makes the total a fixed value modulo m.

- ISBN-10: weights 10, 9, ..., 2 on the nine payload digits and 1 on the
  check; the total is 0 mod 11. The check value 10 is written X.
- EAN-13, ISBN-13 and UPC-A (GS1): from the right, the check has weight 1,
  the digit before it 3, then 1, 3, and so on; the total is 0 mod 10.
- ISO/IEC 7064 MOD 11-2 (ORCID, the Chinese resident identity number): the
  digit at position i from the right (check at i = 1) has weight 2^(i-1)
  mod 11; the total is 1 mod 11. The check value 10 is written X.
- ISO/IEC 7064 MOD 97-10 (IBAN): read the string as a decimal number with the
  two check digits at the end; it must be 1 mod 97. IBAN first moves the
  country code and check digits to the end and replaces each letter by
  10..35.

Cost: Theta(n) for n characters, O(1) extra space.
"""


def _digits(s: str) -> list[int]:
    if not s.isascii() or not s.isdigit():
        raise ValueError("expected decimal digits")
    return [ord(c) - 48 for c in s]


# ---------------------------------------------------------------- ISBN-10 (mod 11)


def isbn10_check(payload: str) -> str:
    """Check character of a 9-digit ISBN-10 payload: '0'..'9' or 'X'."""
    d = _digits(payload)
    if len(d) != 9:
        raise ValueError("ISBN-10 has 9 payload digits")
    s = sum((10 - i) * x for i, x in enumerate(d))
    c = (11 - s % 11) % 11
    return "X" if c == 10 else str(c)


def isbn10_valid(isbn: str) -> bool:
    isbn = isbn.replace("-", "")
    return len(isbn) == 10 and isbn[:9].isdigit() and isbn10_check(isbn[:9]) == isbn[9]


# ---------------------------------------------------------------- GS1 (weights 3 and 1, mod 10)


def gs1_check(payload: str) -> str:
    """GS1 check digit (EAN-13 with 12 payload digits, UPC-A with 11, ISBN-13 with 12)."""
    d = _digits(payload)
    s = sum(x * (3 if i % 2 == 0 else 1) for i, x in enumerate(reversed(d)))
    return str((10 - s % 10) % 10)


def gs1_valid(code: str) -> bool:
    code = code.replace("-", "")
    return len(code) >= 2 and code.isdigit() and gs1_check(code[:-1]) == code[-1]


# ---------------------------------------------------------------- ISO/IEC 7064 MOD 11-2


def mod11_2_check(payload: str) -> str:
    """ISO/IEC 7064 MOD 11-2 check character, by the recursive (Horner) method."""
    p = 0
    for x in _digits(payload):
        p = ((p + x) * 2) % 11
    c = (12 - p) % 11
    return "X" if c == 10 else str(c)


def mod11_2_valid(code: str) -> bool:
    code = code.replace("-", "").upper()
    if len(code) < 2 or not code[:-1].isdigit():
        return False
    return mod11_2_check(code[:-1]) == code[-1]


def chinese_id_check(first17: str) -> str:
    """Check character of an 18-character Chinese resident identity number (GB 11643-1999)."""
    d = _digits(first17)
    if len(d) != 17:
        raise ValueError("the payload has 17 digits")
    weights = [pow(2, 17 - i, 11) for i in range(17)]  # 7 9 10 5 8 4 2 1 6 3 7 9 10 5 8 4 2
    s = sum(w * x for w, x in zip(weights, d))
    c = (12 - s % 11) % 11
    return "X" if c == 10 else str(c)


# ---------------------------------------------------------------- ISO/IEC 7064 MOD 97-10 and IBAN


def mod97(digits: str) -> int:
    """The value of a long decimal string mod 97, nine digits at a time."""
    r = 0
    for i in range(0, len(digits), 9):
        part = digits[i : i + 9]
        r = (r * 10 ** len(part) + int(part)) % 97
    return r


def mod97_10_check(payload: str) -> str:
    """Two check digits cc such that payload + cc is 1 mod 97."""
    _digits(payload)
    return f"{98 - mod97(payload + '00'):02d}"


def _iban_digits(iban: str) -> str:
    s = iban.replace(" ", "").upper()
    if not s.isascii() or not s.isalnum() or len(s) < 5:
        raise ValueError("an IBAN has letters and digits only")
    s = s[4:] + s[:4]
    return "".join(str(int(ch, 36)) for ch in s)


def iban_valid(iban: str) -> bool:
    return mod97(_iban_digits(iban)) == 1


def iban_check_digits(country: str, bban: str) -> str:
    """The two IBAN check digits for a country code and a basic bank account number."""
    return f"{98 - mod97(_iban_digits(country + '00' + bban)):02d}"
