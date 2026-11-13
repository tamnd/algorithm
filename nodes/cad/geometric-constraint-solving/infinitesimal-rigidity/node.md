---
tag: 8VRWCE
kind: definition
slug: infinitesimal-rigidity
name: Infinitesimal rigidity
aliases:
- first-order rigidity
area: cad/geometric-constraint-solving
level: advanced
summary: A framework with n >= d joints is infinitesimally rigid when its rigidity matrix, one row of endpoint differences per bar, has rank dn - d(d + 1)/2. It implies rigidity.
prereqs: [bar-and-joint-framework, rank]
see_also: [generic-rigidity, maxwell-counting-rule, laman-theorem, global-rigidity, rigid-body-twist, kinematic-singularity, rank-computation, gaussian-elimination]
sources:
  - book: isbn:9780821838013
    title: Jack Graver, Brigitte Servatius and Herman Servatius, Combinatorial Rigidity, Graduate Studies in Mathematics 2, American Mathematical Society, 1993
    locator: Chapter 2, Infinitesimal Rigidity
  - paper: doi:10.1090/S0002-9947-1978-0511410-9
    title: L. Asimow and B. Roth, The rigidity of graphs, Transactions of the American Mathematical Society 245, 279 to 289, 1978
    locator: the rigidity matrix, the dimension of the trivial motions, and the theorem that infinitesimal rigidity implies rigidity
  - paper: "L. Asimow and B. Roth, The rigidity of graphs II, Journal of Mathematical Analysis and Applications 68, 171 to 190, 1979"
    locator: infinitesimal rigidity and the static view by loads and stresses
  - paper: doi:10.1016/0020-7683(78)90052-5
    title: C. R. Calladine, Buckminster Fuller's tensegrity structures and Clerk Maxwell's rules for the construction of stiff frames, International Journal of Solids and Structures 14(2), 161 to 172, 1978
    locator: the relation between the numbers of bars, joints, self-stresses and mechanisms
---

Infinitesimal rigidity is the linear version of rigidity for a [bar-and-joint framework](/bar-and-joint-framework/). A velocity for each joint is an *infinitesimal motion* if no bar gets longer or shorter to first order. The framework is infinitesimally rigid when the only such velocities come from moving the whole space. The test is a [rank](/rank/) computation on the *rigidity matrix*, with one row per bar, and infinitesimal rigidity implies rigidity.

## Definition

Let $(G, p)$ be a framework in $\mathbb{R}^d$ with $G = (V, E)$, $V = \{1, \ldots, n\}$ and $m = |E|$. Put $D = d(d + 1)/2$. So $D = 3$ in the plane and $D = 6$ in space.

**Infinitesimal motion.** A list $u = (u_1, \ldots, u_n)$ of vectors $u_i \in \mathbb{R}^d$ is an *infinitesimal motion* of $(G, p)$ if
$$ (p_i - p_j) \cdot (u_i - u_j) = 0 \quad \text{for every bar } ij \in E. $$
This is the derivative at $t = 0$ of $\lVert p_i(t) - p_j(t) \rVert^2$ for a path with $p(0) = p$ and $p'(0) = u$, divided by 2.

**Rigidity matrix.** The rigidity matrix $R(G, p)$ is the $m \times dn$ matrix with one row for each bar $ij$ and $d$ columns for each vertex. The row of $ij$ holds $p_i - p_j$ in the columns of $i$, $p_j - p_i$ in the columns of $j$, and zeros elsewhere. So the infinitesimal motions are the kernel of $R(G, p)$, and $R(G, p)$ is half the Jacobian of the edge function $f_G(q) = (\lVert q_i - q_j \rVert^2)_{ij \in E}$ at $p$. For a triangle $1 2 3$ in the plane:
$$ R = \begin{pmatrix} p_1 - p_2 & p_2 - p_1 & 0 \\ p_1 - p_3 & 0 & p_3 - p_1 \\ 0 & p_2 - p_3 & p_3 - p_2 \end{pmatrix}, $$
where each entry is a block of two columns.

**Trivial motions.** For a skew-symmetric $d \times d$ matrix $A$ ($A^\top = -A$) and a vector $b \in \mathbb{R}^d$, the velocities $u_i = A p_i + b$ form an infinitesimal motion of every framework on the points $p$, because $(p_i - p_j) \cdot A (p_i - p_j) = 0$. They are the derivatives of the rigid motions, the [twists](/rigid-body-twist/) of the whole space, and they form the space $T(p)$ of *trivial* motions. Skew matrices have dimension $d(d - 1)/2$ and translations dimension $d$, so $\dim T(p) \le D$. If the affine span of $p_1, \ldots, p_n$ has dimension at least $d - 1$, then the map $(A, b) \mapsto u$ is injective and $\dim T(p) = D$: a twist that vanishes on $d$ affinely independent points is zero. In the plane this means the points are not all equal.

**Infinitesimally rigid.** $(G, p)$ is *infinitesimally rigid* if every infinitesimal motion is trivial, that is, $\ker R(G, p) = T(p)$. Otherwise it is *infinitesimally flexible*.

**Rank form.** Let $n \ge d$. Then $(G, p)$ is infinitesimally rigid if and only if
$$ \operatorname{rank} R(G, p) = dn - D. $$
For $n \le d + 1$ the condition means that $G$ is complete and the points are affinely independent, and $dn - D = n(n - 1)/2$ at $n = d$ and at $n = d + 1$. For $n < d$ the formula $dn - D$ is wrong, and the right count is $n(n - 1)/2$: a complete graph on affinely independent points.

*Proof of the rank form.* If the points span an affine space of dimension $k \ge d - 1$, then $\dim T(p) = D$ and $T(p) \subseteq \ker R$. So $\ker R = T(p)$ if and only if $\dim \ker R = D$, which is $\operatorname{rank} R = dn - D$. Now let the span have dimension $k \le d - 2$. Every row of $R$ lies in the directions of the span, so $\operatorname{rank} R \le \operatorname{rank} R(K_n, p) = kn - k(k + 1)/2$, and
$$ dn - D - \Big(kn - \tfrac{k(k+1)}{2}\Big) = (d - k)\Big(n - \tfrac{d + k + 1}{2}\Big) > 0 \quad \text{for } n \ge d. $$
So the rank is below $dn - D$. Such a framework is also infinitesimally flexible: the velocities orthogonal to the span are free, which gives $n(d - k)$ dimensions, and only $(d - k)(k + 1)$ of them are trivial, so for $n \ge k + 2$ a non-trivial motion exists. Since $n \ge d \ge k + 2$, both sides of the claimed equivalence are false.

**Infinitesimal rigidity implies rigidity.** Let $(G, p)$ with $n \ge d$ be infinitesimally rigid. The rank of $R(G, q)$ is at most $dn - D$ for every $q$ whose span has dimension at least $d - 1$, and the rank cannot drop near $p$ because a nonzero minor stays nonzero. So the rank is constant, equal to $dn - D$, on a neighborhood of $p$. By the constant rank theorem, the set of equivalent placements $f_G^{-1}(f_G(p))$ is, near $p$, a smooth manifold of dimension $dn - (dn - D) = D$. The placements congruent to $p$ form the orbit of $p$ under the isometry group, which is also a manifold of dimension $D$ (the stabilizer of $p$ is finite, since the span has dimension at least $d - 1$), and it lies inside the fiber. A $D$-manifold inside a $D$-manifold is open in it (invariance of domain), and the orbit is closed. So near $p$ the fiber equals the orbit: every equivalent placement close to $p$ is congruent. This is local uniqueness, which gives rigidity as shown on the [framework page](/bar-and-joint-framework/). For $n < d$, infinitesimal rigidity forces $G$ to be complete, and complete frameworks are rigid.

**Statics.** A vector $\omega \in \mathbb{R}^E$ with $\omega^\top R(G, p) = 0$ is a *self-stress*: tensions $\omega_{ij}$ in the bars that are in equilibrium at every joint. By rank and nullity, with $s = \dim$ of the self-stresses and $f = \dim \ker R - \dim T(p)$ the number of independent non-trivial motions,
$$ m - (dn - D) = s - f $$
when $\dim T(p) = D$. This is the Maxwell and Calladine count. A framework is infinitesimally rigid exactly when $f = 0$, which is also the statement that every load with zero total force and zero total moment is balanced by tensions in the bars (static rigidity).

## Examples and non-examples

The ranks below are exact ranks over the rationals, computed by [Gaussian elimination](/gaussian-elimination/).

- **Triangle in general position.** $K_3$ at three points not on a line has rank 3 $= 2 \cdot 3 - 3$, so it is infinitesimally rigid.
- **Collinear triangle.** $K_3$ at $(0, 0)$, $(1, 0)$, $(3, 0)$ has rank 2. The velocity $u_2 = (0, 1)$, $u_1 = u_3 = 0$ is a non-trivial infinitesimal motion: each row has the form $(x, 0)$ in the columns of each vertex, so a vertical velocity changes no length to first order. The framework is rigid all the same, as the [framework page](/bar-and-joint-framework/) shows. So the converse of the implication fails.
- **Collinear 4-cycle.** The 4-cycle at $0, 1, 2, 3$ on a line, with bars $ab$, $bc$, $cd$, $da$, has rank 3, below $2 \cdot 4 - 3 = 5$. It is rigid, even globally rigid, but not infinitesimally rigid.
- **$K_{3,3}$ on a conic.** The complete bipartite graph $K_{3,3}$ has $9 = 2 \cdot 6 - 3$ bars. At random integer points the rank is 9, so it is infinitesimally rigid. At the six rational points of the unit circle $\big((1 - t^2)/(1 + t^2), 2t/(1 + t^2)\big)$ with $t = 0, 1, 2$ on one side and $t = -1, \tfrac{1}{2}, 3$ on the other, the rank is 8. A classical theorem says that $K_{3,3}$ is infinitesimally flexible exactly when the six points lie on a conic. This is a [kinematic singularity](/kinematic-singularity/) of the same kind as in a [parallel manipulator](/parallel-manipulator/).
- **Planar framework read in space.** The two triangles $abc$, $abd$ sharing $ab$ have rank 5 in the plane and in $\mathbb{R}^3$. In the plane $5 = 2 \cdot 4 - 3$, so it is infinitesimally rigid. In space the target is $3 \cdot 4 - 6 = 6$, so it is infinitesimally flexible, and in fact flexible.
- **Tetrahedron.** $K_4$ at four points not on a plane has rank 6 $= 3 \cdot 4 - 6$ in $\mathbb{R}^3$.

## Related definitions

- **[Rigidity](/bar-and-joint-framework/).** The nonlinear notion. Infinitesimal rigidity implies it. The collinear examples above are rigid but not infinitesimally rigid.
- **[Generic rigidity](/generic-rigidity/).** At a generic placement the rank of $R(G, p)$ is the largest possible, and there rigidity and infinitesimal rigidity agree (Asimow and Roth). This makes rigidity at almost every placement a property of the graph.
- **[Maxwell's counting rule](/maxwell-counting-rule/).** The rank form gives at once that an infinitesimally rigid framework with $n \ge d$ has at least $dn - D$ bars.
- **Rigidity matroid.** The linear matroid of the rows of $R(G, p)$ at a generic $p$, a [linear matroid](/linear-matroid/) on the edge set. In the plane its bases are the graphs of [Laman's theorem](/laman-theorem/).
- **Second-order and prestress stability.** Between infinitesimal rigidity and rigidity there are tests that use a self-stress and second derivatives (Connelly and Whiteley). They prove rigidity for some infinitesimally flexible frameworks, such as the collinear triangle.
- **Robotics.** For a [parallel manipulator](/parallel-manipulator/), a drop in the rank of the constraint Jacobian is a [kinematic singularity](/kinematic-singularity/), the same event as an infinitesimal flex.

## References
