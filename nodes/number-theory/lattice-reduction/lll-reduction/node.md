---
tag: N7FJKD
kind: definition
slug: lll-reduction
name: LLL-reduced basis
aliases:
- Lenstra-Lenstra-Lovász reduced basis
- Lovász-reduced basis
- delta-LLL-reduced basis
area: number-theory/lattice-reduction
level: advanced
summary: Basis that is size-reduced and satisfies the Lovász condition.
prereqs: [lattice-basis, gram-schmidt-orthogonalization, size-reduction, lovasz-condition]
see_also: [lll-algorithm, lll-approximation-guarantee, hkz-reduction, minkowski-reduced-basis, deep-lll, bkz-algorithm, root-hermite-factor, lattice-basis-reduction]
sources:
  - paper: doi:10.1007/BF01457454
    title: A. K. Lenstra, H. W. Lenstra Jr. and L. Lovász, Factoring polynomials with rational coefficients, Mathematische Annalen 261, 1982
    locator: Section 1 (the definition of a reduced basis by conditions (1.4) and (1.5), and the bounds on its vectors)
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 2, Approximation algorithms (LLL reduced bases for a general parameter delta and the bounds on the first vector)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Springer, Graduate Texts in Mathematics 138, 1993
    locator: Section 2.6 (LLL-reduced bases and their properties)
---

An LLL-reduced basis is a [lattice basis](/lattice-basis/) that is [size-reduced](/size-reduction/) and satisfies the [Lovász condition](/lovasz-condition/) at every index, for a parameter $\delta$ with $1/4 < \delta < 1$. It is weaker than the classical notions of Minkowski and HKZ reduction, but it can be computed in polynomial time by the [LLL algorithm](/lll-algorithm/), and its first vector is within a factor $\alpha^{(n-1)/2}$ of the shortest, with $\alpha = 1 / (\delta - 1/4)$. Every bound on an LLL-reduced basis comes from one fact: the Gram-Schmidt lengths fall by at most a factor $\sqrt\alpha$ from each index to the next.

## Definition

**Notation.** As on all pages of this area: basis rows $b_1, \ldots, b_n \in \mathbb{R}^m$ of a lattice $L$, [Gram-Schmidt](/gram-schmidt-orthogonalization/) vectors $b_i^*$, coefficients $\mu_{ij}$, the first minimum $\lambda_1$ and the determinant $\det(L) = \prod_i \|b_i^*\|$. We write $B_i = \|b_i^*\|^2$ and $\alpha = 1 / (\delta - 1/4)$, so $\alpha \ge 4/3$, and $\alpha = 2$ for $\delta = 3/4$.

Let $1/4 < \delta \le 1$. The basis is **$\delta$-LLL-reduced** if

1. (size reduction) $|\mu_{ij}| \le \frac12$ for all $1 \le j < i \le n$, and
2. (Lovász condition) $\delta\, B_{k-1} \le B_k + \mu_{k,k-1}^2 B_{k-1}$ for all $2 \le k \le n$.

"LLL-reduced" without a parameter means $\delta = 3/4$. The value $\delta = 1$ is allowed by the definition, but the LLL algorithm is only known to run in polynomial time for $\delta < 1$.

**Basic consequences.** Let the basis be $\delta$-LLL-reduced. Then for $1 \le j \le i \le n$:

- (a) $B_j \le \alpha^{i-j} B_i$.
- (b) $\|b_i\|^2 \le \alpha^{i-1} B_i$.
- (c) $\|b_j\|^2 \le \alpha^{i-1} B_i$.
- (d) $\|b_1\| \le \alpha^{(n-1)/4} \det(L)^{1/n}$ and $\prod_{i=1}^n \|b_i\| \le \alpha^{n(n-1)/4} \det(L)$.
- (e) $\|b_1\| \le \alpha^{(n-1)/2} \lambda_1(L)$.

*Proof.* (a) Conditions 1 and 2 give $B_k \ge (\delta - \mu_{k,k-1}^2) B_{k-1} \ge (\delta - \frac14) B_{k-1} = B_{k-1} / \alpha$; apply it $i - j$ times. (b) By orthogonality, condition 1 and (a),

$$\|b_i\|^2 = B_i + \sum_{j < i} \mu_{ij}^2 B_j \le B_i \Big(1 + \frac14 \sum_{j=1}^{i-1} \alpha^{i-j}\Big) = B_i \Big(1 + \frac{\alpha^i - \alpha}{4 (\alpha - 1)}\Big).$$

The last factor is at most $\alpha^{i-1}$: multiplied by $4(\alpha - 1)$, this is $3 \alpha - 4 \le \alpha^{i-1} (3 \alpha - 4)$, true because $\alpha \ge 4/3$. (c) By (b) and (a), $\|b_j\|^2 \le \alpha^{j-1} B_j \le \alpha^{j-1} \alpha^{i-j} B_i$. (d) By (c) with $j = 1$, $\|b_1\|^{2n} \le \prod_i \alpha^{i-1} B_i = \alpha^{n(n-1)/2} \det(L)^2$; and by (b), $\prod_i \|b_i\|^2 \le \alpha^{n(n-1)/2} \prod_i B_i$. (e) Every nonzero lattice vector $v = \sum_{j \le k} x_j b_j$ with $x_k \ne 0$ has $\|v\|^2 \ge x_k^2 B_k \ge B_k \ge \alpha^{-(k-1)} \|b_1\|^2 \ge \alpha^{-(n-1)} \|b_1\|^2$, using (c). $\square$

The full set of bounds, including $\|b_j\| \le \alpha^{(n-1)/2} \lambda_i$ for $j \le i$ and the question of how tight they are, is on the [LLL approximation guarantee](/lll-approximation-guarantee/) page.

## Examples and non-examples

**Examples.**

- **A reduced basis in dimension 3.** The basis $(0, 1, 0), (1, 0, 1), (-2, 0, 1)$ has $B_1 = 1$, $B_2 = 2$, $B_3 = 9/2$, $\mu_{21} = \mu_{31} = 0$ and $\mu_{32} = -1/2$. It is size-reduced, and the Lovász conditions $\frac34 \cdot 1 \le 2$ and $\frac34 \cdot 2 \le \frac92 + \frac14 \cdot 2$ hold. It is the output of LLL on the basis $(1, 1, 1), (-1, 0, 2), (3, 5, 6)$, and here $b_1$ is a shortest vector.
- **Dimension 2.** $(2, 0), (-1, 2)$ has $B_1 = B_2 = 4$ and $\mu_{21} = -1/2$. It is $\delta$-LLL-reduced for every $\delta \le 1$, and for $\delta = 1$ in dimension 2 this is the same as [Lagrange-Gauss reduced](/lagrange-gauss-reduction/).
- **Orthogonal bases.** An orthogonal basis is size-reduced, and it satisfies the Lovász condition if and only if $B_{k-1} \le B_k / \delta$ for every $k$; for example any orthogonal basis sorted by increasing length.

**Non-examples.**

- **Size-reduced but badly ordered.** $(1, 1, 1), (-1, 0, 2), (0, 1, 0)$ is size-reduced, with $B_2 = 14/3$, $B_3 = 9/14$ and $\mu_{32} = -1/14$, but $\frac34 \cdot \frac{14}{3} = \frac72 > \frac{9}{14} + \frac{1}{196} \cdot \frac{14}{3} = \frac23$, so the Lovász condition fails at $k = 3$.
- **Reduced, but the first vector is not shortest.** $(4, 0), (2, 3)$ has $B_1 = 16$, $\mu_{21} = 1/2$, $B_2 = 9$, and $\frac34 \cdot 16 = 12 \le 9 + 4$, so it is $\frac34$-LLL-reduced. But $\|b_2\|^2 = 13 < 16 = \|b_1\|^2$, and $\lambda_1 = \sqrt{13}$. The ratio $\|b_1\| / \lambda_1 = 4 / \sqrt{13} \approx 1.11$ is within the bound $\alpha^{1/2} = \sqrt 2$. With $\delta = 1$ this basis is not reduced, since $16 > 13$.
- **Not unique.** The same lattice has the reduced basis $(2, 3), (-2, 3)$ as well, with $B_1 = 13$, $\mu_{21} = 5/13$ and $B_2 = 144/13$. A lattice has in general many LLL-reduced bases, and the one that the algorithm returns depends on the input basis.

## Related definitions

- **[Lovász condition](/lovasz-condition/) and [size reduction](/size-reduction/).** The two parts of the definition.
- **[LLL algorithm](/lll-algorithm/).** Computes a $\delta$-LLL-reduced basis in polynomial time for any fixed $\delta < 1$.
- **[HKZ reduction](/hkz-reduction/).** Asks that each $b_i^*$ be a shortest vector of the projected lattice $\pi_i(L)$, which is much stronger: the Lovász condition only compares $b_{k-1}^*$ with one candidate, $\pi_{k-1}(b_k)$.
- **[Minkowski-reduced basis](/minkowski-reduced-basis/).** The classical notion, where each $b_i$ is as short as possible among vectors that extend $b_1, \ldots, b_{i-1}$ to part of a basis.
- **[BKZ](/bkz-algorithm/) and [deep LLL](/deep-lll/).** Stronger reductions that interpolate between LLL and HKZ.
- **[Root Hermite factor](/root-hermite-factor/).** In practice LLL outputs bases with $\|b_1\| \approx 1.02^n \det(L)^{1/n}$, much better than the bound (d) with $\alpha^{1/4} \approx 1.075$ for $\delta$ near 1.

## References
