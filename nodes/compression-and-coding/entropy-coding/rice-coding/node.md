---
tag: 3VFKPT
kind: algorithm
slug: rice-coding
name: Rice coding
aliases:
- Golomb-Rice code
- Rice code
area: compression-and-coding/entropy-coding
level: intro
summary: Golomb coding with m = 2^k. The quotient x >> k goes in unary and the k low bits follow as they are. Used for residuals in FLAC and JPEG-LS, with k chosen from the mean.
model: word-ram
complexity:
  vars: {x: the integer to code, k: the Rice parameter}
  time: {worst: Θ(x/2^k + k), average: Θ(1 + k), best: Θ(1 + k)}
  space: {extra: Θ(1)}
properties: {deterministic: true, online: true, recursive: false}
history:
  year: 1979
  people: [Robert F. Rice]
  note: Rice described adaptive coders for space data that choose among codes of this form, block by block.
prereqs: [golomb-coding]
see_also: [unary-coding, exp-golomb-coding, elias-gamma-coding, geometric-distribution, run-length-encoding, delta-encoding, huffman-coding, variable-byte-encoding]
sources:
  - url: https://ntrs.nasa.gov/citations/19790014634
    title: Robert F. Rice, Some practical universal noiseless coding techniques, JPL Publication 79-22, Jet Propulsion Laboratory, March 1979
    locator: the split-sample options, which send the low bits of each sample as they are and the high part in unary
  - url: https://www.rfc-editor.org/rfc/rfc9639
    title: M.Q.C. van Beurden and A. Weaver, RFC 9639, Free Lossless Audio Codec (FLAC), December 2024
    locator: Section 9.2.7, Coded Residual, and Section 9.2.7.2, Rice Code
  - paper: doi:10.1109/83.855427
    title: Marcelo J. Weinberger, Gadiel Seroussi and Guillermo Sapiro, The LOCO-I lossless image compression algorithm, principles and standardization into JPEG-LS, IEEE Transactions on Image Processing 9(8), 2000
    locator: pp. 1309 to 1324 (Golomb codes with m = 2^k and the adaptive choice of k)
  - url: https://www.itu.int/rec/T-REC-T.87
    title: ITU-T Recommendation T.87, Lossless and near-lossless compression of continuous-tone still images (JPEG-LS)
    locator: the computation of the Golomb coding variable k from the context counters A and N
  - url: https://ipnpr.jpl.nasa.gov/progress_report/42-159/159E.pdf
    title: Aaron Kiely, Selecting the Golomb parameter in Rice coding, IPN Progress Report 42-159, Jet Propulsion Laboratory, 2004
    locator: the best Rice parameter for a geometric source and its estimate from the sample mean
  - paper: doi:10.1145/3415148
    title: Giulio Ermanno Pibiri and Rossano Venturini, Techniques for inverted index compression, ACM Computing Surveys 53(6), Article 125, 2020
    locator: Section 2.5, Rice (arXiv:1908.10598v2)
---

Rice coding is [Golomb coding](/golomb-coding/) with a parameter that is a power of two, $m = 2^k$. The codeword of $x \ge 0$ is the quotient $x \gg k$ in [unary](/unary-coding/), followed by the $k$ low bits of $x$ as they are. The division becomes a shift, the remainder becomes a fixed-width field, and the decoder needs no truncated binary step. On a geometric source, the best Rice code is at most about 0.09 bits per value longer than the best Golomb code. FLAC codes its audio residuals this way, and JPEG-LS codes its image residuals this way with a context-adaptive $k$. Robert Rice described the scheme in 1979 for space data.

## In plain words

Split each number into a high part and a low part. The low part is its last $k$ binary digits. The high part is what is left, the number divided by $2^k$.

Most numbers from a well-tuned source are small, so the high part is usually 0, 1 or 2. Send it as a count: that many zeros, then a one. Then send the $k$ low digits unchanged.

The choice of $k$ sets the trade. With a small $k$ the low part is cheap, but large numbers give long runs of zeros. With a large $k$ every number pays for $k$ low digits. The best $k$ is about the binary logarithm of half the average value.

## The problem

The input is a sequence of non-negative integers, typically prediction residuals after a fold to non-negative values, with a roughly geometric law $P(x) = (1-\theta)\theta^x$ on a memoryless source. The task is a prefix code that is close to optimal and very cheap to encode and decode, with one small integer parameter that an encoder can choose per block or per context.

Notation: $x$ is one integer to code, $k \ge 0$ is the Rice parameter, $q = \lfloor x / 2^k \rfloor$ is the quotient, $\mu$ is the mean of the source, and $\ell(x)$ is the codeword length in bits. Logarithms are base 2. This page writes unary as zeros ended by a one, as FLAC does; the [Golomb coding](/golomb-coding/) page uses ones ended by a zero. The lengths are the same.

## The algorithm

```pseudo id=main
RICE-ENCODE(x, k, W)                       ▷ x ≥ 0, k ≥ 0, W is a bit writer
L1  q ← x >> k                             ▷ q = ⌊x / 2^k⌋
L2  write q zero bits to W, then one 1 bit
L3  write the k low bits of x to W, most significant first

RICE-DECODE(k, R)                          ▷ R is a bit reader
L4  q ← 0; while READ-BIT(R) = 0 do q ← q + 1
L5  r ← the next k bits of R, read as a binary number
L6  return (q << k) + r
```

Line L1 is a shift and line L3 writes $x \bmod 2^k$, so no division and no comparison is needed. With $k = 0$ the code is plain unary.

**Choosing $k$.** For $P(x) = (1-\theta)\theta^x$ the expected length is

$$L(k) = k + 1 + \frac{t}{1 - t}, \qquad t = \theta^{2^k},$$

since the quotient is geometric with ratio $t$. Then $L(k+1) - L(k) = 1 - t/(1 - t^2)$, which is negative exactly when $t^2 + t - 1 > 0$. So $L$ falls while $\theta^{2^k} > (\sqrt 5 - 1)/2$, and the best parameter is the smallest $k \ge 0$ with $\theta^{2^k} \le (\sqrt 5 - 1)/2$:

$$k^* = \max\left(0, \left\lceil \log_2 \frac{\ln((\sqrt 5 - 1)/2)}{\ln \theta} \right\rceil\right).$$

With $\theta = \mu/(1 + \mu)$ this depends only on the mean, and for large $\mu$ it is about $\log_2(0.48\,\mu)$. Practical coders use simpler rules of the same form:

- **JPEG-LS** (ITU-T T.87, from LOCO-I) keeps, per context, the count $N$ of residuals and the sum $A$ of their absolute values, and takes the smallest $k$ with $N \cdot 2^k \ge A$. The folded value is about twice the absolute residual, so this is close to $2^k \approx \mu/2$.
- **FLAC** (RFC 9639, Section 9.2.7) stores one Rice parameter per partition of the residual, in 4 or 5 bits, and an all-ones parameter as an escape to plain binary. The encoder chooses the parameter per partition, from an estimate or a search.

**Signed residuals.** FLAC folds a residual $v$ to $2v$ if $v \ge 0$ and to $-2v - 1$ if $v < 0$, so $0, -1, 1, -2, 2$ become $0, 1, 2, 3, 4$, before the Rice code.

## Example

Take $k = 2$. Encode $x = 9$: line L1 gives $q = 2$, line L2 writes `001`, and line L3 writes the low bits `01`. The codeword is `001 01`.

| $x$ | $q$ | low bits | codeword | $\ell(x)$ |
|---|---|---|---|---|
| 0 | 0 | 00 | 1 00 | 3 |
| 3 | 0 | 11 | 1 11 | 3 |
| 4 | 1 | 00 | 01 00 | 4 |
| 9 | 2 | 01 | 001 01 | 5 |
| 15 | 3 | 11 | 0001 11 | 6 |

Decode `00101`:

| step | bits read | $q$ | $r$ | result |
|---|---|---|---|---|
| L4 | `0`, `0`, `1` | 2 | | |
| L5 | `01` | 2 | 1 | |
| L6 | | | | $2 \cdot 4 + 1 = 9$ |

The example of RFC 9639, Section 9.2.7.2: with parameter 3, the folded residual 38 has $q = 4$ and low bits $6$, so its codeword is `00001` `110`, which is the byte `0b00001110`. The residual before folding was 19.

## Correctness

Line L4 reads the $q$ zeros and the one of line L2 and returns $q$. Line L5 reads the $k$ bits of line L3, which are $x \bmod 2^k$. Line L6 returns $q \cdot 2^k + (x \bmod 2^k) = x$. The codeword set is prefix-free: two codewords with different quotients differ at the position of the first one bit of the shorter unary part, and two codewords with the same quotient have the same length. This is the Golomb code with $m = 2^k$, where truncated binary has $u = m$ and writes every remainder in $k$ bits, so the proof on the [Golomb coding](/golomb-coding/) page applies. The full proof is in the proof file.

## Complexity

**Length.** $\ell(x) = \lfloor x/2^k \rfloor + 1 + k$.

**Time.** Encoding and decoding take $\Theta(q + k) = \Theta(x/2^k + k)$ bit steps. With the best $k$ on a geometric source, the quotient has mean $t/(1-t) \le (\sqrt 5 + 1)/2$, so the expected time is $\Theta(1 + k)$. On a [word RAM](/word-ram/), the encoder builds the whole codeword with a shift and an OR when it fits in a word, and the decoder finds the end of the unary part with one count-leading-zeros instruction, so a codeword of at most $w$ bits takes $O(1)$ steps.

**Loss against Golomb.** With the best parameter of each code on a geometric source, the Rice code is longer than the [Golomb code](/golomb-coding/) by at most about 0.09 bits per value. The two are equal when the best Golomb $m$ is a power of two, and for $\theta \le (\sqrt 5 - 1)/2$, where both are unary.

| $\theta$ | best $k$ | Rice (bits) | best Golomb (bits) |
|---|---|---|---|
| 0.5 | 0 | 2.000 | 2.000 |
| 0.8 | 2 | 3.694 | 3.639 |
| 0.9 | 3 | 4.756 | 4.725 |

## Properties

- **Prefix-free and complete.** Unary and a fixed $k$-bit field both have Kraft sum 1.
- **One small parameter.** The parameter fits in 4 or 5 bits, so a coder can change it per block at a small cost.
- **Shift-and-mask arithmetic.** No division, no table, and no data-dependent branch in the remainder.
- **Outliers cost a lot.** A value of $x$ takes $x/2^k$ unary bits. FLAC handles outliers with an escape per partition; JPEG-LS caps the unary part.

## Variants and improvements

- **Golomb coding.** [Golomb coding](/golomb-coding/) allows any $m$, which saves up to about 0.09 bits per value at the cost of a division and a truncated binary step.
- **Exp-Golomb coding.** [Exp-Golomb coding](/exp-golomb-coding/) of order $k$ also has a $k$-bit low part, but doubles the bucket size at each step, so large values cost $O(\log x)$ bits instead of $O(x)$.
- **Adaptive parameter.** JPEG-LS updates $A$ and $N$ after each residual and halves both at a set count, so $k$ follows the local statistics without side information.
- **Partitioned parameter.** FLAC splits each residual block into $2^p$ partitions, with the partition order $p$ in 4 bits, and stores one parameter per partition.

## When to use it

Use the Rice code for prediction residuals and gaps with a roughly geometric law when speed and simplicity matter: lossless audio (FLAC), lossless images (JPEG-LS), space instrument data, and Golomb-coded sets such as the compact block filters of Bitcoin's BIP 158. If the law has a heavy tail, use [exp-Golomb](/exp-golomb-coding/) or the [Elias gamma code](/elias-gamma-coding/). If every fraction of a bit matters and a division is cheap, use the best Golomb code. If the alphabet is small, an adaptive arithmetic coder gives a shorter output.

## Pitfalls

- **Unary convention.** Line L2 writes zeros ended by a one in FLAC; the Golomb page and some libraries write ones ended by a zero. A decoder whose line L4 loops on the wrong bit value reads garbage from the first value on.
- **Choosing $k$ from the mean of the signed residuals.** The rule must use the mean of the folded values (or the mean of the absolute residuals, as JPEG-LS does with $A$). The signed mean is near zero, gives $k = 0$, and turns every value into a long unary run.
- **The k rule off by a factor of two.** The best $2^k$ is about half the mean of the folded values, not the mean. A rule $2^k \ge \mu$ on folded values often picks $k^* + 1$, and sometimes $k^* + 2$.
- **Folding with a logical shift.** The fold runs before line L1. In 64-bit code, `(v << 1) ^ (v >> 63)` gives the fold only if `v >> 63` is an arithmetic shift, which gives 0 or all ones. With a logical shift it gives 0 or 1, and every negative residual gets a wrong value.
- **Escapes.** In FLAC, the parameter value with all bits set is not a Rice parameter but an escape to plain binary. A decoder that treats it as $k = 15$ or $k = 31$ desynchronizes.

## Implementations

## History

Robert Rice described in 1979 a family of adaptive coders for space data that, block by block, choose to send each sample's low bits as they are and its high part in unary; these are Golomb codes with $m = 2^k$. The lossless data compression standard of CCSDS for space data builds on his scheme. Weinberger, Seroussi and Sapiro used Rice codes with context-adaptive $k$ in LOCO-I, the basis of JPEG-LS (ITU-T T.87). FLAC uses partitioned Rice codes for its residuals, and RFC 9639 (2024) specifies the format.

## References
