---
tag: XE7KKB
kind: technique
slug: path-halving
name: Path halving
aliases:
- one-pass path compression
area: data-structures/disjoint-sets
level: core
summary: During find, make every node point to its grandparent while walking up in one pass.
prereqs: [disjoint-set-forest, path-compression]
see_also: [path-splitting, path-compression, union-by-rank, union-by-size, union-find-amortized-bound, weighted-union-find, dsu-with-parity]
sources:
  - paper: doi:10.1145/62.2160
    title: "Robert E. Tarjan and Jan van Leeuwen, Worst-case analysis of set union algorithms, Journal of the ACM 31(2) (1984), 245-281"
    locator: the compaction rules (compression, splitting, halving) and the bounds for each with and without a linking rule
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.5, weighted quick-union with path compression (the one-line form that sets each examined node to its grandparent)
  - book: isbn:9780898711875
    title: Robert E. Tarjan, Data Structures and Network Algorithms, SIAM, 1983
    locator: Chapter 2, Disjoint sets (compression, splitting and halving)
---

Path halving is a rule for the find operation of a [disjoint-set forest](/disjoint-set-forest/): walk up from $x$, and at every other node of the path, set its parent to its grandparent. It needs one pass, no recursion and no stack, and it roughly halves the length of the path. Tarjan and van Leeuwen proved that it has the same bounds as full [path compression](/path-compression/): with [union by rank](/union-by-rank/) or [by size](/union-by-size/), $m$ operations on $n$ elements take $O(m\,\alpha(m, n))$ time. Because it changes each edge using only the next edge, it also works directly with data stored on the edges, as in [weighted union-find](/weighted-union-find/).

## In plain words

To find the leader of a group, you climb from boss to boss. Path halving adds one small change to each climb. Before you leave a node, you tell it to skip its boss and point at its boss's boss. Then you jump straight to that boss's boss, and do the same there.

So you visit every second node of the chain, and each visited node now skips one step. The chain becomes about half as long. You do this in the same single walk up, so there is no second walk and nothing to remember. After a few finds through the same nodes, the paths are short.

## When it applies

- **A forest of parent pointers with finds.** The structure is a [disjoint-set forest](/disjoint-set-forest/), or any forest where a query climbs to a root.
- **Any node may point to any of its ancestors.** As for path compression, the answer must not depend on which ancestor is the parent. With edge data, the data of the new edge must be the combination of the two old edges.
- **One pass is wanted.** The code must not recurse, for example in Python or on a small stack, or a second pass is too costly.
- **No undo.** As with compression, the changes of a find are many and are not recorded, so it does not suit [union-find with rollback](/union-find-with-rollback/).

## The template

```pseudo id=main
FIND(x)                                   ▷ path halving
L1  while x.p ≠ x do
L2      ⟨UPDATE⟩(x, x.p)                  ▷ hole: combine edge data, if any
L3      x.p ← x.p.p                       ▷ skip the parent
L4      x ← x.p                           ▷ jump to the old grandparent
L5  return x
```

The loop runs while $x$ is not a root. Line L3 makes the grandparent the new parent of $x$; when the parent of $x$ is the root, the grandparent is the root too, and line L3 changes nothing. Line L4 then moves $x$ to its new parent, so the loop visits the nodes $x_0, x_2, x_4, \ldots$ of the path $x_0, x_1, x_2, \ldots, x_k$, and sets $x_{2i}.p \leftarrow x_{2i+2}$.

The hole ⟨UPDATE⟩ is empty for a plain forest. If each node stores a value $w(x)$ for the edge to its parent, with $w(r) = 0$ at each root, the hole is $w(x) \leftarrow w(x) + w(x.p)$, which gives the value of the new edge from $x$ to its grandparent. The update uses only two edges that are next to each other, so no second pass and no root-first order is needed. This is the main advantage of halving over the two-pass form of [path compression](/path-compression/).

**Why it is safe.** Each new parent is an ancestor of the node, so each node keeps its root, and each set keeps its members. With union by rank, $x.rank < x.p.rank < x.p.p.rank$, so the rank invariant holds after line L3.

**Cost.** For a path of $k$ edges, the loop runs $\lceil k/2 \rceil$ times with two reads and one write each, less than the $2k$ steps of two-pass compression.

### The bounds

Tarjan and van Leeuwen (1984) proved for $n$ elements, at most $n - 1$ unions and $f$ finds:

| linking rule | compaction | total time |
|---|---|---|
| any | halving | $O(n + f (1 + \log_{2 + f/n} n))$ |
| by rank or size | halving | $O(n + f\,\alpha(f + n, n))$ |

These are the same bounds as for full compression. So the [union-find bound](/union-find-amortized-bound/) holds with halving in place of compression, and the [union-find lower bound](/union-find-lower-bound/) shows that no rule can do better.

## Classic examples

### One find on a chain

Take the chain $0 \to 1 \to 2 \to \cdots \to 6$ with root 6, which [quick-union](/quick-union/) builds with the unions $(0, 1), (1, 2), \ldots, (5, 6)$. The depths are $6, 5, \ldots, 0$, with a sum of 21. FIND$(0)$ with halving visits 0, 2 and 4:

| visit | change | parents of 0 to 6 |
|---|---|---|
| start | | 1 2 3 4 5 6 6 |
| $x = 0$ | 0.p ← 2 | 2 2 3 4 5 6 6 |
| $x = 2$ | 2.p ← 4 | 2 2 4 4 5 6 6 |
| $x = 4$ | 4.p ← 6 | 2 2 4 4 6 6 6 |
| $x = 6$ | root, stop | |

The depths are now $3, 3, 2, 2, 1, 1, 0$, with a sum of 12. Full compression would give the sum 6, and [path splitting](/path-splitting/) gives 12 too, with a different shape. A second FIND$(0)$ visits 0 and 4 and leaves depth 2 for 0.

### Where it is used

- The [disjoint-set forest](/disjoint-set-forest/): halving with union by size or rank is a common choice for a short, iterative find. Sedgewick and Wayne give the one-line form `id[p] = id[id[p]]` in the find loop.
- [Kruskal's algorithm](/kruskal/) and [connected component labeling](/connected-component-labeling/), where a one-pass find keeps the inner loop small.
- [Weighted union-find](/weighted-union-find/) and [union-find with parity](/dsu-with-parity/): the hole adds the weight, or the parity, of the skipped edge.

## Variations

- **[Path splitting](/path-splitting/).** Set the parent of *every* node of the path to its grandparent, not every other one. It does twice the writes and splits the path into two.
- **[Path compression](/path-compression/).** Set the parent of every node of the path to the root. It needs two passes or recursion.
- **Halving without a linking rule.** With [quick-union](/quick-union/) linking, halving still gives $O(\log n)$ amortized time per operation when there are at least $n$ finds.

## Pitfalls

- **Moving before the write.** Swapping lines L3 and L4 moves $x$ to its parent first and then changes the parent of that node. The start node keeps its parent, so a find from a node at depth 2 changes nothing for it. The sets stay right, but the start node, which is the one most likely to be found again, gains nothing. Keep L3 before L4.
- **Reading the parent twice with changing data.** In a weighted structure, line L2 must use the weight of the old parent before line L3 changes the parent of $x$. Doing L3 first adds the weight of the wrong edge.
- **A missing root weight.** The update $w(x) \leftarrow w(x) + w(x.p)$ assumes $w(r) = 0$ at each root, so that a step whose parent is the root does not change $w(x)$. Keep the root weight at 0 in UNION.
- **Expecting full compression.** After one halving find, a node can still have depth about half the old depth. Code that assumes a find leaves each node of the path at depth 1, for example to read a root value from the parent, is wrong.

## Exercises

1. Show that a path of $k$ edges has $\lceil k/2 \rceil$ edges from $x$ to the root after one halving find from $x$.
2. Prove that path halving keeps the rank invariant $x.rank < x.p.rank$ of union by rank.
3. Write the hole ⟨UPDATE⟩ for a forest where each edge stores a bit, and the query asks for the parity of the path from $x$ to the root.
4. How many halving finds from the deepest node of a chain of $2^k$ nodes are needed before that node has depth at most 1?

## References
