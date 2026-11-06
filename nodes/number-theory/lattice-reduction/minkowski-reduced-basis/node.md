---
tag: Z7WRP1
kind: definition
slug: minkowski-reduced-basis
name: Minkowski-reduced basis
aliases:
- Minkowski reduction
- Minkowski reduced basis
area: number-theory/lattice-reduction
level: advanced
summary: Basis whose i-th vector is a shortest vector completing the first i-1 vectors to a primitive set.
prereqs: [lattice-basis, successive-minima]
see_also: [lagrange-gauss-reduction, hkz-reduction, lll-reduction, minkowski-second-theorem, hermite-constant, shortest-vector-problem, lattice-basis-reduction]
sources:
  - book: isbn:9783642261640
    title: Phong Q. Nguyen and Brigitte Vallée (editors), The LLL Algorithm, Survey and Applications, Springer, 2010
    locator: Chapter 2, Phong Q. Nguyen, Hermite's constant and lattice algorithms (Minkowski reduction, its comparison with the successive minima and with HKZ reduction)
  - book: isbn:9783540617884
    title: J. W. S. Cassels, An Introduction to the Geometry of Numbers, Springer, Classics in Mathematics, 1997 reprint
    locator: Chapter VIII, Successive minima (bases related to the successive minima)
  - paper: "P. Q. Nguyen and D. Stehlé, Low-dimensional lattice basis reduction revisited, ACM Transactions on Algorithms 5(4), Article 46 (2009)"
    locator: the greedy algorithm, which computes a Minkowski-reduced basis in dimension at most 4 with quadratic bit complexity
---

A Minkowski-reduced basis is built greedily: its first vector is a shortest nonzero vector of the lattice, and each next vector is a shortest lattice vector that, together with the vectors already chosen, can still be extended to a basis. It is the strongest classical notion of reduction, it agrees with [Lagrange-Gauss reduction](/lagrange-gauss-reduction/) in dimension 2, and up to dimension 4 its vectors reach the [successive minima](/successive-minima/). Computing one includes the [shortest vector problem](/shortest-vector-problem/), so it is hard in high dimension, and practical algorithms use the weaker [LLL](/lll-reduction/) or [HKZ](/hkz-reduction/) notions instead.

## Definition

**Notation.** As on all pages of this area: basis rows $b_1, \ldots, b_n$ of a lattice $L$ of rank $n$, Gram-Schmidt vectors $b_i^*$, coefficients $\mu_{ij}$ and successive minima $\lambda_1 \le \cdots \le \lambda_n$. A set of lattice vectors $v_1, \ldots, v_k$ is **primitive** if it can be extended to a basis of $L$; see [lattice basis](/lattice-basis/).

A basis $b_1, \ldots, b_n$ of $L$ is **Minkowski-reduced** if for each $i = 1, \ldots, n$,

$$\|b_i\| \le \|v\| \quad \text{for every } v \in L \text{ such that } b_1, \ldots, b_{i-1}, v \text{ is primitive.}$$

In coordinates: if $v = \sum_j x_j b_j$ with $x_j \in \mathbb{Z}$, the set $b_1, \ldots, b_{i-1}, v$ is primitive exactly when $\gcd(x_i, x_{i+1}, \ldots, x_n) = 1$. So the condition is

$$\|b_i\| \le \Big\| \sum_{j=1}^n x_j b_j \Big\| \quad \text{for all integers } x_j \text{ with } \gcd(x_i, \ldots, x_n) = 1.$$

*Why the gcd.* The set $b_1, \ldots, b_{i-1}, v$ is primitive if and only if the vector $(x_i, \ldots, x_n)$ is primitive in $\mathbb{Z}^{n-i+1}$, which means its entries have gcd 1; then it is the first row of a unimodular matrix, which together with $b_1, \ldots, b_{i-1}$ gives a basis.

**Basic properties.**

- **Existence.** Choose $b_1, b_2, \ldots$ greedily; at step $i$ a shortest admissible vector exists because the admissible vectors form a nonempty set of lattice vectors, and a ball holds only finitely many. The result is primitive at each step, so it is a basis.
- **Sorted lengths.** $\|b_1\| \le \|b_2\| \le \cdots \le \|b_n\|$, because $b_{i+1}$ is admissible at step $i$ ($x_{i+1} = 1$).
- **First vector.** $\|b_1\| = \lambda_1$, since every primitive vector is admissible at step 1, and every shortest vector is primitive.
- **Pairwise condition.** For $j < i$ and $k \in \mathbb{Z}$, $b_i - k b_j$ is admissible at step $i$, so $\|b_i\| \le \|b_i - k b_j\|$, which gives $|\langle b_i, b_j \rangle| \le \frac12 \|b_j\|^2$. This is a condition on $b_j$, not on $b_j^*$, so it is not the same as [size reduction](/size-reduction/).
- **Minima.** If a basis has $\|b_i\| = \lambda_i$ for all $i$, it is Minkowski-reduced. *Proof.* Let $v$ be admissible at step $i$ with $\|v\| < \lambda_i$, and let $j \le i$ be the least index with $\lambda_j = \lambda_i$. Then $b_1, \ldots, b_{j-1}, v$ are $j$ independent vectors, all shorter than $\lambda_j$, which contradicts the definition of $\lambda_j$. $\square$ Conversely, for $n \le 4$ every Minkowski-reduced basis has $\|b_i\| = \lambda_i$ for all $i$; in general one has $\lambda_i \le \|b_i\| \le \max\big(1, (5/4)^{(i-4)/2}\big) \lambda_i$.
- **Bounded defect.** By the last bound and [Minkowski's second theorem](/minkowski-second-theorem/), $\prod_i \|b_i\| \le c_n \det(L)$ with $c_n$ depending only on $n$.
- **Finitely many conditions.** Minkowski proved that in each dimension a finite set of coefficient vectors $x$ suffices in the definition. So the Gram matrices of Minkowski-reduced bases form a cone in the space of symmetric matrices cut out by finitely many linear inequalities, the Minkowski domain, used in the reduction theory of quadratic forms.

## Examples and non-examples

**Examples.**

- **Dimension 2.** A basis $b_1, b_2$ is Minkowski-reduced if and only if $\|b_1\| \le \|b_2\| \le \|b_2 + k b_1\|$ for all integers $k$, that is, $\|b_1\| \le \|b_2\|$ and $|\mu_{21}| \le 1/2$: the definition of a [Lagrange-Gauss reduced](/lagrange-gauss-reduction/) basis. For example, $(2, 0), (-1, 2)$.
- **A basis that reaches the minima.** $(0, 1, 0), (1, 0, 1), (-2, 0, 1)$ has lengths $1, \sqrt 2, \sqrt 5$, which are the three successive minima of the lattice it generates. By the property above it is Minkowski-reduced.
- **$\mathbb{Z}^n$.** The standard basis, and any signed permutation of it.

**Non-examples.**

- **LLL-reduced is weaker.** $(4, 0), (2, 3)$ is LLL-reduced with $\delta = 3/4$, but $(2, 3)$ is shorter than $(4, 0)$, so it is not Minkowski-reduced. Its Minkowski-reduced form is $(2, 3), (-2, 3)$, with $|\mu_{21}| = 5/13$.
- **The minima need not be reached in dimension 5.** Let $L = \mathbb{Z}^5 \cup (\mathbb{Z}^5 + h)$ with $h = (\frac12, \ldots, \frac12)$. Then $\lambda_1 = \cdots = \lambda_5 = 1$, but $e_1, \ldots, e_5$ is not a basis of $L$. The basis $e_1, e_2, e_3, e_4, h$ is Minkowski-reduced: $e_1, \ldots, e_4$ have length 1, and an admissible vector at step 5 has the form $\pm h + \sum_{j \le 4} x_j e_j$, whose five coordinates are all half-integers, so its squared length is at least $5/4 = \|h\|^2$. So $\|b_5\| = \sqrt 5 / 2 > \lambda_5$, which matches the bound $(5/4)^{1/2}$.
- **Not sorted.** Any basis with $\|b_1\| > \|b_2\|$ fails, since $b_2$ is admissible at step 1.

## Related definitions

- **[Lagrange-Gauss reduction](/lagrange-gauss-reduction/).** The case $n = 2$, and an algorithm to compute it.
- **[HKZ reduction](/hkz-reduction/).** Projects instead of completing: $b_i^*$ must be a shortest vector of the projected lattice $\pi_i(L)$, plus size reduction. HKZ and Minkowski reduction agree in dimension 2 and differ in general; both give $\|b_i\| \le c_n \lambda_i$.
- **[LLL-reduced basis](/lll-reduction/).** A relaxation that is computable in polynomial time, with exponential constants in place of the constants of Minkowski reduction.
- **[Successive minima](/successive-minima/).** Minkowski reduction is the basis version of the minima: the minima are reached by independent vectors, the Minkowski basis by a basis.
- **[Hermite constant](/hermite-constant/).** The first vector of a Minkowski-reduced basis has $\|b_1\|^2 = \lambda_1^2 \le \gamma_n \det(L)^{2/n}$.
- **Greedy reduction.** The greedy algorithm of Semaev, and of Nguyen and Stehlé, computes a Minkowski-reduced basis for $n \le 4$ in time quadratic in the bit size; from dimension 5 on it can fail to produce one.

## References
