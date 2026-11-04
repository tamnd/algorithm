---
tag: DZSEHS
kind: concept
slug: lowest-set-bit
name: Lowest set bit
aliases:
- isolating the lowest set bit
- x & -x
- rightmost set bit
area: techniques/bit-tricks
level: intro
summary: The value x & -x isolates the least significant 1-bit of x; x & (x-1) clears it.
prereqs: [bitwise-operations, twos-complement]
see_also: [trailing-zero-count, de-bruijn-bit-scan, kernighan-popcount, power-of-two-test, fenwick-tree, gospers-hack, submask-enumeration, ruler-sequence]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley (2013)
    locator: Chapter 2, Section 2-1 (Manipulating Rightmost Bits)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.1.3 (Bitwise tricks and techniques), the part on working with the rightmost bits of a word and the ruler function
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer (2011)
    locator: Chapter 1, Section 1.3 (Operations on low bits or blocks of a word)
  - book: isbn:9780131103627
    title: Brian W. Kernighan and Dennis M. Ritchie, The C Programming Language, second edition, Prentice Hall (1988)
    locator: Section 2.10 (Assignment Operators and Expressions), Exercise 2-9
  - url: https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf
    title: ISO/IEC 9899:2011 committee draft N1570 (the C11 standard)
    locator: Section 6.5, paragraph 5 (signed overflow), and Section 6.3.1.1 (integer promotions)
---

The lowest set bit of a nonzero word $x$ is its least significant 1-bit. On unsigned $w$-bit words with arithmetic modulo $2^w$, the expression $x \wedge (-x)$ keeps this bit and clears all others, and $x \wedge (x - 1)$ clears this bit and keeps all others. Both take two operations and no loop. They are the base of many [bit tricks](/bit-manipulation/): the [power-of-two test](/power-of-two-test/), [Kernighan's popcount](/kernighan-popcount/), the index arithmetic of the [Fenwick tree](/fenwick-tree/), [Gosper's hack](/gospers-hack/) and the [de Bruijn bit scan](/de-bruijn-bit-scan/). The position of the lowest set bit is the [trailing-zero count](/trailing-zero-count/) of $x$.

## In plain words

Write a number in binary and look at its rightmost 1. Subtract one from the number. The rightmost 1 becomes 0, the zeros to its right become ones, and nothing to its left changes. So the number and the number minus one agree everywhere left of that 1, and differ only from that 1 to the end.

This small fact gives two tools. Combining the two numbers with AND removes the rightmost 1. Combining the number with its negative, which is "flip all bits, then add one", keeps only the rightmost 1. With these tools a program can visit the 1-bits of a word one at a time, from right to left.

## The idea

Fix a word size $w$. Words are unsigned integers in $[0, 2^w)$, all arithmetic is modulo $2^w$, and $-x$ means $2^w - x \bmod 2^w$, the [two's complement](/twos-complement/) negation, which equals $\overline{x} + 1$ where $\overline{x}$ is the bitwise complement.

Let $x \ne 0$ and let $k = \rho(x)$ be the index of its lowest 1-bit; Knuth calls $\rho$ the ruler function. Then $x$ has the form $x = a\,1\,0^k$ in binary: a prefix $a$ of $w - k - 1$ bits, a 1 at position $k$, and $k$ zeros. The three words that matter are

$$x - 1 = a\,0\,1^k, \qquad \overline{x} = \overline{a}\,0\,1^k, \qquad -x = \overline{x} + 1 = \overline{a}\,1\,0^k.$$

The first holds because subtracting 1 borrows through the $k$ zeros and stops at the 1. The third holds because adding 1 to $\overline{a}\,0\,1^k$ carries through the $k$ ones and stops at the 0. From these forms each identity in the table follows by comparing the words bit by bit. The prefix $a$ is untouched by $x - 1$ and $x + 1$ (for the ones that use $x + 1$, let $j$ be the index of the lowest 0-bit of $x$, so $x = c\,0\,1^j$ and $x + 1 = c\,1\,0^j$).

| expression | result | needs |
|---|---|---|
| $x \wedge (-x)$ | $0^{w-k-1}\,1\,0^k = 2^k$, the lowest 1-bit alone | $x \ne 0$ |
| $x \wedge (x - 1)$ | $a\,0\,0^k$, the lowest 1-bit cleared | |
| $x \oplus (x - 1)$ | $0\dots0\,1\,1^k = 2^{k+1} - 1$, ones up to and including the lowest 1-bit | $x \ne 0$ |
| $\overline{x} \wedge (x - 1)$ | $0\dots0\,0\,1^k = 2^k - 1$, a mask of the trailing zeros | $x \ne 0$ |
| $x \vee (x - 1)$ | $a\,1\,1^k$, the trailing zeros set to 1 | $x \ne 0$ |
| $\overline{x} \wedge (x + 1)$ | $2^j$, the lowest 0-bit alone | $x \ne 2^w - 1$ |
| $x \vee (x + 1)$ | $c\,1\,1^j$, the lowest 0-bit set | |
| $x \wedge (x + 1)$ | $c\,0\,0^j$, the trailing ones cleared | |

The identities hold for every $w$ and every $x$ that meets the condition in the last column. For $x = 0$, $x \wedge (-x) = 0$ and $x \wedge (x - 1) = 0$, which is often what a loop needs; but $x \oplus (x - 1)$, $\overline{x} \wedge (x - 1)$ and $x \vee (x - 1)$ all give $2^w - 1$.

**Why the identities need only the low bits.** All operations in the table are $+$, $-$, $\wedge$, $\vee$, $\oplus$ and complement. In each of them, bit $t$ of the result depends only on bits $0$ to $t$ of the operands. So the identities are the same for every word size, and they also hold for the infinite two's complement words of Python, where $-x$ and $\overline{x}$ have infinitely many 1-bits at the top.

**Signed words.** The bit patterns are the same when $x$ is read as a signed two's complement integer. The only change is in the arithmetic of a language: in C, `x & -x` on a signed `int` with value `INT_MIN` computes `-INT_MIN`, which overflows and is undefined behaviour (C11 Section 6.5, paragraph 5). On unsigned types the negation wraps modulo $2^w$ and is defined. On `uint8_t` and `uint16_t` the operands are first promoted to `int` (C11 Section 6.3.1.1), so `-x` is a negative `int`; the result of `x & -x` is still right, but `~x & (x + 1)` on a `uint8_t` holding 255 gives 256, not 0, unless it is cast back to the narrow type.

## Examples

**One word, all identities.** Take $w = 8$ and $x = 180 = 10110100_2$, so $k = 2$. Then $-x = 76 = 01001100_2$.

| expression | binary | value |
|---|---|---|
| $x$ | 10110100 | 180 |
| $x \wedge (-x)$ | 00000100 | 4 |
| $x \wedge (x - 1)$ | 10110000 | 176 |
| $x \oplus (x - 1)$ | 00000111 | 7 |
| $\overline{x} \wedge (x - 1)$ | 00000011 | 3 |
| $x \vee (x - 1)$ | 10110111 | 183 |
| $x \vee (x + 1)$ | 10110101 | 181 |

For $x = 87 = 01010111_2$, which ends in three ones, the lowest 0-bit is at $j = 3$: $\overline{x} \wedge (x + 1) = 00001000_2 = 8$, $x \vee (x + 1) = 01011111_2 = 95$ and $x \wedge (x + 1) = 01010000_2 = 80$. For the top bit alone, $x = 128 = 10000000_2$, the negation is $-128 \bmod 256 = 128$, and $x \wedge (-x) = 128$.

**Visiting the 1-bits.** The loop `while x != 0: b = x & -x; use(b); x = x ^ b` visits the 1-bits of $x$ from the lowest to the highest, once each. On $x = 180$ it visits $b = 4, 16, 32, 128$ and stops after four rounds, the [population count](/population-count/) of 180. Writing `x = x & (x - 1)` instead of `x = x ^ b` gives the same sequence of words and is [Kernighan's popcount](/kernighan-popcount/) when the loop only counts.

**Power of two.** A nonzero $x$ is a power of two exactly when it has one 1-bit, that is when $x \wedge (x - 1) = 0$. So $64 \wedge 63 = 0$ and 64 is a power of two, while $96 \wedge 95 = 64 \ne 0$. This is the [power-of-two test](/power-of-two-test/).

**Fenwick tree.** In a [Fenwick tree](/fenwick-tree/) with indices $1, \dots, n$, node $i$ covers the $i \wedge (-i)$ positions that end at $i$. A prefix query walks $i \gets i - (i \wedge (-i))$, which is $i \gets i \wedge (i - 1)$, and an update walks $i \gets i + (i \wedge (-i))$. For $i = 12 = 1100_2$: $12 \wedge (-12) = 4$, the query visits 12, 8 and stops at 0, and the update from 12 visits 12, 16, 32 and so on up to $n$.

**Ruler function.** The values $\rho(1), \rho(2), \dots, \rho(16)$ are $0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 4$, the [ruler sequence](/ruler-sequence/). When a [binary counter](/binary-counter-increment/) goes from $i - 1$ to $i$, exactly $\rho(i) + 1$ bits change, because $i \oplus (i - 1) = 2^{\rho(i)+1} - 1$.

## Where it is used

- [Power-of-two test](/power-of-two-test/): $x \ne 0$ and $x \wedge (x - 1) = 0$.
- [Kernighan's popcount](/kernighan-popcount/): repeat $x \gets x \wedge (x - 1)$ and count the rounds.
- [Trailing-zero count](/trailing-zero-count/) and the [de Bruijn bit scan](/de-bruijn-bit-scan/): isolate $2^k$ first, then find $k$.
- [Fenwick tree](/fenwick-tree/): the parent and next-node steps add or subtract $i \wedge (-i)$.
- [Gosper's hack](/gospers-hack/) and [next same popcount](/next-same-popcount/): the next larger word with the same number of 1-bits starts from $x \wedge (-x)$.
- [Submask enumeration](/submask-enumeration/) and iteration over a [bit set](/bit-set/) or [bitmask](/bitmask/): take the lowest member, then clear it.
- [Bitboards](/bitboard/) in board-game programs: the moves and pieces of a position are read out one bit at a time.

## References
