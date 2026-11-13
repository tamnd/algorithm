---
tag: AM42WY
kind: algorithm
slug: owen-triconnected-decomposition
name: Owen's triconnected decomposition
aliases:
- top-down constraint decomposition
area: cad/geometric-constraint-solving
level: advanced
summary: Owen's solver that splits the constraint graph at separation pairs into triconnected parts, solves each and reassembles them, for systems solvable by quadratics.
model: real-ram
complexity:
  vars: {n: the number of points, m: "the number of distance constraints, 2n - 3"}
  time: {worst: O(n^2)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: true, exact: true}
history:
  year: 1991
  people: [John C. Owen]
  note: Owen published the method at the first ACM Symposium on Solid Modeling Foundations and CAD/CAM Applications in 1991; Joan-Arinyo, Soto-Riera, Vila-Marta and Vilaplana-Pastó proved in 2002 that it solves the same graphs as the bottom-up reduction of Fudos and Hoffmann.
prereqs: [constructive-constraint-solving, biconnected-components]
see_also: [fudos-hoffmann-reduction, dr-plan, ruler-and-compass-constructibility, root-identification-problem, k-vertex-connected-graph, vertex-cut, hopcroft-tarjan-biconnectivity, circle-circle-intersection]
sources:
  - paper: doi:10.1145/112515.112573
    title: John C. Owen, Algebraic solution for geometry from dimensional constraints, ACM Symposium on Solid Modeling Foundations and CAD/CAM Applications (SMA '91), 397 to 407, 1991
    locator: the decomposition of the constraint graph at separation pairs with virtual edges, the use of the triconnected components algorithm, the solution by quadratic equations and the quadratic running time (general locator)
  - paper: doi:10.1137/0202012
    title: John E. Hopcroft and Robert E. Tarjan, Dividing a graph into triconnected components, SIAM Journal on Computing 2(3), 135 to 158, 1973
    locator: the linear-time algorithm for separation pairs and triconnected components, with virtual edges (general locator)
  - paper: doi:10.1145/566282.566300
    title: Robert Joan-Arinyo, Antoni Soto-Riera, Sebastià Vila-Marta and Josep Vilaplana-Pastó, Revisiting decomposition analysis of geometric constraint graphs, ACM Symposium on Solid Modeling and Applications (SM '02), 105 to 115, 2002
    locator: the proof that Owen's top-down analysis and the bottom-up reduction of Fudos and Hoffmann decompose the same class of graphs (general locator)
  - paper: "Robert Joan-Arinyo, Antoni Soto-Riera, Sebastià Vila-Marta and Josep Vilaplana-Pastó, Revisiting decomposition analysis of geometric constraint graphs, Computer-Aided Design 36(2), 123 to 140, 2004"
    locator: the journal version of the comparison of the top-down and bottom-up analyses (general locator)
  - paper: doi:10.1090/S0002-9947-06-04049-9
    title: J. C. Owen and S. C. Power, The non-solvability by radicals of generic 3-connected planar Laman graphs, Transactions of the American Mathematical Society 359(5), 2269 to 2303, 2007
    locator: the main theorem, which shows that the 3-connected parts where the method stops need more than square roots (general locator)
---

Owen's decomposition is the top-down form of [graph-constructive solving](/constructive-constraint-solving/) for planar sketches. It looks for a *separation pair* $\{a, b\}$, two points whose removal cuts the constraint graph in two. One side is rigid by itself; the other side is rigid once the distance $\lvert ab \rvert$ is known, so the method gives it a *virtual edge* $ab$. Both sides are split again in the same way until every part is a triangle. The solver then works from the leaves: it solves the rigid side, measures $\lvert ab \rvert$ there, solves the other side with that length, and glues the two sides at $a$ and $b$ by a rigid motion. Each triangle is one [circle-circle intersection](/circle-circle-intersection/), so the solution needs only square roots. The method stops at a part with four or more points and no separation pair, that is, a 3-connected part such as the triangular prism, and these parts are exactly where square roots do not suffice. With a linear-time search for separation pairs the analysis takes $O(n^2)$ time.

## In plain words

Look at the sketch as a network of rods. Sometimes two joints hold the whole network together: if you pull them out, it falls into two pieces. Each piece is easier to solve than the whole.

One piece is fixed in shape by its own rods. The other piece is not, since it misses one rod: the one that the first piece holds in place between the two joints. So you solve the first piece, measure the distance between the two joints, and add that distance to the second piece as an extra rod. Now the second piece is fixed too. You solve it and lay it onto the first piece at the two joints.

Each piece is cut again until only triangles are left. A triangle with known sides is easy to draw with ruler and compass. If a piece cannot be cut, the method stops.

## The problem

**Input.** A Laman graph $G = (V, E)$: $n \ge 3$ points and $m = 2n - 3$ distance constraints, with every $k \ge 2$ points spanning at most $2k - 3$ edges, as in [Laman's theorem](/laman-theorem/). Each edge has a length $d(uv) > 0$. An optional integer draft $\hat x$ shows the intended shape.

**Output.** A decomposition tree whose leaves are triangles, or a report that some part is 3-connected and has no separation pair. For a tree, the solver also returns a placement $x : V \to \mathbb{R}^2$ with $\lvert x(u) - x(v) \rvert = d(uv)$ for every edge; each leaf triangle has the orientation of the draft.

**Separation pairs.** A pair $\{a, b\}$ is a separation pair of a part with vertex set $P$ if the graph on $P \setminus \{a, b\}$ is not connected. A Laman graph with at least 3 points is 2-connected, so a separation pair is the smallest kind of [vertex cut](/vertex-cut/) that it can have, and a part with no separation pair is [3-connected](/k-vertex-connected-graph/). Owen finds the pairs with the triconnected components algorithm of Hopcroft and Tarjan; this page splits at one pair at a time, which is simpler to state and to prove.

## The algorithm

```pseudo id=main
OWEN-DECOMPOSE(P, F)                       ▷ a part: points P, edges F (real and virtual)
L1  if |F| ≠ 2|P| − 3 then fail "not a Laman graph"
L2  if |P| = 3 then return TRI(P)
L3  {a, b} ← a separation pair of (P, F)
L4  if there is none then return FAIL         ▷ the part is 3-connected
L5  K ← one component of the graph on P − {a, b}; P1 ← K ∪ {a, b}; P2 ← P − K
L6  F1 ← the edges inside P1, with ab if ab ∈ F; F2 ← the rest; if |F1| < 2|P1| − 3 then swap the two sides
L7  F2 ← F2 ∪ {ab}, marked virtual if ab ∉ F; return SPLIT(a, b, OWEN-DECOMPOSE(P1, F1), OWEN-DECOMPOSE(P2, F2))

OWEN-SOLVE(T, d, x̂)
L8  if T = TRI(u, v, w) then place u at (0, 0), v at (d(uv), 0), and w at distances d(uw), d(vw) on the side of the sign of ORIENT(x̂(u), x̂(v), x̂(w)), computed exactly, 0 counting as +1; return
L9  T = SPLIT(a, b, T1, T2); X1 ← OWEN-SOLVE(T1, d, x̂)             ▷ the rigid side first
L10 if ab is virtual then d(ab) ← |X1(a) − X1(b)|; X2 ← OWEN-SOLVE(T2, d, x̂)
L11 return X1 together with X2 moved by the proper rigid motion that takes X2(a), X2(b) to X1(a), X1(b)
```

**The split.** Line L1 checks the count on each part, which also catches a wrong input. Line L3 finds a separation pair; with the [Hopcroft-Tarjan](/hopcroft-tarjan-biconnectivity/) low-point search for articulation points, run once with each point $a$ removed, it costs $O(k(k + m_k))$ for a part with $k$ points and $m_k$ edges, and Hopcroft and Tarjan's triconnectivity algorithm does it in $O(k + m_k)$. Line L5 takes one component $K$ and gives the pair to both sides. Line L6 puts each edge on its side: an edge cannot join $K$ to the rest, because $\{a, b\}$ separates them. The two sides together have one edge too few to be two Laman graphs, so exactly one side has the full count $2|P_i| - 3$ and the other has one edge less; line L6 makes the full side the first side. Line L7 gives the other side the edge $ab$, which makes it a Laman graph too.

**The solve.** Line L8 draws a triangle. Lines L9 and L10 solve the rigid side first, because the length of a virtual edge is not a given value: it is measured on the solved rigid side. A real edge $ab$ keeps its given length on both sides. Line L11 glues the two sides. The two placements agree on $\lvert ab \rvert$, so one rotation and one translation take $a$ and $b$ of the second side onto $a$ and $b$ of the first; the motion is proper, so it keeps the orientations that the triangles chose.

**The sign.** The draft enters only in line L8, through the [orientation test](/orientation-test/) of the three draft points. In floating point a nearly flat draft triangle can get the wrong sign by [catastrophic cancellation](/catastrophic-cancellation/), and the leaf is then mirrored. The draft here has integer coordinates and the sign is exact; for a floating-point draft use exact arithmetic or a filtered predicate such as [Shewchuk's](/shewchuk-expansion-sum/), as in [exact geometric computation](/exact-geometric-computation/). A flat draft triangle gives 0, and the rule "0 counts as +1" is a crude form of [simulation of simplicity](/simulation-of-simplicity/). A Laman graph that decomposes has $n - 2$ leaves, so a vector of $n - 2$ signs selects one of up to $2^{n-2}$ branches.

## Example

Take the six points with the constraints $01, 02, 12, 34, 35, 45, 03, 04, 15$: two triangles $\{0, 1, 2\}$ and $\{3, 4, 5\}$, joined by bars $03$ and $04$ at point 0 and by the bar $15$. The draft is $(0, 0)$, $(6, 0)$, $(3, -4)$, $(-1, 5)$, $(3, 6)$, $(7, 4)$ for the points 0 to 5, and the lengths are measured on it, with $\lvert 01 \rvert^2 = 36$, $\lvert 02 \rvert^2 = \lvert 12 \rvert^2 = 25$, $\lvert 34 \rvert^2 = 17$, $\lvert 35 \rvert^2 = 65$, $\lvert 45 \rvert^2 = 20$, $\lvert 03 \rvert^2 = 26$, $\lvert 04 \rvert^2 = 45$ and $\lvert 15 \rvert^2 = 17$. Its separation pairs are $\{0, 1\}$ and $\{0, 5\}$. The decomposition makes three splits.

| part | pair | rigid side (first) | other side, with $ab$ |
|---|---|---|---|
| $\{0, 1, 2, 3, 4, 5\}$ | $\{0, 1\}$, a real edge | $\{0, 1, 2\}$ | $\{0, 1, 3, 4, 5\}$, edges $34, 35, 45, 03, 04, 15$ and $01$ |
| $\{0, 1, 3, 4, 5\}$ | $\{0, 5\}$, not an edge | $\{0, 3, 4, 5\}$, after the swap | $\{0, 1, 5\}$, edges $01, 15$ and virtual $05$ |
| $\{0, 3, 4, 5\}$ | $\{3, 4\}$, a real edge | $\{0, 3, 4\}$ | $\{3, 4, 5\}$ |

At the second split the component found first is $K = \{1\}$, so line L6 first gets the side $\{0, 1, 5\}$ with only the two edges $01$ and $15$, and it swaps the sides. The four leaves are solved in this order; the last column is the exact orientation of the draft points.

| leaf | squared sides $uv$, $uw$, $vw$ | ORIENT | where the lengths come from |
|---|---|---|---|
| $(0, 1, 2)$ | 36, 25, 25 | $-24$ | given |
| $(0, 3, 4)$ | 26, 45, 17 | $-21$ | given |
| $(3, 4, 5)$ | 17, 65, 20 | $-12$ | given; then glued at $\{3, 4\}$ into $\{0, 3, 4, 5\}$ |
| $(0, 1, 5)$ | 36, 65, 17 | $+24$ | $\lvert 05 \rvert^2 = 65$ is measured on $\{0, 3, 4, 5\}$ by line L10 |

Gluing at $\{0, 5\}$ and then at $\{0, 1\}$ gives the whole placement. The first leaf puts 0 at the origin and 1 at $(6, 0)$, as in the draft, so OWEN-SOLVE returns the draft itself. With other sign vectors, the measured length changes: if the leaves $(0, 3, 4)$ and $(3, 4, 5)$ put 0 and 5 on opposite sides of the line 34, then $\lvert 05 \rvert^2 = 2113/17 \approx 124.3$, the leaf $(0, 1, 5)$ violates the triangle inequality, and the branch has no real solution. So 8 of the 16 sign vectors give real placements.

The triangular prism, with the bars $03, 14, 25$ instead, is 3-connected: removing any two points leaves a connected graph. Line L4 fails at the root, although the prism is well-constrained for generic lengths. A triangle-decomposable graph is well-constrained, but a well-constrained graph need not be triangle-decomposable.

## Correctness

The [proof](proofs/correctness.md) shows the following for a Laman graph $G$.

- **The split keeps Laman graphs.** Each side has fewer points than the part. The side chosen first in line L6 is a Laman graph, and the other side becomes one when line L7 adds $ab$; no set of its points that holds $a$ and $b$ can have the full count without $ab$, because together with the rigid side it would break the count of $G$.
- **The split lemma.** $G$ is triangle-decomposable, in the sense of the [Fudos-Hoffmann reduction](/fudos-hoffmann-reduction/), exactly when both sides are. For one direction, the merges of the second side, with the edge $ab$ replaced by the rigid cluster of the first side, are merges of $G$. For the other direction, intersect each cluster of $G$ with each side; the counts force the intersections to be clusters of the sides.
- **Every decomposable part with 4 or more points has a separation pair.** In the last merge of three clusters, one cluster has 3 or more points, and its two shared points cut it from the other two clusters.
- **So the choice of pairs does not matter.** By induction, OWEN-DECOMPOSE returns a tree, whatever separation pairs and components it picks, exactly when $G$ is triangle-decomposable. This is the theorem of Joan-Arinyo and his coauthors in the form for points and distances.
- **The solution.** Each part is placed so that its constraints hold, and the glue is exact. If the lengths come from the draft and no leaf triangle is flat in the draft, the result is the draft moved by a proper rigid motion. Every real solution that keeps the two points of each virtual edge apart comes from one sign vector.

## Complexity

- **The tree.** A split of a part with $k$ points gives parts with $k_1 + k_2 = k + 2$ points and one edge more in total. So a decomposition has $n - 2$ leaves and $n - 3$ splits, and every part has at most $n$ points: the parts have $O(n^2)$ points and edges in total.
- **The analysis.** With a linear-time search for a separation pair, each part costs time linear in its size, and the decomposition takes $O(n^2)$ time. This matches the quadratic bound in Owen's paper. The implementation finds a pair by $k$ runs of the articulation point search, $O(k^2)$ per part, so it takes $O(n^3)$ time.
- **The solve.** Each leaf is $O(1)$ work with one square root. Each glue moves the points of the second side, at most $n$, so the solve takes $O(n^2)$ time.
- **Space.** The tree and its parts take $O(n^2)$ space as stored here; storing each part only by its split pair and children brings this to $O(n)$.

## Properties

- **Exact analysis.** The decomposition uses only the graph, so it holds for all values of the lengths.
- **Same class as the bottom-up method.** It decomposes exactly the triangle-decomposable graphs, the class of the [Fudos-Hoffmann reduction](/fudos-hoffmann-reduction/).
- **Quadratic equations only.** Each leaf solves one quadratic equation over the field of the earlier values, so the solution is [ruler-and-compass constructible](/ruler-and-compass-constructibility/), and the coordinates lie in an extension of degree at most $2^{n-2}$.
- **It stops at the right place.** By the theorem of Owen and Power, a generic 3-connected Laman graph with more than 3 points has coordinates that are not solvable by radicals. So the parts where line L4 fails are, for generic lengths, exactly those that no method with square roots, or radicals of any order, can solve.
- **Recursive.** The two sides are independent once $\lvert ab \rvert$ is known, so the recursion is natural, and the two sides of a split can be solved in parallel after the rigid side.

## Variants and improvements

- **All pairs at once.** Owen computes the triconnected components of the graph in one pass with the algorithm of Hopcroft and Tarjan, and treats each component with its virtual edges as one part. The split at one pair at a time is the same idea, one cut per step.
- **Points, lines, distances and angles.** Owen's graphs have points and lines as vertices, each with 2 freedoms, and distances and angles as edges, each of weight 1. A part made only of lines with angles needs care, because angles fix only directions.
- **Bottom-up form.** The [Fudos-Hoffmann reduction](/fudos-hoffmann-reduction/) merges clusters from the leaves, and finds the same plan in the other direction.
- **General parts.** A [DR-plan](/dr-plan/) accepts any rigid part as a node, not only triangles, so a 3-connected part such as the prism becomes one node for a numerical or algebraic solver.
- **Under-constrained sketches.** When a sketch has too few constraints, the method can add virtual edges to complete it, which shows the user which dimensions are still free.

## When to use it

- To analyze a planar sketch top-down, with the cut points visible, so that each part of the sketch is solved and changed separately.
- To get an exact solution by square roots and to choose it by the orientations of the draft.
- To check, in linear time per split, that a sketch can be solved by ruler and compass.

Do not use it alone for sketches with 3-connected parts, such as the prism or $K_{3,3}$: pass these parts to a general solver inside a [DR-plan](/dr-plan/). Do not use it in space, where two points do not fix a part.

## Pitfalls

- **Solving the wrong side first (line L6).** If line L6 does not swap the sides, the side with one edge too few is solved first, and $\lvert ab \rvert$ is not fixed there. In the example, at the pair $\{0, 5\}$ the side $\{0, 1, 5\}$ has only $01$ and $15$, so $\lvert 05 \rvert$ is free; the solver would measure a length that has nothing to do with the constraints.
- **Forgetting the virtual edge (line L7).** Without $ab$ the second side has $2k - 4$ edges, line L1 rejects it, or a solver accepts a part that can still flex.
- **The given length for a virtual edge (line L10).** The length of a virtual edge must be measured on the solved rigid side. Taking it from the draft is wrong as soon as the dimensions differ from the draft, and the glue of line L11 then cannot match both $a$ and $b$.
- **A mirror in the glue (line L11).** A motion that matches $a$ and $b$ but may reflect, such as a best-fit transform, can mirror the second side and destroy the orientations that its leaves chose. Use the rotation and translation fixed by the two points.
- **The sign in floating point (line L8).** A floating-point orientation of a nearly flat draft triangle can have the wrong sign and mirror a leaf. Compute it exactly.

## Implementations

## History

Owen presented the method in 1991, at the first ACM Symposium on Solid Modeling Foundations and CAD/CAM Applications, as an algebraic method to place geometry from given distances and angles. He used the triconnected components algorithm that Hopcroft and Tarjan had published in 1973, and he showed that the decomposed systems need only quadratic equations, with a solution in an extension of degree a power of 2. The bottom-up method of Bouma, Fudos and Hoffmann followed a few years later, and in 2002 Joan-Arinyo, Soto-Riera, Vila-Marta and Vilaplana-Pastó proved that the two methods decompose the same class of graphs. Owen and Power proved in 2007 that the 3-connected parts where the method stops are, for generic lengths, not solvable by radicals.

## References
