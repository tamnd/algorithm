---
tag: HYKYN8
kind: theorem
slug: asimow-roth-theorem
name: Asimow-Roth theorem
aliases:
- Asimow-Roth rigidity theorem
area: cad/geometric-constraint-solving
level: advanced
summary: At a regular placement, where the rigidity matrix has its largest rank, a framework is rigid if and only if it is infinitesimally rigid. So rigidity there is a rank test.
prereqs: [rigidity-matrix, infinitesimal-rigidity]
see_also: [generic-rigidity, bar-and-joint-framework, laman-theorem, witness-configuration-method, global-rigidity, schwartz-zippel-lemma, maxwell-counting-rule]
sources:
  - paper: doi:10.1090/S0002-9947-1978-0511410-9
    title: L. Asimow and B. Roth, The rigidity of graphs, Transactions of the American Mathematical Society 245, 279 to 289, 1978
    locator: the regular points of the edge function and the main theorem that rigidity at a regular point is decided by the rank of its derivative
  - paper: "L. Asimow and B. Roth, The rigidity of graphs II, Journal of Mathematical Analysis and Applications 68, 171 to 190, 1979"
    locator: infinitesimal rigidity, its relation to rigidity, and the static view
  - book: isbn:9780821838013
    title: Jack Graver, Brigitte Servatius and Herman Servatius, Combinatorial Rigidity, Graduate Studies in Mathematics 2, American Mathematical Society, 1993
    locator: Chapter 2, Infinitesimal Rigidity (generic and regular frameworks)
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, CRC Press, 2018
    locator: the chapter on generic rigidity and the regular points of the edge function
---

## Statement

Let $G = (V, E)$ be a graph with $n$ vertices, let $d \ge 1$ and $D = d(d + 1)/2$. For a placement $q \in \mathbb{R}^{dn}$ let $R(G, q)$ be the [rigidity matrix](/rigidity-matrix/) and let
$$ r_d(G) = \max_{q \in \mathbb{R}^{dn}} \operatorname{rank} R(G, q). $$
A placement $p$ is a *regular point* of $G$ if $\operatorname{rank} R(G, p) = r_d(G)$. Rigid means rigid as a [bar-and-joint framework](/bar-and-joint-framework/): every continuous motion that keeps the bar lengths is a rigid motion of the whole space.

**Theorem (Asimow and Roth 1978).** Let $p$ be a regular point of $G$, and let the points $p_1, \ldots, p_n$ affinely span $\mathbb{R}^d$. Then the framework $(G, p)$ is rigid in $\mathbb{R}^d$ if and only if
$$ \operatorname{rank} R(G, p) = dn - D, $$
that is, if and only if $(G, p)$ is [infinitesimally rigid](/infinitesimal-rigidity/). Moreover, at such a point every infinitesimal motion is the velocity of a smooth motion that keeps the bar lengths.

The proof uses only that the rank of $R(G, \cdot)$ is constant on a neighborhood of $p$. Every generic placement, with coordinates algebraically independent over $\mathbb{Q}$, is regular, and for $n \ge d + 1$ it spans $\mathbb{R}^d$. So the theorem covers the generic case of [generic rigidity](/generic-rigidity/).

## In plain words

A framework of bars and pins can resist all motion in two ways. It can resist even the first small push, or it can move a little to first order and then lock. The second kind of rigidity is a property of special shapes, such as three pins on one line. The theorem says that this second kind never happens at a shape in general position. There, a framework is rigid exactly when it resists every first small push, and that is a test on one matrix. The theorem also says that at such a shape every direction that looks free to first order is a real way to move the framework.

## Proof

Write $f = f_G$ for the edge function $q \mapsto (\lVert q_i - q_j \rVert^2)_{ij \in E}$, so that $df(q) = 2 R(G, q)$. Let $r = r_d(G)$.

**Step 1: the rank is constant near $p$.** An $r \times r$ minor of $R(G, p)$ is nonzero, and minors are continuous in $q$, so the rank is at least $r$ on a neighborhood of $p$. It is at most $r$ everywhere by the definition of $r$. So it equals $r$ on an open set $U \ni p$.

**Step 2: the fiber is a manifold.** By the constant rank theorem, there is an open $U' \subseteq U$ containing $p$ such that
$$ X = f^{-1}(f(p)) \cap U' $$
is a smooth embedded submanifold of dimension $dn - r$, and its tangent space at $p$ is $\ker df(p) = \ker R(G, p)$. We may take $U'$ so small that $X$ is connected, since in suitable coordinates $X$ is a piece of a linear subspace.

**Step 3: the orbit is a manifold.** Let $\mathrm{E}(d)$ be the group of isometries of $\mathbb{R}^d$, a Lie group of dimension $D$, and let $O = \{ (g p_1, \ldots, g p_n) : g \in \mathrm{E}(d) \}$ be the set of placements congruent to $p$. An isometry that fixes $d + 1$ affinely independent points is the identity, and the points of $p$ span $\mathbb{R}^d$, so the map $g \mapsto g p$ is injective. Its derivative at the identity sends an element $(A, b)$ of the Lie algebra, with $A$ skew, to the trivial motion $(A p_i + b)_i$, and this linear map is injective for the same reason, so the orbit map is an injective immersion. It is also proper: if $g_k p$ stays bounded, the translation parts of $g_k$ stay bounded, and the orthogonal parts lie in a compact group. So $O$ is a closed embedded submanifold of dimension $D$. Its tangent space at $p$ is the space $T(p)$ of trivial motions. Every congruent placement is equivalent, so $O \subseteq f^{-1}(f(p))$ and $O \cap U' \subseteq X$.

**Step 4: if the rank is $dn - D$, the framework is rigid.** Then $\dim X = D = \dim O$. The set $O \cap U'$ is a $D$-manifold inside the $D$-manifold $X$, so by invariance of domain it is open in $X$. It is also closed in $X$ because $O$ is closed. $X$ is connected and contains $p$, so $X = O \cap U'$. So every placement in $U'$ that is equivalent to $p$ is congruent to $p$. This is local uniqueness, and by the theorem of Asimow and Roth on the [framework page](/bar-and-joint-framework/), local uniqueness is the same as rigidity. (This direction does not need regularity: if the rank is $dn - D$, it is the largest possible rank by the bound $\operatorname{rank} R \le dn - D$ for spanning placements, so $p$ is regular automatically.)

**Step 5: if the rank is below $dn - D$, the framework is flexible.** Then $\dim X = dn - r > D = \dim O$. A submanifold of smaller dimension has empty interior, so $O \cap U'$ does not contain any open subset of $X$. Take a sequence of balls around $p$ shrinking to $p$. Each one meets $X$ in a nonempty open subset of $X$, which therefore contains a point of $X$ that is not in $O$. So there are placements equivalent to $p$ and not congruent to it, arbitrarily close to $p$. Local uniqueness fails, so $(G, p)$ is not rigid. A continuous motion is also explicit: $X$ is a connected manifold, so a smooth path in $X$ joins $p$ to a point $q \in X \setminus O$. Along it every bar keeps its length, and it ends at a placement that is not congruent to $p$, so the path is a non-trivial motion.

**Step 6: infinitesimal motions are real.** Let $u \in \ker R(G, p)$. This is the tangent space of $X$ at $p$, so there is a smooth path $q(t)$ in $X$ with $q(0) = p$ and $q'(0) = u$. It keeps every bar length. $\square$

The two directions together show that at a regular spanning point, rigid and infinitesimally rigid are the same, because infinitesimal rigidity means $\ker R(G, p) = T(p)$, which has dimension $D$, that is, rank $dn - D$.

## Consequences

- **Rigidity at regular points depends only on the graph.** The regular points are the placements where some $r \times r$ minor is nonzero, and some such minor is a nonzero polynomial. So they form an open dense set of full measure. At all of them the answer is the same: rigid if $r_d(G) = dn - D$ and flexible otherwise (for $n \ge d + 1$, at the spanning ones). This is why generic rigidity is a property of $G$ alone.
- **One infinitesimally rigid placement is enough.** If $(G, q)$ is infinitesimally rigid for a single $q$, then $r_d(G) \ge dn - D$, so $r_d(G) = dn - D$ and $G$ is generically rigid. The [witness configuration method](/witness-configuration-method/) uses this: the rank at one random placement is a lower bound on $r_d(G)$, and it is equal to $r_d(G)$ with high probability by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/).
- **Rigidity at one placement is not enough.** A rigid framework at a placement that is not regular says nothing about the graph. The 4-cycle at $0, 1, 2, 3$ on a line, with the closing bar of length 3, is rigid in the plane, but the 4-cycle is not generically rigid.
- **Counting needs regular points.** [Maxwell's rule](/maxwell-counting-rule/) and [Laman's theorem](/laman-theorem/) speak about $r_d(G)$. By the theorem, they predict the behavior of every regular framework, and of no other.
- **Flexes from linear algebra.** At a regular point, the motions of the framework near $p$ form a manifold whose dimension is the nullity of $R(G, p)$. A CAD solver that sees a kernel vector beyond the trivial motions at a regular point knows that the sketch is under-constrained, and the kernel vector is a direction in which the sketch can really move.
- **Local, not global.** The theorem is about motions near $p$. It says nothing about other placements with the same bar lengths far away. That is the question of [global rigidity](/global-rigidity/), which needs the stresses of the [stress matrix](/equilibrium-stress-matrix/).

## Tightness

The exact ranks below are over the rationals.

- **Regularity is needed for the forward direction.** The triangle at $(0, 0)$, $(1, 0)$, $(3, 0)$ is rigid in the plane, but its rigidity matrix has rank 2, below $2 \cdot 3 - 3 = 3$. The placement is not regular, since a triangle in general position has rank 3. The 4-cycle at $0, 1, 2, 3$ on a line is rigid with rank 3, below the generic rank 4 of the 4-cycle and below the target 5.
- **The span is needed.** The triangle in $\mathbb{R}^4$ is complete, so it is rigid at every placement, and its rank at three points not on a line is 3, the largest possible. But $dn - D = 12 - 10 = 2$. With fewer than $d + 1$ vertices the trivial motions have dimension below $D$, and the right count for a complete graph on $n \le d$ affinely independent points is $n(n - 1)/2$.
- **Regular does not mean generic.** The unit square with its 4 sides has rank 4, the generic rank of the 4-cycle, so it is a regular point. The theorem applies and predicts the shear that turns the square into a rhombus. Regular points can have rational or symmetric coordinates.
- **Local only.** A planar 4-cycle with one diagonal at a generic placement is rigid, but the triangle on one side of the diagonal can be reflected across it, which gives an equivalent placement that is not congruent. So the theorem cannot be strengthened to uniqueness of the placement.
- **Distance constraints only.** The proof uses that the constraint map is invariant under all isometries and that its orbit has dimension $D$. For constraint systems with angles or incidences the same argument works with the right group, but the counts change.

## History

James Clerk Maxwell counted bars and joints in 1864, and Laman in 1970 characterized the plane case by counts, both in the language of generic or general position. Herman Gluck used the idea of a generic placement in 1975 to show that almost all triangulated spheres are rigid in space. L. Asimow and B. Roth gave the first general treatment in 1978. They defined rigidity by continuous motions and by local uniqueness, proved the two the same, introduced the regular points of the edge function, and proved the theorem above, so that rigidity at a regular or generic point is a property of the graph and a rank test. Their second paper (1979) developed infinitesimal rigidity and the statics of loads and stresses. Graver, Servatius and Servatius made the theorem the starting point of combinatorial rigidity in their 1993 book.

## References
