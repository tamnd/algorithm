---
tag: 565R0Q
kind: definition
slug: successive-minima
name: Successive minima
aliases:
- Minkowski successive minima
- successive minima of a lattice
area: number-theory/lattice-reduction
level: advanced
summary: Radii lambda_1 through lambda_n of the smallest balls containing i independent lattice vectors.
prereqs: [lattice, lattice-basis, gram-schmidt-orthogonalization]
see_also: [shortest-vector-problem, minkowski-second-theorem, minkowski-theorem, shortest-independent-vectors-problem, minkowski-reduced-basis, hkz-reduction, covering-radius, dual-lattice]
sources:
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 1, Basics (successive minima, the Gram-Schmidt lower bound, and Minkowski's theorems), and Chapter 7, Basis reduction problems (the successive minima problem and SIVP)
  - book: isbn:9783540617884
    title: J. W. S. Cassels, An Introduction to the Geometry of Numbers, Springer, Classics in Mathematics, 1997 reprint
    locator: Chapter VIII, Successive minima (the definition for a general distance function and Minkowski's second theorem)
  - paper: "W. Banaszczyk, New bounds in some transference theorems in the geometry of numbers, Mathematische Annalen 296 (1993)"
    locator: pages 625 to 635 (the bound lambda_i(L) lambda_(n-i+1)(dual of L) at most n)
---

The successive minima $\lambda_1(L) \le \lambda_2(L) \le \cdots \le \lambda_n(L)$ of a [lattice](/lattice/) of rank $n$ are the radii at which a ball around the origin first contains $1, 2, \ldots, n$ [linearly independent](/linear-independence/) lattice vectors. The first one, $\lambda_1$, is the length of a shortest nonzero vector, the target of the [shortest vector problem](/shortest-vector-problem/). Together they describe how the lattice is spread in each direction, and [Minkowski's second theorem](/minkowski-second-theorem/) says that their product is the [determinant](/lattice-determinant/) up to a factor that depends only on $n$.

## Definition

**Notation.** As on all pages of this area, $L = L(B)$ has the basis rows $b_1, \ldots, b_n \in \mathbb{R}^m$, with [Gram-Schmidt](/gram-schmidt-orthogonalization/) vectors $b_i^*$, and $\bar{\mathcal{B}}(r) = \{x \in \mathbb{R}^m : \|x\| \le r\}$ is the closed ball of radius $r$ in the Euclidean norm.

For $i = 1, \ldots, n$, the **$i$-th successive minimum** of $L$ is

$$\lambda_i(L) = \min\big\{ r > 0 : \dim \operatorname{span}\big(L \cap \bar{\mathcal{B}}(r)\big) \ge i \big\}.$$

Equivalently, $\lambda_i(L)$ is the least $r$ such that $L$ has $i$ linearly independent vectors, each of length at most $r$.

**The minimum is attained.** The set of radii in the definition is not empty, since the basis vectors are $n$ independent vectors of length at most $\max_j \|b_j\|$. A ball contains finitely many lattice points, so the function $r \mapsto \dim \operatorname{span}(L \cap \bar{\mathcal{B}}(r))$ is a step function that changes only at the finitely many lengths of lattice vectors below a given bound, and it is continuous from the right. So the infimum is a minimum, and it is the length of some lattice vector.

**Vectors that reach the minima.** There are independent $v_1, \ldots, v_n \in L$ with $\|v_i\| = \lambda_i(L)$ for every $i$. *Proof.* Choose them greedily: let $v_i$ be a shortest lattice vector that is not in $\operatorname{span}(v_1, \ldots, v_{i-1})$. By the definition, the ball $\bar{\mathcal{B}}(\lambda_i)$ contains $i$ independent vectors, and at least one of them is outside the span of the $i - 1$ vectors already chosen, so $\|v_i\| \le \lambda_i$. Conversely $v_1, \ldots, v_i$ are $i$ independent vectors of length at most $\|v_i\|$, since $\|v_1\| \le \cdots \le \|v_i\|$ by the greedy choice, so $\lambda_i \le \|v_i\|$. $\square$

**Bounds through a basis.** For every basis and every $i$,

$$\min_{j \ge i} \|b_j^*\| \;\le\; \lambda_i(L) \;\le\; \max_{j \le i} \|b_j\|.$$

*Proof.* The upper bound holds because $b_1, \ldots, b_i$ are $i$ independent lattice vectors. For the lower bound, take independent $v_1, \ldots, v_i$ of length at most $\lambda_i$. They are not all in $\operatorname{span}(b_1, \ldots, b_{i-1})$, which has dimension $i - 1$. So one of them, $v = \sum_{j \le k} x_j b_j$ with $x_k \ne 0$, has $k \ge i$. Its component along $b_k^*$ is $x_k b_k^*$, so $\lambda_i \ge \|v\| \ge |x_k| \|b_k^*\| \ge \|b_k^*\| \ge \min_{j \ge i} \|b_j^*\|$. $\square$ For $i = 1$ this is the known bound $\lambda_1 \ge \min_j \|b_j^*\|$.

**General norms.** The same definition works with the ball replaced by any convex body $K$ that is symmetric about the origin, which gives $\lambda_i(K, L)$. Minkowski's theorems are stated in this form.

## Examples and non-examples

**Examples.**

- $\mathbb{Z}^n$: $\lambda_1 = \cdots = \lambda_n = 1$.
- The lattice with basis $(2, 0), (1, 2)$: $\lambda_1 = 2$, reached by $\pm (2, 0)$, and $\lambda_2 = \sqrt 5$, reached by $\pm (1, 2)$ and $\pm (-1, 2)$. The product $2 \sqrt 5 \approx 4.47$ is at least $\det = 4$, as it must be.
- The lattice with basis $(0, 1, 0), (1, 0, 1), (-2, 0, 1)$, of determinant 3: an exhaustive search over a coefficient box that is proved large enough gives $\lambda_1 = 1$, $\lambda_2 = \sqrt 2$ and $\lambda_3 = \sqrt 5$, reached by $(0, 1, 0)$, $(1, 0, 1)$ and $(-1, 0, 2)$. The vectors $\pm (1, 1, 1)$ of length $\sqrt 3$ do not count for $\lambda_3$, because $(1, 1, 1) = (0, 1, 0) + (1, 0, 1)$ is in the span of the first two.
- The hexagonal lattice: $\lambda_1 = \lambda_2 = 1$. In dimension 2 the two minima are always reached by a basis, the output of [Lagrange-Gauss reduction](/lagrange-gauss-reduction/).

**Non-examples.**

- **$\lambda_2$ is not the second length.** For the lattice with basis $(1, 0), (0, 10)$, the vector $(2, 0)$ is the second shortest length that occurs, but it is parallel to $(1, 0)$, so $\lambda_2 = 10$, not 2.
- **The minima are not always reached by a basis.** For $L = \mathbb{Z}^5 \cup (\mathbb{Z}^5 + (\tfrac12, \ldots, \tfrac12))$, $\lambda_1 = \cdots = \lambda_5 = 1$, reached only by $\pm e_1, \ldots, \pm e_5$, which generate a sublattice of index 2. Every basis of $L$ has a vector longer than $\lambda_5$; see [lattice basis](/lattice-basis/). For $n \le 4$ some basis always reaches all the minima.
- **The Gram-Schmidt lengths are not the minima.** For the basis $(1, 1, 1), (-1, 0, 2), (3, 5, 6)$ of the 3-dimensional lattice above, $\|b_3^*\| = \sqrt{9/14} < 1 = \lambda_1$. The numbers $\|b_i^*\|$ depend on the basis; the minima do not.

## Related definitions

- **[Shortest vector problem](/shortest-vector-problem/).** Compute $\lambda_1$ and a vector that reaches it.
- **Successive minima problem.** Find independent $v_1, \ldots, v_n$ with $\|v_i\| = \lambda_i$. Its approximate form, minimizing $\max_i \|v_i\|$ only, is the [shortest independent vectors problem](/shortest-independent-vectors-problem/).
- **[Minkowski's second theorem](/minkowski-second-theorem/).** $\det(L) \le \prod_i \lambda_i(L) \le \gamma_n^{n/2} \det(L)$, where $\gamma_n$ is the [Hermite constant](/hermite-constant/).
- **[Covering radius](/covering-radius/).** $\mu(L) \le \frac{\sqrt n}{2} \lambda_n(L)$, because the vectors that reach the minima generate a sublattice whose covering radius is at most $\frac12 (\sum_i \lambda_i^2)^{1/2}$; and $\mu(L) \ge \lambda_n(L) / 2$.
- **[Dual lattice](/dual-lattice/) and transference.** Banaszczyk (1993) proved $1 \le \lambda_i(L)\, \lambda_{n - i + 1}(L^\times) \le n$ for every $i$.
- **Reduced bases.** [Minkowski-reduced](/minkowski-reduced-basis/) and [HKZ-reduced](/hkz-reduction/) bases satisfy $\|b_i\| \le c_n \lambda_i$ with constants $c_n$ that depend only on $n$; an [LLL-reduced](/lll-reduction/) basis satisfies $\|b_i\| \le \alpha^{(n-1)/2} \lambda_i$.

## References
