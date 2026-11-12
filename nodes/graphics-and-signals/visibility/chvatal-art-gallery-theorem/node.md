---
tag: 9V33Q8
kind: theorem
slug: chvatal-art-gallery-theorem
name: Chvátal's art gallery theorem
area: graphics-and-signals/visibility
level: core
summary: Floor(n/3) vertex guards always see all of a simple polygon with n vertices. Chvátal's 1975 proof splits every triangulation into at most floor(n/3) fans by induction.
prereqs: [simple-polygon, polygon-triangulation, two-ears-theorem]
see_also: [art-gallery-theorem, art-gallery-problem, orthogonal-art-gallery-theorem, minimum-guard-np-hardness, visibility-polygon, star-shaped-polygon, polygon-triangulation, two-ears-theorem]
sources:
  - paper: doi:10.1016/0095-8956(75)90061-1
    title: Václav Chvátal, A combinatorial theorem in plane geometry, Journal of Combinatorial Theory, Series B 18(1), 1975, pages 39 to 41
    locator: the whole note (the theorem and the proof by induction on a triangulation)
  - book: isbn:9780195039658
    title: Joseph O'Rourke, Art Gallery Theorems and Algorithms, Oxford University Press, 1987
    locator: Chapter 1, Section 1.2.1 (Chvátal's proof, Lemma 1.1 and Theorem 1.1) and Section 1.2.2 (the remark on a direct implementation)
  - paper: doi:10.1016/0095-8956(78)90059-X
    title: Steve Fisk, A short proof of Chvátal's watchman theorem, Journal of Combinatorial Theory, Series B 24(3), 1978, page 374
    locator: the whole note (the later proof by 3-coloring, given on the art gallery theorem page)
---

Chvátal's art gallery theorem says that $\lfloor n/3 \rfloor$ guards, all placed at vertices, always see every point of a simple polygon with $n$ vertices. Václav Chvátal proved it in 1975, in answer to a question of Victor Klee. This page gives Chvátal's own proof. It shows by induction that every triangulation of the polygon splits into at most $\lfloor n/3 \rfloor$ *fans*, groups of triangles with a common corner, and it puts one guard at the common corner of each fan. The shorter proof by 3-coloring (Fisk 1978), the comb that shows the bound is tight, and the $O(n)$ placement of the guards after a triangulation are on the [art gallery theorem](/art-gallery-theorem/) page in geometry, and are not repeated here. The question of the fewest guards for one given polygon is the [art gallery problem](/art-gallery-problem/), which is [NP-hard](/minimum-guard-np-hardness/).

## Statement

**Setting.** $P$ is a [simple polygon](/simple-polygon/) with $n \ge 3$ vertices, taken as a closed region: its boundary and its interior. A point $x \in P$ *sees* $y \in P$ if the closed segment $xy$ lies in $P$; the segment may touch the boundary. A *triangulation* of $P$ is a partition of $P$ into triangles by diagonals, segments between two vertices that lie inside $P$ and do not cross each other (see [polygon triangulation](/polygon-triangulation/)). Every simple polygon has one, with $n - 2$ triangles and $n - 3$ diagonals. A *fan* is a set of triangles of the triangulation that all have one vertex $c$, the *center*, as a corner.

**Theorem (Chvátal 1975).** Every triangulation of a simple polygon with $n$ vertices can be partitioned into at most $\lfloor n/3 \rfloor$ fans. As a consequence, $\lfloor n/3 \rfloor$ guards placed at vertices of $P$ see all of $P$.

The bound is the best possible: some polygons need $\lfloor n/3 \rfloor$ guards even at arbitrary points. The example is the comb on the [art gallery theorem](/art-gallery-theorem/) page.

## In plain words

Cut the floor plan of a room into triangles with straight walls from corner to corner. A guard who stands at a corner of a triangle sees all of that triangle, because a triangle has no hidden parts. So if many triangles share one corner, one guard there sees all of them. Chvátal showed that you can always sort the triangles into groups that share a corner, with at most one group for every three corners of the room. He did this by cutting off a small piece of the room with four, five or six walls, solving the rest first, and then checking each way the small piece can look. One guard per group is then enough.

## Proof

The guard statement follows from the fan statement: the center of a fan is a corner of each of its triangles, a triangle is convex, so the center sees each triangle of its fan, and the triangles cover $P$. The rest of the proof is about fans and uses only which vertices form triangles, not the coordinates.

Label the vertices $0, 1, \dots, n - 1$ in order along the boundary. A diagonal $(i, j)$ with $i < j$ splits $P$ into the polygon with vertices $i, i + 1, \dots, j$ and the polygon with vertices $j, \dots, n - 1, 0, \dots, i$. The first has $j - i$ edges of $P$ on its boundary, and we say that the diagonal *cuts off* $j - i$ edges on that side and $n - (j - i)$ edges on the other side. Each of the two polygons is triangulated by the triangles of $P$ on its side.

**Lemma 1 (small polygons are fans).** Every triangulation of a polygon with 3, 4 or 5 vertices is a fan.

*Proof.* With 3 vertices there is one triangle. With 4 vertices there is one diagonal, and both triangles contain its two ends. With 5 vertices there are two diagonals, and they cannot have four distinct ends. Suppose their ends are $a < b < c < d$ among $0, \dots, 4$. A diagonal $(i, j)$ with $i < j$ has $2 \le j - i \le 3$, because $(0, 4)$ is an edge. The pairs $(a, c), (b, d)$ cross. The pairs $(a, b), (c, d)$ give $d - a \ge 2 + 1 + 2 = 5$. The pairs $(a, d), (b, c)$ give $d - a \ge 1 + 2 + 1 = 4$, but $d - a \le 3$. So the two diagonals share an end $v$, and each of the three triangles has $v$ as a corner. $\square$

**Lemma 2 (Chvátal).** If $n \ge 6$, every triangulation has a diagonal that cuts off exactly 4, 5 or 6 edges.

*Proof.* First, some diagonal cuts off at least 4 edges on one side. For $n \ge 7$, any diagonal does, since its two sides add to $n$. For $n = 6$, the triangulation has an ear, a triangle with two polygon edges (see the [two ears theorem](/two-ears-theorem/)), and the diagonal of the ear cuts off 4 edges on its other side. Now choose a diagonal $d$ and a side so that the number $k \ge 4$ of edges cut off on that side is as small as possible, and label the vertices so that $d = (0, k)$ and the side is $0, 1, \dots, k$. On this side, $d$ is an edge of one triangle $T = (0, t, k)$ with $0 < t < k$. The segment $(0, t)$ is a polygon edge or a diagonal that cuts off $t$ edges, and $(t, k)$ cuts off $k - t$ edges, both fewer than $k$. By the choice of $k$, $t \le 3$ and $k - t \le 3$, so $k \le 6$. $\square$

**Theorem.** Every triangulation of a polygon with $n \ge 3$ vertices is a union of at most $\lfloor n/3 \rfloor$ fans that do not share triangles.

*Proof.* By induction on $n$. For $n \le 5$, Lemma 1 gives one fan, and $\lfloor n/3 \rfloor = 1$. Let $n \ge 6$. Take $d = (0, k)$, $k \in \{4, 5, 6\}$, and $T = (0, t, k)$ as in Lemma 2. Let $G_1$ be the triangulated polygon $0, 1, \dots, k$ with $k + 1$ vertices, and $G_2$ the rest, with the vertices $k, \dots, n - 1, 0$, that is, $n - k + 1 \ge 3$ vertices. By induction, $G_2$ splits into at most $\lfloor (n - k + 1)/3 \rfloor \le \lfloor (n - 3)/3 \rfloor = \lfloor n/3 \rfloor - 1$ fans. So it is enough to cover the triangles of $G_1$ with one more fan, after we change the fans of $G_2$ if needed. In each case below, a fan $F$ that contains a triangle has its center at a corner of that triangle.

*Case 1: $k = 4$.* $G_1$ has 5 vertices, so it is a fan by Lemma 1. This is the one more fan.

*Case 2: $k = 5$.* $G_1$ is a hexagon. The apex $t$ is not 1, since then $(1, 5)$ would cut off 4 edges, and not 4, since then $(0, 4)$ would cut off 4 edges. The cases $t = 2$ and $t = 3$ are mirror images, so let $t = 2$. The triangle $(0, 1, 2)$ is in $G_1$, and the quadrilateral $2, 3, 4, 5$ has one of its two diagonals.

- *Case 2a: the diagonal $(2, 4)$.* All four triangles of $G_1$, namely $(0, 1, 2)$, $(0, 2, 5)$, $(2, 3, 4)$ and $(2, 4, 5)$, contain 2. So $G_1$ is a fan with center 2.
- *Case 2b: the diagonal $(3, 5)$.* Let $G_0 = G_2 \cup T$, a triangulated polygon with the vertices $5, \dots, n - 1, 0, 2$, that is, $n - 3$ vertices. By induction it splits into at most $\lfloor (n - 3)/3 \rfloor = \lfloor n/3 \rfloor - 1$ fans. Let $F$ be the fan that contains $T$; its center is 0, 2 or 5.
  - *Case 2b.1: the center is 0 or 2.* Add $(0, 1, 2)$ to $F$. The two triangles $(2, 3, 5)$ and $(3, 4, 5)$ form one more fan, with center 3 or 5.
  - *Case 2b.2: the center is 5.* Add $(2, 3, 5)$ and $(3, 4, 5)$ to $F$. The triangle $(0, 1, 2)$ is one more fan.

*Case 3: $k = 6$.* $G_1$ is a heptagon. The apex $t$ is 3: for $t = 1, 2, 4, 5$ the segment $(1, 6)$, $(2, 6)$, $(0, 4)$ or $(0, 5)$ would be a diagonal that cuts off 5, 4, 4 or 5 edges, fewer than 6. The quadrilaterals $0, 1, 2, 3$ and $3, 4, 5, 6$ have one diagonal each, which gives four cases.

- *Case 3a: the diagonals $(1, 3)$ and $(3, 5)$.* Every triangle of $G_1$ contains 3, so $G_1$ is a fan with center 3.
- *Case 3b: the diagonals $(0, 2)$ and $(3, 5)$.* Let $G_0$ be $G_2$ together with the triangles $(0, 2, 3)$ and $T$. It is a triangulated polygon with the vertices $6, \dots, n - 1, 0, 2, 3$, that is, $n - 3$ vertices, so it splits into at most $\lfloor n/3 \rfloor - 1$ fans. Let $F$ be the fan that contains $(0, 2, 3)$.
  - *Case 3b.1: the center is 0 or 2.* Add $(0, 1, 2)$ to $F$. The triangles $(3, 4, 5)$ and $(3, 5, 6)$ form one more fan, with center 3.
  - *Case 3b.2: the center is 3.* Add $(3, 4, 5)$ and $(3, 5, 6)$ to $F$. The triangle $(0, 1, 2)$ is one more fan.
- *Case 3c: the diagonals $(1, 3)$ and $(4, 6)$.* This is the mirror image of Case 3b.
- *Case 3d: the diagonals $(0, 2)$ and $(4, 6)$.* Let $G_0 = G_2 \cup T$, with the vertices $6, \dots, n - 1, 0, 3$, that is, $n - 4$ vertices, so it splits into at most $\lfloor (n - 4)/3 \rfloor \le \lfloor n/3 \rfloor - 1$ fans. Let $F$ be the fan that contains $T$.
  - *Case 3d.1: the center is 0.* Add $(0, 1, 2)$ and $(0, 2, 3)$ to $F$. The triangles $(3, 4, 6)$ and $(4, 5, 6)$ form one more fan, with center 4 or 6.
  - *Case 3d.2: the center is 3.* In $G_0$ the vertex 3 has only the neighbors 0 and 6, so $T$ is the only triangle of $G_0$ at 3, and $F = \{T\}$. Take 0 as its center instead, and go on as in Case 3d.1.
  - *Case 3d.3: the center is 6.* This is the mirror image of Case 3d.1.

In every case, the triangles of $P$ are split into at most $(\lfloor n/3 \rfloor - 1) + 1 = \lfloor n/3 \rfloor$ fans. $\square$

**Why the cut must be at least 4.** Cutting off an ear removes only one vertex. For $n \equiv 1$ or $2 \pmod 3$, induction then gives $\lfloor (n - 1)/3 \rfloor = \lfloor n/3 \rfloor$ fans for the rest, and there is no room for the ear. So the proof cuts off at least 3 vertices. A diagonal that cuts off exactly 4 edges need not exist, as the example below shows, and that is why Lemma 2 allows 5 and 6.

**Example.** Take an octagon with the vertices $0, \dots, 7$ and the triangles $(0, 1, 2)$, $(0, 2, 5)$, $(2, 3, 5)$, $(3, 4, 5)$, $(0, 5, 7)$ and $(5, 6, 7)$. The diagonals and the edges they cut off are:

| diagonal | edges on the two sides |
|---|---|
| $(0, 2)$ | 2 and 6 |
| $(0, 5)$ | 5 and 3 |
| $(2, 5)$ | 3 and 5 |
| $(3, 5)$ | 2 and 6 |
| $(5, 7)$ | 2 and 6 |

No diagonal cuts off 4 edges, and the least cut of at least 4 is $k = 5$, for $d = (0, 5)$ with $G_1$ the hexagon $0, \dots, 5$. The triangle on $d$ is $T = (0, 2, 5)$ with $t = 2$, and the quadrilateral $2, 3, 4, 5$ has the diagonal $(3, 5)$: Case 2b. Then $G_0$ is the pentagon $5, 6, 7, 0, 2$ with the triangles $(0, 2, 5)$, $(0, 5, 7)$ and $(5, 6, 7)$, which is one fan with center 5. So $F$ has center 5: Case 2b.2. Add $(2, 3, 5)$ and $(3, 4, 5)$ to $F$, and make $(0, 1, 2)$ its own fan. The result is $\lfloor 8/3 \rfloor = 2$ fans: five triangles around vertex 5, and the triangle $(0, 1, 2)$ with center 0. Guards at the vertices 5 and 0 see the whole octagon.

## Consequences

- **Vertex guards are enough.** The guards of the proof are at vertices. So the worst case is the same for vertex guards and for guards at any points of $P$: $\lfloor n/3 \rfloor$ in both cases, with the comb for the lower bound.
- **A fan partition.** The proof gives more than guards: a partition of any triangulation into at most $\lfloor n/3 \rfloor$ fans, so $P$ is a union of at most $\lfloor n/3 \rfloor$ sets, each star-shaped from one of its own corners (compare [star-shaped polygons](/star-shaped-polygon/)).
- **An algorithm.** The proof is constructive. Each step finds the diagonal of Lemma 2 and recurses, so a direct implementation costs $O(n)$ per step and $O(n^2)$ in total after the triangulation. Fisk's 3-coloring proof gives a faster method, which is on the [art gallery theorem](/art-gallery-theorem/) page.
- **The method of the proof.** The idea of cutting off a piece of bounded size and checking all its shapes also proves other guard bounds, where coloring arguments do not apply. O'Rourke's book uses it again in Chapter 3.
- **Not the fewest guards.** The theorem bounds the worst case over all polygons with $n$ vertices. For one given polygon, the fewest guards can be far fewer, and finding that number is [NP-hard](/minimum-guard-np-hardness/). For an orthogonal polygon the bound drops to $\lfloor n/4 \rfloor$ ([orthogonal art gallery theorem](/orthogonal-art-gallery-theorem/)).

## Tightness

The bound $\lfloor n/3 \rfloor$ cannot be lowered: a comb with $k$ prongs has $n = 3k$ vertices, and no point sees into two prongs, so it needs $k$ guards. The details are on the [art gallery theorem](/art-gallery-theorem/) page. The fan bound is tight in the same examples, since a fan partition gives a guard set.

The two parts of Lemma 2 are tight as well. The octagon of the example has no diagonal that cuts off exactly 4 edges, so the range cannot shrink to $\{4\}$. The proof needs the range up to 6 because the cut and the apex $t$ can each use up to 3 edges.

The theorem needs a simple polygon. In a polygon with holes, a guard can be blocked by a hole as well, the triangulation has more triangles than $n - 2$, and more than $\lfloor n/3 \rfloor$ guards can be needed (see [polygon with holes](/polygon-with-holes/)).

## History

Victor Klee asked in 1973 how many guards are needed for a gallery whose floor plan is a polygon with $n$ walls. Chvátal answered in a three-page note in 1975, with the proof above. Steve Fisk gave the proof by 3-coloring in 1978, and it is the one most textbooks use. O'Rourke's 1987 book on art gallery theorems gives both proofs in Chapter 1, in the case structure used on this page, and remarks that Chvátal's argument extends to cases where Fisk's does not.

## References
