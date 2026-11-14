---
tag: T3G9B4
kind: definition
slug: cayley-menger-determinant
name: Cayley-Menger determinant
aliases:
- Cayley-Menger matrix
area: cad/geometric-constraint-solving
level: core
summary: A bordered determinant of squared distances. It gives the squared volume of a simplex and tests whether given distances can be realized in d dimensions.
prereqs: [determinant]
see_also: [distance-geometry-problem, multidimensional-scaling, rigidity-matrix, bar-and-joint-framework, circle-circle-intersection, constructive-constraint-solving, root-identification-problem, semidefinite-programming]
sources:
  - paper: "Arthur Cayley, On a theorem in the geometry of position, Cambridge Mathematical Journal 2, 267 to 271, 1841"
    locator: the determinant relation between the ten distances of five points in space and the six of four points in a plane
  - paper: doi:10.1007/BF01448840
    title: Karl Menger, Untersuchungen über allgemeine Metrik, Mathematische Annalen 100, 75 to 163, 1928
    locator: the bordered determinant of squared distances and the characterization of subsets of Euclidean space by distances alone
  - paper: doi:10.2307/1968654
    title: I. J. Schoenberg, Remarks to Maurice Fréchet's article "Sur la définition axiomatique d'une classe d'espaces distanciés vectoriellement applicable sur l'espace de Hilbert", Annals of Mathematics 36(3), 724 to 732, 1935
    locator: a symmetric matrix with zero diagonal is a matrix of squared Euclidean distances if and only if the derived Gram matrix is positive semidefinite
  - book: "Leonard M. Blumenthal, Theory and Applications of Distance Geometry, Oxford, Clarendon Press, 1953"
    locator: the chapters on Cayley-Menger determinants and on the embedding of semimetric spaces in Euclidean space
  - paper: doi:10.1137/120875909
    title: Leo Liberti, Carlile Lavor, Nelson Maculan and Antonio Mucherino, Euclidean distance geometry and applications, SIAM Review 56(1), 3 to 69, 2014
    locator: the sections on Cayley-Menger determinants, Gram matrices and realizability
---

The Cayley-Menger determinant turns a table of squared distances into a volume. For $k + 1$ points it is a single determinant of size $k + 2$, built only from the squared distances between the points, and it equals the squared $k$-dimensional volume of their simplex times a fixed constant. So it needs no coordinates. Its sign tells whether the distances can come from real points, and its vanishing tells whether the points fit in fewer dimensions. In geometric constraint solving it is the standard way to write a distance constraint system without coordinates.

## Definition

Let $p_0, p_1, \ldots, p_k$ be points in $\mathbb{R}^d$ and put $D_{ij} = \lVert p_i - p_j \rVert^2$. The *Cayley-Menger matrix* is the symmetric $(k + 2) \times (k + 2)$ matrix
$$ M = \begin{pmatrix} 0 & 1 & 1 & \cdots & 1 \\ 1 & 0 & D_{01} & \cdots & D_{0k} \\ 1 & D_{10} & 0 & \cdots & D_{1k} \\ \vdots & \vdots & \vdots & \ddots & \vdots \\ 1 & D_{k0} & D_{k1} & \cdots & 0 \end{pmatrix}, $$
the matrix $D$ of squared distances with a border of ones and a zero in the corner. Its [determinant](/determinant/) is the *Cayley-Menger determinant*, written $\mathrm{CM}(p_0, \ldots, p_k)$. The same formula applies to any symmetric table $D$ with zero diagonal, whether or not it comes from points. Then $\mathrm{CM}(D)$ is a polynomial of degree $k + 1$ in the entries of $D$.

Let $V_k$ be the $k$-dimensional volume of the simplex with vertices $p_0, \ldots, p_k$: the length of a segment for $k = 1$, the area of a triangle for $k = 2$, the volume of a tetrahedron for $k = 3$.

**Theorem.** For all points $p_0, \ldots, p_k$,
$$ \mathrm{CM}(p_0, \ldots, p_k) = (-1)^{k + 1} \, 2^k \, (k!)^2 \, V_k^2 . $$

For $k = 1, 2, 3$ this reads $\mathrm{CM} = 2 L^2$ for a segment of length $L$, $\mathrm{CM} = -16 A^2$ for a triangle of area $A$, and $\mathrm{CM} = 288 V^2$ for a tetrahedron of volume $V$.

**Proof for the triangle.** Write $a = D_{12}$, $b = D_{02}$ and $c = D_{01}$ for the squared side lengths. Expansion of the $4 \times 4$ determinant gives
$$ \mathrm{CM}(p_0, p_1, p_2) = \det \begin{pmatrix} 0 & 1 & 1 & 1 \\ 1 & 0 & c & b \\ 1 & c & 0 & a \\ 1 & b & a & 0 \end{pmatrix} = a^2 + b^2 + c^2 - 2ab - 2bc - 2ca . $$
Now put $u = p_1 - p_0$ and $v = p_2 - p_0$. The parallelogram on $u$ and $v$ has area $2A$, so $4A^2 = \lVert u \rVert^2 \lVert v \rVert^2 - (u \cdot v)^2$. From $\lVert u - v \rVert^2 = \lVert u \rVert^2 + \lVert v \rVert^2 - 2 u \cdot v$ we get $u \cdot v = (b + c - a)/2$, with $\lVert u \rVert^2 = c$ and $\lVert v \rVert^2 = b$. So
$$ 16 A^2 = 4bc - (b + c - a)^2 = 2ab + 2bc + 2ca - a^2 - b^2 - c^2 = -\mathrm{CM}(p_0, p_1, p_2) . $$
This is Heron's formula written in squared lengths. $\square$

**Proof in general.** The same idea works for every $k$, through the Gram matrix. Put $u_i = p_i - p_0$ for $i = 1, \ldots, k$ and let $G$ be the $k \times k$ Gram matrix $G_{ij} = u_i \cdot u_j$. As above, $G_{ij} = (D_{0i} + D_{0j} - D_{ij})/2$.

*Step 1: $\mathrm{CM} = (-1)^{k + 1} 2^k \det G$.* Index the rows and columns of the Cayley-Menger matrix by $\ast, 0, 1, \ldots, k$, where $\ast$ is the border. For each $i \ge 1$ subtract row $0$ from row $i$, and then for each $j \ge 1$ subtract column $0$ from column $j$. These operations do not change the determinant. In the border row, the entries in columns $j \ge 1$ become $1 - 1 = 0$, and in the border column the entries in rows $i \ge 1$ become $0$ too. Row $0$ keeps the entries $1$, $0$ and $D_{0j}$. For $i, j \ge 1$ the entry becomes $D_{ij} - D_{0j} - D_{i0} + D_{00} = -2 G_{ij}$. In block form, with $\delta = (D_{01}, \ldots, D_{0k})$,
$$ \det \begin{pmatrix} 0 & 1 & 0 \\ 1 & 0 & \delta^T \\ 0 & \delta & -2G \end{pmatrix} . $$
The border row has its only nonzero entry, a 1, in column $0$, at position $(1, 2)$, so the expansion along it gives the factor $-1$ times the minor without row $\ast$ and column $0$. That minor is block triangular, $\begin{pmatrix} 1 & \delta^T \\ 0 & -2G \end{pmatrix}$, with determinant $\det(-2G) = (-2)^k \det G$. So $\mathrm{CM} = -(-2)^k \det G = (-1)^{k + 1} 2^k \det G$.

*Step 2: $\det G = (k!)^2 V_k^2$.* Choose an orthonormal basis of a $k$-dimensional subspace that contains $u_1, \ldots, u_k$, and let $U$ be the $k \times k$ matrix of the coordinates of the $u_i$ in it. Then $G = U^T U$ and $\det G = (\det U)^2$. The volume of the parallelepiped on $u_1, \ldots, u_k$ is $\lvert \det U \rvert$, and the simplex is $1/k!$ of it, so $\lvert \det U \rvert = k! \, V_k$. $\square$

**Realizability.** A symmetric table $D$ with zero diagonal on $n + 1$ points is *realizable in $\mathbb{R}^d$* if there are points $p_0, \ldots, p_n$ in $\mathbb{R}^d$ with $\lVert p_i - p_j \rVert^2 = D_{ij}$ for all $i, j$. For a set $S \subseteq \{1, \ldots, n\}$ write $\mathrm{CM}_S$ for the Cayley-Menger determinant of $D$ restricted to $\{0\} \cup S$.

**Theorem (Schoenberg 1935, in Cayley-Menger form).** $D$ is realizable in some Euclidean space if and only if $(-1)^{\lvert S \rvert + 1} \mathrm{CM}_S \ge 0$ for every nonempty $S$. It is realizable in $\mathbb{R}^d$ if and only if, in addition, $\mathrm{CM}_S = 0$ for every $S$ with $\lvert S \rvert = d + 1$.

*Proof.* Define $G$ from $D$ by $G_{ij} = (D_{0i} + D_{0j} - D_{ij})/2$ for $i, j = 1, \ldots, n$. Step 1 above used only the entries of $D$, so it gives $(-1)^{\lvert S \rvert + 1} \mathrm{CM}_S = 2^{\lvert S \rvert} \det G_S$ for the principal submatrix $G_S$. A symmetric matrix is positive semidefinite exactly when all of its principal minors are nonnegative, so the sign condition says that $G$ is positive semidefinite. If $D$ comes from points, then $G$ is the Gram matrix of the vectors $p_i - p_0$, which is positive semidefinite of rank at most $d$. Conversely, if $G$ is positive semidefinite of rank $r$, write $G = U^T U$ with $U$ of size $r \times n$, from an eigenvalue decomposition. Put $p_0 = 0$ and let $p_i$ be column $i$ of $U$. Then $p_i \cdot p_j = G_{ij}$, so $\lVert p_i - p_j \rVert^2 = G_{ii} + G_{jj} - 2 G_{ij} = D_{ij}$ and $\lVert p_i \rVert^2 = G_{ii} = D_{0i}$. These points lie in $\mathbb{R}^r$. Finally, a positive semidefinite matrix has rank at most $d$ exactly when all of its principal minors of order $d + 1$ vanish, which is the condition $\mathrm{CM}_S = 0$ for $\lvert S \rvert = d + 1$. $\square$

The proof is also the algorithm used in practice: build $G$, take an eigenvalue decomposition, and read off coordinates. This is classical [multidimensional scaling](/multidimensional-scaling/), which on noisy data keeps the $d$ largest eigenvalues.

## Examples and non-examples

All values are exact.

- **A segment.** For $p_0 = (0, 0)$ and $p_1 = (3, 4)$, $D_{01} = 25$ and $\mathrm{CM} = \det \begin{pmatrix} 0 & 1 & 1 \\ 1 & 0 & 25 \\ 1 & 25 & 0 \end{pmatrix} = 50 = 2 \cdot 5^2$.
- **The 3, 4, 5 triangle.** For $(0, 0)$, $(4, 0)$ and $(0, 3)$, the squared sides are $16$, $9$ and $25$. Then $a^2 + b^2 + c^2 = 962$ and $2(ab + bc + ca) = 1538$, so $\mathrm{CM} = -576 = -16 \cdot 6^2$. The area is 6.
- **Tetrahedra.** The tetrahedron $(0, 0, 0)$, $(1, 0, 0)$, $(0, 1, 0)$, $(0, 0, 1)$ has volume $1/6$ and $\mathrm{CM} = 8 = 288 / 36$. The tetrahedron $(0, 0, 0)$, $(2, 0, 0)$, $(0, 3, 0)$, $(0, 0, 4)$ has volume 4, Gram determinant $576 = (3! \cdot 4)^2$, and $\mathrm{CM} = 4608 = 288 \cdot 16$.
- **Flat simplices.** Points $0, 1, 3$ on a line have squared distances $1, 9, 4$, and $\mathrm{CM} = 98 - 98 = 0$. The four corners of the unit square give $\mathrm{CM} = 0$, as does any set of five points in $\mathbb{R}^3$, since their simplex has no 4-dimensional volume.
- **Lengths that are not a triangle.** The lengths $1, 1, 3$ break the triangle inequality. The squared lengths $1, 1, 9$ give $\mathrm{CM} = 83 - 38 = 45 > 0$, so $-16 A^2 = 45$ has no real solution and no triangle has these sides. For three points the sign condition of the realizability theorem is exactly the triangle inequality.
- **A distance constraint from a determinant.** Take the rectangle $A = (0, 0)$, $B = (4, 0)$, $C = (4, 3)$, $D = (0, 3)$ and forget $x = \lvert BD \rvert^2$. The other five squared distances are $\lvert AB \rvert^2 = 16$, $\lvert BC \rvert^2 = 9$, $\lvert CD \rvert^2 = 16$, $\lvert DA \rvert^2 = 9$ and $\lvert AC \rvert^2 = 25$. Four points in the plane need $\mathrm{CM}(A, B, C, D) = 0$, which as a function of $x$ is
$$ -50 x^2 + 1348 x - 2450 = -2 (25 x^2 - 674 x + 1225) = 0, $$
with roots $x = 25$ and $x = 49/25$. The root 25 is the rectangle. The root $49/25$ belongs to the other placement of $D$, its mirror image $(72/25, -21/25)$ in the diagonal $AC$, which keeps $\lvert AD \rvert^2 = 9$ and $\lvert CD \rvert^2 = 16$. This is the two-solution choice of a [circle-circle intersection](/circle-circle-intersection/), written without coordinates, and the choice between the roots is the [root identification problem](/root-identification-problem/). For $x$ strictly between the roots, $\mathrm{CM} > 0$, which is $288 V^2$ of a real tetrahedron: the triangle $ACD$ turned out of the plane about $AC$.
- **Non-example: unsquared distances.** The determinant must be formed from squared distances. With the plain lengths $3, 4, 5$ in place of $9, 16, 25$ the identity fails, since the matrix entries enter the volume formula through the Gram matrix, which is linear in the squares.
- **Non-example: one sign condition is not enough.** Take five points with squared distances $D_{01} = 1$, $D_{02} = 6$, $D_{03} = 4$, $D_{04} = 1$, $D_{12} = 3$, $D_{13} = 8$, $D_{14} = 7$, $D_{23} = 1$, $D_{24} = 9$ and $D_{34} = 3$. The Gram matrix has $\det G = 1101/16 > 0$, so $\mathrm{CM} = -1101$ has the sign of a real 4-simplex. Yet the face $p_0 p_1 p_4$ has lengths $1, 1, \sqrt 7$, which break the triangle inequality, and its determinant is $51 - 30 = 21 > 0$. A symmetric matrix with a positive determinant can have negative principal minors, which is why the theorem asks for the sign condition on every subset.

## Related definitions

- **Gram matrix and distance matrix.** The map $D \mapsto G$ with $G_{ij} = (D_{0i} + D_{0j} - D_{ij})/2$ and its inverse $D_{ij} = G_{ii} + G_{jj} - 2G_{ij}$ convert between squared distances and inner products. Classical [multidimensional scaling](/multidimensional-scaling/) uses the centred form of the same map.
- **[Distance geometry problem](/distance-geometry-problem/).** When only some of the distances are given, realizability asks for values of the missing entries that make all the Cayley-Menger conditions hold. The missing entries enter the determinants as unknowns, so the conditions become polynomial equations and inequalities. Deciding them is NP-hard already on a line.
- **[Rigidity matrix](/rigidity-matrix/).** The rigidity matrix is the derivative of the squared lengths with respect to coordinates. The Cayley-Menger approach drops the coordinates and works with the squared lengths themselves as unknowns.
- **Distance constraint solving.** For a [bar-and-joint framework](/bar-and-joint-framework/) built by adding one point at a time, as in [constructive constraint solving](/constructive-constraint-solving/), each new point in the plane lies on a triangle, and each in space on a tetrahedron, whose Cayley-Menger determinant gives the new distances in closed form.
- **Semidefinite relaxation.** Realizability in some dimension is the positive semidefiniteness of $G$, a linear matrix inequality in the unknown squared distances, so it can be handled by [semidefinite programming](/semidefinite-programming/). The rank condition for $\mathbb{R}^d$ is not convex, and dropping it is the usual relaxation.

## References
