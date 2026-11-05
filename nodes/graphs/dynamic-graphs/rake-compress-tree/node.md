---
tag: 0SFSXB
kind: data-structure
slug: rake-compress-tree
name: Rake-compress tree
aliases:
- RC-tree
- rake and compress tree
area: graphs/dynamic-graphs
level: research
summary: Dynamic tree contraction structure built from rake and compress operations.
implements: [dynamic-tree]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {expected: O(log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [tree-contraction, dynamic-tree, tree]
see_also: [top-tree, link-cut-tree, euler-tour-tree, dynamic-tree-path-queries, randomized-algorithm, independent-set, list-ranking, monoid]
sources:
  - paper: "Umut A. Acar, Guy E. Blelloch, Robert Harper, Jorge L. Vittes and Shan Leung Maverick Woo, Dynamizing static algorithms, with applications to dynamic trees and history independence, Proceedings of the 15th ACM-SIAM Symposium on Discrete Algorithms (SODA 2004), 531 to 540"
    locator: the sections on tree contraction and RC-trees (randomized rake and compress rounds, the clusters and their tree, O(log n) expected time per link or cut by change propagation on trees of bounded degree)
  - paper: "Umut A. Acar, Guy E. Blelloch and Jorge L. Vittes, An experimental analysis of change propagation in dynamic trees, Proceedings of the 7th Workshop on Algorithm Engineering and Experiments (ALENEX 2005), 41 to 54"
    locator: the description of RC-trees, their queries (path, subtree, nearest marked vertex) and the experiments against link-cut trees and Euler tour trees
  - paper: "Gary L. Miller and John H. Reif, Parallel tree contraction and its application, Proceedings of the 26th IEEE Symposium on Foundations of Computer Science (FOCS 1985), 478 to 489"
    locator: the rake and compress operations and the O(log n) expected number of rounds of randomized contraction
---

A rake-compress tree, or RC-tree, represents a forest by a run of randomized [tree contraction](/tree-contraction/) and records that run as a tree of clusters. In each round, every leaf is raked into its neighbor and an independent set of vertices of degree two is compressed, so that their two edges become one; each removed vertex becomes a cluster that holds the clusters merged at it, together with a summary value such as a path weight. The contraction ends after $O(\log n)$ rounds in expectation, so the cluster tree has expected depth $O(\log n)$, and path and connectivity queries walk up this tree. A link or a cut changes the run of the contraction in only $O(\log n)$ expected places on trees of bounded degree, and change propagation repairs them in $O(\log n)$ expected time; the structure is fully dynamic, randomized, and its bounds are expected bounds against an oblivious adversary. Acar, Blelloch, Harper, Vittes and Woo introduced it in 2004.

## In plain words

Take a tree drawn on paper and shrink it step by step. In each step, every leaf folds into its only neighbor, and some vertices that sit in the middle of a chain are removed and their two edges are joined into one longer edge. A coin flip picks those middle vertices so that two neighbors never vanish in the same step.

Each step removes a fair share of the vertices, so few steps are needed. Write down, for each removed vertex, what it swallowed: the leaves that folded into it and the edges it joined. These notes form a new tree, short and wide, that remembers the whole shrinking.

To find the length of the path between two vertices, climb this short tree from both of them and add up the lengths stored on the way. A small change to the tree changes only a few notes.

## The abstract type

The structure keeps a forest on the vertices $0, \ldots, n - 1$ with a weight on each edge, and supports:

- **link**$(u, v, w)$: add the edge $\{u, v\}$ with weight $w$, if $u$ and $v$ are in different trees;
- **cut**$(u, v)$: remove the edge $\{u, v\}$;
- **connected**$(u, v)$: whether $u$ and $v$ are in one tree;
- **path weight**$(u, v)$: the sum of the weights on the tree path from $u$ to $v$.

The weights may come from any [monoid](/monoid/), and the clusters can also hold subtree sums or other values; this page uses sums of integers. This is the [dynamic tree](/dynamic-tree/) interface of [link-cut trees](/link-cut-tree/) and [top trees](/top-tree/).

## Representation

A **cluster** is a set of edges of the forest that is connected, together with its **boundary**: the vertices of the cluster that also touch edges outside it, or the vertex it hangs on. Every cluster has at most two boundary vertices. A cluster with two boundary vertices is **binary** and stores the weight of the path between them; a cluster with one is **unary**; a cluster with none is a whole tree.

The contraction works on a forest whose edges are binary clusters. At the start, each edge $\{a, b\}$ is a **base cluster** with boundary $\{a, b\}$ and its own weight. Each round looks at every live vertex $v$:

- **finalize**: if $v$ has no live edge, it becomes a cluster with no boundary, the root of the cluster tree of its component;
- **rake**: if $v$ has one live edge, to $u$, it is raked into $u$, unless $u$ is also a leaf and $u < v$; the new cluster $C(v)$ is unary with boundary $\{u\}$;
- **compress**: if $v$ has two live edges, to $a$ and $b$, neither of which is a leaf, its coin for this round is heads and the coins of $a$ and $b$ are tails, then $v$ is compressed; the new cluster $C(v)$ is binary with boundary $\{a, b\}$ and weight equal to the sum of the weights of its two binary children, and it becomes the live edge between $a$ and $b$.

The children of $C(v)$ are the binary clusters at $v$ and all unary clusters raked into $v$ before. The **RC-tree** is the tree of these clusters. Every vertex owns exactly one cluster, so the RC-tree has $n$ inner nodes and $m$ base clusters at its leaves.

The coins are a fixed hash of the vertex, the round and a seed, so the RC-tree depends only on the forest and the seed and not on the order of the updates. This is the **history independence** of the structure.

```pseudo id=main
BUILD
L1  make a base cluster for each edge; all vertices are live
L2  while some vertex is live: start a new round
L3      each live v with no live edge: finalize C(v)
L4      each live leaf v with neighbor u, unless u is a leaf with u < v: choose v to rake
L5      each live v of degree 2 with coin heads, neighbor coins tails, no leaf neighbor: choose v to compress
L6      rake each chosen leaf v: C(v) ← unary with boundary {u}, children the edge and the unary clusters at v
L7      compress each chosen v: C(v) ← binary with boundary {a, b}, weight w(a, v) + w(v, b); it becomes the edge {a, b}

CONNECTED(u, v)
L8  return the root above C(u) is the root above C(v)

PATH-WEIGHT(u, v)
L9  climb from C(u) to the root, keeping the distance from u to the vertex and to the boundary of each cluster
L10 climb from C(v) to the first cluster C(z) on the path from C(u)
L11 return d(u, z) + d(z, v)
```

## Operations

**Link and cut.** The forest changes by one edge, and the contraction is run again. In the original structure, the run is not repeated: change propagation replays only the rake and compress decisions whose inputs changed. A decision at $v$ in round $i$ depends only on the live neighbors of $v$ in round $i$ and on their degrees, so one edge change affects $O(1)$ decisions in each round in expectation, and $O(\log n)$ in total. The implementation on this page rebuilds the whole contraction after each update, in $O(n)$ expected time; it keeps the same clusters and the same queries, and it shows the structure, not the update bound.

**Connected.** Two vertices are in one tree when the walks up from their clusters end at the same root, in $O(\text{depth})$ time.

**Path weight.** The walk up from $C(u)$ keeps the distance from $u$ to the vertex $z$ of the current cluster $C(z)$ and to each of its boundary vertices. At the start, $u$ is at distance 0 from itself and at the weight of a binary child from the other end of that child. When the walk moves from a cluster to its parent $C(z)$, the vertex $z$ is a boundary vertex of the child, so its distance is known; a boundary vertex $x$ of $C(z)$ is either a boundary vertex of the child, with a known distance, or the other end of a binary child of $C(z)$ that meets $z$, at distance $d(u, z)$ plus that child's weight. The walk from $C(v)$ stops at the first cluster $C(z)$ also above $C(u)$, and the path from $u$ to $v$ passes through $z$.

## Example

Take the tree on 7 vertices with the edges $01$ (weight 4), $12$ (1), $23$ (7), $14$ (2), $45$ (3) and $56$ (5), with the seed 3 of the implementation.

| round | finalized | raked | compressed | live edges after the round |
|---|---|---|---|---|
| 1 | | 0 into 1, 3 into 2, 6 into 5 | 4, between 1 and 5 | $12$ (1), $15$ (5) |
| 2 | | 2 into 1, 5 into 1 | | none |
| 3 | 1 | | | none |

In round 1 the leaves 0, 3 and 6 rake. Vertex 4 has degree 2, its neighbors 1 and 5 are not leaves, and its coin is heads while theirs are tails, so it compresses, and the binary cluster $C(4)$ with boundary $\{1, 5\}$ and weight $2 + 3 = 5$ becomes a live edge. In round 2 the vertices 2 and 5 are leaves of the star around 1, and in round 3 the vertex 1 is alone. The RC-tree has the root $C(1)$ with children $C(0)$, $C(2)$ and $C(5)$; $C(2)$ holds $C(3)$ and $C(5)$ holds $C(6)$ and $C(4)$.

For the path weight from 3 to 6: from $C(3)$, the distance to its boundary 2 is 7; at $C(2)$, the boundary 1 is the other end of the base cluster $12$, so its distance is $7 + 1 = 8$. From $C(6)$, the distance to 5 is 5; at $C(5)$, the boundary 1 is the other end of $C(4)$, at $5 + 5 = 10$. The walks meet at $C(1)$, so the answer is $8 + 10 = 18$, which is $7 + 1 + 2 + 3 + 5$.

## Correctness

Call the clusters that have no parent yet **top clusters**. After every round, the top clusters partition the edges of the forest, each top cluster is connected, its only vertices shared with other top clusters are its boundary vertices, and each binary cluster holds the weight of the tree path between its two boundary vertices. A rake joins clusters that all meet at the leaf $v$; a compress joins the two binary clusters at $v$ into the path from $a$ to $b$, with the sum of their weights. Neither removes a connection between live vertices, so the components of the live forest are those of the original forest, and each component ends as one root cluster; this gives connected. For the path weight, the path from $u$ to a boundary vertex of a cluster above $C(u)$ stays in that cluster, and two children of $C(z)$ share only $z$, so a path between them passes through $z$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Rounds.** On a forest of bounded degree, each round removes a constant fraction of the live vertices in expectation, as in the analysis of randomized tree contraction by Miller and Reif. So the contraction has $O(\log n)$ rounds in expectation and with high probability, and the RC-tree has depth $O(\log n)$.
- **Queries.** Connected and path weight walk up the RC-tree, so they take $O(\log n)$ expected time.
- **Updates.** With change propagation, a link or a cut takes $O(\log n)$ expected time on trees of bounded degree. A tree of unbounded degree is first made ternary by replacing each vertex of high degree by a path of copies joined by edges of neutral weight. The implementation rebuilds in $O(n)$ expected time.
- **Space.** $\Theta(n)$ clusters, each with $O(1)$ data apart from its list of children, whose total length is $O(n)$.
- **Kind of bound.** Expected, over the coins. The coins are independent of the updates when the adversary is oblivious, which the expected bound needs. The structure is randomized; with the same seed, the RC-tree of a forest is always the same.

## Variants

- **Deterministic contraction.** The coin flips can be replaced by deterministic choices of the independent set, for example by deterministic coin tossing, at a cost in the constants.
- **Top trees.** [Top trees](/top-tree/) use the same kind of clusters with at most two boundary vertices, but are built around an exposed path, and their usual implementations are deterministic with worst-case or amortized $O(\log n)$ bounds.
- **Batch updates.** Change propagation over a batch of $k$ links and cuts can run in parallel. Acar, Anderson, Blelloch, Dhulipala and Westrick (2020) gave parallel batch-dynamic trees in this way, with $O(k \log(1 + n/k))$ expected work.
- **Other queries.** The clusters can hold subtree sums, the heaviest edge on the cluster path for [dynamic minimum spanning trees](/dynamic-minimum-spanning-tree/), the nearest marked vertex, or centers and medians of trees.

## When to use it

Use an RC-tree when a forest changes by links and cuts and the queries are aggregates over paths or subtrees that combine in a [monoid](/monoid/), especially when the updates come in batches or must run in parallel. For a sequential program with path queries only, a [link-cut tree](/link-cut-tree/) is usually simpler and faster in practice; for connectivity and subtree sums, an [Euler tour tree](/euler-tour-tree/) is simpler. The RC-tree is a good choice when history independence matters, since the structure does not reveal the order of past updates.

## Pitfalls

- **Unbounded degree.** On a star, the center gathers $n$ clusters, and a change near it touches all of them. The $O(\log n)$ update bound needs bounded degree; ternarize first.
- **Neighbors acting in the same round.** Two adjacent vertices must not both be removed in one round. Leaves next to a vertex that compresses, two leaves of a two-vertex tree, and two adjacent vertices of degree two all need a rule; here a compressing vertex needs non-leaf neighbors with tails, and in a two-vertex tree only the smaller vertex rakes.
- **Forgetting the unary children.** When a vertex compresses, the unary clusters raked into it earlier become children of its binary cluster. Dropping them loses edges for subtree queries.
- **Coins that depend on the updates.** If the coins are drawn again after each update, an adaptive adversary can see them and force long contractions; fix them as a hash of the vertex and the round.

## Implementations

## History

Miller and Reif (1985) introduced parallel tree contraction with the rake and compress operations and showed that randomized contraction takes $O(\log n)$ expected rounds. Acar, Blelloch, Harper, Vittes and Woo (2004) turned the static contraction into a dynamic structure by change propagation, the technique of self-adjusting computation, and named its record the RC-tree; they also noted its history independence. Acar, Blelloch and Vittes (2005) compared RC-trees experimentally with link-cut trees and Euler tour trees. Later work used RC-trees for parallel batch-dynamic trees and connectivity.

## References
