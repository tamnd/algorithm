---
tag: MNB3EF
kind: algorithm
slug: golomb-coding
name: Golomb coding
aliases:
- Golomb code
area: compression-and-coding/entropy-coding
level: advanced
summary: Codes x >= 0 with a parameter m as the quotient x div m in unary and the remainder in truncated binary. With the right m it is an optimal prefix code for a geometric source.
model: word-ram
complexity:
  vars: {x: the integer to code, m: the Golomb parameter}
  time: {worst: Θ(x/m + log m), average: Θ(1 + log m), best: Θ(1 + log m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, online: true, recursive: false}
history:
  year: 1966
  people: [Solomon W. Golomb]
  note: Golomb introduced the code for the run lengths of a binary memoryless source. Gallager and van Voorhis proved in 1975 which parameter makes it optimal.
prereqs: [unary-coding, geometric-distribution]
see_also: [rice-coding, exp-golomb-coding, huffman-coding, run-length-encoding, elias-gamma-coding, optimal-prefix-code, inverted-index, binary-entropy-function]
sources:
  - paper: doi:10.1109/TIT.1966.1053907
    title: Solomon W. Golomb, Run-length encodings, IEEE Transactions on Information Theory 12(3), 1966
    locator: pp. 399 to 401 (the code with parameter m for geometric run lengths)
  - paper: doi:10.1109/TIT.1975.1055357
    title: Robert G. Gallager and David C. van Voorhis, Optimal source codes for geometrically distributed integer alphabets, IEEE Transactions on Information Theory 21(2), 1975
    locator: pp. 228 to 230 (the choice of m and the proof of optimality)
  - paper: doi:10.1145/3415148
    title: Giulio Ermanno Pibiri and Rossano Venturini, Techniques for inverted index compression, ACM Computing Surveys 53(6), Article 125, 2020
    locator: Section 2.4, Golomb, and Table 3 (arXiv:1908.10598v2)
  - book: isbn:9781558605701
    title: Ian H. Witten, Alistair Moffat and Timothy C. Bell, Managing Gigabytes, 2nd edition, Morgan Kaufmann, 1999
    locator: Chapter 3, Indexing (Golomb codes for the gaps of inverted lists)
---

The Golomb code with parameter $m \ge 1$ writes an integer $x \ge 0$ in two parts: the quotient $q = \lfloor x/m \rfloor$ in [unary](/unary-coding/), and the remainder $r = x - qm$ in truncated binary, a code for $0, \ldots, m-1$ with $\lfloor \log_2 m \rfloor$ or $\lceil \log_2 m \rceil$ bits. Each increase of $x$ by $m$ adds one bit, so the code suits integers whose probability falls by a constant factor every $m$ steps: the [geometric distribution](/geometric-distribution/). For a geometric source with ratio $\theta$, the Golomb code with the smallest $m$ such that $\theta^m + \theta^{m+1} \le 1$ is an optimal prefix code, as Gallager and van Voorhis proved. Solomon Golomb introduced the code in 1966 for run lengths.

## In plain words

Pick a block size $m$. To send a number, say how many full blocks fit into it, and then where it falls inside the last block.

The count of blocks is sent in unary: one bit for each block and a stop bit. The position inside the block is a number from 0 to $m - 1$, sent in nearly fixed width. If $m$ is a power of two, every position takes the same number of bits. Otherwise a few small positions take one bit less, so that no bit pattern is wasted.

The right block size depends on how fast the numbers become rare. If large numbers are rare, use small blocks. If they are common, use large blocks, so the unary part stays short.

## The problem

The input is a sequence of integers $x_1, \ldots, x_n \ge 0$ from a memoryless source, $P(x) = (1-\theta)\theta^x$ for some $0 < \theta < 1$. Such values arise as run lengths of a binary source, as gaps between the positions of a random subset, and as the absolute residuals of many predictors. The task is a prefix code with the least expected length for this source, which also needs no table: a code with an infinite alphabet cannot be built by a [Huffman](/huffman-coding/) pass.

Notation: $x$ is one integer to code, $m$ is the parameter, $q$ and $r$ are the quotient and remainder, $k = \lfloor \log_2 m \rfloor$, $u = 2^{k+1} - m$, and $\ell(x)$ is the codeword length in bits. Logarithms are base 2. Unary is written as ones ended by a zero.

## The algorithm

```pseudo id=main
GOLOMB-ENCODE(x, m, W)                     ▷ x ≥ 0, m ≥ 1, W is a bit writer
L1  q ← ⌊x / m⌋; r ← x − q·m
L2  write q one bits to W, then one zero bit
L3  k ← ⌊log₂ m⌋; u ← 2^(k+1) − m          ▷ u remainders get the short words
L4  if r < u then write r in k bits
L5  else write r + u in k + 1 bits

GOLOMB-DECODE(m, R)                        ▷ R is a bit reader
L6  q ← 0; while READ-BIT(R) = 1 do q ← q + 1
L7  k ← ⌊log₂ m⌋; u ← 2^(k+1) − m
L8  r ← the next k bits of R, read as a binary number
L9  if r ≥ u then r ← 2r + READ-BIT(R) − u
L10 return q·m + r
```

Lines L3 to L5 are **truncated binary**, the optimal prefix code for $m$ equally likely values. A plain $\lceil \log_2 m \rceil$-bit field would leave $2^{k+1} - m = u$ patterns unused when $m$ is not a power of two. Truncated binary gives $k$-bit words to the first $u$ remainders and $(k+1)$-bit words to the other $m - u$. The short words are the $k$-bit values $0, \ldots, u - 1$. The long words are the $(k+1)$-bit values $2u, \ldots, 2^{k+1} - 1$, whose first $k$ bits are at least $u$, so no short word is a prefix of a long word. If $m$ is a power of two, $u = m$ and every remainder takes $k$ bits: this is [Rice coding](/rice-coding/).

The decoder reads the unary part in line L6. Line L8 reads $k$ bits. If they form a value below $u$, they are a short word. Otherwise they are the top $k$ bits of a long word, and line L9 reads its last bit and subtracts $u$.

**The parameter.** For $P(x) = (1-\theta)\theta^x$, Gallager and van Voorhis showed that the best $m$ is the smallest integer with

$$\theta^m + \theta^{m+1} \le 1, \qquad\text{that is}\qquad m = \left\lceil \frac{\log(1 + \theta)}{-\log \theta} \right\rceil.$$

The choice makes the probability of a quotient step, $\theta^m$, close to $1/2$, so the unary bit of each block carries nearly one full bit of information. In practice $\theta$ is not known and $m$ is set from the mean: with mean $\mu = \theta/(1-\theta)$, $m \approx \ln 2 \cdot \mu \approx 0.69\mu$ for large $\mu$. For gaps in a document list of $f$ entries over $N$ documents, Witten, Moffat and Bell use $m \approx 0.69 N / f$.

## Example

Take $m = 5$. Then $k = 2$ and $u = 8 - 5 = 3$, so remainders 0, 1, 2 take 2 bits and remainders 3, 4 take 3 bits.

| $r$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| word | 00 | 01 | 10 | 110 | 111 |

Encode $x = 17$: line L1 gives $q = 3$ and $r = 2$. Line L2 writes `1110`. Since $2 < 3$, line L4 writes `10`. The codeword is `1110 10`. Encode $x = 9$: $q = 1$, $r = 4 \ge 3$, so line L5 writes $4 + 3 = 7$ in 3 bits. The codeword is `10 111`.

Decode `10111`:

| step | bits read | $q$ | $r$ | result |
|---|---|---|---|---|
| L6 | `1`, `0` | 1 | | |
| L8 | `11` | 1 | 3 | |
| L9 | `1` (since $3 \ge u$) | 1 | $2 \cdot 3 + 1 - 3 = 4$ | |
| L10 | | | | $1 \cdot 5 + 4 = 9$ |

The codewords for $m = 2$ and $x = 0, \ldots, 7$ are `00`, `01`, `100`, `101`, `1100`, `1101`, `11100`, `11101`.

**Expected lengths.** For the geometric source, with the parameter from the rule above:

| $\theta$ | best $m$ | Golomb (bits) | entropy (bits) | unary (bits) |
|---|---|---|---|---|
| 0.5 | 1 | 2.000 | 2.000 | 2.0 |
| 0.6 | 1 | 2.500 | 2.427 | 2.5 |
| 0.7 | 2 | 2.961 | 2.938 | 3.3 |
| 0.8 | 3 | 3.639 | 3.610 | 5.0 |
| 0.9 | 7 | 4.725 | 4.690 | 10.0 |

## Correctness

The decoder inverts the encoder part by part. Line L6 reads the $q$ ones and the zero of line L2, so it returns $q$. Lines L8 and L9 decode truncated binary: a short word $r < u$ is read whole in line L8, and a long word $r + u \ge 2u$ has top $k$ bits $\lfloor (r+u)/2 \rfloor \ge u$, so line L9 runs and recovers $2\lfloor (r+u)/2 \rfloor + (r + u \bmod 2) - u = r$. Then $qm + r = x$. The code is prefix-free because unary is a prefix code and truncated binary is a prefix code. The optimality for geometric sources is the theorem of Gallager and van Voorhis. The full proof of the round trip is in the proof file.

## Complexity

**Length.** $\ell(x) = \lfloor x/m \rfloor + 1 + k + [r \ge u]$, where $[\cdot]$ is 1 if the condition holds and 0 if not. So the length grows by one bit for each $m$ added to $x$.

**Time.** Encoding and decoding take $\Theta(q + \log m) = \Theta(x/m + \log m)$ bit steps. On a geometric source with the best $m$, $E[q] = \theta^m / (1 - \theta^m) \le 1.62$, so the expected time is $\Theta(1 + \log m)$. On a [word RAM](/word-ram/) with a count-leading-zeros instruction, the unary part of up to $w$ bits takes $O(1)$ steps. The division in line L1 is the main cost for a general $m$; a Rice code replaces it by a shift.

**Optimality.** For each $\theta$, the Golomb code with the parameter of Gallager and van Voorhis has the least expected length of any prefix code for $P(x) = (1 - \theta)\theta^x$. Their proof applies the [Huffman](/huffman-coding/) procedure to finite reduced forms of the source and shows that it builds the Golomb code tree. The unary code is the case $m = 1$, optimal for $\theta \le (\sqrt 5 - 1)/2 \approx 0.618$.

## Properties

- **Prefix-free and complete.** Unary and truncated binary both have Kraft sum 1, so the Golomb code has Kraft sum 1.
- **One parameter.** The model is a single integer, cheap to send in a header or to adapt per block.
- **Graceful on the wrong parameter.** A value of $m$ near the best one costs little: the expected length is flat near the optimum.
- **Long codewords on outliers.** A value far above $m$ gets a long unary part. A format with outliers needs an escape or a length limit.

## Variants and improvements

- **Rice coding.** [Rice coding](/rice-coding/) restricts $m$ to powers of two, $m = 2^j$. The remainder is a fixed $j$-bit field, the division is a shift, and the loss against the best Golomb code is small.
- **Exp-Golomb coding.** [Exp-Golomb coding](/exp-golomb-coding/) doubles the bucket size at each step instead of keeping it fixed, so it suits sources with heavier tails than geometric.
- **Limited-length Golomb codes.** JPEG-LS caps the unary part and sends large values with an escape and a fixed-width field.
- **Two-sided geometric sources.** Prediction residuals have a two-sided law. A coder maps signed values to non-negative ones by $v \mapsto 2v$ for $v \ge 0$ and $v \mapsto -2v - 1$ for $v < 0$, then applies the Golomb code.
- **Adaptive parameter.** The encoder and the decoder can update $m$ from the running mean of the values seen so far, which needs no side information.

## When to use it

Use the Golomb code for non-negative integers with a roughly geometric law and a known or estimated mean: run lengths in a binary image, gaps between sorted IDs in an [inverted index](/inverted-index/), gaps between hash values in a Golomb-coded set, and residuals in lossless audio and image coding. If the law has a heavier tail, use [exp-Golomb coding](/exp-golomb-coding/) or the [Elias gamma code](/elias-gamma-coding/). If the alphabet is small and known, a [Huffman code](/huffman-coding/) of the actual frequencies can do better. If speed matters more than the last fraction of a bit, use a Rice code.

## Pitfalls

- **Writing $r$ instead of $r + u$ in line L5.** A long word must be $r + u$ in $k + 1$ bits. Writing $r$ in $k + 1$ bits makes some long words start with a short word; for $m = 5$, $r = 3$ would become `011`, which starts with the word `01` of $r = 1$.
- **Reading $k + 1$ bits at once in line L8.** The decoder must read $k$ bits, test them against $u$, and only then read one more bit in line L9. A decoder that always reads $k + 1$ bits reads one bit of the next codeword after each short word.
- **Using $\lceil \log_2 m \rceil$ for $k$.** Line L3 uses the floor. With the ceiling and an $m$ that is not a power of two, $u$ is larger than $m$, so every remainder takes $\lceil \log_2 m \rceil$ bits. The stream is longer than needed and does not match a decoder that uses the floor.
- **A parameter from the wrong rule.** Setting $m$ so that $\theta^m = 1/2$ exactly, then rounding to the nearest integer, can miss the best $m$ by one. Use the inequality $\theta^m + \theta^{m+1} \le 1$.
- **Outliers.** One huge value writes a unary run of $x/m$ bits. Cap the unary part with an escape when the source can produce outliers.

## Implementations

## History

Solomon Golomb described the code in 1966 for the run lengths of a binary memoryless source, where the run length has a geometric law, and noted that the best $m$ makes $\theta^m$ close to $1/2$. Gallager and van Voorhis gave the exact rule for $m$ in 1975 and proved that the code is optimal. Rice restricted $m$ to powers of two in 1979, for simple adaptive coders. The code became standard for inverted-file compression in the 1990s, and its Rice form is used in FLAC and, with a length limit, in JPEG-LS.

## References
