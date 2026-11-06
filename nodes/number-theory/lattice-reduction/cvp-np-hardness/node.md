---
tag: DEAQ1Y
kind: theorem
slug: cvp-np-hardness
name: NP-hardness of CVP
aliases:
- van Emde Boas result
- NP-completeness of the closest vector problem
- CVP is NP-hard
area: number-theory/lattice-reduction
level: advanced
summary: The closest vector problem is NP-hard, shown by van Emde Boas in 1981.
prereqs: [closest-vector-problem, subset-sum-problem, np-complete]
see_also: [svp-randomized-np-hardness, gap-svp, bounded-distance-decoding, approximate-svp, babai-nearest-plane, shortest-vector-problem, np-hard, knapsack-problem]
sources:
  - paper: "P. van Emde Boas, Another NP-complete partition problem and the complexity of computing short vectors in a lattice, Technical Report 81-04, Mathematisch Instituut, Universiteit van Amsterdam (1981)"
    locator: the NP-completeness of CVP in the Euclidean and other norms, and of SVP in the max norm
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 3, Closest vector problem (NP-completeness by a reduction from subset sum, and the inapproximability results)
  - paper: "S. Arora, L. Babai, J. Stern and Z. Sweedyk, The hardness of approximate optima in lattices, codes, and systems of linear equations, Journal of Computer and System Sciences 54(2) (1997)"
    locator: pages 317 to 331 (NP-hardness of approximating CVP within any constant)
  - paper: "I. Dinur, G. Kindler, R. Raz and S. Safra, Approximating CVP to within almost-polynomial factors is NP-hard, Combinatorica 23(2) (2003)"
    locator: pages 205 to 243 (the factor n^(c / log log n))
---

## Statement

Notation is that of the other pages in this area: basis rows $b_1, \ldots, b_n$, $L(B) = \{x B : x \in \mathbb{Z}^n\}$, and $\operatorname{dist}(t, L) = \min_{v \in L} \|t - v\|$ in the Euclidean norm.

**Theorem (van Emde Boas, 1981).** The decision problem

> **CVP.** Given an integer matrix $B \in \mathbb{Z}^{n \times m}$ with independent rows, a target $t \in \mathbb{Z}^m$ and an integer $R$, is $\operatorname{dist}(t, L(B))^2 \le R$?

is NP-complete. The same holds in every $\ell_p$ norm, $1 \le p \le \infty$. Hence the search problem, finding a closest vector, is NP-hard.

The reduction is deterministic (a Karp reduction), so no randomization or approximation factor enters: this is exact CVP. The theorem does not say anything about approximation factors; those need the stronger results under Consequences.

## In plain words

Some problems are so general that a fast method for them would give fast methods for thousands of other hard problems. The claim here is that finding the grid point nearest to a given point, in a grid described by a list of arrows, is such a problem.

The proof hides a puzzle inside a grid. The puzzle is: given some numbers, choose a few of them that add up to a target. Each number becomes an arrow, and the arrows are arranged so that grid points close to the target point must use each arrow zero times or once, and must make the chosen numbers add up exactly. So the nearest grid point is close enough exactly when the puzzle has an answer, and a fast nearest point method would solve the puzzle fast.

## Proof

The proof has two parts: CVP is in NP, and the NP-complete [subset sum problem](/subset-sum-problem/) reduces to it.

**Subset sum.** Given positive integers $a_1, \ldots, a_n$ and $s$, decide whether there is $x \in \{0, 1\}^n$ with $\sum_i x_i a_i = s$. Karp proved it NP-complete, with the numbers written in binary.

**The reduction.** From $(a_1, \ldots, a_n, s)$ build, in time polynomial in the input size, the vectors in $\mathbb{Z}^{n+1}$

$$b_i = (a_i, 2 e_i) = (a_i, 0, \ldots, 0, 2, 0, \ldots, 0), \qquad t = (s, 1, 1, \ldots, 1), \qquad R = n,$$

where $e_i$ is the $i$-th unit vector of $\mathbb{Z}^n$. The rows $b_i$ are independent because of the block $2 I_n$.

For an integer vector $x$, the lattice vector $x B$ is $(\sum_i x_i a_i, 2x_1, \ldots, 2x_n)$, so

$$\|t - x B\|^2 = \Big(s - \sum_i x_i a_i\Big)^2 + \sum_{i=1}^n (1 - 2 x_i)^2.$$

**Lemma.** For every $x \in \mathbb{Z}^n$, $\|t - x B\|^2 \ge n$, with equality if and only if $x \in \{0, 1\}^n$ and $\sum_i x_i a_i = s$.

*Proof.* Each $1 - 2 x_i$ is an odd integer, so $(1 - 2x_i)^2 \ge 1$, with equality if and only if $x_i \in \{0, 1\}$. The first term is at least 0, with equality if and only if $\sum_i x_i a_i = s$. Adding the $n + 1$ terms gives $\ge n$, and equality forces equality in every term. $\square$

**Correctness of the reduction.** If the subset sum instance has a solution $x \in \{0, 1\}^n$, then $\|t - x B\|^2 = n$, so $\operatorname{dist}(t, L)^2 \le R$. If $\operatorname{dist}(t, L)^2 \le n$, the minimum is attained by some $x \in \mathbb{Z}^n$ with $\|t - x B\|^2 \le n$; by the lemma, $\|t - xB\|^2 = n$ and $x$ is a solution. So the subset sum instance is a YES instance if and only if the CVP instance is.

**CVP is in NP.** A certificate is the coefficient vector $x$ of a lattice vector $v = x B$ with $\|t - v\|^2 \le R$. It has polynomial size: $\|v\| \le \|t\| + \sqrt R$, and $x_i = \langle v, d_i \rangle$ where $d_i$ are the rows of the [dual basis](/dual-lattice/) $D = (B B^T)^{-1} B$, whose entries are rationals of size polynomial in that of $B$ by Cramer's rule. So $|x_i| \le (\|t\| + \sqrt R) \|d_i\|$, an integer of polynomially many digits. Checking the certificate is a matrix-vector product and a comparison.

Both parts together prove that CVP is NP-complete. A polynomial algorithm for the search problem would decide CVP by computing a closest vector and comparing its distance with $R$, so the search problem is NP-hard. $\blacksquare$

**Other norms.** For $1 \le p < \infty$ the same construction works with $R = n$ for $\|\cdot\|_p^p$: each term $|1 - 2x_i|^p \ge 1$ with the same equality case. For $\ell_\infty$, replace the first coordinate $a_i$ by $2 a_i$ and $s$ by $2 s$, and take radius 1: $\|t - xB\|_\infty \le 1$ forces every $1 - 2x_i = \pm 1$ and $|2s - 2\sum x_i a_i| \le 1$, hence $\sum x_i a_i = s$.

**A worked instance.** For $a = (3, 5, 7)$ and $s = 12$, the basis rows are $(3, 2, 0, 0)$, $(5, 0, 2, 0)$, $(7, 0, 0, 2)$ and $t = (12, 1, 1, 1)$. The solution $x = (0, 1, 1)$ gives $x B = (12, 0, 2, 2)$ and $t - x B = (0, 1, -1, -1)$, of squared length $3 = n$. For $s = 11$, which no subset reaches (the subset sums are $0, 3, 5, 7, 8, 10, 12, 15$), the squared distance is 4, attained again at $x = (0, 1, 1)$, which misses the sum by 1.

## Consequences

- **Exact CVP has no polynomial algorithm unless P = NP.** This holds for the search, optimization and decision versions, and with a deterministic reduction.
- **Integer least squares.** The problem $\min_{x \in \mathbb{Z}^n} \|A x - y\|$ of GPS ambiguity resolution and communications is CVP, so it is NP-hard in general.
- **Hardness of approximation.** The theorem gives no gap: the NO instances above have squared distance $\ge n + 1$, a factor only $\sqrt{1 + 1/n}$ above the YES case. Arora, Babai, Stern and Sweedyk (1997) used probabilistically checkable proofs to show that CVP$_\gamma$ is NP-hard for every constant $\gamma$, and Dinur, Kindler, Raz and Safra (2003) reached $\gamma = n^{c / \log \log n}$, still with deterministic reductions.
- **SVP.** Van Emde Boas proved the shortest vector problem NP-hard in the $\ell_\infty$ norm and conjectured it for $\ell_2$. For $\ell_2$ it was proved by Ajtai (1998) only under randomized reductions; see [SVP NP-hardness](/svp-randomized-np-hardness/). CVP is the easier of the two to prove hard because the target $t$ can encode the right-hand side $s$.
- **CVP with preprocessing.** Even with arbitrary advice about the lattice, CVP stays NP-hard (Micciancio, 2001), so the hardness does not come only from a bad basis.

## Tightness

- **Fixed dimension.** For fixed $n$, CVP is solvable in polynomial time, for example by [Kannan's enumeration](/kannan-enumeration/) in $n^{O(n)}$ operations times a polynomial in the input size. The hardness needs the dimension to grow with the input.
- **Approximation limits.** GapCVP$_{\sqrt{n / \log n}}$ is in NP $\cap$ coAM and GapCVP$_{\sqrt n}$ is in NP $\cap$ coNP, so CVP within those factors is not NP-hard unless the polynomial hierarchy collapses. The gap between the hardness factor $n^{c / \log \log n}$ and $\sqrt n$ is open.
- **Polynomial-time approximation.** [Babai's nearest plane method](/babai-nearest-plane/) on an [LLL](/lll-algorithm/)-reduced basis approximates CVP within $2^{n/2}$, so exponential factors are easy.
- **Number sizes.** The reduction above uses the numbers $a_i$ in binary, and subset sum is solvable in time polynomial in $n$ and $s$. Reductions from exact cover give instances with entries in $\{0, 1\}$, so CVP stays NP-hard when all entries are bounded by a constant.
- **Promise versions.** When the target is within $\alpha \lambda_1$ with $\alpha$ small, the problem is [bounded distance decoding](/bounded-distance-decoding/), known to be NP-hard only for $\alpha > 1/\sqrt2$.

## History

Peter van Emde Boas proved the theorem in a 1981 technical report, at the time when Lenstra's integer programming algorithm in fixed dimension and lattice basis reduction were new; the report also showed SVP NP-hard in the max norm. The decades after built hardness of approximation on it: Arora, Babai, Stern and Sweedyk in 1997 with PCP methods, and Dinur, Kindler, Raz and Safra in 2003. Micciancio and Goldwasser's book of 2002 gives the subset sum reduction used here.

## References
