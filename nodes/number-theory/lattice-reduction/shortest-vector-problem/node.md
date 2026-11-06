---
tag: T265CW
kind: problem
slug: shortest-vector-problem
name: Shortest vector problem
aliases:
- SVP
- shortest lattice vector problem
- exact SVP
area: number-theory/lattice-reduction
level: intro
summary: Given a lattice, find a nonzero lattice vector of minimum Euclidean length.
prereqs: [lattice, lattice-basis, gram-schmidt-orthogonalization]
see_also: [closest-vector-problem, approximate-svp, gap-svp, unique-svp, svp-randomized-np-hardness, lll-algorithm, lattice-enumeration, lattice-sieving]
sources:
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 1 (definitions of SVP and its variants), Chapter 2 (the LLL algorithm as an approximation algorithm), and Chapter 4, Shortest vector problem (randomized NP-hardness within factors below the square root of 2)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 18, Algorithms for the closest and shortest vector problems (enumeration in Section 18.5)
  - paper: "M. Ajtai, The shortest vector problem in L2 is NP-hard for randomized reductions, STOC 1998"
    locator: pages 10 to 19 (the first NP-hardness result for SVP in the Euclidean norm)
  - paper: "D. Micciancio, The shortest vector problem is NP-hard to approximate to within some constant, SIAM Journal on Computing 30(6) (2001)"
    locator: pages 2008 to 2035 (randomized NP-hardness within any factor below the square root of 2)
  - paper: "S. Khot, Hardness of approximating the shortest vector problem in lattices, Journal of the ACM 52(5) (2005)"
    locator: pages 789 to 808 (randomized NP-hardness within every constant factor)
  - paper: "I. Haviv and O. Regev, Tensor-based hardness of the shortest vector problem to within almost polynomial factors, Theory of Computing 8 (2012)"
    locator: pages 513 to 531 (hardness within 2^((log n)^(1 - epsilon)) under a quasi-polynomial randomized reduction)
  - paper: "M. Ajtai, R. Kumar and D. Sivakumar, A sieve algorithm for the shortest lattice vector problem, STOC 2001"
    locator: pages 601 to 610 (the first randomized 2^(O(n)) time algorithm)
  - paper: "D. Aggarwal, D. Dadush, O. Regev and N. Stephens-Davidowitz, Solving the shortest vector problem in 2^n time via discrete Gaussian sampling, STOC 2015"
    locator: the main theorem (randomized exact SVP in time and space 2^(n + o(n)))
---

The shortest vector problem (SVP) asks, for a [lattice](/lattice/) $L$ given by a [basis](/lattice-basis/), for a nonzero vector $v \in L$ of the smallest Euclidean length $\lambda_1(L)$. It is the central problem of the geometry of numbers in algorithmic form. In dimension 2 it is solved exactly by [Lagrange-Gauss reduction](/lagrange-gauss-reduction/); in general it is NP-hard under [randomized reductions](/svp-randomized-np-hardness/), and the best exact algorithms take time $2^{\Theta(n)}$ or more in the rank $n$. The [LLL algorithm](/lll-algorithm/) finds a vector within a factor $2^{(n-1)/2}$ of the shortest in polynomial time, and the cost of approximating SVP within polynomial factors is what the security of [lattice-based cryptography](/lattice-based-cryptography/) rests on.

## In plain words

A lattice is a regular grid of points in space, built from a few arrows by adding and subtracting them. The origin is one of the points. The question is: which other grid point is nearest to the origin?

If the arrows are short and at right angles, one of them is the answer. If they are long and point in almost the same direction, the nearest point can be a combination of many arrows with large multiples that cancel out, and nothing in the description shows it. In two dimensions a short loop finds it. In hundreds of dimensions there are far too many combinations to try, and the best known methods take time that grows exponentially with the dimension.

## Definition

**Notation.** As on all pages of this area: $b_1, \ldots, b_n \in \mathbb{R}^m$ are the rows of $B$, $L = L(B) = \{x B : x \in \mathbb{Z}^n\}$, the Gram-Schmidt vectors are $b_i^*$, $\|\cdot\|$ is the Euclidean norm, and

$$\lambda_1(L) = \min\{\|v\| : v \in L, v \ne 0\}.$$

The minimum exists because $L$ is discrete: every ball contains finitely many lattice points. For computation the entries of $B$ are integers or rationals, and the input size is the total number of binary digits of $B$.

**Search SVP.** *Input:* a basis $B$. *Output:* $v \in L(B)$ with $v \ne 0$ and $\|v\| = \lambda_1(L)$, given as the vector or as its coefficients $x \in \mathbb{Z}^n$ with $v = x B$. The answer is never unique, since $-v$ is also a solution.

**A box that contains a solution.** Let $D = (B B^T)^{-1} B$ be the dual basis, so the coefficients of $v \in L$ are $x_i = \langle v, d_i \rangle$. By the Cauchy-Schwarz inequality, $|x_i| \le \|v\| \|d_i\|$, and $\|d_i\|^2 = (G^{-1})_{ii}$ for the Gram matrix $G = B B^T$. With $R = \min_i \|b_i\| \ge \lambda_1$, every shortest vector has coefficients with $x_i^2 \le R^2 (G^{-1})_{ii}$. So exhaustive search over this box solves SVP exactly; the box is finite but can be huge for a bad basis. This is the brute-force check used to test the implementations on these pages.

## Variants

- **Optimization.** Output $\lambda_1(L)$, or $\lambda_1(L)^2$, which is rational for a rational basis.
- **Decision.** Given also $r > 0$, decide whether $\lambda_1(L) \le r$. For exact SVP, search reduces to decision in polynomial time (Kannan).
- **[Approximate SVP](/approximate-svp/) ($\gamma$-SVP).** For $\gamma \ge 1$, output a nonzero $v \in L$ with $\|v\| \le \gamma \lambda_1(L)$.
- **[GapSVP$_\gamma$](/gap-svp/).** A promise problem: given $(B, r)$, answer YES if $\lambda_1(L) \le r$ and NO if $\lambda_1(L) > \gamma r$. Hardness results are usually proved for this version.
- **Hermite SVP.** Output a nonzero $v$ with $\|v\| \le \gamma \det(L)^{1/n}$. Its factor is measured by the [root Hermite factor](/root-hermite-factor/), and it is the form that LLL and BKZ guarantee most directly.
- **[Unique SVP](/unique-svp/) (uSVP$_\gamma$).** The lattice is promised to have $\lambda_2(L) > \gamma \lambda_1(L)$, so the shortest vector is unique up to sign.
- **Other norms.** SVP in the $\ell_p$ norm, in particular $\ell_\infty$, where van Emde Boas proved NP-hardness in 1981.
- **Many short vectors.** Find all shortest vectors, or $n$ independent short vectors: the [shortest independent vectors problem](/shortest-independent-vectors-problem/) and the [successive minima](/successive-minima/).

## Examples

- **$\mathbb{Z}^n$.** $\lambda_1 = 1$, reached by the $2n$ vectors $\pm e_i$.
- **The hexagonal lattice** with rows $(1, 0)$ and $(1/2, \sqrt 3 / 2)$: $\lambda_1 = 1$, reached by 6 vectors.
- **$D_4 = \{x \in \mathbb{Z}^4 : x_1 + \cdots + x_4 \text{ even}\}$**: $\lambda_1 = \sqrt 2$, reached by the 24 vectors with two entries $\pm 1$ and two entries 0. The lattice $E_8$ has 240 vectors of the minimum length $\sqrt 2$ (Conway and Sloane, Chapter 4).
- **A hidden short vector.** Let $B$ have the rows $(1, 1, 1)$, $(-1, 0, 2)$ and $(3, 5, 6)$, of lengths $\sqrt 3$, $\sqrt 5$ and $\sqrt{70}$. The box bound above, with $R^2 = 3$, limits the search to finitely many coefficient vectors, and the search finds $\lambda_1 = 1$, reached only by $\pm (0, 1, 0) = \pm(-4 b_1 - b_2 + b_3)$. The [LLL algorithm](/lll-algorithm/) finds this vector as the first vector of its output.
- **Rank 1.** For $L = \mathbb{Z} b$, $\lambda_1 = \|b\|$; the problem is trivial.
- **A non-example of a method.** Taking the shortest vector of the given basis, or the shortest $b_i^*$, does not solve SVP. In the example above, the shortest basis vector has length $\sqrt 3$, and the shortest Gram-Schmidt vector has length $\sqrt{9/14} \approx 0.80$, which is below $\lambda_1 = 1$ and is not a lattice vector. The bound $\lambda_1 \ge \min_i \|b_i^*\|$ always holds but is usually strict.

## Known algorithms

Here $n$ is the rank. Exact algorithms work on rational numbers whose size stays polynomial in the input size; the costs below are numbers of arithmetic operations, up to factors polynomial in the input size.

- **[Lagrange-Gauss reduction](/lagrange-gauss-reduction/).** Exact in rank 2, polynomial time; proved.
- **[LLL algorithm](/lll-algorithm/).** Polynomial time, factor $2^{(n-1)/2}$ for $\delta = 3/4$ and $(2 / \sqrt 3 + \varepsilon)^{n-1}$ for $\delta$ near 1; proved (see the [LLL guarantee](/lll-approximation-guarantee/)). In practice the factor is far smaller.
- **[BKZ](/bkz-algorithm/).** Block size $\beta$ gives factor about $\beta^{O(n/\beta)}$, at the cost of SVP calls in dimension $\beta$. The quality in practice is predicted by heuristics and experiments, not by theorems.
- **Enumeration.** [Fincke-Pohst](/fincke-pohst-enumeration/) and [Schnorr-Euchner](/schnorr-euchner-enumeration/) enumeration search a tree over the coefficients; on an LLL-reduced basis the time is $2^{O(n^2)}$, proved. [Kannan's algorithm](/kannan-enumeration/) first reduces the basis more strongly and takes $n^{n/(2e) + o(n)}$ time with polynomial space (bound of Hanrot and Stehlé). See [lattice enumeration](/lattice-enumeration/).
- **Sieving.** The [AKS sieve](/lattice-sieving/) solves SVP in randomized time and space $2^{O(n)}$, proved. Heuristic sieves run in time about $2^{0.415 n}$ (the sieve of Nguyen and Vidick; the [Gauss sieve](/gauss-sieve/) is a practical relative), and with locality-sensitive filters about $2^{0.292 n + o(n)}$, under heuristic assumptions confirmed by experiments.
- **Voronoi cell.** Micciancio and Voulgaris solve SVP deterministically in time $2^{2n + o(n)}$, proved.
- **Discrete Gaussian sampling.** Aggarwal, Dadush, Regev and Stephens-Davidowitz solve SVP in randomized time and space $2^{n + o(n)}$, the best proved bound.

## Bounds

- **Existence of short vectors.** $\lambda_1(L) \le \sqrt{\gamma_n} \det(L)^{1/n} \le \sqrt n \det(L)^{1/n}$, where $\gamma_n$ is the [Hermite constant](/hermite-constant/); this follows from [Minkowski's theorem](/minkowski-theorem/).
- **NP-hardness, exact.** Van Emde Boas (1981) proved that SVP in $\ell_\infty$ is NP-hard and asked about $\ell_2$. Ajtai (1998) proved that SVP in $\ell_2$ is NP-hard under **randomized** polynomial-time reductions: a polynomial-time algorithm would put NP in randomized polynomial time ($\mathrm{NP} \subseteq \mathrm{RP}$). See [randomized NP-hardness of SVP](/svp-randomized-np-hardness/).
- **NP-hardness of approximation.** Under randomized reductions, $\gamma$-SVP is NP-hard for every $\gamma < \sqrt 2$ (Micciancio, 2001; his reduction is deterministic under a number-theoretic conjecture) and for every constant $\gamma$ (Khot, 2005). Haviv and Regev (2012) proved hardness within $2^{(\log n)^{1 - \varepsilon}}$ for every $\varepsilon > 0$, unless NP has randomized algorithms of quasi-polynomial time.
- **Limits on hardness.** [GapSVP](/gap-svp/) within $\sqrt{n / \log n}$ is in NP $\cap$ coAM (Goldreich and Goldwasser), and within $\sqrt n$ it is in NP $\cap$ coNP (Aharonov and Regev). So these factors are not NP-hard unless the polynomial hierarchy collapses. Cryptography uses factors polynomial in $n$, above these limits.
- **Upper bounds.** Exact SVP in randomized time $2^{n + o(n)}$ and deterministic time $2^{2n + o(n)}$; polynomial time for factor $2^{O(n \log \log n / \log n)}$ by block reduction with sieving.

## Reductions

- **SVP to CVP.** $\gamma$-SVP reduces to $\gamma$-CVP with $n$ calls (Goldreich, Micciancio, Safra and Seifert, 1999); the proof is on the [closest vector problem](/closest-vector-problem/) page. No reduction in the other direction that keeps the factor is known.
- **SVP and basis reduction.** An exact SVP oracle gives an [HKZ-reduced](/hkz-reduction/) basis with $n$ calls, and every reduced basis gives an approximate shortest vector; see [lattice basis reduction](/lattice-basis-reduction/).
- **uSVP and GapSVP.** Lyubashevsky and Micciancio (2009) proved that uSVP$_\gamma$, [bounded distance decoding](/bounded-distance-decoding/) and GapSVP are equivalent up to small polynomial losses in the factor.
- **Worst case to average case.** [Ajtai's reduction](/ajtai-worst-case-to-average-case-reduction/) shows that finding short vectors in random q-ary lattices is as hard as approximating SVP-type problems in the worst case, within polynomial factors.

## Applications

- **Cryptography.** The security of [learning with errors](/learning-with-errors/), [short integer solution](/short-integer-solution/) and [NTRU](/ntru-problem/) schemes is estimated by the cost of approximate SVP with BKZ and sieving.
- **Cryptanalysis.** Low-density [subset sum](/subset-sum-problem/) and [knapsack](/merkle-hellman-knapsack/) systems are broken by finding a short vector in a lattice built from the weights (Lagarias and Odlyzko, 1985).
- **Algebra and number theory.** [Integer relations](/integer-relation-problem/), minimal polynomials of algebraic numbers, and [simultaneous Diophantine approximation](/simultaneous-diophantine-approximation/) all ask for short vectors.
- **Coding and packing.** $\lambda_1$ is the packing radius times 2; the densest lattice packings and the kissing numbers are SVP-type questions.

## References
