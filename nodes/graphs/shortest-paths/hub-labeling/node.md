---
tag: AFFE5D
kind: algorithm
slug: hub-labeling
name: Hub labeling
aliases:
- 2-hop labeling
- distance labeling by hubs
area: graphs/shortest-paths
level: advanced
summary: Stores for each vertex a set of hubs and distances so that a query takes a merge of two label lists.
solves: [all-pairs-shortest-paths]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs, L: the size of the largest label}
  time: {worst: O(n m log n + n^2 L)}
  space: {extra: O(n L)}
properties: {deterministic: true, recursive: false}
prereqs: [dijkstra, all-pairs-shortest-paths, shortest-path]
see_also: [contraction-hierarchies, dijkstra, all-pairs-shortest-paths, thorup-zwick-oracle, single-pair-shortest-path, alt-algorithm, sorting-barrier, potential-function-reduced-costs]
sources:
  - paper: doi:10.1145/2463676.2465315
    title: Takuya Akiba, Yoichi Iwata and Yuichi Yoshida, Fast exact shortest-path distance queries on large networks by pruned landmark labeling, Proceedings of the ACM SIGMOD Conference, 2013, 349 to 360
    locator: Section 4, the pruned landmark labeling algorithm, its correctness proof and the minimality of the labels for a fixed order
  - paper: "Edith Cohen, Eran Halperin, Haim Kaplan and Uri Zwick, Reachability and distance queries via 2-hop labels, SIAM Journal on Computing 32(5), 1338 to 1355 (2003)"
    locator: the definition of 2-hop covers and the O(log n) approximation of the smallest labeling
  - paper: "Cyril Gavoille, David Peleg, Stephane Perennes and Ran Raz, Distance labeling in graphs, Journal of Algorithms 53(1), 85 to 112 (2004)"
    locator: the lower bounds on label size, Theta(n) bits for general graphs
  - paper: "Ittai Abraham, Daniel Delling, Andrew V. Goldberg and Renato F. Werneck, A hub-based labeling algorithm for shortest paths in road networks, Proceedings of the 10th International Symposium on Experimental Algorithms (SEA), 2011, 230 to 241"
    locator: hub labels from a contraction hierarchy order and the query times on road networks
  - paper: "Ittai Abraham, Amos Fiat, Andrew V. Goldberg and Renato F. Werneck, Highway dimension, shortest paths, and provably efficient algorithms, Proceedings of the 21st ACM-SIAM Symposium on Discrete Algorithms (SODA), 2010, 782 to 793"
    locator: the bound on label size in terms of the highway dimension
  - paper: "Ittai Abraham, Daniel Delling, Andrew V. Goldberg and Renato F. Werneck, Hierarchical hub labelings for shortest paths, Proceedings of the 20th European Symposium on Algorithms (ESA), 2012, 24 to 35"
    locator: canonical labelings for a vertex order and their minimality
---

Hub labeling answers distance queries in a graph by looking up two short lists. Each vertex $u$ gets an *out-label*, a list of pairs $(h, d(u, h))$, and an *in-label*, a list of pairs $(h, d(h, v))$; the vertices $h$ are *hubs*. The labels must have the *cover property*: for every pair $u, v$ with $v$ reachable from $u$, some hub in both labels lies on a shortest path from $u$ to $v$. Then $d(u, v)$ is the least $d(u, h) + d(h, v)$ over the common hubs, found by merging the two lists. This page builds the labels by *pruned landmark labeling* (Akiba, Iwata and Yoshida): take the vertices in a fixed order, run [Dijkstra](/dijkstra/) from each, and prune every vertex whose distance the labels built so far already give. Weights must be nonnegative. On road networks with a good order, labels hold about a hundred hubs, and a query takes under a microsecond.

## In plain words

Before any question is asked, give every place a short list of important places nearby, with the distance to each.

To find the distance between two places, look at both lists and find the important places that appear in both. For each one, add the distance from the first place to it and from it to the second place. The smallest sum is the answer.

To build the lists, take the places from the most important to the least. From each one, search outward as usual, but stop at any place whose distance the lists can already give. Important places are handled first, so later searches stop early and the lists stay short.

## The problem

Given a directed graph $G = (V, E)$ with $n$ vertices, $m$ arcs and weights $w : E \to \mathbb{R}_{\ge 0}$, build a data structure that answers queries $(u, v)$ with the shortest-path distance $d(u, v)$, or $+\infty$ if $v$ is not reachable from $u$. This is a preprocessing version of [all-pairs shortest paths](/all-pairs-shortest-paths/): the goal is small space and fast queries, not an $n \times n$ table.

**Weight assumptions.** Weights are nonnegative real numbers; zero weights and cycles of weight 0 are allowed. Integer weights are not needed. Negative weights are not allowed, because each search is Dijkstra; the implementation rejects them, and so it rejects every [negative cycle](/negative-cycle/). For negative weights without a negative cycle, see the variant with a potential below.

## The algorithm

The vertices are taken in an order $v_1, \ldots, v_n$, most important first. A label is a list of pairs $(k, D)$ for the hub $v_k$, kept in increasing order of $k$; pairs are only ever appended with the current $k$, so the lists stay sorted with no extra work.

```pseudo id=main
HUB-LABELING(G, w, v_1, ..., v_n)
L1  for each v in V do Lout(v) ← empty list, Lin(v) ← empty list
L2  for k ← 1 to n do
L3      PRUNED-SEARCH(G, v_k, k, forward)              ▷ adds (k, d(v_k, x)) to Lin(x)
L4      PRUNED-SEARCH(reverse of G, v_k, k, backward)  ▷ adds (k, d(x, v_k)) to Lout(x)
L5  return Lout, Lin

PRUNED-SEARCH(H, h, k, dir)
L6  run Dijkstra from h in H; each time it extracts a vertex x with key D do
L7      if QUERY(h, x) ≤ D when dir = forward, or QUERY(x, h) ≤ D when dir = backward, then skip x: do not relax its arcs
L8      else append (k, D) to Lin(x) if dir = forward, to Lout(x) if backward, and relax the arcs out of x in H

QUERY(u, v)
L9  merge Lout(u) and Lin(v), which are sorted by k
L10 for each k found in both, with values a in Lout(u) and b in Lin(v), keep the least a + b
L11 return the least sum kept, or ∞ if no k is in both
```

Line L7 asks whether the hubs of earlier rounds already give a path from $h$ to $x$ that is no longer than the one this search found. If so, $x$ and everything reached only through $x$ are covered by earlier hubs, and the search does not go on through $x$. This is the pruning that keeps the labels small.

## Example

Take the arcs $C \to D$ (3), $C \to E$ (2), $D \to F$ (4), $E \to D$ (1), $E \to F$ (2), $E \to G$ (3), $F \to G$ (2), $F \to H$ (1) and $G \to H$ (2), with the order $F, E, D, G, C, H$.

**Round 1, hub $F$.** All labels are empty, so nothing is pruned. The forward search adds $F$ to $\mathrm{Lin}$ of $F$ (0), $H$ (1) and $G$ (2). The backward search adds $F$ to $\mathrm{Lout}$ of $F$ (0), $E$ (2), $C$ (4) and $D$ (4).

**Round 2, hub $E$, forward.** It extracts $E$ with key 0; $\mathrm{Lin}(E)$ is empty, so it adds $(E, 0)$. It extracts $D$ with key 1 and adds $(E, 1)$ to $\mathrm{Lin}(D)$. It extracts $F$ with key 2: $\mathrm{QUERY}(E, F) = 2 + 0 = 2 \le 2$ through the hub $F$, so $F$ is pruned and its arcs are not relaxed. It extracts $G$ with key 3: the query gives $2 + 2 = 4 > 3$, so it adds $(E, 3)$ to $\mathrm{Lin}(G)$ and relaxes $G \to H$. It extracts $H$ with key 5, which is not the true distance 3 because $F$ was pruned; the query gives $2 + 1 = 3 \le 5$, so $H$ is pruned. The backward search from $E$ adds $(E, 0)$ to $\mathrm{Lout}(E)$ and $(E, 2)$ to $\mathrm{Lout}(C)$.

**The final labels.**

| vertex | out-label $(h, d(u, h))$ | in-label $(h, d(h, u))$ |
|---|---|---|
| $C$ | $(F, 4), (E, 2), (C, 0)$ | $(C, 0)$ |
| $D$ | $(F, 4), (D, 0)$ | $(E, 1), (D, 0)$ |
| $E$ | $(F, 2), (E, 0)$ | $(E, 0)$ |
| $F$ | $(F, 0)$ | $(F, 0)$ |
| $G$ | $(G, 0)$ | $(F, 2), (E, 3), (G, 0)$ |
| $H$ | $(H, 0)$ | $(F, 1), (G, 2), (H, 0)$ |

There are 21 pairs in all, against 36 entries in a full distance table.

**Queries.** $\mathrm{QUERY}(C, H)$ merges $\mathrm{Lout}(C)$ and $\mathrm{Lin}(H)$; the only common hub is $F$, which gives $4 + 1 = 5$, the weight of $C E F H$. $\mathrm{QUERY}(D, G)$ finds $F$ with $4 + 2 = 6$. $\mathrm{QUERY}(H, C)$ finds no common hub and returns $+\infty$, and indeed $C$ is not reachable from $H$.

## Correctness

Write $S(u, v)$ for the set of vertices $x$ with $d(u, x) + d(x, v) = d(u, v)$, the vertices on shortest paths from $u$ to $v$. The full proof is in [the correctness proof](proofs/correctness.md); the main steps are these.

1. **Every stored value is an upper bound.** Each key of Dijkstra is the weight of a real path, so every pair $(k, D)$ in $\mathrm{Lin}(x)$ has $D \ge d(v_k, x)$, and the same for out-labels. So $\mathrm{QUERY}(u, v) \ge d(u, v)$ always.
2. **The cover property.** Let $v$ be reachable from $u$, and let $h = v_k$ be the vertex of $S(u, v)$ that comes first in the order. Then the forward search of round $k$ reaches every vertex of a shortest path from $h$ to $v$ with its exact distance and never prunes it: a prune would give, through an earlier hub $h'$, $d(h, h') + d(h', x) \le d(h, x)$, which puts $h'$ in $S(u, v)$ before $h$. So $(k, d(h, v)) \in \mathrm{Lin}(v)$, and in the same way $(k, d(u, h)) \in \mathrm{Lout}(u)$.
3. **Queries.** By step 2 the query finds the sum $d(u, h) + d(h, v) = d(u, v)$, and by step 1 it finds nothing smaller. If $v$ is not reachable from $u$, a common hub would give a path from $u$ to $v$, so there is none and the query returns $+\infty$.

Each round runs two Dijkstra searches, which end, so the algorithm terminates after $2n$ searches.

## Complexity

- **Preprocessing.** Each of the $2n$ searches pushes at most $m$ keys into a binary heap, $O(m \log n)$, and runs at most $n$ queries of cost $O(L)$, where $L$ is the size of the largest label. The total is $O(nm \log n + n^2 L)$, which is $O(nm \log n + n^3)$ in the worst case. With a good order, pruning stops most searches early, and the real cost is much lower.
- **Space.** $O(nL)$ for the labels, at most $O(n^2)$.
- **Query.** $O(|\mathrm{Lout}(u)| + |\mathrm{Lin}(v)|) = O(L)$ for the merge, with no access to the graph.

## Properties

- **Exact.** Queries return exact distances, not estimates.
- **Order dependent.** The label size depends strongly on the order. A random order on a road network gives huge labels; an order by degree, by betweenness or by a [contraction hierarchy](/contraction-hierarchies/) gives small ones.
- **Minimal for the order.** Akiba, Iwata and Yoshida show that pruned landmark labeling stores $v_k$ in the in-label of $x$ exactly when $v_k$ comes first in the order among the vertices of $S(v_k, x)$. This is the *canonical labeling* of the order, and no labeling that respects the order is smaller.
- **Deterministic.** The output is fixed by the graph and the order.
- **Undirected graphs.** One label per vertex suffices, and each round runs one search.

## Variants and improvements

- **Undirected and unweighted graphs.** Breadth-first search in place of Dijkstra, and bit-parallel labels for many hubs at once (Akiba et al.).
- **Hub labels from contraction hierarchies.** Abraham, Delling, Goldberg and Werneck take the upward search spaces of a contraction hierarchy as labels and prune them; on continental road networks this gives queries in well under a microsecond.
- **Highway dimension.** If a graph has highway dimension $h$, labels of size $O(h \log D)$ exist, where $D$ is the diameter (Abraham, Fiat, Goldberg and Werneck). This explains why road networks have small labels.
- **Approximately smallest labels.** Finding a labeling of least total size is NP-hard, and a greedy set-cover method gives an $O(\log n)$ approximation (Cohen, Halperin, Kaplan and Zwick).
- **Negative weights without a negative cycle.** Compute a [potential](/potential-function-reduced-costs/) $p$ by Bellman-Ford, build labels for the reduced weights $w(u, v) + p(u) - p(v) \ge 0$, and return $\mathrm{QUERY}(u, v) - p(u) + p(v)$.
- **Paths, not only distances.** Store with each label pair the next vertex toward the hub, and unpack the path from the two halves.
- **Approximate oracles.** If a bounded error is allowed, the [Thorup-Zwick oracle](/thorup-zwick-oracle/) gives $O(k n^{1 + 1/k})$ space for every graph, at the cost of stretch $2k - 1$.

## When to use it

Use hub labeling when a graph is queried very often and changes rarely, and when it has a structure that gives small labels: road networks, many social and web graphs, and graphs of small highway dimension. It has the fastest exact queries known in practice. Do not use it for a single query, where Dijkstra or [A*](/a-star-search/) is cheaper than the preprocessing; for graphs with no good order, such as expanders or random graphs, where the labels grow toward $n$; or for graphs that change often, since a change can affect many labels.

## Pitfalls

- **A bad order.** Labels can grow to $\Theta(n)$ per vertex. Always use an order that puts central vertices first.
- **Unsorted labels.** The merge in lines L9 to L11 needs both lists in the same order of hubs. Appending in round order keeps them sorted; inserting hubs in any other way does not.
- **One label in a directed graph.** A directed graph needs both an out-label and an in-label; one label per vertex gives wrong answers.
- **Pruning with the wrong test.** Pruning when the query is strictly less than $D$ is still correct but stores more pairs; pruning when it is greater, or before the vertex is extracted, can lose the cover property.
- **Negative weights.** Dijkstra is wrong with negative weights, and the labels then miss shorter paths. Reject them, or reduce them with a potential first.
- **Treating $D$ as the true distance.** A pruned search can extract a vertex with a key larger than its distance, as $H$ in the example. Such vertices are always pruned, but code that stores $D$ before the test, or reuses the keys for other purposes, gets wrong values.

## Implementations

## History

Distance labeling schemes were studied by Peleg and by Gavoille, Peleg, Perennes and Raz around 2000, who showed that general graphs need labels of $\Theta(n)$ bits for exact distances. Cohen, Halperin, Kaplan and Zwick introduced 2-hop covers in 2002, with a greedy approximation of the smallest cover. Abraham, Delling, Goldberg and Werneck made hub labels practical for road networks in 2011, building on their theory of highway dimension, and in 2012 described canonical labelings for a vertex order. Akiba, Iwata and Yoshida gave pruned landmark labeling in 2013, which builds the canonical labeling for any order directly by pruned searches and scales to large social and web graphs.

## References
