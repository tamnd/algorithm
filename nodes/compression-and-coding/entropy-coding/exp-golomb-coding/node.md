---
tag: GFRAJT
kind: algorithm
slug: exp-golomb-coding
name: Exp-Golomb coding
aliases:
- Exponential-Golomb coding
- exp-Golomb code
- ue(v)
area: compression-and-coding/entropy-coding
level: advanced
summary: "A prefix code with order k: write y = x + 2^k in binary after floor(log2 y) - k zeros. Order 0 is the ue(v) code of H.264 and HEVC; order k suits values near 2^k."
model: word-ram
complexity:
  vars: {x: the integer to code, k: the order}
  time: {worst: Θ(log(x + 1) + k), average: Θ(log(x + 1) + k), best: Θ(1 + k)}
  space: {extra: Θ(1)}
properties: {deterministic: true, online: true, recursive: false}
history:
  year: 1978
  people: [Jukka Teuhola]
  note: Teuhola coded run lengths in clustered bit vectors with buckets that double in size, a Golomb code with exponential steps.
prereqs: [elias-gamma-coding, rice-coding]
see_also: [golomb-coding, unary-coding, elias-delta-coding, universal-code, cabac, leading-zero-count, variable-byte-encoding, prefix-code]
sources:
  - paper: doi:10.1016/0020-0190(78)90024-8
    title: Jukka Teuhola, A compression method for clustered bit-vectors, Information Processing Letters 7(6), 1978
    locator: pp. 308 to 311 (the code with bucket sizes that double)
  - url: https://www.itu.int/rec/T-REC-H.264
    title: ITU-T Recommendation H.264, Advanced video coding for generic audiovisual services, edition 11/2007
    locator: Section 9.1 and Table 9-2 (ue(v)), Section 9.1.1 and Table 9-3 (se(v)), Section 9.3.2.3 (UEGk binarization)
  - url: https://www.itu.int/rec/T-REC-H.265
    title: ITU-T Recommendation H.265, High efficiency video coding
    locator: Section 9.2 (parsing process for Exp-Golomb codes)
  - paper: doi:10.1145/3415148
    title: Giulio Ermanno Pibiri and Rossano Venturini, Techniques for inverted index compression, ACM Computing Surveys 53(6), Article 125, 2020
    locator: Section 2.6, Exponential Golomb, and Table 3 (arXiv:1908.10598v2)
---

Exp-Golomb coding of order $k$ is a [prefix code](/prefix-code/) for the integers $x \ge 0$. Let $y = x + 2^k$ and $n = \lfloor \log y \rfloor$. The codeword is $n - k$ zero bits followed by the $n + 1$ binary digits of $y$. Order 0 is the [Elias gamma code](/elias-gamma-coding/) of $x + 1$, and it is the `ue(v)` code that H.264 and HEVC use for most header fields. Order $k$ is the gamma code of $\lfloor x / 2^k \rfloor + 1$ followed by the $k$ low bits of $x$: a [Rice code](/rice-coding/) whose quotient is in gamma instead of [unary](/unary-coding/), so values near $2^k$ are cheap and a large value costs $O(\log x)$ bits, not $O(x)$. Jukka Teuhola described the code in 1978.

## In plain words

Put the numbers into buckets. The first bucket holds the $2^k$ smallest numbers, and each next bucket is twice as big as the one before. To send a number, say which bucket it is in, then say where it sits inside that bucket.

The bucket number goes as a run of zeros. The position inside the bucket goes as a plain binary number, and a bigger bucket needs one more digit. A neat trick joins the two parts: add $2^k$ to the number and write the result in binary. Its length tells the bucket, so the encoder only has to put in front of it as many zeros as the bucket number.

The order $k$ sets the size of the first bucket. A small $k$ suits data that is mostly tiny. A large $k$ suits data that is often near $2^k$.

## The problem

The input is a sequence of non-negative integers whose law is not known in advance, typically small field values, motion vector differences or transform levels, with many small values and a tail that can be long. The task is a prefix code with no table, one small parameter, and a length that grows like $2 \log x$ for large $x$, so that an outlier is never a disaster.

Notation: $x$ is the integer to code, $k \ge 0$ is the order, $y = x + 2^k$, $n = \lfloor \log y \rfloor$, and $\ell(x)$ is the codeword length in bits. Logarithms are base 2. This page writes the unary prefix as zeros ended by a one, as H.264 Section 9.1 does. The CABAC binarization of H.264 Section 9.3.2.3 and the survey of Pibiri and Venturini write ones ended by a zero; the lengths are the same.

## The algorithm

```pseudo id=main
EXPGOLOMB-ENCODE(x, k, W)                  ▷ x ≥ 0, k ≥ 0, W is a bit writer
L1  y ← x + 2^k
L2  n ← ⌊log y⌋                            ▷ the index of the top one bit of y
L3  write n − k zero bits to W
L4  write the n + 1 bits of y to W, most significant first

EXPGOLOMB-DECODE(k, R)                     ▷ R is a bit reader
L5  z ← the number of zero bits before the first one bit; read them and the one
L6  y ← 1                                  ▷ the one bit just read is the top bit of y
L7  repeat z + k times: y ← 2y + READ-BIT(R)
L8  return y − 2^k
```

Line L1 moves $x$ into the range $[2^k, \infty)$, so $y$ has at least $k + 1$ binary digits and $n \ge k$. Line L3 writes the bucket index $n - k$ in unary, without its end marker. The end marker is the top bit of $y$, written first by line L4. So the decoder counts zeros in line L5, and the one that stops the count is already the top bit of $y$. Line L7 reads the $n = z + k$ bits of $y$ below the top bit, and line L8 removes the offset.

**Length.** $\ell(x) = (n - k) + (n + 1) = 2\lfloor \log(x + 2^k) \rfloor - k + 1$. The $2^k$ values $0, \ldots, 2^k - 1$ take $k + 1$ bits, the next $2^{k+1}$ take $k + 3$ bits, the next $2^{k+2}$ take $k + 5$ bits, and so on.

**Signed values.** H.264 maps a signed value $v$ to a code number $c$ and sends $c$ with order 0 (`se(v)`, Section 9.1.1, Table 9-3):

$$c = \begin{cases} 2v - 1 & v > 0 \\ -2v & v \le 0 \end{cases} \qquad v = (-1)^{c+1} \lceil c/2 \rceil.$$

So $0, 1, -1, 2, -2, 3, -3$ get the code numbers $0, 1, \ldots, 6$. A positive value gets an odd code number.

**Order $k$ in CABAC.** The binarization UEGk of H.264 Section 9.3.2.3 sends a truncated unary prefix, then, for the part above the cutoff, an order-$k$ exp-Golomb suffix with ones ended by a zero. Motion vector differences use $k = 3$ and coefficient levels use $k = 0$ (Table 9-24). The suffix is the same code as lines L1 to L4 with the bit values of the unary part swapped. In the standard it is written as a loop: while the value is at least $2^k$, write a one, subtract $2^k$ and add 1 to $k$; then write a zero and the $k$ low bits.

## Example

Order 0, the H.264 `ue(v)` code (Table 9-2):

| $x$ | $y = x + 1$ | $n$ | zeros | codeword | $\ell(x)$ |
|---|---|---|---|---|---|
| 0 | 1 | 0 | | 1 | 1 |
| 1 | 10 | 1 | 0 | 010 | 3 |
| 2 | 11 | 1 | 0 | 011 | 3 |
| 3 | 100 | 2 | 00 | 00100 | 5 |
| 6 | 111 | 2 | 00 | 00111 | 5 |
| 7 | 1000 | 3 | 000 | 0001000 | 7 |
| 9 | 1010 | 3 | 000 | 0001010 | 7 |

Order 2. Here $y = x + 4$ and the first bucket holds 0 to 3:

| $x$ | $y$ | $n$ | zeros ($n - 2$) | codeword | $\ell(x)$ |
|---|---|---|---|---|---|
| 0 | 100 | 2 | | 100 | 3 |
| 3 | 111 | 2 | | 111 | 3 |
| 4 | 1000 | 3 | 0 | 01000 | 5 |
| 9 | 1101 | 3 | 0 | 01101 | 5 |
| 11 | 1111 | 3 | 0 | 01111 | 5 |
| 12 | 10000 | 4 | 00 | 0010000 | 7 |
| 28 | 100000 | 5 | 000 | 000100000 | 9 |

Decode `01101` with $k = 2$:

| step | bits read | $z$ | $y$ | result |
|---|---|---|---|---|
| L5 | `0`, `1` | 1 | | |
| L6 | | 1 | 1 | |
| L7 | `1`, `0`, `1` ($z + k = 3$ bits) | 1 | 1101 = 13 | |
| L8 | | | | $13 - 4 = 9$ |

The same value with order 0 is `0001010`, two bits longer. The value 1000 takes 19 bits with order 0 and 17 bits with order 2. A [Rice code](/rice-coding/) with $k = 2$ would take 253 bits for it.

## Correctness

The invariant of the decoder is: after line L7 has read $j$ bits, $y$ holds the top $j + 1$ binary digits of the encoder's $y$. Line L5 returns $z = n - k$, because line L3 wrote exactly $n - k$ zeros and the next bit, the top bit of $y$, is a one. Line L6 sets $y$ to that top bit. Line L7 then reads the remaining $z + k = n$ digits, so after it $y$ is the encoder's $y$, and line L8 returns $y - 2^k = x$. The code is prefix-free: two codewords with different zero counts differ at the first one bit of the shorter one, and two codewords with the same zero count $z$ have the same length $2z + k + 1$, so neither is a proper prefix of the other. The full proof is in the proof file.

## Complexity

**Length.** $\ell(x) = 2\lfloor \log(x + 2^k) \rfloor - k + 1$. For $k = 0$ this is $2\lfloor \log(x + 1) \rfloor + 1$, the gamma length of $x + 1$. For $x \ge 2^k$ it lies between $2 \log x - k - 1$ and $2 \log x - k + 3$.

**Time.** Encoding and decoding take $\Theta(n - k + n + 1) = \Theta(\log(x + 1) + k)$ bit steps. On a [word RAM](/word-ram/) where the codeword fits in a word, line L2 is one [leading-zero count](/leading-zero-count/) and the encoder writes the codeword with one shift; the decoder finds $z$ with one leading-zero count on the next word of the stream and reads $y$ with one shift and mask. Both are $O(1)$ word operations.

**Space.** $\Theta(1)$ words beyond the input and output.

## Properties

- **Prefix-free and complete.** The bucket $j \ge 0$ holds $2^{j+k}$ codewords of length $2j + k + 1$, so the [Kraft sum](/kraft-inequality/) is $\sum_{j \ge 0} 2^{j+k} 2^{-(2j+k+1)} = \sum_{j \ge 0} 2^{-(j+1)} = 1$.
- **Universal, not asymptotically optimal.** For each fixed $k$, $\ell(x) = 2 \log x + O(k)$. This is within a constant factor of the best length on any decreasing law, so the code is a [universal code](/universal-code/), but the factor tends to 2, not 1. The [Elias delta code](/elias-delta-coding/) has length $\log x + O(\log \log x)$.
- **Implied law.** The code is optimal for $P(x) = 2^{-\ell(x)}$, which is flat inside each bucket and halves from bucket to bucket. For $k = 0$ this is about $1/(2(x + 1)^2)$, a power law with exponent 2.
- **Byte-unaligned and serial.** Each codeword is a variable number of bits, and its length is known only after the zeros are read.

## Variants and improvements

- **Order 0 and Elias gamma.** The order-0 codeword of $x$ is the [Elias gamma](/elias-gamma-coding/) codeword of $x + 1$, so order 0 is the gamma code shifted to start at 0.
- **Order $k$ as Rice with a gamma quotient.** The order-$k$ codeword of $x$ is the gamma codeword of $\lfloor x / 2^k \rfloor + 1$ followed by the $k$ low bits of $x$. Replace the gamma part by unary and the result is the [Rice code](/rice-coding/) with parameter $k$.
- **Truncated unary plus exp-Golomb (UEGk).** H.264 CABAC and HEVC put a short truncated unary or Rice prefix in front, coded with adaptive contexts by [CABAC](/cabac/), and use an exp-Golomb suffix only for large values, which bounds the number of context-coded bins.
- **Mapped signed values.** `se(v)` maps signed values to the code numbers $0, 1, 2, \ldots$ in the order $0, 1, -1, 2, -2, \ldots$. H.264 also has `me(v)`, which maps a code number through a table, and `te(v)`, a truncated form for a field whose range is known.
- **Longer prefixes per step.** The zeta codes of Boldi and Vigna (Pibiri and Venturini, Section 2.7) grow each bucket by a factor $2^h$ instead of 2, which shortens the codes of power laws with an exponent near 1.

## When to use it

Use order 0 for header fields and small counts whose law is unknown but mostly small, as video standards do for `ue(v)` and `se(v)`. Use order $k$ when the values cluster near $2^k$ but have a long tail: CABAC suffixes, gaps in posting lists, residuals with outliers. If the law is close to geometric with a known mean, the [Rice code](/rice-coding/) or the [Golomb code](/golomb-coding/) is shorter. If many values are very large, the [Elias delta code](/elias-delta-coding/) is shorter. If speed matters more than size, a byte-aligned code such as [variable-byte encoding](/variable-byte-encoding/) decodes faster.

## Pitfalls

- **Zero count of $n$ instead of $n - k$.** If line L3 writes $n$ zeros, as for order 0, the code with $k > 0$ is $k$ bits too long and the decoder of line L7 reads the wrong number of bits. The right line is "write $n - k$ zero bits".
- **Reading $z$ bits instead of $z + k$.** For $k > 0$, line L7 must read $z + k$ bits after the first one, not $z$. With $z$ bits the decoder drops the $k$ low bits and loses its place in the stream.
- **Unary convention.** H.264 Section 9.1 writes zeros ended by a one; its CABAC suffix in Section 9.3.2.3 writes ones ended by a zero. A decoder whose line L5 counts the wrong bit value desynchronizes.
- **Signed mapping.** In `se(v)`, a positive value gets the odd code number $2v - 1$ and a non-positive value the even code number $-2v$. Swapping the two gives a valid but incompatible code. In 32-bit arithmetic, $2v - 1$ overflows for $v \ge 2^{30}$; compute it in a wider type.
- **Unbounded zero runs.** A corrupt or hostile stream can hold a long run of zeros. Line L5 must stop at a bound set by the format, or a later shift overflows. A 32-bit code number has at most 31 leading zeros.

## Implementations

## History

Jukka Teuhola described the code in 1978, in a method to compress clustered bit vectors by coding the lengths of zero runs. His code splits the integers into buckets whose sizes double, sends the bucket index in unary and the offset inside it in binary: a [Golomb code](/golomb-coding/) whose bucket size grows exponentially, from which the name comes. The ITU-T and ISO/IEC joint video team adopted order 0 for the syntax elements of H.264 (2003), as `ue(v)` and `se(v)`, and used order-$k$ suffixes in the CABAC binarization. HEVC (H.265, 2013) and later video standards keep both uses.

## References
