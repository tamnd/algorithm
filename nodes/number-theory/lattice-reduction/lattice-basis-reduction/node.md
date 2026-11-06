---
tag: ESZV2K
kind: problem
slug: lattice-basis-reduction
name: Lattice basis reduction
aliases:
- lattice reduction
- basis reduction
- reduction of a lattice basis
area: number-theory/lattice-reduction
level: intro
summary: Given a lattice basis, find a basis of short, nearly orthogonal vectors.
prereqs: [lattice, lattice-basis, gram-schmidt-orthogonalization, lattice-determinant]
see_also: [lll-algorithm, lagrange-gauss-reduction, bkz-algorithm, hkz-reduction, minkowski-reduced-basis, seysen-reduction, shortest-vector-problem, approximate-svp]
sources:
  - book: isbn:9783642261640
    title: Phong Q. Nguyen and Brigitte Vallée (editors), The LLL Algorithm, Survey and Applications, Springer, 2010
    locator: Chapter 2, Phong Q. Nguyen, Hermite's constant and lattice algorithms (the reduction notions of Hermite, Minkowski, HKZ, LLL and BKZ and the relations between them)
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 2, Approximation algorithms (the LLL algorithm), and Chapter 7, Basis reduction problems (the shortest basis problem and its hardness)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 17, Lattice basis reduction, and Chapter 18, Sections 18.4 to 18.5 (enumeration and BKZ)
  - paper: "A. K. Lenstra, H. W. Lenstra Jr. and L. Lovász, Factoring polynomials with rational coefficients, Mathematische Annalen 261 (1982)"
    locator: pages 515 to 534 (the definition of a reduced basis, the reduction algorithm and its use for factoring)
  - paper: "C. P. Schnorr, A hierarchy of polynomial time lattice basis reduction algorithms, Theoretical Computer Science 53 (1987)"
    locator: pages 201 to 224 (block reduction and the approximation factor 2^(O(n (log log n)^2 / log n)) in polynomial time)
  - paper: "J. Blömer and J.-P. Seifert, On the complexity of computing short linearly independent vectors and short bases in a lattice, STOC 1999"
    locator: pages 711 to 720 (NP-hardness of the shortest basis problem and of SIVP)
---

Lattice basis reduction is the problem of transforming a [basis](/lattice-basis/) of a [lattice](/lattice/) into another basis of the same lattice whose vectors are short and close to orthogonal. It is not one problem but a family: each **reduction notion** (size-reduced, [LLL-reduced](/lll-reduction/), [HKZ-reduced](/hkz-reduction/), [Minkowski-reduced](/minkowski-reduced-basis/), BKZ-reduced) is a set of conditions on the [Gram-Schmidt](/gram-schmidt-orthogonalization/) data of the output. The strong notions contain a [shortest vector](/shortest-vector-problem/) and are NP-hard to reach, while the [LLL algorithm](/lll-algorithm/) reaches a weaker notion in polynomial time. That polynomial-time reduction is one of the most used tools of computational number theory and cryptanalysis.

## In plain words

A lattice is a regular grid of points, and a basis is a set of arrows that builds the grid by adding and subtracting copies of the arrows. The same grid has many bases. Some use short arrows that point in clearly different directions. Others use long arrows that point in almost the same direction.

A good basis makes questions about the grid easy: the shortest arrow is close to the shortest grid step, and rounding in terms of the arrows lands near the nearest grid point. A bad basis hides all of this. Reduction starts from any basis and changes it, one step at a time, by adding whole multiples of one arrow to another and by swapping arrows. Each step keeps the grid the same. The goal is a basis of short arrows at nearly right angles.

## Definition

**Notation.** As on all pages of this area, the basis vectors $b_1, \ldots, b_n \in \mathbb{R}^m$ are the rows of $B$, $L = L(B)$, the Gram-Schmidt vectors are $b_i^*$, the coefficients are $\mu_{ij} = \langle b_i, b_j^* \rangle / \|b_j^*\|^2$, $\lambda_1 \le \cdots \le \lambda_n$ are the [successive minima](/successive-minima/), and $\det(L) = \prod_i \|b_i^*\|$ is the [determinant](/lattice-determinant/). For computation, $B$ has integer (or rational) entries, $\beta$ is the largest binary length of an entry, and the input size is about $n m \beta$.

**The problem.** A **reduction notion** $\mathcal{R}$ is a predicate on bases. The problem for $\mathcal{R}$ is:

- *Input:* a basis $B \in \mathbb{Z}^{n \times m}$ of rank $n$.
- *Output:* a basis $C$ with $C = U B$ for some $U \in \mathbb{Z}^{n \times n}$ with $\det U = \pm 1$, such that $C$ satisfies $\mathcal{R}$. The output may include $U$.

The condition $C = U B$ with $U$ [unimodular](/unimodular-matrix/) says that $C$ is a basis of the same lattice. Every reduction algorithm builds $U$ as a product of elementary steps: $b_i \leftarrow b_i - q b_j$ with $q \in \mathbb{Z}$, and swaps of two vectors.

**The main notions**, from weak to strong:

| notion | conditions on the output | what it gives |
|---|---|---|
| size-reduced | $\lvert \mu_{ij} \rvert \le 1/2$ for all $j < i$ | the $b_i$ are not much longer than the $b_i^*$ ([size reduction](/size-reduction/)) |
| $\delta$-LLL-reduced | size-reduced and $\delta \|b_{i-1}^*\|^2 \le \|b_i^*\|^2 + \mu_{i,i-1}^2 \|b_{i-1}^*\|^2$ ([Lovász condition](/lovasz-condition/)) | $\|b_1\| \le \alpha^{(n-1)/2} \lambda_1$, $\alpha = 1/(\delta - 1/4)$ |
| BKZ-$\beta$-reduced | size-reduced and each $b_i^*$ is a shortest vector of the projected block of $\beta$ vectors | quality between LLL and HKZ ([BKZ](/bkz-algorithm/)) |
| HKZ-reduced | size-reduced and each $b_i^*$ is a shortest vector of the projected lattice $\pi_i(L)$ | $\|b_1\| = \lambda_1$ ([HKZ](/hkz-reduction/)) |
| Minkowski-reduced | each $b_i$ is a shortest vector that extends $b_1, \ldots, b_{i-1}$ to a primitive set | $\|b_1\| = \lambda_1$ and $\|b_i\| \le c_n \lambda_i$ ([Minkowski](/minkowski-reduced-basis/)) |

Other notions measure the whole basis, such as the [Seysen measure](/seysen-reduction/) $\sum_i \|b_i\|^2 \|d_i\|^2$, where the $d_i$ are the dual basis vectors.

**Quality measures.** An algorithm is judged by measures of its output:

- the **approximation factor** $\|b_1\| / \lambda_1(L)$;
- the **Hermite factor** $\|b_1\| / \det(L)^{1/n}$, and its $n$-th root, the [root Hermite factor](/root-hermite-factor/);
- the **orthogonality defect** $\prod_i \|b_i\| / \det(L) \ge 1$, which is 1 exactly for an orthogonal basis;
- the ratios $\|b_i\| / \lambda_i(L)$, and $\max_i \|b_i\| / \lambda_n(L)$ for the shortest basis problem below.

## Variants

- **Reduction to a fixed notion.** Output a basis that satisfies $\mathcal{R}$. This is the form of LLL, BKZ, HKZ and Minkowski reduction.
- **Approximation of a measure.** Output a basis whose approximation factor or Hermite factor is at most $\gamma(n)$. With $\gamma = 1$ for the approximation factor this contains [SVP](/shortest-vector-problem/), and an approximate version is [approximate SVP](/approximate-svp/).
- **The shortest basis problem (SBP).** Output a basis that minimizes $\max_i \|b_i\|$, or approximates the minimum within $\gamma$. It is close to the [shortest independent vectors problem](/shortest-independent-vectors-problem/), but a basis is required, and the minimum can exceed $\lambda_n$ (see the example $\mathbb{Z}^5 \cup (\mathbb{Z}^5 + h)$ on the [basis](/lattice-basis/) page).
- **Generating sets.** The input is a list of $k > n$ vectors that may be dependent; the output is a reduced basis of the lattice they generate. The modified LLL of Pohst and the [Hermite normal form](/hermite-normal-form/) handle this case.
- **Gram matrix input.** The input is the Gram matrix $G = B B^T$ only, or a positive definite quadratic form; the output is $U$ such that $U G U^T$ is reduced. This is the classical reduction of quadratic forms of Lagrange, Gauss, Hermite and Minkowski.
- **Dimension 2.** Here all strong notions coincide, and [Lagrange-Gauss reduction](/lagrange-gauss-reduction/) solves the problem exactly in polynomial time.
- **Other norms.** Reduction in the $\ell_1$ or $\ell_\infty$ norm, or for a general norm given by a convex body, as in the generalized basis reduction of Lovász and Scarf.

## Examples

**Dimension 2.** The rows $(4, 4)$ and $(9, 10)$ have $\mu_{21} = 76 / 32 = 2.375$, and they generate a lattice of determinant 4. [Lagrange-Gauss reduction](/lagrange-gauss-reduction/) returns, after three iterations, the basis $(2, 0), (-1, 2)$, with $\mu_{21} = -1/2$, $\|b_1\| = 2 = \lambda_1$ and $\|b_2\| = \sqrt 5 = \lambda_2$. The orthogonality defect drops from $\sqrt{32 \cdot 181} / 4 \approx 19.0$ to $2 \sqrt 5 / 4 \approx 1.12$.

**Dimension 3.** Let $B$ have the rows $(1, 1, 1)$, $(-1, 0, 2)$ and $(3, 5, 6)$. Then $\det(L) = 3$, the squared Gram-Schmidt lengths are $3, 14/3, 9/14$, and $\prod_i \|b_i\| \approx 32.4$, an orthogonality defect of about 10.8. The [LLL algorithm](/lll-algorithm/) with $\delta = 3/4$ returns, after two swaps, the basis

$$(0, 1, 0), \quad (1, 0, 1), \quad (-2, 0, 1),$$

with squared Gram-Schmidt lengths $1, 2, 9/2$ (their product is still $9 = \det(L)^2$), $\mu_{32} = -1/2$ and all other $\mu_{ij} = 0$. Its orthogonality defect is $\sqrt{10} / 3 \approx 1.05$, and $b_1 = (0, 1, 0)$ is a shortest vector: an exhaustive search over a box of coefficients that is large enough finds no nonzero vector of squared length below 1.

**A non-example of progress.** Swapping two vectors, or replacing $b_i$ by $-b_i$, never changes the lattice, and neither does $b_i \leftarrow b_i + q b_j$. But replacing $b_i$ by $2 b_i$, or by $b_i + \tfrac12 b_j$, gives a different lattice: such a step is not allowed, even when it makes the vectors shorter or more orthogonal.

## Known algorithms

Costs are for an integer basis of rank $n$ in $\mathbb{Z}^m$ with entries of binary length $\beta$, and $\log B = O(\beta + \log m)$ bounds the binary length of the squared norms $\|b_i\|^2$.

- **[Lagrange-Gauss reduction](/lagrange-gauss-reduction/).** Rank 2, exact: returns $\lambda_1$ and $\lambda_2$ in $O(\beta)$ iterations; proved.
- **[Size reduction](/size-reduction/).** Makes $|\mu_{ij}| \le 1/2$ in $O(n^2 m)$ arithmetic operations; proved. It is a step inside all the algorithms below.
- **[LLL algorithm](/lll-algorithm/).** Outputs a $\delta$-LLL-reduced basis with $O(n^2 (\beta + \log m))$ swaps and $O(n^3 m (\beta + \log m))$ exact arithmetic operations on numbers of $O(n (\beta + \log m))$ binary digits; proved. The floating-point L² variant of Nguyen and Stehlé costs $O(n^4 m (n + \log B) \log B)$ bit operations with schoolbook multiplication; proved.
- **[Deep insertion LLL](/deep-lll/).** Stronger output in practice; no polynomial bound is proved for the unrestricted version.
- **[Seysen reduction](/seysen-reduction/).** A local search that lowers the Seysen measure of the basis and its dual; it terminates, but its termination proof gives only a bound that is exponential in the input size.
- **[BKZ](/bkz-algorithm/).** Block reduction with SVP calls in dimension $\beta$, each of cost $2^{O(\beta)}$ by sieving or $\beta^{O(\beta)}$ by enumeration. The number of tours is not proved polynomial for the standard version; the output quality $\delta_\beta^n$ in practice is a heuristic based on experiments.
- **[HKZ reduction](/hkz-reduction/).** $n$ calls to an exact SVP solver in decreasing dimensions, for example [Kannan's enumeration](/kannan-enumeration/) in $n^{O(n)}$ time; proved.
- **Minkowski reduction.** Exponential time in general; in dimensions up to 4 the greedy algorithm of Nguyen and Stehlé reaches it in quadratic time.

## Bounds

- **Polynomial-time upper bounds.** LLL gives approximation factor $(2/\sqrt 3 + \varepsilon)^{n-1}$ for $\delta$ close to 1, and $2^{(n-1)/2}$ for $\delta = 3/4$ (proved, see the [LLL guarantee](/lll-approximation-guarantee/)). Schnorr's block reduction (1987) reaches $2^{O(n (\log \log n)^2 / \log n)}$ in polynomial time. In practice LLL reaches a root Hermite factor of about 1.02 and BKZ-20 about 1.013 (Gama and Nguyen, 2008); these are observed values, not theorems.
- **Hardness.** Any notion whose output must contain a shortest vector (HKZ, Minkowski) is at least as hard as SVP, which is NP-hard under [randomized reductions](/svp-randomized-np-hardness/). Blömer and Seifert (1999) proved that the shortest basis problem is NP-hard to approximate within any constant factor. These results say that no polynomial-time algorithm reaches the strong notions unless NP has randomized polynomial-time algorithms (for the SVP-based ones) or P = NP (for SBP).
- **Existence.** Every lattice has a Minkowski-reduced and an HKZ-reduced basis, and so a basis with $\|b_1\| = \lambda_1$ and orthogonality defect at most a function of $n$ alone (Hermite, Minkowski). The hard part is to find one.

## Reductions

- **Reduction gives approximate SVP.** A basis with approximation factor $\gamma$ gives a $\gamma$-approximate shortest vector, namely $b_1$; so an algorithm for $\gamma$-reduction solves [$\gamma$-SVP](/approximate-svp/) at no extra cost.
- **SVP gives HKZ reduction.** With an exact SVP oracle, an HKZ-reduced basis is found with $n$ calls: find a shortest vector of $\pi_i(L)$ for $i = 1, \ldots, n$, lift it to $L$, and size-reduce. The lift needs care so that the vectors stay a basis; Kannan (1987) and Micciancio and Goldwasser give the details.
- **Reduction and CVP.** A reduced basis makes [Babai's nearest plane](/babai-nearest-plane/) method a $2^{O(n)}$-approximation for the [closest vector problem](/closest-vector-problem/) and shrinks the search tree of [enumeration](/lattice-enumeration/).

## Applications

- **Factoring polynomials over the rationals.** LLL was designed for this: [factoring a polynomial with integer coefficients](/polynomial-factorization-over-integers/) in polynomial time.
- **Integer programming in fixed dimension.** [Lenstra's algorithm](/lenstra-algorithm/) uses reduced bases to show that integer programming is polynomial when the number of variables is fixed.
- **Cryptanalysis.** Breaking [knapsack cryptosystems](/merkle-hellman-knapsack/), finding small roots by the [Coppersmith method](/coppersmith-method/), and estimating the security of [learning with errors](/learning-with-errors/) and [NTRU](/ntru-encrypt/) by the cost of BKZ.
- **Integer relations and Diophantine approximation.** Finding an [integer relation](/integer-relation-problem/) among real numbers and solving [simultaneous Diophantine approximation](/simultaneous-diophantine-approximation/); the [PSLQ algorithm](/pslq-algorithm/) is a relative of LLL for the first task.
- **Communications.** Lattice-reduction-aided detection for multiple-antenna channels reduces the channel basis before rounding.

## References
