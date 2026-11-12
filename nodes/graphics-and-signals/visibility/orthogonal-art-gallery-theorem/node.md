---
tag: 0RWN1Z
kind: theorem
slug: orthogonal-art-gallery-theorem
name: Orthogonal art gallery theorem
aliases:
- Kahn-Klawe-Kleitman theorem
area: graphics-and-signals/visibility
level: advanced
summary: Floor(n/4) vertex guards always see all of an orthogonal polygon with n vertices and no holes, and some need that many. The proof cuts the polygon into convex quadrilaterals.
prereqs: [rectilinear-polygon, art-gallery-theorem, triangulation-dual-tree]
see_also: [chvatal-art-gallery-theorem, art-gallery-theorem, art-gallery-problem, minimum-guard-np-hardness, rectilinear-polygon, polygon-with-holes, graph-coloring, visibility-polygon]
sources:
  - paper: doi:10.1137/0604020
    title: J. Kahn, M. Klawe and D. Kleitman, Traditional galleries require fewer watchmen, SIAM Journal on Algebraic and Discrete Methods 4(2), 1983, pages 194 to 206
    locator: the whole paper (the convex quadrilateralization theorem and the floor(n/4) bound)
  - book: isbn:9780195039658
    title: Joseph O'Rourke, Art Gallery Theorems and Algorithms, Oxford University Press, 1987
    locator: Chapter 2, Section 2.2 (Theorem 2.1 and Theorem 2.2), Sections 2.3 and 2.4 (the algorithms of Sack and Lubiw), Section 2.5 (Lemma 2.12, Theorem 2.5 and the proof by L-shaped pieces), and the preface on Chapter 5 (polygons with holes)
---

The orthogonal art gallery theorem says that $\lfloor n/4 \rfloor$ guards, all placed at vertices, always see every point of an orthogonal polygon with $n$ vertices and no holes, and that some orthogonal polygons need that many guards even at arbitrary points. An orthogonal polygon has only horizontal and vertical edges, like most floor plans, so the theorem says that such rooms need only three quarters of the $\lfloor n/3 \rfloor$ guards of [Chvátal's theorem](/chvatal-art-gallery-theorem/) for general polygons. Jeff Kahn, Maria Klawe and Daniel Kleitman proved it in 1980, and published it in 1983. Their proof first cuts the polygon into convex quadrilaterals, and then colors the corners with four colors, in the same way that the [art gallery theorem](/art-gallery-theorem/) page in geometry colors a triangulation with three. The definition and the vertex count of an orthogonal polygon are on the [rectilinear polygon](/rectilinear-polygon/) page. The fewest guards for one given polygon is a different question, the [art gallery problem](/art-gallery-problem/), and it is [NP-hard](/minimum-guard-np-hardness/).

## Statement

**Setting.** $P$ is an orthogonal polygon: a [simple polygon](/simple-polygon/) whose edges are all horizontal or vertical, and alternate between the two. It is taken as a closed region, with its boundary and its interior, and it has no holes. A point $x \in P$ *sees* $y \in P$ if the closed segment $xy$ lies in $P$. A *convex quadrilateralization* of $P$ is a partition of $P$ into convex quadrilaterals by diagonals, segments between two vertices that lie inside $P$ and do not cross each other.

**Theorem 1 (Kahn, Klawe and Kleitman).** Every orthogonal polygon, with or without holes, has a convex quadrilateralization.

**Theorem 2 (Kahn, Klawe and Kleitman).** Let $P$ be an orthogonal polygon with $n$ vertices and no holes. Then $\lfloor n/4 \rfloor$ guards placed at vertices of $P$ see all of $P$. For every $k \ge 1$ there is such a polygon with $n = 4k$ vertices that no set of fewer than $k$ guards at any points of $P$ sees.

**Equivalent form.** An orthogonal polygon with $n$ vertices has exactly $r = (n - 4)/2$ reflex vertices, so $n = 2r + 4$ and $\lfloor n/4 \rfloor = \lfloor r/2 \rfloor + 1$. Theorem 2 thus says that $\lfloor r/2 \rfloor + 1$ guards are always enough and sometimes needed.

## In plain words

Think of a museum whose walls all run north to south or east to west. Some of its corners point into the room, and these corners make places that are hard to see. The theorem says that one guard for every four corners is always enough, and that some museums of this kind need exactly that many. The proof cuts the floor into pieces with four straight sides and no dents, using cuts from corner to corner. Then it paints the corners with four colors, so that every piece has one corner of each color. Some color is used on at most one corner in four. Guards at the corners of that color see all of each piece, and so the whole museum.

## Proof

The proof has two parts. The first part, Theorem 1, is long, and this page gives its plan. The second part derives Theorem 2 from Theorem 1, and this page gives it in full.

**Lemma 1 (counts).** A convex quadrilateralization of an orthogonal polygon $P$ with $n$ vertices and no holes has $(n - 2)/2$ quadrilaterals, and its dual graph is a tree. The dual graph has one node for each quadrilateral and one arc for each diagonal, between the two quadrilaterals on its sides.

*Proof.* The interior angles of a simple polygon with $n$ vertices add up to $(n - 2)\pi$. The diagonals end at vertices, so the angles of the quadrilaterals fill the angles of $P$ exactly, and each quadrilateral has angles that add up to $2\pi$. So there are $(n - 2)\pi / 2\pi = (n - 2)/2$ quadrilaterals. The dual graph is connected, because $P$ is connected. A diagonal of a polygon without holes cuts it into two parts, so removing any arc disconnects the dual graph. A connected graph in which every arc is a bridge is a tree (see [triangulation dual tree](/triangulation-dual-tree/) for the same fact for triangles). $\square$

**Lemma 2 (four colors).** Let $G$ be the graph on the vertices of $P$ with the edges of all quadrilaterals and both diagonals of each quadrilateral. If $P$ has no holes, $G$ has a proper coloring with 4 colors, so the four corners of each quadrilateral have four different colors.

*Proof.* By induction on the number $q$ of quadrilaterals. For $q = 1$, give the four corners four colors. For $q \ge 2$, the dual tree of Lemma 1 has a leaf, a quadrilateral $Q$ that meets the rest along one diagonal $d = uv$. The other three sides of $Q$ are edges of $P$, so its two corners $w, z$ that are not on $d$ lie in no other quadrilateral. Remove $Q$. The rest is an orthogonal polygon without holes, quadrilateralized by the remaining quadrilaterals, and by induction it has a proper 4-coloring. Then $u$ and $v$ have different colors, because $d$ is a side of a quadrilateral in the rest. Give $w$ and $z$ the two colors that $u$ and $v$ do not use. The only new edges of $G$ are the six pairs of corners of $Q$, and they all join different colors. $\square$

The proof of Lemma 2 does not use the four color theorem (see [graph coloring](/graph-coloring/)), only the tree shape of Lemma 1. It also shows that every orthogonal polygon without holes with $n \ge 6$ has at least two leaf quadrilaterals, as a counterpart of the [two ears theorem](/two-ears-theorem/).

**Proof of Theorem 2, sufficiency.** By Theorem 1, $P$ has a convex quadrilateralization. Color $G$ as in Lemma 2. The four color classes split the $n$ vertices, so one class $C$ has at most $\lfloor n/4 \rfloor$ vertices. Each quadrilateral has one corner of each color, so it has a corner in $C$. A convex quadrilateral is seen in full from each of its corners. The quadrilaterals cover $P$, so the guards at $C$ see all of $P$. $\square$

**Proof of Theorem 2, necessity.** See the section on tightness below.

**Plan of the proof of Theorem 1.** This follows Kahn, Klawe and Kleitman, as O'Rourke gives it in Section 2.2.1. It is an induction on a size, where a polygon is smaller than another if it has fewer holes, or the same number of holes and fewer vertices. Without holes, this is the number of vertices.

1. *General position.* A small change of the coordinates does not change which quadrilateralizations exist, so it is enough to treat polygons where no two vertices have the same $x$ or the same $y$.
2. *Neighbors and tabs.* A top edge (the interior below it) and a bottom edge (the interior above it) are *neighbors* if they see each other and neither sees a closer edge of the other kind. A *tab* is a pair of neighbors joined by a vertical edge. A tab with the edges $ab$ and $cd$ forces the quadrilateral $abdc$ into every convex quadrilateralization (O'Rourke, Lemma 2.3). Tabs play the part that ears play for triangulations.
3. *Three reductions.* If $P$ has neighbors that do not form a tab, or a "good" tab, or a "tab pair" (an up tab and a down tab that face each other), then $P$ can be cut into smaller polygons with new tabs (or, with holes, into one polygon with fewer holes). A quadrilateralization of the smaller polygons then gives one of $P$ (O'Rourke, Lemmas 2.4, 2.5 and 2.6).
4. *One reduction always applies.* If none of the three applies, the edges of $P$ form an infinite sequence of distinct bottom edges, which is impossible (O'Rourke, Lemmas 2.7, 2.8 and 2.9).

A rectangle is the base case. A simple greedy method does not work: O'Rourke gives a polygon in which no pairing of the triangles of a triangulation gives convex quadrilaterals, and a polygon in which cutting off quadrilateral "ears" in a natural order leaves a piece that is not convex. That is why the proof needs the more careful tab structure.

**A second proof, by L-shaped pieces.** O'Rourke (Section 2.5, after his 1983 paper) proves the form $\lfloor r/2 \rfloor + 1$ without Theorem 1. A *cut* extends an edge at a reflex vertex into $P$ until it meets the boundary. It splits $P$ into two orthogonal polygons and makes that vertex convex in both. For $r \le 1$, $P$ is a rectangle or an L shape, and one guard at the reflex vertex (or anywhere, for a rectangle) sees it. For $r \ge 2$ there are two cases. If one cut joins two reflex vertices, the two pieces have $L$ and $R$ reflex vertices with $r = L + R + 2$, and induction gives $\lfloor L/2 \rfloor + \lfloor R/2 \rfloor + 2 \le \lfloor r/2 \rfloor + 1$ guards. If not, the proof uses an *odd cut*, a cut with an odd number $R$ of reflex vertices on one side. Then $r = L + R + 1$, and induction gives $\lfloor L/2 \rfloor + 1 + \lfloor (R - 1)/2 \rfloor + 1 = \lfloor r/2 \rfloor + 1$ guards. If $r$ is even, every cut is an odd cut, because $L + R = r - 1$ is odd. If $r$ is odd, O'Rourke shows that an odd cut exists when no two reflex vertices see each other along a horizontal or vertical line (Lemma 2.17), and this is the hard part of the proof. The pieces at the end are rectangles and L shapes, so the proof gives a partition into at most $\lfloor r/2 \rfloor + 1$ pieces, each seen from one point.

**Example.** Take the comb with two prongs and the vertices $0 = (0, 0)$, $1 = (3, 0)$, $2 = (3, 4)$, $3 = (2, 4)$, $4 = (2, 1)$, $5 = (1, 1)$, $6 = (1, 4)$, $7 = (0, 4)$, in counterclockwise order. It has $n = 8$ vertices, and the reflex vertices are 4 and 5, so $r = 2$ and $n = 2r + 4$. The diagonals $(1, 4)$ and $(0, 5)$ cut it into $(8 - 2)/2 = 3$ convex quadrilaterals: the trapezoid $(0, 1, 4, 5)$ at the bottom, and the right prong $(1, 2, 3, 4)$ and the left prong $(5, 6, 7, 0)$. The dual tree is a path with the trapezoid in the middle. Color the trapezoid with $0 \to a$, $1 \to b$, $4 \to c$, $5 \to d$. The right prong meets it on $(1, 4)$, colored $b, c$, so its other corners get $2 \to a$ and $3 \to d$. The left prong meets it on $(5, 0)$, colored $d, a$, so $6 \to b$ and $7 \to c$. Each color is used twice, $\lfloor 8/4 \rfloor = 2$, and each class is a guard set. For the class $a$, the guards are at $(0, 0)$ and $(3, 4)$: the first one is a corner of the trapezoid and of the left prong, and the second one is a corner of the right prong.

## Consequences

- **Vertex guards are enough.** The guards of the proof are at vertices, and the lower bound holds for guards at any points. So for orthogonal polygons without holes the worst case is $\lfloor n/4 \rfloor$ for both kinds of guard.
- **Fewer guards than for general polygons.** For the same number of vertices, an orthogonal polygon needs at most $\lfloor n/4 \rfloor$ guards, and a general simple polygon can need $\lfloor n/3 \rfloor$ ([Chvátal's theorem](/chvatal-art-gallery-theorem/)).
- **Convex quadrilaterals are a basic tool.** Theorem 1 does for orthogonal polygons what [triangulation](/polygon-triangulation/) does for general ones. It also holds with holes.
- **Algorithms.** The proof of Theorem 1 does not give a fast algorithm. Sack (1984) gave the first $O(n \log n)$ algorithm for a convex quadrilateralization, and Lubiw (1985) gave a short new proof that also gives an $O(n \log n)$ algorithm. After the quadrilateralization, the coloring of Lemma 2 and the choice of the smallest class take $O(n)$ time by a walk of the dual tree. The L-shaped proof also gives an $O(n \log n)$ method (O'Rourke, Section 2.6).
- **Not the fewest guards.** The theorem bounds the worst case over all orthogonal polygons with $n$ vertices. For one given polygon, the fewest guards can be much smaller, and computing it is [NP-hard](/minimum-guard-np-hardness/) for general polygons.

## Tightness

The bound $\lfloor n/4 \rfloor$ cannot be lowered. Take the orthogonal comb with $k$ prongs: a base $[0, 2k - 1] \times [0, 1]$ and the prongs $[2p, 2p + 1] \times [1, 4]$ for $p = 0, \dots, k - 1$, with gaps of width 1 between them. Its boundary has $n = 4k$ vertices. Let $m_p = (2p + 1/2, 4)$ be the middle of the top edge of prong $p$. A point $x$ that sees $m_p$ is in prong $p$, or the segment from $m_p$ to $x$ passes through the bottom of the prong, the segment from $(2p, 1)$ to $(2p + 1, 1)$. In the second case the segment moves at most $1/2$ sideways in its first 3 units of drop, so at most $2/3$ sideways by the time it reaches the floor $y = 0$. So every point that sees $m_p$ has $2p - 1/6 \le x \le 2p + 7/6$. These ranges are disjoint for different $p$, so no point sees two of the $m_p$, and $k = n/4$ guards are needed.

The theorem needs a polygon without holes. With holes, Theorem 1 still holds, but the dual graph of a quadrilateralization has cycles and the coloring of Lemma 2 can fail. Guards for orthogonal polygons with holes are a different problem (see [polygon with holes](/polygon-with-holes/)); O'Rourke's Chapter 5 treats the case of one hole.

## History

Victor Klee's art gallery question of 1973 was answered for general polygons by Chvátal in 1975. Kahn, Klawe and Kleitman found the orthogonal version and its proof in 1980, and published it in 1983 under the title "Traditional galleries require fewer watchmen", where a traditional gallery is one with walls at right angles. O'Rourke gave the second proof by L-shaped pieces in 1983. Sack (1984) and Lubiw (1985) gave fast algorithms for the quadrilateralization. O'Rourke's 1987 book collects these proofs and algorithms in Chapter 2, and remarks that, as with Chvátal and Fisk, the first proof was later eclipsed by simpler ones but keeps its own interest, because of the quadrilateralization theorem.

## References
