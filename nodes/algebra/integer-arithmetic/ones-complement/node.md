---
tag: QQ16ZW
kind: definition
slug: ones-complement
name: One's complement
aliases:
- 1's complement
- ones' complement
- ones-complement representation
area: algebra/integer-arithmetic
level: intro
summary: Signed integer encoding where negation is bitwise inversion, with two representations of zero.
prereqs: [positional-number-system, bitwise-operations]
see_also: [twos-complement, sign-magnitude-representation, ones-complement-arithmetic, integer-overflow, congruence, signed-digit-representation]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.1, Positional number systems (signed magnitude, ones' complement and two's complement notations, and the placement of the apostrophe)
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 2, Representing signed numbers (complement representations, diminished-radix complement, end-around carry)
  - book: isbn:9780134092669
    title: Randal E. Bryant and David R. O'Hallaron, Computer Systems, A Programmer's Perspective, third edition, Pearson, 2016
    locator: Section 2.2.3, Two's-complement encodings (the aside on other representations of signed numbers)
  - url: https://www.rfc-editor.org/rfc/rfc1071
    title: R. Braden, D. Borman and C. Partridge, RFC 1071, Computing the Internet Checksum, 1988
    locator: Section 1 and Section 2 (the one's complement sum and its properties)
---

One's complement is an encoding of signed integers in $w$ bits in which the negative of a value is its bitwise complement: every 0 bit becomes 1 and every 1 bit becomes 0. The top bit acts as a sign, the range is $[-(2^{w-1} - 1), 2^{w-1} - 1]$, and zero has two encodings, $00\cdots0$ and $11\cdots1$, the second called negative zero. Arithmetic in one's complement is arithmetic modulo $2^w - 1$, and addition uses an *end-around carry*: a carry out of the top bit is added back into the bottom bit. Several early computers used it, but [two's complement](/twos-complement/) has replaced it in processors; it survives in the Internet checksum.

## Definition

Fix a width $w \ge 2$. A word is a string $x = x_{w-1} x_{w-2} \cdots x_0$ of bits, and $U(x) = \sum_{i=0}^{w-1} x_i 2^i$ is its unsigned value in the [positional number system](/positional-number-system/) of radix 2.

**One's complement value.** The one's complement value of $x$ is

$$O(x) = \sum_{i=0}^{w-2} x_i 2^i \; - \; x_{w-1}\,(2^{w-1} - 1) .$$

The top bit has the weight $-(2^{w-1} - 1)$ instead of $+2^{w-1}$. Equivalently, $O(x) = U(x)$ if $x_{w-1} = 0$, and $O(x) = U(x) - (2^w - 1)$ if $x_{w-1} = 1$.

**Complement.** The one's complement of $x$ is the word $\bar{x}$ with $\bar{x}_i = 1 - x_i$ for every $i$, the bitwise NOT. Since $U(x) + U(\bar{x}) = 2^w - 1$ (the word of all ones), the name is the complement with respect to $11\cdots1$.

**Facts.**

1. **Range.** $O$ takes every value in $[-(2^{w-1} - 1), 2^{w-1} - 1]$. Each nonzero value has exactly one encoding, and $0$ has two: $00\cdots0$ (positive zero) and $11\cdots1$ (negative zero). So $2^w$ words encode $2^w - 1$ values.
2. **Negation.** $O(\bar{x}) = -O(x)$ for every word $x$. If $x_{w-1} = 0$, then $\bar{x}$ has top bit 1 and $O(\bar{x}) = (2^w - 1 - U(x)) - (2^w - 1) = -U(x)$. The case $x_{w-1} = 1$ is the same with the roles exchanged.
3. **Sign.** The top bit is 1 exactly for the negative values and for negative zero. A nonnegative value has the same encoding as in the unsigned and the two's complement systems.
4. **Congruence.** $O(x) \equiv U(x) \pmod{2^w - 1}$, from the second form of the value. So one's complement arithmetic is arithmetic of residues modulo $2^w - 1$, with the residue $0$ written two ways.
5. **End-around carry.** To add $O(x) + O(y)$, add $U(x) + U(y)$ in $w$ bits. If there is a carry out of bit $w - 1$, add 1 to the low bit; this second addition cannot carry out. The result is correct whenever the true sum is in the range. The reason is fact 4: the carry out has the weight $2^w \equiv 1 \pmod{2^w - 1}$.
6. **Overflow.** The sum overflows exactly when the two operands have the same sign bit and the result has the other one, the same rule as in two's complement; see [integer overflow](/integer-overflow/).

The name is written *one's complement* or *ones' complement*. Knuth argues for the second, because the complement is taken with respect to a word of many ones, while *two's complement* is taken with respect to a single power of two.

## Examples and non-examples

All examples use $w = 8$, so the range is $[-127, 127]$. They were checked by script.

- **A pair.** $5 = 00000101$ and $-5 = 11111010$: each bit is flipped, and $O(11111010) = 250 - 255 = -5$.
- **End-around carry.** $7 + (-5)$: $00000111 + 11111010 = 1\,00000001$. The carry out of bit 7 is 1, so add it to the low bit: $00000001 + 1 = 00000010 = 2$.
- **Two negatives.** $(-3) + (-4)$: $11111100 + 11111011 = 1\,11110111$, and the end-around carry gives $11111000 = -7$.
- **Negative zero.** $5 + (-5)$: $00000101 + 11111010 = 11111111$, with no carry out. This is negative zero, $O(11111111) = 255 - 255 = 0$. A test for zero must accept both words.
- **Overflow.** $100 + 100 = 200 > 127$: the sum $11001000$ has top bit 1, and $O(11001000) = 200 - 255 = -55$. Both operands are positive and the result is negative, so the overflow is detected.
- **The extremes.** $127 = 01111111$ and $-127 = 10000000$. Unlike two's complement, there is no $-128$, and the range is symmetric, so negation never overflows.

**Non-examples.**

- **$10000000$ is not $-128$.** In two's complement it is; in one's complement it is $-127$, and $11111111$ is $-0$, not $-1$.
- **Adding without the end-around carry** is not one's complement addition. Dropping the carry in $7 + (-5)$ gives $00000001 = 1$, which is wrong by one.
- **Sign-magnitude.** The word $10000101$ is $-5$ in [sign-magnitude](/sign-magnitude-representation/), but $-122$ in one's complement: flipping only the sign bit is not the one's complement negation.

## Related definitions

- **Two's complement.** The radix complement $2^w - U(x)$, one more than the one's complement. It has one zero and the range $[-2^{w-1}, 2^{w-1} - 1]$, and its arithmetic is modulo $2^w$, so plain binary addition works without an end-around carry. See [two's complement](/twos-complement/). In general radix $r$, the one's complement is the *diminished radix complement* $(r^w - 1) - U(x)$, for example the nines' complement in decimal.
- **Sign-magnitude.** A sign bit and an unsigned magnitude. It also has two zeros and the same range. See [sign-magnitude representation](/sign-magnitude-representation/).
- **One's complement sum.** The checksum of IP, TCP and UDP is the one's complement of the one's complement sum of 16-bit words, as in RFC 1071. Because the sum is modulo $2^{16} - 1$, it is the same on machines of either byte order, and it can be updated when one word changes. See [one's complement arithmetic](/ones-complement-arithmetic/).
- **Modular arithmetic.** Fact 4 makes one's complement a representation of the ring of integers modulo $2^w - 1$; see [congruence](/congruence/).

### History

Several early computers used one's complement for their integers, among them the CDC 6600, the UNIVAC 1100 series and the PDP-1. The cost of two zeros, and the extra end-around carry, led later machines to use two's complement. The C standard allowed one's complement, sign-magnitude and two's complement for signed integers until C23, and C++ until C++20; both now require two's complement.

## References
