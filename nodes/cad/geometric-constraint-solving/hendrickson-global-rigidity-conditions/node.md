---
tag: FVG8C4
kind: theorem
slug: hendrickson-global-rigidity-conditions
name: Hendrickson's necessary conditions for global rigidity
aliases:
- Hendrickson's theorem
area: cad/geometric-constraint-solving
level: advanced
summary: A globally rigid generic framework in d dimensions with at least d + 2 vertices has a (d + 1)-connected graph, and the graph stays rigid when any one edge is removed.
prereqs: [global-rigidity, rigidity-matrix, vertex-connectivity]
see_also: [jackson-jordan-theorem, connelly-global-rigidity-theorem, gortler-healy-thurston-theorem, double-banana-graph, equilibrium-stress-matrix, asimow-roth-theorem, k-vertex-connected-graph, distance-geometry-problem]
sources:
  - paper: doi:10.1137/0221008
    title: Bruce Hendrickson, Conditions for unique graph realizations, SIAM Journal on Computing 21(1), 65 to 84, 1992
    locator: the two necessary conditions, (d + 1)-connectivity and redundant rigidity, their proofs by reflection and by a closed curve of flexes, and the conjecture that they are sufficient
  - paper: "R. Connelly, On generic global rigidity, in Applied Geometry and Discrete Mathematics (The Victor Klee Festschrift), DIMACS Series in Discrete Mathematics and Theoretical Computer Science 4, American Mathematical Society, 147 to 155, 1991"
    locator: the complete bipartite graph K(5,5) as a counterexample to sufficiency in three dimensions
  - paper: doi:10.1016/j.jctb.2004.11.002
    title: Bill Jackson and Tibor Jordán, Connected rigidity matroids and unique realizations of graphs, Journal of Combinatorial Theory, Series B 94(1), 1 to 29, 2005
    locator: the proof that the two conditions are sufficient in the plane
  - paper: doi:10.1353/ajm.0.0132
    title: Steven J. Gortler, Alexander D. Healy and Dylan P. Thurston, Characterizing generic global rigidity, American Journal of Mathematics 132(4), 897 to 939, 2010
    locator: the algebraic lemma that the bar lengths of a generic framework form a regular value, used for the redundant rigidity proof
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, CRC Press, 2018
    locator: the chapter on global rigidity (Hendrickson's conditions and the counterexamples in space)
---

## Statement

Let $G = (V, E)$ be a graph with $n$ vertices, let $d \ge 1$, and let $D = d(d + 1)/2$. A framework $(G, p)$ in $\mathbb{R}^d$ is *globally rigid* if every framework $(G, q)$ in $\mathbb{R}^d$ with the same bar lengths is congruent to it. $G$ is *redundantly rigid* in $\mathbb{R}^d$ if $G - e$ is generically rigid in $\mathbb{R}^d$ for every edge $e$. A placement is *generic* if its $dn$ coordinates are algebraically independent over $\mathbb{Q}$. $G$ is *$k$-connected* if it has more than $k$ vertices and no set of fewer than $k$ vertices separates it, as on the [k-vertex-connected graph](/k-vertex-connected-graph/) page.

**Theorem (Hendrickson 1992).** Let $n \ge d + 2$ and let $p$ be a generic placement in $\mathbb{R}^d$. If $(G, p)$ is globally rigid, then

1. $G$ is $(d + 1)$-connected, and
2. $G$ is redundantly rigid in $\mathbb{R}^d$.

Both proofs build an explicit framework $(G, q)$ with the same bar lengths that is not congruent to $(G, p)$. For a small separating set, $q$ reflects one side. For an edge $e$ that is not redundant, $q$ comes from flexing $G - e$ along a closed curve of shapes until $e$ has its old length again.

## In plain words

Take a framework of bars and pins whose shape is in general position. If its bar lengths fix its shape completely, with at least $d + 2$ pins in $d$ dimensions, then two things must be true of its graph. First, no small group of pins, at most as many as the dimension, can cut the graph in two, because one side could then be mirrored through a flat that holds the cut pins. Second, every bar must be spare in the sense that the framework stays rigid without it. If some bar is not spare, take it out, let the framework move, and follow the motion until the bar would fit again in a new shape.

## Proof

Write $f_H(q) = (\lVert q_i - q_j \rVert^2)_{ij \in E(H)}$ for the edge function of a graph $H$ on $V$, and $R(H, q)$ for its [rigidity matrix](/rigidity-matrix/). A framework with the same bar lengths as $(G, p)$ is called *equivalent*. Throughout, $(G, p)$ is generic and globally rigid with $n \ge d + 2$.

**Part 1: connectivity.** Suppose that $G$ is not $(d + 1)$-connected. Since $n \ge d + 2$, this means that $G$ is not complete and some set $S$ with $|S| \le d$ separates it: $V \setminus S = A \cup B$ with $A$ and $B$ nonempty and no edge between $A$ and $B$. ($S$ may be empty if $G$ is disconnected.)

The points $p_s$, $s \in S$, are at most $d$ generic points, so they are affinely independent and lie on some hyperplane $W$. If $|S| = d$ the hyperplane is unique, and no other point $p_x$ lies on it, because $d + 1$ generic points are affinely independent. If $|S| < d$ the hyperplanes through $p(S)$ form a family of positive dimension, and we choose one that avoids the finitely many other points. Let $\sigma$ be the reflection in $W$ and set
$$ q_x = \sigma(p_x) \text{ for } x \in B, \qquad q_x = p_x \text{ for } x \in A \cup S. $$
Every edge has both ends in $A \cup S$ or both ends in $B \cup S$. On $A \cup S$ the map $p \mapsto q$ is the identity, and on $B \cup S$ it is $\sigma$, because $\sigma$ fixes $p(S) \subset W$. Both are isometries, so every bar keeps its length. Now take $a \in A$ and $b \in B$. The points at equal distance from $p_b$ and $\sigma(p_b) \ne p_b$ form the hyperplane $W$, and $p_a \notin W$, so $\lVert q_a - q_b \rVert = \lVert p_a - \sigma(p_b) \rVert \ne \lVert p_a - p_b \rVert$. So $(G, q)$ is equivalent to $(G, p)$ and not congruent to it, which contradicts global rigidity. $\square$

**Part 2: redundant rigidity.** Global rigidity implies rigidity, so by the [Asimow and Roth theorem](/asimow-roth-theorem/) $\operatorname{rank} R(G, p) = dn - D$ and $\ker R(G, p)$ is the space $T(p)$ of trivial motions. Suppose some edge $e = uv$ is not redundant, so $G - e$ is not generically rigid. Removing one row lowers the rank by at most one, so $H = G - e$ has generic rank $r = dn - D - 1$. By Part 1, $G$ is $(d + 1)$-connected, hence 2-connected, so $H$ is connected.

*Step 1: the bar lengths form a regular value.* Let $Z = \{ q : \operatorname{rank} R(H, q) < r \}$. It is the common zero set of the $r \times r$ minors, an algebraic set defined over $\mathbb{Q}$. On each smooth piece of $Z$ the map $f_H$ has rank below $r$, so $f_H(Z)$ has dimension below $r$ (the semialgebraic form of Sard's theorem). The closure $X$ of the image $f_H(\mathbb{R}^{dn})$ in the Zariski topology is an irreducible variety of dimension $r$ defined over $\mathbb{Q}$, so there is a polynomial $g$ with rational coefficients that vanishes on $f_H(Z)$ and not on $X$. Then $g \circ f_H$ is a nonzero polynomial with rational coefficients, so it does not vanish at the generic point $p$. So $f_H(p) \notin f_H(Z)$: every placement $q$ equivalent to $(H, p)$ has $\operatorname{rank} R(H, q) = r$. This is the lemma that Gortler, Healy and Thurston state in general.

*Step 2: the fiber is a manifold of dimension $D + 1$.* The rank of $R(H, \cdot)$ is $r$ on the open set $\mathbb{R}^{dn} \setminus Z$, which contains $M = f_H^{-1}(f_H(p))$. By the constant rank theorem, $M$ is a closed smooth submanifold of $\mathbb{R}^{dn}$ of dimension $dn - r = D + 1$, and its tangent space at $p$ is $\ker R(H, p)$.

*Step 3: no point of $M$ is flat.* Let $q \in M$ and suppose its points lie in a hyperplane. Then every row of $R(H, q)$ has its blocks in the $(d - 1)$-dimensional direction space of the hyperplane, so $\operatorname{rank} R(H, q)$ is at most the largest rank of a complete graph on $n$ vertices in $\mathbb{R}^{d - 1}$, which is $(d - 1) n - d(d - 1)/2$ for $n \ge d$. But
$$ r - \Big( (d - 1) n - \tfrac{d (d - 1)}{2} \Big) = n - d - 1 \ge 1 $$
because $n \ge d + 2$. This contradicts $\operatorname{rank} R(H, q) = r$. So every $q \in M$ affinely spans $\mathbb{R}^d$. This is the only place where $n \ge d + 2$ is used in Part 2.

*Step 4: the shapes form circles.* The isometry group $\mathrm{E}(d)$, of dimension $D$, acts on $M$. An isometry that fixes a spanning set of points is the identity, so by Step 3 the action is free. It is also proper, so $\mathcal{C} = M / \mathrm{E}(d)$ is a smooth manifold of dimension $(D + 1) - D = 1$ without boundary. It is compact: every class has a representative with centroid $0$, and since $H$ is connected, every distance $\lVert q_i - q_j \rVert$ is at most the sum of the bar lengths along a path, so these representatives form a closed and bounded set that maps onto $\mathcal{C}$. A compact 1-manifold without boundary is a finite union of circles. Let $C$ be the circle that holds the class $[p]$.

*Step 5: the length of $e$ is not stationary at $p$.* The function $h(q) = \lVert q_u - q_v \rVert^2$ is invariant under isometries, so it is a smooth function on $C$. The tangent line of $C$ at $[p]$ is $\ker R(H, p) / T(p)$, which has dimension $(D + 1) - D = 1$. Let $w \in \ker R(H, p)$ be a vector outside $T(p)$. The derivative of $h$ along $w$ is $2 (p_u - p_v) \cdot (w_u - w_v)$, which is twice the row of $e$ applied to $w$. If it were zero, $w$ would lie in $\ker R(G, p) = T(p)$. So the derivative is nonzero, and $h - h(p)$ changes sign at $[p]$ along $C$.

*Step 6: a second shape.* Walk around the circle $C$ from a point just after $[p]$, where $h - h(p)$ has one sign, to a point just before $[p]$, where it has the other sign, without passing $[p]$. By the intermediate value theorem $h$ takes the value $h(p)$ at some class $[q] \ne [p]$. Then $q \in M$ keeps the lengths of all edges of $H$, and $h(q) = h(p)$ keeps the length of $e$. So $(G, q)$ is equivalent to $(G, p)$, and since $[q] \ne [p]$ in the quotient by all isometries, it is not congruent to $(G, p)$. This contradicts global rigidity. $\square$

## Consequences

- **Edge and degree bounds.** A generically globally rigid graph with $n \ge d + 2$ has at least $dn - D + 1$ edges, since removing one edge must leave a generically rigid graph, which needs $dn - D$. Every vertex has degree at least $d + 1$ by Part 1.
- **The plane.** Jackson and Jordán (2005) proved the converse for $d = 2$: a graph with $n \ge 4$ is generically globally rigid in the plane if and only if it is 3-connected and redundantly rigid. See the [Jackson and Jordán theorem](/jackson-jordan-theorem/). Both conditions are tested in polynomial time, the first with flows and [Menger's theorem](/menger-theorem/), the second with the [pebble game](/pebble-game-rigidity/).
- **The line.** For $d = 1$ the theorem says that a generically globally rigid graph with $n \ge 3$ is 2-connected. The converse also holds, so on the line generic global rigidity is 2-connectivity.
- **A test that fails fast.** Before a costly computation such as a stress matrix rank, a solver can check both conditions. If either fails, the generic system has a second solution, and Part 1 even builds it by a reflection. This is the reason why a CAD sketch with a cut pair of points in the plane has a mirror solution.
- **A certificate of non-uniqueness.** The proof of Part 2 explains the many solutions of a minimally rigid system. Each bar that is not redundant gives at least one more solution, reached by flexing the rest and closing the bar again.

## Tightness

- **The bound $n \ge d + 2$ is needed.** $K_{d + 1}$ is globally rigid at every placement in $\mathbb{R}^d$, but it has $D$ edges and $K_{d + 1} - e$ is not rigid, and $K_{d + 1}$ is only $d$-connected. In the proof of Part 2 the shape space of $K_{d + 1} - e$ is an interval, not a circle: in the plane, the path $u, x, v$ has the angle at $x$ as its only shape parameter, the length of $uv$ is monotone in it, and each length is reached once.
- **A worked case of Part 2.** The triangular prism in the plane, with triangles $123$ and $456$ and rungs $14$, $25$, $36$, is 3-connected and minimally rigid. At $p_1 = (0, 0)$, $p_2 = (4, 0)$, $p_3 = (2, -3)$, $p_4 = (1, 3)$, $p_5 = (5, 4)$, $p_6 = (3, 6)$ its rigidity matrix has rank 9. Remove the rung $36$: what is left is a four-bar linkage, with the triangle $456$ carried by the bars $14$ and $25$. Following its motion until $\lVert q_3 - q_6 \rVert = \sqrt{82}$ again gives $q_4 = (-1, 3)$, $q_5 = (3, 4)$, $q_6 = (1, 6)$, with the other points fixed. All 9 bar lengths are equal (for example $\lVert q_2 - q_5 \rVert = \sqrt{17} = \lVert p_2 - p_5 \rVert$), the rank is still 9, and $\lVert q_1 - q_5 \rVert = 5$ while $\lVert p_1 - p_5 \rVert = \sqrt{41}$. So the two frameworks are not congruent.
- **A worked case of Part 1.** On the line, two triangles that share the vertex $c$, at $a = 0$, $b = 3$, $c = 7$, $d = 8$, $e = 12$, form a 2-edge-connected graph, so it is redundantly rigid on the line, but $c$ alone separates it. Reflect $d$ and $e$ in the point $7$ to get $6$ and $2$. All six bar lengths stay, and the distance from $a$ to $d$ changes from 8 to 6.
- **The conditions are not sufficient in space.** The complete bipartite graph $K_{5,5}$ is 5-connected. At random integer placements in $\mathbb{R}^3$ its rigidity matrix has rank $24 = 3 \cdot 10 - 6$, and the rank stays 24 after the removal of any one of its 25 edges, so it is redundantly rigid. Connelly (1991) showed that it is still not generically globally rigid in $\mathbb{R}^3$. In the language of the [stress matrix](/equilibrium-stress-matrix/), its stress space at a generic placement has dimension 1, and the stress matrix has rank 2, below the rank $10 - 3 - 1 = 6$ that the theorem of [Gortler, Healy and Thurston](/gortler-healy-thurston-theorem/) requires. Connelly gave the family of complete bipartite graphs $K_{a,b}$ with $a + b = (d + 1)(d + 2)/2$ and $a, b \ge d + 2$ for every $d \ge 3$, and Frank and Jiang later found more families.
- **The double banana is not the counterexample.** The [double banana](/double-banana-graph/) is sometimes named as the graph that shows the conditions are not sufficient in space. It does not. It is only 2-connected, since the two hinge vertices separate it, and it is not even generically rigid, with generic rank 17 for 18 edges. It fails both conditions. It is the counterexample to the $3k - 6$ count for generic rigidity, not to Hendrickson's conditions.

## History

Bruce Hendrickson proved both conditions in 1992, in a paper on the computation of molecular structure from distance measurements, where unique realization is the question. He conjectured that the two conditions are also sufficient. Connelly showed in 1991 that $K_{5,5}$ breaks this in three dimensions, using the stress matrix that he had developed for tensegrity frameworks. In the plane the conjecture holds: Jackson and Jordán proved it in 2005, with Connelly's sufficient stress condition from the same year. In dimension 3 and higher no combinatorial characterization of generic global rigidity is known, although Gortler, Healy and Thurston (2010) proved that the stress matrix condition is exact.

## References
