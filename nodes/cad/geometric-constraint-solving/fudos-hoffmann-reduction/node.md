---
tag: G145A2
kind: algorithm
slug: fudos-hoffmann-reduction
name: Fudos-Hoffmann cluster reduction
aliases:
- triangle decomposition solving
- bottom-up cluster merging
area: cad/geometric-constraint-solving
level: advanced
summary: Solves well-constrained 2D systems by merging rigid clusters three at a time whenever three clusters pairwise share an element, in O(n^2) time.
model: real-ram
complexity:
  vars: {n: the number of points, m: the number of distance constraints}
  time: {worst: O(m (n + m)), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1997
  people: [Ioannis Fudos, Christoph M. Hoffmann]
  note: Fudos and Hoffmann developed the reduction at Purdue for the constraint solver of Bouma, Fudos, Hoffmann, Cai and Paige (1995), and published the quadratic algorithm with its proof in ACM Transactions on Graphics in 1997.
prereqs: [constructive-constraint-solving, laman-theorem]
see_also: [owen-triconnected-decomposition, dr-plan, root-identification-problem, ruler-and-compass-constructibility, henneberg-construction, pebble-game-rigidity, circle-circle-intersection, orientation-test]
sources:
  - paper: doi:10.1145/248210.248223
    title: Ioannis Fudos and Christoph M. Hoffmann, A graph-constructive approach to solving systems of geometric constraints, ACM Transactions on Graphics 16(2), 179 to 216, 1997
    locator: the cluster formation by triangles, its proof of correctness and its quadratic running time; Section 2.2 on multiple solutions and root identification
  - paper: "William Bouma, Ioannis Fudos, Christoph M. Hoffmann, Jiazhen Cai and Robert Paige, Geometric constraint solver, Computer-Aided Design 27(6), 1995"
    locator: the solver in which the reduction is the analysis phase, with points, lines, distances and angles (general locator)
  - paper: doi:10.1145/566282.566300
    title: Robert Joan-Arinyo, Antoni Soto-Riera, Sebastià Vila-Marta and Josep Vilaplana-Pastó, Revisiting decomposition analysis of geometric constraint graphs, ACM Symposium on Solid Modeling and Applications (SM '02), 105 to 115, 2002
    locator: the proof that the bottom-up reduction and Owen's top-down method decompose the same class of graphs (general locator)
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, Chapman and Hall/CRC, 2018
    locator: the chapters on decomposition and constructive solving (general locator)
---

The Fudos-Hoffmann reduction is the bottom-up form of [graph-constructive solving](/constructive-constraint-solving/) for planar sketches. Its unit is the *cluster*, a set of points whose relative placement is fixed. It starts with one cluster per distance constraint, and it merges three clusters into one whenever they pairwise share one point, at three different points, because the three shared points then form a triangle with known sides. When one cluster holds every point, the graph is triangle-decomposable, and the list of merges is a plan: each merge is one [circle-circle intersection](/circle-circle-intersection/) and two rigid motions. The analysis takes $O(m(n + m))$ time, which is $O(n^2)$ for the $2n - 3$ constraints of a well-constrained system, and the final clusters do not depend on the order of the merges. A system that is well-constrained but not triangle-decomposable, such as the triangular prism, stops with several clusters, and the reduction reports them.

## In plain words

Think of each rod of a structure as a small rigid piece. Two pieces that share a joint can swing about it. Three pieces that share joints in a ring, the first with the second, the second with the third and the third with the first, cannot swing: the three joints form a triangle with known sides, so the three pieces together form one rigid piece.

The method looks for such rings again and again, replacing three pieces by one bigger piece. If one piece is left at the end, the whole structure is rigid, and the order of the merges says how to build it: for each merge, draw the triangle of the three joints with ruler and compass, then move the three pieces onto it. Each triangle can open to the left or to the right, and the method keeps the side that the user's draft shows.

## The problem

**Input.** A constraint graph $G = (V, E)$ of $n$ points and $m$ distance constraints, with a length $d(uv) > 0$ for each edge, and optionally an integer draft placement $\hat x$ that shows the intended shape. The graph is Laman-sparse: every $k \ge 2$ points span at most $2k - 3$ edges, which is the condition of [Laman's theorem](/laman-theorem/) without the total count.

**Output.** The final set of clusters and the list of merges. If one cluster holds all of $V$, the graph is *triangle-decomposable*, and the solver also returns a placement $x : V \to \mathbb{R}^2$ with $\lvert x(u) - x(v) \rvert = d(uv)$ for every edge, the one whose merge triangles have the orientations of the draft. Otherwise the output lists the rigid clusters; a merge that finds two clusters with two common points reports that the graph is over-constrained.

**Clusters.** A merge is valid for clusters $A, B, C$ when $A \cap B = \{p\}$, $A \cap C = \{q\}$, $B \cap C = \{r\}$ and $p, q, r$ are distinct. The new cluster is $A \cup B \cup C$. In the full method of Fudos and Hoffmann, clusters can also hold lines, and angle constraints give clusters of lines with fixed directions; this page treats points and distances, where all ideas already appear.

## The algorithm

```pseudo id=main
FH-REDUCE(V, E)
L1  S ← {{u, v} : uv ∈ E}                      ▷ one cluster per constraint
L2  W ← a stack that holds every cluster of S
L3  while W is not empty do
L4      A ← pop(W); if A ∉ S then continue
L5      for each cluster B ≠ A of S that meets A, let s(B) be the point it shares with A
L6          if B meets A in two points then fail "over-constrained"
L7      find B, C among them with a common point x ∉ A; if s(B) = s(C) then fail "over-constrained"
L8      if there are no such B, C then continue
L9      N ← A ∪ B ∪ C; append (A, B, C) to merges
L10     S ← (S − {A, B, C}) ∪ {N}; push N on W
L11 return S, merges

FH-SOLVE(V, E, d, x̂)
L12 S, merges ← FH-REDUCE(V, E); fail unless S = {V}
L13 place each cluster {u, v} with u at (0, 0) and v at (d(uv), 0)
L14 for each (A, B, C) in merges, in order do
L15     p ← the point of A ∩ B; q ← the point of A ∩ C; r ← the point of B ∩ C
L16     s ← sign of ORIENT(x̂(p), x̂(q), x̂(r)), computed exactly; 0 counts as +1
L17     R ← the point at distance |pr| (measured in B) from A's p and |qr| (measured in C) from A's q, on side s of pq
L18     move B by the proper rigid motion that takes its p to A's p and its r to R
L19     move C by the proper rigid motion that takes its q to A's q and its r to R
L20     give N the coordinates of A and of the moved B and C
L21 return the coordinates of the cluster V
```

**The reduction.** Lines L1 and L2 make each constraint a cluster of two points, and the stack $W$ holds the clusters that may still be part of a merge. Line L4 takes one; a cluster that an earlier merge used up is skipped. Lines L5 and L6 collect the clusters that meet $A$, each with its common point. Line L7 looks for two of them, $B$ and $C$, that also meet each other outside $A$: then $A, B, C$ pairwise share one point. To find them fast, keep a table from each point $x \notin A$ to the first collected cluster that holds it; a second cluster that holds $x$ gives the pair. If $B$ and $C$ meet $A$ at the same point, they share two points, and the graph is over-constrained. Line L10 replaces the three clusters by their union and pushes it, since the new cluster can be part of a new merge.

**The construction.** Each cluster has coordinates in its own frame. In a merge, $A$ already has $p$ and $q$, so the distance $\lvert pq \rvert$ is known, and $B$ and $C$ give $\lvert pr \rvert$ and $\lvert qr \rvert$. Line L17 places $r$ on the circle of radius $\lvert pr \rvert$ about $p$ and the circle of radius $\lvert qr \rvert$ about $q$, on the side of the draft. Lines L18 and L19 move $B$ and $C$ onto this triangle. Each motion is a rotation and a translation, fixed by two points, so it never mirrors a cluster.

**The sign.** Line L16 is the only place where the draft enters. The predicate is the [orientation test](/orientation-test/) of the three draft points: the sign of $(q - p) \times (r - p)$. Computed in floating point, a value near zero can have the wrong sign by [catastrophic cancellation](/catastrophic-cancellation/), and then line L17 builds the mirror triangle. The draft here has integer coordinates and the sign is exact; for a floating-point draft, use exact arithmetic or a filtered predicate such as [Shewchuk's](/shewchuk-expansion-sum/), as in [exact geometric computation](/exact-geometric-computation/). A collinear draft gives the sign 0, and the fixed rule "0 counts as +1" is a crude form of [simulation of simplicity](/simulation-of-simplicity/). Given a sign vector instead of a draft, one entry per merge, the solver follows any of the $2^{n-2}$ branches.

## Example

Take six points with the constraints $01, 02, 12, 34, 35, 45, 03, 04, 15$: two triangles $\{0, 1, 2\}$ and $\{3, 4, 5\}$ joined by three bars, two of which meet at point 0. (The prism, whose bars $03, 14, 25$ are disjoint, does not decompose.) The draft is $(0, 0)$, $(6, 0)$, $(3, -4)$, $(-1, 5)$, $(3, 6)$, $(7, 4)$ for the points 0 to 5, and the squared lengths are measured on it: $\lvert 01 \rvert^2 = 36$, $\lvert 02 \rvert^2 = 25$, $\lvert 12 \rvert^2 = 25$, $\lvert 34 \rvert^2 = 17$, $\lvert 35 \rvert^2 = 65$, $\lvert 45 \rvert^2 = 20$, $\lvert 03 \rvert^2 = 26$, $\lvert 04 \rvert^2 = 45$ and $\lvert 15 \rvert^2 = 17$.

The stack holds the nine edge clusters in input order, so the first pop is $\{1, 5\}$. It meets $\{0, 1\}$ and $\{1, 2\}$ at 1 and $\{3, 5\}$ and $\{4, 5\}$ at 5, but no two of these share a point outside $\{1, 5\}$, so line L8 goes on. The next pop, $\{0, 4\}$, finds $\{3, 4\}$ and $\{0, 3\}$, which meet at 3. These are the four merges. The column "squared sides" lists $\lvert pq \rvert^2$, $\lvert pr \rvert^2$, $\lvert qr \rvert^2$, and the last column is the exact orientation determinant of the draft points $p, q, r$.

| merge | $A$ | $B$ | $C$ | $p, q, r$ | squared sides | ORIENT |
|---|---|---|---|---|---|---|
| 1 | $\{0, 4\}$ | $\{3, 4\}$ | $\{0, 3\}$ | 4, 0, 3 | 45, 17, 26 | $-21$ |
| 2 | $\{0, 3, 4\}$ | $\{4, 5\}$ | $\{3, 5\}$ | 4, 3, 5 | 17, 20, 65 | $+12$ |
| 3 | $\{0, 3, 4, 5\}$ | $\{1, 5\}$ | $\{0, 1\}$ | 5, 0, 1 | 65, 17, 36 | $+24$ |
| 4 | $\{0, 1, 3, 4, 5\}$ | $\{1, 2\}$ | $\{0, 2\}$ | 1, 0, 2 | 36, 25, 25 | $+24$ |

In merge 3, the side $\lvert 50 \rvert^2 = 65$ is not a constraint: it is measured inside the cluster $\{0, 3, 4, 5\}$ built by the first two merges. The run makes $n - 2 = 4$ merges. With these signs, FH-SOLVE returns $x(0) = (0, 0)$, $x(4) = (\sqrt{45}, 0) \approx (6.7082, 0)$, $x(3) \approx (4.0249, 3.1305)$, $x(5) \approx (6.7082, -4.4721)$, $x(1) \approx (2.6833, -5.3666)$ and $x(2) \approx (-2.2361, -4.4721)$: the draft turned so that the first cluster $\{0, 4\}$ lies on the $x$-axis. All nine distances hold, and all signed areas equal those of the draft.

The other sign vectors show why a branch can fail. The draft has 0 and 5 on the same side of the line 34. If merges 1 and 2 put them on opposite sides, the measured side becomes $\lvert 50 \rvert^2 = 2113/17 \approx 124.3$, so $\lvert 50 \rvert \approx 11.15$ is longer than $\lvert 01 \rvert + \lvert 15 \rvert = 6 + \sqrt{17} \approx 10.12$, and merge 3 has no real triangle. So 8 of the $2^4 = 16$ sign vectors fail, and the other 8 give 8 different real placements.

On the prism, the reduction builds the two triangles and stops with five clusters: $\{0, 1, 2\}$, $\{3, 4, 5\}$ and the bars $\{0, 3\}$, $\{1, 4\}$, $\{2, 5\}$. No three of them pairwise share a point.

## Correctness

The [proof](proofs/correctness.md) shows the following for a Laman-sparse graph.

- **Cluster invariant.** At every step the edge sets of the clusters partition $E$, a cluster $C$ holds exactly $2|C| - 3$ edges, and two clusters share at most one point. A merge keeps the count, since $|A \cup B \cup C| = |A| + |B| + |C| - 3$. Two clusters with two common points would span more than $2k - 3$ edges on their $k$ points, so lines L6 and L7 fail only on graphs that are not sparse.
- **No merge is missed.** Every triple of clusters that could merge contains a cluster that is still on the stack. So when the stack is empty, no merge is possible.
- **The result does not depend on the order.** Every cluster formed in any run, in any order, lies inside a cluster of every final state. Two final states therefore have the same clusters.
- **The solution.** By induction over the merges, each cluster is placed so that all its constraints hold. If the lengths come from the draft and no merge triangle is flat in the draft, the placement is the draft moved by a proper rigid motion. Every solution in which the points $p$ and $q$ of each merge are distinct arises from one sign vector, so a triangle-decomposable system has at most $2^{n-2}$ such solutions up to proper motion.

## Complexity

- **One pop.** Lines L5 to L8 scan the clusters that meet $A$ and the points of each. The clusters are edge-disjoint and a cluster with $k$ points has $2k - 3 \ge k/2$ edges, so all clusters together have at most $2m$ points, and one pop costs $O(n + m)$.
- **All pops.** The stack receives $m$ edge clusters and one cluster per merge, and each merge removes two clusters, so there are at most $m + m/2$ pops. The reduction takes $O(m(n + m))$ time, which is $O(n^2)$ for a Laman graph. If no cluster meets another at all (a matching), each pop is $O(1)$ and the time is $\Theta(n + m)$.
- **The construction.** Each merge moves the points of $B$ and $C$, so the moves cost at most the total size of the clusters, $O(n)$ per merge and $O(n^2)$ in all. Each square root and each orientation test is $O(1)$ in the real RAM.
- **Space.** The clusters, the table from points to clusters and the stack take $\Theta(n + m)$ space.

## Properties

- **Exact analysis.** The reduction uses only the graph, so it is exact and fast, and the plan holds for all values of the lengths.
- **Order independent.** The final clusters, and so the answer to "is the graph triangle-decomposable", do not depend on the order of the stack. The list of merges does depend on it.
- **Solutions in a quadratic tower.** Each merge solves one quadratic equation, so the coordinates lie in a tower of quadratic extensions: the solution is [ruler-and-compass constructible](/ruler-and-compass-constructibility/).
- **Generic rigidity of clusters.** Each cluster is placed up to finitely many choices, so it is rigid for generic lengths. The converse fails: a rigid graph such as the prism need not reduce.
- **All roots or one root.** With the draft signs the solver returns the intended solution; with all sign vectors it lists all real solutions, up to $2^{n-2}$, except degenerate ones in which two shared points of a merge coincide, and the branches that fail a triangle inequality drop out, as in the example.

## Variants and improvements

- **Lines and angles.** Fudos and Hoffmann treat lines as entities as well. Two lines with an angle constraint fix only directions, so the method keeps sets of lines with fixed directions, with their own merge rules, and the triangle rule then works with points and lines mixed.
- **Top-down form.** [Owen's decomposition](/owen-triconnected-decomposition/) splits the graph at separation pairs from the top. Joan-Arinyo, Soto-Riera, Vila-Marta and Vilaplana-Pastó proved that it succeeds on the same graphs as the bottom-up reduction.
- **General clusters.** A [DR-plan](/dr-plan/) replaces the triangle rule by any minimal dense subgraph, found by flows, so a system such as the prism becomes one step for a general solver.
- **Completion of under-constrained systems.** When the reduction ends with several clusters, adding distance constraints between them that create new triangles makes the system decomposable. The added constraints are then shown to the user as free dimensions.
- **Incremental analysis.** When the user adds one constraint, only clusters that meet it can change, so the reduction can restart from the old clusters.

## When to use it

- To solve planar sketches with points, lines, distances and angles, which are triangle-decomposable in most practical cases, exactly and fast.
- To list all solutions of a sketch, or to choose one by the orientations of the draft.
- To reuse the plan: the analysis runs once, and each change of a dimension costs only the construction.

Do not use it alone for systems such as the prism or $K_{3,3}$, which are well-constrained but not triangle-decomposable; use a [DR-plan](/dr-plan/) with a general solver for the parts that remain. Do not use it in space, where the triangle rule does not make rigid clusters.

## Pitfalls

- **Missing the distinct-points test (line L7).** If line L7 accepts $B$ and $C$ that meet $A$ at the same point, the three clusters do not form a triangle: $B$ and $C$ share two points. Merging them silently accepts an over-constrained system, such as four points with all six distances, and the construction then fails or violates a constraint.
- **Not pushing the new cluster (line L10).** If line L10 does not push $N$ on the stack, merges that need $N$ are never found, and the reduction reports a decomposable graph as not decomposable. In the example, merges 2, 3 and 4 each use the cluster that the merge before them made.
- **The sign in floating point (line L16).** A floating-point orientation of nearly collinear draft points can have the wrong sign, and line L17 then builds the mirror triangle. Compute the sign exactly.
- **A mirror in the motion (lines L18 and L19).** A motion that matches two points but allows a reflection, such as a best-fit transform, can mirror a cluster and destroy the orientations that earlier merges chose. Use the rotation and translation fixed by two points.
- **Hiding a missing solution (line L17).** When $\lvert pr \rvert + \lvert qr \rvert < \lvert pq \rvert$, the circles do not meet. Code that clamps the negative square to 0 without a test returns a point that violates two constraints; clamp only within a relative tolerance, as the implementation does, and report the failure otherwise.

## Implementations

## History

Fudos worked on the reduction in his Purdue PhD research with Hoffmann in the early 1990s, as the analysis phase of the constraint solver of Bouma, Fudos, Hoffmann, Cai and Paige (Computer-Aided Design, 1995). The 1997 paper in ACM Transactions on Graphics gave the cluster rules for points and lines, a proof of correctness, and the quadratic algorithm. It also showed that the choice of the intended root is hard in general, which became the [root identification problem](/root-identification-problem/). Owen's top-down method of 1991 decomposes the same class of graphs, as Joan-Arinyo and his coauthors proved in 2002.

## References
