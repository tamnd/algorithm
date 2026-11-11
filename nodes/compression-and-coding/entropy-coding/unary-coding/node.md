---
tag: KAJ1DT
kind: definition
slug: unary-coding
name: Unary coding
aliases:
- unary code
area: compression-and-coding/entropy-coding
level: intro
summary: Writes an integer x >= 0 as x one bits and a final zero bit. It is the optimal prefix code for P(x) = 2^-(x+1) and the building block of the gamma, Golomb and Rice codes.
prereqs: [prefix-code, geometric-distribution]
see_also: [elias-gamma-coding, golomb-coding, rice-coding, exp-golomb-coding, kraft-inequality, huffman-coding, elias-fano-encoding, universal-code]
sources:
  - paper: doi:10.1109/TIT.1975.1055349
    title: Peter Elias, Universal codeword sets and representations of the integers, IEEE Transactions on Information Theory 21(2), 1975
    locator: pp. 194 to 203 (the unary codeword set alpha, used as the first part of the gamma and delta codes)
  - paper: doi:10.1109/TIT.1966.1053907
    title: Solomon W. Golomb, Run-length encodings, IEEE Transactions on Information Theory 12(3), 1966
    locator: pp. 399 to 401 (the quotient of a run length written in unary)
  - paper: doi:10.1109/TIT.1975.1055357
    title: Robert G. Gallager and David C. van Voorhis, Optimal source codes for geometrically distributed integer alphabets, IEEE Transactions on Information Theory 21(2), 1975
    locator: pp. 228 to 230 (the optimal Golomb parameter; m = 1 gives the unary code)
  - paper: doi:10.1145/3415148
    title: Giulio Ermanno Pibiri and Rossano Venturini, Techniques for inverted index compression, ACM Computing Surveys 53(6), Article 125, 2020
    locator: Section 2.2, Unary and Binary, and Table 3 (arXiv:1908.10598v2)
  - url: https://www.rfc-editor.org/rfc/rfc9639
    title: M.Q.C. van Beurden and A. Weaver, RFC 9639, Free Lossless Audio Codec (FLAC), December 2024
    locator: Section 9.2.7.2, Rice Code (unary written as zero bits ended by a one bit)
---

The unary code writes an integer $x \ge 0$ as $x$ one bits followed by one zero bit, so the codeword of $x$ has $x + 1$ bits. It is a [prefix code](/prefix-code/), and it is the optimal prefix code when $P(x) = 2^{-(x+1)}$, the [geometric distribution](/geometric-distribution/) with ratio $1/2$. Few sources are that skewed, so the unary code is rarely used alone. Its main job is to be the first part of other codes: the [Elias gamma code](/elias-gamma-coding/) writes a bit length in unary, and the [Golomb](/golomb-coding/) and [Rice](/rice-coding/) codes write a quotient in unary.

## Definition

Notation: $x$ is the integer to code, $\ell(x)$ is the length of its codeword in bits, and logarithms are base 2. The probability results assume a memoryless source of integers.

For an integer $x \ge 0$, the **unary codeword** of $x$ is

$$U(x) = \underbrace{1 1 \cdots 1}_{x} \, 0, \qquad \ell(x) = x + 1.$$

The decoder reads bits until it reads a zero, and returns the number of ones that it read. The final zero is the *stop bit*, sometimes called the comma.

Three conventions are in use, and a format must say which one it uses:

- **Ones, then a zero** (this page): $U(x) = 1^x 0$.
- **Zeros, then a one**: $U(x) = 0^x 1$. FLAC writes the quotient of its Rice code this way (RFC 9639, Section 9.2.7.2), and the prefix of the exp-Golomb codes of H.264 is $0^z 1$.
- **Positive integers**: $x \ge 1$ is written as $1^{x-1} 0$, with $x$ bits. This is the same code applied to $x - 1$. The survey of Pibiri and Venturini uses this form.

The three forms have the same lengths up to the offset, so every statement below holds for each of them.

**Facts.**

1. *The code is prefix-free.* Each codeword holds exactly one zero, and the zero is its last bit. If $U(x)$ were a proper prefix of $U(y)$, then $U(y)$ would have a zero at position $x + 1$ and more bits after it, which is not possible. So $U$ is a prefix code and a stream of codewords decodes in one way.
2. *The code is complete.* The [Kraft sum](/kraft-inequality/) is $\sum_{x \ge 0} 2^{-(x+1)} = 1$. So no codeword can be added and no codeword can be made shorter without the loss of the prefix property.
3. *It is optimal for $P(x) = 2^{-(x+1)}$.* For this source $\ell(x) = x + 1 = -\log P(x)$ for each $x$. The expected length is $\sum_{x \ge 0} (x+1) 2^{-(x+1)} = 2$, which equals the [Shannon entropy](/shannon-entropy/) $H = 2$ bits of the source. By the [source coding theorem](/source-coding-theorem/), no uniquely decodable code has a smaller expected length.
4. *It is optimal for each geometric source with ratio $\theta \le (\sqrt 5 - 1)/2 \approx 0.618$.* For $P(x) = (1-\theta)\theta^x$, the unary code is the Golomb code with parameter $m = 1$. Gallager and van Voorhis proved that the Golomb code with the smallest $m$ such that $\theta^m + \theta^{m+1} \le 1$ is optimal. For $m = 1$ the condition is $\theta + \theta^2 \le 1$, that is $\theta \le (\sqrt 5 - 1)/2$. For a larger $\theta$, a Golomb code with $m \ge 2$ is strictly better.

**Expected length.** For $P(x) = (1-\theta)\theta^x$, the expected length of the unary code is $\sum_{x \ge 0} (x+1)(1-\theta)\theta^x = 1/(1-\theta)$. The entropy of the same source is $h(\theta)/(1-\theta)$, where $h$ is the [binary entropy function](/binary-entropy-function/).

| $\theta$ | entropy (bits) | unary length (bits) |
|---|---|---|
| 0.5 | 2.000 | 2.0 |
| 0.6 | 2.427 | 2.5 |
| 0.75 | 3.245 | 4.0 |
| 0.9 | 4.690 | 10.0 |

At $\theta = 0.6$ the unary code is still optimal, but it is above the entropy, because each codeword has an integer length. At $\theta = 0.9$ the unary code uses more than twice the entropy, and the right tool is a Golomb code with a larger $m$.

**Cost.** The encoder writes $x + 1$ bits. A decoder that reads one bit at a time does $x + 1$ steps. On a [word RAM](/word-ram/) with a count-leading-zeros instruction, the decoder finds the stop bit in a $w$-bit word in one step, so it takes $O(1 + x/w)$ steps.

## Examples and non-examples

**Codewords.**

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $U(x)$ | 0 | 10 | 110 | 1110 | 11110 | 111110 |
| $\ell(x)$ | 1 | 2 | 3 | 4 | 5 | 6 |

**A stream.** The list $3, 0, 2$ codes as $1110 \cdot 0 \cdot 110$, that is the 8 bits `11100110`. The decoder reads three ones and a zero (3), then a zero at once (0), then two ones and a zero (2).

**The Huffman code of the dyadic geometric source.** Take the weights $2^{-1}, 2^{-2}, \ldots, 2^{-30}$ for $x = 0, \ldots, 29$, plus one extra symbol with the rest of the mass, $2^{-30}$. The [Huffman code](/huffman-coding/) of these 31 weights gives the codeword lengths $1, 2, \ldots, 30$ to $x = 0, \ldots, 29$. These are the unary lengths.

**Non-examples.**

- *Plain binary* is not a prefix code: the codeword `1` of 1 is a prefix of the codeword `10` of 2. A reader of a stream cannot tell where a number ends.
- *A run of ones with no stop bit* is not uniquely decodable: `111` could be 3, or 1 and 2, or three times 1.
- *Truncated unary* drops the stop bit of the largest value of a bounded range $0 \ldots c$, because no longer codeword exists. It is a complete prefix code for the finite range, and CABAC uses it as a binarization (the TU binarization of H.264, Section 9.3.2.2). It is not a code for all integers.
- *The unary code is not a [universal code](/universal-code/).* For the uniform distribution on $1 \ldots 2^k$ the entropy is $k$ bits, but the expected unary length is about $2^{k-1}$ bits.

## Related definitions

- [Prefix code](/prefix-code/) and the [Kraft inequality](/kraft-inequality/): the unary code meets the Kraft inequality with equality.
- [Elias gamma coding](/elias-gamma-coding/): the unary code of the bit length, then the bits of the number.
- [Golomb coding](/golomb-coding/) and [Rice coding](/rice-coding/): the quotient in unary, the remainder in binary. The unary code is the Golomb code with $m = 1$ and the Rice code with $k = 0$.
- [Exp-Golomb coding](/exp-golomb-coding/): the unary code of a bucket number, then an offset inside the bucket.
- [Elias-Fano encoding](/elias-fano-encoding/): it stores the high parts of a sorted list as gaps in unary in a bit vector. This is a representation of a sorted sequence, not a code for one integer.
- [Run-length encoding](/run-length-encoding/): runs of a binary source have geometric lengths, which is why Golomb put a unary part into his run-length code.

## References
