---
tag: CG98HE
kind: definition
slug: bar-and-joint-framework
name: Bar-and-joint framework
aliases:
- bar framework
area: cad/geometric-constraint-solving
level: core
summary: A graph with a position for each vertex, read as rigid bars joined at pins. It is rigid when every continuous motion that keeps bar lengths is a rigid motion.
prereqs: [graph, special-euclidean-group]
see_also: [infinitesimal-rigidity, generic-rigidity, global-rigidity, maxwell-counting-rule, laman-theorem, well-constrained-system, grubler-formula, distance-based-formation-control]
sources:
  - book: isbn:9780821838013
    title: Jack Graver, Brigitte Servatius and Herman Servatius, Combinatorial Rigidity, Graduate Studies in Mathematics 2, American Mathematical Society, 1993
    locator: the opening chapters on frameworks, motions and rigidity, and Chapter 2, Infinitesimal Rigidity (general locator)
  - paper: doi:10.1090/S0002-9947-1978-0511410-9
    title: L. Asimow and B. Roth, The rigidity of graphs, Transactions of the American Mathematical Society 245, 279 to 289, 1978
    locator: the definitions of a framework, of rigidity by continuous paths and by local uniqueness, and the proof that the two agree
  - paper: doi:10.1080/14786446408643668
    title: J. Clerk Maxwell, On the calculation of the equilibrium and stiffness of frames, Philosophical Magazine, Series 4, 27(182), 294 to 299, 1864
    locator: the frames of points joined by bars, and the count of bars needed for a stiff frame
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, Chapman and Hall/CRC, 2018
    locator: the chapter Planar Rigidity (general locator)
---

A bar-and-joint framework is a [graph](/graph/) together with a point for each vertex. Each vertex is a joint, a pin that turns freely, and each edge is a rigid bar whose length is the distance between its two points. The framework is rigid when the only continuous motions that keep all bar lengths are the motions of the whole space, and flexible otherwise. Frameworks model trusses in structural engineering, distance constraints between points in CAD, and robot formations and sensor networks that measure distances between pairs.

## Definition

**Framework.** Let $G = (V, E)$ be a finite [simple graph](/simple-graph/) with $V = \{1, \ldots, n\}$, and let $d \ge 1$. A *framework* in $\mathbb{R}^d$ is a pair $(G, p)$, where $p = (p_1, \ldots, p_n)$ is a list of points $p_i \in \mathbb{R}^d$, the *placement* or configuration. Two points may coincide. The *length* of the bar $ij \in E$ is $\lVert p_i - p_j \rVert$. It is convenient to see $p$ as one vector in $\mathbb{R}^{dn}$ and to use the *edge function*
$$ f_G : \mathbb{R}^{dn} \to \mathbb{R}^{E}, \qquad f_G(q) = \big( \lVert q_i - q_j \rVert^2 \big)_{ij \in E}. $$

**Equivalent and congruent.** A second framework $(G, q)$ is *equivalent* to $(G, p)$ if $f_G(q) = f_G(p)$, that is, every bar has the same length. It is *congruent* to $(G, p)$ if $\lVert q_i - q_j \rVert = \lVert p_i - p_j \rVert$ for all pairs $i, j \in V$, edges or not. Two point lists are congruent exactly when an isometry of $\mathbb{R}^d$ (a rotation, a reflection, a translation, or a composition of them) maps $p_i$ to $q_i$ for every $i$. Congruent implies equivalent. The converse fails in general, and the converse is exactly what rigidity asks for, locally or globally.

**Motion.** A *continuous motion* (or *flex*) of $(G, p)$ is a continuous path $t \mapsto p(t)$, $t \in [0, 1]$, with $p(0) = p$ and $f_G(p(t)) = f_G(p)$ for all $t$. It is *trivial* if every $p(t)$ is congruent to $p$. A path $p(t) = A(t) p + b(t)$ with $A(t)$ a rotation and $b(t)$ a translation, applied to all points at once, is trivial. These are the rigid motions, the elements of the [special Euclidean group](/special-euclidean-group/).

**Rigid.** The framework $(G, p)$ is *rigid* in $\mathbb{R}^d$ if every continuous motion of it is trivial. It is *flexible* otherwise.

**Local uniqueness.** $(G, p)$ is rigid if and only if there is an $\varepsilon > 0$ such that every framework $(G, q)$ equivalent to $(G, p)$ with $\lVert q - p \rVert < \varepsilon$ is congruent to $(G, p)$. Asimow and Roth (1978) proved this. The direction from local uniqueness to rigidity is short. Let $p(t)$ be a motion and let $S$ be the set of $t$ with $p(t)$ congruent to $p$. $S$ is closed, because congruence is a closed condition, and it contains 0. $S$ is open: if $p(t_0)$ is congruent to $p$, then $p(t_0)$ is also locally unique, because it is an isometric copy of $p$, and $p(t)$ for $t$ near $t_0$ is close to $p(t_0)$ and equivalent to it. Since $[0, 1]$ is connected, $S = [0, 1]$. The other direction needs the curve selection lemma for real algebraic sets, since the set of equivalent placements is cut out by polynomial equations.

The definition depends on $d$. A framework in the plane can also be read as a framework in $\mathbb{R}^3$, and it can be rigid in the plane and flexible in space.

## Examples and non-examples

- **Triangle.** $K_3$ at three points that are not on a line is rigid in the plane, and it is even globally rigid: the three side lengths fix the triangle up to congruence (SSS). The degenerate triangle with points $0$, $1$, $3$ on a line and lengths $1$, $2$, $3$ is also rigid, because $\lVert p_1 - p_3 \rVert = \lVert p_1 - p_2 \rVert + \lVert p_2 - p_3 \rVert$ forces the three points onto a line in that order.
- **Square.** The 4-cycle $a b c d$ at the corners of a unit square is flexible. The motion $p_a = (0, 0)$, $p_b = (1, 0)$, $p_c = (1 + \cos\theta, \sin\theta)$, $p_d = (\cos\theta, \sin\theta)$, for $\theta$ from $90°$ down to $60°$, keeps all four lengths equal to 1 and turns the square into a rhombus, so the distance from $a$ to $c$ changes. Adding the diagonal $ac$ makes the framework rigid: it becomes two triangles that share the bar $ac$.
- **Rigid with too few bars.** Put $a, b, c, d$ at $0, 1, 2, 3$ on a line, with bars $ab$, $bc$, $cd$ of length 1 and $da$ of length 3. Then $\lVert p_a - p_d \rVert = 3 = \lVert p_a - p_b \rVert + \lVert p_b - p_c \rVert + \lVert p_c - p_d \rVert$, and equality in the triangle inequality forces every equivalent framework onto a line in this order. So the framework is rigid in the plane, and even globally rigid, with 4 bars, although a rigid framework in general position needs $2n - 3 = 5$ (see [Maxwell's counting rule](/maxwell-counting-rule/)). Its rigidity matrix has rank 3, so it is not [infinitesimally rigid](/infinitesimal-rigidity/).
- **Dimension matters.** Two triangles $abc$ and $abd$ that share the bar $ab$ (the graph $K_4$ minus the edge $cd$) form a rigid framework in the plane. Read in $\mathbb{R}^3$, the triangle $abd$ can turn about the line through $p_a$ and $p_b$ like a hinge, so the same framework is flexible in space. The [complete graph](/complete-graph/) $K_4$ on four points that are not on one plane is rigid in $\mathbb{R}^3$.
- **Complete graphs.** $(K_n, p)$ is rigid in every dimension for every placement, because all pairwise distances are bars, so every equivalent framework is congruent.
- **Flexible by a rigid part.** A rigid framework with an extra vertex joined by one bar is flexible: the new point turns on a circle around its neighbor.
- **Not a framework model.** A linkage where a bar can slide through a joint, or a constraint on the angle between two bars, is not a bar-and-joint framework. Angles and incidences between lines are handled by the more general [geometric constraint graphs](/geometric-constraint-graph/), and rigid bodies joined by bars by the body-and-bar model of [Tay's theorem](/tay-theorem/).

## Related definitions

- **[Infinitesimal rigidity](/infinitesimal-rigidity/).** The linearized version: the rigidity matrix, which is half the Jacobian of $f_G$, has the largest rank allowed by the trivial motions. It implies rigidity and is easy to test.
- **[Generic rigidity](/generic-rigidity/).** For almost every placement, rigidity depends only on the graph. In the plane, [Laman's theorem](/laman-theorem/) gives the graphs, and the [pebble game](/pebble-game-rigidity/) tests them.
- **[Global rigidity](/global-rigidity/).** Every equivalent framework, near or far, is congruent. It is stronger than rigidity: $K_4$ minus an edge in the plane is rigid but can be folded across its shared bar.
- **[Well-constrained system](/well-constrained-system/).** The CAD view: a system of distance constraints with finitely many solutions up to rigid motion. A rigid framework gives a locally unique solution.
- **Mechanism mobility.** The [Grübler formula](/grubler-formula/) counts the degrees of freedom of a linkage of rigid links, much as [Maxwell's counting rule](/maxwell-counting-rule/) counts those of a framework, and it has the same failure at special positions.
- **Formations.** In [distance-based formation control](/distance-based-formation-control/), robots are joints and the controlled distances are bars, so the formation keeps its shape exactly when the framework is rigid.

## References
