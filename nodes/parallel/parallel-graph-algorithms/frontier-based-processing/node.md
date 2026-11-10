---
tag: P1N9CM
kind: concept
slug: frontier-based-processing
name: Frontier-based graph processing
aliases:
- frontier
- vertex subset
- edgeMap and vertexMap
area: parallel/parallel-graph-algorithms
level: core
summary: Parallel graph algorithms advance a set of active vertices (the frontier) one round at a time.
prereqs: [work-span-model, parallel-pack, all-prefix-sums, compressed-sparse-row]
see_also: [parallel-bfs, direction-optimizing-bfs, delta-stepping, bellman-ford, connected-components, pregel-model, gas-model, graph-contraction]
sources:
  - paper: doi:10.1145/2442516.2442530
    title: Julian Shun and Guy E. Blelloch, Ligra, a lightweight graph processing framework for shared memory, PPoPP 2013
    locator: the vertexSubset type, the edgeMap and vertexMap operators, the sparse and dense forms of edgeMap with the threshold m/20, and the applications; section numbers to be checked
  - paper: doi:10.5555/2388996.2389013
    title: Scott Beamer, Krste Asanović and David Patterson, Direction-optimizing breadth-first search, SC 2012, Article 12
    locator: Sections IV and V (the bottom-up step and the switch between the two directions)
  - url: https://sites.google.com/site/alphalambdabook/
    title: Umut A. Acar and Guy E. Blelloch, Algorithms, Parallel and Sequential, draft book for Carnegie Mellon course 15-210
    locator: part Graph Search (frontiers in parallel BFS and their cost); chapter numbers differ between drafts
---

Frontier-based processing is a way to write parallel graph algorithms as a sequence of rounds, each of which works only on a set of active vertices called the frontier. A round applies an update to the edges that leave the frontier, in parallel, and the vertices whose state changed form the next frontier. The cost of a round is in proportion to the frontier and its edges, not to the whole graph, so the total work is the sum of the frontier sizes. [Parallel BFS](/parallel-bfs/), [Δ-stepping](/delta-stepping/) and label propagation for [connected components](/connected-components/) all have this form, and the Ligra framework of Shun and Blelloch (2013) is built on it.

## In plain words

Many graph algorithms touch only a few vertices at a time. A search touches the vertices that it reached last. A shortest path method touches the vertices whose distance just went down. All other vertices wait.

Frontier-based processing makes this the main structure of the program. Keep a set of the vertices that are active now. In one round, look at all the edges out of the active vertices at the same time, update their other ends, and collect the vertices that changed. Those become the active set of the next round. Stop when the set is empty.

The set can be stored in two ways: as a short list of names, or as one yes or no flag for every vertex. A short list is cheap when few vertices are active. The flags are better when most are, and a good framework picks the form in each round.

## The idea

Notation: $G = (V, E)$ has $n$ vertices and $m$ edges, stored as [compressed adjacency lists](/compressed-sparse-row/). A frontier is a set $U \subseteq V$, and $m_U = \sum_{u \in U} \deg(u)$ is the number of edges out of $U$. $W$ is the work and $S$ the span. The model is the [work-span model](/work-span-model/) with an atomic compare-and-swap on one memory cell; the bounds below are proved here for that model.

A frontier program uses two operators, in the names of Ligra:

- $\mathrm{vertexMap}(U, f)$ applies $f$ to each $u \in U$ in parallel and returns $\{u \in U : f(u)\}$.
- $\mathrm{edgeMap}(G, U, F, C)$ applies $F(u, v)$ to each edge $(u, v)$ with $u \in U$ and $C(v)$ true, in parallel, and returns the set of $v$ for which some call $F(u, v)$ returned true.

The update $F$ must be safe when many edges with the same head $v$ run at the same time. It uses an atomic operation (a compare-and-swap, or a write-min) and returns true for at most one of the concurrent calls on $v$ when the output must hold $v$ once. The condition $C$ lets the code skip heads that are done, such as visited vertices in BFS.

A program is a loop:

$$U_0 = \text{start set}, \qquad U_{r+1} = \mathrm{edgeMap}(G, U_r, F, C), \qquad \text{stop when } U_r = \emptyset.$$

**The sparse form.** $U$ is a list. edgeMap gives each edge out of $U$ a slot by a [prefix sum](/all-prefix-sums/) of the degrees, runs $F$ on each slot, and [packs](/parallel-pack/) the heads that returned true. This costs $O(|U| + m_U)$ work and $O(\log n)$ span.

**The dense form.** $U$ is a bitmap of $n$ flags. For each $v$ with $C(v)$ true, in parallel, edgeMap scans the in-edges $(u, v)$ and runs $F(u, v)$ for those with $u \in U$; it can stop the scan as soon as $C(v)$ turns false. This costs $O(n + m)$ work in the worst case, but it needs no atomic operation, since each $v$ is written by one task only. With a sequential scan its span is $O(\log n + \Delta)$, where $\Delta$ is the largest in-degree.

**The switch.** Ligra uses the dense form when $|U| + m_U > m/20$ and the sparse form otherwise; a conversion between a list and a bitmap costs $O(n)$ work and $O(\log n)$ span. This is the rule of [direction-optimizing BFS](/direction-optimizing-bfs/) in general form. With the sparse form in every round, a program with $R$ rounds costs

$$W = O\Big(\sum_{r} (|U_r| + m_{U_r})\Big), \qquad S = O(R \log n).$$

So the work is small when each vertex is active in few rounds, and the span is small when there are few rounds.

## Examples

**BFS.** $U_0 = \{s\}$. The update $F(u, v)$ is a compare-and-swap of $parent[v]$ from $nil$ to $u$, and $C(v)$ is "$parent[v] = nil$". Each vertex enters one frontier, so $\sum_r (|U_r| + m_{U_r}) \le n + m$ for a directed graph, and the number of rounds is the number of levels. See [parallel BFS](/parallel-bfs/).

**Label propagation for connected components.** Each vertex starts with $label[v] = v$, and $U_0 = V$. The update is a write-min of $label[u]$ into $label[v]$; it returns true when $label[v]$ goes down. The graph has 7 vertices and the undirected edges $\{3,1\}$, $\{1,0\}$, $\{0,2\}$, $\{5,6\}$, $\{6,4\}$, that is, the paths 3, 1, 0, 2 and 5, 6, 4.

| round | frontier $U$ | edge slots $m_U$ | labels after the round | changed |
|---|---|---|---|---|
| 1 | [0, 1, 2, 3, 4, 5, 6] | 10 | [0, 0, 0, 1, 4, 5, 4] | [1, 2, 3, 6] |
| 2 | [1, 2, 3, 6] | 6 | [0, 0, 0, 0, 4, 4, 4] | [3, 5] |
| 3 | [3, 5] | 2 | [0, 0, 0, 0, 4, 4, 4] | [] |

The rounds look at $10 + 6 + 2 = 18$ edge slots, against $3 \times 10 = 30$ if every round looked at the whole graph. The labels are the least vertex of each component. The number of rounds can be as large as the diameter plus one, so on a long path this is slow; [Shiloach-Vishkin](/shiloach-vishkin/) and [graph contraction](/graph-contraction/) avoid that.

**Bellman-Ford with a frontier.** $U_0 = \{s\}$. The update is a write-min of $dist[u] + w(u, v)$ into $dist[v]$, and $U_{r+1}$ is the set of vertices whose distance went down in round $r$. This is [Bellman-Ford](/bellman-ford/) that skips the vertices that did not change. [Δ-stepping](/delta-stepping/) groups the frontier by distance into buckets to cut the number of updates that are later undone.

**Non-example.** [Luby's MIS algorithm](/luby-mis/) works in rounds on a shrinking set of live vertices, but a round must look at all the edges among the live vertices, not only at the edges out of the vertices that changed. It is a round-based algorithm whose active set is the whole remaining graph, so the frontier gives no saving there.

## Where it is used

- **Shared-memory graph frameworks.** Ligra (Shun and Blelloch, 2013) has the vertexSubset type and the edgeMap and vertexMap operators, with the automatic switch between the sparse and dense forms. Its paper gives BFS, betweenness centrality, graph radii, connected components, PageRank and Bellman-Ford in this style.
- **BFS on low-diameter graphs.** The bottom-up step of Beamer, Asanović and Patterson (2012) is the dense form of edgeMap with an early exit.
- **Vertex-centric models.** The [Pregel model](/pregel-model/) and the [gather-apply-scatter model](/gas-model/) also run in rounds over active vertices, but on distributed memory with messages instead of shared memory.

## References
