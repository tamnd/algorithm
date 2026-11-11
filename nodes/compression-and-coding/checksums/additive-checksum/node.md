---
tag: MQA7XD
kind: algorithm
slug: additive-checksum
name: Additive checksum
aliases:
- modular sum checksum
- byte sum checksum
area: compression-and-coding/checksums
level: intro
summary: Add the data words modulo 2^k, the simplest multi-bit checksum. It catches every one-word error but misses reordered words and errors that cancel.
model: word-ram
complexity:
  vars: {n: the number of message bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1988
  people: [Intel]
  note: The method is older than any single document and has no known inventor. Intel's hexadecimal object file format (Revision A, 1988) is a well known use, with the two's complement of the 8-bit byte sum as the record checksum.
prereqs: [checksum, congruence]
see_also: [twos-complement, ones-complement-arithmetic, internet-checksum, fletcher-checksum, longitudinal-redundancy-check, cyclic-redundancy-check, undetected-error-probability, error-detection]
sources:
  - paper: doi:10.1109/TDSC.2007.70216
    title: Theresa C. Maxino and Philip J. Koopman, The effectiveness of checksums for embedded control networks, IEEE Transactions on Dependable and Secure Computing 6(1), 2009, pages 59 to 72
    locator: Section 3.2 (the two's complement addition checksum, its undetected pairs of errors in the top bit) and Section 3.3 (the ones' complement addition checksum for comparison)
  - paper: "Intel Corporation, Hexadecimal Object File Format Specification, Revision A, January 6, 1988"
    title: Hexadecimal Object File Format Specification
    locator: The record format, the CHKSUM field (the two's complement of the 8-bit sum of the record bytes)
  - url: https://www.rfc-editor.org/rfc/rfc1071
    title: R. Braden, D. Borman and C. Partridge, RFC 1071, Computing the Internet Checksum, September 1988
    locator: Section 3 (the example bytes 00 01 f2 03 f4 f5 f6 f7, used on this page with a two's complement sum for contrast)
---

An additive checksum adds the words of a message modulo $2^k$ and keeps the low $k$ bits of the total. With bytes ($k = 8$) it is the 8-bit sum mod 256; with 16-bit words it is the sum mod 65536. It is the simplest [checksum](/checksum/) with more than one bit. It catches every change to a single word, but it cannot see the order of the words, and it misses any set of changes whose total is a multiple of $2^k$. This page is about the plain sum in [two's complement](/twos-complement/) arithmetic, where the carry out of the top bit is lost. The [ones' complement](/ones-complement-arithmetic/) sum, which adds that carry back in, is the base of the [Internet checksum](/internet-checksum/). The [Fletcher checksum](/fletcher-checksum/) adds a second sum that sees the order.

## In plain words

Read the message as a list of numbers, for example one number per byte. Add them all up. Keep only the last part of the total, as a car odometer keeps only its last digits. Send that short number with the message. The receiver adds the numbers again and compares.

If one number changes, the total changes, so the error is caught. But addition does not care about order. If two numbers swap places, the total is the same, and the error is missed. If one number goes up by 5 and another goes down by 5, the total is also the same. So the sum is cheap and catches simple slips, but it is weak against errors that come in pairs.

## The problem

The input is a message of $n$ bytes and a word size of $w$ bytes, with $k = 8w$ bits per word. If $n$ is not a multiple of $w$, append zero bytes up to the next multiple. Read the message as words $x_1, \ldots, x_m$ with $m = \lceil n/w \rceil$, each a big-endian unsigned integer in $[0, 2^k)$. The output is

$$S = \left(\sum_{i=1}^{m} x_i\right) \bmod 2^k.$$

The sender either sends $S$ next to the message, or appends a check word $c = (-S) \bmod 2^k$, so that the sum of the message and $c$ is 0. The receiver accepts the message when its own sum matches, or when the sum with $c$ is 0. We write the cost in the [word RAM](/word-ram/) model, with one $k$-bit addition per word.

## The algorithm

```pseudo id=main
ADDITIVE-CHECKSUM(x[1 .. m], k)            ▷ words of k bits
L1  s ← 0
L2  for i ← 1 to m do
L3      read the word x[i]                  ▷ w = k/8 bytes, big-endian, zero padded at the end
L4      s ← (s + x[i]) mod 2^k              ▷ two's complement addition: drop the carry out of bit k − 1
L5  return s
```

On a machine with $k$-bit registers, line L4 is one ADD instruction, and the reduction mod $2^k$ is free, because the carry out of the top bit is lost. The check word is the two's complement negation $c = (2^k - s) \bmod 2^k$. A receiver can run the same loop over the message and the check word and test for 0.

## Example

Take the eight bytes 00 01 f2 03 f4 f5 f6 f7 from RFC 1071 Section 3. The 8-bit sum ($k = 8$) runs as follows.

| byte | 00 | 01 | f2 | 03 | f4 | f5 | f6 | f7 |
|---|---|---|---|---|---|---|---|---|
| $s$ after line L4 | 00 | 01 | f3 | f6 | ea | df | d5 | cc |

So the 8-bit sum is 0xCC, and its check byte is $0x100 - 0xCC = 0x34$. With 16-bit words ($k = 16$), the words are 0001, f203, f4f5 and f6f7. Their total is 0x2DDF0. The carry 2 is lost, so the 16-bit sum is 0xDDF0, and the check word is 0x2210. The ones' complement sum of the same words adds the carry back and gives 0xDDF2, the value in RFC 1071.

A real use: the Intel HEX record `:0300300002337A1E` holds the bytes 03 00 30 00 02 33 7A and the checksum byte 1E. The bytes sum to 0xE2, and $0x100 - 0xE2 = 0x1E$. The sum of all eight bytes is 0x100, which is 0 mod 256.

## Correctness

The loop of line L2 keeps the invariant $s = (x_1 + \cdots + x_{i-1}) \bmod 2^k$, so line L5 returns $S$. The check word works because $S + c \equiv 0 \pmod{2^k}$. The detection result is exact: an error that changes word $i$ by $\delta_i$ (with $-2^k < \delta_i < 2^k$) is missed if and only if $\sum_i \delta_i \equiv 0 \pmod{2^k}$. So every change to one word is caught, and every permutation of the words is missed. The proofs are in the correctness file below.

## Complexity

The loop does one addition per word, so the time is $\Theta(m) = \Theta(n/w)$ word operations, which is $\Theta(n)$ for a fixed word size, in each case. The extra space is one $k$-bit register, $\Theta(1)$. The sum is [online](/online-algorithm/): it can take the message in pieces of any length that is a multiple of $w$. Because addition is associative and commutative, several cores or SIMD lanes can add parts of the message and then add their partial sums.

## Properties

- **Every single-word error is caught.** A change $\delta \ne 0$ with $|\delta| < 2^k$ is not a multiple of $2^k$. In particular, every single-bit error is caught.
- **Order is invisible.** Any permutation of the words gives the same sum. With $k = 8$, all 28 swaps of two of 8 distinct bytes are missed. With $k = 16$ on the same 8 bytes, a swap of two bytes in the same half of their words (both high or both low) is missed, and a swap of a high byte with a low byte changes the sum by $255(b - a)$, which is not 0 mod 65536 when $a \ne b$. So sum16 misses exactly 12 of the 28 swaps.
- **Compensating errors are missed.** Raising one word by $d$ and lowering another by $d$ leaves the sum unchanged, for every $d$.
- **Hamming distance 2.** Two bit errors can cancel. On all 65536 two-byte messages, flipping the top bit of both bytes changes the sum by 0 or $\pm 256$, so the 8-bit sum misses all 65536 cases. The ones' complement sum mod 255 misses only the 32768 cases where one top bit goes from 0 to 1 and the other from 1 to 0 (Maxino and Koopman, Section 3.2 and 3.3).
- **Uniform spread on random data.** For two-byte messages, each of the 256 values of the 8-bit sum is taken by exactly 256 messages. So a random wrong message of the same length is missed with probability $255/65535 = 1/257$.

The tests check each of these counts by enumeration.

## Variants and improvements

- **Ones' complement sum.** Add the carry out of the top bit back into the low bit, which is the same as working mod $2^k - 1$. The top bit is then no weaker than the other bits, and the result does not depend on the byte order. See [ones' complement arithmetic](/ones-complement-arithmetic/) and the [Internet checksum](/internet-checksum/).
- **XOR instead of ADD.** The [longitudinal redundancy check](/longitudinal-redundancy-check/) XORs the bytes. It has no carries at all, so it is weaker: two flips in the same bit column always cancel. The ASCII mode of Modbus calls its two's complement byte sum an LRC.
- **Position-dependent sums.** The [Fletcher checksum](/fletcher-checksum/) and [Adler-32](/adler-32/) add a second sum of the running sums, which weights each word by its position and so detects most swaps.
- **Polynomial division.** A [CRC](/cyclic-redundancy-check/) treats the message as a polynomial over GF(2). It detects all bursts up to its width and has a larger Hamming distance at the same check size.

## When to use it

Use an additive checksum when the cost must be as small as possible and the errors you expect are single, independent changes: a small boot loader, a record in a text file format such as Intel HEX, or a hand-written protocol on a slow serial line. Do not use it to detect reordered or shifted data, data with many 0x00 or 0xFF bytes, or deliberate changes. For a small extra cost, the ones' complement sum or Fletcher's checksum is better, and a CRC is better again.

## Pitfalls

- **Treating the check word as a separate sum.** If the sender appends $c = -S$, the receiver must sum the message and $c$ and test for 0. Summing only the message and comparing with $c$ fails.
- **The padding rule.** With $k = 16$, an odd last byte must be padded on the right, as the high byte of the last word. Padding on the left gives a different sum.
- **Byte order.** A 16-bit sum of big-endian words differs from a sum of little-endian words. Both ends must agree. The ones' complement sum does not have this problem.
- **Signed arithmetic.** In C, adding `char` values that are signed gives a different sum from unsigned bytes once the total is reduced. Use unsigned types.
- **Expecting order to count.** A shuffled or rotated record passes the check. If order matters, use Fletcher or a CRC.

## Implementations

## History

Adding up the data is one of the oldest ways to check it, and it has no single inventor. Many record formats use the 8-bit sum or its two's complement. Intel's hexadecimal object file format, Revision A of 1988, defines the record checksum as the two's complement of the 8-bit sum of the record bytes. The ones' complement sum of the ARPANET protocols and Fletcher's checksum (1982) remove two of its weaknesses, the weak top bit and the blindness to order. Maxino and Koopman (2009) measured the two's complement sum against the other checksums and found it worse than the ones' complement sum and Fletcher's checksum.

## References
