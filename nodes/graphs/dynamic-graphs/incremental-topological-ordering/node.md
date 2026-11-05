---
tag: D5SS95
kind: algorithm
slug: incremental-topological-ordering
name: Incremental topological ordering algorithm
aliases:
- Haeupler et al. topological order maintenance
- Pearce-Kelly algorithm
area: graphs/dynamic-graphs
level: research
summary: Maintains a topological order under edge insertions while detecting cycles.
solves: [dynamic-topological-order]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, K: the number of vertices visited by the two searches plus the number of edges at them}
  time: {worst: O(K log K)}
  space: {extra: O(m + n)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [topological-sort, directed-acyclic-graph, depth-first-search, incremental-graph]
see_also: [dynamic-topological-order, cycle-detection, strongly-connected-components, italiano-dynamic-transitive-closure, dynamic-reachability, kahns-algorithm, ramalingam-reps, amortized-update-time]
sources:
  - paper: doi:10.1145/1187436.1210590
    title: David J. Pearce and Paul H. J. Kelly, A dynamic topological sort algorithm for directed acyclic graphs, ACM Journal of Experimental Algorithmics 11 (2007)
    locator: the algorithm PK (forward and backward search inside the affected region, reordering within the positions it already uses) and its bounded complexity
  - paper: doi:10.1145/2071379.2071382
    title: Bernhard Haeupler, Telikepalli Kavitha, Rogers Mathew, Siddhartha Sen and Robert E. Tarjan, Incremental cycle detection, topological ordering, and strong component maintenance, ACM Transactions on Algorithms 8(1), 1 to 33 (2012)
    locator: the two-way search with interleaved forward and backward steps (O(m^(3/2)) total time) and its lower bound for local algorithms
  - paper: doi:10.1016/0020-0190(96)00075-0
    title: Alberto Marchetti-Spaccamela, Umberto Nanni and Hans Rohnert, Maintaining a topological order under edge insertions, Information Processing Letters 59(1), 53 to 58 (1996)
    locator: the whole paper (forward search only, O(mn) total time)
  - paper: doi:10.1145/2756553
    title: Michael A. Bender, Jeremy T. Fineman, Seth Gilbert and Robert E. Tarjan, A new approach to incremental cycle detection and related problems, ACM Transactions on Algorithms 12(2), 1 to 22 (2016)
    locator: the main theorems (O(m min(m^(1/2), n^(2/3))) total time for sparse graphs and O(n^2 log n) for dense graphs)
---

The incremental topological ordering algorithm keeps a [topological order](/topological-sort/) of a directed graph while edges are inserted, and rejects the first edge that would close a cycle. When a new edge $(u, v)$ already goes forward in the order, nothing changes. Otherwise it searches forward from $v$ and backward from $u$, but only among the positions between $v$ and $u$, the **affected region**. If the forward search reaches $u$, the edge closes a cycle. If not, the vertices found backward from $u$ move in front of the vertices found forward from $v$, using only the positions those vertices already held. This is the algorithm of Pearce and Kelly (2007). It supports insertions only, is deterministic, and takes $O(K \log K)$ time per insertion, where $K$ is the size of the searched region; Haeupler, Kavitha, Mathew, Sen and Tarjan (2012) showed that interleaving the two searches carefully gives $O(m^{3/2})$ total time.

## In plain words

Keep a to-do list that respects rules of the form "do this before that". A new rule says $u$ before $v$.

If $u$ is already above $v$ in the list, nothing moves. Otherwise only the tasks between $v$ and $u$ can be in the way. Collect, from that stretch, the tasks that must come after $v$, and the tasks that $u$ must come after.

If $u$ itself must come after $v$, the new rule makes a circle of rules, and it is refused. Otherwise put the second group before the first, using the same spots of the list that they used before. Every other task stays where it was.

## The problem

The input is a number $n$ of vertices and a sequence of edge insertions into a directed graph, starting with no edges. The algorithm keeps an order $\mathrm{pos} : V \to \{0, \ldots, n - 1\}$, a bijection, with $\mathrm{pos}(x) < \mathrm{pos}(y)$ for every edge $(x, y)$. For each insertion it must either accept the edge and update the order, or report that the edge would close a cycle and refuse it. This is the incremental form of [dynamic topological order](/dynamic-topological-order/), and it also solves incremental [cycle detection](/cycle-detection/). Deleting an edge never makes an order invalid, so deletions are free.

## The algorithm

```pseudo id=main
ADD-EDGE(u, v)
L1  if pos(u) < pos(v) then add the edge and return accepted
L2  F ← the vertices reachable from v through vertices y with pos(y) < pos(u)   ▷ forward search
L3  if the search finds an edge into u then return cycle
L4  B ← the vertices that reach u through vertices y with pos(y) > pos(v)       ▷ backward search
L5  sort B and F by pos; P ← the sorted positions of B ∪ F
L6  give the positions of P, in order, to B in its old order and then to F in its old order; add the edge

ORDER
L7  return the vertices sorted by pos
```

Line L1 is the cheap case. Lines L2 and L4 are [depth-first searches](/depth-first-search/) that never leave the window of positions between $\mathrm{pos}(v)$ and $\mathrm{pos}(u)$: a vertex outside the window cannot lie on a path from $v$ to $u$ in a valid order. Line L3 detects a cycle: a path from $v$ to $u$ together with the new edge. Lines L5 and L6 are the reordering. They keep the relative order inside $B$ and inside $F$, and they put all of $B$ before all of $F$, which places $u \in B$ before $v \in F$. Vertices outside $B \cup F$ keep their positions.

## Example

Take six vertices in the order $0, 1, 2, 3, 4, 5$ and insert $(0, 1)$, $(1, 2)$, $(4, 5)$, $(5, 1)$, $(3, 4)$, $(2, 3)$.

| edge | case | $F$ | $B$ | order after |
|---|---|---|---|---|
| $(0, 1)$, $(1, 2)$, $(4, 5)$ | already forward | | | 0 1 2 3 4 5 |
| $(5, 1)$ | reorder | $\{1, 2\}$ | $\{4, 5\}$ | 0 4 5 3 1 2 |
| $(3, 4)$ | reorder | $\{4, 5\}$ | $\{3\}$ | 0 3 4 5 1 2 |
| $(2, 3)$ | cycle | reaches 3 | | 0 3 4 5 1 2 |

For $(5, 1)$ the window is the positions 1 to 5. The forward search from 1 finds 2; vertex 3 is in the window but not reachable, so it stays at position 3. The backward search from 5 finds 4. The four vertices held the positions 1, 2, 4, 5, and they get them in the order 4, 5, 1, 2. For $(3, 4)$, vertex 4 is at position 1 and 3 at position 3; the forward search from 4 finds 5 at position 2 and stops at 1 at position 4, outside the window, and the positions 1, 2, 3 go to 3, 4, 5. The edge $(2, 3)$ would close the cycle $3, 4, 5, 1, 2, 3$: the forward search from 3 reaches 2 through 4, 5 and 1, so it is refused.

## Correctness

If the forward search reaches $u$, there is a path from $v$ to $u$, and the edge closes a cycle. Conversely, if the edge closes a cycle, there is a path from $v$ to $u$, and in a valid order all its vertices lie between $v$ and $u$, so the forward search finds it. For the reordering, an edge between two vertices of $F$, two of $B$, or two vertices outside $B \cup F$ keeps its direction, because the relative order of each group is kept. An edge from outside into $F$, or from $B$ to outside, also keeps it, and edges from $F$ to $B$ cannot exist, since they would give a cycle through the new edge. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Per insertion.** The two searches visit $K_v$ vertices and their edges, $K$ in total, and the sort of line L5 costs $O(K_v \log K_v)$. So an insertion costs $O(K \log K)$ time, where $K$ is the size of the affected part only, not of the graph. Pearce and Kelly call this a **bounded** algorithm in the sense of Ramalingam and Reps.
- **Worst case per insertion.** $K$ can be $\Theta(m)$, so one insertion can cost $O(m + n \log n)$.
- **Total.** The simple version above has no good bound on the total time of $m$ insertions in the worst case. Haeupler et al. proved that searching forward and backward one edge at a time, and stopping as soon as the two searches cannot meet, gives $O(m^{3/2})$ total time, and that any algorithm of this local kind needs $\Omega(m^{3/2})$ in the worst case.
- **Space.** $O(m + n)$.
- **Deterministic.**

## Properties

- **Insertions only.** Deletions keep the order valid and need no work, so the structure handles them by removing the edge, but no bound improves.
- **Local.** Only vertices whose position changes are touched besides the searched ones; every vertex outside $B \cup F$ keeps its position.
- **Cycle detection.** The first edge that closes a cycle is refused, and the graph and the order are left as they were.
- **Deterministic.**

## Variants and improvements

- **Forward search only.** Marchetti-Spaccamela, Nanni and Rohnert (1996) search only forward from $v$ and shift the found vertices after $u$, in $O(mn)$ total time.
- **Two-way search.** Haeupler, Kavitha, Mathew, Sen and Tarjan (2012) interleave the two searches one edge at a time, keep the order in an order-maintenance list, and get $O(m^{3/2})$ total time; they also maintain strongly connected components under insertions with the same bound.
- **Dense graphs.** Bender, Fineman, Gilbert and Tarjan (2016) gave $O(m \min(m^{1/2}, n^{2/3}))$ total time for sparse graphs and $O(n^2 \log n)$ for dense ones, using levels instead of local searches.
- **Randomized.** Bernstein and Chechik (2018) gave $O(m n^{1/2})$ expected total time against an oblivious adversary, which is better for sparse graphs with many edges per vertex.
- **Strong components.** When cycles are allowed, contract each cycle into one vertex and keep an order of the [strongly connected components](/strongly-connected-components/).

## When to use it

Use it when edges arrive one at a time and a valid order or an immediate cycle check is needed after each, as in build systems, spreadsheets that recompute cells, pointer analysis in compilers, and deadlock detection. Pearce and Kelly found the simple version fast on sparse graphs in practice. For a fixed graph, a static [topological sort](/topological-sort/) or [Kahn's algorithm](/kahns-algorithm/) is simpler. For worst-case guarantees on adversarial input, use the two-way search with its total bound.

## Pitfalls

- **Searching outside the window.** Without the bound $\mathrm{pos}(y) < \mathrm{pos}(u)$, the forward search can walk the whole rest of the graph, and the search no longer stays proportional to the affected region.
- **Reassigning fresh positions.** Moving $B$ and $F$ to new positions, for example to the end of the list, breaks edges to and from the vertices left in place. Reuse exactly the positions they held.
- **Forgetting the order inside each group.** Each of $B$ and $F$ must keep its own internal order; the sort of line L5 does this.
- **Adding the edge before the cycle test.** If the edge is added first, the forward search sees it and must undo it. Add it only after the test.

## Implementations

## History

Alpern, Hoover, Rosen, Sweeney and Zadeck (1990) gave an early bounded algorithm for incremental topological order. Marchetti-Spaccamela, Nanni and Rohnert (1996) gave $O(mn)$ total time. Pearce and Kelly (2004, journal 2007) gave the local reordering of this page and showed it is fast in practice. Katriel and Bodlaender (2006) proved an $O(m^{3/2} \log n)$ bound for a related method, and Haeupler, Kavitha, Mathew, Sen and Tarjan (2008, journal 2012) reached $O(m^{3/2})$ with two-way search. Bender, Fineman, Gilbert and Tarjan and then Bernstein and Chechik gave the best bounds for dense graphs.

## References
