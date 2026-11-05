---
tag: MH2HKP
kind: technique
slug: dynamic-fractional-cascading
name: Dynamic fractional cascading
aliases:
- dynamic cascading
area: searching/fractional-cascading
level: research
summary: A variant of fractional cascading that supports insertions and deletions in the catalogs while keeping fast multiple-list search.
prereqs: [fractional-cascading-bridge, catalog-graph, multiple-list-search, b-tree]
see_also: [fractional-cascading-lower-bound, layered-range-tree, segment-tree, dynamic-range-searching, pointer-machine, hive-graph]
sources:
  - paper: doi:10.1007/BF01840386
    title: Kurt Mehlhorn and Stefan Naher, Dynamic fractional cascading, Algorithmica 5 (1990)
    locator: pages 215 to 241 (search in O(log N + k log log N) time, insert and delete in O(log log N) amortized time, and O(1) in the insert-only or delete-only case; dynamic segment and range trees)
  - paper: doi:10.1007/BF01840440
    title: Bernard Chazelle and Leonidas J. Guibas, Fractional cascading I, A data structuring technique, Algorithmica 1 (1986)
    locator: pages 133 to 162 (the dynamic part of the paper)
  - paper: "Peyman Afshani, A lower bound for dynamic fractional cascading, Proceedings of the ACM-SIAM Symposium on Discrete Algorithms (SODA 2021), arXiv:2011.00503"
    locator: Section 1 (the survey of the upper bounds of Chazelle and Guibas, Mehlhorn and Naher, Dietz and Raman, and Giora and Kaplan; the lower bound and its model)
---

Dynamic fractional cascading keeps a [fractional cascading](/fractional-cascading-bridge/) structure correct while single items are inserted into and deleted from the catalogs of a [catalog graph](/catalog-graph/). The static structure answers a [multiple list search](/multiple-list-search/) over $k$ catalogs in $O(\log N + k)$ time, where $N$ is the total size; with updates, the best bounds known on a [pointer machine](/pointer-machine/) are $O(\log N + k \log \log N)$ per query and $O(\log \log N)$ per update, by Mehlhorn and Naher (amortized) and by Dietz and Raman (worst case). The technique keeps the gaps between bridges within fixed limits, as a [B-tree](/b-tree/) keeps its nodes within fixed sizes. Afshani proved in 2021 that the extra factor on the query cannot be removed entirely in that model.

## In plain words

The static method copies every second item of each list into the list before it, and each copy remembers its place. A search then needs a step or two per list.

Now items arrive and leave. A new item lands between two copies, so the stretch between two copies grows. If it gets too long, the search becomes slow again. The fix is the one that a B-tree uses for a full node: when a stretch gets too long, cut it in the middle by copying its middle item to the list before. That copy is itself a new item in that list, so it can make a stretch there too long, and the cut can pass further back. Because each list passes on only a fraction of its items, these chains of cuts are short on average. Deletions work the same way, with stretches that get too short.

## When it applies

- The search is a multiple list search on a catalog graph of small degree: one key located in many sorted lists along a path or tree.
- The catalogs change, one item at a time, and each update comes with a pointer to the place of the change (the item to delete, or the neighbour of the item to insert). The structure does not search for the place itself.
- Queries must stay fast after each update, so rebuilding the static structure from scratch, at $\Theta(N)$ per rebuild, is too slow.
- Typical hosts are dynamic [segment trees](/segment-tree/) and dynamic [range trees](/range-tree/), where an update of one segment or point changes the catalogs of $O(\log n)$ nodes on a root-to-leaf path.

## The template

```pseudo id=main
INSERT(v, y, at)                       ▷ add key y to catalog C_v; at: its position in A_v
L1  insert y into C_v and into the augmented catalog A_v at position at
L2  for each edge vu whose range contains y do
L3      g ← the gap of A_v between the two bridges of vu around y
L4      if |g| > b then                    ▷ hole: the gap limit b, a constant times the degree
L5          z ← the middle element of g
L6          make z a bridge of vu: INSERT(u, copy of z, its position in A_u)   ▷ a copy, not a catalog item of u
L7          split the next-bridge structure of vu at z    ▷ hole: a union-split-find structure

QUERY(x, v_1, v_2, ..., v_k)            ▷ the path may be chosen step by step
L8  p ← the position of succ(x) in A_{v_1}, by binary search
L9  for i ← 1 to k do
L10     report the successor of x in C_{v_i}, read from p
L11     if i < k then
L12         z ← NEXT-BRIDGE(p, v_i v_{i+1})          ▷ hole: the first bridge of the edge at or after p
L13         p ← the position of z in A_{v_{i+1}}; move back within the gap of z to succ(x)
```

**The holes.** The gap limit $b$ sets the trade-off. A larger $b$ makes overflows rarer but each step of the query longer. Deletion is the mirror case: when a gap becomes too short, merge it with a neighbour by removing a bridge, which deletes a copy from $A_u$ and can make a gap of $A_u$ too short. With lower and upper limits that differ by a constant factor, as the node sizes of a B-tree, the amortized number of overflows and underflows per update is $O(1)$.

**The hard hole.** Line L12 needs the first bridge of a given edge at or after a position of $A_{v_i}$. In the static structure each element stores this answer as a pointer. In the dynamic structure, a new bridge would change this pointer for every element of its gap in $A_{v_i}$, and these gaps can hold many items of $C_{v_i}$. So line L12 becomes a search in a dynamic partition of a list into intervals, where line L7 splits an interval, and this is the union-split-find problem. On a pointer machine it costs $O(\log \log N)$ per operation, and this is the source of the extra $\log \log N$ factor in the query and in the update.

**The walk-through.** Lines L1 to L7 keep the gap invariant of the static structure: each gap that a query crosses has at most $b$ elements. Lines L8 to L13 are the static query, with the stored pointer replaced by the call of line L12. The cascade of line L6 goes from $v$ to its neighbours and can return, which is why the analysis needs a potential argument and why the bounds are amortized.

### The known bounds

| structure | query | update | notes |
|---|---|---|---|
| static fractional cascading, rebuilt after each update | $O(\log N + k)$ | $\Theta(N)$ | baseline |
| Chazelle and Guibas, insertions only or deletions only | $O(\log N + k)$ | $O(\log N)$ amortized | Part I |
| Chazelle and Guibas, both kinds of update | $O(\log N + k \log \log N)$ | | Part I |
| Mehlhorn and Naher | $O(\log N + k \log \log N)$ | $O(\log \log N)$ amortized | $O(1)$ amortized with only insertions or only deletions |
| Dietz and Raman | $O(\log N + k \log \log N)$ | $O(\log \log N)$ worst case | as reported by Afshani |
| Giora and Kaplan | $O(\log N + k(\log \log N + \log d))$ | | degree $d$, as reported by Afshani |

**The lower bound.** Afshani proved that on a pointer machine, a fully dynamic structure with polylogarithmic amortized update time, or an insert-only structure with polylogarithmic worst-case update time, has worst-case query time $\Omega(\log N \sqrt{\log \log N})$ for some path queries of length $O(\log N)$. A static structure answers such queries in $O(\log N)$ time, so the dynamic problem is strictly harder in this model. The gap between $\sqrt{\log \log N}$ and $\log \log N$ per step remains open.

## Classic examples

- **Dynamic segment trees.** In a [segment tree](/segment-tree/) with sorted lists at the nodes, a query walks a root-to-leaf path of length $O(\log n)$, and an update changes $O(\log n)$ lists. Mehlhorn and Naher get $O(\log n \log \log n)$ time for queries, insertions and deletions, against $O(\log^2 n)$ with a balanced tree in each node.
- **Dynamic range trees.** The same holds for a dynamic [layered range tree](/layered-range-tree/) for [orthogonal range reporting](/orthogonal-range-reporting/), with the output size added to the query time. See also [dynamic range searching](/dynamic-range-searching/).
- **Dynamic orthogonal segment intersection.** The vertical query of [orthogonal segment intersection](/orthogonal-segment-intersection/) searches its $x$-coordinate in the lists of a segment tree on the $y$-coordinates. With dynamic cascading, segments can be added and removed between queries.
- **Insert-only catalogs.** When items are only added, as in an offline sweep that inserts segments one by one, the cheaper semi-dynamic bounds apply, with $O(1)$ amortized time per insertion in the bound of Mehlhorn and Naher.

## Variations

- **Global rebuilding for deletions.** Mark deleted items instead of removing them, and rebuild the whole structure after a constant fraction of the items is marked. Each rebuild costs $O(N)$ and is paid for by $\Omega(N)$ deletions, so the amortized cost per deletion is $O(1)$. This works only while the marked items do not slow the queries too much.
- **Worst-case bounds.** Dietz and Raman remove the amortization from the update bound of Mehlhorn and Naher, so that each single update costs $O(\log \log N)$.
- **Bounded degree only in ranges.** The edge ranges of the catalog graph allow nodes of high fan-out, as in a B-tree, as long as each key lies in the ranges of few edges at each node. Giora and Kaplan make the dependence on the degree $d$ additive.
- **The model of the lower bound.** In the model of Afshani, a memory cell holds one catalog value and at most two pointers, and a query pays for each pointer it follows. His bound says nothing about structures that compute addresses, as on a [word RAM](/word-ram/).

## Pitfalls

- **Updating stored pointers.** Keeping the static next-bridge pointer in each element makes a new bridge cost the length of its gap, which is not bounded by a constant. This is the step that needs the union-split-find structure of line L7.
- **Copies of copies.** A bridge inserted into $A_u$ by line L6 is an element of $A_u$, so it can itself be copied on. It is not an item of $C_u$, and the query must never report it as an answer for $C_u$. Mark copies and keep, for each element of $A_u$, a way to reach the successor in $C_u$.
- **Overflows that never stop.** If each overflow passed more than one copy on for each item it receives, the cascade could grow without bound. The fraction of items passed on must be small enough that each level receives fewer copies than it gains, as in the space bound of the static structure.
- **Quoting amortized bounds as worst-case.** The bounds of Chazelle and Guibas and of Mehlhorn and Naher for updates are amortized. A single update can cause a long cascade.
- **The position is part of the input.** The update bound $O(\log \log N)$ assumes that the update gives the position of the change. Finding that position costs a search, $O(\log N)$ in general.

## Exercises

1. In the static path structure of the [bridge](/fractional-cascading-bridge/) page, insert a new item into $C_i$ and into $M_i$ only. Show that the query stays correct if the test of one position before $\mathit{down}_i[p]$ is replaced by a backward scan, and that the scan costs at most the number of items of $M_{i+1}$ between two consecutive bridges.
2. In the insert-only path structure with gap limit $b = 3$, show that a gap that overflows has received at least two insertions since it was created. Conclude that $j$ insertions into $M_{i+1}$ cause at most $j/2$ insertions of copies into $M_i$, and that a single insertion causes $O(1)$ insertions into all lists in the amortized sense.
3. Explain why the global rebuilding of the Variations section does not give an $O(\log N + k)$ query bound under a long run of insertions, even when the rebuild is triggered after each $N/2$ updates.

## References
