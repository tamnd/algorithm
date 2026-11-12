---
tag: 9K8HSX
kind: problem
slug: minimum-distance-problem
name: Minimum distance problem
aliases:
- computing the minimum distance of a linear code
area: compression-and-coding/error-correcting-codes
level: advanced
summary: Given a generator matrix of a linear code and w, decide if some nonzero codeword has weight at most w. NP-hard (Vardy 1997) and hard to approximate (Dumer, Micciancio and Sudan 2003).
prereqs: [linear-code, minimum-distance, generator-matrix, np-hard]
see_also: [nearest-codeword-problem, parity-check-matrix, systematic-code, information-set-decoding, stern-algorithm, shortest-vector-problem, singleton-bound, griesmer-bound]
sources:
  - paper: doi:10.1109/18.641542
    title: Alexander Vardy, The intractability of computing the minimum distance of a code, IEEE Transactions on Information Theory 43(6), 1997, pages 1757 to 1766
    locator: The main theorem, NP-completeness of the minimum distance problem for binary linear codes
  - paper: doi:10.1109/TIT.2002.806118
    title: Ilya Dumer, Daniele Micciancio and Madhu Sudan, Hardness of approximating the minimum distance of a linear code, IEEE Transactions on Information Theory 49(1), 2003, pages 22 to 37
    locator: Abstract and Section 1 (no constant factor approximation in RP unless NP = RP, no additive approximation linear in n, and the factor 2^(log^(1 - ε) n) unless NP is in RQP, over every finite field)
  - paper: doi:10.1109/TIT.1978.1055873
    title: Elwyn R. Berlekamp, Robert J. McEliece and Henk C. A. van Tilborg, On the inherent intractability of certain coding problems, IEEE Transactions on Information Theory 24(3), 1978, pages 384 to 386
    locator: The problem Subspace Weights (a codeword of weight exactly w) and the conjecture that the minimum distance problem is NP-complete
  - paper: doi:10.1007/978-3-540-37634-7_13
    title: Markus Grassl, Searching for linear codes with large minimum distance, in Discovering Mathematics with Magma, Springer, 2006, pages 287 to 313
    locator: The minimum distance algorithm of Brouwer with disjoint information sets and its extension by Zimmermann with overlapping information sets
---

The minimum distance problem asks for the minimum distance of a [linear code](/linear-code/) given by a generator matrix, or, in its decision form, whether some nonzero codeword has weight at most a given $w$. The answer fixes how many errors the code can correct, so code designers compute it for every new code. Berlekamp, McEliece and van Tilborg conjectured in 1978 that the problem is NP-complete, and Vardy proved it in 1997. Exact algorithms enumerate codewords; the best practical one, due to Brouwer and Zimmermann, enumerates low weight messages over several information sets and stops early with a proof that no lighter codeword exists.

## In plain words

A code is described by a few basis words, and every valid word is a sum of some of them. The quality of the code is the number of nonzero symbols in its lightest valid word, other than the all zero word. The problem is to find that number.

The direct method lists every valid word, but their number doubles with each basis word. A smarter method writes the code in several forms, each with a different group of positions that carries the message. A light valid word must look light in at least one form, so trying light messages in every form finds it quickly, and the method can prove when to stop.

No method is fast for all codes. The problem is as hard as any problem in the class NP, and even a rough estimate within a fixed factor is hard.

## Definition

**Notation.** $C$ is an $[n, k, d]_q$ linear code over $\mathrm{GF}(q)$ with a $k \times n$ generator matrix $G$ ($c = m G$) and an $(n - k) \times n$ parity-check matrix $H$ ($H c^T = 0$). Vectors are rows. $\mathrm{wt}$ is the Hamming weight. For a linear code, the [minimum distance](/minimum-distance/) equals the least weight of a nonzero codeword.

**Search form.** Input: $G$. Output: $d = \min \{\, \mathrm{wt}(m G) : m \in \mathrm{GF}(q)^k,\ m \ne 0 \,\}$, and a codeword of that weight.

**Decision form (MINIMUM DISTANCE).** Input: $G$ (or $H$) and an integer $w > 0$. Question: is there a nonzero codeword $c$ with $\mathrm{wt}(c) \le w$?

**Column form.** By the theorem on the [parity-check matrix](/parity-check-matrix/) page, the same question is: are some $w$ or fewer columns of $H$ linearly dependent? Over $\mathrm{GF}(2)$: is there a nonempty set of at most $w$ columns of $H$ that adds to zero? In parameterized complexity this binary form is called Even Set.

The problem is not a decoding problem: there is no received word. It is the homogeneous version of the [nearest codeword problem](/nearest-codeword-problem/), where the target is the zero word and the zero codeword itself is excluded.

## Variants

- **Exact weight (SUBSPACE WEIGHTS).** Is there a codeword of weight exactly $w$? Berlekamp, McEliece and van Tilborg proved this NP-complete in 1978 by a reduction from three dimensional matching. Their proof did not cover "at most $w$", the minimum distance itself.
- **Approximation.** Output a value between $d$ and $\gamma d$, for a factor $\gamma \ge 1$, or between $d$ and $d + \delta n$ for an additive error.
- **Over larger fields.** The input is a code over $\mathrm{GF}(q)$ for a fixed $q$, or a code over a field that grows with $n$.
- **Weight distribution.** Count the codewords of each weight $w$. The [MacWilliams identity](/macwilliams-identity/) transfers it to the dual code, so one can enumerate whichever of $C$ and $C^\perp$ is smaller.
- **Low weight search.** Find some light codeword quickly, without proof that it is the lightest. Probabilistic methods of the information set type, such as [Stern's algorithm](/stern-algorithm/), do this for long codes.
- **Lattices.** The analog for lattices is the [shortest vector problem](/shortest-vector-problem/), and Dumer, Micciancio and Sudan adapt a hardness proof for it.

## Examples

- **Hamming code.** The $[7, 4]$ [Hamming code](/hamming-code/) has $15$ nonzero codewords: seven of weight 3, seven of weight 4 and one of weight 7, so $d = 3$. In the column form, columns $110$, $011$ and $101$ of its parity-check matrix add to zero, and no two columns do.
- **A [5, 2] code.** With generator rows $10110$ and $01011$, the three nonzero codewords are $10110$, $01011$ and $11101$, of weights 3, 3 and 4, so $d = 3$.
- **Golay code.** The extended binary Golay code is a $[24, 12, 8]$ code. Plain enumeration computes all $2^{12} - 1 = 4095$ nonzero codewords. Brouwer's algorithm (below) finds two disjoint information sets, positions that each carry the message in some generator matrix, since $24 = 2 \cdot 12$. It enumerates the messages of weight 1, 2 and 3 for both matrices, $2 \cdot (12 + 66 + 220) = 596$ codewords. After weight 3, every codeword not yet seen has weight at least 4 on each information set, so at least $2 \cdot 4 = 8$ in total. The lightest codeword seen has weight 8, so the algorithm stops with $d = 8$.

## Known algorithms

**Plain enumeration.** Compute $\mathrm{wt}(m G)$ for all $q^k - 1$ nonzero messages, or for one message from each line through the origin, $(q^k - 1)/(q - 1)$ of them, since scalar multiples have the same weight. Time $O(q^k n k)$, or $O(q^k n)$ with a Gray code order that adds one row at a time. The dual form tries the column subsets of $H$ of size $1, 2, \ldots$, which costs $\sum_{i \le w} \binom{n}{i}$ rank tests and is good when $d$ is small.

**Brouwer's algorithm.** An information set $I$ is a set of $k$ positions on which $G$ can be made systematic, $G_I = I_k$ (see [systematic code](/systematic-code/)). With $G$ in that form, the codeword $m G$ restricted to $I$ is $m$ itself, so its weight on $I$ is $\mathrm{wt}(m)$.

1. Find $s$ pairwise disjoint information sets $I_1, \ldots, I_s$ by Gaussian elimination, each time only on columns not used before, and for each a generator matrix $G_j$ systematic on $I_j$.
2. For $w = 1, 2, \ldots, k$: for each $j$, compute $m G_j$ for all messages $m$ of weight $w$ (with the first nonzero entry 1), and keep the least codeword weight $\hat d$ seen so far.
3. After round $w$, each codeword not yet computed has weight at least $w + 1$ on every $I_j$, so weight at least $s (w + 1)$. If $\hat d \le s (w + 1)$, stop: $d = \hat d$.

The cost is about $s \sum_{i \le \bar w} \binom{k}{i} (q - 1)^{i - 1}$ codewords, where $\bar w$ is about $d/s$, far less than $q^k$ for good codes.

**Zimmermann's extension.** When $n$ is not a multiple of $k$, or when the columns outside the disjoint sets also have rank, Zimmermann uses overlapping information sets. For each generator matrix he counts only the rank on the positions not covered by the earlier ones, a relative rank, and gets a lower bound that grows faster with $w$. This Brouwer-Zimmermann algorithm is the standard exact method in computer algebra systems such as Magma, as Grassl describes.

**Probabilistic searches.** Leon's and Stern's algorithms guess an information set and search for codewords with few nonzero entries on it. They find light codewords in long codes quickly, but they do not prove that no lighter codeword exists.

The implementation of this page has the plain enumeration and Brouwer's algorithm with disjoint information sets, and checks that they agree on known codes and on random codes over $\mathrm{GF}(2)$, $\mathrm{GF}(3)$ and $\mathrm{GF}(5)$.

## Bounds

- **NP-complete.** The decision form is in NP (a codeword of weight at most $w$ is a certificate), and Vardy (1997) proved it NP-hard for binary linear codes. So the minimum distance of a binary linear code cannot be computed in polynomial time unless P = NP. This settled the conjecture of Berlekamp, McEliece and van Tilborg.
- **Hard to approximate.** Dumer, Micciancio and Sudan (2003) proved, for codes over any finite field, including binary codes: the minimum distance cannot be approximated within any constant factor in random polynomial time unless NP = RP; it cannot be approximated within an additive error linear in $n$ under the same assumption; and it cannot be approximated within the factor $2^{\log^{1 - \varepsilon} n}$, for any $\varepsilon > 0$, unless NP is contained in random quasi-polynomial time (RQP). Later work by Cheng and Wan, and by Austrin and Khot, gave deterministic reductions.
- **Exact algorithms.** Plain enumeration gives $O(q^{\min(k, n - k)} \mathrm{poly}(n))$ by working on $C$ or on its dual.
- **Bounds on the answer.** The [Singleton](/singleton-bound/), Hamming, Plotkin and [Griesmer](/griesmer-bound/) bounds give upper bounds on $d$ from $n$, $k$ and $q$. They do not compute $d$ for a given code, but they tell a search when it can stop early, and a code that meets a bound has a known $d$.

## Reductions

- **To the minimum distance problem.** The hard problems known in 1978, exact weight and the coset weights form of the [nearest codeword problem](/nearest-codeword-problem/), are inhomogeneous: they ask about a given weight or a given coset. A reduction to the minimum distance problem must encode such a question in a homogeneous one, a light codeword of $C$, without letting new light codewords appear. This is why the conjecture stayed open for nineteen years until Vardy's proof.
- **To the nearest codeword problem.** $d$ is the least, over positions $i$ and nonzero values, of the distance from a word to a subcode: for binary codes, $d = \min_i \min \{\, \mathrm{wt}(c) : c \in C,\ c_i = 1 \,\}$, and each inner problem is a nearest codeword problem for the subcode with $c_i = 0$ and a target $y$ from $C$ with $y_i = 1$. So a polynomial algorithm for the nearest codeword problem would give one for the minimum distance.
- **Lattices.** Dumer, Micciancio and Sudan adapt Micciancio's proof for the shortest vector problem; the two problems are analogs.

## Applications

- **Tables of codes.** Tables of the best known linear codes, such as the one Grassl maintains, list for each $n$ and $k$ a code and its minimum distance; each entry needs an exact computation or a proof, usually by the Brouwer-Zimmermann algorithm.
- **Code design.** A designer who builds a code by computer search, or who shortens or punctures a known code, must compute $d$ to know what the code corrects.
- **Cryptanalysis.** In code-based cryptography, a codeword of unusually low weight in a public code, or in its dual, can reveal the hidden structure, so low weight searches are part of the analysis.
- **LDPC codes.** The minimum distance of an LDPC code limits its error rate at high signal to noise ratio; estimating it for long codes uses the probabilistic searches above.

## References
