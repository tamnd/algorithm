---
tag: Q5168P
kind: problem
slug: unique-svp
name: Unique shortest vector problem
aliases:
- uSVP
- unique SVP
- uSVP_gamma
area: number-theory/lattice-reduction
level: advanced
summary: SVP promised to have a shortest vector much shorter than every other nonparallel vector.
prereqs: [shortest-vector-problem, successive-minima]
see_also: [bounded-distance-decoding, gap-svp, lll-approximation-guarantee, root-hermite-factor, learning-with-errors, svp-randomized-np-hardness, subset-sum-problem, ntru-problem]
sources:
  - paper: "V. Lyubashevsky and D. Micciancio, On bounded distance decoding, unique shortest vectors, and the minimum distance problem, Advances in Cryptology, Crypto 2009, LNCS 5677"
    locator: pages 577 to 594 (the reductions between uSVP, BDD and GapSVP with their losses in the factor)
  - paper: "M. Ajtai and C. Dwork, A public-key cryptosystem with worst-case/average-case equivalence, STOC 1997"
    locator: pages 284 to 293 (the first public-key system whose security rests on the worst-case hardness of uSVP within a polynomial factor)
  - paper: "O. Regev, New lattice-based cryptographic constructions, Journal of the ACM 51(6) (2004)"
    locator: pages 899 to 942 (public-key encryption from uSVP within the factor n^(3/2))
  - paper: "R. Kumar and D. Sivakumar, On the unique shortest lattice vector problem, Theoretical Computer Science 255 (2001)"
    locator: pages 641 to 648 (NP-hardness of uSVP under randomized reductions for factors close to 1)
  - paper: "Nicolas Gama and Phong Q. Nguyen, Predicting lattice reduction, Advances in Cryptology, Eurocrypt 2008, LNCS 4965"
    locator: pages 31 to 51 (the experiments in which reduction finds the unique shortest vector once the gap is a fixed fraction of the Hermite factor)
  - paper: "M. R. Albrecht, F. Göpfert, F. Virdia and T. Wunderer, Revisiting the expected cost of solving uSVP and applications to LWE, Advances in Cryptology, Asiacrypt 2017"
    locator: the experiments that confirm the success condition for BKZ on embedding lattices
---

The unique shortest vector problem uSVP$_\gamma$ is the [shortest vector problem](/shortest-vector-problem/) on lattices that are promised to have a gap: the second [successive minimum](/successive-minima/) is more than $\gamma$ times the first, $\lambda_2(L) > \gamma \lambda_1(L)$. Then the shortest vector is unique up to sign, and every vector shorter than $\lambda_2$ is a multiple of it. The larger the gap, the easier the problem: [LLL](/lll-algorithm/) solves it when $\gamma > 2^{(n-1)/2}$, and in practice when $\gamma$ is a fixed fraction of the Hermite factor of the reduction. Many lattice attacks, on [LWE](/learning-with-errors/), [NTRU](/ntru-problem/) and low-density [subset sum](/subset-sum-problem/), work by building a lattice in which the secret is such a unique short vector.

## In plain words

Think of a grid of points in which one point, and its mirror image, sits unusually close to the origin, and every other point is far away in comparison. We are told that this is the case, and we must find that special point.

The gap helps. A rough search that only promises a point within some factor of the shortest is forced to return the special point when the factor is smaller than the gap, because every other candidate is too long. That is why lattice reduction finds hidden short secrets when they are short enough, and why attacks on lattice-based codes try to set up a grid with a large gap.

## Definition

**Notation.** As on all pages of this area: $b_1, \ldots, b_n$ are the rows of a basis of the lattice $L$ of rank $n$, with Gram-Schmidt vectors $b_i^*$, coefficients $\mu_{ij}$, determinant $\det(L)$ and the LLL parameter $\delta$; $\lambda_1 \le \lambda_2$ are the first two successive minima.

**uSVP$_\gamma$ (search).** *Input:* a basis $B$ and a factor $\gamma \ge 1$, with the promise that $\lambda_2(L) > \gamma \lambda_1(L)$. *Output:* a shortest nonzero vector $s \in L$.

**What the promise gives.** If $v \in L$ and $\|v\| < \lambda_2$, then $v$ is an integer multiple of $s$: otherwise $s$ and $v$ would be two independent vectors of length less than $\lambda_2$. The shortest vector is primitive, so the multiples of $s$ in $L$ are exactly $k s$ with $k \in \mathbb{Z}$, and the solution is unique up to sign as soon as $\gamma \ge 1$.

**Finding a multiple is enough.** Any algorithm that returns a nonzero $v \in L$ with $\|v\| < \lambda_2$ solves uSVP: $v = k s$, and $s = v / k$ with $k = \gcd$ of the coefficients of $v$ in the basis, up to sign. So a $\gamma'$-approximate SVP algorithm with $\gamma' \le \gamma$ solves uSVP$_\gamma$.

## Variants

- **Exact uniqueness.** $\gamma = 1$: the shortest vector is unique up to sign, with no quantitative gap.
- **Decision and promise versions.** Distinguish lattices with $\lambda_2 > \gamma \lambda_1$ and a given bound on $\lambda_1$ from lattices with no short vector; these are the versions used in the reductions to and from GapSVP.
- **[Bounded distance decoding](/bounded-distance-decoding/) (BDD$_\alpha$).** Given a target within distance $\alpha \lambda_1(L)$ of the lattice, find the closest lattice vector. Its embedding turns it into uSVP, as in the example below.
- **Planted versions.** In cryptanalysis the lattice is random apart from one planted short vector, for example the secret and error of an LWE sample; the gap is then estimated by the [Gaussian heuristic](/gaussian-heuristic/) for $\lambda_2$.

## Examples

- **A visible gap.** The lattice $\{(x, y) \in \mathbb{Z}^2 : y \equiv 3 x \pmod{101}\}$ has the basis $(1, 3), (0, 101)$ and determinant 101. Its shortest vector is $(1, 3)$ of length $\sqrt{10}$, and $\lambda_1 \lambda_2 \ge \det(L)$ in dimension 2 gives $\lambda_2 \ge 101 / \sqrt{10}$, so the gap is at least $10.1$.
- **Bounded distance decoding as uSVP.** Let $L'$ have the basis $(7, 2), (3, 9)$, with $\det(L') = 57$ and $\lambda_1(L') = \sqrt{53}$. The target $t = (18, 13)$ is at distance 1 from the lattice vector $2 (7, 2) + (3, 9) = (17, 13)$. The embedding lattice with rows
  $$(7, 2, 0), \quad (3, 9, 0), \quad (18, 13, 1)$$
  contains $t - (17, 13)$ with the extra coordinate 1, that is $(1, 0, 1)$, of length $\sqrt 2$. By enumeration $\lambda_1 = \sqrt 2$ and $\lambda_2 = \sqrt{29}$, reached by $(-4, -2, 3)$, so the gap is $\sqrt{29 / 2} \approx 3.81$. This is above $2^{(3 - 1)/2} = 2$, so LLL with $\delta = 3/4$ must find the short vector, and it returns $(1, 0, 1)$ as its first vector, which recovers the error $(1, 0)$ and the closest vector $(17, 13)$.
- **No gap.** In $\mathbb{Z}^n$ with $n \ge 2$, $\lambda_1 = \lambda_2 = 1$, so the promise fails for every $\gamma \ge 1$.

## Known algorithms

Here $n$ is the rank. The bounds count arithmetic operations on numbers of size polynomial in the input; proved and heuristic results are marked.

- **Any approximate SVP algorithm.** By the remark in the definition, a $\gamma$-SVP algorithm solves uSVP$_\gamma$.
- **LLL (proved).** An LLL-reduced basis has $\|b_1\| \le \alpha^{(n-1)/2} \lambda_1$ with $\alpha = 1 / (\delta - 1/4)$, by the [LLL guarantee](/lll-approximation-guarantee/). If $\gamma > \alpha^{(n-1)/2}$, then $\|b_1\| < \lambda_2$, so $b_1 = k s$, and $k = \pm 1$ because a basis vector is primitive. So LLL solves uSVP$_\gamma$ for $\gamma > 2^{(n-1)/2}$ with $\delta = 3/4$ in polynomial time.
- **Block reduction (proved).** [BKZ](/bkz-algorithm/) and slide reduction solve uSVP$_\gamma$ for $\gamma = \beta^{O(n / \beta)}$ with SVP calls in dimension $\beta$, by the same argument.
- **In practice (heuristic).** Gama and Nguyen observed that a reduction with root Hermite factor $\delta_0$ finds the unique shortest vector when $\lambda_2 / \lambda_1 \ge \tau \delta_0^n$, with a constant $\tau < 1$ that depends on the algorithm and the lattice family. So the practical threshold is a fraction of the Hermite factor $\delta_0^n$, much smaller than the proved factor; see the [root Hermite factor](/root-hermite-factor/).
- **BKZ on embedding lattices (heuristic).** For an embedding lattice of dimension $d$ whose planted vector has entries of standard deviation $\sigma$, BKZ with block size $\beta$ is predicted to succeed when $\sigma \sqrt \beta \le \delta_0^{2 \beta - d} \det(L)^{1/d}$, where $\delta_0$ is the root Hermite factor of BKZ-$\beta$. The reason is that the projection of the secret onto the last $\beta$ Gram-Schmidt directions becomes the shortest vector of that block. Albrecht, Göpfert, Virdia and Wunderer confirmed this condition in experiments, and it is the primal attack in LWE security estimates.
- **Exact algorithms.** Every SVP algorithm, such as [enumeration](/lattice-enumeration/) or [sieving](/lattice-sieving/), solves uSVP; enumeration can use the radius $\lambda_1$ when an estimate is known, which a large gap makes cheap to check.

## Bounds

- **NP-hardness.** Kumar and Sivakumar (2001) showed that uSVP$_\gamma$ is NP-hard under randomized reductions for some factors $\gamma > 1$ close to 1, by combining the [randomized hardness of SVP](/svp-randomized-np-hardness/) with an isolation argument that makes the shortest vector unique. No NP-hardness is known for large constant or polynomial $\gamma$.
- **Equivalences (Lyubashevsky and Micciancio, 2009).** For factors polynomial in $n$, BDD$_{1/(2\gamma)}$ reduces to uSVP$_\gamma$, uSVP$_\gamma$ reduces to BDD$_{1/\gamma}$, uSVP$_\gamma$ reduces to GapSVP$_\gamma$, and GapSVP$_{\gamma \sqrt{n / \log n}}$ reduces to BDD$_{1/\gamma}$. So uSVP, BDD and [GapSVP](/gap-svp/) are equivalent up to polynomial losses in the factor.
- **Upper bounds.** Polynomial time for $\gamma > 2^{(n-1)/2}$ (LLL) and for $\gamma = 2^{O(n \log \log n / \log n)}$ (block reduction); exact in randomized time $2^{n + o(n)}$ through SVP.

## Reductions

- **BDD to uSVP (embedding).** Given a basis $B$ and a target $t = v + e$ with $v \in L$ and $\|e\|$ small, the lattice with rows $(b_i, 0)$ and $(t, M)$ contains $(e, M)$. For a suitable $M$ about $\|e\|$, this is the unique shortest vector when $\|e\|$ is small compared with $\lambda_1(L)$ (Kannan's embedding technique). The example above is an instance.
- **uSVP to GapSVP and BDD.** The reductions of Lyubashevsky and Micciancio listed under Bounds.
- **Average case.** Ajtai and Dwork (1997) built a public-key system whose security reduces to the worst-case hardness of uSVP within a polynomial factor; Regev (2004) improved the factor to $n^{3/2}$. Later systems are based on [LWE](/learning-with-errors/), which reduces to GapSVP and SIVP instead.

## Applications

- **LWE and NTRU attacks.** The primal attack on [learning with errors](/learning-with-errors/) embeds an LWE sample into a lattice whose unique short vector holds the secret and the error; the cost of BKZ that reaches the needed gap sets the security level. Key recovery for [NTRU](/ntru-problem/) is a uSVP instance in the lattice spanned by the public key.
- **Low-density subset sum.** Lagarias and Odlyzko, and later Coster and others, solve [subset sum](/subset-sum-problem/) with density below a threshold by showing that the solution vector is the unique shortest vector of a lattice built from the weights, with high probability.
- **Hidden denominators.** A [simultaneous Diophantine approximation](/simultaneous-diophantine-approximation/) problem with a planted denominator much better than Dirichlet's bound is a uSVP instance.
- **Cryptographic hardness.** The Ajtai-Dwork and Regev systems were the first public-key systems with worst-case security guarantees, both based on uSVP.

## References
