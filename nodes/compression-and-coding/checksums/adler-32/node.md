---
tag: G06YQ1
kind: algorithm
slug: adler-32
name: Adler-32
aliases:
- Adler checksum
area: compression-and-coding/checksums
level: intro
summary: Fletcher-style checksum with two byte sums modulo the prime 65521, the first started at 1. The check value of zlib (RFC 1950), fast in software but weak on short messages.
model: word-ram
complexity:
  vars: {n: the number of message bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1996
  people: [Mark Adler]
  note: Mark Adler wrote it for the zlib library of Jean-loup Gailly and Mark Adler, and RFC 1950 specified it in May 1996 as the check value of the zlib format.
prereqs: [fletcher-checksum]
see_also: [deflate, cyclic-redundancy-check, crc32c, rolling-checksum, internet-checksum, prime-number, undetected-error-probability, checksum]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc1950
    title: P. Deutsch and J-L. Gailly, RFC 1950, ZLIB Compressed Data Format Specification version 3.3, May 1996
    locator: Section 2.2 (the ADLER32 field and the definition), Section 8.2 (the deferred modulo for 5552 bytes, the prime base, the start value 1) and Section 9 (sample code)
  - url: https://www.rfc-editor.org/rfc/rfc3309
    title: J. Stone, R. Stewart and D. Otis, RFC 3309, Stream Control Transmission Protocol (SCTP) Checksum Change, September 2002
    locator: Section 1 (the weakness of Adler-32 on short packets and the move to CRC32c)
  - paper: doi:10.1109/TDSC.2007.70216
    title: Theresa C. Maxino and Philip J. Koopman, The effectiveness of checksums for embedded control networks, IEEE Transactions on Dependable and Secure Computing 6(1), 2009, pages 59 to 72
    locator: Section 3.5 (the Adler checksum) and Section 4.3 (Adler compared with Fletcher)
  - paper: doi:10.1109/TCOM.1982.1095369
    title: John G. Fletcher, An Arithmetic Checksum for Serial Transmissions, IEEE Transactions on Communications COM-30(1), January 1982, pages 247 to 252
    locator: The two running sums that Adler-32 extends
---

Adler-32 is the checksum of the zlib format (RFC 1950). It is the [Fletcher checksum](/fletcher-checksum/) with three changes: it adds bytes, not 16-bit words; both sums are taken modulo 65521, the largest prime below $2^{16}$, in place of 65535; and the first sum starts at 1, not 0. For each byte $d$ it does $s_1 \leftarrow s_1 + d$ and $s_2 \leftarrow s_2 + s_1$, and the result is $s_2 \cdot 65536 + s_1$. The prime modulus removes Fletcher's blind spot for 0x00 against 0xFF and catches every error confined to two bytes. Mark Adler designed it to be much faster than a [CRC](/cyclic-redundancy-check/) in software. Its weakness is on short messages: there $s_1$ cannot reach most of its 16-bit range, which is why SCTP moved from Adler-32 to [CRC32C](/crc32c/).

## In plain words

Keep two counters. Start the first at 1 and the second at 0. For each byte, add the byte to the first counter, then add the first counter to the second. When a counter reaches 65521, it wraps around to 0. The answer is the two counters side by side, the second one in the high half.

The first counter is the sum of the bytes. The second counter counts each byte once for every step after it arrives, so it also sees where each byte is. Because 65521 is prime, no change of one byte, or of two bytes that are close together, can hide in both counters at once. But a short message has a small byte sum, so the first counter stays small and much of the 32-bit value is wasted.

## The problem

The input is a message of $n$ bytes $d_1, \ldots, d_n$. With $P = 65521$, the output is the 32-bit value $s_2 \cdot 2^{16} + s_1$, where

$$s_1 = \Big(1 + \sum_{i=1}^{n} d_i\Big) \bmod P, \qquad s_2 = \Big(n + \sum_{i=1}^{n} (n - i + 1)\, d_i\Big) \bmod P.$$

The second form follows from $s_2 = \sum_t s_1^{(t)}$, the sum of the values of $s_1$ after each byte, as for Fletcher. The term $n$ comes from the start value 1, which is added $n$ times. So, as RFC 1950 Section 8.2 says, for three bytes $a, b, c$ the second sum is $3a + 2b + c + 3$. The input may also be a running value from an earlier call, so a stream can be checked in pieces. We count word operations in the [word RAM](/word-ram/) with 32-bit registers.

## The algorithm

Like zlib, the code defers the reduction. It adds up to $N_{\max} = 5552$ bytes into 32-bit sums, then reduces both modulo $P$.

```pseudo id=main
ADLER32(d[1 .. n], v)                       ▷ v = 1 for a new message
L1  s1 ← v mod 2^16                          ▷ the low half of the running value
L2  s2 ← ⌊v / 2^16⌋
L3  i ← 1; while i ≤ n do
L4      e ← min(i + NMAX − 1, n)            ▷ NMAX = 5552
L5      for j ← i to e do                   ▷ no reduction inside a block
L6          s1 ← s1 + d[j]
L7          s2 ← s2 + s1
L8      s1 ← s1 mod 65521                   ▷ i ← e + 1
L9      s2 ← s2 mod 65521
L10 return s2 · 2^16 + s1
```

The bound comes from the worst case, all bytes 0xFF with $s_1 = s_2 = P - 1$ at the start of a block. After $k$ bytes, $s_2 \le 255 k(k+1)/2 + (k + 1)(P - 1)$. This is at most $2^{32} - 1$ for $k \le 5552$ and above it for $k = 5553$, which is the value of NMAX in zlib and in RFC 1950 Section 8.2.

**Combine.** If $B$ has length $\ell$, the checksum of the concatenation $AB$ follows from the checksums of the parts: $s_1(AB) = s_1(A) + s_1(B) - 1$ and $s_2(AB) = s_2(A) + s_2(B) + \ell\,(s_1(A) - 1)$, modulo $P$. The reason is that the run over $B$ starts from $s_1(A)$ in place of 1, and each of its $\ell$ steps adds the extra $s_1(A) - 1$ to $s_2$. This is zlib's `adler32_combine`, and it lets parts of a file be checked in parallel.

## Example

Adler-32 of the ASCII string "Wikipedia":

| byte | W | i | k | i | p | e | d | i | a |
|---|---|---|---|---|---|---|---|---|---|
| value | 87 | 105 | 107 | 105 | 112 | 101 | 100 | 105 | 97 |
| $s_1$ | 88 | 193 | 300 | 405 | 517 | 618 | 718 | 823 | 920 |
| $s_2$ | 88 | 281 | 581 | 986 | 1503 | 2121 | 2839 | 3662 | 4582 |

No sum reaches 65521, so no reduction happens. The result is $4582 \cdot 65536 + 920$ = 0x11E6 · 0x10000 + 0x0398 = 0x11E60398. The empty message gives 0x00000001. The tests check these values, check the trace row by row, and compare the implementation with Python's `zlib.adler32` on 600 random messages, on 10,000 bytes of 0xFF, with running values, and with combine.

## Correctness

Lines L6 and L7 apply the definition without reduction. Reduction modulo $P$ commutes with addition, so reducing only at lines L8 and L9 gives the same residues, and the bound above shows that the 32-bit sums never overflow. The proof, the combine rule and the exact detection results are in the correctness file below.

## Complexity

Each byte costs two additions, and each block of 5552 bytes costs two reductions, so the time is $\Theta(n)$ and the extra space is two registers. Combine takes $O(1)$ time. In software Adler-32 is faster than a table-driven CRC-32, which needs a table lookup and a shift per byte. Hardware CRC instructions, such as those for [CRC32C](/crc32c/), remove most of that difference.

## Properties

Let $P = 65521$. An error changes byte $i$ by $\delta_i$, with $|\delta_i| \le 255$, and keeps the length. It is missed if and only if $\sum \delta_i \equiv 0$ and $\sum (n - i + 1) \delta_i \equiv 0 \pmod P$.

- **One or two bytes.** Every error confined to one byte, or to two bytes less than $P$ apart, is detected. For one byte, $0 < |\delta_i| < P$. For two bytes $i < j$, the two conditions give $(j - i)\delta_i \equiv 0$, and since $P$ is prime and $0 < j - i < P$, $\delta_i \equiv 0$, so $\delta_i = 0$. This is the gain over Fletcher, whose modulus $255 = 3 \cdot 5 \cdot 17$ misses 0x00 against 0xFF. The tests check every change 0x00 to 0xFF on a random message made of these two bytes.
- **Swaps.** A swap of two different bytes less than $P$ apart is an error in two bytes, so it is detected.
- **Short messages.** For $n$ bytes, $s_1 \le 1 + 255 n$. For $n \le 128$ this is below $2^{15}$, so the top bit of $s_1$ is always 0. Over all two-byte messages, $s_1$ takes only 511 values. So a short message uses only a small part of the $2^{32}$ check values, and random corruption of a short message is missed far more often than $2^{-32}$. RFC 3309 gives this as the reason to replace Adler-32 in SCTP, whose packets are often short.
- **Unused values.** The values 65521 to 65535 never appear in either half, so 15 values of each half are unused.
- **Zero bytes.** Unlike Fletcher, the start value 1 makes $s_2$ depend on the length (RFC 1950 Section 8.2). Adding $k$ zero bytes at the start adds $k$ to $s_2$, and adding them at the end adds $k\,s_1$, so either change is detected unless that amount is a multiple of 65521.

## Variants and improvements

- **Fletcher-32.** The [Fletcher checksum](/fletcher-checksum/) on 16-bit words with modulus 65535. It takes half as many steps per byte and uses the whole 16-bit range of each half, but it misses 0x0000 against 0xFFFF. Maxino and Koopman (Section 4.3) compare the two and find no general gain for Adler.
- **CRC-32 and CRC32C.** A [CRC](/cyclic-redundancy-check/) guarantees a Hamming distance on short messages and detects every burst up to its width. The gzip format uses CRC-32, and SCTP replaced Adler-32 by [CRC32C](/crc32c/) in RFC 3309.
- **The rsync weak checksum.** The [rolling checksum](/rolling-checksum/) of rsync is the same pair of sums with modulus $2^{16}$ and start value 0, chosen because it can slide over the data one byte at a time.
- **Vectorized code.** The block loop can run in SIMD registers with several partial sums, which modern zlib forks use. The result is the same.

## When to use it

Use Adler-32 when you write or read the zlib format, which requires it, or when you need a fast check on long blocks of data and a CRC is not available. Do not use it for short messages, as in packet protocols, or where the error model needs a guaranteed Hamming distance; use a CRC there. It is not a [cryptographic hash](/cryptographic-hash-function/): anyone can change data and keep the same Adler-32.

## Pitfalls

- **The start value.** $s_1$ starts at 1. Starting at 0 gives a different checksum, the empty message then gives 0, and the length no longer enters $s_2$.
- **The modulus.** The modulus is 65521, not 65536 or 65535. Code that lets 16-bit sums wrap computes a different and weaker checksum.
- **Byte order in zlib.** The zlib stream stores the checksum after the compressed data, most significant byte first (RFC 1950 Section 2.2).
- **Overflow.** A deferred reduction with blocks longer than 5552 bytes can overflow 32-bit sums. With 64-bit sums the block can be much longer.
- **Combine needs the length.** `adler32_combine` needs the length of the second part, reduced modulo 65521. Passing the wrong length gives a wrong result without any error.

## Implementations

## History

Mark Adler wrote the checksum for zlib, the compression library of Jean-loup Gailly and Mark Adler, as a faster replacement for the CRC-32 of gzip. RFC 1950 (May 1996), by L. Peter Deutsch and Jean-loup Gailly, specified it as "a 32-bit extension and improvement of the Fletcher algorithm, used in the ITU-T X.224 / ISO 8073 standard". The zlib format and so Adler-32 are used in PNG and in many other file formats. In 2000, SCTP (RFC 2960) adopted Adler-32 as its checksum. In 2002, RFC 3309 replaced it by CRC32C because Adler-32 is weak on the short packets that SCTP often sends.

## References
