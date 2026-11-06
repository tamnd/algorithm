---
tag: P3TK17
kind: definition
slug: covering-radius
name: Covering radius
aliases:
- lattice covering radius
- mu(L)
- deep hole distance
area: number-theory/lattice-reduction
level: advanced
summary: Smallest radius r such that balls of radius r around lattice points cover the whole space.
prereqs: [lattice, successive-minima, closest-vector-problem]
see_also: [dual-lattice, babai-nearest-plane, bounded-distance-decoding, gram-schmidt-orthogonalization, lattice-determinant, ajtai-worst-case-to-average-case-reduction, hermite-constant, gaussian-heuristic]
sources:
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 1, Basics, and Chapter 7, Basis reduction problems (the covering radius, its relation to the successive minima, and its use in bounding reduced bases)
  - book: isbn:9780387985855
    title: J. H. Conway and N. J. A. Sloane, Sphere Packings, Lattices and Groups, third edition, Springer, 1999
    locator: Chapter 2, Coverings, lattices and quantizers (covering radius, deep holes and the Voronoi cell)
  - paper: "V. Guruswami, D. Micciancio and O. Regev, The complexity of the covering radius problem, Computational Complexity 14(2) (2005)"
    locator: the main theorems (approximation factors in AM, coAM and NP intersect coNP)
  - paper: "W. Banaszczyk, New bounds in some transference theorems in the geometry of numbers, Mathematische Annalen 296 (1993)"
    locator: the transference bound mu(L) lambda_1(L dual) at most n/2
---

The covering radius $\mu(L)$ of a [lattice](/lattice/) $L$ is the largest distance from a point of the span of $L$ to the nearest lattice point. Equivalently, it is the smallest $r$ such that the balls of radius $r$ centred at the lattice points cover the span. It is the worst case of the [closest vector problem](/closest-vector-problem/): every target is within $\mu(L)$ of the lattice, and some targets, the deep holes, are exactly that far.

## Definition

Let $L = L(B)$ be a lattice of rank $n$ with basis rows $b_1, \ldots, b_n$, and write $\operatorname{dist}(t, L) = \min_{v \in L} \|t - v\|$. The **covering radius** is

$$\mu(L) = \max_{t \in \operatorname{span}(L)} \operatorname{dist}(t, L).$$

The maximum exists, because $\operatorname{dist}(\cdot, L)$ is continuous and periodic modulo $L$, so it is enough to look at $t$ in a fundamental parallelepiped, a compact set. A point $t$ with $\operatorname{dist}(t, L) = \mu(L)$ is a **deep hole**. Equivalently:

- $\mu(L)$ is the smallest $r$ with $L + r \mathcal{B} \supseteq \operatorname{span}(L)$, where $\mathcal{B}$ is the closed unit ball of the span;
- $\mu(L)$ is the circumradius of the **Voronoi cell** $\mathcal{V} = \{x \in \operatorname{span}(L) : \|x\| \le \|x - v\| \ \forall v \in L\}$, and the deep holes are the vertices of $\mathcal{V}$ that are farthest from $0$, translated by lattice vectors.

**Bounds.** Let $\lambda_1 \le \cdots \le \lambda_n$ be the [successive minima](/successive-minima/) and $b_i^*$ the [Gram-Schmidt vectors](/gram-schmidt-orthogonalization/).

1. $\mu(L) \ge \lambda_n / 2$. *Proof.* The lattice vectors shorter than $\lambda_n$ span a subspace $W$ of dimension less than $n$. Take $t \in \operatorname{span}(L)$ orthogonal to $W$ with $\|t\| = \lambda_n / 2$. If $v \in L$ has $\|v\| < \lambda_n$, then $v \in W$ and $\|t - v\|^2 = \|t\|^2 + \|v\|^2 \ge \lambda_n^2/4$. If $\|v\| \ge \lambda_n$, then $\|t - v\| \ge \|v\| - \|t\| \ge \lambda_n/2$. So $\operatorname{dist}(t, L) \ge \lambda_n/2$. $\square$
2. $\mu(L) \le \tfrac12 \big(\sum_{i=1}^n \|b_i^*\|^2\big)^{1/2}$ for every basis, and $\mu(L) \le \tfrac{\sqrt n}{2} \lambda_n$. *Proof.* [Babai's nearest plane algorithm](/babai-nearest-plane/) returns, for every target, a lattice vector whose error has a component of size at most $\tfrac12 \|b_i^*\|$ along each $b_i^*$. For the second bound, take independent $v_1, \ldots, v_n \in L$ with $\|v_i\| = \lambda_i$. They generate a sublattice $L'$ with the same span, so $\mu(L) \le \mu(L') \le \tfrac12 (\sum \|v_i^*\|^2)^{1/2} \le \tfrac12 (\sum \|v_i\|^2)^{1/2} \le \tfrac{\sqrt n}{2} \lambda_n$. $\square$
3. **Volume.** The balls of radius $\mu$ around the lattice points cover the span, so the Voronoi cell, which has volume $\det(L)$, lies inside the ball of radius $\mu$ around $0$: $\operatorname{vol}(\mu \mathcal{B}) \ge \det(L)$, that is $\mu(L) \ge (\det(L) / V_n)^{1/n}$, with $V_n$ the volume of the unit $n$-ball. This is close to the [Gaussian heuristic](/gaussian-heuristic/) value of $\lambda_1$.
4. **Transference.** For the [dual lattice](/dual-lattice/) $L^\times$, $\tfrac12 \le \mu(L)\, \lambda_1(L^\times) \le \tfrac n2$. The lower bound holds because $L$ lies on hyperplanes $1 / \lambda_1(L^\times)$ apart, and a point halfway between two of them is far from all of them. The upper bound is Banaszczyk's theorem.

**Computation.** Deciding $\mu(L) \le r$ is a $\forall \exists$ question (for every target there is a close lattice point), so it lies in the second level $\Pi_2$ of the polynomial hierarchy. Guruswami, Micciancio and Regev showed that approximating $\mu$ within a factor 2 is in AM and within $\sqrt{n / \log n}$ is in coAM, so these approximations are unlikely to be NP-hard. Exact computation goes through the Voronoi cell, whose number of vertices can grow like $(n+1)!$, so it is practical only in small dimension.

## Examples and non-examples

**Examples.**

- **$\mathbb{Z}^n$.** $\mu = \sqrt n / 2$, with deep holes at $(\tfrac12, \ldots, \tfrac12) + \mathbb{Z}^n$. Here $\lambda_n = 1$, so bound 1 is tight for $n = 1$ and bound 2 is tight for every $n$.
- **A lattice in the plane.** For $b_1 = (2, 0)$, $b_2 = (1, 2)$, the basis is reduced and the triangle $0, b_1, b_2$ is acute, with sides $2, \sqrt5, \sqrt5$. In dimension 2 the covering radius is the circumradius of such a triangle: $\mu = abc / (4 \cdot \text{area}) = 2 \cdot 5 / (4 \cdot 2) = \tfrac54$, with deep hole $(1, \tfrac34)$, at distance $\tfrac54$ from $0$, $(2, 0)$ and $(1, 2)$. Compare the bounds: $\lambda_2 / 2 = \sqrt5/2 \approx 1.118$, the volume bound $\sqrt{4/\pi} \approx 1.128$, and the Gram-Schmidt bound $\tfrac12 \sqrt{4 + 4} = \sqrt2 \approx 1.414$.
- **The hexagonal lattice** $A_2$, with minimal distance 1: $\mu = 1/\sqrt3$, the circumradius of the unit equilateral triangle, with deep holes at the centroids of the triangles. It is the thinnest lattice covering of the plane.
- **The checkerboard lattice** $D_3 = \{x \in \mathbb{Z}^3 : x_1 + x_2 + x_3 \text{ even}\}$: $\mu = 1$, with deep holes at the points of $\mathbb{Z}^3$ of odd coordinate sum such as $(1, 0, 0)$, the centres of the octahedral holes of the face-centred cubic packing. The point $(\tfrac12, \tfrac12, \tfrac12)$ is a shallow hole, at distance $\sqrt3/2$.
- **Rank 1.** For $L = \mathbb{Z} v$, $\mu = \|v\|/2$, with deep holes at $(k + \tfrac12) v$.

**Non-examples.**

- **The packing radius.** $\lambda_1 / 2$ is the largest radius at which balls around lattice points do not overlap. It is a lower bound for $\mu$, not $\mu$ itself: for $\mathbb{Z}^n$ it is $\tfrac12$ while $\mu = \sqrt n/2$.
- **Points outside the span.** For a lattice that is not full rank, $\max_{t \in \mathbb{R}^m} \operatorname{dist}(t, L)$ is infinite. The definition takes the maximum over $\operatorname{span}(L)$ only.
- **A basis quantity.** The value $\tfrac12 (\sum \|b_i^*\|^2)^{1/2}$ depends on the basis and is only an upper bound; the covering radius depends only on the lattice. For $\mathbb{Z}^2$ with the basis $(1, 0), (5, 1)$ the Gram-Schmidt lengths are $1, 1$ and the bound is exact, but for the basis $(1, 1), (1, 2)$ of $\mathbb{Z}^2$ they are $\sqrt2$ and $1/\sqrt2$, giving $\tfrac12 \sqrt{5/2} \approx 0.79 > \mu = 0.71$.
- **The half-diameter of a fundamental parallelepiped.** Half the longest diagonal of the parallelepiped spanned by the basis is also only an upper bound, and it can be much larger than $\mu$ for a skewed basis.

## Related definitions

- **[Closest vector problem](/closest-vector-problem/).** CVP asks for a lattice point within $\operatorname{dist}(t, L) \le \mu(L)$; the deep holes are its hardest targets.
- **[Bounded distance decoding](/bounded-distance-decoding/).** The promise version where the target is much closer than $\lambda_1/2$, far below $\mu$.
- **Voronoi cell and Voronoi relevant vectors.** The cell is the intersection of the half-spaces $\langle x, v \rangle \le \|v\|^2 / 2$ over at most $2(2^n - 1)$ relevant vectors $v$; its circumradius is $\mu$.
- **[Successive minima](/successive-minima/).** $\lambda_n / 2 \le \mu \le \tfrac{\sqrt n}{2} \lambda_n$.
- **Covering density.** The ratio $V_n \mu^n / \det(L)$, at least 1; the covering problem asks for lattices that make it small, as the packing problem asks to make $V_n (\lambda_1/2)^n / \det(L)$ large.
- **Smoothing parameter.** A Gaussian quantity $\eta_\varepsilon(L)$ used in [worst-case to average-case reductions](/ajtai-worst-case-to-average-case-reduction/); it lies between multiples of $1 / \lambda_1(L^\times)$ and $\lambda_n$ and plays the role of the covering radius in probability arguments.

## References
