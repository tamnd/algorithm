---
tag: VEAQHT
kind: theorem
slug: planar-edge-bound
name: Planar edge bound
aliases:
- 3V-6 bound
area: graphs/planar-graphs
level: intro
summary: A simple planar graph with V >= 3 vertices has at most 3V - 6 edges.
prereqs: [euler-formula, planar-face]
see_also: [maximal-planar-graph, kuratowski-theorem, five-color-theorem, degeneracy, sparse-graph, crossing-lemma, outerplanar-graph, handshake-lemma]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 4.2, Plane graphs (Euler's formula and its corollary on the number of edges of a plane graph and of a plane triangulation)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 6.1, Embeddings and Euler's formula (the bound 3n - 6, the bound for triangle-free graphs and the bound for a given girth)
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 10, Planar graphs (the section on Euler's formula and its corollaries)
---

The planar edge bound says that a [simple](/simple-graph/) [planar graph](/planar-graph/) with $n \ge 3$ vertices has at most $3n - 6$ edges, with equality exactly for the [maximal planar graphs](/maximal-planar-graph/), whose faces are all triangles. A planar graph with no triangle has at most $2n - 4$ edges. Both bounds follow in a few lines from [Euler's formula](/euler-formula/), and they show that planar graphs are [sparse](/sparse-graph/): $m = O(n)$, and some vertex has degree at most 5.

## Statement

Let $G$ be a simple planar graph with $n$ vertices and $m$ edges.

**Theorem.**

1. If $n \ge 3$, then $m \le 3n - 6$.
2. If $n \ge 3$ and $G$ has no cycle of length 3, then $m \le 2n - 4$.
3. More generally, if $G$ contains a cycle and every cycle of $G$ has length at least $g \ge 3$ (the girth is $g$ or more), then $m \le \dfrac{g}{g-2}\,(n - 2)$.
4. If $n \ge 3$, then $m = 3n - 6$ if and only if $G$ is connected and in some (and then in every) planar embedding every face is bounded by a triangle.

The hypothesis "simple" matters: loops and parallel edges are not allowed. The hypothesis $n \ge 3$ matters: $K_2$ has $m = 1 > 3 \cdot 2 - 6$.

## In plain words

When you draw a graph with no crossings, each region of the drawing has at least three lines around it, if no two lines join the same pair of points and the graph has at least three points. Each line borders at most two regions. So the number of regions is at most two thirds of the number of lines. Euler's formula ties the points, lines and regions together, and the two facts together say that the lines are at most three times the points, minus six. If no three points form a triangle, each region needs four lines, and the limit drops to twice the points minus four.

## Proof

We use the face notions of the page [planar face](/planar-face/): fix a planar embedding of $G$; each face $f$ has a facial walk of length $\ell(f)$, every edge side (dart) lies on exactly one facial walk, and so

$$\sum_f \ell(f) = 2m. \tag{1}$$

**Step 1: reduce to a connected graph.** Suppose $G$ has $c \ge 2$ components. Each component is drawn somewhere in the plane; move the drawings apart so that each lies in the outer face of the others, then join a vertex of one component to a vertex of the next by a new edge in the outer face, $c - 1$ times. The result $G'$ is simple, planar, connected, has $n$ vertices and $m + c - 1 > m$ edges. So a bound $m' \le 3n - 6$ for $G'$ gives $m < 3n - 6$ for $G$. The same holds for parts 2 and 3, because the new edges are bridges and lie on no cycle. From now on $G$ is connected.

**Step 2: every face has length at least 3.** Let $G$ be connected, simple, with $n \ge 3$. A facial walk is a closed walk of the darts of $G$, and it is not empty because $m \ge n - 1 \ge 2$. A walk of length 1 is a loop, which a simple graph does not have. Suppose a walk has length 2, made of the darts $(u, v)$ and then $(v, u)$. The face successor of $(u, v)$ is $(v, w)$ where $w$ is the neighbour just before $u$ in the rotation at $v$; here $w = u$, so $u$ is the only neighbour of $v$. In the same way $v$ is the only neighbour of $u$. Then $\{u, v\}$ is a whole component, which contradicts $n \ge 3$ and connectivity. (A length-2 walk through two different parallel edges $u v$ cannot occur either, because $G$ has no parallel edges.) So $\ell(f) \ge 3$ for each face, and (1) gives $3f \le 2m$.

**Step 3: part 1.** Euler's formula for the connected plane graph $G$ gives $f = 2 - n + m$. With $3f \le 2m$:

$$3(2 - n + m) \le 2m \iff m \le 3n - 6 .$$

**Step 4: parts 2 and 3.** Let $G$ be connected and contain a cycle, and let every cycle have length at least $g$. If $G$ is not a [tree](/tree/), the facial walk of each face contains a cycle of $G$ (West, Section 6.1; Diestel, Section 4.2: the frontier of a face of a plane graph that is not a forest contains a cycle). So $\ell(f) \ge g$ and (1) gives $g f \le 2m$. Then

$$g(2 - n + m) \le 2m \iff (g - 2)\,m \le g\,(n - 2) \iff m \le \frac{g}{g - 2}(n - 2).$$

For part 2: if $G$ is a tree, then $m = n - 1 \le 2n - 4$ for $n \ge 3$. Otherwise $G$ has a cycle, every cycle has length at least 4, and part 3 with $g = 4$ gives $m \le 2(n - 2) = 2n - 4$.

**Step 5: part 4.** If $G$ is disconnected, Step 1 shows $m < 3n - 6$. If $G$ is connected, then by Steps 2 and 3, $m = 3n - 6$ holds if and only if $3f = 2m$, which by (1) and $\ell(f) \ge 3$ holds if and only if $\ell(f) = 3$ for every face. A closed walk of length 3 in a simple graph is a triangle. The count $m = 3n - 6$ does not depend on the embedding, so if one embedding has only triangular faces, every embedding does. $\blacksquare$

## Consequences

**A vertex of degree at most 5.** If $n \ge 3$, the sum of the degrees is $2m \le 6n - 12 < 6n$, so the average degree is less than 6 and some vertex has degree at most 5. For $n \le 2$ every degree is at most 1. So every simple planar graph is 5-[degenerate](/degeneracy/), which gives a greedy 6-coloring and is the base of the [five color theorem](/five-color-theorem/).

**Linear size.** $m \le 3n$, so an [adjacency list](/adjacency-list/) of a simple planar graph has $O(n)$ size, and the running times of planar algorithms are stated in $n$ alone.

**$K_5$ and $K_{3,3}$ are not planar.** $K_5$ has $10 > 3 \cdot 5 - 6 = 9$ edges. $K_{3,3}$ is bipartite, so it has no triangle, and it has $9 > 2 \cdot 6 - 4 = 8$ edges. These are the two graphs of [Kuratowski's theorem](/kuratowski-theorem/).

**The Petersen graph is not planar.** It has $n = 10$, $m = 15$ and girth 5, and part 3 allows at most $\frac{5}{3} \cdot 8 = 13.3$ edges.

**Thickness.** A graph that is the union of $t$ planar graphs has $m \le t(3n - 6)$. So $K_n$ needs at least $\lceil n(n-1) / (6n - 12) \rceil$ planar layers; for $K_9$ this is $\lceil 72/42 \rceil = 2$.

**Bipartite planar graphs** have $m \le 2n - 4$, so some vertex has degree at most 3.

**[Outerplanar graphs](/outerplanar-graph/)** have $m \le 2n - 3$: add one new vertex in the outer face, joined to all $n$ vertices, to get a planar graph with $n + 1$ vertices and $m + n$ edges, so $m + n \le 3(n + 1) - 6$.

**The [crossing lemma](/crossing-lemma/)** starts from the bound: a drawing of $G$ with $\mathrm{cr}$ crossings becomes planar after deleting one edge per crossing, so $\mathrm{cr}(G) \ge m - 3n + 6$ for $n \ge 3$.

## Tightness

| graph | $n$ | $m$ | bound | tight? |
|---|---|---|---|---|
| triangle $K_3$ | 3 | 3 | $3n - 6 = 3$ | yes |
| $K_4$ | 4 | 6 | $3n - 6 = 6$ | yes |
| $K_5 - e$ | 5 | 9 | $3n - 6 = 9$ | yes |
| the octahedron | 6 | 12 | $3n - 6 = 12$ | yes |
| the icosahedron | 12 | 30 | $3n - 6 = 30$ | yes |
| $K_{2, n-2}$ | $n$ | $2n - 4$ | $2n - 4$ | yes, part 2 |
| the cube $Q_3$ | 8 | 12 | $2n - 4 = 12$ | yes, part 2 |
| the dodecahedron (girth 5) | 20 | 30 | $\frac{5}{3} \cdot 18 = 30$ | yes, part 3 |
| a tree | $n$ | $n - 1$ | $3n - 6$ | no, for $n \ge 3$ |

For every $n \ge 3$ a graph with exactly $3n - 6$ edges exists: take a path $p_1, \ldots, p_{n-2}$, add a vertex $a$ above it and a vertex $b$ below it, join both to every $p_i$, and join $a$ to $b$ around the end $p_1$. This has $(n - 3) + 2(n - 2) + 1 = 3n - 6$ edges, and all its faces are triangles.

**The bound is not sufficient for planarity.** $K_{3,3}$ together with 3 isolated vertices has $n = 9$ and $m = 9 \le 21$, but it is not planar. The bound only shows non-planarity when it fails.

**Multigraphs.** Two vertices joined by $k$ parallel edges form a planar multigraph with $m = k$, for any $k$. For loopless multigraphs with no face of length 2 the proof still works, but for general multigraphs no bound in $n$ holds.

## History

Euler's relation between vertices, edges and faces dates from his work on polyhedra in the 1750s, and the bounds on this page are its direct corollaries. The forms used here, with the girth version and the equality case for triangulations, are standard textbook material: Diestel (Section 4.2), West (Section 6.1) and Bondy and Murty (Chapter 10) all give them with this proof.

## References
