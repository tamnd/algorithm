---
tag: 6EK3RF
kind: definition
slug: lattice-basis
name: Lattice basis
aliases:
- generating set of a lattice
- basis of a lattice
- basis matrix
area: number-theory/lattice-reduction
level: intro
summary: Linearly independent vectors whose integer combinations give the whole lattice.
prereqs: [lattice, linear-independence, unimodular-matrix]
see_also: [lattice-determinant, gram-schmidt-orthogonalization, lattice-basis-reduction, hermite-normal-form, dual-lattice, successive-minima, lll-reduction, minkowski-reduced-basis]
sources:
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 1, Basics (bases, equivalent bases and unimodular matrices, the fundamental parallelepiped, and primitive vectors)
  - book: isbn:9783540617884
    title: J. W. S. Cassels, An Introduction to the Geometry of Numbers, Springer, Classics in Mathematics, 1997 reprint
    locator: Chapter I, Lattices (bases, sublattices and their index, and the extension of a primitive set to a basis)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 16, Lattices (bases, the basis matrix as rows, and the change of basis by unimodular matrices)
---

A basis of a [lattice](/lattice/) $L$ is a list of [linearly independent](/linear-independence/) vectors $b_1, \ldots, b_n$ such that the integer combinations of them are exactly the points of $L$. Every lattice has a basis, and every lattice of rank $n \ge 2$ has infinitely many: two bases of the same lattice differ by a [unimodular matrix](/unimodular-matrix/). Algorithms receive a lattice as a basis, and the quality of the basis decides how hard a problem on the lattice is to solve. [Lattice basis reduction](/lattice-basis-reduction/) is the task of turning a bad basis into a good one.

## Definition

**Notation used on the pages of this area.** The vectors $b_1, \ldots, b_n \in \mathbb{R}^m$ are the **rows** of the $n \times m$ matrix $B$, and $L(B) = \{x B : x \in \mathbb{Z}^n\} = \{\sum_i x_i b_i : x_i \in \mathbb{Z}\}$. The inner product is $\langle u, v \rangle$, and $\|v\| = \langle v, v \rangle^{1/2}$. The [Gram-Schmidt](/gram-schmidt-orthogonalization/) vectors are $b_1^*, \ldots, b_n^*$, with coefficients $\mu_{ij} = \langle b_i, b_j^* \rangle / \langle b_j^*, b_j^* \rangle$ for $j < i$. The first minimum is $\lambda_1(L)$, the length of a shortest nonzero vector of $L$, and $\det(L)$ is the [determinant](/lattice-determinant/). The parameter of the [LLL algorithm](/lll-algorithm/) is $\delta$, with $1/4 < \delta \le 1$.

**Basis.** Let $L \subseteq \mathbb{R}^m$ be a lattice. An ordered list $(b_1, \ldots, b_n)$ of vectors of $L$ is a **basis** of $L$ if

1. $b_1, \ldots, b_n$ are linearly independent over $\mathbb{R}$, and
2. $L(B) = L$: each $v \in L$ is $v = \sum_{i=1}^n x_i b_i$ with $x_1, \ldots, x_n \in \mathbb{Z}$.

The integers $x_i$ are then unique, by condition 1. They are the **coordinates** of $v$ in the basis. The number $n$ is the same for all bases, because it is the dimension of the real span of $L$. It is the **rank** of $L$, and $L$ is **full rank** when $n = m$. The order of the vectors matters for the Gram-Schmidt data and for every reduction notion, so a basis is a list, not a set.

**Change of basis.** Let $B$ be a basis of $L$, and let $C$ be an $n \times m$ matrix. Then $C$ is a basis of $L$ if and only if $C = U B$ for an integer matrix $U$ with $\det U = \pm 1$. The proof is on the [lattice](/lattice/) page: each basis is an integer combination of the other, so $C = U B$ and $B = V C$ with integer $U$ and $V$, independence gives $V U = I$, and $\det U \det V = 1$ for two integers forces $\det U = \pm 1$.

**Three tests for a basis.** Let $c_1, \ldots, c_n \in L$ be linearly independent, where $n$ is the rank of $L$, and let $B$ be a known basis. Then $C = U B$ for an integer matrix $U$ with $\det U \ne 0$, and the following are equivalent.

1. $C$ is a basis of $L$.
2. $\det U = \pm 1$, that is, $\det(C C^T) = \det(B B^T)$, because $\det(C C^T) = (\det U)^2 \det(B B^T)$.
3. The **fundamental parallelepiped** $\mathcal{P}(C) = \{\sum_i t_i c_i : 0 \le t_i < 1\}$ contains no point of $L$ other than $0$.

*Proof of 1 if and only if 3.* If $v \in L \cap \mathcal{P}(C)$ and $v \ne 0$, then some coordinate $t_i$ of $v$ in $C$ lies strictly between 0 and 1, so $v \notin L(C)$ and $C$ is not a basis. Conversely, if $C$ is not a basis, take $v \in L \setminus L(C)$. It lies in the span of $C$, because the span of $L$ has dimension $n$. Write $v = \sum_i t_i c_i$. The point $v - \sum_i \lfloor t_i \rfloor c_i$ is in $L$, in $\mathcal{P}(C)$, and not $0$, since $v \notin L(C)$. $\square$

The index of the sublattice is $[L : L(C)] = |\det U| = \det(L(C)) / \det(L)$. It counts the points of $L$ in $\mathcal{P}(C)$.

**Primitive vectors.** A vector $v \in L$ is **primitive** if $v \ne 0$ and $v / k \notin L$ for every integer $k \ge 2$. A vector of $L$ is the first vector of some basis if and only if it is primitive. More generally, independent vectors $c_1, \ldots, c_k \in L$ can be extended to a basis of $L$ if and only if $L \cap \operatorname{span}(c_1, \ldots, c_k) = L(c_1, \ldots, c_k)$; such a list is a **primitive set**. Cassels proves this in Chapter I.

## Examples and non-examples

**Examples.**

- $\mathbb{Z}^2$ has the standard basis $(1, 0), (0, 1)$. The rows $(2, 1), (1, 1)$ are also a basis, because the matrix $\begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$ is integer with determinant 1. The bases of $\mathbb{Z}^n$ are the rows of the matrices of $\mathrm{GL}_n(\mathbb{Z})$.
- The vector $(3, 5)$ is primitive in $\mathbb{Z}^2$, since $\gcd(3, 5) = 1$, and $(3, 5), (1, 2)$ is a basis, since $3 \cdot 2 - 5 \cdot 1 = 1$. In $\mathbb{Z}^n$ a vector is primitive exactly when the gcd of its entries is 1.
- The lattice with basis $(2, 0), (1, 2)$ also has the basis $(1, 2), (3, 2)$. The change of basis is $U = \begin{pmatrix} 0 & 1 \\ 1 & 1 \end{pmatrix}$, with $\det U = -1$.
- A lattice that is not full rank: $A_2 = \{x \in \mathbb{Z}^3 : x_1 + x_2 + x_3 = 0\}$ has the basis $(1, -1, 0), (0, 1, -1)$, with Gram matrix $\begin{pmatrix} 2 & -1 \\ -1 & 2 \end{pmatrix}$ of determinant 3, so $\det(A_2) = \sqrt 3$. The rows $(1, 0, -1), (0, 1, -1)$ are another basis, with $U = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$.
- Rank 1: the lattice $\{k b : k \in \mathbb{Z}\}$ with $b \ne 0$ has exactly two bases, $(b)$ and $(-b)$.

**Non-examples.**

- The rows $(2, 0), (0, 1)$ are independent vectors of $\mathbb{Z}^2$ but not a basis of it. The parallelepiped $\mathcal{P}$ is $[0, 2) \times [0, 1)$, and it contains the point $(1, 0)$ of $\mathbb{Z}^2$. They generate a sublattice of index $|\det| = 2$.
- The list $(2), (3)$ generates $\mathbb{Z}$, but it is not a basis, because the two vectors are dependent. A generating set with more than $n$ vectors is never a basis. A basis can be computed from it, for example with the [Hermite normal form](/hermite-normal-form/) of the integer matrix.
- The list $(1, 1), (1, -1)$ has the right number of independent vectors of $\mathbb{Z}^2$, but $\det = -2$. It generates the checkerboard lattice $\{x \in \mathbb{Z}^2 : x_1 + x_2 \text{ even}\}$, not $\mathbb{Z}^2$.
- **Short independent vectors need not form a basis.** Let $L = \mathbb{Z}^5 \cup (\mathbb{Z}^5 + h)$ with $h = (\tfrac12, \ldots, \tfrac12)$. Its vectors of length 1 are only $\pm e_1, \ldots, \pm e_5$, because a vector of the coset $\mathbb{Z}^5 + h$ has length at least $\sqrt 5 / 2 > 1$. So $e_1, \ldots, e_5$ are 5 independent vectors that reach all the [successive minima](/successive-minima/) $\lambda_1 = \cdots = \lambda_5 = 1$, but they generate only $\mathbb{Z}^5$, of index 2 in $L$. No basis of $L$ has all its vectors of length 1. This is why the [Minkowski-reduced basis](/minkowski-reduced-basis/) is defined by a greedy rule and not by the minima.

## Related definitions

- **[Unimodular matrix](/unimodular-matrix/).** An integer square matrix with determinant $\pm 1$; the changes of basis of a lattice.
- **[Lattice determinant](/lattice-determinant/).** $\det(L) = \det(B B^T)^{1/2} = \prod_i \|b_i^*\|$; it is the same for all bases.
- **[Gram-Schmidt orthogonalization](/gram-schmidt-orthogonalization/).** The vectors $b_i^*$ and the numbers $\mu_{ij}$ of a basis. They depend on the order of the basis.
- **Gram matrix.** $G = B B^T$, with $G_{ij} = \langle b_i, b_j \rangle$. It determines the lattice up to an isometry, and the change of basis acts as $G \mapsto U G U^T$.
- **[Hermite normal form](/hermite-normal-form/).** The unique triangular basis of an integer lattice; two integer bases generate the same lattice exactly when their Hermite normal forms are equal.
- **[Dual lattice](/dual-lattice/).** The dual basis $D = (B B^T)^{-1} B$ satisfies $\langle b_i, d_j \rangle = 1$ for $i = j$ and $0$ otherwise, and it is a basis of the dual lattice.
- **Reduced bases.** Bases with short, nearly orthogonal vectors: [LLL-reduced](/lll-reduction/), [HKZ-reduced](/hkz-reduction/), [Minkowski-reduced](/minkowski-reduced-basis/) and [Seysen-reduced](/seysen-reduction/) bases. Finding one is [lattice basis reduction](/lattice-basis-reduction/).

## References
