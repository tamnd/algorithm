---
tag: 4GV784
kind: algorithm
slug: fletcher-checksum
name: Fletcher checksum
aliases:
- Fletcher-16
- Fletcher-32
area: compression-and-coding/checksums
level: intro
summary: Two running sums modulo 2^b - 1, A of the data and B of A, so that B weights each word by its position. It catches swaps that a plain sum misses, for two additions per word.
model: word-ram
complexity:
  vars: {n: the number of message bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1982
  people: [John G. Fletcher]
  note: Fletcher of the Lawrence Livermore Laboratory published the checksum in the IEEE Transactions on Communications in January 1982. The OSI protocols and RFC 1146 adopted it.
prereqs: [additive-checksum]
see_also: [adler-32, ones-complement-arithmetic, internet-checksum, cyclic-redundancy-check, rolling-checksum, undetected-error-probability, checksum, hamming-distance]
sources:
  - paper: doi:10.1109/TCOM.1982.1095369
    title: John G. Fletcher, An Arithmetic Checksum for Serial Transmissions, IEEE Transactions on Communications COM-30(1), January 1982, pages 247 to 252
    locator: The two sums, the moduli 255 and 256, and the analysis of the errors detected
  - paper: doi:10.1109/TDSC.2007.70216
    title: Theresa C. Maxino and Philip J. Koopman, The effectiveness of checksums for embedded control networks, IEEE Transactions on Dependable and Secure Computing 6(1), 2009, pages 59 to 72
    locator: Section 3.4 (the Fletcher checksum, its Hamming distance by data length, and the 0x00 and 0xFF weakness) and Section 4.3 (Fletcher compared with Adler)
  - url: https://www.rfc-editor.org/rfc/rfc1146
    title: J. Zweig and C. Partridge, RFC 1146, TCP Alternate Checksum Options, March 1990
    locator: Appendix I (the 8-bit Fletcher checksum, 1's complement form) and Appendix II (the 16-bit Fletcher checksum)
  - url: https://www.rfc-editor.org/rfc/rfc1561
    title: D. Piscitello, RFC 1561, Use of ISO CLNP in TUBA Environments, December 1993
    locator: Appendix A, Checksum Algorithms (from ISO/IEC 8473), the generation, checking and adjustment of the check octets X and Y
  - url: https://www.rfc-editor.org/rfc/rfc1950
    title: P. Deutsch and J-L. Gailly, RFC 1950, ZLIB Compressed Data Format Specification version 3.3, May 1996
    locator: Section 2.2 (Adler-32 as an extension of the Fletcher algorithm of ITU-T X.224 / ISO 8073) and Section 8.2 (why Fletcher's modulus 255 misses 0x00 versus 0xFF)
---

The Fletcher checksum keeps two running sums over the data words: $A$ adds the words, and $B$ adds the values of $A$. Both sums are taken modulo $M = 2^b - 1$, which is 255 for Fletcher-16 (bytes, $b = 8$) and 65535 for Fletcher-32 (16-bit words, $b = 16$). The checksum is $B \cdot 2^b + A$. Since $B$ gives the last word weight 1, the one before it weight 2, and so on, the checksum sees the order of the words, which the [additive checksum](/additive-checksum/) and the [Internet checksum](/internet-checksum/) cannot. John G. Fletcher published it in 1982. The OSI transport and network protocols use it, and [Adler-32](/adler-32/) is a variant with a prime modulus. Its main weakness is that the words 0x00 and 0xFF (or 0x0000 and 0xFFFF) are the same number modulo $M$.

## In plain words

Keep two counters. For each byte, add the byte to the first counter, then add the first counter to the second. The first counter is the plain sum. The second counter is a sum of sums: the first byte has been added into it many times, the last byte only once.

So if two bytes swap places, the first counter does not change, but the second one does, because the two bytes now count a different number of times. Both counters wrap around at 255, which uses the end-around carry of [ones' complement arithmetic](/ones-complement-arithmetic/). Because of that wrap, the byte 255 counts the same as 0, and a change from one to the other is never caught.

## The problem

The input is a message of $n$ bytes. Fletcher-16 reads it as bytes, $d_1, \ldots, d_m$ with $m = n$ and $M = 255$. Fletcher-32 reads it as 16-bit words, with $m = \lceil n/2 \rceil$ and $M = 65535$, after one zero byte of padding if $n$ is odd. The output is the pair

$$A = \sum_{i=1}^{m} d_i \bmod M, \qquad B = \sum_{i=1}^{m} (m - i + 1)\, d_i \bmod M,$$

packed as $B \cdot 2^b + A$. The second form of $B$ follows from $B = \sum_i A_i$, where $A_i = d_1 + \cdots + d_i$. Fletcher-32 needs a byte order for its words. The common test vectors use little-endian words. The checksum is defined up to that choice, so both ends must agree. We count word operations in the [word RAM](/word-ram/) model with 32-bit registers.

## The algorithm

The definition reduces both sums after each word. Fast code defers the reduction: it adds up to $K$ words into 32-bit sums and reduces at the end of each block.

```pseudo id=main
FLETCHER(d[1 .. m], M, K)                  ▷ M = 255 or 65535, K = the block length
L1  A ← 0, B ← 0
L2  i ← 1; while i ≤ m do
L3      e ← min(i + K − 1, m)
L4      for j ← i to e do                   ▷ no reduction inside a block
L5          A ← A + d[j]
L6          B ← B + A
L7      A ← A mod M                         ▷ i ← e + 1
L8      B ← B mod M
L9  return (A, B)                           ▷ the checksum is B · 2^b + A
```

At the start of a block, $A, B \le M - 1$, and every word is at most $M$. After $k$ words of a block, $A \le (M - 1) + kM$ and $B \le (M - 1) + k(M - 1) + M k(k+1)/2$. This is at most $2^{32} - 1$ for $k \le 5802$ when $M = 255$, and for $k \le 360$ when $M = 65535$. So $K = 5802$ for Fletcher-16 and $K = 360$ for Fletcher-32 keep both sums inside 32 bits. The implementation checks the bound with an assertion and tests it on all-0xFF input, the worst case.

**Check bytes.** The OSI protocols do not send $(A, B)$. They append, or insert, two check bytes chosen so that the receiver's sums are both 0 mod 255. At the end of the message, the bytes $c_0 = 255 - ((A + B) \bmod 255)$ and $c_1 = 255 - ((A + c_0) \bmod 255)$ do this. ISO/IEC 8473 puts the two check octets $X$ and $Y$ inside the header and gives formulas that depend on their position, as RFC 1561 Appendix A reproduces.

## Example

Fletcher-16 of the ASCII string "abcde" (bytes 97, 98, 99, 100, 101), with $M = 255$:

| byte | 97 | 98 | 99 | 100 | 101 |
|---|---|---|---|---|---|
| $A$ | 97 | 195 | 39 | 139 | 240 |
| $B$ | 97 | 37 | 76 | 215 | 200 |

For example, at the third byte $A = (195 + 99) \bmod 255 = 39$ and $B = (37 + 39) \bmod 255 = 76$. The result is $B = 200 = 0xC8$ and $A = 240 = 0xF0$, so the checksum is 0xC8F0. The published test values are 0xC8F0 for "abcde", 0x2057 for "abcdef" and 0x0627 for "abcdefgh". Fletcher-32 with little-endian words gives 0xF04FC729, 0x56502D2A and 0xEBE19591 for the same three strings. The tests check all six, and they check the deferred version against the definition on random inputs.

## Correctness

Inside a block, lines L5 and L6 compute exact integer sums, and the bound above shows that they fit in 32 bits. Reduction modulo $M$ commutes with addition, so reducing only at lines L7 and L8 gives the same residues as reducing after every word. By induction on the words, $B$ is the sum of the prefix sums, which is $\sum (m - i + 1) d_i$. The proof, and the exact rules for the errors that Fletcher misses, are in the correctness file below.

## Complexity

Each word costs two additions, and each block of $K$ words costs two reductions. So the time is $\Theta(n)$, and the extra space is two registers, in each case. Fletcher-16 does one pair of additions per byte; Fletcher-32 does one pair per two bytes, so it is about twice as fast in software. A [CRC](/cyclic-redundancy-check/) needs a table lookup or a carry-less multiply per byte or per block.

## Properties

The exact rules follow from the formulas for $A$ and $B$. Here $M = 255$, and the same rules hold for Fletcher-32 with 65535 and 16-bit words.

- **Single errors.** A change of one byte from $x$ to $y$ is missed if and only if $x - y \equiv 0 \pmod{255}$, that is, $\{x, y\} = \{0x00, 0xFF\}$. The tests check all 255 changes of each of 40 random bytes.
- **Swaps.** Swapping the bytes $x$ at position $i$ and $y$ at position $j > i$ leaves $A$ unchanged and changes $B$ by $(j - i)(x - y)$. So the swap is missed if and only if $255 \mid (j - i)(x - y)$. Adjacent swaps are missed only for the pair 0x00 and 0xFF. Since $255 = 3 \cdot 5 \cdot 17$, a swap at a distance $d$ with $\gcd(d, 255) > 1$, such as 3, 5, 6 or 17, is missed for some other pairs too. For example, at distance 3 it is missed whenever $85 \mid x - y$.
- **Bursts.** A burst of at most 8 bits touches at most two adjacent bytes, and it is missed only if it turns a whole aligned byte from 0x00 into 0xFF or back. So every burst of at most 7 bits is detected.
- **Hamming distance.** Maxino and Koopman give Hamming distance 3 for short messages and 2 beyond a length that grows with the block size: Fletcher-16 has $HD = 2$ from a code word length of 2,056 bits, and Fletcher-32 from 1,048,592 bits (Section 3.4).
- **0x00 and 0xFF.** Data with many 0x00 and 0xFF bytes, which is common, can change between the two without detection. Maxino and Koopman measured this weakness.

## Variants and improvements

- **Modulus 256.** Fletcher's paper also treats two's complement sums mod 256. They are cheaper, but the carries out of the top bit are lost, so errors in the high bits are caught less often. The ones' complement form, mod 255, is the one in use.
- **Adler-32.** [Adler-32](/adler-32/) uses the prime 65521, starts $A$ at 1, and works on bytes with 16-bit sums. It has no 0x00/0xFF blind spot, but its first sum fills its range slowly on short messages, which makes it weak there (RFC 3309). Maxino and Koopman (Section 4.3) compare the two and find no general gain for Adler over Fletcher.
- **Check bytes in the data.** The OSI form, with two check bytes such that both sums are 0, lets a receiver run one loop and test for zero. RFC 1561 Appendix A gives the formulas of ISO/IEC 8473, including an adjustment rule for a changed octet, the analogue of the [incremental update](/incremental-checksum-update/) of the Internet checksum.
- **Fletcher-64.** Two sums mod $2^{32} - 1$ over 32-bit words. It is used in some file systems, but it has no common specification.

## When to use it

Use Fletcher when you need much better detection than a sum, at almost the same cost, and you cannot use a CRC: a small microcontroller without CRC hardware, or a protocol defined around it (OSI CLNP and TP4, IS-IS). Prefer Fletcher-32 to Adler-32 for short messages. Prefer a CRC when the hardware has one, when the data has long runs of 0x00 or 0xFF, or when you need a guaranteed Hamming distance on long messages.

## Pitfalls

- **The names.** "Fletcher-16" is the checksum with two 8-bit sums, a 16-bit result. RFC 1146 calls the same thing the "8-bit Fletcher checksum". Check which one a document means.
- **Byte order of Fletcher-32.** The 16-bit words can be read big-endian or little-endian, and the two give different checksums. The common test vectors are little-endian.
- **Modulus 256 by accident.** Code that uses `uint8_t` sums wraps mod 256, not mod 255. That is a different and weaker checksum.
- **The block bound.** A deferred reduction with blocks that are too long overflows the 32-bit sums. Use at most 5802 bytes per block for Fletcher-16 and 360 words for Fletcher-32.
- **Zero padding.** Appending a zero byte adds $A$ to $B$ (every earlier byte gains weight) and leaves $A$ unchanged. Prepending zero bytes changes nothing. So a lost or extra leading zero byte is missed.

## Implementations

## History

John G. Fletcher, of the Lawrence Livermore Laboratory, published "An Arithmetic Checksum for Serial Transmissions" in the IEEE Transactions on Communications in January 1982. He proposed it as a checksum that software can compute fast and that detects far more errors than a plain sum. The OSI transport protocol (ISO 8073, ITU-T X.224) and the connectionless network protocol (ISO/IEC 8473) adopted it with check octets that make both sums zero. In 1990, RFC 1146 proposed the 8-bit and 16-bit Fletcher checksums as TCP alternate checksum options. Mark Adler derived [Adler-32](/adler-32/) from it for zlib (RFC 1950, 1996). In 2009, Maxino and Koopman measured it against the additive, ones' complement, Adler and CRC checksums on the short messages of embedded networks.

## References
