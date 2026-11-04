---
tag: K6KFX8
kind: concept
slug: bitwise-operations
name: Bitwise operations
aliases:
- bitwise logic
- AND OR XOR NOT
- bit shifts
area: techniques/bit-tricks
level: intro
summary: AND, OR, XOR, NOT and left/right shifts applied to the bits of an integer.
prereqs: [positional-number-system]
see_also: [bit-manipulation, bitmask, bit-set, lowest-set-bit, sign-extension, xor-swap, bit-parallelism, word-ram]
sources:
  - book: isbn:9780131103627
    title: Brian W. Kernighan and Dennis M. Ritchie, The C Programming Language, second edition, Prentice Hall (1988)
    locator: Section 2.9 (Bitwise Operators)
  - book: isbn:9780134092669
    title: Randal E. Bryant and David R. O'Hallaron, Computer Systems, A Programmer's Perspective, third edition, Pearson (2016)
    locator: Section 2.1.7 (Bit-level operations in C), Section 2.1.8 (Logical operations in C) and Section 2.1.9 (Shift operations in C)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.1.3 (Bitwise tricks and techniques), the opening part on bitwise operations and their algebraic laws
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley (2013)
    locator: Chapter 2 (Basics), Section 2-15 (Rotate Shifts)
  - url: https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf
    title: ISO/IEC 9899:2011 committee draft N1570 (the C11 standard)
    locator: Section 6.5.7 (Bitwise shift operators), paragraphs 3 to 5, and Section 6.3.1.1 (integer promotions)
---

Bitwise operations act on integers as strings of bits. AND, OR and exclusive-or (XOR) combine two words position by position, NOT inverts every bit of one word, and the shifts move all bits of a word left or right by a given count. On the [word RAM](/word-ram/) each of them costs one step on a $w$-bit word, so one operation does $w$ Boolean operations at once; this [bit parallelism](/bit-parallelism/) is the base of all [bit manipulation](/bit-manipulation/). They are also the only operations needed to treat a word as a small set, a [bitmask](/bitmask/).

## In plain words

Write two numbers in binary, one above the other, and look at each column separately. AND writes 1 where both have a 1. OR writes 1 where at least one has a 1. XOR writes 1 where they differ. NOT turns every 1 into 0 and every 0 into 1. No column looks at its neighbours, and there are no carries.

A shift slides the whole row of bits. A left shift by one place adds a 0 at the right end and doubles an unsigned number, as long as nothing falls off the left end. A right shift by one place drops the last bit and halves the number, rounding down.

## The idea

Fix a word size $w$ and write a word $x$ as bits $x_{w-1} \dots x_1 x_0$, so that its unsigned value is $\sum_i x_i 2^i$. The operations, with their usual symbols in mathematics and in C, Java and Python, are:

| operation | math | code | bit $i$ of the result |
|---|---|---|---|
| AND | $x \wedge y$ | `x & y` | $x_i y_i$ |
| OR | $x \vee y$ | `x \| y` | $x_i + y_i - x_i y_i$ |
| XOR | $x \oplus y$ | `x ^ y` | $x_i + y_i \bmod 2$ |
| NOT | $\overline{x}$ | `~x` | $1 - x_i$ |
| left shift by $s$ | $x \ll s$ | `x << s` | $x_{i-s}$, or 0 if $i < s$ |
| logical right shift by $s$ | $x \gg s$ | `x >> s` (unsigned) | $x_{i+s}$, or 0 if $i + s \ge w$ |
| arithmetic right shift by $s$ | | `x >> s` (signed, usually) | $x_{i+s}$, or $x_{w-1}$ if $i + s \ge w$ |
| rotate left by $s$ | | `(x << s) \| (x >> (w - s))` | $x_{(i - s) \bmod w}$ |

**Laws.** AND, OR and XOR are associative and commutative. AND and OR distribute over each other, and AND distributes over XOR. De Morgan's laws hold: $\overline{x \wedge y} = \overline{x} \vee \overline{y}$ and $\overline{x \vee y} = \overline{x} \wedge \overline{y}$. XOR has $x \oplus 0 = x$ and $x \oplus x = 0$, so the words form an abelian group under XOR in which each element is its own inverse; the [XOR swap](/xor-swap/) and the [single number](/single-number/) trick use only this. Each law holds bit by bit, because each operation in the table except the shifts acts on each position alone.

**Arithmetic.** For unsigned words, $x \ll s = x \cdot 2^s \bmod 2^w$ and $x \gg s = \lfloor x / 2^s \rfloor$. For signed words in [two's complement](/twos-complement/), the arithmetic right shift gives $\lfloor x / 2^s \rfloor$, rounded toward $-\infty$, and NOT gives $\overline{x} = -x - 1$. Addition links to the bitwise operations by

$$x + y = (x \oplus y) + 2(x \wedge y) = (x \vee y) + (x \wedge y),$$

because $x \oplus y$ is the sum without carries and $x \wedge y$ marks the positions that create a carry. One consequence is the overflow-free average $\lfloor (x + y)/2 \rfloor = (x \wedge y) + ((x \oplus y) \gg 1)$.

**Logical versus bitwise.** In C, `&&`, `||` and `!` treat a whole value as true (nonzero) or false (zero) and give 0 or 1; `&`, `|` and `~` act on each bit. For example `2 & 1` is 0 while `2 && 1` is 1.

**Rules of C that matter.** C does the operations on the promoted type: an operand of type `uint8_t` or `uint16_t` becomes `int` first (C11 Section 6.3.1.1), so `~x` on a `uint8_t` holding 180 is the `int` $-181$, not 75. A shift by a count that is negative or at least the width of the promoted left operand is undefined behaviour (Section 6.5.7, paragraph 3); x86 processors, for example, use only the low 5 bits of the count for 32-bit shifts, so `x << 32` often returns `x`. A left shift of a negative signed value, or of a signed value whose result does not fit, is undefined (paragraph 4). A right shift of a negative signed value is implementation-defined (paragraph 5). For portable bit work, use unsigned types of a fixed width. Also, `&`, `^` and `|` have lower precedence than `==`, so `x & 1 == 0` means `x & (1 == 0)`.

**Other languages.** Java has `>>>` for the logical right shift and uses only the low 5 or 6 bits of the shift count. Python integers have no fixed width: `<<` never loses bits, `>>` is the arithmetic shift, and `~x` is $-x - 1$; to simulate a $w$-bit word, apply `& ((1 << w) - 1)` after each operation.

## Examples

Take $w = 8$, $x = 180 = 10110100_2$ and $y = 105 = 01101001_2$.

| expression | binary | value |
|---|---|---|
| $x \wedge y$ | 00100000 | 32 |
| $x \vee y$ | 11111101 | 253 |
| $x \oplus y$ | 11011101 | 221 |
| $\overline{x}$ | 01001011 | 75 |
| $x \ll 1$ | 01101000 | 104 ($360 \bmod 256$) |
| $x \gg 2$, logical | 00101101 | 45 ($\lfloor 180/4 \rfloor$) |
| $x \gg 2$, arithmetic | 11101101 | $-19$ as signed ($x$ is $-76$ as signed, and $\lfloor -76/4 \rfloor = -19$) |
| rotate $x$ left by 3 | 10100101 | 165 |

Check the addition identity: $x + y = 285$, and $(x \oplus y) + 2(x \wedge y) = 221 + 64 = 285$.

**Bits as a set.** Read $x$ as the set of positions of its 1-bits: $180$ is $\{2, 4, 5, 7\}$ and $105$ is $\{0, 3, 5, 6\}$. Then AND is intersection, $\{5\}$; OR is union; XOR is symmetric difference; NOT is the complement in $\{0, \dots, 7\}$; $x \wedge \overline{y}$ is the difference. This is the [bitmask](/bitmask/) view.

**Masks of constant patterns.** The words `0x55`, `0x33` and `0x0F` are $01010101_2$, $00110011_2$ and $00001111_2$. ANDing with them keeps every other bit, every other pair or every other nibble; the [SWAR popcount](/swar-popcount/) and [bit reversal](/bit-reversal/) are built from such masks and shifts.

**Testing, setting and clearing one bit.** Bit $i$ of $x$ is $(x \gg i) \wedge 1$. Setting it is $x \vee (1 \ll i)$, clearing it is $x \wedge \overline{(1 \ll i)}$, and flipping it is $x \oplus (1 \ll i)$.

## Where it is used

- [Bitmasks](/bitmask/) and [bit sets](/bit-set/): sets of small integers with union, intersection and membership in one operation each.
- [Lowest set bit](/lowest-set-bit/), [power-of-two test](/power-of-two-test/) and [population count](/population-count/): tricks that mix bitwise operations with addition and subtraction.
- [Sign extension](/sign-extension/): shifts and XOR to widen a signed field.
- [XOR swap](/xor-swap/), [single number](/single-number/) and [Nim](/nim/): the group laws of XOR.
- [SIMD within a register](/simd-within-a-register/): masks and shifts that treat one word as many small fields.
- [Cyclic redundancy checks](/cyclic-redundancy-check/) and [xorshift](/xorshift/) generators: shifts and XOR as arithmetic over the field with two elements.
- [Boolean functions](/boolean-function/): a word of $2^k$ bits can store the truth table of a function of $k$ variables, and the bitwise operations combine such tables.

## References
