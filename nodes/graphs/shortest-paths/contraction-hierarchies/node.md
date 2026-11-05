---
tag: K2PFVE
kind: algorithm
slug: contraction-hierarchies
name: Contraction hierarchies
aliases:
- CH
area: graphs/shortest-paths
level: advanced
summary: Preprocesses a graph by contracting vertices in an importance order, enabling fast bidirectional point-to-point queries.
solves: [single-pair-shortest-path]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, M: the number of edges plus shortcuts}
  time: {worst: O(M log n), best: Θ(1)}
  space: {extra: Θ(n + M)}
properties: {deterministic: true, recursive: true}
prereqs: [bidirectional-dijkstra, dijkstra, single-pair-shortest-path]
see_also: [highway-hierarchies, hub-labeling, alt-algorithm, distance-oracle, distance-labeling, shortest-path-tree, planar-separator-theorem, treewidth]
sources:
  - paper: doi:10.1007/978-3-540-68552-4_24
    title: Robert Geisberger, Peter Sanders, Dominik Schultes and Daniel Delling, Contraction hierarchies, faster and simpler hierarchical routing in road networks, WEA 2008, LNCS 5038, 319 to 333
    locator: the whole paper (node contraction, witness searches, the edge-difference priority with lazy updates, and the bidirectional upward query)
  - paper: doi:10.1287/trsc.1110.0401
    title: Robert Geisberger, Peter Sanders, Dominik Schultes and Christian Vetter, Exact routing in large road networks using contraction hierarchies, Transportation Science 46(3), 388 to 404 (2012)
    locator: the sections on contraction, the query and its correctness, path unpacking, and the experiments
  - paper: doi:10.1007/978-3-319-49487-6_2
    title: Hannah Bast, Daniel Delling, Andrew Goldberg, Matthias Müller-Hannemann, Thomas Pajor, Peter Sanders, Dorothea Wagner and Renato F. Werneck, Route planning in transportation networks, in Algorithm Engineering, LNCS 9220, 19 to 80 (2016)
    locator: Section 2, Shortest paths in road networks, the part on hierarchical techniques (contraction hierarchies and customizable CH)
  - paper: doi:10.1137/1.9781611973075.64
    title: Ittai Abraham, Amos Fiat, Andrew V. Goldberg and Renato F. Werneck, Highway dimension, shortest paths, and provably efficient algorithms, SODA 2010, 782 to 793
    locator: the whole paper (highway dimension and query bounds for contraction hierarchies and other methods)
---

Contraction hierarchies (CH) are a speed-up technique for [point-to-point shortest paths](/single-pair-shortest-path/) on large, fixed graphs such as road networks. Preprocessing orders the vertices by importance and *contracts* them one by one, from least to most important: a vertex is removed, and a *shortcut* edge is added between two of its neighbors whenever the path through it is the only shortest one. A query runs a [bidirectional Dijkstra](/bidirectional-dijkstra/) search in which both sides only go *up* the order. For every order, the answer is exact; with a good order, the searches are tiny. On continental road networks a query scans a few hundred vertices and takes well under a millisecond, against seconds for [Dijkstra](/dijkstra/). The method is due to Geisberger, Sanders, Schultes and Delling (2008).

## In plain words

Rank all places by how important they are: a small side street at the bottom, a motorway junction at the top.

Remove places one at a time, starting with the least important. When you remove a place, look at each pair of its neighbors. If the best way between them went through the removed place, add a direct road between them with the same length, a shortcut. If some other route is just as short, no shortcut is needed.

To find a route, search from the start, but only along roads that lead to more important places. Do the same from the destination, backward. The two searches climb toward the important places and meet near the top. The best meeting point gives the answer, and the shortcuts are expanded back into real roads.

## The problem

The input is a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges and a weight $w(u, v)$ on each edge. Preprocessing builds the hierarchy once. Each query gives $s$ and $t$ and asks for $\operatorname{dist}(s, t)$ and a shortest path.

**Weight assumptions.** Weights are nonnegative real numbers; zero weights, parallel edges and self-loops are allowed (only the lightest of parallel edges matters, and self-loops are dropped). Witness searches and queries are Dijkstra searches, so a negative weight would make them wrong; the implementation rejects negative weights, which also rules out negative cycles. If $t$ is not reachable from $s$, the query returns $+\infty$ and no path.

## The algorithm

```pseudo id=main
CONTRACTION-HIERARCHY(G, w, order; query s, t)
L1  for each v in order (least important first) do
L2      for each edge (u, v) and edge (v, x) with u, x not contracted, u ≠ x do
L3          if no u-x path avoiding v in the remaining graph weighs ≤ w(u, v) + w(v, x) then
L4              add or lower the shortcut (u, x) to weight w(u, v) + w(v, x), middle v
L5      remove v; its edges to remaining vertices become upward edges (out of v) and downward edges (into v)
L6  query: d↑[s] ← 0, d↓[t] ← 0; Dijkstra from s on upward edges, from t on reversed downward edges
L7      alternate the two searches until both least keys are ≥ μ
L8      at each scanned vertex v: μ ← min(μ, d↑[v] + d↓[v]), and remember v
L9  if no vertex was remembered then return ∞
L10 return μ and the path through the remembered vertex, with each shortcut expanded through its middle
```

Line L3 is a *witness search*, a Dijkstra search from $u$ in the graph of uncontracted vertices without $v$, stopped once its least key exceeds the limit. If it finds a path of weight at most $w(u, v) + w(v, x)$, the shortcut is not needed. Real implementations stop witness searches early, after a few hundred scans or a few hops; this can only add shortcuts that are not needed, never miss one, so correctness is kept. The implementation here searches exactly.

**The order.** Correctness holds for every order; speed depends on it. The standard priority is the *edge difference*, the number of shortcuts that contracting $v$ would add minus the number of edges it removes, often combined with terms that spread contraction evenly. Priorities change as neighbors are contracted, so they are kept in a heap and recomputed lazily when a vertex reaches the top, as in the implementation.

## Example

The graph has the vertices $a, b, c, d, e$ and the edges, each in both directions, $a - b$ (1), $b - c$ (1), $c - d$ (1), $a - e$ (3), $e - d$ (1). The order is $b, e, c, a, d$.

| contract | pairs of neighbors | witness? | shortcut |
|---|---|---|---|
| $b$ | $a, c$: through $b$ weighs 2 | $a, e, d, c$ weighs 5 | $a - c$ (2), middle $b$ |
| $e$ | $a, d$: through $e$ weighs 4 | $a, c, d$ weighs 3 | none |
| $c$ | $a, d$: through $c$ weighs 3 | none left | $a - d$ (3), middle $c$ |
| $a$ | only $d$ remains | | |
| $d$ | | | |

There are two shortcuts, four directed edges. The upward edges are $b \to a$ (1), $b \to c$ (1), $e \to a$ (3), $e \to d$ (1), $c \to d$ (1), $c \to a$ (2), $a \to d$ (3).

**Query $b$ to $e$.** The forward search from $b$ climbs to $a$ (1), $c$ (1), then $d$ (2 through $c$). The backward search from $e$ climbs to $d$ (1) and $a$ (3). The meeting candidates are $a$ with $1 + 3 = 4$ and $d$ with $2 + 1 = 3$, so $\mu = 3$ through $d$, and the path is $b, c, d, e$. No search ever goes down to a less important vertex.

**Query $a$ to $d$.** The forward search uses the shortcut $a \to d$ (3) at once. Expanding it through its middle $c$ gives $a, c, d$, and expanding $a \to c$ through $b$ gives $a, b, c, d$, weight 3.

**Unreachable target.** In the graph $0 \to 1 \to 2$, $3 \to 0$, no vertex reaches 3, so for the query 0 to 3 the two upward searches never share a vertex, no meeting vertex is remembered, and line L9 returns $\infty$, for every order.

## Correctness

**Theorem.** Let all weights be nonnegative and let the hierarchy be built with any order. For all $s, t$, the query returns $\operatorname{dist}(s, t)$, and when it is finite, a walk from $s$ to $t$ of that weight in $G$ (a simple path if all weights are positive).

Let $H$ be $G$ plus all shortcuts. Each shortcut stands for a path of the same weight in $G$, so distances in $H$ equal those in $G$. The key fact is that some shortest $s$-$t$ path in $H$ is *up-down*: the ranks first rise and then fall. Take a shortest path in $H$; if an inner vertex $v$ has a lower rank than both its neighbors $u$ and $x$ on the path, then when $v$ was contracted, $u$ and $x$ were still present, so line L3 either found a witness of weight at most $w(u, v) + w(v, x)$ through higher vertices, or line L4 added a shortcut $u \to x$. Replacing $u, v, x$ by it keeps the path shortest and replaces $v$ by vertices of higher rank. This cannot go on forever, so a shortest up-down path exists. Its top vertex is reached by both upward searches, and the stopping rule of line L7 is the one of bidirectional Dijkstra. The full proof is in the proof file below.

## Complexity

The model is the [word RAM](/word-ram/), with $M$ the number of edges plus shortcuts.

- **Query, worst case.** Each side is a Dijkstra search over at most $n$ vertices and $M$ edges, $O(M \log n)$ with a binary heap, plus the expansion, linear in the length of the output path. In the worst case, the hierarchy does not help.
- **Query, best case.** When $s = t$ the query answers at once, $\Theta(1)$.
- **Preprocessing.** Each contraction runs witness searches between pairs of neighbors. In the worst case the graph fills in and $M$ is $\Theta(n^2)$, as for a bad elimination order in sparse Gaussian elimination. On road networks with the edge-difference order, $M$ is less than $2m$ and preprocessing takes minutes for a continent.
- **Space.** The ranks, the upward and downward edges and the shortcut middles take $\Theta(n + M)$.
- **Provable bounds.** Abraham, Fiat, Goldberg and Werneck (2010) showed that graphs of small *highway dimension* $h$ have orders for which a CH query takes about $O((h \log D)^2)$ time, with $D$ the diameter, which explains the speed on road networks.

## Properties

- **Exact for every order.** Order and witness limits change only speed and the number of shortcuts.
- **Upward searches only.** Each side scans only vertices of higher rank, so the search spaces are small when the order puts important vertices on top.
- **Shortcuts unpack recursively.** Each shortcut stores its middle vertex, and expansion is a recursion of depth at most $n$.
- **Graph-only.** No coordinates or geometry are needed, unlike A* with straight-line bounds.
- **Fixed weights.** Changing a weight can invalidate shortcuts or witnesses; plain CH must then be rebuilt, which is what customizable CH avoids.
- **Relation to elimination.** Contraction is vertex elimination as in sparse Gaussian elimination, with witnesses removing unneeded fill; without witnesses the number of shortcuts relates to the [treewidth](/treewidth/) of the order.

## Variants and improvements

- **Customizable CH.** Contract by a metric-independent order from nested dissection (using [separators](/planar-separator-theorem/)) with no witnesses, then fill in weights in a fast customization phase; weights can change in seconds.
- **Many-to-many and one-to-many.** Run the backward upward searches from all targets once, store buckets, and answer a whole distance table with one forward search per source (bucket-based CH).
- **Hub labels from CH.** The upward search space of each vertex, pruned, is a [hub label](/hub-labeling/); this gives the fastest known exact queries.
- **Time-dependent CH.** Weights are functions of the departure time, and shortcuts store linked functions.
- **Stall-on-demand.** During a query, a vertex whose distance is beaten by a downward edge from a scanned higher vertex is stalled, which prunes the search further.

## When to use it

Use CH for many exact point-to-point queries on a large, mostly fixed graph with a hierarchy, such as road networks, which is why it is common in route planners. Use [ALT](/alt-algorithm/) when weights increase often and memory is less tight, plain [bidirectional Dijkstra](/bidirectional-dijkstra/) for one-off queries, and [hub labeling](/hub-labeling/) when queries must be even faster and space is available. CH helps little on graphs without a hierarchy, such as random graphs or social networks, where the contraction fills in.

## Pitfalls

- **Searching down.** The query must use only upward edges on each side; letting a side go down makes it a plain bidirectional Dijkstra with extra edges, which is correct but slow.
- **Stopping at the first meeting.** As in bidirectional Dijkstra, the first vertex scanned by both sides need not be on a shortest path; stop only when both least keys reach $\mu$.
- **Witness search with strict inequality.** A witness of *equal* weight is enough; requiring a strictly shorter witness adds many unneeded shortcuts on graphs with ties, though it stays correct.
- **Witness limits that drop shortcuts.** A limit may only make the search give up and *add* the shortcut. Treating "not found within the limit" as "witness exists" is wrong.
- **Directed graphs.** The backward search runs on the reversed downward edges, edges into a vertex from a higher one. Mixing the directions gives wrong distances on one-way streets.
- **Self-loops and parallel edges.** Keep only the lightest parallel edge and drop self-loops before contraction, or the witness and shortcut tests compare the wrong weights.

## Implementations

The Python version contracts in a given order, or by edge difference with lazy updates, uses exact witness searches, stores the middle vertex of each shortcut, and answers queries with the bidirectional upward search and recursive unpacking.

## History

Hierarchical route planning goes back to highway hierarchies (Sanders and Schultes 2005), of which contraction was one ingredient. Geisberger, Sanders, Schultes and Delling (2008) showed that contraction alone, one vertex per level, is simpler and faster, and named it contraction hierarchies; the journal version with Vetter appeared in 2012. Abraham, Fiat, Goldberg and Werneck (2010) explained its speed through highway dimension. Customizable CH (Dibbelt, Strasser and Wagner) separated the order from the weights.

## References
