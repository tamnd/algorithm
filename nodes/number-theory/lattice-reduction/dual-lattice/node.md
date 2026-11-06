---
tag: ZHAF5B
kind: definition
slug: dual-lattice
name: Dual lattice
aliases:
- lattice dual
- reciprocal lattice
- polar lattice
area: number-theory/lattice-reduction
level: advanced
summary: Lattice of vectors having integer inner product with every lattice vector.
prereqs: [lattice, lattice-basis, lattice-determinant]
see_also: [gram-schmidt-orthogonalization, covering-radius, successive-minima, gap-svp, babai-rounding, bkz-algorithm, learning-with-errors, short-integer-solution]
sources:
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 1, Basics (the dual lattice and the dual basis)
  - book: isbn:9780387985855
    title: J. H. Conway and N. J. A. Sloane, Sphere Packings, Lattices and Groups, third edition, Springer, 1999
    locator: Chapter 4, Certain important lattices and their properties (the lattices A_n, D_n and E_8 and their duals)
  - paper: "W. Banaszczyk, New bounds in some transference theorems in the geometry of numbers, Mathematische Annalen 296 (1993)"
    locator: pages 625 to 635 (the bounds lambda_1(L) lambda_n(L dual) at most n and mu(L) lambda_1(L dual) at most n/2)
---

The dual of a [lattice](/lattice/) $L$ is the set $L^\times$ of vectors in the span of $L$ whose inner product with every vector of $L$ is an integer. It is again a lattice, of the same rank, with determinant $1/\det(L)$, and its dual is $L$ again. Short dual vectors cut $L$ into widely spaced parallel hyperplanes, which is why the dual appears in transference theorems, in the hardness and cryptography of lattice problems, and in reduction algorithms that work on both sides.

## Definition

Notation is that of the other pages in this area: $b_1, \ldots, b_n \in \mathbb{R}^m$ are linearly independent **rows** of the $n \times m$ matrix $B$, and $L = L(B) = \{x B : x \in \mathbb{Z}^n\}$.

**Definition.** The **dual lattice** of $L$ is

$$L^\times = \{ y \in \operatorname{span}(L) : \langle y, v \rangle \in \mathbb{Z} \text{ for every } v \in L \}.$$

It is enough to test the basis vectors: $y \in \operatorname{span}(L)$ is in $L^\times$ if and only if $\langle y, b_i \rangle \in \mathbb{Z}$ for $i = 1, \ldots, n$. Other books write $L^*$ or $\hat L$; this site writes $L^\times$ so that $b_i^*$ can keep its Gram-Schmidt meaning.

**The dual basis.** Let

$$D = (B B^T)^{-1} B,$$

an $n \times m$ matrix with rows $d_1, \ldots, d_n$. Then $L^\times = L(D)$, and $D$ is characterized by the two conditions

$$\operatorname{span}(D) = \operatorname{span}(B) \qquad \text{and} \qquad D B^T = I_n, \text{ that is } \langle d_i, b_j \rangle = [i = j].$$

For a full-rank lattice ($n = m$) this is $D = B^{-T}$. *Proof that $L(D) = L^\times$.* The rows of $D$ are combinations of the rows of $B$, so they lie in the span, and $D B^T = (B B^T)^{-1} B B^T = I$, so each $d_i$ has integer products with the basis; hence $L(D) \subseteq L^\times$. Conversely, write $y \in L^\times$ as $y = c D$ for a real vector $c$ (possible because $D$ spans the same space). Then $\langle y, b_j \rangle = c_j$, which is an integer, so $y \in L(D)$. $\square$

**Basic facts.** Each one follows from $D = (B B^T)^{-1} B$.

1. **Determinant.** $D D^T = (B B^T)^{-1}$, so $\det(L^\times) = 1/\det(L)$.
2. **Involution.** $(L^\times)^\times = L$, because $(D D^T)^{-1} D = B$.
3. **Change of basis.** If $B' = U B$ with $U$ [unimodular](/unimodular-matrix/), the dual basis of $B'$ is $U^{-T} D$. So the dual depends only on the lattice, and duality reverses inclusions: $L_1 \subseteq L_2$ implies $L_2^\times \subseteq L_1^\times$.
4. **Scaling.** $(c L)^\times = c^{-1} L^\times$ for $c > 0$.
5. **Gram-Schmidt in reverse order.** Orthogonalize the dual basis in the reverse order $d_n, d_{n-1}, \ldots, d_1$. The Gram-Schmidt vector attached to $d_i$ is $b_i^* / \|b_i^*\|^2$. So the reversed dual basis has Gram-Schmidt lengths $1/\|b_n^*\|, \ldots, 1/\|b_1^*\|$, and a basis whose lengths $\|b_i^*\|$ decrease slowly has a dual whose lengths also decrease slowly. *Proof.* Put $e_i = b_i^*/\|b_i^*\|^2$. The span of $d_{i+1}, \ldots, d_n$ is the set of $y \in \operatorname{span}(L)$ orthogonal to $b_1, \ldots, b_i$, which is $\operatorname{span}(b_{i+1}^*, \ldots, b_n^*)$; so $e_i$ is orthogonal to it. For $j \le i$, $\langle e_i, b_j \rangle = [i = j]$, since $b_i^*$ is orthogonal to $b_j$ for $j < i$ and $\langle b_i^*, b_i \rangle = \|b_i^*\|^2$. So $d_i - e_i$ is orthogonal to $b_1, \ldots, b_i$ and lies in $\operatorname{span}(d_{i+1}, \ldots, d_n)$. These two facts say that $e_i$ is the Gram-Schmidt vector of $d_i$ in the order $d_n, \ldots, d_1$. $\square$
6. **Hyperplanes.** For a nonzero $y \in L^\times$, the lattice $L$ lies on the parallel hyperplanes $H_k = \{x : \langle x, y \rangle = k\}$, $k \in \mathbb{Z}$, which are $1/\|y\|$ apart. If $y$ is primitive (not a proper multiple of another dual vector), every hyperplane $H_k$ contains lattice points.

**Transference.** The minima of $L$ and $L^\times$ are linked. With $\lambda_i$ the [successive minima](/successive-minima/) and $\mu$ the [covering radius](/covering-radius/):

- $1 \le \lambda_1(L) \, \lambda_n(L^\times) \le n$ (the upper bound is Banaszczyk's);
- $\lambda_1(L) \, \lambda_1(L^\times) \le \gamma_n \le n$, with $\gamma_n$ the [Hermite constant](/hermite-constant/), because $\det(L) \det(L^\times) = 1$;
- $\tfrac12 \le \mu(L) \, \lambda_1(L^\times) \le \tfrac n2$ (the upper bound is again Banaszczyk's).

The lower bound in the first line: take $v \in L$ with $\|v\| = \lambda_1(L)$ and $n$ independent dual vectors $y_1, \ldots, y_n$ of length at most $\lambda_n(L^\times)$. Some $y_j$ is not orthogonal to $v$, so $\langle v, y_j \rangle$ is a nonzero integer and $1 \le \|v\| \|y_j\|$. The lower bound in the third line follows from fact 6: a point halfway between two consecutive hyperplanes is at distance at least $1 / (2 \|y\|)$ from $L$.

## Examples and non-examples

**Examples.**

- $(\mathbb{Z}^m)^\times = \mathbb{Z}^m$. A lattice equal to its dual is **self-dual** (unimodular and integral); other examples are $E_8$ and the Leech lattice.
- **A worked dual basis.** For $b_1 = (2, 0)$, $b_2 = (1, 2)$, with $\det(L) = 4$, the dual basis is $d_1 = (\tfrac12, -\tfrac14)$, $d_2 = (0, \tfrac12)$. Check: $\langle d_1, b_1 \rangle = 1$, $\langle d_1, b_2 \rangle = \tfrac12 - \tfrac12 = 0$, $\langle d_2, b_1 \rangle = 0$, $\langle d_2, b_2 \rangle = 1$. The determinant is $\tfrac12 \cdot \tfrac12 = \tfrac14$, and $\lambda_1(L^\times) = \tfrac12$, reached by $d_2$. Since $L$ is integral, $L \subseteq L^\times$, with index $\det(L)^2 = 16$.
- **The hexagonal lattice.** For $A_2$ with rows $(1, 0)$ and $(\tfrac12, \tfrac{\sqrt3}{2})$, the dual basis is $(1, -\tfrac{1}{\sqrt 3})$, $(0, \tfrac{2}{\sqrt 3})$. Both have squared length $\tfrac43$ and they meet at 120 degrees, so $A_2^\times$ is again hexagonal, scaled by $2/\sqrt3$ and rotated by 30 degrees.
- **The checkerboard lattice.** $D_3$ has basis $(1, -1, 0), (0, 1, -1), (1, 1, 0)$ and determinant 2. Its dual is $D_3^\times = \mathbb{Z}^3 \cup (\mathbb{Z}^3 + (\tfrac12, \tfrac12, \tfrac12))$, the body-centred cubic lattice, with determinant $\tfrac12$ and $\lambda_1^2 = \tfrac34$, reached by $(\tfrac12, \tfrac12, \tfrac12)$. So the face-centred and body-centred cubic lattices are dual to each other.
- **q-ary lattices.** For $A \in \mathbb{Z}_q^{k \times m}$, the lattices $\Lambda_q^\perp(A) = \{x \in \mathbb{Z}^m : A x \equiv 0 \pmod q\}$ and $\Lambda_q(A) = \{A^T s + q z : s \in \mathbb{Z}^k, z \in \mathbb{Z}^m\}$ are dual up to scaling: $\Lambda_q^\perp(A)^\times = \tfrac1q \Lambda_q(A)$. The [SIS](/short-integer-solution/) problem lives on the first, and [LWE](/learning-with-errors/) decoding on the second.
- **Rank 1.** For $L = \mathbb{Z} (1, 1, 1)$, the dual is $\mathbb{Z} (\tfrac13, \tfrac13, \tfrac13)$, of length $1/\sqrt3 = 1/\det(L)$.

**Non-examples.**

- **Dropping the span condition.** For the rank-1 lattice $\mathbb{Z} (1, 1, 1)$, the set $\{y \in \mathbb{R}^3 : \langle y, (1,1,1) \rangle \in \mathbb{Z}\}$ contains the whole plane $y_1 + y_2 + y_3 = 0$, so it is not discrete and not a lattice. The definition must restrict to $\operatorname{span}(L)$.
- **The transpose.** The rows of $B^T$ are not a dual basis in general. For $b_1 = (2, 0)$, $b_2 = (1, 2)$ the rows of $B^T$ are $(2, 1)$ and $(0, 2)$, and $\langle (2, 1), (2, 0) \rangle = 4$, not $1$ or $0$. The correct formula is $D = B^{-T}$ in the full-rank case.
- **Dual of a non-lattice.** For the dense group $\mathbb{Z} + \sqrt 2 \mathbb{Z} \subset \mathbb{R}$, the only real $y$ with $y \in \mathbb{Z}$ and $\sqrt 2 y \in \mathbb{Z}$ is $0$; the dual of a non-discrete group is not a lattice of the same rank.
- **The polar body.** The polar of a convex body, $\{y : \langle x, y \rangle \le 1 \ \forall x\}$, is a convex body, not a lattice. The two notions share a name in some books.

## Related definitions

- **[Lattice basis](/lattice-basis/) and [determinant](/lattice-determinant/).** $D$ is the dual basis of $B$, and $\det(L^\times) = 1/\det(L)$.
- **Integral lattice.** $L$ is integral if $\langle u, v \rangle \in \mathbb{Z}$ for all $u, v \in L$, which is the same as $L \subseteq L^\times$. Then $L^\times / L$ is a finite group of order $\det(L)^2$, the discriminant group.
- **[Covering radius](/covering-radius/) and [successive minima](/successive-minima/).** Linked to the dual by the transference bounds above.
- **[Gram-Schmidt orthogonalization](/gram-schmidt-orthogonalization/).** Fact 5 relates the Gram-Schmidt data of $B$ and of the reversed dual basis. **Dual reduction** reduces $D$ in reverse order to reduce $B$; dual [BKZ](/bkz-algorithm/) and Seysen's algorithm use this.
- **[Babai rounding](/babai-rounding/).** The coordinates of a target $t$ in the basis are $\langle t, d_i \rangle$, and the error of rounding them is governed by the lengths $\|d_i\|$.
- **[GapSVP](/gap-svp/).** Short dual vectors certify that $L$ has no short vectors only up to a factor; Aharonov and Regev used the dual to put GapSVP with factor $\sqrt n$ in NP $\cap$ coNP.
- **Enumeration bounds.** The coefficient $x_i$ of a lattice vector $v = x B$ is $\langle v, d_i \rangle$, so $\|v\| \le R$ implies $|x_i| \le R \|d_i\|$. This gives the coefficient box used by brute-force checks.

## References
