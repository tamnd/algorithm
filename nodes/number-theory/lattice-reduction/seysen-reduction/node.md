---
tag: WRVXKA
kind: algorithm
slug: seysen-reduction
name: Seysen reduction
aliases:
- Seysen's algorithm
- Seysen basis reduction
area: number-theory/lattice-reduction
level: advanced
summary: Basis reduction that minimizes a global size measure on the basis and its dual.
solves: [lattice-basis-reduction]
model: word-ram
complexity:
  vars: {n: the rank of the lattice, m: the length of the basis vectors, K: the number of basis updates which is at most n X^n for an integer basis, X: the largest squared length of an input vector of an integer basis, M: the cost M(k) of multiplying two integers of k binary digits}
  time: {worst: O(n^3 + n^2 m + (n^2 + m) K), best: O(n^3 + n^2 m)}
  space: {extra: O(n^2 + n m)}
  bit_operations: {worst: O((n^3 + n^2 m + (n^2 + m) K) M(n log X))}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1993
  people: [Martin Seysen]
  note: Published in Combinatorica as a reduction of a lattice basis and its reciprocal basis at the same time.
prereqs: [lattice-basis, dual-lattice, unimodular-matrix]
see_also: [lll-algorithm, lagrange-gauss-reduction, size-reduction, lattice-basis-reduction, lll-reduction, babai-nearest-plane, closest-vector-problem, minkowski-reduced-basis]
sources:
  - paper: "Martin Seysen, Simultaneous reduction of a lattice basis and its reciprocal basis, Combinatorica 13(3), 1993"
    locator: pages 363 to 376 (the measure S(B), the pairwise update and its optimal coefficient, and the existence of bases with small products of primal and dual lengths)
  - book: isbn:9783642261640
    title: Phong Q. Nguyen and Brigitte Vallée (editors), The LLL Algorithm, Survey and Applications, Springer, 2010
    locator: Chapter 2, Phong Q. Nguyen, Hermite's constant and lattice algorithms (reduction notions for a basis together with its dual basis)
---

Seysen reduction improves a lattice basis by reducing it and its [dual basis](/dual-lattice/) at the same time. It measures a basis by $S(B) = \sum_i \|b_i\|^2 \|d_i\|^2$, where $d_1, \ldots, d_n$ is the dual basis, and repeatedly adds an integer multiple of one basis vector to another whenever that lowers $S$, choosing the multiple that lowers it most. Unlike [LLL](/lll-algorithm/) it treats all pairs of vectors alike, with no order on the basis; it has no proved approximation factor for $\lambda_1$, and the only proved bound on its number of steps is pseudo-polynomial, but in practice it gives bases that are close to orthogonal in both directions, which is what [Babai's](/babai-nearest-plane/) and other decoding methods need.

## In plain words

A good basis is one whose vectors are short and point in very different directions. Each basis has a partner, the dual basis, whose vectors measure coordinates. When the basis is bad, the dual vectors are long, so a single number that adds up the lengths of both is a fair score of how bad a basis is.

The algorithm looks at two basis vectors at a time and asks: if I add a whole number of copies of one to the other, does the score go down? There is a best number to add, given by a short formula. If it helps, it does it. It keeps going until no pair can be improved. The score always goes down, so it must stop.

## The problem

**Notation.** As on all pages of this area: basis rows $b_1, \ldots, b_n \in \mathbb{Q}^m$ of a lattice $L$ of rank $n$, Gram matrix $G = (\langle b_i, b_j \rangle)$, and $\det(L) = \det(G)^{1/2}$. The **dual basis** is the set of rows $d_1, \ldots, d_n$ of $D = G^{-1} B$, the unique vectors in the span of $L$ with $\langle b_i, d_j \rangle = 1$ if $i = j$ and $0$ otherwise; its Gram matrix is $H = G^{-1}$, so $\|d_i\|^2 = H_{ii}$. They form a basis of the [dual lattice](/dual-lattice/).

**Seysen's measure.**

$$S(B) = \sum_{i=1}^n \|b_i\|^2 \|d_i\|^2 = \sum_{i=1}^n G_{ii} H_{ii}.$$

By Cauchy-Schwarz, $\|b_i\| \|d_i\| \ge \langle b_i, d_i \rangle = 1$, so $S(B) \ge n$, with equality exactly for orthogonal bases. More precisely, $d_i$ is orthogonal to every $b_j$ with $j \ne i$, so $\|d_i\| = 1 / \|p_i\|$ where $p_i$ is the component of $b_i$ orthogonal to the other basis vectors, and $\|b_i\| \|d_i\| = 1 / \sin \theta_i$ with $\theta_i$ the angle between $b_i$ and the span of the others. So $S$ is small when every $b_i$ is nearly orthogonal to all the others.

**Task.** Given a basis, find a basis of the same lattice that is **Seysen-reduced**: no update $b_j \leftarrow b_j + \lambda b_i$ with $i \ne j$ and $\lambda \in \mathbb{Z}$ lowers $S$.

## The algorithm

The update $b_j \leftarrow b_j + \lambda b_i$ changes the dual basis by $d_i \leftarrow d_i - \lambda d_j$, with all other vectors unchanged. Only two terms of $S$ change, and

$$\Delta S = 2 \|b_i\|^2 \|d_j\|^2 \big( \lambda^2 - 2 \lambda \lambda_{ij}^* \big), \qquad \lambda_{ij}^* = \frac12 \left( \frac{\langle d_i, d_j \rangle}{\|d_j\|^2} - \frac{\langle b_i, b_j \rangle}{\|b_i\|^2} \right).$$

So the real minimizer is $\lambda_{ij}^*$, the best integer is $\lceil \lambda_{ij}^* \rfloor$, and it lowers $S$ exactly when $|\lambda_{ij}^*| > 1/2$.

```pseudo id=main
SEYSEN(b_1..b_n)                      ▷ G and H are the Gram matrices of the basis and its dual
L1  G ← (⟨b_i, b_j⟩); H ← G⁻¹
L2  repeat
L3      changed ← false
L4      for each ordered pair (i, j) with i ≠ j do
L5          λ* ← (H_ij / H_jj − G_ij / G_ii) / 2
L6          λ ← ⌈λ*⌋
L7          if λ² − 2 λ λ* < 0 then                      ▷ the update lowers S
L8              b_j ← b_j + λ b_i
L9              G: row j += λ row i, then column j += λ column i;  H: row i −= λ row j, then column i −= λ column j
L10             changed ← true
L11 until not changed
L12 return b_1..b_n
```

Line L9 keeps $G$ and $H$ exact in $O(n)$ operations instead of recomputing $G^{-1}$: the update is $B \leftarrow T B$ with $T = I + \lambda E_{ji}$, so $G \leftarrow T G T^{\mathsf T}$ and $H \leftarrow T^{-\mathsf T} H T^{-1}$ with $T^{-1} = I - \lambda E_{ji}$. The test at line L7 is $\Delta S < 0$ divided by the positive factor $2 G_{ii} H_{jj}$. With $\lceil x \rfloor = \lfloor x + 1/2 \rfloor$, a tie $\lambda^* = \pm 1/2$ gives $\Delta S = 0$ and no update.

## Example

**Dimension 2.** Take $b_1 = (5, 3)$ and $b_2 = (8, 5)$, a basis of $\mathbb{Z}^2$. Then $G = \begin{pmatrix} 34 & 55 \\ 55 & 89 \end{pmatrix}$, $\det G = 1$, $H = \begin{pmatrix} 89 & -55 \\ -55 & 34 \end{pmatrix}$, and $S = 34 \cdot 89 + 89 \cdot 34 = 6052$.

| pair $(i, j)$ | $\lambda^*$ | $\lambda$ | new basis | $S$ |
|---|---|---|---|---|
| $(1, 2)$ | $-55/34$ | $-2$ | $(5, 3), (-2, -1)$ | $340$ |
| $(2, 1)$ | $13/5$ | $3$ | $(-1, 0), (-2, -1)$ | $10$ |
| $(1, 2)$ | $-2$ | $-2$ | $(-1, 0), (0, -1)$ | $2$ |

The next pass finds $\lambda^* = 0$ for both pairs and stops, with $S = 2 = n$: an orthogonal basis after 3 updates. In dimension 2, $H_{12} / H_{22} = -G_{12} / G_{11}$, so $\lambda_{12}^* = -G_{12} / G_{11} = -\mu_{21}$; the update is a step of [Lagrange-Gauss reduction](/lagrange-gauss-reduction/), and Seysen-reduced means $2 |G_{12}| \le \min(G_{11}, G_{22})$, which is Lagrange-Gauss reduced up to the order of the two vectors.

**Dimension 3.** For $b_1 = (1, 1, 1)$, $b_2 = (-1, 0, 2)$, $b_3 = (3, 5, 6)$, with $\det(L) = 3$, the measure starts at $S = 619/3$. Seven updates bring it to $29/9 \approx 3.22$, with the basis $(-1, 0, -1), (-2, 0, 1), (0, -1, 0)$ of lengths $\sqrt 2, \sqrt 5, 1$; these are the successive minima of this lattice, in another order. The scripts in the tests check both runs.

## Correctness

Each update is a unimodular row operation, so the rows stay a basis of $L$, and line L9 keeps $G$ and $H$ equal to the Gram matrices of the current basis and its dual. The formula for $\Delta S$ follows by expanding the two changed terms. When a full pass makes no update, every pair has $\lceil \lambda_{ij}^* \rfloor^2 - 2 \lceil \lambda_{ij}^* \rfloor \lambda_{ij}^* \ge 0$, which forces $|\lambda_{ij}^*| \le 1/2$, and then $\lambda^2 - 2 \lambda \lambda^* \ge |\lambda| (|\lambda| - 1) \ge 0$ for every integer $\lambda$: the output is Seysen-reduced. For an integer basis, $S(B) \det(G) = \sum_i G_{ii} \operatorname{adj}(G)_{ii}$ is a positive integer and $\det G$ never changes, so each update lowers it by at least 1 and the loop stops. The full proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

**Cost model.** Exact rational arithmetic on an input of $n$ linearly independent rows in $\mathbb{Q}^m$; for the bit bounds an integer basis with squared row lengths at most $X$. $K$ is the number of updates.

- **Operations (proved).** Line L1 costs $O(n^2 m)$ for $G$ and $O(n^3)$ for the inverse. Each update costs $O(n + m)$, and each pass costs $O(n^2)$ for the tests; every pass except the last makes an update, so there are at most $K + 1$ passes. The total is $O(n^3 + n^2 m + (n^2 + m) K)$, and $O(n^3 + n^2 m)$ when the input is already reduced.
- **Number of updates (proved, pseudo-polynomial).** For an integer basis, $K \le (S_0 - S_{\text{end}}) \det(G) \le S_0 \det(G) = \sum_i G_{ii} \operatorname{adj}(G)_{ii} \le n X^n$ by Hadamard's inequality on the minors. This is exponential in the input size $n \log X$; no polynomial bound on the number of updates is known to us for this greedy form.
- **Bits (proved).** Throughout, $G$ is an integer matrix, $\det(G) H = \operatorname{adj}(G)$ is an integer matrix, and their diagonal entries are at most $S_0 \det(G) \le n X^n$, so all entries, by Cauchy-Schwarz for the off-diagonal ones, have $O(n \log X)$ digits; each operation costs $O(M(n \log X))$.
- **Observed.** In practice the number of updates is far below this bound; on the small random inputs of the tests it is a few dozen at most. Seysen proved that every lattice has a basis with all products $\|b_i\| \|d_i\|$ at most $\exp(O((\log n)^2))$, but not that the algorithm finds one.
- **Space.** $O(n^2)$ for $G$ and $H$ and $O(n m)$ for the basis.

## Properties

- **Symmetric in the basis and its dual.** If $B$ is Seysen-reduced, so is its dual basis $D$, since $S(D) = S(B)$ and an update of one is an update of the other.
- **No order.** All pairs are treated alike, so the output is not sorted and the first vector need not be the shortest; there is no proved bound on $\|b_1\| / \lambda_1$.
- **Monotone.** $S$ decreases strictly at each update.
- **Deterministic.** The result depends on the order in which pairs are visited.

## Variants and improvements

- **Greedy pair choice.** Instead of a cyclic pass, choose at each step the pair $(i, j)$ with the largest decrease of $S$; this common variant costs $O(n^2)$ per step to find the pair, or less if the decreases are kept in a priority queue.
- **Floating point.** Practical versions keep $G$ and $H$ in floating point and recompute them when they drift.
- **Combined with LLL.** Running LLL first and Seysen after, or alternating them, gives bases good for both $\lambda_1$ and orthogonality.
- **Lattice-reduction-aided decoding.** In multiple-antenna communication, Seysen reduction of the channel matrix is used before linear and nearest plane detection, since both the channel basis and its dual enter the detection error.

## When to use it

Use it when the dual basis matters as much as the basis: for decoding with [Babai's methods](/babai-nearest-plane/) or for [closest vector](/closest-vector-problem/) heuristics, where both short vectors and short dual vectors help, and in moderate dimension. For a proved short first vector use [LLL](/lll-algorithm/) or BKZ instead.

## Pitfalls

- **Recomputing the inverse.** Inverting $G$ after each update costs $O(n^3)$; line L9 does it in $O(n)$.
- **Updating the wrong dual vector.** The update $b_j \leftarrow b_j + \lambda b_i$ changes $d_i$, not $d_j$; mixing them up breaks $\langle b_i, d_j \rangle = \delta_{ij}$ at once.
- **Ties.** With $\lambda^* = \pm 1/2$ the change is 0; accepting it can loop forever. The test must be strict.
- **Not a shortest vector.** A Seysen-reduced basis can have a first vector longer than $\lambda_1$ in dimension 3 and more; do not use it as an SVP solver.
- **Rational input.** The integrality argument for termination needs an integer basis; scale a rational basis first, which does not change the steps.

## Implementations

## History

Seysen (1993) introduced the measure $S$ and the algorithm in a paper on reducing a basis and its reciprocal basis together, and proved the existence of bases with small products $\|b_i\| \|d_i\|$. LaMacchia's 1991 thesis had already used Seysen's method for subset sum lattices, alongside LLL. Later work on lattice-reduction-aided detection in wireless communication made it popular again, as a reduction aimed at both the basis and its dual.

## References
