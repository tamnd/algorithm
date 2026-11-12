---
tag: XEFEQH
kind: problem
slug: nearest-codeword-problem
name: Nearest codeword problem
aliases:
- NCP
- coset weights problem
area: compression-and-coding/error-correcting-codes
level: advanced
summary: Given a linear code and a word y, find a codeword nearest to y in Hamming distance. NP-hard (1978) and hard to approximate within any constant factor (1997).
prereqs: [linear-code, syndrome, maximum-likelihood-decoding, np-hard, three-dimensional-matching]
see_also: [syndrome-decoding, syndrome-decoding-problem, nearest-codeword-inapproximability, minimum-distance-problem, information-set-decoding, learning-parity-with-noise, closest-vector-problem, polynomial-time-reduction]
sources:
  - paper: doi:10.1109/TIT.1978.1055873
    title: Elwyn R. Berlekamp, Robert J. McEliece and Henk C. A. van Tilborg, On the inherent intractability of certain coding problems, IEEE Transactions on Information Theory 24(3), 1978, pages 384 to 386
    locator: The problems Coset Weights and Subspace Weights, their NP-completeness by reductions from three dimensional matching, and the conjecture on the minimum distance
  - paper: doi:10.1006/jcss.1997.1472
    title: Sanjeev Arora, László Babai, Jacques Stern and Z. Sweedyk, The hardness of approximate optima in lattices, codes, and systems of linear equations, Journal of Computer and System Sciences 54(2), 1997, pages 317 to 331
    locator: The results on the nearest codeword problem, hardness within any constant factor and within 2^(log^(1 - ε) n) under a quasi-polynomial time assumption
  - paper: "J. Bruck and M. Naor, The hardness of decoding linear codes with preprocessing, IEEE Transactions on Information Theory 36(2), 1990"
    title: Jehoshua Bruck and Moni Naor, The hardness of decoding linear codes with preprocessing
    locator: The main theorem, hardness of maximum likelihood decoding when the code is fixed in advance
  - paper: "V. Guruswami and A. Vardy, Maximum-likelihood decoding of Reed-Solomon codes is NP-hard, IEEE Transactions on Information Theory 51(7), 2005"
    title: Venkatesan Guruswami and Alexander Vardy, Maximum-likelihood decoding of Reed-Solomon codes is NP-hard
    locator: The main theorem, for Reed-Solomon codes over fields of growing size
  - paper: doi:10.1109/TIT.2002.806118
    title: Ilya Dumer, Daniele Micciancio and Madhu Sudan, Hardness of approximating the minimum distance of a linear code, IEEE Transactions on Information Theory 49(1), 2003, pages 22 to 37
    locator: Section 1 (the survey of results on the nearest codeword problem, including the results of Dinur, Kindler, Raz and Safra and of Berman and Karpinski)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, W. H. Freeman, 1979
    locator: Section 3.1 (three dimensional matching is NP-complete)
---

The nearest codeword problem (NCP) asks, for a [linear code](/linear-code/) given by a matrix and a word $y$, for a codeword nearest to $y$ in Hamming distance. It is hard decision [maximum likelihood decoding](/maximum-likelihood-decoding/) on a binary symmetric channel, written as a problem on matrices. Its decision form is NP-complete (Berlekamp, McEliece and van Tilborg, 1978), and its optimization form is NP-hard to approximate within any constant factor (Arora, Babai, Stern and Sweedyk, 1997). The problem is about the worst case over all codes; the cryptographic [syndrome decoding problem](/syndrome-decoding-problem/) is about random codes.

## In plain words

A code is a list of allowed words, given in a compact form by a few basis words: every allowed word is a sum of some of them. A received word arrives, with some symbols changed. The task is to find the allowed word that differs from it in the fewest places.

For a short code you can try every allowed word, or prepare a table. But the number of allowed words doubles with each basis word, so this fails for long codes. Is there always a clever method? Unless a long-standing belief in complexity theory is false, no: some codes are so badly structured that no fast method finds the nearest word, or even a word that is only a fixed number of times farther away than the nearest.

Good codes in practice are built with extra structure exactly so that fast decoders exist for them.

## Definition

**Notation.** $C$ is an $[n, k, d]_q$ linear code over $\mathrm{GF}(q)$ given by a $k \times n$ generator matrix $G$ ($c = m G$) or an $(n - k) \times n$ parity-check matrix $H$ ($H c^T = 0$). Vectors are rows. $\mathrm{wt}$ is the Hamming weight and $d(x, y) = \mathrm{wt}(x - y)$. The input size is the size of the matrix, about $k n \log q$ or $(n - k) n \log q$.

**NCP, search form.** Input: $G$ and $y \in \mathrm{GF}(q)^n$. Output: a codeword $c$ with $d(y, c) = \min_{c' \in C} d(y, c')$.

**NCP, decision form.** Input: $G$, $y$ and an integer $w$. Question: is there a codeword $c$ with $d(y, c) \le w$?

**Syndrome form (coset weights).** Input: $H$, a syndrome $s \in \mathrm{GF}(q)^{n-k}$ and $w$. Question: is there $e$ with $\mathrm{wt}(e) \le w$ and $H e^T = s$? This is the problem COSET WEIGHTS of Berlekamp, McEliece and van Tilborg, stated over $\mathrm{GF}(2)$.

**The forms are equivalent.** From $(G, y, w)$, compute a parity-check matrix $H$ and $s = H y^T$. The words $y - c$ with $c \in C$ are exactly the $e$ with $H e^T = s$, so the answers agree. From $(H, s, w)$, solve $H y^T = s$ by Gaussian elimination (there is always a solution when $H$ has full rank) and take a basis of the null space of $H$ as $G$. Both maps take polynomial time. A search algorithm for one form gives one for the other in the same way, and binary search over $w$ turns a decision oracle into the optimal value.

**Which channel.** NCP is ML decoding for the binary symmetric channel BSC($p$) with $p < 1/2$, or the $q$-ary symmetric channel, with hard decisions. It is not ML decoding on other channels; see [maximum likelihood decoding](/maximum-likelihood-decoding/).

## Variants

- **Optimization and approximation.** Find a codeword $c$ with $d(y, c) \le \gamma \cdot \min_{c'} d(y, c')$ for an approximation factor $\gamma \ge 1$.
- **Bounded distance decoding.** The promise that $y$ is within a fraction of $d$ of the code, for example within $t = \lfloor (d - 1)/2 \rfloor$, so that the nearest codeword is unique. Algebraic decoders solve this for Reed-Solomon and BCH codes.
- **Decoding with preprocessing.** The code is fixed in advance and an algorithm may compute any advice from it, of polynomial size; only $y$ is the input. Bruck and Naor (1990) showed that this is still hard: some codes have no such decoder unless NP $\subseteq$ P/poly.
- **Fixed families.** The problem restricted to one family of codes. For Reed-Solomon codes, ML decoding is NP-hard over fields of growing size (Guruswami and Vardy, 2005), although decoding up to the Guruswami-Sudan radius is polynomial.
- **Exact weight.** Ask for $e$ with $\mathrm{wt}(e) = w$ exactly and $H e^T = s$. The reduction below shows this is NP-complete too.
- **Average case.** $H$ uniformly random and $e$ of a fixed weight: this is the [syndrome decoding problem](/syndrome-decoding-problem/) of code-based cryptography, and with a Bernoulli noise model it is [learning parity with noise](/learning-parity-with-noise/). Hardness in the worst case, the subject of this page, does not imply hardness on average, and the cryptographic pages rest on separate assumptions.

## Examples

- **Hamming code.** For the $[7, 4, 3]$ [Hamming code](/hamming-code/) with generator rows $1000110$, $0100011$, $0010111$, $0001101$, the word $y = 1111110$ is at distance 1 from the codeword $1111111$, the sum of all four rows, and every other codeword is at distance at least 2. Since the code is perfect, every word is within distance 1 of exactly one codeword.
- **Ties.** For the $[5, 2, 3]$ code with generator rows $10110$ and $01011$, the word $y = 11000$ is at distance 2 from $00000$ and from $11101$, and at distance 3 from $01011$ and from $10110$. The nearest distance is 2, and the nearest codeword is not unique.
- **The reduction on a small instance.** Take $X = Y = Z = \{0, 1\}$ and the triples $(0,0,0)$, $(1,1,1)$, $(0,1,1)$, $(1,0,1)$. The reduction below builds the $6 \times 4$ matrix whose column for $(x, y, z)$ has ones in rows $x$, $2 + y$ and $4 + z$, the syndrome $s = 111111$ and $w = 2$. The pattern $e = 1100$, which picks the disjoint triples $(0,0,0)$ and $(1,1,1)$, has $H e^T = s$, so the answer is yes. For the triples $(0,0,0)$, $(0,1,1)$, $(1,1,0)$ there is no perfect matching (the only triple with $x = 1$ shares $z = 0$ with the only triple with $y = 0$), and no $e$ of weight at most 2 has $H e^T = s$.

## Known algorithms

All exact algorithms for general linear codes take exponential time.

- **Search over codewords.** Compute $d(y, m G)$ for all $q^k$ messages: $O(q^k n k)$ time, or $O(q^k n)$ with a Gray code order.
- **Syndrome table.** [Syndrome decoding](/syndrome-decoding/) stores a least weight coset leader for each of the $q^{n-k}$ syndromes. After a build of up to $O(q^n n^2)$ time, each query costs $O(n^2)$. This is good when $n - k$ is small.
- **Search over error patterns.** Try all $e$ of weight $0, 1, 2, \ldots$ until $H e^T = s$. This takes $\sum_{i \le w} \binom{n}{i} (q - 1)^i$ syndrome tests, which is polynomial when $w$ is a constant.
- **Information set decoding.** Guess $k$ positions where $y$ has no error, re-encode, and check the weight. [Information set decoding](/information-set-decoding/) and its improvements (Prange, Lee-Brickell, Stern) are the fastest known methods for random codes, still exponential in $n$ for a fixed rate and a fixed error fraction.
- **Structured codes.** For Reed-Solomon, BCH, Reed-Muller and other algebraic codes, polynomial algorithms decode up to half the minimum distance and, with list decoding, beyond. They do not solve NCP for every $y$.

## Bounds

- **NP-complete.** The decision form is in NP, since a codeword $c$ with $d(y, c) \le w$ is a certificate that can be checked in polynomial time, and it is NP-hard by the reduction below (Berlekamp, McEliece and van Tilborg, 1978, for binary codes). Hence the search form is [NP-hard](/np-hard/).
- **Hard to approximate.** Arora, Babai, Stern and Sweedyk (1997) proved, for the optimization form of NCP over $\mathrm{GF}(2)$ (the minimum distance from $y$ to the code), that approximating it within any constant factor is NP-hard, and that approximating it within $2^{\log^{1 - \varepsilon} n}$ for any $\varepsilon > 0$ is not possible in polynomial time unless NP has quasi-polynomial time algorithms. Their proof goes through label cover and the PCP theorem. The theorem page [nearest codeword inapproximability](/nearest-codeword-inapproximability/) states it in full. Dinur, Kindler, Raz and Safra later raised the factor to $n^{1/O(\log \log n)}$ under the assumption P $\ne$ NP, as the survey in the paper of Dumer, Micciancio and Sudan reports.
- **Approximation algorithms.** Any codeword is within distance $n$ of $y$, and the distance is at least 1 unless $y$ is a codeword (which a syndrome test detects), so a factor $n$ is trivial. Berman and Karpinski gave, over every finite field, a factor $\varepsilon n / \log n$ in randomized polynomial time and $\varepsilon n$ in deterministic polynomial time, for each fixed $\varepsilon > 0$ (as reported by Dumer, Micciancio and Sudan).
- **Upper bound.** Exhaustive search gives $\min(q^k, q^{n-k}) \cdot \mathrm{poly}(n)$ time, so the problem is in exponential time.

## Reductions

**Three dimensional matching to coset weights (Berlekamp, McEliece and van Tilborg).** An instance of [three dimensional matching](/three-dimensional-matching/) has sets $X, Y, Z$ of $q$ elements each (here $q$ is the size, not a field) and a set $T$ of $t$ triples in $X \times Y \times Z$. It asks for $q$ triples that cover each element exactly once. Build:

- $H$: a $3q \times t$ binary matrix, with a column for each triple $(x, y, z)$ that has ones in the row of $x$, the row of $y$ and the row of $z$ and zeros elsewhere;
- $s = (1, 1, \ldots, 1)$ of length $3q$, and $w = q$.

*Claim.* $T$ has a perfect matching if and only if some $e$ with $\mathrm{wt}(e) \le q$ has $H e^T = s$ over $\mathrm{GF}(2)$.

*Proof.* If $M$ is a perfect matching, let $e$ be its indicator vector. Each row of $H$ meets exactly one column of $M$, so $H e^T = s$, and $\mathrm{wt}(e) = q$. Conversely, let $H e^T = s$ with $\mathrm{wt}(e) \le q$. Each of the $3q$ rows must meet an odd number, so at least one, of the chosen columns. The chosen columns have $3\, \mathrm{wt}(e) \le 3q$ ones in total. So each row meets exactly one chosen column, $\mathrm{wt}(e) = q$, and the chosen triples are disjoint and cover every element: a perfect matching. $\blacksquare$

The construction takes polynomial time, so COSET WEIGHTS is NP-complete, and by the equivalence of the forms, so is the decision NCP. The proof also shows that the exact weight version, $\mathrm{wt}(e) = q$, is NP-complete. The same paper shows that SUBSPACE WEIGHTS (is there a codeword of weight exactly $w$?) is NP-complete; the version with "at most $w$", which is the [minimum distance problem](/minimum-distance-problem/), stayed open until Vardy (1997).

**Other links.**

- NCP is the analog for codes of the [closest vector problem](/closest-vector-problem/) for lattices; Arora, Babai, Stern and Sweedyk treat both together.
- NCP is the problem of satisfying as many equations as possible in an overdetermined linear system $m G = y$ over $\mathrm{GF}(q)$: the unsatisfied equations are the positions where $m G \ne y$.
- NCP reduces to the minimum distance problem only in special ways; the hardness of the minimum distance problem needed new ideas (see that page).

## Applications

- **Limits of decoding.** The hardness results explain why practical codes are designed with structure (algebraic, sparse or recursive) that allows fast decoders, and why a decoder for an arbitrary linear code is exponential.
- **Code-based cryptography.** The McEliece and Niederreiter cryptosystems hide a structured code behind a random-looking generator matrix. Their security needs the average case problem, which the worst case results here motivate but do not prove.
- **Testing decoders.** Exact NCP solvers, by codeword search or syndrome tables, are reference decoders for small codes in tests and in simulations of block error rates.

## References
