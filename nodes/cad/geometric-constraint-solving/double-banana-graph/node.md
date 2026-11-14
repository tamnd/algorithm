---
tag: CMMX2H
kind: concept
slug: double-banana-graph
name: Double banana graph
aliases:
- double banana
area: cad/geometric-constraint-solving
level: advanced
summary: Two triangular bipyramids glued at their two apexes. It has 3n - 6 edges and passes every subset count, yet it flexes in 3D, so Laman's count fails in three dimensions.
prereqs: [generic-rigidity, maxwell-counting-rule]
see_also: [laman-theorem, rigidity-matrix, hendrickson-global-rigidity-conditions, tay-theorem, witness-configuration-method, degrees-of-freedom-analysis, pebble-game-rigidity, dr-plan]
sources:
  - book: isbn:9780821838013
    title: Jack Graver, Brigitte Servatius and Herman Servatius, Combinatorial Rigidity, Graduate Studies in Mathematics 2, American Mathematical Society, 1993
    locator: Chapter 5, Rigidity in Higher Dimensions (the failure of the Laman count in space and the double banana)
  - paper: doi:10.1090/S0002-9947-1978-0511410-9
    title: L. Asimow and B. Roth, The rigidity of graphs, Transactions of the American Mathematical Society 245, 279 to 289, 1978
    locator: generic rigidity as a property of the graph and the rank test used for the double banana
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, CRC Press, 2018
    locator: the chapters on combinatorial rigidity in three dimensions and on decomposition of constraint systems, where the double banana is the standard example of a count that fails
  - paper: doi:10.1006/jsco.2000.0402
    title: Christoph M. Hoffmann, Andrew Lomonosov and Meera Sitharam, Decomposition plans for geometric constraint systems, part I, Journal of Symbolic Computation 31(4), 367 to 408, 2001
    locator: the discussion of dense subsystems that are not rigid in three dimensions
---

## In plain words

Take two spindle shapes, each made of six bars around a middle triangle and two tips. Each spindle is rigid on its own. Now glue the two spindles together at their tips, so that both share the same two tip pins. The result has exactly the number of bars that a rigid frame in space should have, and no part of it has too many bars. It still moves: one spindle can swing around the line through the two shared tips while the other stays fixed. So in three dimensions you cannot decide rigidity by counting bars, the way you can in the plane.

## The idea

**The graph.** Let $a$ and $b$ be two vertices, and let $c_1, c_2, c_3$ and $d_1, d_2, d_3$ be six more. The first *banana* is the complete graph on $\{a, b, c_1, c_2, c_3\}$ minus the edge $ab$, and the second banana is the complete graph on $\{a, b, d_1, d_2, d_3\}$ minus the edge $ab$. The double banana is their union. Each banana is a triangular bipyramid: the triangle $c_1 c_2 c_3$ with the two apexes $a$ and $b$, each joined to the three triangle vertices. So the double banana has
$$ n = 8, \qquad m = 9 + 9 = 18 = 3n - 6 . $$

**It passes the counts.** In $\mathbb{R}^3$ the analogue of [Laman's](/laman-theorem/) count asks for $m = 3n - 6$ edges and at most $3k - 6$ edges on every set of $k \ge 3$ vertices. These counts are necessary for generic minimal rigidity in space by [Maxwell's rule](/maxwell-counting-rule/). The double banana meets them. A banana spans exactly $9 = 3 \cdot 5 - 6$ edges, and inside one banana any 4 vertices span at most $6$ edges and any 3 at most 3. For a set $X$ that meets both bananas, let $X_1$ and $X_2$ be its parts in the two vertex sets, which overlap in $s = |X \cap \{a, b\}| \le 2$ vertices. The edges of $X$ are the edges inside $X_1$ plus those inside $X_2$, since no edge joins $c_i$ to $d_j$ and $ab$ is not an edge. If both parts have at least 3 vertices, this is at most $(3|X_1| - 6) + (3|X_2| - 6) = 3(k + s) - 12 \le 3k - 6$. If a part has at most 2 vertices, it adds at most one edge, on vertices that the other part does not hold. A brute force check over all $2^8$ subsets gives the largest edge counts $3, 6, 9, 11, 14, 18$ for $k = 3, \ldots, 8$, against the bounds $3, 6, 9, 12, 15, 18$.

**It is flexible.** Every point of the line $\ell$ through $p_a$ and $p_b$ stays fixed under a rotation about $\ell$. Rotate the second banana about $\ell$ and keep the first banana fixed. The bars of the second banana move with one rigid motion, so they keep their lengths. The bars of the first banana do not move. The only shared vertices are $a$ and $b$, which lie on $\ell$. So every bar keeps its length, while the distance from $c_1$ to $d_1$ changes. This is a continuous non-trivial motion at every placement, not only at a special one. So the double banana is not rigid in $\mathbb{R}^3$, and since generic rigidity is a property of the graph, it is not generically rigid.

**Where the count goes wrong.** Each banana is rigid, so it fixes the distance between its apexes $a$ and $b$. The length of the missing edge $ab$ is therefore implied twice, once by each banana. In the language of the [rigidity matrix](/rigidity-matrix/), the 18 rows have rank 17 and there is a one-dimensional space of self-stresses: the stress that writes the implied $ab$ row through the first banana, minus the same row through the second. This stress is nonzero on all 18 edges. One row too many is dependent, so one degree of freedom remains, which is exactly the hinge rotation. The count cannot see this, because the dependence comes from the edge $ab$, which is not in the graph. In the plane, two rigid parts can share at most one vertex without being rigid together, and Laman's count already accounts for it. In space, two rigid parts can share two vertices, which gives a hinge with one degree of freedom, and two vertices carry only one implied distance, not the $3 \cdot 2 - 6 = 0$ that the count assumes.

**The body and hinge view.** Read each banana as one rigid body. The two bodies are joined by a hinge, the line $ab$. In the body and hinge count of [Tay's theorem](/tay-theorem/) and its hinge form, two bodies have $6 \cdot 2 - 6 = 6$ degrees of freedom beyond the rigid motions, and a hinge removes 5. One remains, as found.

**It fails Hendrickson's conditions.** The double banana is sometimes named as the graph that shows that [Hendrickson's conditions](/hendrickson-global-rigidity-conditions/) for global rigidity are not sufficient in space. That is not right. The set $\{a, b\}$ separates it, so it is only 2-connected, not 4-connected, and it is not rigid at all, so it is not redundantly rigid. It fails both conditions. The graph that is 4-connected and redundantly rigid in space but not globally rigid is the complete bipartite graph $K_{5,5}$, found by Connelly (1991).

## Examples

All ranks are exact over the rationals, at random integer placements unless the coordinates are given.

- **Rank.** At three random integer placements in $\mathbb{R}^3$ the rank of the rigidity matrix is 17, one less than $3 \cdot 8 - 6 = 18$. Each banana alone has rank $9 = 3 \cdot 5 - 6$.
- **An explicit motion.** Put $a = (0, 0, 0)$, $b = (0, 0, 4)$, $c_1 = (2, 1, 1)$, $c_2 = (-1, 2, 2)$, $c_3 = (1, -2, 3)$, $d_1 = (3, 1, 2)$, $d_2 = (1, 3, 1)$, $d_3 = (-2, -1, 2)$. The axis $ab$ is the $z$-axis. Turn the second banana by $90°$, which sends $(x, y, z)$ to $(-y, x, z)$: $d_1 \mapsto (-1, 3, 2)$, $d_2 \mapsto (-3, 1, 1)$, $d_3 \mapsto (1, -2, 2)$. All 18 squared bar lengths are the same, and the squared distance from $c_1$ to $d_1$ changes from 2 to 14. The rank at this placement is also 17.
- **Adding the hinge does not help.** With the edge $ab$ added, $m = 19$ and the rank is still 17. The new row is implied by either banana, and the hinge rotation does not change $\lvert ab \rvert$. So the double banana plus $ab$ has two independent self-stresses and is still flexible.
- **One edge across.** With an edge $c_1 d_1$ added instead, the rank is $18 = 3 \cdot 8 - 6$ and the framework is generically rigid. The new edge blocks the rotation. The result has 19 edges and is rigid but not minimally rigid.
- **The plane analogue is caught.** In the plane, two rigid parts glued at one vertex turn about it. Two triangles sharing a vertex have $6 < 2 \cdot 5 - 3 = 7$ edges, so the count already reports the missing degree of freedom. The double banana pattern needs a hinge line, which first exists in three dimensions.

## Where it is used

- **Why there is no 3D Laman theorem.** The double banana is the standard proof that the counts $3n - 6$ and $3k - 6$ do not characterize generic rigidity in space. Any combinatorial algorithm for 3D rigidity must handle it, and none is known that is both exact and polynomial in general.
- **Pitfall for degree of freedom counting in CAD.** Solvers that decompose a 3D constraint system by counting degrees of freedom, as in [degrees of freedom analysis](/degrees-of-freedom-analysis/) and in [DR-plans](/dr-plan/), would accept the double banana as well-constrained, since no subset is over-constrained and the total is right. The system then has a one-parameter family of solutions, and a numerical solver sees a singular Jacobian. The [witness configuration method](/witness-configuration-method/) catches this: the rank of the Jacobian at a random placement is 17, not 18.
- **Pebble games in space.** The [pebble game](/pebble-game-rigidity/) decides the planar $(2, 3)$ count. The graphs with at most $3k - 6$ edges on every $k$ vertices do not even form a matroid, since sparse graphs for a $(k, l)$ count form a matroid only when $l < 2k$, so no such greedy test exists for bar frameworks in space. For body and bar frameworks the $(6, 6)$ count of Tay's theorem is a matroid count, and a pebble game decides it.
- **Molecules.** Bar frameworks with many triangles and shared hinges model molecules, where bond lengths and bond angles fix distances between atoms at distance one and two. The molecular conjecture of Tay and Whiteley, proved by Katoh and Tanigawa, says that for these special graphs (squares of graphs) generic rigidity agrees with that of a body and hinge framework, which has an exact count.
- **Test case.** Rigidity software, from rank tests to stress computations, uses the double banana as a first check that a method does not trust counts alone.

## References
