---
tag: DAB5AT
kind: algorithm
slug: offline-dynamic-connectivity
name: Offline dynamic connectivity
aliases:
- segment tree over time with rollback union-find
- divide-and-conquer over time connectivity
area: graphs/dynamic-graphs
level: advanced
summary: Places each edge on a segment tree over time and uses rollback union-find to answer all queries.
solves: [dynamic-connectivity]
model: word-ram
complexity:
  vars: {T: the number of operations, n: the number of vertices}
  time: {worst: O(T log T log n)}
  space: {extra: O(T log T + n)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [union-find-with-rollback, segment-tree, offline-dynamic-graph]
see_also: [divide-and-conquer-on-queries, rollback-technique, dynamic-connectivity, holm-de-lichtenberg-thorup, link-cut-tree, offline-deletion, dsu-with-parity, dynamic-bipartiteness]
sources:
  - url: https://cp-algorithms.com/data_structures/deleting_in_log_n.html
    title: cp-algorithms, Deleting from a data structure in O(T(n) log n)
    locator: sections Algorithm and Implementation (lifetimes of edges, segment tree over time, union-find with rollbacks, dynamic connectivity)
  - paper: "David Eppstein, Offline algorithms for dynamic minimum spanning tree problems, Journal of Algorithms 17(2), 237 to 250 (1994), doi:10.1006/jagm.1994.1033"
    locator: the recursion over blocks of the update sequence, with contraction of edges that are present in the whole block
  - paper: "Jeffery Westbrook and Robert E. Tarjan, Amortized analysis of algorithms for set union with backtracking, SIAM Journal on Computing 18(1), 1 to 11 (1989)"
    locator: Section 1 (union by rank or size without path compression gives O(log n) worst-case finds with undo)
---

Offline dynamic connectivity answers connectivity queries on a graph whose edges are inserted and deleted, when the whole sequence of operations is known in advance. It computes the interval of time during which each edge is present, stores each interval at $O(\log T)$ nodes of a [segment tree](/segment-tree/) over the $T$ time steps, and walks the tree depth first with a [union-find with rollback](/union-find-with-rollback/). Each leaf then sees exactly the edges present at its time, and the total time is $O(T \log T \log n)$. It is deterministic, fully dynamic (insertions and deletions) and much simpler than online methods such as the [Holm-de Lichtenberg-Thorup algorithm](/holm-de-lichtenberg-thorup/).

## In plain words

Union-find joins groups fast, but it cannot split them. This method avoids splits by reordering the work.

Write the operations on a time line. Each edge lives from the moment it is added to the moment it is removed. Build a balanced tree over the time line, where each node covers a range of moments, and give each edge to the few nodes that together cover its life exactly.

Now walk the tree from the root, going left before right. When you enter a node, join the groups of its edges. When you reach a leaf, the joined groups are exactly the groups at that moment, so answer its question. When you leave a node, undo the joins you made there. Undo is cheap because the joins are undone in the reverse order of making them.

## The problem

The input is a number $n$ of vertices and a sequence $o_0, o_1, \ldots, o_{T-1}$ of operations, each one of:

- $\mathrm{add}(u, v)$: insert an edge $\{u, v\}$ (parallel edges allowed);
- $\mathrm{remove}(u, v)$: delete one copy of an edge $\{u, v\}$ that is present;
- $\mathrm{query}(u, v)$: are $u$ and $v$ connected in the current graph?
- $\mathrm{count}$: the number of connected components of the current graph.

The graph at time $t$ is the graph after the operations $o_0, \ldots, o_t$. The output is the list of answers of the queries, in order. This is the [offline](/offline-dynamic-graph/) form of the [dynamic connectivity](/dynamic-connectivity/) problem: the algorithm may read all operations before it answers the first query.

## The algorithm

A copy of an edge added at time $a$ and removed at time $d$ is present at the times $a, a+1, \ldots, d-1$, its **lifetime** $[a, d)$. A copy that is never removed has the lifetime $[a, T)$. A segment tree over $[0, T)$ splits any interval into at most $2 \lceil \lg T \rceil$ **canonical** nodes, whose ranges are disjoint and whose union is the interval.

```pseudo id=main
OFFLINE-DYNAMIC-CONNECTIVITY(n, o[0..T−1])
L1  compute the lifetime [a, d) of each copy of each edge
L2  for each lifetime [a, d) of an edge e: add e to the list of each canonical node of [a, d)
    D ← a union-find with rollback on n elements
    VISIT(root)

VISIT(x)
L3  h ← CHECKPOINT(D)
L4  for each edge {u, v} in the list of x: UNION(D, u, v)
L5  if x is the leaf of time t then answer o[t] if it is a query, from D
L6  else VISIT(left child of x); VISIT(right child of x)
L7  ROLLBACK(D, h)
```

Line L1 is one pass over the operations, with a stack of open start times for each edge. Line L2 inserts each lifetime as in a segment tree range update. The union-find uses union by size and no [path compression](/path-compression/), so each union writes a constant number of fields and records them in a log; ROLLBACK pops the log back to the height saved in line L3. The number of components is a counter in the union-find, updated by each union and restored by each undo. The implementation runs VISIT with an explicit stack instead of recursion.

## Example

Take $n = 4$ and the operations below, at times 0 to 9.

| time | operation | edges present after it | answer |
|---|---|---|---|
| 0 | add(0, 1) | 01 | |
| 1 | add(1, 2) | 01, 12 | |
| 2 | query(0, 2) | 01, 12 | yes |
| 3 | remove(0, 1) | 12 | |
| 4 | query(0, 2) | 12 | no |
| 5 | add(2, 3) | 12, 23 | |
| 6 | add(0, 3) | 12, 23, 03 | |
| 7 | query(0, 1) | 12, 23, 03 | yes |
| 8 | remove(1, 2) | 23, 03 | |
| 9 | count | 23, 03 | 2 |

The lifetimes are $[0, 3)$ for $\{0, 1\}$, $[1, 8)$ for $\{1, 2\}$, $[5, 10)$ for $\{2, 3\}$ and $[6, 10)$ for $\{0, 3\}$. The segment tree over 16 leaves splits them into canonical ranges:

| edge | lifetime | canonical ranges |
|---|---|---|
| $\{0, 1\}$ | $[0, 3)$ | $[0, 2)$, $[2, 3)$ |
| $\{1, 2\}$ | $[1, 8)$ | $[1, 2)$, $[2, 4)$, $[4, 8)$ |
| $\{2, 3\}$ | $[5, 10)$ | $[5, 6)$, $[6, 8)$, $[8, 10)$ |
| $\{0, 3\}$ | $[6, 10)$ | $[6, 8)$, $[8, 10)$ |

At the leaf of time 7, the walk has entered the ranges $[0, 16)$, $[0, 8)$, $[4, 8)$, $[6, 8)$ and $[7, 8)$. On the way it has joined $\{1, 2\}$ at $[4, 8)$ and $\{2, 3\}$ and $\{0, 3\}$ at $[6, 8)$, so 0 and 1 are in one set and the answer is yes. The edge $\{0, 1\}$ was joined at $[0, 2)$ and $[2, 3)$, but those joins were undone when the walk left those ranges. At time 9, only $\{2, 3\}$ and $\{0, 3\}$ were joined, at $[8, 10)$, so the sets are $\{0, 2, 3\}$ and $\{1\}$, and the count is 2.

## Correctness

At the leaf of time $t$, the sets of the union-find are the connected components of the graph at time $t$. Two facts give this. First, the canonical nodes of an interval partition it, so the edge copies whose lists lie on the path from the root to the leaf of $t$ are exactly the copies whose lifetime contains $t$, which are the edges present at time $t$. Second, by induction over the walk, when VISIT$(x)$ starts, the union-find holds the unions of exactly the edges on the path from the root to the parent of $x$, because line L7 restores the state that line L3 saved. Union-find on a set of edges gives the components of the graph of those edges. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Lifetimes and the tree.** Line L1 takes $O(T)$ expected time with a hash table of open edges. Each lifetime goes to at most $2 \lceil \lg T \rceil$ nodes, so line L2 and the lists take $O(T \log T)$ time and space.
- **The walk.** Each stored copy causes one union, which runs two finds of $O(\log n)$ worst-case time each, because union by size keeps every tree of depth at most $\lg n$ and no path compression changes it. Each union is undone once in $O(1)$. The tree has $O(T)$ nodes. So the walk takes $O(T \log T \log n)$ time, and each query takes $O(\log n)$ at its leaf.
- **Total.** $O(T \log T \log n)$ time in the worst case over the whole sequence, which is $O(\log T \log n)$ per operation amortized over the sequence. No single operation has its own bound, because all answers come out of one walk. Space $O(T \log T + n)$.
- **Deterministic.** The algorithm uses no random choices; a sorted map or a radix sort can replace the hash table of line L1.

Path compression would break the rollback: its bound is amortized, and an undo restores the potential that pays for it; see the [rollback technique](/rollback-technique/).

## Properties

- **Offline.** The algorithm must know every operation before it answers the first query, because it needs the deletion time of each edge.
- **Fully dynamic.** Insertions and deletions are allowed in any order, with parallel edges.
- **Deterministic and simple.** It needs only a segment tree and a union-find with an undo log.
- **General.** Any structure that supports insertions with worst-case cost $c$ and undo of the last insertion gives a fully dynamic offline structure with cost $O(c \log T)$ per insertion; this is [divide and conquer on queries](/divide-and-conquer-on-queries/).

## Variants and improvements

- **Bipartiteness.** With a [union-find with parity](/dsu-with-parity/), the same walk answers whether the current graph is bipartite; see [dynamic bipartiteness](/dynamic-bipartiteness/).
- **Divide and conquer with contraction.** Eppstein (1994) recursed over blocks of the operation sequence and contracted the edges present in the whole block, so the graph at each recursion node has size proportional to the number of operations in it. This removes the union-find factor and gives offline [dynamic minimum spanning trees](/dynamic-minimum-spanning-tree/) and connectivity in $O(\log n)$ time per operation, amortized over the sequence.
- **Maximum spanning forest by deletion time.** Give each edge the weight of its deletion time, and keep a maximum spanning forest of the present edges in a [link-cut tree](/link-cut-tree/). An inserted edge that closes a cycle replaces the cycle edge that is deleted earliest. Two vertices are connected if and only if they are connected in this forest, so each operation takes $O(\log n)$ amortized time, and the algorithm needs to know only the deletion time of each edge when it is inserted.
- **Two- and three-edge connectivity.** Peng, Sandlund and Sleator (2019) gave offline algorithms for 2- and 3-edge and vertex connectivity with $O(\log n)$ time per operation, by divide and conquer over the operation sequence.

## When to use it

Use it when all operations are known in advance, for example in a batch job or a programming contest, and the edges are both inserted and deleted. It is short, deterministic and fast in practice. If the deletion times are known at insertion time but the queries must be answered online, use the spanning forest by deletion time. If the operations arrive one at a time and nothing is known about the future, use an online method such as the [Holm-de Lichtenberg-Thorup algorithm](/holm-de-lichtenberg-thorup/). If there are no deletions, a plain union-find with path compression is enough; see [incremental connectivity](/incremental-connectivity/).

## Pitfalls

- **Path compression.** A union-find with path compression cannot be rolled back cheaply, and its amortized bound fails under undo. Use union by size or by rank alone.
- **Off by one in lifetimes.** An edge removed at time $d$ is absent at time $d$ itself. With the lifetime $[a, d]$ instead of $[a, d)$, a query just after a deletion still sees the edge.
- **Parallel edges.** If the same edge is added twice and removed once, it is still present. Keep a stack of start times per edge, not one start time.
- **Unions that change nothing.** A union of two vertices in one set writes nothing. Roll back to the saved log height, not by the number of edges in the list.
- **Deep recursion.** The segment tree has depth $\lceil \lg T \rceil$, which is small, but recursive languages with small stacks can still fail on other parts, such as a recursive find. Use loops.

## Implementations

## History

The technique combines two old ideas. Union-find with backtracking, which undoes the most recent unions, was posed by Mannila and Ukkonen in 1986 and analyzed by Westbrook and Tarjan in 1989. Recursion over the time line of an offline update sequence appears in Eppstein's 1994 algorithm for offline dynamic minimum spanning trees. The combination with a segment tree over time became a standard method in programming contests, where it is often called "offline dynamic connectivity"; the cp-algorithms article describes it for any structure with undo.

## References
