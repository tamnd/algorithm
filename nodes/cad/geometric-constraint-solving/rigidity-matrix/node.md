---
tag: EK6JQ0
kind: definition
slug: rigidity-matrix
name: Rigidity matrix
aliases:
- framework rigidity matrix
area: cad/geometric-constraint-solving
level: core
summary: The m by dn matrix of a framework, one row per bar holding p_i - p_j and p_j - p_i. It is half the Jacobian of the squared bar lengths, and its kernel holds the rigid motions.
prereqs: [bar-and-joint-framework, rank]
see_also: [infinitesimal-rigidity, generic-rigidity, equilibrium-stress-matrix, asimow-roth-theorem, laman-theorem, pebble-game-rigidity, witness-configuration-method, incidence-matrix]
sources:
  - paper: doi:10.1090/S0002-9947-1978-0511410-9
    title: L. Asimow and B. Roth, The rigidity of graphs, Transactions of the American Mathematical Society 245, 279 to 289, 1978
    locator: the edge function, its derivative, and the rank of the derivative at regular points
  - book: isbn:9780821838013
    title: Jack Graver, Brigitte Servatius and Herman Servatius, Combinatorial Rigidity, Graduate Studies in Mathematics 2, American Mathematical Society, 1993
    locator: Chapter 2 (the rigidity matrix and infinitesimal motions) and Chapter 4 (the rigidity matroid in the plane)
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, CRC Press, 2018
    locator: the chapters on combinatorial rigidity and on frameworks
---

The rigidity matrix is the linear part of a [bar-and-joint framework](/bar-and-joint-framework/). It has one row for each bar and $d$ columns for each joint, and it is half the derivative of the map that sends a placement to its squared bar lengths. Every question about first-order motion, about stresses in the bars, and about rigidity at a generic placement is a question about the [rank](/rank/), the kernel or the left kernel of this one sparse matrix.

## Definition

Let $G = (V, E)$ be a graph with $V = \{1, \ldots, n\}$ and $m = |E|$ edges, and let $p = (p_1, \ldots, p_n)$ be a placement of the vertices in $\mathbb{R}^d$. Fix an order of the edges and write each edge as $ij$ with $i < j$. Put $D = d(d + 1)/2$.

**The matrix.** The rigidity matrix $R(G, p)$ is the real $m \times dn$ matrix whose columns come in $n$ blocks of $d$, one block per vertex. The row of the edge $ij$ is
$$ \big( 0, \ldots, 0, \; \underbrace{p_i - p_j}_{\text{block } i}, \; 0, \ldots, 0, \; \underbrace{p_j - p_i}_{\text{block } j}, \; 0, \ldots, 0 \big). $$
So a row has at most $2d$ nonzero entries, the two blocks in a row are negatives of each other, and the sum of the $n$ blocks of every row is zero. The order of the rows and of the vertices changes $R$ only by permutations, which do not change the rank, the kernel dimension or the left kernel dimension.

**The edge function.** The edge function of $G$ is the polynomial map
$$ f_G : \mathbb{R}^{dn} \to \mathbb{R}^{m}, \qquad f_G(q) = \big( \lVert q_i - q_j \rVert^2 \big)_{ij \in E}. $$
Two placements are *equivalent* when they have the same image under $f_G$.

**Fact 1 (Jacobian).** $df_G(p) = 2 R(G, p)$. In words, $R(G, p)$ is half the Jacobian matrix of $f_G$ at $p$.

*Proof.* The coordinate of $f_G$ for the edge $ij$ is $g(q) = \sum_{k=1}^{d} (q_{i,k} - q_{j,k})^2$. It depends only on the $2d$ coordinates of $q_i$ and $q_j$. Its partial derivatives are $\partial g / \partial q_{i,k} = 2(q_{i,k} - q_{j,k})$ and $\partial g / \partial q_{j,k} = -2(q_{i,k} - q_{j,k}) = 2(q_{j,k} - q_{i,k})$, and zero for every other coordinate. At $q = p$ this is twice the row of $ij$. $\square$

So for a velocity $u \in \mathbb{R}^{dn}$ the entry of $R(G, p)\, u$ at the edge $ij$ is $(p_i - p_j) \cdot (u_i - u_j)$, which is half the rate of change of the squared length of $ij$ when the joints move with velocities $u$. The kernel of $R(G, p)$ is the space of *infinitesimal motions*.

**Fact 2 (the rigid motions lie in the kernel).** Let $A$ be a skew-symmetric $d \times d$ matrix and $b \in \mathbb{R}^d$. Then $u_i = A p_i + b$ for all $i$ gives $R(G, p)\, u = 0$ for every graph $G$. If the points $p_1, \ldots, p_n$ affinely span a space of dimension at least $d - 1$, these vectors form a subspace of dimension exactly $D$, so
$$ \operatorname{rank} R(G, p) \le dn - D. $$

*Proof.* Let $Q(t) = e^{tA}$. It is orthogonal for every $t$ because $Q(t)^\top Q(t) = e^{-tA} e^{tA} = I$. The path $q_i(t) = Q(t) p_i + t b$ moves all the points by an isometry, so $f_G(q(t)) = f_G(p)$ for all $t$. Differentiate at $t = 0$ and use Fact 1: $0 = 2 R(G, p)\, q'(0)$, and $q_i'(0) = A p_i + b$. For the dimension, the map $(A, b) \mapsto u$ is linear on a space of dimension $d(d - 1)/2 + d = D$. If $u = 0$, then the affine map $x \mapsto Ax + b$ vanishes on the points, so $A$ vanishes on the linear span $W$ of the differences $p_i - p_1$, which has dimension at least $d - 1$. A skew matrix with $A w = 0$ for all $w \in W$ also has $A^\top = -A$ zero on $W$, so its image is orthogonal to $W$ and has dimension at most 1. A skew matrix has even rank, so $A = 0$, and then $b = -A p_1 = 0$. So the map is injective, its image has dimension $D$ and lies in the kernel, and rank and nullity give the bound. $\square$

The velocities $A p_i + b$ are the *trivial* motions. A framework is [infinitesimally rigid](/infinitesimal-rigidity/) when the bound in Fact 2 is reached.

**Fact 3 (the left kernel is the stresses).** A vector $\omega \in \mathbb{R}^{E}$ satisfies $\omega^\top R(G, p) = 0$ if and only if for every vertex $i$
$$ \sum_{j : ij \in E} \omega_{ij} \, (p_i - p_j) = 0. $$

*Proof.* The block of columns of vertex $i$ in $\omega^\top R$ is the sum over the rows that touch $i$ of $\omega_e$ times the block of $i$ in row $e$. For the edge $ij$ that block is $p_i - p_j$, whichever endpoint has the smaller label. $\square$

Read $\omega_{ij}$ as a tension in the bar $ij$. The vertex condition says that the forces of the bars on each joint add up to zero, so the left kernel is the space of *self-stresses* or *equilibrium stresses*. They are the subject of the [stress matrix page](/equilibrium-stress-matrix/). By rank and nullity the dimension of the left kernel is $m - \operatorname{rank} R(G, p)$.

**Fact 4 (affine invariance).** For an invertible $d \times d$ matrix $M$ and $c \in \mathbb{R}^d$, the placement $q_i = M p_i + c$ has
$$ R(G, q) = R(G, p) \, (I_n \otimes M^\top), $$
where $I_n \otimes M^\top$ is the block diagonal matrix with $n$ copies of $M^\top$, a [Kronecker product](/kronecker-product/). So the rank, the dimension of the kernel and the left kernel itself are the same for $p$ and $q$.

*Proof.* The block of vertex $i$ in the row of $ij$ becomes $(M p_i - M p_j)^\top = (p_i - p_j)^\top M^\top$ when written as a row. The right factor is invertible, so the rank does not change and $\omega^\top R(G, q) = 0$ if and only if $\omega^\top R(G, p) = 0$. $\square$

**Fact 5 (the line).** In $\mathbb{R}^1$ with distinct points, $R(G, p)$ is the oriented [incidence matrix](/incidence-matrix/) of $G$ with the row of $ij$ multiplied by the nonzero number $p_i - p_j$. Its rank is $n - c$, where $c$ is the number of connected components of $G$.

*Proof.* Scaling rows by nonzero numbers does not change the rank. The oriented incidence matrix has rank $n - c$: its kernel is the set of vectors that are constant on each component, because a kernel vector $u$ has $u_i = u_j$ on every edge, so the kernel has dimension $c$. $\square$

So on a line the framework is infinitesimally rigid exactly when $G$ is connected, and the rows of a set of edges are independent exactly when the edges form a forest. The rows form the [graphic matroid](/graphic-matroid/), and the rigidity matroid in higher dimension extends it.

**Generic rank.** Every minor of $R(G, p)$ is a polynomial in the $dn$ coordinates with integer coefficients. Let $r(G)$ be the largest rank over all $p$, and fix an $r(G) \times r(G)$ minor that is not the zero polynomial. The placements where this minor is nonzero form an open dense set, and the rank is $r(G)$ on all of it. In particular the rank is $r(G)$ at every *generic* placement, where the coordinates are algebraically independent over $\mathbb{Q}$. This number is the generic rank of $G$ in dimension $d$. It depends only on the graph and on $d$, and it is the basis of [generic rigidity](/generic-rigidity/) and of the [Asimow and Roth theorem](/asimow-roth-theorem/). A set of edges is *independent* when its rows are independent at a generic placement. These sets are the independent sets of a [linear matroid](/linear-matroid/) on $E$, the generic $d$-dimensional rigidity matroid. For $d = 1$ it is the graphic matroid by Fact 5, and for $d = 2$ [Laman's theorem](/laman-theorem/) describes it by counts.

**Computing it.** Building $R(G, p)$ takes $O(dm)$ time. Its exact rank over the rationals by [Gaussian elimination](/gaussian-elimination/) takes $O(m \, (dn)^2)$ field operations, but the sizes of the fractions can grow. A floating-point rank needs a tolerance on the singular values, and near a special position a small singular value is not a reliable sign of rank loss. The [witness method](/witness-configuration-method/) computes the generic rank at a random integer placement, and in the plane the [pebble game](/pebble-game-rigidity/) finds it with no arithmetic at all.

## Examples and non-examples

All ranks and kernels here are exact over the rationals.

- **A right triangle.** Take $p_1 = (0, 0)$, $p_2 = (4, 0)$, $p_3 = (0, 3)$ and the edges $12$, $13$, $23$ in that order. Then
$$ R = \begin{pmatrix} -4 & 0 & 4 & 0 & 0 & 0 \\ 0 & -3 & 0 & 0 & 0 & 3 \\ 0 & 0 & 4 & -3 & -4 & 3 \end{pmatrix}, $$
which has rank $3 = 2 \cdot 3 - 3$. The kernel has dimension 3. It is spanned by the two translations $(1, 0, 1, 0, 1, 0)$ and $(0, 1, 0, 1, 0, 1)$ and the rotation $u_i = (-y_i, x_i)$, which is $(0, 0, 0, 4, -3, 0)$. The left kernel is zero, so the triangle has no self-stress.
- **A square with both diagonals.** $K_4$ at $(0, 0)$, $(1, 0)$, $(1, 1)$, $(0, 1)$, with the four sides first and then the diagonals $13$ and $24$, has $m = 6$ and rank $5 = 2 \cdot 4 - 3$. The left kernel is spanned by $\omega = (-1, -1, -1, -1, 1, 1)$: compression in the sides and tension in the diagonals, or the other way round. At the corner $(0, 0)$ the forces are $-1 \cdot ((0, 0) - (1, 0)) - 1 \cdot ((0, 0) - (0, 1)) + 1 \cdot ((0, 0) - (1, 1))$, which is $(1, 0) + (0, 1) + (-1, -1) = 0$.
- **The square alone.** The 4-cycle at the same corners has rank 4, so the kernel has dimension $8 - 4 = 4$. One dimension beyond the three trivial motions is the shear of the square into a rhombus. Add one diagonal and the rank is 5, the framework is infinitesimally rigid, and there is still no stress.
- **A line.** In $\mathbb{R}^1$ at $0, 2, 5, 9$, the path $12, 23, 34$ has rank 3, the 4-cycle $12, 23, 34, 14$ also has rank 3 with a one-dimensional left kernel, and the two edges $12, 34$ have rank 2. These are $n - c$ with $c = 1, 1, 2$, as in Fact 5.
- **Rank below the generic rank.** For $K_{3,3}$ in the plane the generic rank is 9, but six points on a conic give rank 8, as the [infinitesimal rigidity](/infinitesimal-rigidity/) page shows. A collinear triangle has rank 2. So a single placement only gives a lower bound on the generic rank.
- **The double banana in space.** Two copies of $K_5$ minus one edge, glued at the two ends of the missing edge, have $n = 8$ and $m = 18 = 3 \cdot 8 - 6$ bars. At three random integer placements in $\mathbb{R}^3$ the rank is 17, and it stays 17 when the hinge edge is added. So the rows of the 18 edges are dependent although every subset of $k \ge 3$ vertices spans at most $3k - 6$ edges. See the [double banana page](/double-banana-graph/).
- **Non-example: the Jacobian of the lengths.** The derivative of the unsquared length $\lVert q_i - q_j \rVert$ is the row of $ij$ divided by the length. That matrix has the same rank as $R$ for distinct endpoints, but its entries are not polynomials, and it is not defined when two joined points coincide. The standard rigidity matrix uses the squared lengths for this reason.
- **Non-example: a constraint Jacobian in general.** A CAD system with angle, incidence and tangency constraints has a Jacobian with rows of other forms. Facts 1 and 2 hold for it only when every constraint is a distance between points, so the counts of this page do not carry over unchanged.

## Related definitions

- **[Infinitesimal rigidity](/infinitesimal-rigidity/).** The framework is infinitesimally rigid when the kernel of $R(G, p)$ holds only the trivial motions, that is, rank $dn - D$ for $n \ge d$. It implies rigidity.
- **[Equilibrium stress matrix](/equilibrium-stress-matrix/).** Each vector in the left kernel of $R(G, p)$ gives an $n \times n$ matrix, the main tool of the [global rigidity](/global-rigidity/) theorems.
- **[Asimow and Roth theorem](/asimow-roth-theorem/).** At a placement where the rank of $R(G, \cdot)$ is locally maximal, rigidity and infinitesimal rigidity agree.
- **[Maxwell's counting rule](/maxwell-counting-rule/).** The bound of Fact 2 gives $m \ge dn - D$ bars for an infinitesimally rigid framework.
- **Rigidity matroid.** The linear matroid of the rows at a generic placement. In the plane its independent sets are the sets that satisfy the $2k - 3$ counts of [Laman's theorem](/laman-theorem/), which the [pebble game](/pebble-game-rigidity/) tests.
- **Body-and-bar and body-and-hinge matrices.** For frameworks made of rigid bodies, each body has $D$ columns and each bar a row given by a line in screw coordinates. The counts change to those of [Tay's theorem](/tay-theorem/).

## References
