---
tag: 50G04W
kind: concept
slug: lattice-determinant
name: Lattice determinant
aliases:
- covolume
- volume of fundamental domain
- lattice volume
area: number-theory/lattice-reduction
level: intro
summary: Absolute determinant of a basis matrix, the volume of a fundamental domain.
prereqs: [lattice, lattice-basis, determinant]
see_also: [gram-schmidt-orthogonalization, minkowski-theorem, hermite-constant, gaussian-heuristic, dual-lattice, hadamard-bound, lll-algorithm, root-hermite-factor]
sources:
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 1, Basics (the determinant as the volume of the fundamental parallelepiped, its invariance under change of basis, and its value through Gram-Schmidt)
  - book: isbn:9783540617884
    title: J. W. S. Cassels, An Introduction to the Geometry of Numbers, Springer, Classics in Mathematics, 1997 reprint
    locator: Chapter I, Lattices (the determinant, sublattices and the index), and Chapter III, Theorems of Blichfeldt and Minkowski
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 16, Lattices (the determinant, the Hadamard inequality and the q-ary lattices)
---

The determinant of a [lattice](/lattice/) $L$ with [basis](/lattice-basis/) rows $b_1, \ldots, b_n$ is $\det(L) = \det(B B^T)^{1/2}$, the $n$-dimensional volume of the parallelepiped that the basis spans. It does not depend on the basis, so it is a number attached to the lattice itself: the volume of space that each lattice point owns. It equals the product $\prod_i \|b_i^*\|$ of the [Gram-Schmidt](/gram-schmidt-orthogonalization/) lengths, which makes it the yardstick of basis reduction: a short first vector means a short vector compared with $\det(L)^{1/n}$.

## In plain words

Lay tiles in a pattern so that every tile has one corner on a grid point and the tiles cover the floor with no gaps and no overlaps. The area of one tile is the same for every way of choosing the tiles from the grid, even for long thin tiles. That area is the determinant of the grid.

So the determinant tells how crowded the grid is. A small value means many points in a given region; a large value means few. Since the area is fixed, a basis with long arrows must have arrows that lean on each other, and a basis with arrows at right angles to each other has the shortest arrows that the area allows. Lattice reduction tries to get close to that ideal, and its results are measured against the determinant.

## The idea

**Definition.** Let $B$ be an $n \times m$ basis matrix with rows $b_1, \ldots, b_n$, and let $G = B B^T$ be its Gram matrix, $G_{ij} = \langle b_i, b_j \rangle$. Then

$$\det(L(B)) = \sqrt{\det G}.$$

For a full-rank lattice ($n = m$), $\det G = (\det B)^2$, so $\det(L) = |\det B|$.

**It does not depend on the basis.** Another basis is $C = U B$ with $U$ integer and $\det U = \pm 1$. Then $\det(C C^T) = \det(U G U^T) = (\det U)^2 \det G = \det G$.

**The product of the Gram-Schmidt lengths.** Write $b_i = b_i^* + \sum_{j < i} \mu_{ij} b_j^*$. In matrix form $B = M B^*$, where $M$ is lower triangular with ones on the diagonal and $\mu_{ij}$ below it, and $B^*$ has the rows $b_i^*$. The rows $b_i^*$ are orthogonal, so $B^* (B^*)^T = \operatorname{diag}(\|b_1^*\|^2, \ldots, \|b_n^*\|^2)$, and

$$\det G = \det M \cdot \det\big(B^* (B^*)^T\big) \cdot \det M^T = \prod_{i=1}^n \|b_i^*\|^2, \qquad \det(L) = \prod_{i=1}^n \|b_i^*\|.$$

**The volume.** The fundamental parallelepiped $\mathcal{P}(B) = \{\sum_i t_i b_i : 0 \le t_i < 1\}$ has volume base times height, step by step: the height of $b_i$ over the span of $b_1, \ldots, b_{i-1}$ is $\|b_i^*\|$. So $\det(L)$ is the volume of $\mathcal{P}(B)$ inside the span of $L$. The translates $v + \mathcal{P}(B)$, $v \in L$, cover the span with no overlap, so $\mathcal{P}(B)$ is a **fundamental domain**. Every measurable fundamental domain has the same volume; this is the name **covolume**.

**Counting points.** Because the translates of $\mathcal{P}(B)$ tile the span, the number of lattice points in a large ball of radius $r$ is close to the volume of the ball divided by $\det(L)$: the ratio tends to 1 as $r \to \infty$. The [Gaussian heuristic](/gaussian-heuristic/) applies this estimate to balls of moderate size.

**Bounds that involve it.**

- *Hadamard's inequality.* $\|b_i^*\| \le \|b_i\|$, so $\det(L) \le \prod_i \|b_i\|$, with equality exactly for an orthogonal basis; see the [Hadamard bound](/hadamard-bound/). The ratio $\prod_i \|b_i\| / \det(L) \ge 1$ is the **orthogonality defect** of the basis.
- *Minkowski's bound.* $\lambda_1(L) \le \sqrt{n}\, \det(L)^{1/n}$, by [Minkowski's first theorem](/minkowski-theorem/). The best constant is the [Hermite constant](/hermite-constant/): $\lambda_1(L)^2 \le \gamma_n \det(L)^{2/n}$.
- *A lower bound by Gram-Schmidt.* $\lambda_1(L) \ge \min_i \|b_i^*\|$, which with the product formula shows that some $\|b_i^*\| \le \det(L)^{1/n}$.

**Sublattices and the dual.** If $L' \subseteq L$ has the same rank, then $\det(L') = [L : L'] \det(L)$, where the index $[L : L']$ is $|\det U|$ for the integer matrix $U$ with $B' = U B$. For an integer lattice of full rank in $\mathbb{Z}^n$, $\det(L) = [\mathbb{Z}^n : L]$ is a positive integer. The [dual lattice](/dual-lattice/) has the basis $D = G^{-1} B$, whose Gram matrix is $D D^T = G^{-1}$, so $\det(L^\times) = 1/\det(L)$.

**Computing it.** For an integer or rational basis, $\det G$ is an exact rational number. Computing $G$ takes $O(n^2 m)$ arithmetic operations, and [fraction-free Gaussian elimination](/determinant-computation/) then takes $O(n^3)$ operations on integers whose size stays polynomial in the input size. The square root is usually not taken: algorithms compare $\det G$, or the integers $d_i = \prod_{j \le i} \|b_j^*\|^2$ that the [LLL algorithm](/lll-algorithm/) uses, which are integers for an integer basis.

## Examples

- **$\mathbb{Z}^n$.** The standard basis is orthogonal with unit vectors, so $\det(\mathbb{Z}^n) = 1$.
- **A lattice of rank 2.** For the rows $(2, 0)$ and $(1, 2)$, $\det B = 4$. The Gram-Schmidt vectors are $b_1^* = (2, 0)$ and $b_2^* = (0, 2)$, with $\mu_{21} = 1/2$, and $2 \cdot 2 = 4$. The disc of radius 50 around the origin contains 1951 points of this lattice, against the estimate $\pi \cdot 50^2 / 4 \approx 1963.5$.
- **The same lattice, a bad basis.** The rows $(4, 4)$ and $(9, 10)$ generate the same lattice, and $|4 \cdot 10 - 4 \cdot 9| = 4$. But $\|b_1\| \|b_2\| = \sqrt{32 \cdot 181} \approx 76.1$, so the orthogonality defect is about $76.1 / 4 \approx 19.0$, against $2 \sqrt 5 / 4 \approx 1.12$ for the basis $(2, 0), (1, 2)$.
- **A lattice that is not full rank.** $A_2 = \{x \in \mathbb{Z}^3 : x_1 + x_2 + x_3 = 0\}$ has the basis $(1, -1, 0), (0, 1, -1)$ and $\det G = 2 \cdot 2 - 1 = 3$, so $\det(A_2) = \sqrt 3$. Here $B$ is not square, and $\det B$ does not exist; only the Gram form applies.
- **A sublattice.** The checkerboard lattice $D_3 = \{x \in \mathbb{Z}^3 : x_1 + x_2 + x_3 \text{ even}\}$ has the basis $(1, -1, 0), (0, 1, -1), (1, 1, 0)$ and $\det G = 4$, so $\det(D_3) = 2 = [\mathbb{Z}^3 : D_3]$.
- **A q-ary lattice.** $\Lambda = \{x \in \mathbb{Z}^3 : x_1 + 2 x_2 + 3 x_3 \equiv 0 \pmod 5\}$ has the triangular basis $(5, 0, 0), (-2, 1, 0), (-3, 0, 1)$, so $\det(\Lambda) = 5$. The count agrees: 25 of the 125 points of $\{0, \ldots, 4\}^3$ lie in $\Lambda$, so the index is $125 / 25 = 5$. For a prime $q$ and an integer $k \times m$ matrix $A$ of rank $k$ modulo $q$, the lattice $\{x : A x \equiv 0 \pmod q\}$ has determinant $q^k$, because $\mathbb{Z}^m / \Lambda$ is in bijection with the image of $x \mapsto A x \bmod q$, which has $q^k$ elements.

## Where it is used

- **Measuring reduction.** The [LLL algorithm](/lll-algorithm/) guarantees $\|b_1\| \le (4/3 + \varepsilon)^{(n-1)/4} \det(L)^{1/n}$, and the [root Hermite factor](/root-hermite-factor/) $(\|b_1\| / \det(L)^{1/n})^{1/n}$ compares reduction algorithms in practice.
- **The LLL potential.** The proof that LLL stops uses the product $\prod_i d_i$ of the determinants of the leading sublattices, which drops by a factor $\delta$ at each swap.
- **Existence of short vectors.** [Minkowski's first theorem](/minkowski-theorem/) and the [Hermite constant](/hermite-constant/) bound $\lambda_1$ by $\det(L)^{1/n}$; [Minkowski's second theorem](/minkowski-second-theorem/) bounds the product of all [successive minima](/successive-minima/) by $\det(L)$.
- **Predicting the shortest vector.** The [Gaussian heuristic](/gaussian-heuristic/) predicts $\lambda_1 \approx \sqrt{n / (2 \pi e)}\, \det(L)^{1/n}$ for a random lattice of large rank, which sets the radius of [enumeration](/lattice-enumeration/) and the targets of [sieving](/lattice-sieving/).
- **Cryptography.** The parameters of [learning with errors](/learning-with-errors/) and [short integer solution](/short-integer-solution/) schemes are chosen so that the secret is short compared with $\det(L)^{1/n}$ for the attack lattice.

## References
