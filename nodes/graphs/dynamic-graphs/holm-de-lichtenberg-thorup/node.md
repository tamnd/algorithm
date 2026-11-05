---
tag: 4DN5PG
kind: algorithm
slug: holm-de-lichtenberg-thorup
name: Holm-de Lichtenberg-Thorup algorithm
aliases:
- HDT algorithm
- HDT dynamic connectivity
area: graphs/dynamic-graphs
level: research
summary: Polylogarithmic amortized fully dynamic connectivity using edge levels and spanning forests.
solves: [dynamic-connectivity]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {amortized: O(log^2 n)}
  space: {extra: O(m + n log n)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [dynamic-connectivity, euler-tour-tree, spanning-forest]
see_also: [dynamic-minimum-spanning-tree, eppstein-galil-italiano-nissenzweig, dynamic-connectivity-lower-bound, decremental-connectivity, dynamic-biconnectivity, amortized-update-time, worst-case-update-time, link-cut-tree]
sources:
  - paper: doi:10.1145/502090.502095
    title: Jacob Holm, Kristian de Lichtenberg and Mikkel Thorup, Poly-logarithmic deterministic fully-dynamic algorithms for connectivity, minimum spanning tree, 2-edge, and biconnectivity, Journal of the ACM 48(4), 723 to 760 (2001)
    locator: Section 2 (the levels, the invariants on the forests F_i, the replacement search, O(log^2 n) amortized update and O(log n / log log n) query)
  - paper: doi:10.1145/320211.320215
    title: Monika R. Henzinger and Valerie King, Randomized fully dynamic graph algorithms with polylogarithmic time per operation, Journal of the ACM 46(4), 502 to 516 (1999)
    locator: the connectivity algorithm (levels of edges and sampling, O(log^3 n) expected amortized time), the randomized forerunner
  - paper: "Christian Wulff-Nilsen, Faster deterministic fully-dynamic graph connectivity, Proceedings of the 24th ACM-SIAM Symposium on Discrete Algorithms (SODA 2013), 1757 to 1769"
    locator: the main theorem (O(log^2 n / log log n) amortized update time, deterministic)
  - paper: "Mihai Pătraşcu and Erik D. Demaine, Logarithmic lower bounds in the cell-probe model, SIAM Journal on Computing 35(4), 932 to 963 (2006)"
    locator: the dynamic connectivity lower bound (the maximum of update and query time is Ω(log n))
---

The Holm-de Lichtenberg-Thorup algorithm, often called HDT, answers connectivity queries in an undirected graph under edge insertions and deletions in $O(\log^2 n)$ amortized time per update and $O(\log n / \log \log n)$ time per query, deterministically. It keeps a spanning forest in [Euler tour trees](/euler-tour-tree/) and gives every edge a **level** between 0 and $\lg n$. When a forest edge is deleted, it searches for a replacement edge among the non-tree edges near the smaller of the two new trees, and it raises the level of every edge it checks and rejects. A tree of the forest at level $i$ has at most $n / 2^i$ vertices, so an edge can rise at most $\lg n$ times, and those rises pay for the search. Holm, de Lichtenberg and Thorup published it in 1998 (journal 2001); it was the first deterministic fully dynamic connectivity algorithm with polylogarithmic update time.

## In plain words

The program keeps a skeleton of the graph: a set of edges with no loops that still connects everything that is connected. As long as the skeleton is intact, two points are connected exactly when the skeleton connects them.

Adding an edge is easy. Deleting a skeleton edge splits a piece in two, and the program must find another edge that joins the two halves, if there is one.

It looks only around the smaller half. Each edge it looks at and finds useless is pushed one floor up. An edge on a high floor lives in a small piece, because each push halves the size limit. So no edge is pushed more than a few dozen times, and the total work stays small.

## The problem

The input is a number $n$ of vertices and a sequence of operations, given one at a time:

- $\mathrm{insert}(u, v)$ adds an edge $\{u, v\}$;
- $\mathrm{delete}(u, v)$ removes an edge that is present;
- $\mathrm{connected}(u, v)$ asks whether $u$ and $v$ are in one connected component.

Each query must be answered before the next operation is read. This is the fully dynamic form of [dynamic connectivity](/dynamic-connectivity/). The graph may have parallel edges; a copy beyond the first changes no component.

## The algorithm

Every edge $e$ has a level $\ell(e) \in \{0, 1, \ldots, L\}$ with $L = \lfloor \lg n \rfloor$. Let $G_i$ be the graph of edges of level at least $i$. The algorithm keeps a spanning forest $F$ of $G$ and its restrictions $F_i = F \cap G_i$, which satisfy two invariants:

- **(I1) Maximality.** $F_i$ is a spanning forest of $G_i$. Equivalently, the two ends of a non-tree edge of level $i$ are connected in $F_i$.
- **(I2) Size.** Every tree of $F_i$ has at most $n / 2^i$ vertices.

Each $F_i$ is stored as an Euler tour forest. Each node carries two counters, summed over its subtree: the number of tree edges of level exactly $i$ on its arcs, and the number of non-tree edges of level $i$ at its vertex. A search down from the root then finds such an edge in $O(\log n)$ time.

```pseudo id=main
INSERT(u, v)
L1  if u and v are not connected in F_0 then
L2      add {u, v} to F with level 0              ▷ else it is a non-tree edge of level 0

DELETE(u, v)
L3  if {u, v} is a non-tree edge then remove it and return
L4  ℓ ← ℓ({u, v}); cut {u, v} from F_0, …, F_ℓ
L5  for i ← ℓ down to 0:
L6      T_u, T_v ← the trees of F_i containing u and v, with |T_u| ≤ |T_v|
L7      raise every tree edge of level i in T_u to level i + 1
        for each non-tree edge f of level i with an end in T_u:
L8          take f and look at its other end y
L9          if y is in T_v then make f a tree edge of level i, link it in F_0, …, F_i; return
L10         else raise f to level i + 1
L11 no replacement exists; the component stays split

CONNECTED(u, v)
L12 return whether u and v are in one tree of F_0
```

Line L4 removes the edge from all forests that contain it. Line L6 picks the smaller side at the current level, which is the key to (I2): after line L7, $T_u$ is a tree of $F_{i+1}$ with at most $\frac{1}{2} \cdot n / 2^i$ vertices. Line L10 raises a rejected edge whose two ends are both in $T_u$, so (I1) holds at level $i + 1$. The search goes from the level of the deleted edge down, because by (I1) no edge of a higher level can join the two sides.

## Example

Take six vertices, the triangles $0, 1, 2$ and $3, 4, 5$, and the edge $\{2, 3\}$ between them, inserted in the order 01, 12, 20, 23, 34, 45, 53. The forest edges are 01, 12, 23, 34, 45, all at level 0, and 02 and 35 are non-tree edges at level 0.

| operation | levels after it (T: tree edge, N: non-tree edge) | answer |
|---|---|---|
| inserts | 01 T0, 12 T0, 02 N0, 23 T0, 34 T0, 45 T0, 35 N0 | |
| delete 23 | 01 T1, 12 T1, 02 N1, 34 T0, 45 T0, 35 N0 | connected(0, 5) = false |
| delete 01 | 12 T1, 02 T1, 34 T0, 45 T0, 35 N0 | connected(0, 1) = true |
| insert 14 | 12 T1, 02 T1, 14 T0, 34 T0, 45 T0, 35 N0 | |
| delete 34 | 12 T1, 02 T1, 14 T0, 45 T0, 35 T0 | connected(0, 3) = true |

Deleting 23 splits $F_0$ into $\{0, 1, 2\}$ and $\{3, 4, 5\}$, both of size 3, so the first is searched. Its tree edges 01 and 12 rise to level 1. The only non-tree edge at its vertices is 02, whose ends are both on the same side, so it rises too, and no replacement is found. Deleting 01, a tree edge of level 1, starts the search at level 1: the side $\{0\}$ is smaller, its non-tree edge 02 of level 1 reaches 2 on the other side, and it becomes a tree edge of level 1. Deleting 34 splits $\{0, 1, 2, 3, 4, 5\}$ at level 0 into $\{3\}$ and the rest; the non-tree edge 35 joins them and becomes a tree edge.

## Correctness

The two invariants hold at the start and are kept by every operation. An insertion of a non-tree edge of level 0 keeps (I1) because its ends are connected in $F_0$. In a deletion, an edge that can replace the deleted tree edge $e$ has level at most $\ell(e)$: an edge of higher level $j$ has its ends connected in $F_j$, which does not contain $e$. At level $i$, every non-tree edge of level $i$ with an end in $T_u$ has its other end in $T_u$ or $T_v$ by (I1), so the scan either finds a replacement or proves that there is none at level $i$. Raised edges keep (I1) because $T_u$ becomes a tree of $F_{i+1}$, and they keep (I2) because $T_u$ is the smaller half of a tree with at most $n / 2^i$ vertices. If no level has a replacement, no edge joins the two sides, and the forest is still spanning. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Level bound.** By (I2), a tree of $F_i$ with an edge has at least 2 vertices, so $i \le \lg n$, and every edge rises at most $\lg n$ times.
- **Cost per rise.** A rise is a search in an Euler tour forest plus a link or a change of counters, $O(\log n)$ time.
- **Insertion.** $O(\log n)$ time, plus a charge of $O(\log^2 n)$ for all later rises of the new edge.
- **Deletion.** Up to $\lg n + 1$ levels, each with a cut, two size queries and two failed searches, $O(\log^2 n)$, plus one successful scan. Every other scanned edge rises and is paid for by its insertion.
- **Total.** $O(\log^2 n)$ amortized time per update. A query takes $O(\log n)$ with balanced trees, and $O(\log n / \log \log n)$ with the B-trees of degree $\log n$ used in the paper for $F_0$.
- **Space.** $O(m + n \log n)$: every edge is in one adjacency set, and every level has an Euler tour forest on all $n$ vertices.
- **Kind of bound.** Amortized and deterministic. The implementation uses treaps, whose random priorities affect only the running time, which is then expected amortized.

## Properties

- **Fully dynamic.** Insertions and deletions in any order.
- **Amortized.** One deletion can raise many edges and take $\Theta(m \log n)$ time; the bound is for a whole sequence.
- **Deterministic.** The bound holds against an adaptive adversary, unlike many randomized dynamic algorithms.
- **Spanning forest included.** $F_0$ is an explicit spanning forest of the current graph, with $O(1)$ changes per update.

## Variants and improvements

- **Minimum spanning forest.** With levels and a search in weight order, the same paper keeps a [minimum spanning forest](/dynamic-minimum-spanning-tree/) in $O(\log^4 n)$ amortized time per update. Later work lowered this bound.
- **2-edge connectivity and biconnectivity.** The paper also gives $O(\log^4 n)$ and $O(\log^5 n)$ amortized bounds; see [dynamic biconnectivity](/dynamic-biconnectivity/).
- **Decremental.** With deletions only, [decremental connectivity](/decremental-connectivity/) admits faster methods.
- **Faster connectivity.** Wulff-Nilsen (2013) improved the deterministic bound to $O(\log^2 n / \log \log n)$ amortized. Randomized algorithms reach $O(\log n (\log \log n)^3)$ expected amortized time (Thorup, 2000) and then $O(\log n (\log \log n)^2)$ (Huang, Huang, Kopelowitz, Pettie and Thorup, 2017).
- **Lower bound.** Pătraşcu and Demaine (2006) proved that the larger of update and query time is $\Omega(\log n)$ in the cell-probe model; see the [connectivity lower bound](/dynamic-connectivity-lower-bound/).
- **Worst case.** For bounds on each single update, see [worst-case update time](/worst-case-update-time/) and the $O(n^{1/2})$ bound of [sparsification](/eppstein-galil-italiano-nissenzweig/).

## When to use it

Use it when a graph gains and loses edges in an arbitrary order and connectivity queries come between the updates, with no knowledge of the future. When all operations are known in advance, the [offline method](/offline-dynamic-connectivity/) is simpler and faster. When edges are only added, a union-find is enough. For forests only, a [link-cut tree](/link-cut-tree/) or an Euler tour tree alone suffices.

## Pitfalls

- **Searching the larger side.** The size invariant needs the smaller tree at each level. Searching the side of a fixed end breaks (I2) and the amortized bound.
- **Raising tree edges after the scan.** The tree edges of level $i$ in $T_u$ must rise before the non-tree edges, so that the raised non-tree edges have their ends connected in $F_{i+1}$.
- **Linking a replacement only at level 0.** A replacement of level $i$ must be linked in $F_0, \ldots, F_i$, or (I1) fails at the levels between.
- **Counters not refreshed.** The counters on the Euler tour nodes must change when an edge changes level or kind; a stale counter makes the search loop or miss an edge.
- **Parallel edges.** Keep a count per vertex pair, or give each copy its own identity; a set of pairs loses copies.

## Implementations

## History

Henzinger and King (1995, journal 1999) gave the first fully dynamic connectivity algorithm with polylogarithmic time, $O(\log^3 n)$ expected amortized, using levels and random sampling. Holm, de Lichtenberg and Thorup presented the deterministic algorithm with $O(\log^2 n)$ amortized updates at STOC 1998 and in the Journal of the ACM in 2001, together with results for minimum spanning forests, 2-edge connectivity and biconnectivity. Thorup (2000) and later authors improved the randomized bound, and Wulff-Nilsen (2013) the deterministic one, toward the $\Omega(\log n)$ lower bound of Pătraşcu and Demaine.

## References
