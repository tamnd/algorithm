---
tag: AJZG8R
kind: problem
slug: tree-center
name: Tree center
aliases:
- center of a tree
area: graphs/tree-algorithms
level: intro
summary: Find the node or nodes of minimum eccentricity in a tree.
prereqs: [tree, eccentricity, tree-diameter]
see_also: [tree-center-leaf-peeling, tree-diameter-double-sweep, centroid, rerooting-technique, tree-isomorphism, ahu-algorithm, free-tree-properties, k-median-problem]
sources:
  - paper: Camille Jordan, Sur les assemblages de lignes, Journal für die reine und angewandte Mathematik 70, 185 to 190 (1869)
    locator: the theorem that the centre of a tree is one vertex or two adjacent vertices, and the centroid result in the same paper
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 2.1 (Basic properties of trees, distance in trees, the definitions of eccentricity, radius and centre, and Jordan's theorem on the centre of a tree)
  - paper: S. L. Hakimi, Optimum locations of switching centers and the absolute centers and medians of a graph, Operations Research 12(3), 450 to 459 (1964)
    locator: the absolute centre, a point on an edge that minimizes the largest distance, and the vertex median
---

The tree center problem asks for the vertices of a [tree](/tree/) whose [eccentricity](/eccentricity/), the largest distance to another vertex, is the smallest. Jordan proved in 1869 that the centre of a tree is always one vertex or two adjacent vertices, and it is the middle of every longest path, so the problem is closely tied to the [tree diameter](/tree-diameter/). It takes $\Theta(n)$ time, by [peeling leaves](/tree-center-leaf-peeling/) or by finding a diametral path with a [double sweep](/tree-diameter-double-sweep/) and taking its middle. The centre gives a canonical root for a free tree, which [tree isomorphism](/tree-isomorphism/) tests use.

## In plain words

Towns are joined by roads that form a tree. You want to build a fire station in a town so that the farthest town is as close as possible. For each town, look at its worst trip, the trip to the town farthest from it. The best towns for the station are those with the shortest worst trip. They form the centre.

In a tree, the centre is always one town, or two towns next to each other. It sits in the middle of the longest route of the network: if that route has an even number of roads, the centre is its middle town; if odd, the centre is the two towns at the middle road.

## Definition

**Input.** A free tree $T = (V, E)$ with $n \ge 1$ vertices, numbered $0, \ldots, n-1$, given as a list of $n - 1$ edges. The tree is not rooted. In the main version it is not weighted, and $d(u, v)$ is the number of edges of the path from $u$ to $v$.

**Quantities.** The *eccentricity* is $\mathrm{ecc}(v) = \max_{u \in V} d(v, u)$. The *radius* is $\mathrm{rad}(T) = \min_{v} \mathrm{ecc}(v)$, and the *diameter* is $D(T) = \max_v \mathrm{ecc}(v)$.

**Output.** The *centre* $Z(T) = \{ v \in V : \mathrm{ecc}(v) = \mathrm{rad}(T) \}$, and usually the radius too.

**Jordan's theorem.** For every tree, $Z(T)$ is a single vertex or two adjacent vertices. More exactly, if $P = (p_0, \ldots, p_D)$ is any diametral path, then $Z(T) = \{p_{D/2}\}$ and $\mathrm{rad} = D/2$ when $D$ is even, and $Z(T) = \{p_{(D-1)/2}, p_{(D+1)/2}\}$ and $\mathrm{rad} = (D+1)/2$ when $D$ is odd. So $\mathrm{rad}(T) = \lceil D(T)/2 \rceil$.

*Proof.* Let $a = p_0$ and $b = p_D$. For $w \ge 0$, each vertex $v$ has $\mathrm{ecc}(v) = \max(d(v, a), d(v, b))$ (proved on the [double sweep](/tree-diameter-double-sweep/) page). For $v = p_i$ on $P$, this is $\max(i, D - i)$, which is smallest, equal to $\lceil D/2 \rceil$, exactly at $i = D/2$ when $D$ is even and at $i = (D \pm 1)/2$ when $D$ is odd. For $v$ off $P$, let $p_i$ be the vertex of $P$ nearest to $v$, at distance $h \ge 1$. Then $d(v, a) = h + i$ and $d(v, b) = h + D - i$, so $\mathrm{ecc}(v) = h + \max(i, D - i) > \lceil D/2 \rceil$. So the vertices of minimum eccentricity are exactly the middle vertices of $P$. $\square$

## Variants

- **Weighted trees, vertex centre.** With positive edge lengths, the same proof shows that the vertex centre is one vertex or two adjacent vertices of a diametral path, the ones nearest to its midpoint. With some lengths equal to $0$ the centre can be larger, since vertices joined by edges of length $0$ have the same eccentricity.
- **Absolute centre.** Allow the facility at any point of an edge. In a tree with non-negative lengths, the absolute centre is the midpoint of each diametral path, at distance $D/2$ from both ends. Hakimi introduced absolute centres for general graphs.
- **Median.** Minimize the sum of the distances, not the largest one. In a tree with unit vertex weights, the median vertices are the [centroid](/centroid/) vertices, which can differ from the centre.
- **$k$-centre.** Place $k$ facilities so that the largest distance from a vertex to its nearest facility is smallest. On trees it is solvable in polynomial time; on general graphs it is NP-hard.
- **Centre of a general graph.** The same definition applies, but the centre can be any set of vertices, and computing it needs the eccentricities, for example from [all-pairs shortest paths](/all-pairs-shortest-paths/).

## Examples

| tree | $n$ | $D$ | radius | centre |
|---|---|---|---|---|
| single vertex | 1 | 0 | 0 | $\{0\}$ |
| one edge | 2 | 1 | 1 | $\{0, 1\}$ |
| path $0, \ldots, n-1$, $n$ odd | $n$ | $n - 1$ | $(n-1)/2$ | $\{(n-1)/2\}$ |
| path $0, \ldots, n-1$, $n$ even | $n$ | $n - 1$ | $n/2$ | $\{n/2 - 1, n/2\}$ |
| star, centre $0$, $n \ge 3$ | $n$ | 2 | 1 | $\{0\}$ |
| edges $01, 02, 13, 14, 25, 46, 47$ | 8 | 5 | 3 | $\{0, 1\}$ |

In the last tree the eccentricities of $0, \ldots, 7$ are $3, 3, 4, 4, 4, 5, 5, 5$. The diametral path $6, 4, 1, 0, 2, 5$ has $D = 5$, and its two middle vertices are $1$ and $0$. The [centroid](/centroid/) of this tree is $\{1\}$: removing $1$ leaves parts of sizes $1, 3, 3$, while removing $0$ leaves a part of size $5$. So the centre and the centroid differ.

## Known algorithms

| algorithm | time | idea |
|---|---|---|
| [Leaf peeling](/tree-center-leaf-peeling/) | $\Theta(n)$ | delete all leaves in rounds; the last one or two vertices are the centre |
| [Double sweep](/tree-diameter-double-sweep/) and the middle of the path | $\Theta(n)$ | find a diametral path, take its middle vertex or vertices |
| [Rerooting](/rerooting-technique/) | $\Theta(n)$ | compute every eccentricity with one up and one down pass |
| A search from each vertex | $\Theta(n^2)$ | compute each eccentricity directly |

## Bounds

The problem takes $\Theta(n)$ time in the [word RAM](/word-ram/) model. The upper bound comes from the algorithms above. For the lower bound, take the path $0, 1, \ldots, k$ with $k \ge 2$, and $m$ more edges, each from a new vertex to $0$ or to $k$. If all new vertices hang at $0$, then $D = k + 1$; if at least one hangs at $k$ and at least one at $0$, then $D = k + 2$, and the middle of the diametral path moves. An adversary answers that each edge the algorithm reads hangs at $0$. Until the algorithm has read all $m$ of them, the last one can still hang at $k$, which changes the centre. So it must read $\Omega(n)$ entries of the input. The output has at most two vertices.

## Reductions

- **Centre from diameter.** By Jordan's theorem, a diametral path gives the centre in $O(n)$ extra time, so the centre reduces to the [diameter](/tree-diameter/).
- **Diameter from centre.** Leaf peeling counts $k$ rounds and ends with $c \in \{1, 2\}$ vertices. Then $D = 2k$ if $c = 1$ and $D = 2k + 1$ if $c = 2$. So the diameter length reduces to the peeling.
- **Rooting for isomorphism.** Two free trees are isomorphic if and only if, for some choice of a centre vertex in each, the two rooted trees are isomorphic. Since there are at most two centres, the free-tree isomorphism test reduces to at most two rooted tests, as in the [AHU algorithm](/ahu-algorithm/).

## Applications

- **Facility location.** Place a server, a fire station or a hub on a tree network so that the worst distance is smallest.
- **Minimum height rooting.** Rooting a tree at a centre vertex gives the smallest possible height, which is the radius. This helps algorithms whose cost grows with the height.
- **Canonical forms.** [Tree isomorphism](/tree-isomorphism/), tree hashing and the counting of unlabelled free trees root each tree at its centre, with a special rule for a bicentre.
- **Broadcast.** A message sent from a centre vertex reaches all vertices of a tree network in $\mathrm{rad}(T)$ rounds, the least possible from one source.

## References
