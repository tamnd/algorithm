---
tag: C4CPMJ
kind: technique
slug: offline-deletion
name: Offline deletion
aliases:
- segment tree over time
- line segment tree divide and conquer
area: data-structures/range-query-structures
level: advanced
summary: Technique that handles deletions by processing operations offline, often reversing time or using divide and conquer, to avoid hard deletes.
prereqs: [segment-tree, rollback-technique, offline-query-processing]
see_also: [union-find-with-rollback, offline-dynamic-connectivity, dynamic-connectivity, dsu-with-parity, divide-and-conquer-on-queries, mo-algorithm-with-updates, decremental-connectivity, persistent-segment-tree]
sources:
  - url: https://cp-algorithms.com/data_structures/deleting_in_log_n.html
    title: cp-algorithms, Deleting from a data structure in O(T(n) log n)
    locator: the sections Algorithm (a segment tree over the queries, each lifetime split into O(log n) nodes, a DFS that adds on entry and undoes on exit with a stack of changes) and Notes, and the Implementation for dynamic connectivity
  - url: https://oi-wiki.org/topic/segment-tree-offline/
    title: OI Wiki, 线段树与离线询问 (segment trees and offline queries, also called 线段树分治)
    locator: the introduction (simulating deletion with a structure that supports undo), the section 过程 (the total cost O(n log n (T(n) + M(n))) and the remark that undo breaks amortized bounds) and the example luogu P5787 (bipartiteness with a union-find with parity, union by rank and no path compression)
---

Offline deletion is the technique of supporting deletions in a structure that only supports insertions, by reading all operations first and changing the order in which the structure sees them. In its main form, each item gets its *lifetime*, the interval of time steps during which it is present, and the lifetime is stored on the $O(\log T)$ canonical nodes of a [segment tree](/segment-tree/) over the $T$ time steps. A depth-first walk of this tree inserts the items of a node on entry and undoes them on exit with the [rollback technique](/rollback-technique/), so at each leaf the structure holds exactly the items alive at that time. If one insertion costs $O(I)$ and can be undone at the same cost, all $m$ items cost $O(m I \log T)$ in total, with no deletion code at all.

## In plain words

Some tools are easy to add to and hard to take things out of. A union-find structure is the usual example: joining two groups is quick, but splitting a group again is not.

If you know the whole story in advance, you can avoid taking things out. Write down, for each item, from which moment to which moment it exists. Then visit the moments in a nested way, like the chapters and sections of a book. When you open a chapter, add the items that exist for the whole chapter. When you close it, undo exactly those additions, in reverse order. At each single moment, the tool then holds the right items, and you only ever add or undo the last thing you added.

## When it applies

- All operations are known in advance, so the answers may come after the whole input is read; this is the [offline](/offline-query-processing/) setting.
- The structure supports INSERT and a way to undo the *most recent* insertion, at about the same cost. This holds for any structure whose insertion changes $O(I)$ memory words that can be logged, such as [union-find with rollback](/union-find-with-rollback/) (union by size or rank, no path compression), a linear basis over $\mathrm{GF}(2)$, a knapsack table, or the set of a hash map.
- A query depends only on the set of items present at its time, not on the order in which they came.
- Either deletions of arbitrary items are mixed with insertions and queries, which needs the segment tree over time, or the operations only delete, in which case reversing time is enough.

## The template

Number the time steps $0, \ldots, T - 1$, one per operation or one per query. An item inserted at step $s$ and deleted at step $e$ is alive on $[s, e)$; an item never deleted is alive on $[s, T)$.

```pseudo id=main
OFFLINE-DELETION(items, queries, T)        ▷ items with lifetimes [s, e), queries with times
L1  for each item x with lifetime [s, e) do
L2      store x on the canonical nodes of [s, e) in a segment tree over [0, T)
L3  VISIT(root)

VISIT(v)                                   ▷ v covers the time steps [lo, hi)
L4  mark ← the size of the undo stack
L5  for each item x stored on v do INSERT(x), pushing its changes on the undo stack
L6  if v is a leaf for time t then answer the queries of time t
L7  else VISIT(left(v)), VISIT(right(v))
L8  while the undo stack is larger than mark do undo its top change
```

**Invariant.** On entry to line L6 or L7 at a node $v$ over $[lo, hi)$, the structure holds exactly the items whose lifetime contains all of $[lo, hi)$ and that are stored on $v$ or an ancestor of $v$. For a leaf $t$, these are exactly the items alive at $t$, because the canonical nodes of $[s, e)$ are disjoint and cover it, so $t \in [s, e)$ if and only if one of them lies on the path from the root to $t$. Line L8 restores the state on entry to $v$, since undo reverses the changes of line L5 and of the recursive calls, which each restored their own state.

**Cost.** Each item is stored on at most $2 \lceil \lg T \rceil$ nodes, so line L5 runs $O(m \log T)$ insertions in total, and line L8 undoes each of them once. With insertions and undos in $O(I)$ worst-case time and queries in $O(Q)$, the total is $O(m I \log T + q Q + T)$, and the space is $O(m \log T + T)$ for the tree plus the undo stack. The bound must be worst case per insertion: an amortized bound breaks, because the walk can undo and redo the same expensive step many times.

**Reverse time.** If the operations are only deletions and queries, start from the final set, answer the queries from the last to the first, and turn each deletion into an insertion. This needs no undo and costs $O(m I + q Q)$.

## Classic examples

**Dynamic connectivity.** Edges are added and removed, and queries ask for the number of connected components, or whether $u$ and $v$ are connected. Store each edge on its lifetime nodes; INSERT is a union in a union-find with union by size, which changes $O(1)$ words, and FIND takes $O(\log n)$ without path compression. The total is $O(m \log T \log n)$, which is [offline dynamic connectivity](/offline-dynamic-connectivity/).

Take four vertices and the operations at steps 0 to 3: add $e_1 = \{1, 2\}$, add $e_2 = \{2, 3\}$, delete $e_1$, add $e_3 = \{3, 4\}$, with a query for the number of components after each step. The lifetimes are $e_1$ on $[0, 2)$, $e_2$ on $[1, 4)$ and $e_3$ on $[3, 4)$. In a tree over $[0, 4)$, $e_1$ is stored on the node $[0, 2)$, $e_2$ on the leaf $1$ and the node $[2, 4)$, and $e_3$ on the leaf $3$.

| node visited | inserted on entry | components | answer |
|---|---|---|---|
| $[0, 4)$ | none | 4 | |
| $[0, 2)$ | $e_1$ | 3 | |
| leaf 0 | none | 3 | 3 |
| leaf 1 | $e_2$ | 2 | 2, then undo $e_2$ |
| $[2, 4)$ | $e_2$, after undoing $e_1$ on leaving $[0, 2)$ | 3 | |
| leaf 2 | none | 3 | 3 |
| leaf 3 | $e_3$ | 2 | 2 |

The answers $3, 2, 3, 2$ match the graphs $\{e_1\}$, $\{e_1, e_2\}$, $\{e_2\}$ and $\{e_2, e_3\}$.

**Dynamic bipartiteness.** The same walk with a [union-find with parity](/dsu-with-parity/) tells after each step whether the graph is bipartite; OI Wiki uses it as the model problem.

**Linear basis under deletions.** Insertion into an XOR basis of $b$-bit numbers changes one slot and costs $O(b)$; with the time tree, queries "the largest XOR of a subset of the current set" under insertions and deletions take $O(m b \log T)$.

**Deleting edges, reverse time.** Edges are only deleted and queries ask for the number of components. Start from the graph with all edges that are never deleted, then add the edges back from the last deletion to the first, with full path compression, in $O((m + q) \alpha(n))$.

## Variations

- **Divide and conquer without a tree.** The same walk can be written as a recursion on $[lo, hi)$ that passes down the list of items whose lifetime meets the interval; items that cover it are inserted, the others are passed on. This is the form of [divide and conquer on queries](/divide-and-conquer-on-queries/).
- **Removing one kind of item.** To answer "the answer without the items of colour $c$" for every colour $c$, make each colour a time step and let every item be alive on all steps except its own colour, as in the second OI Wiki example.
- **Persistent structures.** A persistent version of the structure also allows going back in time, at the cost of more memory; the undo stack is cheaper when the walk is depth first.
- **Online alternatives.** Fully dynamic connectivity has online solutions with polylogarithmic amortized time per operation, such as [dynamic connectivity](/dynamic-connectivity/) by Holm, de Lichtenberg and Thorup, which are much harder to write.
- **Point updates in Mo's order.** [Mo's algorithm with updates](/mo-algorithm-with-updates/) handles a different kind of deletion, overwriting array values, by moving through time step by step.

## Pitfalls

- **Path compression.** Undo needs the changes of an insertion to be few and logged. Path compression changes many parents and is amortized; use union by size or rank only, which keeps FIND at $O(\log n)$.
- **Amortized structures in general.** A structure with amortized $O(1)$ insertion can take $\Theta(n)$ on one insertion, and the walk may repeat that insertion at many nodes. Use structures with worst-case bounds.
- **Lifetimes that are off by one.** An item deleted at step $e$ must not be present at the query of step $e$ if the query comes after the deletion. Decide whether time steps are operations or queries, and make the intervals half open.
- **The same item inserted twice.** If an edge is added again after a deletion, it has two lifetimes, and each must be stored separately; a map from the item to the start of its open lifetime handles this.
- **Memory of the walk.** The walk has depth $\lceil \lg T \rceil + 1$. The undo stack holds only the insertions of the nodes on the current root-to-leaf path, and the canonical nodes of one lifetime are disjoint, so it holds at most one insertion per item, $O(m I)$ words. The $O(m \log T)$ lists on the tree are the larger cost.

## Exercises

1. Show that an item with lifetime $[s, e)$ is stored on at most two nodes per level of the time tree.
2. A graph gets edge insertions and deletions, and queries ask whether the graph is bipartite. Give the full algorithm and its cost.
3. Explain why union-find with path compression and union by rank cannot be used in the walk, even though it is faster without undo.
4. Edges are only deleted. Solve the components queries by reversing time, and compare the cost with the time-tree method.
5. A multiset of numbers gets insertions, deletions and queries "the largest XOR of two numbers in the set". Can the time tree with a binary trie answer them? What does undo need?

## References
