---
tag: N7XGPH
kind: theorem
slug: minkowski-theorem
name: Minkowski's first theorem
aliases:
- Minkowski's convex body theorem
- Minkowski's lattice point theorem
area: number-theory/lattice-reduction
level: advanced
summary: Every symmetric convex body of volume at least 2^n det(L) contains a nonzero lattice point.
prereqs: [lattice, lattice-determinant, convex-set]
see_also: [minkowski-second-theorem, hermite-constant, successive-minima, shortest-vector-problem, gaussian-heuristic, lll-approximation-guarantee, simultaneous-diophantine-approximation, pigeonhole-principle]
sources:
  - book: isbn:9783540617884
    title: J. W. S. Cassels, An Introduction to the Geometry of Numbers, Springer, Classics in Mathematics, 1997 reprint
    locator: Chapter III, Theorems of Blichfeldt and Minkowski (Blichfeldt's lemma, the convex body theorem and the compact case)
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 1, Basics (Blichfeldt's theorem, Minkowski's convex body theorem and the bound lambda_1 at most the square root of n times det^(1/n))
  - paper: "H. F. Blichfeldt, A new principle in the geometry of numbers, with some applications, Transactions of the American Mathematical Society 15 (1914)"
    locator: pages 227 to 235 (the translation principle used in the proof)
---

Minkowski's first theorem says that a convex set that is symmetric about the origin and has volume more than $2^n \det(L)$ contains a lattice point other than the origin. It is the founding result of the geometry of numbers. Applied to a ball it gives $\lambda_1(L) \le \sqrt n \det(L)^{1/n}$: every [lattice](/lattice/) has a nonzero vector that is short compared with its [determinant](/lattice-determinant/). The proof shows that such a vector exists but gives no way to find it; finding it is the [shortest vector problem](/shortest-vector-problem/).

## Statement

**Notation.** $L \subset \mathbb{R}^n$ is a full-rank lattice with determinant $\det(L)$, and $\operatorname{vol}$ is Lebesgue measure in $\mathbb{R}^n$. A set $K$ is **symmetric** if $x \in K$ implies $-x \in K$, and **convex** if it contains the segment between any two of its points. For a lattice of rank $n$ in $\mathbb{R}^m$, apply the theorem inside $\operatorname{span}(L)$, which is isometric to $\mathbb{R}^n$.

**Lemma (Blichfeldt).** If $S \subseteq \mathbb{R}^n$ is measurable and $\operatorname{vol}(S) > \det(L)$, then there are $x \ne y$ in $S$ with $x - y \in L$.

**Theorem (Minkowski).** Let $K \subseteq \mathbb{R}^n$ be convex and symmetric.

1. If $\operatorname{vol}(K) > 2^n \det(L)$, then $K$ contains a point of $L \setminus \{0\}$.
2. If $K$ is also compact and $\operatorname{vol}(K) \ge 2^n \det(L)$, the same holds.

**Corollary.** With $V_n = \pi^{n/2} / \Gamma(n/2 + 1)$ the volume of the unit ball,

$$\lambda_1(L) \le 2 \left( \frac{\det(L)}{V_n} \right)^{1/n} \le \sqrt n\, \det(L)^{1/n}.$$

## In plain words

Draw a lattice of points on a sheet, and draw a shape around the origin that is the same on both sides of the origin and has no dents, such as a disc, an ellipse or a square. If the shape is large enough, it must hit another lattice point. "Large enough" means its area is more than four times the area of one tile of the lattice; in higher dimensions the factor is two to the power of the dimension.

The proof cuts the half-size shape into pieces, one for each tile, and slides all pieces into one tile. The pieces have more area than the tile, so two of them overlap, and the overlap gives two points of the half-size shape whose difference is a lattice point. The symmetry and the lack of dents then place that lattice point inside the full shape.

## Proof

*Proof of the lemma.* Let $\mathcal{P} = \mathcal{P}(B)$ be the fundamental parallelepiped of a basis $B$ of $L$. The translates $v + \mathcal{P}$, $v \in L$, are pairwise disjoint and cover $\mathbb{R}^n$, and $\operatorname{vol}(\mathcal{P}) = \det(L)$. For $v \in L$ let $S_v = (S \cap (v + \mathcal{P})) - v$, a measurable subset of $\mathcal{P}$. The sets $S \cap (v + \mathcal{P})$ partition $S$ into countably many parts, and translation keeps volume, so

$$\sum_{v \in L} \operatorname{vol}(S_v) = \operatorname{vol}(S) > \det(L) = \operatorname{vol}(\mathcal{P}).$$

If the sets $S_v$ were pairwise disjoint, their union would be a subset of $\mathcal{P}$ of volume $\sum_v \operatorname{vol}(S_v) > \operatorname{vol}(\mathcal{P})$, which is impossible. So there are $u \ne v$ in $L$ and a point $z \in S_u \cap S_v$. Then $x = z + u$ and $y = z + v$ are in $S$, $x \ne y$, and $x - y = u - v \in L$. $\square$

*Proof of part 1.* Let $S = \tfrac12 K = \{x / 2 : x \in K\}$. Then $\operatorname{vol}(S) = 2^{-n} \operatorname{vol}(K) > \det(L)$. By the lemma there are $x \ne y$ in $S$ with $w = x - y \in L$, and $w \ne 0$. Now $2x \in K$ and $2y \in K$, so $-2y \in K$ by symmetry. By convexity the midpoint $\tfrac12 (2x) + \tfrac12 (-2y) = x - y = w$ is in $K$. $\square$

*Proof of part 2.* For each integer $k \ge 1$ the set $(1 + 1/k) K$ is convex and symmetric, with volume $(1 + 1/k)^n \operatorname{vol}(K) > 2^n \det(L)$ (here $\operatorname{vol}(K) > 0$, since $\operatorname{vol}(K) \ge 2^n \det(L) > 0$). By part 1 it contains some $w_k \in L \setminus \{0\}$. All $w_k$ lie in the bounded set $2K$, which contains only finitely many lattice points, so one point $w \ne 0$ equals $w_k$ for infinitely many $k$. Then $w \in (1 + 1/k) K$ for arbitrarily large $k$, and since $K$ is closed, $w \in \bigcap_k (1 + 1/k) K = K$. $\square$

*Proof of the corollary.* The closed ball of radius $r = 2 (\det(L) / V_n)^{1/n}$ is compact, convex and symmetric, with volume $V_n r^n = 2^n \det(L)$. By part 2 it contains a nonzero lattice vector, so $\lambda_1 \le r$. For the second bound, the cube $[-d, d]^n$ with $d = \det(L)^{1/n}$ has volume $2^n \det(L)$, so it contains a nonzero $w \in L$ with $|w_k| \le d$ for all $k$, and $\|w\| \le \sqrt n\, d$. $\blacksquare$

## Consequences

- **The Hermite constant is finite.** The corollary gives $\gamma_n \le 4 / V_n^{2/n} \le n$ for the [Hermite constant](/hermite-constant/) $\gamma_n = \sup_L \lambda_1(L)^2 / \det(L)^{2/n}$. Every bound of the form $\|b_1\| \le \text{factor} \cdot \det(L)^{1/n}$ for reduced bases, such as the [LLL guarantee](/lll-approximation-guarantee/), is compared with it.
- **Sums of two squares.** Let $p$ be a prime with $p \equiv 1 \pmod 4$, and let $s^2 \equiv -1 \pmod p$. The lattice $L = \{(a, b) \in \mathbb{Z}^2 : b \equiv s a \pmod p\}$, with basis $(1, s), (0, p)$, has $\det = p$. The open disc $a^2 + b^2 < 2p$ has area $2 \pi p > 4p$, so it holds a nonzero $(a, b) \in L$. Then $a^2 + b^2 \equiv a^2 (1 + s^2) \equiv 0 \pmod p$ and $0 < a^2 + b^2 < 2p$, so $a^2 + b^2 = p$. For $p = 13$ and $s = 5$ the disc contains $\pm(2, -3)$ and $\pm(3, 2)$, and $4 + 9 = 13$. The same method with a lattice in $\mathbb{Z}^4$ proves Lagrange's four-square theorem.
- **Diophantine approximation.** Applied to a box, the theorem gives Dirichlet's theorem on [simultaneous Diophantine approximation](/simultaneous-diophantine-approximation/): for reals $\alpha_1, \ldots, \alpha_k$ and $Q \ge 1$ there is an integer $1 \le q \le Q^k$ with $|q \alpha_i - p_i| \le 1/Q$ for all $i$.
- **Linear forms.** For a real invertible $n \times n$ matrix $A$ and positive $c_1, \ldots, c_n$ with $\prod c_i \ge |\det A|$, there is a nonzero $x \in \mathbb{Z}^n$ with $|(A x)_1| \le c_1$ and $|(A x)_i| < c_i$ for $i \ge 2$ (Minkowski's linear forms theorem).
- **[Successive minima](/successive-minima/).** [Minkowski's second theorem](/minkowski-second-theorem/) strengthens the first: $\prod_i \lambda_i \le 2^n \det(L) / V_n$.
- **Algorithms.** The bound $\sqrt n \det(L)^{1/n}$ is the radius used to start [enumeration](/lattice-enumeration/) when nothing better is known, and the existence of short vectors in the lattices built by [Coppersmith's method](/coppersmith-method/) and by knapsack attacks is argued with it.

## Tightness

- **The constant $2^n$.** For $L = \mathbb{Z}^n$, the open cube $(-1, 1)^n$ is convex and symmetric with volume exactly $2^n = 2^n \det(L)$, and it contains no nonzero integer point. So part 1 fails with $\ge$ in place of $>$ for sets that are not closed, and the factor $2^n$ cannot be lowered for any $n$. The closed cube $[-1, 1]^n$ shows that part 2 is also sharp: its only nonzero lattice points are on its boundary.
- **Convexity and symmetry are needed.** For $L = \mathbb{Z}^2$, the strip $\{(x, y) : 0.1 < x < 0.9\}$ is convex, has infinite area and contains no lattice point, but it is not symmetric. The set $\{(x, y) : 0.1 < |x| < 0.9\}$ is symmetric, has infinite area and contains no lattice point, but it is not convex.
- **The corollary.** The bound $\lambda_1 \le \sqrt n \det(L)^{1/n}$ is tight up to a constant factor: by the Minkowski-Hlawka theorem there are lattices with $\lambda_1 \ge c \sqrt n \det(L)^{1/n}$ for a constant $c > 0$, and the [Gaussian heuristic](/gaussian-heuristic/) predicts $\lambda_1 \approx \sqrt{n / (2 \pi e)} \det(L)^{1/n}$ for random lattices. For $\mathbb{Z}^n$ the bound is far from tight: $\lambda_1 = 1$ while $\sqrt n \det^{1/n} = \sqrt n$.

## History

Hermann Minkowski proved the convex body theorem around 1889 and published it in his book *Geometrie der Zahlen* (1896), which founded the geometry of numbers. Hans Blichfeldt gave the translation principle of the lemma in 1914, which yields the short proof above. The compact case and the many applications are in Cassels, Chapter III.

## References
