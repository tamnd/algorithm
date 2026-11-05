---
tag: KNMAYJ
kind: problem
slug: minimum-arborescence
name: Minimum arborescence problem
aliases:
- minimum spanning arborescence
- optimum branching
area: graphs/spanning-trees
level: advanced
summary: Find a minimum-cost spanning out-tree rooted at a given vertex in a directed graph.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs}
  time: {worst: Ω(m)}
prereqs: [arborescence, directed-graph, minimum-spanning-tree, cycle-contraction]
see_also: [edmonds-arborescence, minimum-spanning-tree, matroid-intersection, fibonacci-heap, graphic-matroid, partition-matroid, minimum-bottleneck-spanning-tree, linear-programming-problem]
sources:
  - paper: doi:10.6028/jres.071B.032
    title: "Jack Edmonds, Optimum branchings, Journal of Research of the National Bureau of Standards 71B(4) (1967), 233-240"
    locator: the whole paper (the algorithm and the integrality of the linear program)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.9, Minimum-Cost Arborescences, a Multi-Phase Greedy Algorithm
  - paper: doi:10.1002/net.3230070103
    title: "Robert E. Tarjan, Finding optimum branchings, Networks 7(1) (1977), 25-35"
    locator: the whole paper (the O(m log n) and O(n^2) implementations)
  - paper: doi:10.1007/BF02579168
    title: "Harold N. Gabow, Zvi Galil, Thomas Spencer and Robert E. Tarjan, Efficient algorithms for finding minimum spanning trees in undirected and directed graphs, Combinatorica 6(2) (1986), 109-122"
    locator: the sections on directed graphs (the O(m + n log n) algorithm)
---

The minimum arborescence problem is the directed version of the [minimum spanning tree](/minimum-spanning-tree/) problem. Given a [directed graph](/directed-graph/) with a cost on each arc and a root $r$, it asks for a spanning [arborescence](/arborescence/) rooted at $r$, a set of arcs in which every vertex other than $r$ has exactly one entering arc and every vertex is reachable from $r$, of least total cost. The greedy methods for undirected graphs fail here, because the arborescences do not form the bases of a matroid. The problem is still polynomial: the Chu-Liu/Edmonds algorithm ([Edmonds' algorithm](/edmonds-arborescence/)) solves it in $O(mn)$ time by [cycle contraction](/cycle-contraction/), Tarjan's implementation in $O(m \log n)$, and the algorithm of Gabow, Galil, Spencer and Tarjan in $O(m + n \log n)$.

## In plain words

You must send something from one source to every point of a network of one-way links, such as a message spreading from a central server. Each point must receive it over exactly one incoming link, and each link has a cost. You want the cheapest set of links that reaches every point.

For two-way links, a simple rule works: always take the cheapest link that does not close a loop. With one-way links this fails. Taking the cheapest incoming link of each point can create a loop of points that only feed each other, with no path from the source.

The fix is to treat such a loop as one big point, solve the smaller problem, and then open the loop again.

## Definition

**Input.** A directed graph $G = (V, A)$ with $n$ vertices and $m$ arcs, a root $r \in V$, and a real cost $c(a)$ on each arc. Costs may be negative and may tie. Parallel arcs are allowed; self-loops and arcs into $r$ are in no arborescence and can be dropped.

**Output.** A set $T \subseteq A$ such that each $v \ne r$ has exactly one arc of $T$ entering it, no arc of $T$ enters $r$, and $T$ has no cycle, so that every vertex is reachable from $r$ along $T$, with least total cost $c(T) = \sum_{a \in T} c(a)$.

**Existence.** A spanning arborescence rooted at $r$ exists if and only if every vertex is reachable from $r$ in $G$, which a [breadth-first search](/breadth-first-search/) checks in $O(n + m)$ time. If not, there is no solution, and the usual output is a report of the unreachable vertices.

**Ties and negative costs.** All arborescences have exactly $n - 1$ arcs, so adding a constant to every cost does not change which arborescences are optimal; negative costs need no special care. With ties, several arborescences can be optimal.

**Why greedy fails.** The arborescences rooted at $r$ are the common bases of two matroids, the [graphic matroid](/graphic-matroid/) of the underlying undirected graph and the [partition matroid](/partition-matroid/) that allows one arc into each vertex. They are not the bases of a single matroid, and the simple greedy algorithm is not correct:

- Growing a tree from $r$ like Prim's algorithm fails. With the arcs $ra = 2$, $rb = 3$ and $ba = 1$, it takes $ra$ and then $rb$, of total cost 5, while $\{rb, ba\}$ costs 4.
- Taking the cheapest entering arc of each vertex can form a cycle that the root does not reach.

## Variants

- **Minimum branching.** A *branching* is a set of arcs with at most one arc into each vertex and no cycle, a forest of arborescences. The minimum cost branching is the empty set when costs are positive, so the interesting forms are the *maximum* weight branching, which Edmonds' paper solves, and the minimum arborescence with any root, solved by adding a new root with an arc of a large equal cost to each vertex.
- **In-arborescences.** All vertices must reach $r$; reverse every arc.
- **Maximum arborescence.** Negate the costs.
- **Bottleneck version.** Minimize the costliest arc; a threshold test with reachability solves it, as for the [minimum bottleneck spanning tree](/minimum-bottleneck-spanning-tree/).
- **Packing.** Edmonds' branching theorem: there are $k$ arc-disjoint spanning arborescences rooted at $r$ if and only if every set $S$ with $r \notin S$ has at least $k$ entering arcs.
- **Degree or depth constraints.** Bounds on out-degrees or on the depth make the problem NP-hard, as in the undirected case.

## Examples

**A graph with four vertices.** Take the root $r$, the vertices $a, b, c$ and the arcs $ra = 5$, $rb = 6$, $ab = 1$, $ba = 2$, $ac = 4$, $bc = 3$, $rc = 10$. Each non-root vertex chooses one entering arc:

| arc into $a$ | arc into $b$ | arc into $c$ | arborescence? | cost |
|---|---|---|---|---|
| $ra = 5$ | $ab = 1$ | $bc = 3$ | yes | **9** |
| $ra = 5$ | $ab = 1$ | $ac = 4$ | yes | 10 |
| $ba = 2$ | $rb = 6$ | $bc = 3$ | yes | 11 |
| $ba = 2$ | $ab = 1$ | $bc = 3$ | no: $a$ and $b$ form a cycle | |

The cheapest entering arcs, $ba$, $ab$ and $bc$, form the cycle $a, b$, which shows why the problem needs more than a local choice. The optimum is $\{ra, ab, bc\}$ of cost 9; the page on [cycle contraction](/cycle-contraction/) traces how Edmonds' algorithm finds it.

**The undirected minimum spanning tree is not the answer.** In the example above, the minimum spanning tree of the underlying undirected graph is $\{ab, bc, ra\}$, which happens to be right, but in the three-arc example $ra = 2$, $rb = 3$, $ba = 1$ it is $\{ba, ra\}$, of cost 3, and it is not an arborescence: $ba$ and $ra$ both enter $a$.

## Known algorithms

| algorithm | time | idea |
|---|---|---|
| [Chu-Liu/Edmonds](/edmonds-arborescence/) | $O(mn)$ | pick the cheapest arc into each vertex, contract a cycle with reduced costs, recurse |
| Tarjan (1977) | $O(m \log n)$, or $O(n^2)$ for dense graphs | the same contractions with mergeable heaps of entering arcs and a [disjoint-set](/disjoint-set/) structure |
| Gabow, Galil, Spencer and Tarjan (1986) | $O(m + n \log n)$ | the same with [Fibonacci heaps](/fibonacci-heap/) and a careful order of the contractions |
| general LP or matroid intersection | polynomial | the linear program below, or weighted [matroid intersection](/matroid-intersection/) |

**The linear program.** With a variable $x_a \ge 0$ for each arc, the program

$$\min \sum_a c(a) x_a \quad \text{subject to} \quad \sum_{a \text{ enters } S} x_a \ge 1 \ \text{ for each } S \subseteq V \setminus \{r\}, \ S \ne \emptyset$$

has an integral optimal solution, an arborescence, when the costs are non-negative (Edmonds, 1967). The reduced costs of Edmonds' algorithm are a dual solution that proves optimality.

## Bounds

- **Upper bound.** $O(m + n \log n)$ deterministic time.
- **Lower bound.** $\Omega(m)$. In the complete directed graph on $n \ge 3$ vertices, each arc $u \to v$ with $v \ne r$ is in some arborescence and is avoided by another. If an algorithm never reads the cost of such an arc, the adversary makes it very cheap when the output omits it, and very costly when the output contains it; either way the output is not optimal. So all $m - (n - 1)$ arcs that do not enter $r$ must be read.
- **Open.** Whether a deterministic $O(m)$ algorithm exists is open, as for undirected minimum spanning trees.

## Reductions

- **To the undirected MST.** For a symmetric graph, in which each edge appears as two opposite arcs of equal cost, a minimum arborescence rooted at any $r$ is a minimum spanning tree with its edges directed away from $r$.
- **Matroid intersection.** As above, arborescences rooted at $r$ are the common bases of a graphic matroid and a partition matroid.
- **Any root.** Add a new vertex $s$ with an arc $s \to v$ of cost $M$ to each $v$, where $M$ exceeds the sum of all absolute costs. An optimal arborescence rooted at $s$ uses exactly one arc out of $s$, if some vertex reaches all others, and its other arcs form an optimal arborescence of $G$ with the best root.

## Applications

- **Broadcast and multicast.** The cheapest set of one-way links that reaches every node from a source.
- **Dependency parsing.** In natural language processing, the best dependency tree of a sentence, under arc scores from a model, is a maximum arborescence of a dense graph on the words, found by Chu-Liu/Edmonds.
- **Phylogenetics and data compression.** Optimum branchings choose, for each object, one parent from which it can be described most cheaply, for example to encode a set of similar files as differences.
- **Taxonomies and hierarchies.** The best tree-shaped hierarchy under pairwise scores between items.

## References
