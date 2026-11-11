# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/playfair-cipher/. The authors are listed in prov/3G0PKX.jsonl.

import random

import pytest

from playfair_cipher import (
    ALPHABET25,
    digraph_table,
    key_square,
    known_digraphs,
    letters,
    playfair_decrypt,
    playfair_encrypt,
    prepare,
)

KEY = "playfair example"
PLAIN = "Hide the gold in the tree stump"
CIPHER = "BMODZBXDNABEKUDMUIXMMOUVIF"


def oracle_pair(square: str, a: str, b: str) -> str:
    """An independent statement of the rules, through a grid of rows."""
    grid = [square[5 * r : 5 * r + 5] for r in range(5)]
    where = {grid[r][c]: (r, c) for r in range(5) for c in range(5)}
    (r1, c1), (r2, c2) = where[a], where[b]
    if r1 == r2:
        return grid[r1][(c1 + 1) % 5] + grid[r2][(c2 + 1) % 5]
    if c1 == c2:
        return grid[(r1 + 1) % 5][c1] + grid[(r2 + 1) % 5][c2]
    return grid[r1][c2] + grid[r2][c1]


def test_example() -> None:
    assert key_square(KEY) == "PLAYFIREXMBCDGHKNOQSTUVWZ"
    assert prepare(PLAIN) == ["HI", "DE", "TH", "EG", "OL", "DI", "NT", "HE", "TR", "EX", "ES", "TU", "MP"]
    assert playfair_encrypt(PLAIN, KEY) == CIPHER
    assert playfair_decrypt(CIPHER, KEY) == "HIDETHEGOLDINTHETREXESTUMP"


def test_fillers_and_edge_cases() -> None:
    assert prepare("") == []
    assert prepare("A") == ["AX"]
    assert prepare("BALLOON") == ["BA", "LX", "LO", "ON"]
    assert prepare("XX") == ["XQ", "XQ"]
    assert prepare("JUMP") == ["IU", "MP"]
    with pytest.raises(ValueError):
        playfair_decrypt("ABC", KEY)


def test_round_trip_and_oracle() -> None:
    rng = random.Random(8)
    for _ in range(600):
        kw = "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(rng.randrange(12)))
        square = key_square(kw)
        assert sorted(square) == sorted(ALPHABET25)
        p = "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ ") for _ in range(rng.randrange(30)))
        c = playfair_encrypt(p, kw)
        assert c == "".join(oracle_pair(square, d[0], d[1]) for d in prepare(p))
        assert playfair_decrypt(c, kw) == "".join(prepare(p))


def test_digraph_properties() -> None:
    rng = random.Random(9)
    for _ in range(20):
        kw = "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(8))
        table = digraph_table(kw)
        assert len(table) == 600 and len(set(table.values())) == 600  # a permutation of digraphs
        for ab, cd in table.items():
            assert cd[0] != ab[0] and cd[1] != ab[1]  # no letter stays in its place
            assert cd[0] != cd[1]
            assert table[ab[::-1]] == cd[::-1]  # the reversal property


def test_equivalent_squares() -> None:
    # Cyclic shifts of the rows or of the columns give the same cipher, so at
    # most 25!/25 = 24! ciphers are different. The transpose is not equivalent.
    square = key_square(KEY)
    rows = [square[5 * r : 5 * r + 5] for r in range(5)]
    row_shift = "".join(rows[1:] + rows[:1])
    col_shift = "".join(r[2:] + r[:2] for r in rows)
    transpose = "".join(rows[r][c] for c in range(5) for r in range(5))

    def table(sq: str) -> dict[str, str]:
        return {a + b: oracle_pair(sq, a, b) for a in ALPHABET25 for b in ALPHABET25 if a != b}

    base = table(square)
    assert table(row_shift) == base
    assert table(col_shift) == base
    assert table(transpose) != base


def test_known_plaintext() -> None:
    known = known_digraphs(PLAIN, CIPHER)
    assert known["BM"] == "HI" and known["MB"] == "IH"
    # Every known cipher digraph decrypts as the key would decrypt it.
    for cd, ab in known.items():
        assert playfair_decrypt(cd, KEY) == ab
    # A new message that reuses known digraphs is read in part without the key.
    c2 = playfair_encrypt("the gold is here", KEY)
    read = [known.get(c2[i : i + 2], "??") for i in range(0, len(c2), 2)]
    assert c2 == "ZBXDNABEZSXEXM"
    assert read == ["TH", "EG", "OL", "DI", "??", "??", "EX"]
    assert letters("the gold is here") == "THEGOLDISHERE"
