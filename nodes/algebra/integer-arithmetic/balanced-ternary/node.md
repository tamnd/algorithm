---
tag: NR7RJT
kind: definition
slug: balanced-ternary
name: Balanced ternary
aliases:
- balanced base 3
area: algebra/integer-arithmetic
level: intro
summary: Base-3 signed-digit system with digits -1, 0, 1, which represents negation without a sign.
prereqs: [positional-number-system, division-with-remainder]
see_also: [signed-digit-representation, non-adjacent-form, twos-complement, ones-complement, redundant-number-system, radix-conversion]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.1, Positional number systems (balanced ternary notation, its rounding property and the weighing problem)
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 3, Redundant number systems (signed digit sets, of which balanced ternary is the nonredundant case)
  - url: https://www.americanscientist.org/article/third-base
    title: Brian Hayes, Third Base, American Scientist 89(6), 2001
    locator: the whole article (balanced ternary, radix economy and the Setun computer)
---

Balanced ternary is the positional number system with base 3 and the digits $-1$, $0$ and $1$. Each integer, positive, negative or zero, has exactly one representation, with no sign in front: the sign of the number is the sign of its leading digit, and negation flips every digit. The digit $-1$ is usually written $\bar 1$ or $\mathrm{T}$. Knuth calls it perhaps the prettiest number system of all, and the Setun computer, built at Moscow State University in 1958, used it as its native arithmetic.

## Definition

A *balanced ternary numeral* is a finite string $d_{k-1} \cdots d_1 d_0$ with each $d_i \in \{-1, 0, 1\}$. Its value is

$$\sum_{i=0}^{k-1} d_i \, 3^i .$$

We write $\mathrm{T}$ for the digit $-1$. The numeral is *normalized* if it is empty (the value 0) or $d_{k-1} \ne 0$.

**Theorem.** Each integer $n$ is the value of exactly one normalized balanced ternary numeral. The numerals of $k$ digits have exactly the values $-\frac{3^k - 1}{2}, \ldots, \frac{3^k - 1}{2}$.

*Proof.* *Range.* The largest value of $k$ digits is $1 + 3 + \cdots + 3^{k-1} = \frac{3^k - 1}{2}$, and the smallest is its negative, so the $3^k$ strings of $k$ digits take values in a set of $3^k$ integers. *Existence.* For $n \ne 0$, let $r \in \{-1, 0, 1\}$ be the unique digit with $r \equiv n \pmod 3$, and $q = (n - r)/3$. Then $|q| \le (|n| + 1)/3 < |n|$, so repeating the step reaches 0, and the digits $r$ in order form a numeral for $n$. *Uniqueness.* If $\sum d_i 3^i = \sum e_i 3^i$, then $d_0 \equiv e_0 \pmod 3$, and two digits of $\{-1, 0, 1\}$ that are congruent mod 3 are equal. Subtract $d_0$, divide by 3 and repeat. So the map from $k$-digit strings to the range is a bijection, and each integer has one normalized numeral. $\blacksquare$

The existence proof is the conversion algorithm: it is [division with remainder](/division-with-remainder/) by 3 with the remainder taken in $\{-1, 0, 1\}$ instead of $\{0, 1, 2\}$. Equivalently, for $|n| \le \frac{3^k - 1}{2}$, write $n + \frac{3^k - 1}{2}$ in ordinary ternary with $k$ digits and subtract 1 from each digit.

**Basic properties.**

- *Negation* replaces each digit $d_i$ by $-d_i$ (swap 1 and T). There is no separate sign, and no asymmetry as in [two's complement](/twos-complement/), where $-2^{w-1}$ has no negative.
- *Sign.* $n > 0$ exactly when the leading digit is 1, because the leading term $3^{k-1}$ is larger than the sum $\frac{3^{k-1} - 1}{2}$ of all lower terms.
- *Comparison* of two numerals padded to the same length is lexicographic with $\mathrm{T} < 0 < 1$.
- *Rounding.* The fractional numerals $0.d_1 d_2 \ldots$ have values in $[-\frac12, \frac12]$. So cutting off the digits after the point rounds a number to a nearest integer: truncation and rounding are the same operation.
- *Addition.* The digit sum $a_i + b_i + c_i$ lies in $\{-3, \ldots, 3\}$, and it is written as $s_i + 3 c_{i+1}$ with $s_i, c_{i+1} \in \{-1, 0, 1\}$. Subtraction is addition of the negation.
- *Multiplication* of digits needs no carry: $1 \cdot 1 = \mathrm{T} \cdot \mathrm{T} = 1$ and $1 \cdot \mathrm{T} = \mathrm{T}$. A partial product is the multiplicand, its negation or zero.

## Examples and non-examples

**Small integers.** Each row is a normalized numeral and its value.

| $n$ | numeral | check |
|---|---|---|
| 1 | $1$ | $1$ |
| 2 | $1\mathrm{T}$ | $3 - 1$ |
| 5 | $1\mathrm{T}\mathrm{T}$ | $9 - 3 - 1$ |
| $-5$ | $\mathrm{T}11$ | $-9 + 3 + 1$ |
| 8 | $10\mathrm{T}$ | $9 - 1$ |
| 13 | $111$ | $9 + 3 + 1$, the largest 3-digit value |
| 25 | $10\mathrm{T}1$ | $27 - 3 + 1$ |
| 100 | $11\mathrm{T}01$ | $81 + 27 - 9 + 1$ |
| 2026 | $10\mathrm{T}10001$ | $2187 - 243 + 81 + 1$ |

**Conversion of 100.** $100 = 3 \cdot 33 + 1$, digit 1. $33 = 3 \cdot 11 + 0$, digit 0. $11 = 3 \cdot 4 - 1$, digit T. $4 = 3 \cdot 1 + 1$, digit 1. $1 = 3 \cdot 0 + 1$, digit 1. Read from the last digit: $11\mathrm{T}01$.

**Addition.** $5 + 8 = 1\mathrm{TT} + 10\mathrm{T}$. Position 0: $-1 - 1 = -2 = 1 + 3 \cdot (-1)$, digit 1 and carry T. Position 1: $-1 + 0 - 1 = -2$, digit 1 and carry T. Position 2: $1 + 1 - 1 = 1$, digit 1 and no carry. The sum is $111 = 13$.

**Weights.** With weights of 1, 3, 9 and 27 grams on a balance, every whole weight up to 40 grams can be measured, putting a weight on the same pan as the object for the digit T and on the other pan for the digit 1. For example $25 = 10\mathrm{T}1$: 27 and 1 on one side, the object and 3 on the other. The four weights cover exactly $-40, \ldots, 40$, since $40 = 1111$.

**Radix economy.** If the cost of a digit is proportional to the base $b$, the cost of representing numbers up to $N$ is about $b \cdot \log_b N = \frac{b}{\ln b} \ln N$. The factor $b / \ln b$ is smallest at $b = e$, and among integers at $b = 3$: it is $2.731$ for base 3, $2.885$ for base 2, and $4.343$ for base 10. This is a heuristic argument for ternary hardware, not a law of circuits.

**Non-examples.**

- Ordinary ternary, with digits 0, 1 and 2, needs a separate sign for negative numbers; 5 is $12$ in ordinary ternary but $1\mathrm{TT}$ in balanced ternary.
- The digit set $\{-1, 0, 1\}$ in base 2 is a [signed-digit representation](/signed-digit-representation/) that is *redundant*: $1 = 01 = 1\mathrm{T}$, since $2 - 1 = 1$. Balanced ternary has the same digits but base 3, and it is not redundant. The [non-adjacent form](/non-adjacent-form/) chooses one of the binary signed-digit forms.
- Fractions are not always unique: $\frac12 = 0.111\ldots = 1.\mathrm{TTT}\ldots$ in balanced ternary, the analogue of $0.999\ldots = 1$ in decimal. The uniqueness theorem is about integers and finite numerals.
- A string with leading zeros, such as $0101$, is a valid numeral but not normalized; it has the same value 10 as $101$.

## Related definitions

- [Positional number system](/positional-number-system/): balanced ternary is the base 3 case with the digit set $\{-1, 0, 1\}$.
- [Signed-digit representation](/signed-digit-representation/): positional systems with negative digits. In an odd base $\beta$ the digit set $\{-\frac{\beta-1}{2}, \ldots, \frac{\beta-1}{2}\}$ is the *balanced* system of base $\beta$, nonredundant like balanced ternary; larger digit sets give the [redundant number systems](/redundant-number-system/) used to limit carries.
- [Two's complement](/twos-complement/) and [ones' complement](/ones-complement/): the binary encodings of signed integers. In ones' complement negation flips every bit, as here, but zero has two forms; in two's complement negation is a flip followed by adding 1.
- [Non-adjacent form](/non-adjacent-form/): a binary signed-digit form with no two adjacent nonzero digits, used to save operations in exponentiation.
- [Radix conversion](/radix-conversion/): the conversion between bases, of which the algorithm above is one case.

## References
