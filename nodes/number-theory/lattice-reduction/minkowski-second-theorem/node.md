---
tag: XAWYRF
kind: theorem
slug: minkowski-second-theorem
name: Minkowski's second theorem
aliases:
- Minkowski's second theorem on successive minima
- Minkowski's theorem on successive minima
area: number-theory/lattice-reduction
level: advanced
summary: Relates the product of successive minima to the lattice determinant up to a dimension factor.
prereqs: [minkowski-theorem, successive-minima, hermite-constant]
see_also: [lattice-determinant, gram-schmidt-orthogonalization, minkowski-reduced-basis, hkz-reduction, shortest-independent-vectors-problem, lattice-basis]
sources:
  - book: isbn:9783540617884
    title: J. W. S. Cassels, An Introduction to the Geometry of Numbers, Springer, Classics in Mathematics, 1997 reprint
    locator: Chapter VIII, Successive minima (Minkowski's second theorem for a general symmetric convex body, with a full proof of the upper bound)
  - book: isbn:9783642261640
    title: Phong Q. Nguyen and Brigitte Vallée (editors), The LLL Algorithm, Survey and Applications, Springer, 2010
    locator: Chapter 2, Phong Q. Nguyen, Hermite's constant and lattice algorithms (the form with the Hermite constant and its use for reduced bases)
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 1, Basics (Minkowski's theorems for the Euclidean norm)
---

Minkowski's second theorem bounds the product of all the [successive minima](/successive-minima/) of a lattice by its [determinant](/lattice-determinant/): $\det(L) \le \lambda_1 \lambda_2 \cdots \lambda_n \le \gamma_n^{n/2} \det(L)$, where $\gamma_n \le n$ is the [Hermite constant](/hermite-constant/). It strengthens [Minkowski's first theorem](/minkowski-theorem/), which bounds $\lambda_1$ alone: the minima can be unequal, but their geometric mean behaves like $\det(L)^{1/n}$. It is the reason why a basis whose vectors are close to the minima has a small orthogonality defect.

## Statement

**Notation.** $L$ is a lattice of rank $n$ with successive minima $\lambda_1 \le \cdots \le \lambda_n$ in the Euclidean norm, $V_n$ is the volume of the unit ball of $\mathbb{R}^n$, and $\gamma_n = \sup_L \lambda_1(L)^2 / \det(L)^{2/n}$ is the Hermite constant. For a compact convex set $K$ that is symmetric about the origin and has nonempty interior, $\lambda_i(K, L)$ is the least $r$ such that $r K$ contains $i$ independent lattice vectors.

**Theorem (Euclidean form).** For every lattice $L$ of rank $n$,

$$\det(L) \;\le\; \prod_{i=1}^n \lambda_i(L) \;\le\; \gamma_n^{n/2} \det(L) \;\le\; \frac{2^n}{V_n} \det(L).$$

So $\big(\prod_i \lambda_i\big)^{1/n} \le \sqrt{\gamma_n}\, \det(L)^{1/n} \le \sqrt n\, \det(L)^{1/n}$.

**Theorem (convex body form, Minkowski).** For $K$ as above and a full-rank lattice $L \subset \mathbb{R}^n$,

$$\frac{2^n}{n!} \frac{\det(L)}{\operatorname{vol}(K)} \;\le\; \prod_{i=1}^n \lambda_i(K, L) \;\le\; \frac{2^n \det(L)}{\operatorname{vol}(K)}.$$

## In plain words

Minkowski's first theorem says that a lattice with small cells must have a short nonzero vector. But it says nothing about the other directions: the lattice could be very dense along one line and sparse across it.

The second theorem looks at all directions at once. It takes the shortest vector, then the shortest vector in a new direction, and so on, until the vectors fill the space. Multiply their lengths. The theorem says that this product is never smaller than the volume of one cell, and never larger than that volume times a number that depends only on the dimension. So if some of these lengths are very short, others must be long, and the other way round.

## Proof

We prove the Euclidean form in full, and the lower bound of the convex body form. Fix independent $v_1, \ldots, v_n \in L$ with $\|v_i\| = \lambda_i$; they exist by the greedy argument on the [successive minima](/successive-minima/) page. Let $v_1^*, \ldots, v_n^*$ be their [Gram-Schmidt](/gram-schmidt-orthogonalization/) vectors. We work in $\operatorname{span}(L)$, identified with $\mathbb{R}^n$.

**Lower bound.** The vectors $v_i$ generate a sublattice $L' \subseteq L$ of rank $n$, so $\det(L') = [L : L'] \det(L) \ge \det(L)$. By the product formula and $\|v_i^*\| \le \|v_i\|$,

$$\det(L) \le \det(L') = \prod_i \|v_i^*\| \le \prod_i \|v_i\| = \prod_i \lambda_i.$$

**Upper bound.** Let $T$ be the linear map that divides the component along $v_i^*$ by $\lambda_i$:

$$T(y) = \sum_{i=1}^n \frac{\langle y, v_i^* \rangle}{\lambda_i \|v_i^*\|^2} v_i^*, \qquad \|T(y)\|^2 = \sum_{i=1}^n \frac{\langle y, v_i^* \rangle^2}{\lambda_i^2 \|v_i^*\|^2}.$$

*Claim: $\|T(y)\| \ge 1$ for every $y \in L \setminus \{0\}$.* Let $k$ be the least index with $y \in \operatorname{span}(v_1, \ldots, v_k)$; it exists because the $v_i$ span the space. Then $y \notin \operatorname{span}(v_1, \ldots, v_{k-1})$.

*Step 1.* Since $y \in \operatorname{span}(v_1^*, \ldots, v_k^*)$, only the terms $i \le k$ are nonzero, and $\lambda_i \le \lambda_k$ for $i \le k$, so

$$\|T(y)\|^2 \ge \frac{1}{\lambda_k^2} \sum_{i \le k} \frac{\langle y, v_i^* \rangle^2}{\|v_i^*\|^2} = \frac{\|y\|^2}{\lambda_k^2}.$$

*Step 2: $\|y\| \ge \lambda_k$.* The $k$ vectors $v_1, \ldots, v_{k-1}, y$ are independent. Suppose $\|y\| < \lambda_k$. Let $j$ be the least index with $\lambda_j = \lambda_k$, so $j \le k$. Since $v_1, \ldots, v_{k-1}, y$ are independent, so are the $j$ vectors $v_1, \ldots, v_{j-1}, y$, all of length less than $\lambda_k = \lambda_j$ (because $\lambda_i < \lambda_j$ for $i < j$). That contradicts the definition of $\lambda_j$. So $\|y\| \ge \lambda_k$ and $\|T(y)\| \ge 1$, which proves the claim.

*Conclusion.* $T$ is invertible and maps $L$ to the lattice $T(L)$ of rank $n$. In the orthonormal basis $v_i^* / \|v_i^*\|$, $T$ is diagonal with entries $1 / \lambda_i$, so $\det(T(L)) = \det(L) / \prod_i \lambda_i$. By the claim $\lambda_1(T(L)) \ge 1$, and by the definition of $\gamma_n$,

$$1 \le \lambda_1(T(L))^2 \le \gamma_n \det(T(L))^{2/n} = \gamma_n \left( \frac{\det(L)}{\prod_i \lambda_i} \right)^{2/n}.$$

Raising to the power $n/2$ gives $\prod_i \lambda_i \le \gamma_n^{n/2} \det(L)$. Finally, the corollary of [Minkowski's first theorem](/minkowski-theorem/) gives $\gamma_n \le 4 / V_n^{2/n}$, so $\gamma_n^{n/2} \le 2^n / V_n$. $\square$

**Lower bound of the convex body form.** Take independent $v_i \in L$ with $v_i \in \lambda_i(K, L) K$; they exist by the same greedy argument, and the minimum is attained because $K$ is compact. The points $\pm v_i / \lambda_i(K, L)$ lie in $K$, so by convexity $K$ contains their convex hull, a cross-polytope of volume $\frac{2^n}{n!} |\det(v_1, \ldots, v_n)| / \prod_i \lambda_i(K, L)$. Since $|\det(v_1, \ldots, v_n)| = \det(L') \ge \det(L)$, this gives the lower bound. $\square$

**Upper bound of the convex body form.** For a general $K$ the map $T$ above does not work, because $K$ is not an ellipsoid. Minkowski's proof, in a simplified form, is in Cassels, Chapter VIII; it shrinks $K$ in the directions of the minima step by step and applies the first theorem to the result. We do not reproduce it here. $\blacksquare$

## Consequences

- **Short vectors in all directions.** The vectors that reach the minima generate a sublattice of index $[L : L'] = \det(L') / \det(L) \le \prod_i \lambda_i / \det(L) \le \gamma_n^{n/2}$, a bound that depends only on $n$.
- **Reduced bases have bounded orthogonality defect.** For a [Minkowski-reduced](/minkowski-reduced-basis/) or [HKZ-reduced](/hkz-reduction/) basis, $\|b_i\| \le c_n \lambda_i$ for a constant $c_n$ depending only on $n$, so $\prod_i \|b_i\| \le c_n^n \gamma_n^{n/2} \det(L)$.
- **Analysis of LLL.** An [LLL-reduced](/lll-reduction/) basis satisfies $\|b_i\| \le \alpha^{(n-1)/2} \lambda_i$, and together with the theorem this bounds its orthogonality defect by $\alpha^{n(n-1)/2} \gamma_n^{n/2}$; the direct bound $\prod_i \|b_i\| \le \alpha^{n(n-1)/4} \det(L)$ is better.
- **The last minimum is long.** Since $\lambda_n$ is the largest factor, $\lambda_n^n \ge \prod_i \lambda_i \ge \det(L)$, so $\lambda_n \ge \det(L)^{1/n}$. This is why the [shortest independent vectors problem](/shortest-independent-vectors-problem/) is measured against $\lambda_n$: no set of $n$ independent vectors can all be shorter than $\det(L)^{1/n}$.
- **First theorem as a special case.** Since $\lambda_1$ is the smallest factor, $\lambda_1^n \le \prod_i \lambda_i \le \gamma_n^{n/2} \det(L)$, which is the definition of $\gamma_n$ again; the second theorem is never weaker than the first.

## Tightness

- **Upper bound, Euclidean form.** The hexagonal lattice with basis $(1, 0), (1/2, \sqrt 3 / 2)$ has $\lambda_1 = \lambda_2 = 1$ and $\det = \sqrt 3 / 2$, and $\gamma_2 = 2 / \sqrt 3$. Then $\gamma_2^{2/2} \det = 1 = \lambda_1 \lambda_2$: equality. In general equality holds for every lattice that reaches $\gamma_n$ and has $\lambda_1 = \cdots = \lambda_n$.
- **Lower bound, Euclidean form.** $\mathbb{Z}^n$ has $\prod \lambda_i = 1 = \det$: equality. Equality holds exactly when the minima are reached by an orthogonal basis.
- **Convex body form.** For $L = \mathbb{Z}^n$ and the cube $K = [-1, 1]^n$, $\operatorname{vol}(K) = 2^n$ and all $\lambda_i(K, L) = 1$, so the upper bound is an equality. For the cross-polytope $K = \{x : \sum |x_i| \le 1\}$, of volume $2^n / n!$, again all $\lambda_i = 1$, so the lower bound is an equality.
- **An example in between.** The lattice with basis $(0, 1, 0), (1, 0, 1), (-2, 0, 1)$ has $\det = 3$ and minima $1, \sqrt 2, \sqrt 5$, with product $\sqrt{10} \approx 3.16$. The upper bound is $\gamma_3^{3/2} \cdot 3 = \sqrt 2 \cdot 3 \approx 4.24$, using $\gamma_3 = 2^{1/3}$, and the weaker $2^3 \cdot 3 / V_3 \approx 5.73$.

## History

Minkowski stated and proved the theorem in *Geometrie der Zahlen* (1896). His proof of the upper bound was long and was found hard to follow, and later authors gave shorter proofs; Cassels gives one in Chapter VIII. The form with the Hermite constant and the proof through the linear map $T$ are standard in the algorithmic literature, for example in Nguyen's survey in the book of Nguyen and Vallée.

## References
