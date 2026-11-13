---
tag: BQRK68
kind: theorem
slug: tay-theorem
name: Tay's theorem
aliases:
- body-and-bar rigidity theorem
area: cad/geometric-constraint-solving
level: advanced
summary: A body-and-bar framework in d dimensions is generically rigid if and only if its multigraph has D edge-disjoint spanning trees, with D = d(d + 1)/2.
prereqs: [infinitesimal-rigidity, generic-rigidity, nash-williams-tutte-theorem]
see_also: [laman-theorem, spanning-tree-packing, nash-williams-arboricity-theorem, graphic-matroid, pebble-game-rigidity, parallel-manipulator, assembly-constraint-solving, maxwell-counting-rule]
sources:
  - paper: doi:10.1016/0095-8956(84)90016-9
    title: Tiong-Seng Tay, Rigidity of multigraphs. I. Linking rigid bodies in n-space, Journal of Combinatorial Theory, Series B 36(1), 95 to 112, 1984
    locator: the main theorem, generic rigidity of body-and-bar frameworks in every dimension by edge-disjoint spanning trees
  - paper: doi:10.1137/0401025
    title: Walter Whiteley, The union of matroids and the rigidity of frameworks, SIAM Journal on Discrete Mathematics 1(2), 237 to 255, 1988
    locator: the generic body-and-bar matroid as a union of graphic matroids, and the rank formula
  - paper: doi:10.1112/jlms/s1-36.1.445
    title: C. St. J. A. Nash-Williams, Edge-disjoint spanning trees of finite graphs, Journal of the London Mathematical Society 36, 445 to 450, 1961
    locator: the partition condition for k edge-disjoint spanning trees
  - paper: doi:10.1112/jlms/s1-36.1.221
    title: W. T. Tutte, On the problem of decomposing a graph into n connected factors, Journal of the London Mathematical Society 36, 221 to 230, 1961
    locator: the partition condition for k edge-disjoint spanning trees
  - paper: doi:10.1016/j.disc.2007.07.104
    title: Audrey Lee and Ileana Streinu, Pebble game algorithms and sparse graphs, Discrete Mathematics 308(8), 1425 to 1437, 2008
    locator: the (k, l) pebble game, which for k = l = D tests the body-and-bar count
  - book: isbn:9780821838013
    title: Jack Graver, Brigitte Servatius and Herman Servatius, Combinatorial Rigidity, Graduate Studies in Mathematics 2, American Mathematical Society, 1993
    locator: Chapter 5, Rigidity in Higher Dimensions (general locator for body-and-bar frameworks)
---

Tay's theorem describes the generic rigidity of a structure of rigid bodies joined by bars, in every dimension. A body in $\mathbb{R}^d$ has $D = d(d + 1)/2$ degrees of freedom, and each bar removes at most one of them from the relative motion of the two bodies it joins. Tay (1984) proved that for bars in general position the count is also sufficient, in a sharp form: the framework is rigid exactly when its multigraph, with a vertex per body and an edge per bar, contains $D$ edge-disjoint spanning trees. This gives what bar-and-joint frameworks in space lack, a combinatorial test that a polynomial algorithm can run.

## Statement

Fix $d \ge 1$ and $D = d(d + 1)/2$. Let $T$ be the space of trivial infinitesimal motions of $\mathbb{R}^d$, the maps $S(q) = Aq + c$ with $A$ a skew-symmetric $d \times d$ matrix and $c \in \mathbb{R}^d$, so $\dim T = D$.

A *body-and-bar framework* is a multigraph $G = (V, E)$ without loops, with $n = |V| \ge 1$ vertices (the bodies) and $m$ edges (the bars), together with two points $a_e \ne b_e$ in $\mathbb{R}^d$ for each bar $e = ij$, where $a_e$ is fixed to body $i$ and $b_e$ to body $j$. An *infinitesimal motion* gives each body $i$ a motion $S_i \in T$ so that the length of every bar stays to first order:
$$ \big(S_i(a_e) - S_j(b_e)\big) \cdot (a_e - b_e) = 0 \quad \text{for every bar } e = ij. $$
The motions with all $S_i$ equal are *trivial*. The framework is *infinitesimally rigid* if every infinitesimal motion is trivial. It is *generic* if the $2dm$ coordinates of the points $a_e$, $b_e$ are algebraically independent over $\mathbb{Q}$, and $G$ is *generically rigid* as a body-and-bar framework in $\mathbb{R}^d$ if its generic frameworks are infinitesimally rigid.

**Theorem (Tay 1984).** For a multigraph $G$ with $n \ge 1$ vertices, these are equivalent:

1. $G$ is generically rigid as a body-and-bar framework in $\mathbb{R}^d$.
2. For every partition of $V$ into $r$ parts, at least $D(r - 1)$ edges of $G$ join different parts.
3. $G$ contains $D$ edge-disjoint spanning trees.

**Theorem (independent bars).** A set $F$ of bars has linearly independent rows at a generic framework if and only if every nonempty $F' \subseteq F$ satisfies $|F'| \le D(|V(F')| - 1)$, where $V(F')$ is the set of bodies that $F'$ touches, and this holds if and only if $F$ is the union of $D$ forests.

## In plain words

A rigid body in the plane can slide in two directions and turn, so it has three ways to move. Two bodies joined by three bars in general position form one rigid unit. For many bodies, count the bars that join different groups: for every way of splitting the bodies into groups, there must be enough bars between the groups to lock them together, three for each extra group in the plane and six in space. If this holds for every split, the structure is rigid, unless the bars sit in a special position, for example all passing through one point. The test is the same as asking whether the bars can be sorted into three (or six) trees, each of which reaches every body.

## Proof

Choose a basis of $T$ with integer entries, for example the matrices $E_{kl} - E_{lk}$ for $k < l$ and the unit translations. Then an infinitesimal motion is a vector in $\mathbb{R}^{Dn}$, and the conditions form a matrix $M(G; a, b)$ with one row per bar and $D$ columns per body, whose entries are polynomials in the coordinates of the points with integer coefficients.

**Lemma 1 (the bar functional).** For every $S \in T$ and every bar $e$, $S(a_e) \cdot (a_e - b_e) = S(b_e) \cdot (a_e - b_e)$. So with the linear functional $\ell_e(S) = S(a_e) \cdot (a_e - b_e)$ on $T$, the condition for the bar $e = ij$ reads $\ell_e(S_i) - \ell_e(S_j) = 0$, and the row of $e$ in $M$ is $\ell_e$ in the columns of body $i$, $-\ell_e$ in the columns of body $j$, and zero elsewhere.

*Proof.* $\big(S(a) - S(b)\big) \cdot (a - b) = \big(A(a - b)\big) \cdot (a - b) = 0$, because $A$ is skew-symmetric. Apply this to $S_j$: $S_j(b_e) \cdot (a_e - b_e) = S_j(a_e) \cdot (a_e - b_e) = \ell_e(S_j)$. $\square$

In $\mathbb{R}^3$, write $S(q) = \omega \times q + c$. Then $\ell_e(S) = \omega \cdot (a_e \times u) + c \cdot u$ with $u = a_e - b_e$, so $\ell_e$ is given by the Plücker coordinates $(u, a_e \times u)$ of the line of the bar.

**Lemma 2 (lines span the dual).** The functionals $\ell_e$, over all pairs of distinct points, span the dual space $T^*$.

*Proof.* If not, some $S \ne 0$ in $T$ has $\ell(S) = 0$ for all of them. Pick a point $a$ with $S(a) \ne 0$ and put $b = a - S(a)$. Then $\ell(S) = S(a) \cdot S(a) > 0$, a contradiction. $\square$

**Lemma 3 (rank and rigidity).** The trivial motions form a $D$-dimensional subspace of the kernel of $M$. So the framework is infinitesimally rigid if and only if $\operatorname{rank} M = D(n - 1)$. At a generic framework the rank of $M$ is the largest rank over all choices of points.

*Proof.* The first claim is Lemma 1 and the count of columns. For the second, take a square submatrix of size $r$ (the largest rank) that is nonsingular at some choice of points. Its determinant is a nonzero polynomial with integer coefficients, so it does not vanish at algebraically independent coordinates. $\square$

**Proof of the theorem on independent bars.** *Independence implies the count.* Let $F' \subseteq F$ be nonempty, with $k = |V(F')|$ bodies. The rows of $F'$ are zero outside the $Dk$ columns of those bodies. On these columns they vanish on the $D$ motions that give every body of $V(F')$ the same $S$, by Lemma 1. So these rows have rank at most $Dk - D$, and if they are independent, $|F'| \le D(k - 1)$.

*The count implies $D$ forests.* By the [Nash-Williams arboricity theorem](/nash-williams-arboricity-theorem/), a multigraph can be covered by $D$ forests if and only if every subgraph with $k \ge 1$ vertices has at most $D(k - 1)$ edges. The count is this condition.

*$D$ forests are independent.* Let $F = F_1 \cup \cdots \cup F_D$ with disjoint forests $F_k$. By Lemma 2, choose pairs of points $(a^1, b^1), \ldots, (a^D, b^D)$ whose functionals $\lambda_1, \ldots, \lambda_D$ form a basis of $T^*$. Give every bar $e = ij$ of $F_k$ the points $a_e = a^k$ on body $i$ and $b_e = b^k$ on body $j$. In the coordinates $S \mapsto (\lambda_1(S), \ldots, \lambda_D(S))$ of $T$, which is a change of basis in each block of columns, the row of such a bar is the unit vector $\epsilon_k$ in block $i$ and $-\epsilon_k$ in block $j$. Group the columns by $k$. The rows of $F_k$ use only the $n$ columns of coordinate $k$, and there they form the signed incidence matrix of the forest $F_k$. The rows of a forest's incidence matrix are independent: a forest with an edge has a leaf, the edge at the leaf is the only row with a nonzero entry in the leaf's column, so its coefficient in any vanishing combination is zero, and induction on the number of edges removes it. Different $k$ use disjoint columns, so all $|F|$ rows are independent at this framework. By Lemma 3 they are independent at every generic framework. $\square$

**Proof of Tay's theorem.** *1 implies 2.* Take a generic framework, which is infinitesimally rigid, and a partition $V = P_1 \cup \cdots \cup P_r$ with $c$ edges between different parts. Consider the motions that are constant on each part: $S_i = S^{(t)}$ for $i \in P_t$, with $S^{(1)}, \ldots, S^{(r)} \in T$ free. They form a space of dimension $Dr$. A bar inside a part gives $\ell_e(S^{(t)}) - \ell_e(S^{(t)}) = 0$, so only the $c$ crossing bars restrict these motions, and the infinitesimal motions among them form a space of dimension at least $Dr - c$. All of these must be trivial, a space of dimension $D$, so $Dr - c \le D$, which is $c \ge D(r - 1)$.

*2 implies 3.* This is the [Nash-Williams and Tutte theorem](/nash-williams-tutte-theorem/): a multigraph contains $D$ edge-disjoint spanning trees if and only if every partition into $r$ parts has at least $D(r - 1)$ crossing edges.

*3 implies 1.* The union of $D$ edge-disjoint spanning trees is a union of $D$ forests with $D(n - 1)$ edges. By the theorem on independent bars, its rows are independent at every generic framework, so $\operatorname{rank} M \ge D(n - 1)$, and by Lemma 3 the framework is infinitesimally rigid. $\square$

## Consequences

- **The generic body-and-bar matroid.** The independent sets of bars are the unions of $D$ forests, so the generic body-and-bar matroid is the union of $D$ copies of the [graphic matroid](/graphic-matroid/), as Whiteley (1988) put it. Its rank on $E$ is the size of the largest union of $D$ forests in $G$, which the matroid union formula gives as $\min_{F \subseteq E} \big(|E \setminus F| + D\, r(F)\big)$, with $r(F)$ the rank of $F$ in the graphic matroid.
- **A polynomial test in every dimension.** Packing $D$ spanning trees is a matroid problem with polynomial algorithms ([spanning tree packing](/spanning-tree-packing/)), and the $(D, D)$ [pebble game](/pebble-game-rigidity/) of Lee and Streinu tests the count of the theorem on independent bars, with $D$ pebbles per body. This contrasts with bar-and-joint frameworks in $\mathbb{R}^3$, for which no such test is known.
- **The Maxwell count for bodies.** A minimally rigid body-and-bar framework has exactly $D(n - 1)$ bars, so in the plane $3n - 3$ and in space $6n - 6$. This is the body version of [Maxwell's rule](/maxwell-counting-rule/), and here, unlike for joints in space, the subset counts are also sufficient.
- **Parallel platforms.** A Gough-Stewart [parallel manipulator](/parallel-manipulator/) is two bodies, the base and the platform, joined by six legs. By the proof, it is infinitesimally rigid when the legs are locked exactly when the six rows $\ell_e$, the Plücker vectors of the leg lines, are linearly independent. The singular positions are those where the six lines are dependent, for example when all six lines meet one common line.
- **Assemblies in CAD.** In [assembly constraint solving](/assembly-constraint-solving/), rigid parts in space have 6 degrees of freedom each, and point-to-point distance constraints between parts are bars. For constraints in general position, Tay's theorem decides whether the assembly is generically well-constrained.
- **Hinges.** In space, a hinge between two bodies removes 5 of the 6 relative degrees of freedom, like 5 bars that all meet the hinge line. Tay and Whiteley proved that body-and-hinge frameworks are generically rigid exactly when the multigraph with every edge replaced by $D - 1$ copies contains $D$ edge-disjoint spanning trees, and Katoh and Tanigawa (2011) proved that the same holds when the hinges at each body pass through one point, the molecular conjecture.

## Tightness

The ranks below are exact ranks of the matrix $M$ with rational arithmetic, at random integer points unless stated.

- **Genericity is needed.** Two bodies in the plane joined by three bars have rank $3 = D(n - 1)$ at random points. If the three bar lines pass through one point, the rank is 2: the bodies can turn about that point relative to each other. In space, two bodies joined by six bars have rank 6, but rank 5 when all six bar lines meet one common line, which allows an infinitesimal rotation about it.
- **The total count is not enough.** In the plane, take three bodies, four bars between bodies 1 and 2, and two between bodies 2 and 3. There are $6 = D(n - 1)$ bars, but the partition $\{1, 2\}, \{3\}$ has only $2 < 3$ crossing bars, and the rank is 5. The partition condition fails, and body 3 can move.
- **The condition is met.** Three bodies in the plane with two bars between each pair have $6$ bars and rank 6. The three trees $\{12, 23\}$, $\{23', 13\}$, $\{13', 12'\}$, with primes for the second copy of each bar, are edge-disjoint spanning trees.
- **Joints are not bodies.** A bar-and-joint framework in space cannot be treated as a body-and-bar framework with one body per joint: all bars at a joint would pass through one point, which is a special position, so the theorem gives no information. This is why the double banana, which meets the count $3n - 6$ and is flexible, is no counterexample to Tay's theorem.
- **Dimension 1.** For $d = 1$, $D = 1$, and the theorem says that bodies on a line joined by bars are rigid exactly when the multigraph is connected, the same answer as for joints.

## History

Tay (1984) proved the theorem for bodies in every dimension, in the first paper of his series on the rigidity of multigraphs. Whiteley (1988) gave a proof through the union of matroids and placed the result among other rigidity matroids that are unions of graphic matroids. The combinatorial side is older: Nash-Williams and Tutte (1961) found the partition condition for edge-disjoint spanning trees, and Nash-Williams (1964) the covering of a graph by forests. Tay and Whiteley then treated body-and-hinge frameworks, and Katoh and Tanigawa settled the molecular conjecture for hinges through one point per body in 2011.

## References
