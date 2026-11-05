---
tag: 08JB9Z
kind: algorithm
slug: italiano-dynamic-transitive-closure
name: Italiano's dynamic transitive closure algorithm
aliases:
- Italiano algorithm
area: graphs/dynamic-graphs
level: research
summary: Maintains reachability of a directed graph under edge insertions and deletions.
solves: [dynamic-transitive-closure]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {amortized: O(n)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [transitive-closure, reachability, incremental-graph]
see_also: [dynamic-transitive-closure, dynamic-reachability, decremental-graph, directed-acyclic-graph, even-shiloach-tree, incremental-topological-ordering, floyd-warshall, amortized-update-time]
sources:
  - paper: "Giuseppe F. Italiano, Amortized efficiency of a path retrieval data structure, Theoretical Computer Science 48, 273 to 281 (1986)"
    locator: the whole paper (one reachability tree per vertex, insertions in O(n) amortized time, constant-time queries, paths in time proportional to their length)
  - paper: "Giuseppe F. Italiano, Finding paths and deleting edges in directed acyclic graphs, Information Processing Letters 28(1), 5 to 11 (1988)"
    locator: the whole paper (edge deletions in directed acyclic graphs in O(mn) total time, with the same queries)
  - paper: "Camil Demetrescu and Giuseppe F. Italiano, Fully dynamic transitive closure: breaking through the O(n^2) barrier, Proceedings of the 41st IEEE Symposium on Foundations of Computer Science (FOCS 2000), 381 to 389"
    locator: Section 1 (survey of the earlier incremental and decremental methods and the fully dynamic bounds)
---

Italiano's algorithm keeps the transitive closure of a directed graph, the answer to "can $x$ reach $y$?" for every pair, as one spanning tree of reachable vertices per source. A query reads one entry of an $n \times n$ table, and a path from $x$ to $y$ is read by following parent pointers, in time proportional to its length. The 1986 paper handles **edge insertions only**, in any directed graph, in $O(n)$ amortized time per insertion: a new edge $(i, j)$ grafts the part of the tree of $j$ that is new to $x$ onto the tree of each $x$ that reaches $i$. The 1988 paper handles **edge deletions only**, in [directed acyclic graphs](/directed-acyclic-graph/), in $O(mn)$ total time. Both are deterministic. The two halves do not combine into a fully dynamic algorithm with the same bounds.

## In plain words

For every starting point, keep a family tree of all the places it can reach: each reachable place records the place it was reached from. Asking whether one place reaches another is then a single lookup, and the route is found by walking back up the tree.

When a new one-way road from $i$ to $j$ opens, every start that reaches $i$ now also reaches everything that $j$ reaches. So copy the tree of $j$ into the tree of that start, hanging it below $i$. Skip any branch whose top is already in the tree, since its whole branch is already reachable.

Each pair of start and place is added only once, which keeps the total work small.

## The problem

The input is a number $n$ of vertices and a sequence of operations on a directed graph, starting with no edges:

- $\mathrm{insert}(i, j)$ adds the edge $(i, j)$;
- $\mathrm{reachable}(x, y)$ asks whether there is a path from $x$ to $y$;
- $\mathrm{path}(x, y)$ returns such a path, or reports that there is none.

This is the [incremental](/incremental-graph/) form of [dynamic transitive closure](/dynamic-transitive-closure/). In the decremental form, the graph starts as a given acyclic graph and the updates delete edges.

## The algorithm

For each vertex $x$ the structure keeps the **reachability tree** $\mathrm{desc}(x)$: a tree rooted at $x$ that spans the vertices reachable from $x$, made of graph edges, stored as an array $\mathrm{par}_x$ with an entry for "not reachable", and with child lists.

```pseudo id=main
INSERT(i, j)
L1  add the edge (i, j)
L2  for each vertex x with i ∈ desc(x) and j ∉ desc(x):
L3      walk desc(j) from j, depth first, skipping every subtree whose top w is already in desc(x)
L4      add each visited w to desc(x), with parent i if w = j and otherwise its parent in desc(j)

REACHABLE(x, y)
L5  return whether y ∈ desc(x)

PATH(x, y)
L6  follow par_x from y up to x and return the vertices in reverse

DELETE(u, v)                         ▷ deletions only, in a DAG
L7  remove the edge (u, v)
L8  for each x where u is the parent of v in desc(x): Q ← {v}, ordered by topological number
L9      take w with the least number; advance its pointer past edges (z, w) with z ∉ desc(x)
L10     if an edge (z, w) is found then hook w below z, else remove w from desc(x) and put its children into Q
```

Line L2 picks the trees that grow. If $j$ is already in $\mathrm{desc}(x)$, the new edge gives $x$ nothing new, because everything reachable from $j$ was reachable from $x$ before. Line L3 prunes at a vertex $w$ already in $\mathrm{desc}(x)$ for the same reason: all of $w$'s subtree in $\mathrm{desc}(j)$ is reachable from $w$, and so already in $\mathrm{desc}(x)$. Line L4 copies the shape of $\mathrm{desc}(j)$, so every tree edge is a graph edge and paths can be read back. The tree of $j$ itself does not change during the insertion: $j \in \mathrm{desc}(j)$ always.

**Deletions in a DAG.** For deletions only, fix a topological numbering of the acyclic graph. Each vertex $w$ in $\mathrm{desc}(x)$ keeps a pointer into its list of in-edges, at its tree parent; the edges before the pointer come from vertices that are no longer reachable from $x$, or were deleted (lines L7 to L10). Processing in topological order makes the test $z \in \mathrm{desc}(x)$ final: an in-neighbor of $w$ has a smaller number, so its status is already settled. A vertex not reachable from $x$ never becomes reachable again, so each pointer moves only forward.

## Example

Insert the edges $(0, 1)$, $(2, 3)$, $(3, 4)$, $(1, 2)$, $(4, 0)$ into a graph on five vertices. The table shows the rows of the reachability table and the number of pairs added.

| edge | row 0 | row 1 | row 2 | row 3 | row 4 | pairs added |
|---|---|---|---|---|---|---|
| $(0, 1)$ | 11000 | 01000 | 00100 | 00010 | 00001 | 1 |
| $(2, 3)$ | 11000 | 01000 | 00110 | 00010 | 00001 | 1 |
| $(3, 4)$ | 11000 | 01000 | 00111 | 00011 | 00001 | 2 |
| $(1, 2)$ | 11111 | 01111 | 00111 | 00011 | 00001 | 6 |
| $(4, 0)$ | 11111 | 11111 | 11111 | 11111 | 11111 | 10 |

Inserting $(1, 2)$ grows the trees of 0 and 1, the vertices that reach 1. For $x = 0$, the walk copies the tree of 2, which is the path $2 \to 3 \to 4$, below 1, so $\mathrm{desc}(0)$ becomes the path $0, 1, 2, 3, 4$. Inserting $(4, 0)$ makes the graph one cycle; for $x = 2$, the walk of $\mathrm{desc}(0)$ adds 0 below 4 and 1 below 0, and prunes at 2, which is already there. In total 20 pairs are added, one for each pair that becomes reachable.

For deletions, take the DAG with edges $(0, 1)$, $(0, 2)$, $(1, 3)$, $(2, 3)$, $(3, 4)$. In $\mathrm{desc}(0)$, vertex 3 hangs below 1. Deleting $(1, 3)$ makes 3 an orphan in the trees of 0 and 1. In $\mathrm{desc}(0)$, its pointer moves on to the edge $(2, 3)$, and 3 hangs below 2; in $\mathrm{desc}(1)$ it finds no reachable in-neighbor, so 3 and then its child 4 leave the tree. Deleting $(2, 3)$ then removes 3 and 4 from $\mathrm{desc}(0)$ and $\mathrm{desc}(2)$.

## Correctness

The invariant is that $\mathrm{desc}(x)$ is a tree of graph edges rooted at $x$ whose vertex set is exactly the set of vertices reachable from $x$. An insertion of $(i, j)$ makes the new reachable set of $x$ equal to the old one together with the set reachable from $j$, if $x$ reaches $i$, and leaves it unchanged otherwise. The walk of lines L3 and L4 adds exactly the vertices of $\mathrm{desc}(j)$ that are new, each below a vertex already in the tree, so the result is again a tree of graph edges. For deletions, processing orphans in topological order decides the status of every in-neighbor before it is used. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Insertions.** Line L2 checks $n$ vertices, $O(n)$ per insertion. The walk of lines L3 and L4 adds a new pair $(x, w)$ for every visited vertex that is not pruned, and each pruned vertex is a child in $\mathrm{desc}(j)$ of an added vertex, or $j$ itself, which is never pruned there. So the walk costs $O(1)$ per added pair plus $O(1)$. At most $n^2$ pairs are ever added, so $m$ insertions take $O(mn + n^2)$ time, which is $O(n)$ amortized per insertion when $m \ge n$. A single insertion can take $\Theta(n^2)$ time.
- **Queries.** $O(1)$ for reachability and $O(k)$ for a path with $k$ edges.
- **Deletions in a DAG.** For each source, each in-edge pointer moves forward at most $m$ times in total, and each vertex leaves the tree at most once. Italiano's bound is $O(mn)$ total time for any sequence of deletions; the implementation here uses a binary heap for the topological order and takes $O(mn \log n)$.
- **Space.** $O(n^2)$ for the table and the trees, plus the pointers for deletions.
- **Kind of bound.** Amortized and deterministic.

## Properties

- **Insertions only, or deletions only in a DAG.** Mixing the two loses the bounds: an insertion can make an unreachable vertex reachable, which breaks the monotone pointers of deletions.
- **Path retrieval.** Paths come with the answer at no extra cost, which was the purpose of the 1986 paper.
- **Amortized.** The $O(n)$ bound is for a long sequence; one insertion can add $\Theta(n^2)$ pairs.
- **Deterministic.**

## Variants and improvements

- **Cycles in the decremental case.** In general digraphs, deletions can split strongly connected components, and the method above fails. Decremental algorithms for general digraphs keep the components first; La Poutré and van Leeuwen, and later Roditty and Zwick, gave such algorithms.
- **Fully dynamic.** Fully dynamic transitive closure has $O(n^2)$ amortized update time with constant query time (Demetrescu and Italiano, 2000, and Roditty, 2003), and subquadratic update times with slower queries; see [dynamic transitive closure](/dynamic-transitive-closure/) and [dynamic reachability](/dynamic-reachability/).
- **Single source.** For one source, the incremental case is a search that only extends, and the decremental case is an [Even-Shiloach tree](/even-shiloach-tree/) with no depth bound, or faster methods.
- **Topological order.** When only acyclicity matters, [incremental topological ordering](/incremental-topological-ordering/) is cheaper than full closure.

## When to use it

Use it when a directed graph only grows, or an acyclic graph only shrinks, and many reachability or path questions are asked between the updates. The $O(n^2)$ space limits it to graphs of a few thousand to tens of thousands of vertices. For a graph that does not change, compute the closure once with a search from each vertex or with [Floyd-Warshall](/floyd-warshall/). For few queries, run a search per query instead.

## Pitfalls

- **Pruning too little.** Without the pruning at line L3, the walk of $\mathrm{desc}(j)$ visits its whole tree for every $x$, and the bound becomes $O(n^2)$ per insertion.
- **Walking the graph instead of the tree.** Walking the edges of the graph from $j$ costs $O(m)$ per source. The tree of $j$ has at most $n - 1$ edges.
- **Deleting in a graph with cycles.** In a cycle, two vertices can serve as each other's parent after the real path is gone. The decremental method needs an acyclic graph.
- **Processing orphans in the wrong order.** Without topological order, an orphan may hook below another orphan that is about to leave the tree.

## Implementations

## History

Italiano introduced the reachability trees in 1986 for incremental path retrieval and in 1988 extended them to deletions in acyclic graphs. Together with work by La Poutré and van Leeuwen, these were the first dynamic transitive closure algorithms with good amortized bounds. Henzinger and King (1995) gave the first fully dynamic algorithm with sublinear query time, and Demetrescu and Italiano (2000) and King (1999) reached $O(n^2)$ amortized updates with fast queries.

## References
