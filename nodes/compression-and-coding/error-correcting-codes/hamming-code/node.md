---
tag: NYBA8H
kind: definition
slug: hamming-code
name: Hamming code
aliases:
- Hamming(7,4) code
- binary Hamming code
area: compression-and-coding/error-correcting-codes
level: core
summary: A perfect [2^r - 1, 2^r - 1 - r, 3] linear code whose parity-check matrix has every nonzero r bit column once. It corrects one error per block.
prereqs: [parity-check-matrix, syndrome]
see_also: [hamming-bound, syndrome-decoding, simplex-code, golay-code, reed-muller-code, bch-code, parity-bit, error-detection]
sources:
  - paper: doi:10.1002/j.1538-7305.1950.tb00463.x
    title: R. W. Hamming, Error detecting and error correcting codes, Bell System Technical Journal 29(2), 1950, pages 147 to 160
    locator: The single error correcting codes, with check bits at the positions 1, 2, 4, ... and the checking number that gives the position of the error, and the single error correcting plus double error detecting codes
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 1 (Hamming codes, perfect codes, the weight distribution of the Hamming code)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 4, Section 4.1 (Hamming codes) and Section 4.2 (single error correcting and double error detecting codes)
  - paper: "M. Y. Hsiao, A class of optimal minimum odd-weight-column SEC-DED codes, IBM Journal of Research and Development 14(4), 1970, pages 395 to 401"
    title: A class of optimal minimum odd-weight-column SEC-DED codes
    locator: The SECDED codes for computer memory, including the code with 64 data bits and 8 check bits
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 1, Section 1.2 (the (7, 4) Hamming code, its decoding by syndrome, and its error probability on the binary symmetric channel)
---

A Hamming code is a binary [linear code](/linear-code/) of length $n = 2^r - 1$ and dimension $k = 2^r - 1 - r$ whose [parity-check matrix](/parity-check-matrix/) has every nonzero column of length $r$ exactly once. It has minimum distance 3, so it corrects one error in each block, and it is perfect: the balls of radius 1 around the codewords fill the whole space. Richard Hamming published the codes in 1950, and the extended code with one more parity bit protects computer memory as a SECDED code.

## Definition

**Notation.** $\mathrm{GF}(q)$ is the finite field with $q$ elements. An $[n, k, d]_q$ code has length $n$, dimension $k$ and minimum distance $d$; the subscript is left out for $q = 2$. Vectors are rows, $c = m G$ for a generator matrix $G$, and $H c^T = 0$ for a parity-check matrix $H$. The rate is $R = k/n$, and the code corrects $t = \lfloor (d - 1)/2 \rfloor$ errors.

**Binary Hamming code.** Let $r \ge 2$ and $n = 2^r - 1$. Let $H$ be an $r \times n$ binary matrix whose columns are the $n$ nonzero vectors of $\mathrm{GF}(2)^r$, each once, in any order. The binary Hamming code of order $r$ is

$$\mathcal{H}_r = \{\, c \in \mathrm{GF}(2)^n : H c^T = 0 \,\}.$$

A different order of the columns gives an equivalent code, so one speaks of *the* Hamming code.

**Parameters.** $\mathcal{H}_r$ is a $[2^r - 1,\ 2^r - 1 - r,\ 3]$ code with rate $R = 1 - r/(2^r - 1)$, and it corrects $t = 1$ error.

- *Dimension.* The columns include the $r$ unit vectors, so $H$ has rank $r$ and $k = n - r$.
- *Distance.* $d$ is the least number of linearly dependent columns of $H$. No column is zero and no two columns are equal, so no one or two columns are dependent. The columns $e_1$, $e_2$ and $e_1 + e_2$ add to zero, so $d = 3$.

**Perfect.** The [Hamming bound](/hamming-bound/) for a binary code with $t = 1$ is $2^k (1 + n) \le 2^n$. For $\mathcal{H}_r$ the two sides are equal: $2^{n - r} \cdot 2^r = 2^n$. So the balls of radius 1 around the codewords are disjoint and cover $\mathrm{GF}(2)^n$, and every word is at distance at most 1 from exactly one codeword. The covering radius is 1.

**Decoding by the syndrome.** If $c$ is sent and one error hits position $j$, the [syndrome](/syndrome/) is $H (c + e_j)^T = h_j$, column $j$ of $H$. Since the columns are distinct and nonzero, the syndrome names $j$. If column $j$ is the binary form of the number $j$, as in Hamming's paper, the syndrome read as a binary number *is* the position of the error. The decoder flips that bit; a zero syndrome means no error. On BSC($p$) with $p < 1/2$ this hard decision decoder is the maximum likelihood decoder.

**Extended Hamming code.** Add an overall parity bit to every codeword. The result is a $[2^r,\ 2^r - 1 - r,\ 4]$ code: every codeword now has even weight, so the weight 3 codewords become weight 4. The SECDED decoder (single error correction, double error detection) uses the syndrome $s$ of the first $2^r - 1$ bits and the parity $p$ of all $2^r$ bits:

| $s$ | $p$ | decision |
|---|---|---|
| $0$ | $0$ | no error |
| any | $1$ | one error (an odd number); flip the bit that $s$ names, or the parity bit if $s = 0$ |
| $\ne 0$ | $0$ | two errors (an even nonzero number); report, do not correct |

**$q$-ary Hamming code.** Over $\mathrm{GF}(q)$, take one nonzero vector from each one dimensional subspace of $\mathrm{GF}(q)^r$ as the columns of $H$, for example the vectors whose first nonzero entry is 1. There are $n = (q^r - 1)/(q - 1)$ of them, no two are scalar multiples, and three are dependent, so the code is a $[(q^r - 1)/(q - 1),\ n - r,\ 3]_q$ code. It is perfect too: $q^{n - r} (1 + n (q - 1)) = q^{n - r} q^r = q^n$. A single error of value $a$ at position $j$ gives the syndrome $a h_j$, so the decoder finds $j$ from the direction of the syndrome and $a$ from its scale.

## Examples and non-examples

**Examples.**

- **The [7, 4] code in Hamming's layout.** Number the positions $1, \ldots, 7$, put check bits at the powers of two $1, 2, 4$ and the message at $3, 5, 6, 7$. Column $j$ of $H$ is $j$ in binary:

  $$H = \begin{pmatrix} 0&0&0&1&1&1&1 \\ 0&1&1&0&0&1&1 \\ 1&0&1&0&1&0&1 \end{pmatrix}.$$

  Each check bit makes the sum of the positions whose binary form contains it even. The message $1011$ goes to positions $3, 5, 6, 7$; then bit 1 covers positions $3, 5, 7$ and is $1 + 0 + 1 = 0$, bit 2 covers $3, 6, 7$ and is $1$, and bit 4 covers $5, 6, 7$ and is $0$. The codeword is $0110011$. If position 5 flips, the received word is $0110111$; the positions that hold a 1 are $2, 3, 5, 6, 7$, and their XOR is $5 = 101_2$. The decoder flips bit 5 and recovers $0110011$.
- **Weight distribution.** The [7, 4] code has 1 word of weight 0, 7 of weight 3, 7 of weight 4 and 1 of weight 7. The seven words of weight 3 have their 1s on the seven lines of the Fano plane: $\{1,2,3\}$, $\{1,4,5\}$, $\{1,6,7\}$, $\{2,4,6\}$, $\{2,5,7\}$, $\{3,4,7\}$, $\{3,5,6\}$ in Hamming's numbering. The [15, 11] code has 35 words of weight 3, 105 of weight 4 and 168 of weight 5.
- **Systematic form.** Reordered so that the message comes first, the [7, 4] code has the generator matrix with rows $1000110$, $0100011$, $0010111$, $0001101$ (see [systematic code](/systematic-code/)).
- **Error rate.** Because the code is perfect, the decoder is right exactly when at most one of the 7 bits flips. On BSC($p$) the block is decoded correctly with probability $(1 - p)^7 + 7 p (1 - p)^6$. At $p = 0.01$ this is about $0.99797$, so the block error rate is about $0.0020$, against $1 - 0.99^4 \approx 0.039$ for 4 bits sent with no code.
- **Extended [8, 4, 4] code.** Its weights are 0 (once), 4 (14 times) and 8 (once). It is self dual (see [dual code](/dual-code/)), and it is the [Reed-Muller code](/reed-muller-code/) $\mathrm{RM}(1, 3)$. The extended [16, 11, 4] code has 140 words of weight 4.
- **SECDED in memory.** ECC memory stores 64 data bits with 8 check bits. A [72, 64, 4] code is the extended Hamming code of length 128 shortened by 56 positions, up to equivalence. Hsiao (1970) chose 72 columns of $H$ of odd weight with as few 1s as possible, which makes the check circuits smaller and faster.
- **Ternary Hamming code.** For $q = 3$ and $r = 2$, the columns $01, 10, 11, 12$ give $H = \begin{pmatrix} 0&1&1&1 \\ 1&0&1&2 \end{pmatrix}$ and a $[4, 2, 3]_3$ code, the tetracode, with 9 codewords. For $r = 3$ it is a $[13, 10, 3]_3$ code.
- **Cyclic form.** With a suitable order of the columns, $\mathcal{H}_r$ is a [cyclic code](/cyclic-code/): its generator polynomial is a primitive polynomial of degree $r$, for example $1 + x + x^3$ for $r = 3$. So it is also the [BCH code](/bch-code/) of designed distance 3.

**Non-examples.**

- **A repeated column.** If two columns of $H$ are equal, the two matching unit errors have the same syndrome, $d = 2$, and the code only detects one error. The columns must be distinct.
- **A missing column.** If $H$ has fewer than $2^r - 1$ distinct nonzero columns, the code is a *shortened* Hamming code. It still has $d \ge 3$, but it is not perfect: some syndromes match no single error. The [72, 64] memory codes are of this kind.
- **The repetition code [3, 1, 3].** It is the Hamming code for $r = 2$, so it is an example, not a different code: $H$ has the columns $01, 10, 11$. For $r = 1$ there is no Hamming code, since $n = 1$ and $k = 0$.
- **The Golay code.** The binary [23, 12, 7] [Golay code](/golay-code/) is also perfect, but with $t = 3$. Tietäväinen and van Lint proved in 1973 that over prime power alphabets every nontrivial perfect code has the parameters of a Hamming code or of a Golay code. Some perfect codes with Hamming parameters are not linear, so they are not Hamming codes.
- **Two errors.** The [7, 4] decoder does not detect double errors: two errors give the sum of two columns, which is a third column, and the decoder flips a third bit and outputs a wrong codeword. Only the extended code detects them.

## Related definitions

- [Hamming bound](/hamming-bound/): the sphere packing bound that the Hamming codes meet with equality.
- [Syndrome decoding](/syndrome-decoding/): the general method; for the Hamming code the coset leaders are the zero word and the $n$ unit vectors.
- [Simplex code](/simplex-code/): the [dual code](/dual-code/) of $\mathcal{H}_r$, with $G$ equal to the $H$ above; all its nonzero codewords have weight $2^{r - 1}$.
- [Reed-Muller code](/reed-muller-code/): $\mathrm{RM}(r - 2, r)$ is the extended Hamming code of length $2^r$.
- [Parity bit](/parity-bit/): one check bit over all positions; the extended code adds one to the Hamming code.
- [Error detection](/error-detection/): used alone, a Hamming code detects any 1 or 2 errors, and the extended code detects any 1, 2 or 3 errors.

## References
