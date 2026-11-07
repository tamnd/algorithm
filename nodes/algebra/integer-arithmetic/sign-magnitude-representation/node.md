---
tag: SGMQGC
kind: definition
slug: sign-magnitude-representation
name: Sign-magnitude representation
aliases:
- signed magnitude
- sign and magnitude
- sign-and-magnitude representation
area: algebra/integer-arithmetic
level: intro
summary: Signed integer encoding that stores a sign bit separately from the absolute value.
prereqs: [positional-number-system]
see_also: [twos-complement, ones-complement, multiprecision-integer, integer-overflow, ieee-754, signed-digit-representation]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.1, Positional number systems (signed magnitude, ones' complement and two's complement notations)
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 2, Representing signed numbers (signed-magnitude representation and its adder)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.1, Representation of integers (a sign and an array of words for the absolute value)
  - url: https://gmplib.org/manual/Integer-Internals
    title: GNU MP manual, Integer Internals
    locator: the fields _mp_size, whose sign is the sign of the integer, and _mp_d, the limbs of the absolute value
---

Sign-magnitude representation writes a signed integer as a sign and the absolute value, kept apart: in $w$ bits, the top bit is 1 for a negative number and 0 otherwise, and the other $w - 1$ bits hold $|v|$ in binary. It is the way people write signed numbers, $-5$ and $+5$, and it makes negation, absolute value and multiplication easy. Addition is harder, since the signs decide whether to add or to subtract the magnitudes, and zero has two encodings. Processors use [two's complement](/twos-complement/) for integers, but sign-magnitude is the form of floating-point numbers and of the [multiprecision integers](/multiprecision-integer/) of libraries such as GMP.

## Definition

Fix a width $w \ge 2$. A word $x = x_{w-1} x_{w-2} \cdots x_0$ of bits has, in sign-magnitude representation, the value

$$S(x) = (-1)^{x_{w-1}} \sum_{i=0}^{w-2} x_i 2^i .$$

The bit $x_{w-1}$ is the **sign** and the number $|S(x)| = \sum_{i < w-1} x_i 2^i$ is the **magnitude**, an unsigned integer in the [positional number system](/positional-number-system/) of radix 2.

**Facts.**

1. **Range.** $S$ takes every value in $[-(2^{w-1} - 1), 2^{w-1} - 1]$. Each nonzero value has exactly one encoding. Zero has two: $00\cdots0$ (positive zero) and $10\cdots0$ (negative zero).
2. **Negation and absolute value.** $-S(x)$ is encoded by flipping the sign bit, and $|S(x)|$ by clearing it. Neither can overflow, since the range is symmetric.
3. **Multiplication and division.** The sign of $S(x) S(y)$ is $x_{w-1} \oplus y_{w-1}$ (exclusive or), and its magnitude is the product of the magnitudes. Quotients use the same rule. The sign and the magnitude are handled apart.
4. **Addition.** If the signs agree, add the magnitudes and keep the sign; the sum overflows exactly when the magnitudes sum to $2^{w-1}$ or more. If the signs differ, compare the magnitudes, subtract the smaller from the larger, and take the sign of the larger. This never overflows. The comparison makes sign-magnitude addition slower than two's complement addition, where one binary adder handles every case.
5. **Order.** Two nonnegative values compare as their magnitudes; two negative values compare in reverse order of their magnitudes. Comparing the words as unsigned integers is wrong for negative values.

**General radix.** The same definition works with any radix and any width: a sign and a magnitude in radix $\beta$. A [multiprecision integer](/multiprecision-integer/) in radix $\beta = 2^w$ is a sign together with an array of $n$ limbs for the magnitude.

## Examples and non-examples

All examples use $w = 8$, so the range is $[-127, 127]$. They were checked by script.

- **A pair.** $+5 = 00000101$ and $-5 = 10000101$: only the sign bit differs.
- **The extremes.** $127 = 01111111$ and $-127 = 11111111$.
- **Negative zero.** $10000000$ is $-0$. A test for zero must look at the magnitude only.
- **Addition, same signs.** $(-3) + (-4)$: the magnitudes add to 7, and the sign stays negative: $10000111 = -7$.
- **Addition, different signs.** $7 + (-5)$: the magnitudes are 7 and 5, the larger is positive, so the result is $+(7 - 5) = 00000010 = 2$. And $5 + (-7) = -(7 - 5) = 10000010 = -2$.
- **Overflow.** $100 + 100$: the magnitudes add to $200 \ge 128$, which does not fit in 7 bits, so the sum overflows.
- **Floating point.** A number in [IEEE 754](/ieee-754/) is a sign bit, an exponent and a significand: the significand is a magnitude, and $-0.0$ and $+0.0$ are different words that compare equal.
- **GMP.** A GMP integer has a field `_mp_size` whose absolute value is the number of limbs and whose sign is the sign of the integer, and an array `_mp_d` of limbs that holds the magnitude. This is sign-magnitude with a magnitude of variable length.

**Non-examples.**

- **$11111111$ is not $-1$.** It is $-1$ in two's complement and $-0$ in [one's complement](/ones-complement/), but $-127$ in sign-magnitude.
- **Plain binary addition is not sign-magnitude addition.** Adding $00000111 + 10000101$ as unsigned words gives $10001100$, which is $-12$, not $7 + (-5) = 2$.
- **Flipping all the bits is not negation.** It maps $00000101 = 5$ to $11111010 = -122$.

## Related definitions

- **Two's complement.** The top bit has the weight $-2^{w-1}$, there is one zero, and addition is plain binary addition modulo $2^w$. See [two's complement](/twos-complement/).
- **One's complement.** The negative of a value is its bitwise complement, and there are two zeros, like here. See [one's complement](/ones-complement/).
- **Excess-$k$ (biased) representation.** The word $x$ encodes $U(x) - k$. The exponent of an IEEE 754 number uses it, with $k = 2^{e-1} - 1$ for an $e$-bit exponent.
- **Signed digits.** Each digit carries its own sign, instead of one sign for the whole number; see [signed-digit representation](/signed-digit-representation/).
- **Integer overflow.** The rules for sign-magnitude overflow are in fact 4; for the other encodings see [integer overflow](/integer-overflow/).

### History

Sign-magnitude is the ordinary written form of signed numbers. Some early binary computers used it for integers, among them the IBM 704 and its successors the IBM 709 and 7090, before two's complement became the rule for processor integers. It remains the form of floating-point numbers and of the arbitrary-precision integers of most libraries, where negation and multiplication by sign rules are cheap and the magnitude can grow.

## References
