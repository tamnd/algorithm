---
tag: CE66Y2
kind: definition
slug: positional-number-system
name: Positional number system
aliases:
- Radix representation
- place-value notation
- positional notation
area: algebra/integer-arithmetic
level: intro
summary: Represents a number as a digit string where each position has a weight that is a power of the radix.
prereqs: [radix, division-with-remainder]
see_also: [radix, radix-conversion, multiprecision-integer, horner-rule, balanced-ternary, signed-digit-representation, redundant-number-system, factorial-number-system]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.1, Positional number systems (the definition, radix points, mixed radices, other digit sets, and the history); Section 4.4, Radix conversion
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.1, Representation of integers
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 1, Numbers and arithmetic (fixed-radix positional number systems, digit sets and radix conversion)
---

A positional number system writes a number as a string of digits in which the value of a digit depends on its position: the digit in position $i$ is multiplied by $b^i$, where $b \ge 2$ is the [radix](/radix/). With the digits $0, 1, \ldots, b - 1$, each nonnegative integer has exactly one representation without leading zeros, and the representation is found by repeated [division with remainder](/division-with-remainder/) by $b$. All arithmetic on long integers in this area works on such strings, in the radix $\beta = 2^w$ of the machine word.

## Definition

Fix a radix $b \ge 2$. A **numeral** of length $k \ge 0$ is a string $d_{k-1} d_{k-2} \cdots d_0$ of digits with $0 \le d_i \le b - 1$. Its value is

$$[d_{k-1} \cdots d_0]_b = \sum_{i=0}^{k-1} d_i \, b^i .$$

The numeral is **normalized** if $k = 0$ or $d_{k-1} \ne 0$. The empty numeral has the value 0.

**Theorem (unique representation).** For each radix $b \ge 2$ and each integer $N \ge 0$, there is exactly one normalized numeral with value $N$.

*Proof.* *Existence*, by strong induction on $N$. For $N = 0$, take the empty numeral. For $N \ge 1$, division with remainder gives $N = q b + r$ with $0 \le r \le b - 1$ and $q = \lfloor N / b \rfloor$. Since $b \ge 2$, $q \le N/2 < N$. By the hypothesis, $q$ has a normalized numeral $e_{m-1} \cdots e_0$. Then $e_{m-1} \cdots e_0 \, r$ has the value $q b + r = N$. It is normalized: if $m \ge 1$ its first digit is $e_{m-1} \ne 0$, and if $m = 0$ then $q = 0$ and $r = N \ge 1$.

*Uniqueness.* Let two normalized numerals $d_{k-1} \cdots d_0$ and $e_{m-1} \cdots e_0$ have the same value $N$. If $N = 0$, both are empty, because a normalized nonempty numeral has value at least $b^{k-1} \ge 1$. If $N \ge 1$, then $N = b \cdot [d_{k-1} \cdots d_1]_b + d_0$ with $0 \le d_0 < b$, so $d_0 = N \bmod b$ by the uniqueness of the remainder; in the same way $e_0 = N \bmod b$, so $d_0 = e_0$. The two shorter numerals $d_{k-1} \cdots d_1$ and $e_{m-1} \cdots e_1$ are normalized and both have the value $\lfloor N / b \rfloor < N$, so they are equal by induction. $\blacksquare$

The proof is an algorithm. It produces the digits from the least significant one, one division by $b$ for each digit. The inverse direction, from digits to value, is [Horner's rule](/horner-rule/):

$$N = ( \cdots ((d_{k-1}) b + d_{k-2}) b + \cdots ) b + d_0 ,$$

with $k - 1$ multiplications by $b$ and $k - 1$ additions.

**Bounds.** A numeral of length $k$ has a value in $\{0, \ldots, b^k - 1\}$, and each value in that range has exactly one numeral of length exactly $k$ (pad with leading zeros). So the $b^k$ strings of length $k$ are in bijection with $\{0, \ldots, b^k - 1\}$. This bijection is what a fixed-width machine word implements for $b = 2$, and it is the reason for [integer overflow](/integer-overflow/): a value of $b^k$ or more has no numeral of length $k$.

**Fractions.** A radix point extends the system to real numbers: $0.d_1 d_2 d_3 \ldots$ has the value $\sum_{i \ge 1} d_i b^{-i}$. Each real number in $[0, 1)$ has such an expansion, by repeated multiplication by $b$. The expansion is unique except for the numbers $m / b^j$, which have two: one that ends in zeros and one that ends in the digit $b - 1$. A rational number $p/q$ in lowest terms has a finite expansion exactly when each prime factor of $q$ divides $b$.

**Notation of this area.** For long integers the radix is $\beta = 2^w$, where $w$ is the word size, and a digit is a *limb*. An $n$-limb number is $A = \sum_{i=0}^{n-1} a_i \beta^i$ with $0 \le a_i < \beta$. Costs are in limb operations on the [word RAM](/word-ram/), or in bit operations, and $M(n)$ is the cost of a product of two $n$-limb numbers.

## Examples and non-examples

**Digits by division.** In radix 8, the year 2026 gives $2026 = 253 \cdot 8 + 2$, $253 = 31 \cdot 8 + 5$, $31 = 3 \cdot 8 + 7$ and $3 = 0 \cdot 8 + 3$. Read from the last remainder: $2026 = [3752]_8$. Horner's rule gives the value back: $((3 \cdot 8 + 7) \cdot 8 + 5) \cdot 8 + 2 = 2026$.

**Limbs.** In the radix $\beta = 2^8$, $2026 = 7 \cdot 256 + 234$, so its limb array, least significant limb first, is $[234, 7]$. Libraries store the limbs in this order, so that the carry of an addition moves to higher indices.

**Fixed length.** In radix 2 with length 4, the 16 strings $0000$ to $1111$ are the numbers 0 to 15. The sum $1111 + 0001$ is 16, which needs the fifth digit $10000$.

**A fraction that does not end.** $\frac{1}{10} = [0.0\overline{0011}]_2$: in binary the digits $0011$ repeat for ever, because $10 = 2 \cdot 5$ and 5 does not divide 2. This is why the decimal 0.1 is not exact in binary floating point. In radix 10 the same number is $0.1$.

**Two expansions.** $[0.0111\ldots]_2 = [0.1]_2 = \frac12$, as $[0.999\ldots]_{10} = 1$.

**Non-examples.**

- Roman numerals are not positional. The value of X is 10 in each place, and the order of the symbols only says whether to add or to subtract.
- Unary notation, with $N$ marks for $N$, is not positional: its length is $N$, not about $\log_b N$.
- A string with leading zeros, such as $[0042]_{10}$, is a numeral but not a normalized one.
- The [factorial number system](/factorial-number-system/) is positional with a *mixed* radix: the weight of position $i$ is $(i+1)!$, not a power of one radix. The theorem above holds for it with the digit $d_i$ in $\{0, \ldots, i + 1\}$, by the same division argument.

## Related definitions

- [Radix](/radix/): the base $b$ and the count $\lfloor \log_b N \rfloor + 1$ of digits.
- [Radix conversion](/radix-conversion/): changing a numeral from one radix to another.
- [Multiprecision integer](/multiprecision-integer/): the limb array with a sign, used by the algorithms of this area.
- Signed values: [sign-magnitude](/sign-magnitude-representation/), [ones' complement](/ones-complement/) and [two's complement](/twos-complement/) for fixed length in radix 2.
- Other digit sets: [balanced ternary](/balanced-ternary/), [signed-digit representations](/signed-digit-representation/), the [non-adjacent form](/non-adjacent-form/) and the [redundant number systems](/redundant-number-system/), where a number can have more than one numeral.

### History

Positional notation is old. The Babylonians wrote numbers in radix 60, and the decimal system with a digit for zero came to Europe from India through Arabic texts. Knuth, Section 4.1, gives the history and the later study of other radices, such as binary.

## References
