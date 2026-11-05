---
tag: 2F2QE8
kind: technique
slug: multi-source-bfs
name: Multi-source BFS
aliases:
- multi-source breadth-first search
area: graphs/traversal
level: intro
summary: Starts BFS from a set of sources at once to get each vertex's distance to its nearest source.
prereqs: [breadth-first-search]
see_also: [bfs-layers, bfs-tree, zero-one-bfs, dijkstra, flood-fill, implicit-graph, bidirectional-search, shortest-path-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.2, Breadth-first search (the procedure and its proof of correctness, which carry over to a queue that starts with several vertices at distance 0)
  - paper: doi:10.1016/0020-0190(88)90066-X
    title: Kurt Mehlhorn, A faster approximation algorithm for the Steiner problem in graphs, Information Processing Letters 27(3), 125 to 128 (1988)
    locator: the partition of the vertices by their nearest terminal, computed by one shortest-path search from all terminals at once
  - paper: "Martin Erwig, The graph Voronoi diagram with applications, Networks 36(3), 156 to 163 (2000)"
    locator: the definition of the graph Voronoi diagram and its computation by one search from all centres
---

Multi-source BFS is [breadth-first search](/breadth-first-search/) that starts with a whole set $S$ of sources in its queue, all at distance 0. It computes, for every vertex $v$, the distance $\delta(S, v) = \min_{s \in S} \delta(s, v)$ to the nearest source, a shortest path from that source, and which source it is, in one pass of $\Theta(n + m)$ time. This is the same as one BFS from a new *super source* joined to every vertex of $S$, so all facts about BFS carry over. Running a separate BFS from each of $k$ sources would cost $k$ times as much. The technique computes distance maps on grids, simulates things that spread from several places at once, and splits a graph into the regions of its nearest centres.

## In plain words

Light several fires in a dry field at the same moment. Each minute, every burning patch sets fire to the patches next to it. The minute when a patch catches fire is its distance to the nearest starting fire, and the fire that reached it first is its nearest one.

Multi-source BFS does exactly this. Put all the starting points in the queue at time 0. Then run ordinary BFS. The queue still handles everything at time 0 first, then everything at time 1, and so on, so each vertex is reached first by the closest starting point.

## When it applies

- The graph is unweighted, or all edges have the same length.
- The question is about the *nearest* member of a set: the distance to the nearest source, the nearest source itself, or the time when something that spreads from all sources at once reaches each vertex.
- The sources are known at the start.

For edges of different lengths, the same idea works with [Dijkstra's algorithm](/dijkstra/), and for lengths 0 and 1 with [0-1 BFS](/zero-one-bfs/).

## The template

```pseudo id=main
MULTI-SOURCE-BFS(G, S)
L1  for each vertex u ∈ V do dist[u] ← ∞, π[u] ← NIL, owner[u] ← NIL
L2  Q ← empty queue
L3  for each s ∈ S do
L4      dist[s] ← 0, owner[s] ← s, ENQUEUE(Q, s)
L5  while Q is not empty do
L6      u ← DEQUEUE(Q)
L7      for each v ∈ Adj[u] do
L8          if dist[v] = ∞ then
L9              dist[v] ← dist[u] + 1, π[v] ← u, owner[v] ← owner[u]
L10             ENQUEUE(Q, v)
L11 return dist, π, owner
```

Only lines L3 and L4 differ from BFS, and the array $\mathrm{owner}$ is optional.

**Why it is correct.** Add a new vertex $s^*$ with an edge to each source. A BFS from $s^*$ first dequeues $s^*$ and enqueues the sources in the order of line L3, all at distance 1, with parent $s^*$. From then on it does exactly what lines L5 to L10 do, with every distance one larger. By the correctness of BFS, it finds $\delta(s^*, v)$, and $\delta(s^*, v) = 1 + \delta(S, v)$, because a shortest path from $s^*$ is one edge to some source followed by a shortest path from that source. So $\mathrm{dist}[v] = \delta(S, v)$. The tree path from $v$ goes back to a source $s$ through the parents and has $\mathrm{dist}[v]$ edges, so it is a shortest path from the nearest source, and $\mathrm{owner}[v] = s$ is a nearest source of $v$.

**Cost.** Each vertex is enqueued at most once and each list is scanned at most once, so the time is $\Theta(n + m)$, whatever the size of $S$. The extra space is $\Theta(n)$.

## Classic examples

**Distance map on a grid.** In a grid of cells, some cells are marked. For each cell, find the number of steps to the nearest marked cell, moving up, down, left and right. Put all marked cells in the queue at distance 0 and run the template on the [implicit](/implicit-graph/) grid graph. For example, on a row of 7 cells with marks at positions 1 and 5 (counting from 0), the distances are $1, 0, 1, 2, 1, 0, 1$. The cell at position 3 is at distance 2 from both marks, and its owner is the mark that was enqueued first.

**Spreading in rounds.** Rot spreads in a box of fruit, a rumour spreads in a network, a fire spreads in a forest: each step, every affected vertex affects its neighbours. The time when everything is affected is the largest finite $\mathrm{dist}[v]$, and an unaffected vertex is one with $\mathrm{dist}[v] = \infty$.

**Voronoi regions of a graph.** The sets $\{v : \mathrm{owner}[v] = s\}$ for $s \in S$ split the reachable vertices into regions of nearest centres, with ties broken by the queue order. Erwig calls this the graph Voronoi diagram. Mehlhorn used the same partition, computed by one shortest-path search from all terminals, for a fast 2-approximation of the Steiner tree problem.

**Closest pair of sources.** Find the smallest distance between two different sources. After the template, compute $D' = \min \{\mathrm{dist}[u] + 1 + \mathrm{dist}[v]\}$ over the edges $\{u, v\}$ of an undirected graph with $\mathrm{owner}[u] \ne \mathrm{owner}[v]$. Then $D'$ is the answer $D$. For each such edge, the walk from $\mathrm{owner}[u]$ to $u$, the edge, and the walk from $v$ to $\mathrm{owner}[v]$ joins two different sources, so $D' \ge D$. Conversely, take a shortest path $P$ between two sources $a$ and $b$ at distance $D$. The owner along $P$ starts as $a$ and ends as $b$, because each source owns itself, so some edge $\{u, v\}$ of $P$ has $\mathrm{owner}[u] \ne \mathrm{owner}[v]$, and $\mathrm{dist}[u] + 1 + \mathrm{dist}[v] \le \delta(a, u) + 1 + \delta(v, b) = D$. So one search and one scan of the edges find $D$ in $\Theta(n + m)$ time.

**Distance between two sets.** The distance from a set $A$ to a set $B$ is the smallest $\mathrm{dist}[b]$ for $b \in B$ after a multi-source BFS from $A$. The search can stop as soon as it dequeues a vertex of $B$.

## Variations

- **Weighted edges.** Put all sources in the priority queue of [Dijkstra's algorithm](/dijkstra/) with key 0. The super-source argument is the same, with edges of length 0 from $s^*$.
- **Sources with start times.** If source $s$ starts at time $t_s$, give it key $t_s$. With integer start times, a BFS that adds the sources to the queue when the current distance reaches $t_s$ works; in general use Dijkstra.
- **Directed graphs.** The template gives the distance *from* the nearest source. For the distance *to* the nearest target, run it on the [transpose graph](/transpose-graph/) with the targets as sources.
- **Two searches that meet.** [Bidirectional search](/bidirectional-search/) grows a search from the source and one from the target, and stops when they meet. Multi-source BFS with $S = \{s, t\}$ and owners finds the meeting edge in the same way as the closest-pair example.
- **Unique nearest source.** To find the vertices with two or more nearest sources, keep a second owner when an edge reaches a vertex at the same distance from a different owner.

## Pitfalls

- **One BFS per source.** Running $k$ separate searches and taking the minimum gives the same distances in $\Theta(k(n + m))$ time. Put all sources in one queue instead.
- **Sources not marked at the start.** Every source must get $\mathrm{dist} = 0$ before the loop starts. If a source is only enqueued and marked later, another source can reach it first and give it a positive distance.
- **Duplicate sources.** If $S$ lists a vertex twice, line L4 enqueues it twice. This does not change the distances, but it scans the list twice. Check $\mathrm{dist}[s] = \infty$ before line L4.
- **Ties.** The owner of a vertex at the same distance from two sources depends on the queue order. Do not rely on a particular choice unless the order of line L3 is fixed.

## Exercises

1. On a grid of $r \times c$ cells with some walls and some marked cells, write the template for the distance to the nearest marked cell, and prove that it takes $O(rc)$ time.
2. Prove that the queue of the template holds, at each moment, vertices with at most two values of $\mathrm{dist}$, the smaller ones first.
3. In the closest-pair example, show that the minimum over the edges with different owners is wrong if the owners are replaced by "the vertex is reached from some source". What extra information do the owners give?
4. Given a set of sources with integer start times $t_s \le T$, give an $O(n + m + T)$ algorithm for the time when each vertex is first reached.
5. Use the template to find, for each vertex of a tree, the distance to the nearest leaf, in $O(n)$ time.

## References
