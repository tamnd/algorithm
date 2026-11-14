---
tag: TYQ8Y9
kind: definition
slug: equilibrium-stress-matrix
name: Equilibrium stress matrix
aliases:
- stress matrix
- self-stress
area: cad/geometric-constraint-solving
level: advanced
summary: An equilibrium stress puts a weight on each bar so the bar forces cancel at every joint. Its stress matrix is a signed weighted Laplacian, the key tool for global rigidity.
prereqs: [rigidity-matrix, laplacian-matrix]
see_also: [connelly-global-rigidity-theorem, gortler-healy-thurston-theorem, jackson-jordan-theorem, global-rigidity, infinitesimal-rigidity, hendrickson-global-rigidity-conditions, tutte-embedding, semidefinite-programming]
sources:
  - paper: doi:10.1007/BF01404753
    title: R. Connelly, Rigidity and energy, Inventiones Mathematicae 66(1), 11 to 33, 1982
    locator: the stress matrix, the quadratic energy form of a stress, and the use of positive semidefinite stress matrices to prove rigidity
  - paper: doi:10.1007/s00454-004-1124-4
    title: R. Connelly, Generic global rigidity, Discrete and Computational Geometry 33(4), 549 to 563, 2005
    locator: the stress matrix of a generic framework, its kernel, and the rank n - d - 1 condition
  - paper: doi:10.1353/ajm.0.0132
    title: Steven J. Gortler, Alexander D. Healy and Dylan P. Thurston, Characterizing generic global rigidity, American Journal of Mathematics 132(4), 897 to 939, 2010
    locator: the stress kernel and the shared stresses of equivalent generic frameworks
  - paper: doi:10.1137/S0895480192229236
    title: R. Connelly and W. Whiteley, Second-order rigidity and prestress stability for tensegrity frameworks, SIAM Journal on Discrete Mathematics 9(3), 453 to 491, 1996
    locator: the stress matrix as the Hessian of the stress energy and prestress stability
  - book: isbn:9780821838013
    title: Jack Graver, Brigitte Servatius and Herman Servatius, Combinatorial Rigidity, Graduate Studies in Mathematics 2, American Mathematical Society, 1993
    locator: Chapter 2, the static view of the rigidity matrix (stresses and loads)
---

An equilibrium stress of a [bar-and-joint framework](/bar-and-joint-framework/) is a number on each bar, read as a tension or a compression, such that the bar forces cancel at every joint. The stresses are the left kernel of the [rigidity matrix](/rigidity-matrix/). Each stress gives an $n \times n$ symmetric matrix, the stress matrix, which is a [Laplacian](/laplacian-matrix/) with signed weights. Its kernel contains the coordinates of the joints, and its quadratic form is the stress energy. These two facts make it the main tool of the [global rigidity](/global-rigidity/) theorems of Connelly and of Gortler, Healy and Thurston.

## Definition

Let $(G, p)$ be a framework in $\mathbb{R}^d$, with $G = (V, E)$, $V = \{1, \ldots, n\}$, $m = |E|$, and points $p_i \in \mathbb{R}^d$. Write $\omega_{ij} = \omega_{ji}$ for the value of a vector $\omega \in \mathbb{R}^E$ on the edge $ij$. Let $P$ be the $n \times d$ matrix whose row $i$ is $p_i^\top$, and let $\mathbf{1}$ be the all-ones vector of length $n$.

**Equilibrium stress.** A vector $\omega \in \mathbb{R}^E$ is an *equilibrium stress* (or *self-stress*) of $(G, p)$ if for every vertex $i$
$$ \sum_{j : ij \in E} \omega_{ij} \, (p_j - p_i) = 0. $$
With the convention used here, $\omega_{ij} > 0$ is a tension: the bar pulls each end toward the other. By Fact 3 of the [rigidity matrix page](/rigidity-matrix/), the equilibrium stresses are exactly the vectors with $\omega^\top R(G, p) = 0$. They form a linear space $S(G, p)$ of dimension $m - \operatorname{rank} R(G, p)$. In the count of Maxwell and Calladine on the [infinitesimal rigidity page](/infinitesimal-rigidity/), this dimension is the number $s$ of independent self-stresses.

**Stress matrix.** For any $\omega \in \mathbb{R}^E$, the *stress matrix* $\Omega = \Omega(\omega)$ is the symmetric $n \times n$ matrix with
$$ \Omega_{ij} = -\omega_{ij} \ (ij \in E), \qquad \Omega_{ij} = 0 \ (i \ne j, \ ij \notin E), \qquad \Omega_{ii} = \sum_{j : ij \in E} \omega_{ij}. $$
It is the weighted Laplacian of $G$ with the weights $\omega$, which may be negative or zero. Every row sums to zero, so $\Omega \mathbf{1} = 0$. The matrix is defined for every $\omega$, but it is called an *equilibrium* stress matrix of $(G, p)$ only when $\omega \in S(G, p)$.

**Fact 1 (quadratic form).** For every $x \in \mathbb{R}^n$,
$$ x^\top \Omega x = \sum_{ij \in E} \omega_{ij} \, (x_i - x_j)^2 . $$
So for a placement $q$ with coordinate matrix $Q$ (rows $q_i^\top$), the *stress energy* is
$$ E_\omega(q) = \sum_{ij \in E} \omega_{ij} \, \lVert q_i - q_j \rVert^2 = \operatorname{tr}(Q^\top \Omega Q) = \sum_{k=1}^{d} x_k^\top \Omega x_k , $$
where $x_k$ is column $k$ of $Q$, the vector of the $k$-th coordinates.

*Proof.* Expand $\sum_{ij \in E} \omega_{ij} (x_i - x_j)^2 = \sum_{ij \in E} \omega_{ij} (x_i^2 + x_j^2) - 2 \sum_{ij \in E} \omega_{ij} x_i x_j$. The first sum gives $x_i^2$ the weight $\sum_j \omega_{ij} = \Omega_{ii}$. The second sum is $\sum_{i \ne j} \Omega_{ij} x_i x_j$ with $\Omega_{ij} = -\omega_{ij}$, counted once for each ordered pair, which is twice per edge. Together this is $x^\top \Omega x$. The formula for $E_\omega$ follows by summing over the $d$ coordinates, since $\lVert q_i - q_j \rVert^2$ is the sum of the squared coordinate differences. $\square$

Note that $E_\omega(q) = \omega \cdot f_G(q)$, where $f_G(q) = (\lVert q_i - q_j \rVert^2)_{ij \in E}$ is the edge function. So $E_\omega$ takes the same value on all placements with the same bar lengths, and its Hessian is the constant matrix $2\, \Omega \otimes I_d$.

**Fact 2 (equilibrium in matrix form).** $\omega$ is an equilibrium stress of $(G, p)$ if and only if $\Omega P = 0$. Then also $\Omega [\, P \;\; \mathbf{1} \,] = 0$, and $E_\omega(p) = 0$.

*Proof.* Row $i$ of $\Omega P$ is $\Omega_{ii} p_i^\top - \sum_{j : ij \in E} \omega_{ij} p_j^\top = \sum_{j : ij \in E} \omega_{ij} (p_i - p_j)^\top$, which is zero for all $i$ exactly when $\omega$ is in equilibrium. $\Omega \mathbf{1} = 0$ always holds. Then $E_\omega(p) = \operatorname{tr}(P^\top \Omega P) = 0$. $\square$

**Fact 3 (rank bound).** If the points of $p$ affinely span $\mathbb{R}^d$ and $\omega$ is an equilibrium stress, then
$$ \operatorname{rank} \Omega \le n - d - 1. $$

*Proof.* The $n \times (d + 1)$ matrix $[\, P \;\; \mathbf{1} \,]$ has rank $d + 1$: a vector $(a, b)$ in its kernel gives $a \cdot p_i + b = 0$ for all $i$, an affine function that vanishes on a spanning set, so $a = 0$ and $b = 0$. Its columns lie in $\ker \Omega$ by Fact 2, so $\dim \ker \Omega \ge d + 1$. $\square$

**Fact 4 (affine images and the kernel).** Let $\omega$ be an equilibrium stress of $(G, p)$. Then $\omega$ is an equilibrium stress of $(G, q)$ for every affine image $q_i = M p_i + c$, with $M$ any $d' \times d$ matrix and $c \in \mathbb{R}^{d'}$, in any dimension $d'$. If moreover $p$ spans $\mathbb{R}^d$ and $\operatorname{rank} \Omega = n - d - 1$, the converse holds: $\omega$ is an equilibrium stress of $(G, q)$ only if $q$ is an affine image of $p$.

*Proof.* The coordinate matrix of $q$ is $Q = P M^\top + \mathbf{1} c^\top$, so $\Omega Q = \Omega P M^\top + \Omega \mathbf{1} c^\top = 0$, and Fact 2 applies. For the converse, $\ker \Omega$ has dimension $d + 1$ and contains the $d + 1$ independent columns of $[\, P \;\; \mathbf{1} \,]$, so it is their span. If $\Omega Q = 0$, every column of $Q$ is in this span, that is, each coordinate of $q_i$ is $a \cdot p_i + b$ for fixed $a$ and $b$. This is the statement $q_i = M p_i + c$. $\square$

**Fact 5 (positive semidefinite stresses).** If $\Omega$ is positive semidefinite, $p$ spans $\mathbb{R}^d$, $\operatorname{rank} \Omega = n - d - 1$, and $\omega$ is an equilibrium stress of $(G, p)$, then every placement $q$ in any dimension with the same bar lengths as $p$ is an affine image of $p$.

*Proof.* $E_\omega(q) = \omega \cdot f_G(q) = \omega \cdot f_G(p) = E_\omega(p) = 0$. By Fact 1, $\sum_k x_k^\top \Omega x_k = 0$, and each term is at least 0, so each is 0. For a positive semidefinite matrix, $x^\top \Omega x = 0$ implies $\Omega x = 0$. So $\Omega Q = 0$ and Fact 4 applies. $\square$

Fact 5 is the first step of Connelly's sufficient condition for [global rigidity](/connelly-global-rigidity-theorem/). The second step rules out the affine images that are not congruent to $p$. In the generic case Connelly drops the sign condition and uses a different argument, and [Gortler, Healy and Thurston](/gortler-healy-thurston-theorem/) prove the converse.

**Computing.** A basis of $S(G, p)$ is a basis of the null space of $R(G, p)^\top$, found by [Gaussian elimination](/gaussian-elimination/) in $O(m \, (dn)^2)$ field operations. A random linear combination of the basis vectors has, with high probability, the largest stress matrix rank over the whole space, by the same [Schwartz-Zippel](/schwartz-zippel-lemma/) argument as in the [witness method](/witness-configuration-method/), because the rank of $\Omega(\omega)$ is the rank of a matrix linear in the coefficients.

## Examples and non-examples

All values are exact rationals. The random placements are integer points with a fixed seed.

- **The square with both diagonals.** $K_4$ at $p_1 = (0, 0)$, $p_2 = (1, 0)$, $p_3 = (1, 1)$, $p_4 = (0, 1)$ has a one-dimensional space of stresses, spanned by $\omega = 1$ on the four sides and $\omega = -1$ on the diagonals $13$ and $24$. The stress matrix is
$$ \Omega = \begin{pmatrix} 1 & -1 & 1 & -1 \\ -1 & 1 & -1 & 1 \\ 1 & -1 & 1 & -1 \\ -1 & 1 & -1 & 1 \end{pmatrix} = v v^\top, \qquad v = (1, -1, 1, -1)^\top . $$
It has rank $1 = 4 - 2 - 1$ and is positive semidefinite. Its kernel is $v^\perp$, which holds $\mathbf{1}$, the $x$-coordinates $(0, 1, 1, 0)$ and the $y$-coordinates $(0, 0, 1, 1)$. The energy is $E_\omega(q) = (v \cdot x)^2 + (v \cdot y)^2$. For $q = (0, 0), (2, 0), (3, 1), (0, 1)$ the sides give $4 + 2 + 9 + 1 = 16$, the diagonals give $10 + 5 = 15$, and $16 - 15 = 1 = (0 - 2 + 3 - 0)^2 + (0 - 0 + 1 - 1)^2$. As a tensegrity, the sides are cables in tension and the diagonals are struts in compression.
- **Four points on a line.** The 4-cycle $12, 23, 34, 14$ at $0, 2, 5, 9$ in $\mathbb{R}^1$ has the stress $\omega = (-18, -12, -9, 4)$, unique up to scale. At vertex 1: $-18 \cdot (2 - 0) + 4 \cdot (9 - 0) = 0$. Its stress matrix
$$ \Omega = \begin{pmatrix} -14 & 18 & 0 & -4 \\ 18 & -30 & 12 & 0 \\ 0 & 12 & -21 & 9 \\ -4 & 0 & 9 & -5 \end{pmatrix} $$
has rank $2 = 4 - 1 - 1$, with kernel spanned by $\mathbf{1}$ and $(0, 2, 5, 9)$. It is not positive semidefinite, since its diagonal has negative entries.
- **$K_5$ in the plane.** At a random placement the stresses form a space of dimension $10 - 7 = 3$. The basis vectors that elimination returns have stress matrices of rank 1, while a random combination has rank $2 = 5 - 2 - 1$, the largest allowed by Fact 3.
- **A triangular prism with one more edge.** The prism (triangles $123$ and $456$ and the edges $14$, $25$, $36$) at a random placement in the plane has no stress, since its 9 edges are independent. With the edge $15$ added, the stress space has dimension 1, the stress is nonzero on all 10 edges, and $\Omega$ has rank $3 = 6 - 2 - 1$. The graph is 3-connected and redundantly rigid, so by the [Jackson and Jordán theorem](/jackson-jordan-theorem/) it is generically globally rigid, in line with this rank.
- **$K_{5,5}$ in space.** At three random placements in $\mathbb{R}^3$ the rigidity matrix has rank $24 = 3 \cdot 10 - 6$, the stress space has dimension 1, the stress is nonzero on all 25 edges, and the stress matrix has rank 2, far below $10 - 3 - 1 = 6$. By the theorem of [Gortler, Healy and Thurston](/gortler-healy-thurston-theorem/) this shows that $K_{5,5}$ is not generically globally rigid in space.
- **A stress at a special placement.** $K_{3,3}$ in the plane has no stress at a random placement. At six rational points of the unit circle (parameters $t = 0, 1, 2$ and $t = -1, \tfrac{1}{2}, 3$ of $((1 - t^2)/(1 + t^2), 2t/(1 + t^2))$) the rank drops to 8, and a one-dimensional stress space appears, with stress matrix of rank 3.
- **Non-example: the plain Laplacian.** All weights $\omega_{ij} = 1$ give the Laplacian $L$ of $G$. It is an equilibrium stress only if $L P = 0$, that is, every point is the average of its neighbors. For a connected graph this forces all points to coincide, because $\ker L$ is spanned by $\mathbf{1}$. A [Tutte embedding](/tutte-embedding/) uses positive weights of this kind, but it pins the outer face and asks for equilibrium only at the inner vertices.
- **Non-example: a vector off the left kernel.** For the square above, $\omega = 1$ on every edge gives a stress matrix with $\Omega P \ne 0$: at $p_1$ the forces are $(1, 0) + (0, 1) + (1, 1) = (2, 2)$. Fact 3 does not apply, and the matrix says nothing about the framework.

## Related definitions

- **[Rigidity matrix](/rigidity-matrix/).** The stresses are its left kernel. Their number is $m - \operatorname{rank} R(G, p)$.
- **[Infinitesimal rigidity](/infinitesimal-rigidity/).** By duality, a framework is infinitesimally rigid exactly when every equilibrium load is resolved by bar tensions. A stress is a resolution of the zero load.
- **Redundant edge.** An edge is redundant at $p$ exactly when some stress is nonzero on it, because removing it keeps the rank exactly when its row is a combination of the others. This links the stresses to the redundant rigidity condition of [Hendrickson](/hendrickson-global-rigidity-conditions/).
- **[Connelly's theorem](/connelly-global-rigidity-theorem/).** A generic framework with a stress whose matrix has rank $n - d - 1$ is globally rigid.
- **[Gortler, Healy and Thurston](/gortler-healy-thurston-theorem/).** The converse: a generically globally rigid graph with $n \ge d + 2$ has such a stress at every generic placement.
- **Tensegrity and universal rigidity.** With cables ($\omega \ge 0$) and struts ($\omega \le 0$), a positive semidefinite stress matrix of rank $n - d - 1$ plus a condition on the edge directions proves rigidity in every dimension. Finding such a matrix is a [semidefinite program](/semidefinite-programming/).
- **Prestress stability.** The Hessian of $E_\omega$ is $2\, \Omega \otimes I_d$. Connelly and Whiteley test rigidity of an infinitesimally flexible framework by asking that this form be positive on the non-trivial infinitesimal motions for some stress $\omega$.

## References
