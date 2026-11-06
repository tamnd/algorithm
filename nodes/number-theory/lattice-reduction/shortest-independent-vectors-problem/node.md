---
tag: T3MVE7
kind: problem
slug: shortest-independent-vectors-problem
name: Shortest independent vectors problem
aliases:
- SIVP
- approximate SIVP
- GapSIVP
area: number-theory/lattice-reduction
level: advanced
summary: Find n linearly independent lattice vectors minimizing the longest one.
prereqs: [successive-minima, shortest-vector-problem, lattice-basis]
see_also: [closest-vector-problem, gap-svp, lll-approximation-guarantee, minkowski-reduced-basis, short-integer-solution, learning-with-errors, ajtai-worst-case-to-average-case-reduction, dual-lattice]
sources:
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 7, Basis reduction problems (the successive minima problem, SIVP, the shortest basis problem, and the conversion of independent vectors into a basis)
  - paper: "J. Blömer and J.-P. Seifert, On the complexity of computing short linearly independent vectors and short bases in a lattice, STOC 1999"
    locator: the NP-hardness of SIVP and of the shortest basis problem, exactly and within factors n^(c/log log n)
  - paper: "D. Micciancio, Efficient reductions among lattice problems, SODA 2008"
    locator: the main theorem (approximating all successive minima within a factor reduces to CVP within the same factor, preserving the rank)
  - paper: "D. Micciancio and O. Regev, Worst-case to average-case reductions based on Gaussian measures, SIAM Journal on Computing 37(1) (2007)"
    locator: the main theorem (the average-case SIS problem is as hard as SIVP within factors of about n in the worst case)
  - paper: "D. Micciancio and P. Voulgaris, A deterministic single exponential time algorithm for most lattice problems based on Voronoi cell computations, STOC 2010"
    locator: the applications section (SVP, CVP and SIVP in deterministic time 2^(2n + o(n)))
---

The shortest independent vectors problem (SIVP) asks, for a lattice $L$ of rank $n$ given by a [basis](/lattice-basis/), for $n$ linearly independent lattice vectors whose longest member is as short as possible. The optimal value is the last [successive minimum](/successive-minima/) $\lambda_n(L)$, so SIVP is to $\lambda_n$ what the [shortest vector problem](/shortest-vector-problem/) is to $\lambda_1$. Its approximate version is the problem on which the worst-case security of [SIS](/short-integer-solution/) and [LWE](/learning-with-errors/) is based, and it is NP-hard exactly and within factors $n^{c / \log \log n}$.

## In plain words

A lattice is a regular grid of points, and a shortest vector is the nearest grid point to the origin. Here we want more: one short arrow for every direction of the space, pointing in genuinely different directions, so that no arrow is a combination of the others. Among all such choices we want the longest arrow to be as short as possible.

The answer need not be a set of arrows that rebuilds the whole grid; it only has to span all directions. Like the shortest vector question, this is easy in two dimensions and very hard in high dimension. Cryptographers care because breaking some lattice-based schemes on average would solve this problem in every lattice.

## Definition

**Notation.** As on all pages of this area: $b_1, \ldots, b_n \in \mathbb{R}^m$ are the rows of a basis $B$ of the lattice $L = L(B)$ of rank $n$, with Gram-Schmidt vectors $b_i^*$, coefficients $\mu_{ij}$, determinant $\det(L)$ and the LLL parameter $\delta$, and

$$\lambda_i(L) = \min\{ r : L \text{ has } i \text{ linearly independent vectors of length at most } r \}.$$

**SIVP (search).** *Input:* a basis $B$. *Output:* linearly independent $v_1, \ldots, v_n \in L$ with $\max_i \|v_i\| = \lambda_n(L)$. Such vectors exist by the greedy argument on the [successive minima](/successive-minima/) page.

**$\gamma$-SIVP.** For $\gamma \ge 1$, output linearly independent $v_1, \ldots, v_n \in L$ with $\max_i \|v_i\| \le \gamma \lambda_n(L)$. The factor $\gamma$ may depend on $n$.

**GapSIVP$_\gamma$.** A promise problem: given $(B, r)$, answer YES if $\lambda_n(L) \le r$ and NO if $\lambda_n(L) > \gamma r$.

Independence is over $\mathbb{R}$. The vectors $v_1, \ldots, v_n$ generate a sublattice of $L$ of finite index, which is often larger than 1, so the output is in general not a basis of $L$.

## Variants

- **Successive minima problem (SMP).** Output independent $v_1, \ldots, v_n$ with $\|v_i\| = \lambda_i(L)$ for every $i$, or within $\gamma \lambda_i$ in the approximate form. SMP implies SIVP with the same factor, since only $\lambda_n$ is compared.
- **Shortest basis problem (SBP).** Output a basis of $L$ minimizing $\max_i \|b_i\|$. Since a basis is a set of independent vectors, its optimum is at least $\lambda_n$; the example below shows that it can be larger.
- **Computing $\lambda_n$.** Output the value $\lambda_n(L)$, or $\lambda_n(L)^2$, which is rational for a rational basis.
- **Other norms.** SIVP in $\ell_p$ norms, defined the same way with the minima in that norm.
- **Generalized versions.** In the worst-case to average-case reductions, the target $\lambda_n$ is sometimes replaced by another lattice quantity of similar size, such as the smoothing parameter; the reductions solve that variant, which implies $\gamma$-SIVP for a slightly larger $\gamma$.

## Examples

- **$\mathbb{Z}^n$.** $\lambda_n = 1$, reached by the standard basis.
- **A three-dimensional lattice.** The basis $(1, 1, 1), (-1, 0, 2), (3, 5, 6)$ has $\max_i \|b_i\| = \sqrt{70}$, while $\lambda_1, \lambda_2, \lambda_3 = 1, \sqrt 2, \sqrt 5$ (checked by enumeration). So SIVP has the value $\sqrt 5$, reached by $(0, 1, 0), (1, 0, 1), (-2, 0, 1)$, which here is also a basis.
- **An LLL-reduced basis is not optimal.** The basis $(4, 0), (2, 3)$ is LLL-reduced with $\delta = 3/4$ and has $\max_i \|b_i\| = 4$. The shortest vectors are $\pm(2, 3)$ and $\pm(-2, 3)$, of length $\sqrt{13} \approx 3.61$, so $\lambda_1 = \lambda_2 = \sqrt{13}$ and $(2, 3), (-2, 3)$ solve SIVP.
- **Independent vectors that are not a basis.** Let $L = \mathbb{Z}^5 \cup (\mathbb{Z}^5 + h)$ with $h = (\frac12, \ldots, \frac12)$. Then $\lambda_5 = 1$, reached by $e_1, \ldots, e_5$, which generate $\mathbb{Z}^5$, a sublattice of index 2. Every basis of $L$ contains a vector of the coset $\mathbb{Z}^5 + h$, whose length is at least $\sqrt 5 / 2$; so the shortest basis problem has the value $\sqrt 5 / 2 > \lambda_5$, reached by $e_1, \ldots, e_4, h$.
- **Rank 1.** $\lambda_1 = \lambda_n$ and SIVP is the same as SVP.

## Known algorithms

Here $n$ is the rank; costs are numbers of arithmetic operations on numbers whose size is polynomial in the input size, unless stated otherwise.

- **Greedy over a list.** Enumerate all lattice vectors of length at most $R = \max_i \|b_i\|$ (a valid bound, since the basis is one candidate), sort them by length, and pick vectors greedily, keeping a vector when it is independent of those kept. This returns $v_1, \ldots, v_n$ with $\|v_i\| = \lambda_i$ for all $i$, by the matroid greedy argument on the [successive minima](/successive-minima/) page. The number of vectors can be exponential in $n$ and in the input size; after [LLL](/lll-algorithm/) it is $2^{O(n^2)}$.
- **LLL.** An LLL-reduced basis has $\|b_j\| \le \alpha^{(n-1)/2} \lambda_i$ for $j \le i$, with $\alpha = 1 / (\delta - 1/4)$ (the [LLL guarantee](/lll-approximation-guarantee/)). So the basis itself solves $\gamma$-SMP, and hence $\gamma$-SIVP, with $\gamma = 2^{(n-1)/2}$ for $\delta = 3/4$, in polynomial time; proved.
- **Block reduction.** [BKZ](/bkz-algorithm/) and its relatives improve the factor to $2^{O(n \log \log n / \log n)}$ in polynomial time and to $\beta^{O(n / \beta)}$ with SVP calls in dimension $\beta$.
- **Voronoi cell.** Micciancio and Voulgaris solve SIVP exactly in deterministic time $2^{2n + o(n)}$; proved.
- **Through CVP.** By Micciancio's reduction below, every CVP algorithm gives an SIVP algorithm in the same rank with the same factor. With the CVP algorithm of Aggarwal, Dadush and Stephens-Davidowitz this gives randomized time $2^{n + o(n)}$ for exact SIVP.

## Bounds

- **Elementary bounds.** For every basis, $\|b_n^*\| \le \lambda_n \le \max_i \|b_i\|$; the lower bound is the Gram-Schmidt bound $\lambda_i \ge \min_{j \ge i} \|b_j^*\|$ of the [successive minima](/successive-minima/) page with $i = n$.
- **Products.** [Minkowski's second theorem](/minkowski-second-theorem/) gives $\lambda_1 \cdots \lambda_n \le \gamma_n^{n/2} \det(L)$.
- **Transference.** For the [dual lattice](/dual-lattice/) $L^*$, $1 \le \lambda_1(L^*) \lambda_n(L) \le n$ (Banaszczyk, 1993). So a short dual vector certifies a lower bound on $\lambda_n$, which places GapSIVP within a factor $n$ in coNP.
- **Basis versus independent vectors.** From any independent $v_1, \ldots, v_n \in L$, sorted by length, one can compute in polynomial time a basis with $\|b_i\| \le \max(1, \sqrt i / 2) \|v_i\|$ (Micciancio and Goldwasser, Chapter 7). So SBP and SIVP differ by a factor of at most $\sqrt n / 2$, and the five-dimensional example above shows that this factor is reached for $n = 5$.
- **NP-hardness.** Blömer and Seifert (1999) proved that SIVP is NP-hard, and NP-hard to approximate within $n^{c / \log \log n}$ for some constant $c > 0$, by a deterministic reduction from CVP. These are hardness results under deterministic reductions, in contrast with the randomized ones known for [SVP](/svp-randomized-np-hardness/).
- **Limits on hardness.** GapSIVP within $\sqrt{n / \log n}$ is in coAM and within $\sqrt n$ is in coNP (Guruswami, Micciancio and Regev, 2004), so these factors are not NP-hard unless the polynomial hierarchy collapses.

## Reductions

- **CVP to SIVP.** Blömer and Seifert reduce CVP to SIVP, which transfers the NP-hardness of CVP.
- **SIVP and SMP to CVP.** Micciancio (2008) reduces $\gamma$-SMP, and so $\gamma$-SIVP, to $\gamma$-CVP by a deterministic reduction that keeps the rank and the factor. Together with the reduction above, exact SIVP and exact CVP are equivalent under rank-preserving reductions.
- **SVP to SIVP.** No reduction that keeps the factor is known in this direction; SVP and SIVP are related only through transference, which loses a factor about $n$.
- **Worst case to average case.** [Ajtai's reduction](/ajtai-worst-case-to-average-case-reduction/), improved by Micciancio and Regev, shows that solving the [short integer solution](/short-integer-solution/) problem on random instances solves $\gamma$-SIVP in every lattice for $\gamma = \tilde O(n)$. Regev's reduction for [learning with errors](/learning-with-errors/) solves $\gamma$-SIVP and GapSVP with $\gamma = \tilde O(n / \alpha)$ for the error rate $\alpha$, by a quantum algorithm.

## Applications

- **Security of lattice cryptography.** The worst-case guarantees of SIS and LWE based schemes are stated as the hardness of approximate SIVP within polynomial factors, which the best known algorithms solve only in time exponential in $n$.
- **Bounds in the geometry of numbers.** Short independent vectors bound the [covering radius](/covering-radius/), $\mu(L) \le \frac{\sqrt n}{2} \lambda_n(L)$, which is used to bound the error of [Babai's nearest plane](/babai-nearest-plane/) method and the cost of CVP.
- **Short bases from short vectors.** Trapdoor constructions and the reductions above produce short independent vectors and convert them into short bases with the conversion bound.

## References
