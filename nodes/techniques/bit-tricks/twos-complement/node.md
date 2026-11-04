---
tag: 17XGVH
kind: definition
slug: twos-complement
name: Two's complement
aliases:
- 2's complement
- two's complement representation
area: techniques/bit-tricks
level: intro
summary: Signed integer encoding in which negation is bitwise inversion plus one, and addition is uniform.
prereqs: [positional-number-system, bitwise-operations]
see_also: [ones-complement, sign-magnitude-representation, sign-extension, integer-overflow, lowest-set-bit, additive-group-modulo-n, word-ram, ieee-754]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley (1997)
    locator: Section 4.1 (Positional Number Systems), the discussion of two's complement and ones' complement notation
  - book: isbn:9780134092669
    title: Randal E. Bryant and David R. O'Hallaron, Computer Systems, A Programmer's Perspective, third edition, Pearson (2016)
    locator: Section 2.2.3 (Two's-complement encodings), Section 2.3.2 (Two's-complement addition) and Section 2.3.3 (Two's-complement negation)
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley (2013)
    locator: Chapter 2, Section 2-12 (Comparison Predicates) and Section 2-13 (Overflow Detection)
  - url: https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf
    title: ISO/IEC 9899:2011 committee draft N1570 (the C11 standard)
    locator: Section 6.2.6.2, paragraph 2 (the three permitted signed representations), Section 6.5, paragraph 5 (signed overflow) and Section 6.3.1.3 (Signed and unsigned integers)
---

Two's complement is the encoding of signed integers in which a $w$-bit word stores the integer $x$ with $-2^{w-1} \le x < 2^{w-1}$ as the unsigned number $x \bmod 2^w$. The top bit then has weight $-2^{w-1}$ instead of $+2^{w-1}$, it is 1 exactly for negative numbers, and the other bits have their usual weights. Because the encoding is reduction modulo $2^w$, the same adder, subtractor and multiplier serve signed and unsigned words, and negation is "invert all bits, then add 1". Nearly all current processors use it, and C23 and C++20 make it the only signed representation.

## Definition

Fix a word size $w \ge 1$. A word is a bit string $b = (b_{w-1} b_{w-2} \dots b_0)$ with each $b_i \in \{0, 1\}$; $b_{w-1}$ is the top bit or sign bit.

**Value.** The two's complement value of $b$ is

$$\mathrm{val}(b) = -b_{w-1} 2^{w-1} + \sum_{i=0}^{w-2} b_i 2^i.$$

Its unsigned value is $\mathrm{uval}(b) = \sum_{i=0}^{w-1} b_i 2^i$. The two differ by $2^w$ when $b_{w-1} = 1$ and agree otherwise, so $\mathrm{val}(b) \equiv \mathrm{uval}(b) \pmod{2^w}$.

**Range.** As $b$ runs over all $2^w$ words, $\mathrm{val}(b)$ runs over each integer in $[-2^{w-1}, 2^{w-1} - 1]$ exactly once. So the encoding of an integer $x$ in this range is the unique word $b$ with $\mathrm{uval}(b) = x \bmod 2^w$.

**Operations.** The integer operations on encoded values are the unsigned operations modulo $2^w$, followed by the reading $\mathrm{val}$:

- addition, subtraction and multiplication: the word of $x \pm y$ or $x \cdot y$ is $(\mathrm{uval}(x) \pm \mathrm{uval}(y)) \bmod 2^w$ or $(\mathrm{uval}(x) \cdot \mathrm{uval}(y)) \bmod 2^w$, and it is correct whenever the true result lies in the range;
- negation: $-x \equiv \overline{x} + 1 \pmod{2^w}$, where $\overline{x}$ inverts every bit, because $x + \overline{x} = 2^w - 1$; equivalently $-x = \overline{x - 1}$;
- comparison: $x < y$ as signed numbers exactly when $x \oplus 2^{w-1} < y \oplus 2^{w-1}$ as unsigned numbers (flip the sign bits, then compare unsigned).

**Overflow.** A sum $s = x + y$ computed modulo $2^w$ is wrong exactly when $x$ and $y$ have the same sign and $s$ has the other sign. As a bit formula, the top bit of $(x \oplus s) \wedge (y \oplus s)$ is 1 exactly in this case (Warren, Section 2-13). Most processors record this condition in an overflow flag.

**The name.** For $x > 0$, the word of $-x$ is $2^w - x$, the complement of $x$ with respect to $2^w$, a power of two. Knuth notes that, by the same logic, ones' complement is a complement with respect to $2^w - 1$, a string of ones.

## Examples and non-examples

**Eight-bit words.** With $w = 8$ the range is $[-128, 127]$.

| integer | word | unsigned reading |
|---|---|---|
| 0 | 00000000 | 0 |
| 1 | 00000001 | 1 |
| 5 | 00000101 | 5 |
| 127 | 01111111 | 127 |
| $-1$ | 11111111 | 255 |
| $-5$ | 11111011 | 251 |
| $-127$ | 10000001 | 129 |
| $-128$ | 10000000 | 128 |

**Negation.** $5 = 00000101_2$; inverted it is $11111010_2$; adding 1 gives $11111011_2$, the word of $-5$. Reading $11111011_2$ by the value formula gives $-128 + 64 + 32 + 16 + 8 + 2 + 1 = -5$.

**The asymmetric end.** The range has one more negative number than positive numbers. Negating $-128 = 10000000_2$ gives $01111111_2 + 1 = 10000000_2$, again $-128$: the true result 128 is out of range. In C, computing `-x` for `x == INT_MIN` on a signed `int` is signed overflow, which is undefined behaviour (C11 Section 6.5, paragraph 5). The same holds for `INT_MIN / -1` and for `abs(INT_MIN)`.

**Overflow of a sum.** $100 + 100$ on signed 8-bit words: the unsigned sum is $200 = 11001000_2$, which reads as $200 - 256 = -56$. Both operands are positive and the result is negative, so the overflow formula fires. On unsigned C types the wrap is defined; on signed C types the overflow is undefined, and a compiler may assume it does not happen.

**Uniform addition.** $-5 + 7$: the words are $11111011_2$ and $00000111_2$, their unsigned sum is $251 + 7 = 258$, and $258 \bmod 256 = 2 = 00000010_2$, the right answer. The adder does not look at the signs.

**Non-example: ones' complement.** In [ones' complement](/ones-complement/) the word of $-x$ is $\overline{x}$, so $-5 = 11111010_2$ and there are two zeros, $00000000_2$ and $11111111_2$. Addition needs an end-around carry. The range is symmetric, $[-127, 127]$ for $w = 8$.

**Non-example: sign-magnitude.** In [sign-magnitude](/sign-magnitude-representation/) the top bit is the sign and the other bits are $|x|$, so $-5 = 10000101_2$, there are again two zeros, and addition must compare signs first. The sign of [IEEE 754](/ieee-754/) floating-point numbers is stored this way.

**Non-example: offset binary.** The excess-$2^{w-1}$ code stores $x$ as $x + 2^{w-1}$, so $-5$ is $01111011_2$. It is two's complement with the sign bit flipped, which is why the comparison rule above works. The exponent field of IEEE 754 numbers uses a biased code of this kind.

**C before C23.** C11 allows three signed representations: sign and magnitude, two's complement and ones' complement (Section 6.2.6.2, paragraph 2). Converting an unsigned value that does not fit to a signed type gives an implementation-defined result (Section 6.3.1.3, paragraph 3). On all common platforms the result is the two's complement reading, but portable code converts in the other direction, from signed to unsigned, which is defined as reduction modulo $2^w$.

## Related definitions

- [Ones' complement](/ones-complement/) and [sign-magnitude representation](/sign-magnitude-representation/): the two other signed codes allowed by C11.
- [Sign extension](/sign-extension/): widening a two's complement word by copying its top bit.
- [Integer overflow](/integer-overflow/): a result outside $[-2^{w-1}, 2^{w-1})$, which the modular arithmetic silently wraps.
- [Positional number system](/positional-number-system/): the unsigned reading $\mathrm{uval}$ is base-2 positional notation.
- [Additive group modulo n](/additive-group-modulo-n/): two's complement words with addition form the group $\mathbb{Z}/2^w\mathbb{Z}$, with representatives taken from $[-2^{w-1}, 2^{w-1})$ instead of $[0, 2^w)$.
- [Lowest set bit](/lowest-set-bit/): the identity $x \wedge (-x)$ depends on $-x = \overline{x} + 1$.
- [Word RAM](/word-ram/): the model whose arithmetic on $w$-bit words is this modular arithmetic.

## References
