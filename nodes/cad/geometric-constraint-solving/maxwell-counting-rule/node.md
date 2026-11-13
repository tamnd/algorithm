---
tag: 4BTY52
kind: theorem
slug: maxwell-counting-rule
name: Maxwell's counting rule
aliases:
- Maxwell count
area: cad/geometric-constraint-solving
level: core
summary: A framework in the plane with n >= 2 joints that is infinitesimally or generically rigid needs 2n - 3 bars, and in a minimal one every k >= 2 joints span at most 2k - 3 bars.
prereqs: [infinitesimal-rigidity, rank]
see_also: [laman-theorem, generic-rigidity, bar-and-joint-framework, grubler-formula, degrees-of-freedom-analysis, well-constrained-system, tay-theorem, pebble-game-rigidity]
sources:
  - paper: doi:10.1080/14786446408643668
    title: J. Clerk Maxwell, On the calculation of the equilibrium and stiffness of frames, Philosophical Magazine, Series 4, 27(182), 294 to 299, 1864
    locator: the rule that a stiff frame of n points needs 2n - 3 bars in the plane and 3n - 6 in space
  - paper: doi:10.1016/0020-7683(78)90052-5
    title: C. R. Calladine, Buckminster Fuller's tensegrity structures and Clerk Maxwell's rules for the construction of stiff frames, International Journal of Solids and Structures 14(2), 161 to 172, 1978
    locator: the extended rule that relates bars, joints, states of self-stress and mechanisms
  - book: isbn:9780821838013
    title: Jack Graver, Brigitte Servatius and Herman Servatius, Combinatorial Rigidity, Graduate Studies in Mathematics 2, American Mathematical Society, 1993
    locator: Chapter 2, Infinitesimal Rigidity, Chapter 4, Linear and Planar Rigidity, and Chapter 5, Rigidity in Higher Dimensions (the double banana)
  - paper: doi:10.1090/S0002-9947-1978-0511410-9
    title: L. Asimow and B. Roth, The rigidity of graphs, Transactions of the American Mathematical Society 245, 279 to 289, 1978
    locator: the rank condition for infinitesimal rigidity and its agreement with rigidity at generic points
---

Maxwell's counting rule says that a [framework](/bar-and-joint-framework/) of $n \ge 2$ joints in the plane needs at least $2n - 3$ bars to be stiff, because $n$ points have $2n$ coordinates and the motions of the plane use up 3 of them. If it has exactly $2n - 3$ bars and is stiff, then no part of it can carry more bars than its own count, so every $k \ge 2$ joints span at most $2k - 3$ bars. In space the numbers are $3n - 6$ and $3k - 6$. The rule holds for [infinitesimal rigidity](/infinitesimal-rigidity/) and for [generic rigidity](/generic-rigidity/), but not for rigidity at special positions, and it is necessary but not sufficient.

## Statement

Let $(G, p)$ be a framework in $\mathbb{R}^d$ with $n \ge d$ joints and $m$ bars, and let $D = d(d + 1)/2$. For a set $X$ of joints, let $m(X)$ be the number of bars with both ends in $X$. Call $(G, p)$ *minimally infinitesimally rigid* if it is infinitesimally rigid and removing any bar makes it infinitesimally flexible.

**Theorem (Maxwell's counting rule).**

1. If $(G, p)$ is infinitesimally rigid, then $m \ge dn - D$. In the plane, $m \ge 2n - 3$.
2. If $(G, p)$ is minimally infinitesimally rigid, then $m = dn - D$, and every set $X$ of $k \ge d$ joints has $m(X) \le dk - D$. In the plane: $m = 2n - 3$ and $m(X) \le 2k - 3$ for every $X$ with $k \ge 2$ joints.
3. The same holds for graphs: if $G$ is generically rigid in $\mathbb{R}^d$, then $m \ge dn - D$, and if $G$ is generically minimally rigid, then $m = dn - D$ and $m(X) \le dk - D$ for every $X$ with $k \ge d$.
4. (Maxwell and Calladine.) If the joints span an affine space of dimension at least $d - 1$, then
$$ m - (dn - D) = s - f, $$
where $s$ is the dimension of the space of self-stresses and $f$ is the dimension of the non-trivial infinitesimal motions (the infinitesimal motions modulo the trivial ones).

## In plain words

Each joint in the plane can move in two directions, so free joints have twice as many ways to move as there are joints. Each bar blocks at most one of these ways. Three ways always remain, because you can still slide the whole structure left, slide it up, or turn it. So a stiff structure needs at least two bars per joint, minus three.

If a structure has just that many bars and is still stiff, then no bar is wasted. A wasted bar would be a bar inside a part that already had enough bars. So every part, on its own, has at most two bars per joint, minus three.

The count is a necessary test, not a proof of stiffness. Bars can be badly placed and still meet the count.

## Proof

Let $R = R(G, p)$ be the rigidity matrix, with one row per bar and $dn$ columns. Its kernel is the space of infinitesimal motions, and it contains the space $T(p)$ of trivial motions, $u_i = A p_i + b$ with $A$ skew-symmetric.

**Part 1.** Let $(G, p)$ be infinitesimally rigid with $n \ge d$. By the rank form of [infinitesimal rigidity](/infinitesimal-rigidity/), $\operatorname{rank} R = dn - D$. A matrix with $m$ rows has rank at most $m$, so $m \ge dn - D$.

**Part 2, the total.** If some row of $R$ is a linear combination of the other rows, then deleting that bar does not change the rank, so the framework stays infinitesimally rigid. So in a minimally infinitesimally rigid framework the $m$ rows are linearly independent, and $m = \operatorname{rank} R = dn - D$.

**Part 2, the subsets.** Let $X$ be a set of $k$ joints. The rows of the bars inside $X$ are independent, and they are zero outside the columns of $X$. In those columns they form the rigidity matrix of the framework $(G[X], p|_X)$, so
$$ m(X) = \operatorname{rank} R(G[X], p|_X) \le \operatorname{rank} R(K_k, p|_X). $$
Let the points of $X$ span an affine space of dimension $j$, with $j \le \min(d, k - 1)$. Every row lies in the directions of that space, so $\operatorname{rank} R(K_k, p|_X)$ is at most $jk - j(j + 1)/2$, the rank of a framework in $\mathbb{R}^j$, by the rank form applied in $\mathbb{R}^j$. If $j = d$ this is $dk - D$. If $j \le d - 1$, then
$$ dk - D - \Big(jk - \tfrac{j(j + 1)}{2}\Big) = (d - j)\Big(k - \tfrac{d + j + 1}{2}\Big) \ge 0, $$
because $k \ge d \ge (d + j + 1)/2$. In both cases $m(X) \le dk - D$. In the plane the same bound holds for every $k \ge 2$: if the points of $X$ are not all equal, the three trivial motions restricted to $X$ are independent and lie in the kernel, so the rank is at most $2k - 3$; if they are all equal, every row is zero and $m(X) = 0$.

**Part 3.** At a generic placement $p$, rigidity and infinitesimal rigidity agree (Asimow and Roth), and the rank of $R(G, p)$ equals the generic rank. So $G$ is generically rigid if and only if $(G, p)$ is infinitesimally rigid, and $G$ is generically minimally rigid if and only if $(G, p)$ is minimally infinitesimally rigid. Parts 1 and 2 at this $p$ give part 3.

**Part 4.** The self-stresses are the vectors $\omega \in \mathbb{R}^E$ with $\omega^\top R = 0$, so $s = m - \operatorname{rank} R$. The infinitesimal motions have dimension $dn - \operatorname{rank} R$, and if the joints span dimension at least $d - 1$ the trivial ones have dimension $D$, so $f = dn - \operatorname{rank} R - D$. Subtracting gives $s - f = m - dn + D$.

## Consequences

- **Laman's theorem.** In the plane the two counts of part 2 are also sufficient for generic minimal rigidity. This is [Laman's theorem](/laman-theorem/), and the [pebble game](/pebble-game-rigidity/) tests the counts in $O(n^2)$ time.
- **Every extra bar is a stress.** By part 4, a framework with $m > dn - D$ bars has at least $m - (dn - D)$ independent self-stresses. A statically determinate truss, with no self-stress and no mechanism, has exactly $dn - D$ bars. Engineers use this to decide whether the forces in a truss follow from equilibrium alone.
- **Degrees of freedom in CAD.** A sketch with $n$ points and $m$ distance constraints has $2n - m$ degrees of freedom by the naive count, and 3 of them are the rigid motions of the sketch. [Degrees of freedom analysis](/degrees-of-freedom-analysis/) in constraint solvers applies the count to every subsystem to find over-constrained and well-constrained parts, which is the subset condition of part 2.
- **Mechanisms.** The [Grübler formula](/grubler-formula/) for the mobility of a linkage is the same count for rigid links and joints, and it fails in the same way for special geometry, for example for the Bennett and Bricard linkages.
- **Body-and-bar frameworks.** For rigid bodies joined by bars, the count $D(n - 1)$ is necessary and, with the subset conditions on partitions, sufficient in every dimension ([Tay's theorem](/tay-theorem/)).

## Tightness

Each hypothesis is needed. The ranks below are exact ranks of the rigidity matrix, computed with rational arithmetic.

- **The count is not sufficient.** $K_4$ plus a fifth joint tied by one bar to a vertex of the $K_4$ has $n = 5$ and $m = 7 = 2n - 3$, but its rank is 6, so it is flexible: the fifth joint turns on a circle. The $K_4$ has 6 bars on 4 joints, above $2 \cdot 4 - 3 = 5$, so one bar is wasted. The total count passes and the subset count fails.
- **The subset counts are not sufficient in space.** The double banana, two copies of $K_5$ minus an edge glued at the two ends of the missing edge, has $n = 8$ and $m = 18 = 3n - 6$, and every set of $k \ge 3$ joints spans at most $3k - 6$ bars (an exhaustive check over all subsets). Its rank in $\mathbb{R}^3$ is 17, and the two bananas can turn about the line through their shared joints. So the converse of part 2 fails for $d = 3$, and no count of this kind characterizes generic rigidity in space.
- **Rigid frameworks can have fewer bars.** Put four joints at $0, 1, 2, 3$ on a line in the plane, with bars of lengths $1, 1, 1$ between neighbors and a bar of length 3 between the ends. By equality in the triangle inequality, every framework with these lengths is again on a line in this order, so the framework is rigid, even globally rigid. It has $4 < 2 \cdot 4 - 3 = 5$ bars. Its rigidity matrix has rank 3, so it is not infinitesimally rigid. The rule is about infinitesimal or generic rigidity, and a statement for every rigid framework is false.
- **Special positions break minimality.** $K_{3,3}$ meets both counts of part 2 and is generically minimally rigid, but on six points of a conic its rank is 8 $< 9$, so that framework is not infinitesimally rigid. The counts describe the graph, not each placement.
- **The condition $k \ge d$ in part 2.** For $k < d$ the bound $dk - D$ is less than $k(k - 1)/2$ or even negative, and the true bound is $k(k - 1)/2$. In the plane this only excludes $k = 1$, where $2k - 3 = -1$.

## History

Maxwell (1864) stated the rule in his paper on the equilibrium and stiffness of frames: a stiff frame of $n$ points needs $2n - 3$ bars in the plane and $3n - 6$ in space. Calladine (1978), studying the tensegrity structures of Buckminster Fuller, gave the exact form $m - (dn - D) = s - f$ with self-stresses and mechanisms. Pollaczek-Geiringer (1927) and Laman (1970) showed that in the plane the counts on all subsets are sufficient for generic minimal rigidity. Asimow and Roth (1978) put the rule on the footing of the rank of the rigidity matrix at generic points. The double banana, a standard example in the rigidity literature, shows that the counts are not sufficient in space.

## References
