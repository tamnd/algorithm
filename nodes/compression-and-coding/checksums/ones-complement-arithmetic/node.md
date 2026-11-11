---
tag: RDWD1R
kind: concept
slug: ones-complement-arithmetic
name: Ones' complement arithmetic
aliases:
- one's complement arithmetic
- end-around carry
area: compression-and-coding/checksums
level: intro
summary: Addition of k-bit words in which the carry out of the top bit wraps around to the low bit. It is addition mod 2^k - 1 with two zeros, and the base of the Internet checksum.
prereqs: [ones-complement]
see_also: [internet-checksum, incremental-checksum-update, additive-checksum, fletcher-checksum, twos-complement, congruence, checksum]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc1071
    title: R. Braden, D. Borman and C. Partridge, RFC 1071, Computing the Internet Checksum, September 1988
    locator: Section 1 (the one's complement sum and the -0 test), Section 2 (A) to (C) (commutative and associative, byte order independence, parallel summation) and items (1) to (4) (deferred carries, unwinding loops, data copying, incremental update), Section 3 (the numerical examples)
  - url: https://www.rfc-editor.org/rfc/rfc1624
    title: A. Rijsinghani, editor, RFC 1624, Computation of the Internet Checksum via Incremental Update, May 1994
    locator: Section 3 (the two zeros of ones' complement arithmetic, +0 and -0) and Section 6 (the CDC 6000 series, which used subtraction as its primitive)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.1, Positional number systems (ones' complement notation)
  - paper: doi:10.1109/TDSC.2007.70216
    title: Theresa C. Maxino and Philip J. Koopman, The effectiveness of checksums for embedded control networks, IEEE Transactions on Dependable and Secure Computing 6(1), 2009, pages 59 to 72
    locator: Section 3.3 (the ones' complement addition checksum, why the end-around carry helps the top bit)
---

Ones' complement arithmetic adds two $k$-bit words and, when the sum carries out of the top bit, adds that carry back into the low bit. This *end-around carry* makes the addition work modulo $2^k - 1$ instead of $2^k$. The value $2^k - 1$, all ones, is a second zero, called *negative zero* or $-0$. The page [ones' complement](/ones-complement/) defines the signed number encoding with bitwise negation. This page is about the addition itself as checksums use it: the unsigned view, the two zeros, the fold of a wide sum, and the facts that make the [Internet checksum](/internet-checksum/) fast, such as byte order independence.

## In plain words

Think of a counter with four digits that runs from 0000 to 9999. Normal adding throws away anything above 9999. Ones' complement adding keeps it: when the counter overflows, the extra 1 goes back in at the bottom. Then nothing is lost, and the counter behaves as if it counts around a circle of 9999 places, not 10000.

On a computer the digits are bits. The overflow bit is added back in at the low end. The result is a sum in which every bit of the input has the same weight, including the top bit. There is one odd thing: all ones and all zeros both mean zero. Checksums use this addition because it is cheap, does not care about byte order, and lets a fast machine add 32 or 64 bits at a time and fold the result down.

## The idea

**The operation.** For $k$-bit words $a, b \in [0, 2^k - 1]$, the ones' complement sum is

$$a \oplus b = \begin{cases} a + b & \text{if } a + b < 2^k, \\ a + b - 2^k + 1 & \text{otherwise.} \end{cases}$$

In code with $k = 16$, this is the add-and-fold of lines L1 to L3 below. A long sum may defer the carries into a wider register and fold at the end, lines L4 to L6.

```pseudo id=main
ADD16(a, b)                                ▷ a, b in [0, 0xFFFF]
L1  s ← a + b                              ▷ at most 0x1FFFE
L2  s ← (s and 0xFFFF) + (s >> 16)         ▷ end-around carry: add the carry back at bit 0
L3  return s

FOLD(x)                                    ▷ x ≥ 0, for example a 32-bit or 64-bit sum
L4  while x ≥ 2^16 do
L5      x ← (x and 0xFFFF) + (x >> 16)
L6  return x
```

**Arithmetic mod $2^k - 1$.** Since $2^k \equiv 1 \pmod{2^k - 1}$, the value $c \cdot 2^k + r$ is congruent to $c + r$. So line L2 and line L5 keep the value mod $2^k - 1$, and each run makes the value smaller while it is at least $2^k$. Line L2 needs only one run: $a + b \le 2^{k+1} - 2$, so $c \le 1$ and $c + r \le 2^k - 1$. The result is never $2^k$, so no second carry can occur.

**Two zeros.** The words $0$ ($+0$) and $2^k - 1$ ($-0$) are both $\equiv 0 \pmod{2^k - 1}$. The sum keeps them apart in a precise way. For words $x_1, \ldots, x_m$ and $T = \sum x_i$, the repeated sum $x_1 \oplus \cdots \oplus x_m$ (from $0$) equals $0$ if every $x_i = 0$, and otherwise the unique value in $[1, 2^k - 1]$ that is congruent to $T$ modulo $2^k - 1$. Proof: a step that starts from a nonzero value or adds a nonzero word gives a result of at least 1, because line L2 never returns 0 from a positive $s$; and a value in $[1, 2^k - 1]$ is fixed by its residue. So $x \oplus (\lnot x) = -0$ for every $x$, and a sum of nonzero data that is a multiple of $2^k - 1$ is $-0$, never $+0$. RFC 1624 Section 3 builds on this.

**Commutative and associative.** By the rule above, the result depends only on $T$ and on whether all words are zero. So the order and the grouping of the words do not matter (RFC 1071 Section 2 (A)). This is what lets many cores, SIMD lanes or a wider register add parts of the data and combine them.

**Byte order independence.** Let $\mathrm{swap}(x)$ exchange the two bytes of a 16-bit word. If $x = 256h + l$, then $\mathrm{swap}(x) = 256l + h$, and

$$256 \cdot x = 65536h + 256l \equiv h + 256l = \mathrm{swap}(x) \pmod{65535}.$$

So swapping bytes is the same as multiplying by 256 modulo 65535, and multiplication distributes over the sum: $\mathrm{swap}(x_1) \oplus \cdots \oplus \mathrm{swap}(x_m) = \mathrm{swap}(x_1 \oplus \cdots \oplus x_m)$. Both zeros map to themselves. So a little-endian machine can add the words in its own byte order and swap only the result (RFC 1071 Section 2 (B)). A two's complement sum does not have this property.

**Wide sums and the fold.** A machine with 32-bit or 64-bit registers can add the data 4 or 8 bytes at a time, with an end-around carry at that width. Since $2^{32} - 1 = 65535 \cdot 65537$ and $2^{64} - 1 = (2^{32} - 1)(2^{32} + 1)$, a sum mod $2^{32} - 1$ or mod $2^{64} - 1$ keeps its residue mod 65535. FOLD then brings it down to 16 bits (RFC 1071 Section 2 (C)). A second way is to add the 16-bit words into a 32-bit register without any end-around carry, and fold once at the end. This is the deferred carry of RFC 1071 Section 2 (1). It is safe for up to 65537 words, because $65537 \cdot 65535 = 2^{32} - 1$.

**Negation and subtraction.** The ones' complement negative of $x$ is $\lnot x = 2^k - 1 - x$, the bitwise complement, so $a - b$ is $a \oplus \lnot b$. The checksum takes the complement of the sum, so that a receiver that adds the data and the checksum gets $-0$, all ones.

## Examples

**Small cases with $k = 16$.**

| $a$ | $b$ | $a + b$ | $a \oplus b$ | note |
|---|---|---|---|---|
| 0x8000 | 0x8000 | 0x10000 | 0x0001 | the carry comes back as 1 |
| 0x1234 | 0xEDCB | 0xFFFF | 0xFFFF | $x \oplus \lnot x = -0$ |
| 0xFFFF | 0xFFFF | 0x1FFFE | 0xFFFF | $-0 \oplus -0 = -0$ |
| 0xFFFF | 0x0000 | 0xFFFF | 0xFFFF | $-0 \oplus +0 = -0$ |
| 0x0000 | 0x0000 | 0x0000 | 0x0000 | the only way to get $+0$ |

**RFC 1071 Section 3.** The bytes 00 01 f2 03 f4 f5 f6 f7, as big-endian words, are 0001, f203, f4f5 and f6f7. Their total is 0x2DDF0, and the fold gives $0xDDF0 + 0x2 = 0xDDF2$. Read as little-endian words, the same bytes give 0x0100, 0x03f2, 0xf5f4 and 0xf7f6, and the sum is 0xF2DD, which is $\mathrm{swap}(0xDDF2)$. With 32-bit chunks the sum is $0x0001F203 + 0xF4F5F6F7 = 0xF4F7E8FA$, with no carry. The fold gives $0xF4F7 + 0xE8FA = 0x1DDF1$, then $0xDDF1 + 1 = 0xDDF2$. With one 64-bit chunk, 0x0001F203F4F5F6F7 folds to the same 0xDDF2. All four numbers match the RFC.

**Fold of a large value.** $\mathrm{FOLD}(2^{64} - 1)$ runs $0xFFFFFFFFFFFF + 0xFFFF$, and so on, and ends at 0xFFFF. This is $-0$, as it must be: $2^{64} - 1$ is a nonzero multiple of 65535.

The implementation checks all of these values. It also checks ADD16 on a grid of pairs against $a + b \bmod 65535$, 600 random sums of up to 29 words, rich in 0x0000 and 0xFFFF, against the rule for the two zeros, byte order independence on random data, and the 32-bit and 64-bit chunk sums against the 16-bit sum.

## Where it is used

- **The Internet checksum** of IPv4, ICMP, UDP and TCP is the complement of the 16-bit ones' complement sum (RFC 1071). See [Internet checksum](/internet-checksum/). Its [incremental update](/incremental-checksum-update/) after a router changes one header field is the place where the two zeros matter most (RFC 1141 and RFC 1624).
- **Fletcher's checksum** in its 1's complement form sums modulo 255 or 65535 (RFC 1146 Appendix I). See [Fletcher checksum](/fletcher-checksum/).
- **Hardware.** Several early computers, such as the CDC 6600 and the UNIVAC 1100 series, used ones' complement integers. Today almost every processor uses [two's complement](/twos-complement/), and checksum code builds the end-around carry from a normal add and an add-with-carry instruction, or from a wide sum and a fold.
- **Detection strength.** The end-around carry gives the top bit the same weight as the others. So the ones' complement checksum detects a pair of top-bit flips that the two's complement [additive checksum](/additive-checksum/) misses, and it detects all bursts shorter than the word size (Maxino and Koopman, Section 3.3).

## References
