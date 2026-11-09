# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/faro-shuffle/. The authors are listed in prov/0P38K0.jsonl.

from typing import TypeVar

T = TypeVar("T")


def faro_shuffle(a: list[T], out: bool = True) -> list[T]:
    """Return the perfect shuffle of a deck a with an even number of cards.

    The deck is cut into halves a[:m] and a[m:], which are interleaved one
    card at a time. An out-shuffle keeps the top card a[0] on top; an
    in-shuffle puts the top card of the bottom half, a[m], on top.
    Theta(n) time and Theta(n) extra space.
    """
    n = len(a)
    if n % 2:
        raise ValueError("the deck must have an even number of cards")
    m = n // 2  # @line L1
    b: list[T] = [a[0]] * n if n else []
    for k in range(m):  # @line L2
        if out:  # @line L3
            b[2 * k], b[2 * k + 1] = a[k], a[m + k]
        else:  # @line L4
            b[2 * k], b[2 * k + 1] = a[m + k], a[k]
    return b  # @line L5


def multiplicative_order(base: int, modulus: int) -> int:
    """The least e >= 1 with base**e = 1 mod modulus; gcd(base, modulus) = 1."""
    if modulus == 1:
        return 1
    e, x = 1, base % modulus
    while x != 1:
        x = x * base % modulus
        e += 1
    return e


def shuffle_order(n: int, out: bool = True) -> int:
    """Number of perfect shuffles of n cards (n even) that restore the deck.

    Out-shuffle: the order of 2 modulo n - 1. In-shuffle: modulo n + 1.
    """
    return multiplicative_order(2, n - 1 if out else n + 1)


def elmsley_moves(p: int) -> str:
    """The shuffles that move the top card to position p (0-based).

    Write p in binary from the most significant bit; I (in) for 1, O (out) for 0.
    """
    return "".join("I" if bit == "1" else "O" for bit in bin(p)[2:]) if p else ""
