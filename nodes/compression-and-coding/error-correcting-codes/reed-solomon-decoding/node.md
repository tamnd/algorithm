---
tag: KQB2R4
kind: problem
slug: reed-solomon-decoding
name: Reed-Solomon decoding
aliases:
- RS decoding
- Reed-Solomon error and erasure correction
area: compression-and-coding/error-correcting-codes
level: advanced
summary: Given a received word of a Reed-Solomon code, find the codeword within the decoding radius, correcting nu errors and rho erasures whenever 2 nu + rho is at most n - k.
prereqs: [reed-solomon-code, syndrome]
see_also: [berlekamp-massey, chien-search, forney-algorithm, peterson-gorenstein-zierler, berlekamp-welch, guruswami-sudan, erasure-decoding, nearest-codeword-problem]
sources:
  - paper: doi:10.1016/S0019-9958(75)90090-X
    title: Y. Sugiyama, M. Kasahara, S. Hirasawa and T. Namekawa, A method for solving key equation for decoding Goppa codes, Information and Control 27(1), 1975
    locator: pp. 87 to 99 (the key equation solved by the extended Euclidean algorithm)
  - paper: doi:10.1109/TIT.1965.1053825
    title: G. D. Forney, Jr., On decoding BCH codes, IEEE Transactions on Information Theory 11(4), 1965
    locator: pp. 549 to 557 (the error values, and the decoding of errors and erasures together)
  - paper: doi:10.1137/0109020
    title: D. Gorenstein and N. Zierler, A class of error-correcting codes in p^m symbols, Journal of the Society for Industrial and Applied Mathematics 9(2), 1961
    locator: pp. 207 to 214 (syndrome decoding of the nonbinary codes by a linear system)
  - paper: doi:10.1109/TIT.1969.1054260
    title: J. L. Massey, Shift-register synthesis and BCH decoding, IEEE Transactions on Information Theory 15(1), 1969
    locator: pp. 122 to 127 (the error locator as the shortest LFSR of the syndromes)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 7 (decoding of nonbinary BCH and Reed-Solomon codes, errors and erasures, and the Euclidean decoding algorithm)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Chapter 6 (decoding of generalized Reed-Solomon codes, the key equation, and errors and erasures)
  - paper: "V. Guruswami and A. Vardy, Maximum-likelihood decoding of Reed-Solomon codes is NP-hard, IEEE Transactions on Information Theory 51(7), 2005"
    title: V. Guruswami and A. Vardy, Maximum-likelihood decoding of Reed-Solomon codes is NP-hard, 2005
    locator: The main theorem (the hardness of nearest codeword decoding for Reed-Solomon codes)
---

Reed-Solomon decoding is the problem of recovering a codeword of a [Reed-Solomon code](/reed-solomon-code/) from a received word with some symbols changed (errors) and some symbols marked as unknown (erasures). An $[n, k]$ Reed-Solomon code has minimum distance $d = n - k + 1$, so a unique decoder can correct any $\nu$ errors and $\rho$ erasures with $2\nu + \rho \le n - k$. The standard solution is the syndrome pipeline: compute $n - k$ syndromes, find the error locator with the [Berlekamp-Massey algorithm](/berlekamp-massey/) or the extended Euclidean algorithm, find its roots with the [Chien search](/chien-search/), and compute the error values with the [Forney algorithm](/forney-algorithm/). It runs in $O(n(n-k))$ field operations. The [Berlekamp-Welch algorithm](/berlekamp-welch/) solves the same problem in the evaluation view, and the [Guruswami-Sudan algorithm](/guruswami-sudan/) goes beyond half the distance by returning a list.

## In plain words

A Reed-Solomon codeword is a block of symbols, usually bytes, with some extra check symbols. Noise changes a few symbols on the way. If the receiver knows which symbols are bad, it can rebuild them from the others; these are erasures. If it does not know, it must first find where the bad symbols are; these are errors. An error is twice as costly as an erasure, because it hides both a position and a value. With $r$ check symbols, the decoder can repair any mix in which twice the number of errors plus the number of erasures is at most $r$. Above that, it can fail, and a good decoder says so instead of returning a wrong block.

## Definition

Fix an $[n, k]$ Reed-Solomon code $C$ over $\mathrm{GF}(q)$ in the cyclic view: $n \le q - 1$ (a shortened code if $n < q - 1$), and $c(x) \in C$ exactly when $c(\beta^j) = 0$ for $j = b, \ldots, b + n - k - 1$, where $\beta$ is an element of order $q - 1$ (usually $\beta = \alpha$). Write $r = n - k$ and $t = \lfloor r/2 \rfloor$.

**Input.** A received word $y \in \mathrm{GF}(q)^n$ and a set $E \subseteq \{0, \ldots, n-1\}$ of erasure positions, $|E| = \rho$.

**Output (bounded distance decoding).** The codeword $c \in C$ that differs from $y$ in at most $\nu$ positions outside $E$, where $2\nu + \rho \le r$, if one exists; otherwise "failure".

If such a $c$ exists, it is unique: two codewords $c, c'$ with this property agree outside $E$ except at at most $2\nu$ positions, so they differ in at most $2\nu + \rho \le r < d$ positions, which forces $c = c'$.

**Syndromes.** Let $e = y - c$ be the error pattern (erased positions count as errors at known places). Since $c(\beta^j) = 0$, the syndromes depend on $e$ only:

$$S_j = y(\beta^j) = \sum_{k} Y_k X_k^{\,j}, \qquad j = b, \ldots, b + r - 1,$$

where $X_k = \beta^{i_k}$ is the locator and $Y_k$ the value of the error at position $i_k$.

**The key equation.** With $S(x) = \sum_{i<r} S_{b+i} x^i$, the error locator $\Lambda(x) = \prod_{k}(1 - X_k x)$ over the unknown errors, the erasure locator $\Gamma(x) = \prod_{l \in E}(1 - \beta^{l} x)$, and $\Psi = \Lambda\Gamma$,

$$\Psi(x)\, S(x) \equiv \Omega(x) \pmod{x^{r}}, \qquad \deg \Lambda = \nu, \quad \deg \Omega < \nu + \rho.$$

With $2\nu + \rho \le r$, the pair $(\Lambda, \Omega)$ with $\Lambda(0) = 1$ is the unique solution of least degree. The roots of $\Lambda$ give the error positions, and $\Omega$ gives the values by the Forney formula.

## Variants

- **Errors only** ($\rho = 0$): correct up to $t = \lfloor (n-k)/2 \rfloor$ errors.
- **Erasures only** ($\nu = 0$): recover up to $n - k$ erased symbols, by interpolation from any $k$ known symbols, or by the Forney formula with $\Psi = \Gamma$. See [erasure decoding](/erasure-decoding/).
- **Errors and erasures**: the general case above, with the condition $2\nu + \rho \le n - k$.
- **Evaluation view**: the code is $\{(f(a_1), \ldots, f(a_n)) : \deg f < k\}$ and the output is the message polynomial $f$. The [Berlekamp-Welch algorithm](/berlekamp-welch/) and Gao's algorithm solve this form directly.
- **List decoding**: return all codewords within a radius larger than $t$. The [Guruswami-Sudan algorithm](/guruswami-sudan/) does this up to about $n - \sqrt{nk}$ errors. See [list decoding](/list-decoding/).
- **Soft decision decoding**: use the reliability of each symbol. Generalized minimum distance decoding (Forney) and the Koetter-Vardy algebraic soft decision decoder are the classic methods.
- **Maximum likelihood decoding**: return the nearest codeword at any distance. This is the [nearest codeword problem](/nearest-codeword-problem/) for Reed-Solomon codes.

## Examples

**Two errors in RS(15, 11).** Over $\mathrm{GF}(16)$ with $\alpha^4 = \alpha + 1$, $b = 1$, $r = 4$, $t = 2$. Add $\alpha^5$ at position 2 and $\alpha^{11}$ at position 7 to a codeword. The decoder runs:

| stage | result |
|---|---|
| syndromes $S_1, \ldots, S_4$ | $\alpha^4, \alpha^{13}, \alpha^9, \alpha^{10}$ |
| [Berlekamp-Massey](/berlekamp-massey/) | $L = 2$, $\Lambda(x) = 1 + \alpha^{12} x + \alpha^9 x^2$ |
| [Chien search](/chien-search/) | $\Lambda(\alpha^{-2}) = \Lambda(\alpha^{-7}) = 0$: positions 2 and 7 |
| evaluator | $\Omega(x) = S(x)\Lambda(x) \bmod x^4 = \alpha^4 + \alpha^{12} x$ |
| [Forney](/forney-algorithm/) | $Y = \Omega(X^{-1})/\Lambda'(X^{-1})$: $\alpha^5$ at 2 and $\alpha^{11}$ at 7 |
| check | the syndromes of the corrected word are 0 |

**Errors and erasures.** The same code with $r = 4$ can correct 2 errors, or 1 error and 2 erasures, or 4 erasures, but not 2 errors and 1 erasure ($2 \cdot 2 + 1 = 5 > 4$).

**QR codes.** A version 1-M QR symbol has 26 codewords, 16 data and 10 error correction codewords, over $\mathrm{GF}(256)$ with the polynomial 0x11D and $b = 0$. The code can correct 5 codeword errors, or 10 erasures, for example parts of the symbol that are covered or damaged. ISO/IEC 18004 rates it at 4 errors, because it keeps 2 codewords as a reserve against misdecoding.

**CCSDS RS(255, 223).** With $E = 16$ and the zeros $\beta^{112}, \ldots, \beta^{143}$, $\beta = \alpha^{11}$, the decoder corrects 16 symbol errors per codeword. With interleaving depth $I$, it corrects a burst of up to $16 I$ consecutive symbols.

**Beyond the radius.** RS(7, 3) over $\mathrm{GF}(8)$ has $t = 2$. With 3 errors, the bounded distance decoder either reports a failure or returns a different codeword within distance 2 of the received word (a decoder error). The decoder cannot tell the second case from a correct decoding.

## Known algorithms

| algorithm | stage | operations | notes |
|---|---|---|---|
| syndromes by Horner's rule | syndromes | $O(n r)$ | $r$ evaluations of a degree $n-1$ polynomial |
| [Peterson-Gorenstein-Zierler](/peterson-gorenstein-zierler/) (1960, 1961) | locator | $O(t^4)$ | solve the syndrome matrix, $O(t^3)$ for each try, and reduce $\nu$ until it is nonsingular |
| [Berlekamp-Massey](/berlekamp-massey/) (1968, 1969) | locator | $O(t^2)$ | shortest LFSR of the syndromes; erasures by a start at $\Gamma$ |
| Euclid: Sugiyama, Kasahara, Hirasawa and Namekawa (1975) | locator and evaluator | $O(t^2)$ | extended Euclid on $x^r$ and $S(x)\Gamma(x)$, stop when $\deg < (r + \rho)/2$ |
| [Chien search](/chien-search/) (1964) | positions | $O(n t)$ | test each position with fixed multipliers |
| [Forney](/forney-algorithm/) (1965) | values | $O(t^2)$ | $Y = -X^{1-b}\Omega(X^{-1})/\Psi'(X^{-1})$ |
| [Berlekamp-Welch](/berlekamp-welch/) (1986) | all, evaluation view | $O(n^3)$ | one linear system for $E$ and $Q = E f$ |
| Gao (2003), fast Euclid and FFT methods | all | $O(n \log^2 n)$ or less | for long codes |
| [Guruswami-Sudan](/guruswami-sudan/) (1999) | list decoding | polynomial | radius below $n - \sqrt{n(k-1)}$ |

The syndrome pipeline costs $O(n t)$ field operations in total, with $O(n t)$ for the syndromes and the Chien search and $O(t^2)$ for the rest.

**Failure detection.** A bounded distance decoder can detect many patterns beyond its radius. It reports a failure if the locator has $L > t$ (or $2\nu + \rho > r$), if $\deg \Lambda$ differs from the LFSR length, if the Chien search finds fewer than $\deg \Lambda$ roots, or roots outside a shortened code or on an erasure, if a Forney denominator is zero, or if the corrected word has nonzero syndromes.

## Bounds

- **Unique decoding radius.** No decoder can always correct $\nu$ errors and $\rho$ erasures with $2\nu + \rho \ge d = n - k + 1$: two codewords at distance $d$ have a received word between them. So $2\nu + \rho \le n - k$ is the exact limit for unique decoding, and the syndrome pipeline reaches it.
- **Erasures.** $n - k$ erasures are the limit, because $k$ symbols are needed to fix a polynomial of degree below $k$.
- **List decoding.** With a list of polynomial size, the Guruswami-Sudan algorithm corrects any number of errors below $n - \sqrt{n(k-1)}$, the Johnson radius. See [list decoding](/list-decoding/).
- **Maximum likelihood decoding.** Finding the nearest codeword of a Reed-Solomon code is NP-hard in general (Guruswami and Vardy, 2005).
- **Time.** Any decoder must read the $n$ symbols, so $\Omega(n)$ operations are necessary; the fast methods reach $O(n \log^2 n)$ or less.

## Reductions

- **To LFSR synthesis.** The error locator is the shortest LFSR of the syndrome sequence when $\nu \le t$. So the main step is [LFSR synthesis](/lfsr-synthesis/).
- **To rational reconstruction.** The key equation is a Padé problem modulo $x^r$, which the [extended Euclidean algorithm](/polynomial-extended-euclidean-algorithm/) solves.
- **To root finding.** The positions are the roots of $\Lambda$ among $\beta^{-i}$, $0 \le i < n$.
- **To a linear system.** The [Peterson-Gorenstein-Zierler](/peterson-gorenstein-zierler/) and [Berlekamp-Welch](/berlekamp-welch/) decoders reduce the problem to [Gaussian elimination](/gaussian-elimination/).
- **From binary BCH decoding.** A binary BCH code is a subfield subcode of a Reed-Solomon code, so a Reed-Solomon decoder decodes it; the error values are then all 1.

## Applications

- Deep space and satellite links (CCSDS RS(255, 223), often as the outer code of a [concatenated code](/concatenated-codes/) with a convolutional inner code).
- QR codes and other two-dimensional bar codes, with erasures for damaged areas.
- Compact discs (cross-interleaved Reed-Solomon codes), DVDs and Blu-ray discs.
- Digital television (DVB), DSL, and storage systems such as RAID 6 and distributed storage, where erasure decoding rebuilds lost disks.

## References
