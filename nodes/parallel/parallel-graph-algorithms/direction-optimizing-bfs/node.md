---
tag: HZS2BB
kind: algorithm
slug: direction-optimizing-bfs
name: Direction-optimizing BFS
aliases:
- hybrid BFS
- Beamer's BFS
- top-down bottom-up BFS
area: parallel/parallel-graph-algorithms
level: advanced
summary: Switches between top-down and bottom-up frontier expansion depending on frontier size.
solves: [graph-reachability]
model: crcw-pram
complexity:
  vars: {n: the number of vertices, m: the number of edges, D: the number of BFS levels, k: the largest in-degree}
  time: {worst: O((n + m) D)}
  depth: {worst: O(D (log n + k))}
  space: {extra: O(n + m)}
properties: {deterministic: false, recursive: false}
prereqs: [parallel-bfs, breadth-first-search, frontier-based-processing, graph-transpose]
see_also: [multi-source-bfs, bfs-layers, small-world-network, scale-free-network, erdos-renyi-model, compressed-sparse-row, work-span-model]
sources:
  - paper: doi:10.5555/2388996.2389013
    title: Scott Beamer, Krste Asanović and David Patterson, Direction-optimizing breadth-first search, SC 2012, Article 12
    locator: Section IV (bottom-up BFS, Fig. 5), Section V (the hybrid algorithm and its switch conditions, Fig. 7), Section VI-B (the values alpha = 14 and beta = 24)
  - paper: doi:10.1145/2442516.2442530
    title: Julian Shun and Guy E. Blelloch, Ligra, a lightweight graph processing framework for shared memory, PPoPP 2013
    locator: the edgeMap operator with its sparse and dense forms and the switch threshold m/20; section number to be checked
  - paper: doi:10.3233/SPR-130370
    title: Scott Beamer, Krste Asanović and David Patterson, Direction-optimizing breadth-first search, Scientific Programming 21(3-4), 2013
    locator: journal version of the SC 2012 paper; DOI to be checked
---

Direction-optimizing BFS is a [parallel breadth-first search](/parallel-bfs/) that chooses, in each round, between two ways to build the next frontier. The top-down step lets each frontier vertex look at its edges; the bottom-up step lets each unvisited vertex look for a parent in the frontier and stop at the first one it finds. Beamer, Asanović and Patterson (2012) switch to bottom-up when the frontier's edges outnumber a fraction of the unvisited vertices' edges, and back when the frontier is small again. On graphs with a small diameter this looks at far fewer edges than plain BFS, but it gives no better worst-case bound.

Notation on this page: $n$ is the number of vertices, $m$ the number of edges, $D$ the number of levels (the largest finite distance from the source plus one), $W$ the work, $S$ the span, and $T_p$ the time on $p$ processors. For the round with frontier $F$: $n_f = |F|$, $m_f$ is the number of edges out of $F$, and $m_u$ is the number of edges into the vertices that are not yet visited. The model is the synchronous CRCW PRAM with the arbitrary write rule; only the top-down step uses concurrent writes.

## In plain words

Plain parallel BFS lets every vertex of the current ring call all its neighbours. For a small ring that is cheap. In a social network the ring soon holds a large part of the graph, and then almost every call reaches a vertex that already has a parent, so most of the work is wasted.

The bottom-up step turns the calls around. Each vertex that nobody has reached yet asks its own neighbours, one at a time, whether one of them is in the current ring. It stops at the first yes. When the ring is large, the first or second neighbour usually says yes, so each vertex asks only a few questions.

The algorithm counts the edges on both sides before each round and picks the cheaper direction. It goes top-down at the start and at the end, and bottom-up in the middle rounds, where the ring is large.

## The problem

The input is a graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, a source $s$, and two positive parameters $\alpha$ and $\beta$. The top-down step needs the out-adjacency lists and the bottom-up step needs the in-adjacency lists (the [transpose](/graph-transpose/)); for an undirected graph the two are the same. The output is the same as for [parallel BFS](/parallel-bfs/): $dist[v]$, the distance from $s$, and a parent $parent[v]$ with $dist[parent[v]] = dist[v] - 1$ for each reachable $v \ne s$.

## The algorithm

Lines L5 to L8 are the heuristic of Beamer et al. (Section V of the paper). The top-down step is the round of [parallel BFS](/parallel-bfs/), shown here in short form. In the bottom-up step each unvisited vertex scans its in-neighbours in sequence and stops at the first one in $F$; different vertices run in parallel.

```pseudo id=main
DIRECTION-OPTIMIZING-BFS(G, s, α, β)
L1  for all v in parallel do dist[v] ← ∞, parent[v] ← nil
L2  dist[s] ← 0, parent[s] ← s, F ← [s], d ← 0, mode ← top-down, n_prev ← 0
L3  while F is not empty do
L4      d ← d + 1
L5      m_f ← Σ_{u ∈ F} outdeg(u)                    ▷ m_u is kept up to date at line L11
L6      if mode = top-down and m_f > m_u / α and |F| > n_prev then mode ← bottom-up
L7      else if mode = bottom-up and |F| < n / β and |F| < n_prev then mode ← top-down
L8      n_prev ← |F|
L9      if mode = top-down then F' ← TOP-DOWN-STEP(F)
L10     else F' ← BOTTOM-UP-STEP(F)
L11     for all v in F' in parallel do dist[v] ← d     ▷ and m_u ← m_u − Σ_{v ∈ F'} indeg(v)
L12     F ← F'
L13 return dist, parent

TOP-DOWN-STEP(F)
L14 for all u in F, for all out-neighbours v of u, in parallel do
L15     if parent[v] = nil then parent[v] ← u          ▷ concurrent write, an arbitrary writer wins
L16 return PACK of the heads v with parent[v] = u and dist[v] = ∞, one slot for each edge

BOTTOM-UP-STEP(F)
L17 in_F[u] ← true for u in F, false for the other vertices
L18 for all v with dist[v] = ∞ in parallel do
L19     for each in-neighbour u of v, in order do       ▷ sequential, stops at the first hit
L20         if in_F[u] then parent[v] ← u, mark v, and stop the scan
L21 return PACK of the marked vertices
```

At the start, $m_u$ is the number of edges into the vertices other than $s$. The test $|F| > n_{prev}$ is "the frontier is growing" and the test $|F| < n_{prev}$ is "the frontier is shrinking". Beamer et al. report that these two tests are usually redundant, but that they give a speedup of about 10%. The paper uses $\alpha = 14$ and $\beta = 24$, found by experiment (Section VI-B). In an undirected graph, $m_f$ and $m_u$ can count one edge twice.

## Example

The graph has 7 vertices and the 8 undirected edges $\{0,1\}$, $\{0,2\}$, $\{1,3\}$, $\{2,3\}$, $\{2,4\}$, $\{3,5\}$, $\{4,5\}$, $\{5,6\}$, with source 0 and the small values $\alpha = 2$, $\beta = 2$ that suit a graph this small. The adjacency lists are in increasing order. Then $n/\beta = 3.5$, and $m_u = 16 - 2 = 14$ at the start.

| round | $F$ | $m_f$ | $m_u$ | mode | edges examined | next frontier |
|---|---|---|---|---|---|---|
| 1 | [0] | 2 | 14 | top-down ($2 \le 7$) | 2 | [1, 2] |
| 2 | [1, 2] | 5 | 9 | bottom-up ($5 > 4.5$, growing) | 6 | [3, 4] |
| 3 | [3, 4] | 5 | 4 | bottom-up (not shrinking) | 2 | [5] |
| 4 | [5] | 3 | 1 | top-down ($1 < 3.5$, shrinking) | 3 | [6] |
| 5 | [6] | 1 | 0 | top-down (not growing) | 1 | [] |

In round 2 the unvisited vertices are 3, 4, 5 and 6. Vertex 3 finds 1 at its first in-neighbour, vertex 4 finds 2 at its first, vertex 5 scans all of 3, 4, 6 and finds none, and vertex 6 scans 5 and finds none: 6 edges. The bottom-up parents are $parent[3] = 1$, $parent[4] = 2$ and $parent[5] = 3$, the first hits in list order. The run looks at 14 edge slots; plain top-down BFS looks at 16. On a random graph with 300 vertices and edge probability 0.05 (4,524 edge slots), the same heuristic with $\alpha = 14$, $\beta = 24$ runs top-down, top-down, bottom-up, bottom-up, and looks at 505 edge slots instead of 4,524.

## Correctness

Each round, top-down or bottom-up, turns the frontier $L_d$ into $L_{d+1}$, the set of vertices at distance $d + 1$. For the top-down step this is the invariant of [parallel BFS](/parallel-bfs/). For the bottom-up step: an unvisited vertex at distance $d + 1$ has an in-neighbour at distance $d$, which is in $F$, so its scan finds a parent; an unvisited vertex at distance more than $d + 1$ has no in-neighbour in $L_d$, so its scan finds none. The heuristic only chooses between two correct steps, so it changes the cost and never the distances. The full proof is in the proof file.

## Complexity

The model is the CRCW PRAM, arbitrary write. These bounds are proved on this page; the speedups that the paper measures are cited, not proved.

- A top-down round costs $O(n_f + m_f)$ work and $O(\log n)$ time, as in [parallel BFS](/parallel-bfs/).
- A bottom-up round costs $O(n + e_b)$ work, where $e_b \le m_u$ is the number of edges examined, and $O(\log n + \ell)$ time, where $\ell$ is the longest scan of one vertex. The $O(n)$ term is the bitmap of line L17 and the pack of line L21 over all vertices.

Let $k$ be the largest in-degree, so $\ell \le k$. The top-down rounds together cost $O(n + m)$, as in plain BFS. Each bottom-up round costs at most $O(n + m)$ work and $O(\log n + k)$ time, so in the worst case

$$W = O((n + m) D), \qquad S = O(D (\log n + k)).$$

If each scan is done as a parallel search for the first hit (a minimum reduction over the in-list), the span becomes $O(D \log n)$, but each scan then reads the whole list.

The heuristic gives no worst-case guarantee. In a bottom-up round, each unvisited vertex with no in-neighbour in $F$ scans its whole list, and it can do so again in the next bottom-up round. So the bound above is all that holds in general, and it is worse than the $O(n + m)$ of plain BFS. The gain is on low-diameter graphs: when $F$ holds a large part of the vertices, most unvisited vertices find a frontier neighbour within a few edges, so $e_b$ is far less than $m_u$. Beamer et al. measure this on Kronecker and other low-diameter graphs (Section VI). By [Brent's theorem](/brent-theorem/), $T_p = O(W/p + S)$ with the $W$ and $S$ of the run.

## Properties

- **Same output as BFS.** The distances are those of BFS. The parents are a BFS tree, but a different one: in a bottom-up round each vertex takes its first in-neighbour in $F$ in list order.
- **Bottom-up needs no concurrent writes.** Each vertex writes only its own cells, so a bottom-up round runs on the CREW PRAM. Only the top-down step needs the arbitrary write or a compare-and-swap.
- **Two graph forms.** The bottom-up step reads in-edges, so a directed graph must be stored with its transpose, which doubles the memory.
- **Two frontier forms.** The top-down step uses a list of the frontier vertices; the bottom-up step uses a bitmap of $n$ flags. Each switch converts one form to the other in $O(n)$ work.

## Variants and improvements

- **Ligra's switch.** Shun and Blelloch (2013) use the same idea for any frontier operation: edgeMap uses the dense (bottom-up) form when $n_f + m_f$ exceeds a threshold, $m/20$ by default, and the sparse form otherwise. See [frontier-based processing](/frontier-based-processing/).
- **Parallel first-hit search.** Each vertex can split its in-list among processors and take the first hit by a minimum reduction. This lowers the span of a round to $O(\log n)$ but loses the early exit.

## When to use it

Use it for BFS on graphs with a small diameter and a skewed degree distribution, such as [small-world](/small-world-network/) and [scale-free](/scale-free-network/) networks and [random graphs](/erdos-renyi-model/), where a few middle rounds hold most of the vertices. On a road network or a mesh the frontier stays small and the heuristic stays top-down, so it costs only the counters. If the graph is directed and memory is tight, the transpose may cost too much.

## Pitfalls

- **A bottom-up step that does not stop at the first hit.** Without the early exit, each unvisited vertex reads its whole list, and the step costs $O(n + m_u)$ every time. That is the dense form of [frontier-based processing](/frontier-based-processing/) and gives no gain.
- **Reading the new frontier inside a bottom-up round.** The bitmap $in_F$ must hold the old frontier only. If a vertex marked in this round sets its own flag, a later vertex of the same round can take it as a parent, and the distances become wrong.
- **Out-edges in the bottom-up step.** On a directed graph, the bottom-up step must scan the in-neighbours. Scanning the out-neighbours gives distances in the reverse graph.
- **Counting the unvisited edges from scratch.** Computing $m_u$ by a sum over all vertices in each round adds $O(n)$ work to every top-down round. Keep it by subtraction, as line L11 does.
- **Copying the constants.** The values $\alpha = 14$ and $\beta = 24$ come from experiments on one machine and one set of graphs. They are a start, not a rule.

## Implementations

## History

Beamer, Asanović and Patterson presented the bottom-up step and the hybrid algorithm at SC 2012, with a journal version in Scientific Programming in 2013. Shun and Blelloch (2013) built the same switch into the edgeMap operator of Ligra, for any algorithm that works on frontiers.

## References
