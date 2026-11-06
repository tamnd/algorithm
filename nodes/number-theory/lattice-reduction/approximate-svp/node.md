---
tag: AS0FNQ
kind: problem
slug: approximate-svp
name: Approximate shortest vector problem
aliases:
- gamma-SVP
- SVP approximation
- approximate SVP
- SVP_gamma
area: number-theory/lattice-reduction
level: advanced
summary: Find a lattice vector within a factor gamma of the shortest length.
prereqs: [shortest-vector-problem, lattice-determinant]
see_also: [gap-svp, lll-approximation-guarantee, bkz-algorithm, hermite-constant, root-hermite-factor, svp-randomized-np-hardness, unique-svp, lattice-based-cryptography]
sources:
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 1 (search, optimization and promise versions of SVP), Chapter 2, Approximation algorithms (the LLL algorithm and its factor), and Chapter 4, Shortest vector problem (hardness of approximation)
  - book: isbn:9783642261640
    title: Phong Q. Nguyen and Brigitte Vallée (editors), The LLL Algorithm, Survey and Applications, Springer, 2010
    locator: Chapter 2, Phong Q. Nguyen, Hermite's constant and lattice algorithms (Hermite SVP, approximate SVP and the algorithms that solve them)
  - paper: "S. Khot, Hardness of approximating the shortest vector problem in lattices, Journal of the ACM 52(5) (2005)"
    locator: pages 789 to 808 (NP-hardness for every constant factor under randomized reductions)
  - paper: "I. Haviv and O. Regev, Tensor-based hardness of the shortest vector problem to within almost polynomial factors, Theory of Computing 8 (2012)"
    locator: the main theorem (hardness within 2^((log n)^(1 - epsilon)) under NP not in RTIME(2^poly(log n)))
  - paper: "N. Gama and P. Q. Nguyen, Predicting lattice reduction, EUROCRYPT 2008, LNCS 4965"
    locator: the experiments on the Hermite factor reached by LLL, BKZ and DEEP in practice
---

The approximate shortest vector problem $\gamma$-SVP asks, given a basis of a [lattice](/lattice/) $L$ and a factor $\gamma \ge 1$, for a nonzero vector $v \in L$ with $\|v\| \le \gamma \lambda_1(L)$. For $\gamma = 1$ it is the exact [shortest vector problem](/shortest-vector-problem/). The factor sets the difficulty: [LLL](/lll-algorithm/) reaches $\gamma = 2^{(n-1)/2}$ in polynomial time, [BKZ](/bkz-algorithm/) trades time for smaller factors, the problem is NP-hard under randomized reductions for every constant factor, and lattice-based cryptography rests on the belief that factors polynomial in $n$ need time exponential in $n$.

## In plain words

You are given a skewed grid of points and asked for a short step from one point to another. The best step may be hard to find, so you accept any step at most a fixed number of times longer than the best.

The fixed number is the slack. With a huge slack, a fast method that tidies up the grid description is enough. With a slack close to one, the problem is as hard as finding the best step, and nobody knows a fast method. In between, the known methods let you buy a smaller slack with more time, and the security of many modern encryption schemes depends on how expensive that trade is.

## Definition

Notation is that of the other pages in this area: a basis $B$ with rows $b_1, \ldots, b_n \in \mathbb{Q}^m$, the lattice $L = L(B)$ of rank $n$, its first minimum $\lambda_1(L)$ and its [determinant](/lattice-determinant/) $\det(L)$.

**$\gamma$-SVP (search).** Input: a basis $B$. Output: a vector $v \in L \setminus \{0\}$ with $\|v\| \le \gamma(n) \cdot \lambda_1(L)$.

The factor $\gamma = \gamma(n) \ge 1$ is a function of the rank, fixed in advance; typical choices are a constant, $\operatorname{poly}(n)$, or $2^{n^c}$. The input size is the binary length of $B$, and an algorithm is efficient when it runs in time polynomial in that size. Since $\lambda_1$ is unknown, the algorithm cannot check its own answer; this is what separates $\gamma$-SVP from problems with a certificate.

**Optimization version.** Output a number $d$ with $\lambda_1 \le d \le \gamma \lambda_1$. It reduces to the search version.

**Decision version.** [GapSVP$_\gamma$](/gap-svp/): decide whether $\lambda_1 \le r$ or $\lambda_1 > \gamma r$, with no requirement in between. It reduces to the optimization version.

## Variants

- **Hermite SVP (HSVP$_\gamma$).** Find $v \ne 0$ with $\|v\| \le \gamma \det(L)^{1/n}$. For $\gamma \ge \sqrt{\gamma_n}$, the square root of the [Hermite constant](/hermite-constant/), a solution always exists. HSVP does not need $\lambda_1$, so a solution can be checked, and it is the quantity that reduction algorithms control directly.
- **[Unique SVP](/unique-svp/) (uSVP$_\gamma$).** The promise $\lambda_2 > \gamma \lambda_1$; find a shortest vector.
- **[Shortest independent vectors](/shortest-independent-vectors-problem/) (SIVP$_\gamma$).** Find $n$ independent vectors of length at most $\gamma \lambda_n$; the problem used in [worst-case to average-case reductions](/ajtai-worst-case-to-average-case-reduction/).
- **Other norms.** $\gamma$-SVP in $\ell_p$ norms; in $\ell_\infty$ even the exact problem is NP-hard under deterministic reductions (van Emde Boas, 1981).
- **SVP with preprocessing.** The lattice is fixed and arbitrary advice about it may be computed in advance.

## Examples

- **A bad basis.** The lattice generated by $(2, 0)$ and $(1, 2)$ has $\lambda_1 = 2$. The bases $(4, 4), (9, 10)$ generate it too (the change of basis has determinant 1). Its first vector $(4, 4)$ has length $4\sqrt2 \approx 5.66$, a solution only for $\gamma \ge 2\sqrt2$. [Lagrange-Gauss reduction](/lagrange-gauss-reduction/) returns $(2, 0)$, a solution for $\gamma = 1$. The vector $(1, 2)$ of length $\sqrt5$ solves $\gamma$-SVP for $\gamma \ge \sqrt5/2 \approx 1.118$.
- **HSVP is weaker than SVP.** For $L$ generated by $(1, 0)$ and $(0, 100)$, $\lambda_1 = 1$ and $\det(L)^{1/2} = 10$. With $\gamma = 1.1 > \sqrt{\gamma_2} \approx 1.075$, the vector $(10, 0)$ solves HSVP$_\gamma$, since $10 \le 11$, but it is only a 10-approximate shortest vector. When $\lambda_1$ is much smaller than $\det^{1/n}$, an HSVP solution says little about $\lambda_1$.
- **The LLL factor.** The bound $\|b_1\| \le 2^{(n-1)/2} \lambda_1$ for $\delta = 3/4$ is a worst case. On random lattices LLL returns $\|b_1\| \approx 1.022^n \det(L)^{1/n}$ in practice (Gama and Nguyen), so in dimension 100 it finds vectors of length about $1.022^{100} \approx 8.8$ times $\det(L)^{1/n}$, or about $3.5$ times the [Gaussian heuristic](/gaussian-heuristic/), while the bound allows a factor $2^{49.5}$.

## Known algorithms

All algorithms below work on integer or rational input with exact arithmetic or with floating point of proved sufficient precision, and their times are polynomial in the input size times the stated function of $n$.

| method | factor $\gamma$ | time | status |
|---|---|---|---|
| [LLL](/lll-algorithm/), $\delta = 3/4$ | $2^{(n-1)/2}$ | polynomial | proved |
| LLL, $\delta \to 1$ | $(4/3 + \varepsilon)^{(n-1)/2}$; Hermite factor $(4/3 + \varepsilon)^{(n-1)/4}$ | polynomial | proved |
| slide reduction, block size $\beta$ | $((1 + \varepsilon)\gamma_\beta)^{(n - \beta)/(\beta - 1)}$ | $\beta$-dimensional SVP calls, polynomially many | proved |
| [BKZ](/bkz-algorithm/), block size $\beta$ | root Hermite factor $\approx (\beta / (2\pi e))^{1/(2\beta)}$ | not proved polynomial; terminates in practice after few tours | observed, heuristic |
| block reduction with the sieve of Ajtai, Kumar and Sivakumar | $2^{O(n \log \log n / \log n)}$ | polynomial, randomized | proved |
| [enumeration](/lattice-enumeration/) on an HKZ-like basis ([Kannan](/kannan-enumeration/)) | 1 | $n^{n/(2e) + o(n)}$, polynomial space | proved |
| sieving ([Gauss sieve](/gauss-sieve/) and successors) | 1 | $2^{0.292 n + o(n)}$ | heuristic |
| discrete Gaussian sampling (Aggarwal, Dadush, Regev, Stephens-Davidowitz) | 1 | $2^{n + o(n)}$, randomized | proved |

Small polynomial factors are no easier in the known algorithms: reaching $\gamma = n^c$ costs $2^{\Theta(n)}$ for all known methods, by running BKZ with block size linear in $n$.

## Bounds

- **NP-hardness.** Exact SVP is NP-hard under randomized reductions (Ajtai, 1998; see [SVP NP-hardness](/svp-randomized-np-hardness/)). Micciancio extended this to every $\gamma < \sqrt2$, Khot (2005) to every constant $\gamma$, and Haviv and Regev (2012) to $\gamma = 2^{(\log n)^{1 - \varepsilon}}$ under the assumption that NP is not in randomized quasi-polynomial time. All these reductions are randomized.
- **Limits of NP-hardness.** GapSVP$_\gamma$ is in NP $\cap$ coAM for $\gamma = \sqrt{n / \log n}$ (Goldreich and Goldwasser) and in NP $\cap$ [coNP](/co-np/) for $\gamma = \sqrt n$ (Aharonov and Regev). So it is not NP-hard for those factors unless the [polynomial hierarchy](/polynomial-hierarchy/) collapses. The hardness of the search problem for such factors is open.
- **Fine-grained bounds.** Under the gap exponential time hypothesis, exact SVP in some $\ell_p$ norms needs time $2^{\Omega(n)}$ (Aggarwal and Stephens-Davidowitz, 2018).
- **Quantum algorithms.** No quantum algorithm is known that solves $\gamma$-SVP for polynomial $\gamma$ in subexponential time; quantum speedups of sieving change the exponent only, to about $0.265 n$.

## Reductions

- **SVP$_\gamma$ to CVP$_\gamma$.** Approximate SVP reduces to approximate [CVP](/closest-vector-problem/) with the same factor and rank (Goldreich, Micciancio, Safra and Seifert, 1999).
- **SVP$_{\gamma^2}$ to HSVP$_\gamma$.** Lovász showed that an HSVP oracle with factor $\gamma$ gives an SVP algorithm with factor $\gamma^2$, by applying it to the lattice and to its projections.
- **Search to decision.** For exact SVP the search version reduces to the decision version. For approximate factors, the known reductions lose in the factor.
- **GapSVP to SIVP.** By transference with the [dual lattice](/dual-lattice/), an SIVP$_\gamma$ oracle applied to $L^\times$ solves GapSVP$_{n \gamma}$ on $L$.
- **Worst case to average case.** Ajtai's reduction maps worst-case SIVP$_\gamma$ and GapSVP$_\gamma$ with $\gamma = \operatorname{poly}(n)$ to the average-case [SIS](/short-integer-solution/) problem; Regev's maps them to [LWE](/learning-with-errors/), with a quantum step.

## Applications

- **Cryptanalysis.** Breaking the [Merkle-Hellman knapsack](/merkle-hellman-knapsack-cryptosystem/), attacks on [RSA](/rsa-cryptosystem/) with small exponents through the [Coppersmith method](/coppersmith-method/), and the cost estimates for attacks on LWE and NTRU all come down to $\gamma$-SVP with a given $\gamma$.
- **Lattice-based cryptography.** The security of [lattice-based schemes](/lattice-based-cryptography/) is reduced to $\gamma$-SVP or SIVP with $\gamma = \operatorname{poly}(n)$, and parameters are chosen from the observed cost of BKZ.
- **Algorithms.** Factoring polynomials over the rationals, [simultaneous Diophantine approximation](/simultaneous-diophantine-approximation/), finding [integer relations](/integer-relation-problem/), and Lenstra's integer programming in fixed dimension all need a short vector only within a factor depending on $n$, which LLL provides.

## References
