---
tag: 498P2W
kind: concept
slug: gaussian-heuristic
name: Gaussian heuristic
aliases:
- expected shortest vector heuristic
- GH(L)
- Gauss heuristic
area: number-theory/lattice-reduction
level: advanced
summary: Estimate that lambda_1 is about the radius of a ball whose volume equals the determinant.
prereqs: [lattice, lattice-determinant, hermite-constant]
see_also: [root-hermite-factor, bkz-algorithm, lattice-enumeration, lattice-sieving, gauss-sieve, unique-svp, minkowski-theorem, shortest-vector-problem]
sources:
  - book: isbn:9783642261640
    title: Phong Q. Nguyen and Brigitte Vallée (editors), The LLL Algorithm, Survey and Applications, Springer, 2010
    locator: Chapter 2, Phong Q. Nguyen, Hermite's constant and lattice algorithms (the Gaussian heuristic and random lattices)
  - paper: "Y. Chen and P. Q. Nguyen, BKZ 2.0, Better lattice security estimates, ASIACRYPT 2011, LNCS 7073"
    locator: the BKZ simulator, which assumes the Gaussian heuristic for the projected blocks
  - paper: "N. Gama, P. Q. Nguyen and O. Regev, Lattice enumeration using extreme pruning, EUROCRYPT 2010, LNCS 6110"
    locator: the estimate of the number of enumeration nodes by volumes of balls and cylinders
  - paper: "C. L. Siegel, A mean value theorem in geometry of numbers, Annals of Mathematics 46(2) (1945)"
    locator: the mean value theorem for the number of lattice points in a set, over random unimodular lattices
---

The Gaussian heuristic predicts that a measurable set $S$ contains about $\operatorname{vol}(S) / \det(L)$ points of a [lattice](/lattice/) $L$. Applied to a ball, it predicts the first minimum: $\lambda_1(L) \approx \operatorname{GH}(L) = (\det(L) / V_n)^{1/n} \approx \sqrt{n / (2 \pi e)}\, \det(L)^{1/n}$, where $V_n$ is the volume of the unit ball. It is accurate for random lattices of moderate and large dimension, it is wrong for structured lattices, and it underlies almost every cost estimate for [enumeration](/lattice-enumeration/), [sieving](/lattice-sieving/) and [BKZ](/bkz-algorithm/).

## In plain words

A grid of points fills space evenly: each point owns the same amount of room. So a big region should contain about as many grid points as the number of times that room fits into the region.

Use this to guess how far the nearest neighbour of a grid point is. Grow a ball around the point until it is big enough to hold one point's room. The radius at that moment is the guess.

For a grid chosen at random, in many dimensions, the guess is very good. For special grids it can be far off: the square grid has its neighbours much closer than predicted, and grids built with a hidden short arrow are designed to break it. It is a rule of thumb, not a theorem, and the cost estimates of the best attacks on lattice cryptography rely on it.

## The idea

Notation is that of the other pages in this area: $L$ has rank $n$, basis rows $b_1, \ldots, b_n$, Gram-Schmidt vectors $b_i^*$, first minimum $\lambda_1$ and [determinant](/lattice-determinant/) $\det(L) = \prod \|b_i^*\|$.

**The heuristic.** For a "nice" set $S \subset \operatorname{span}(L)$,

$$\#(S \cap L) \approx \frac{\operatorname{vol}(S)}{\det(L)}.$$

**The prediction for $\lambda_1$.** Take $S$ the ball of radius $r$, of volume $V_n r^n$ with $V_n = \pi^{n/2} / \Gamma(n/2 + 1)$. The ball first holds a nonzero point when its volume reaches $\det(L)$, which gives

$$\operatorname{GH}(L) = \Big(\frac{\det(L)}{V_n}\Big)^{1/n} = \frac{\Gamma(n/2 + 1)^{1/n}}{\sqrt\pi} \det(L)^{1/n} = \sqrt{\frac{n}{2 \pi e}}\, (\pi n)^{1/(2n)} (1 + o(1)) \det(L)^{1/n}.$$

Compare [Minkowski's theorem](/minkowski-theorem/), which proves $\lambda_1 \le 2 \operatorname{GH}(L)$ for every lattice. In the language of the [Hermite constant](/hermite-constant/), the heuristic says that a typical lattice has $\lambda_1^2 / \det^{2/n} \approx V_n^{-2/n} \approx n / (2 \pi e)$, while the maximum $\gamma_n$ is between $n/(2\pi e)$ and $1.744\, n/(2 \pi e)$ for large $n$.

**Why it is believed.** For a lattice chosen at random from the natural (Haar) probability measure on lattices of determinant 1, Siegel's mean value theorem says that the expected number of nonzero lattice points in $S$ is exactly $\operatorname{vol}(S)$. Rogers showed that, as $n$ grows, the number of pairs $\pm v$ in a ball of volume $V$ tends to a Poisson variable of mean $V/2$. So for random lattices $\lambda_1 / \operatorname{GH}(L)$ tends to 1 in probability. Lattices from cryptography are not Haar-random, and for them the heuristic is an assumption, checked by experiment.

**What it is used for.** The heuristic is applied to projected sublattices as well as to $L$:

- **Enumeration cost.** The number of nodes at depth $k$ of an [enumeration](/lattice-enumeration/) tree of radius $R$ is predicted to be $V_k R^k / \prod_{i = n-k+1}^n \|b_i^*\|$, the number of points of the projected lattice $\pi_{n-k+1}(L)$ in a $k$-ball. Pruned enumeration replaces the ball by a cylinder intersection and uses its volume.
- **Sieving.** The list size $(4/3)^{n/2 + o(n)}$ of heuristic [sieves](/lattice-sieving/) and the [Gauss sieve](/gauss-sieve/) comes from the heuristic that the lattice points of norm close to $\operatorname{GH}(L)$ behave like uniform points on a sphere.
- **BKZ.** The Chen-Nguyen simulator predicts the Gram-Schmidt profile of a [BKZ](/bkz-algorithm/)-reduced basis by assuming that the first vector of every projected block of size $\beta$ has length $\operatorname{GH}$ of that block. This gives the predicted [root Hermite factor](/root-hermite-factor/) $\delta_\beta \approx \big(\tfrac{\beta}{2\pi e} (\pi \beta)^{1/\beta}\big)^{1/(2(\beta - 1))}$ for large $\beta$.
- **[Unique SVP](/unique-svp/) and attacks on LWE.** An attack succeeds when the planted short vector is shorter than what the heuristic predicts for the rest of the lattice; the "2016 estimate" of Alkim, Ducas, Pöppelmann and Schwabe compares the projected planted vector with $\operatorname{GH}$ of the last block.
- **Choosing a radius.** Enumeration and sieving codes start with the radius $1.05\, \operatorname{GH}(L)$ or similar when no better bound is known, and the Darmstadt SVP challenge accepts vectors shorter than $1.05\, \operatorname{GH}(L)$.

## Examples

Values of $\operatorname{GH}$ for $\det(L) = 1$, with $\sqrt{n / (2 \pi e)}$ for comparison:

| $n$ | 2 | 8 | 10 | 18 | 24 | 50 | 100 | 150 |
|---|---|---|---|---|---|---|---|---|
| $\operatorname{GH}$ | 0.5642 | 0.8394 | 0.9106 | 1.1489 | 1.2975 | 1.7999 | 2.4903 | 3.0250 |
| $\sqrt{n/(2\pi e)}$ | 0.3422 | 0.6844 | 0.7652 | 1.0266 | 1.1854 | 1.7110 | 2.4197 | 2.9635 |

- **A small lattice.** For $b_1 = (2, 0)$, $b_2 = (1, 2)$ with $\det = 4$: $\operatorname{GH} = \sqrt{4/\pi} \approx 1.128$, while $\lambda_1 = 2$. In small dimension the heuristic says little: a lattice of rank 2 and determinant 4 can have any $\lambda_1$ in $(0, (8/\sqrt3)^{1/2}]$, about $(0, 2.15]$, and there is no averaging effect to pull it towards $\operatorname{GH}$.
- **$\mathbb{Z}^n$.** Here $\det = 1$ and $\lambda_1 = 1$. The heuristic predicts $\operatorname{GH} > 1$ from $n = 13$ on ($\operatorname{GH} \approx 1.007$) and $\approx 2.49$ at $n = 100$. The cube lattice has far more short vectors than a random lattice: it is a structured lattice.
- **$E_8$ and the Leech lattice.** Both have determinant 1. $E_8$ has $\lambda_1 = \sqrt2 \approx 1.414$ against $\operatorname{GH} \approx 0.839$, and the Leech lattice has $\lambda_1 = 2$ against $\operatorname{GH} \approx 1.30$. The densest lattices have $\lambda_1$ well above the heuristic, as the bound $\gamma_n \ge n / (2\pi e)$ allows.
- **q-ary lattices.** $\Lambda_q^\perp(A)$ of dimension $m$ with $A \in \mathbb{Z}_q^{k \times m}$ random has $\det = q^k$, and $\lambda_1 \approx \min(q, \sqrt{m/(2\pi e)}\, q^{k/m})$: the heuristic holds until it predicts more than $q$, where the vectors $q e_i$ take over.
- **LWE lattices.** The embedding lattice of an LWE instance contains the error vector, of length about $\sigma \sqrt m$, far below $\operatorname{GH}$. The heuristic still describes the rest of the lattice, which is what attack estimates need.

## Where it is used

- Security estimates for [lattice-based cryptography](/lattice-based-cryptography/), through the cost models of enumeration, sieving and BKZ above.
- Predicting $\lambda_1$ to set the radius of exact [SVP](/shortest-vector-problem/) solvers and to decide when an approximate solution is good enough.
- The [geometric series assumption](/root-hermite-factor/) for reduced bases, which is a consequence of applying the heuristic to every block.
- Average-case analyses of [Kannan enumeration](/kannan-enumeration/) and [Fincke-Pohst enumeration](/fincke-pohst-enumeration/), where the proved worst-case node bounds are replaced by volume estimates.

## References
