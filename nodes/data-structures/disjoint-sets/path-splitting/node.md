---
tag: YT2KWQ
kind: technique
slug: path-splitting
name: Path splitting
area: data-structures/disjoint-sets
level: core
summary: During find, make every node on the path point to its grandparent, updating all nodes on the path.
prereqs: [disjoint-set-forest, path-compression]
see_also: [path-halving, path-compression, union-by-rank, union-by-size, union-find-amortized-bound, weighted-union-find]
sources:
  - paper: doi:10.1145/62.2160
    title: "Robert E. Tarjan and Jan van Leeuwen, Worst-case analysis of set union algorithms, Journal of the ACM 31(2) (1984), 245-281"
    locator: the compaction rules (compression, splitting, halving) and the bounds for each with and without a linking rule
  - book: isbn:9780898711875
    title: Robert E. Tarjan, Data Structures and Network Algorithms, SIAM, 1983
    locator: Chapter 2, Disjoint sets (compression, splitting and halving)
---

Path splitting is a rule for the find operation of a [disjoint-set forest](/disjoint-set-forest/): walk up from $x$, and make every node of the path point to its grandparent. It needs one pass and no recursion. The path splits into two paths, one through the nodes at even positions and one through the nodes at odd positions, each about half as long. Tarjan and van Leeuwen proved that it has the same bounds as full [path compression](/path-compression/): with [union by rank](/union-by-rank/) or [by size](/union-by-size/), $m$ operations on $n$ elements take $O(m\,\alpha(m, n))$ time.

## In plain words

To find the leader of a group, you climb from boss to boss. Path splitting changes each node that you pass. Before you leave a node, you tell it to skip its boss and point at its boss's boss. Then you step to the old boss, not to the boss's boss, and do the same there.

So you still visit every node of the chain, and every one of them now skips one step. The one long chain becomes two chains side by side, each about half as long: one through the first, third and fifth nodes, and one through the second, fourth and sixth. You do this in the same single walk up.

## When it applies

- **A forest of parent pointers with finds.** The structure is a [disjoint-set forest](/disjoint-set-forest/), or any forest where a query climbs to a root.
- **Any node may point to any of its ancestors.** With edge data, the data of the new edge must be the combination of the two old edges.
- **One pass is wanted.** The code must not recurse or keep a stack.
- **No undo.** As with compression, the changes of a find are not recorded, so it does not suit [union-find with rollback](/union-find-with-rollback/).

## The template

```pseudo id=main
FIND(x)                                   ▷ path splitting
L1  while x.p ≠ x do
L2      y ← x.p
L3      ⟨UPDATE⟩(x, y)                    ▷ hole: combine edge data, if any
L4      x.p ← y.p                         ▷ skip the parent
L5      x ← y                             ▷ step to the old parent
L6  return x
```

For the path $x_0, x_1, \ldots, x_k$ with root $x_k$, the loop visits $x_0, x_1, \ldots, x_{k-1}$ and sets $x_i.p \leftarrow x_{i+2}$ for $i \le k - 2$. At $x_{k-1}$, the grandparent is the root itself, so line L4 changes nothing. Line L2 saves the old parent before line L4 changes it, so line L5 steps to the next node of the old path.

The hole ⟨UPDATE⟩ is empty for a plain forest. If each node stores a value $w(x)$ for the edge to its parent, with $w(r) = 0$ at each root, the hole is $w(x) \leftarrow w(x) + w(y)$. When the loop reaches $x$, the edge from $y$ to its parent has not changed yet, because the loop changes the nodes in order from the bottom, so $w(y)$ is still the value of the old edge from $y$ to $x_{i+2}$.

**Why it is safe.** Each new parent is an ancestor of the node, so roots and sets do not change. With union by rank, ranks increase along the path, so the new parent has a larger rank than the node.

**Cost.** For a path of $k$ edges, the loop runs $k$ times with two reads and one write each. It writes about twice as often as [path halving](/path-halving/), and about as often as two-pass compression, but in one pass.

### The bounds

Tarjan and van Leeuwen (1984) proved for $n$ elements, at most $n - 1$ unions and $f$ finds:

| linking rule | compaction | total time |
|---|---|---|
| any | splitting | $O(n + f (1 + \log_{2 + f/n} n))$ |
| by rank or size | splitting | $O(n + f\,\alpha(f + n, n))$ |

These are the bounds of full compression and of halving.

## Classic examples

### One find on a chain

Take the chain $0 \to 1 \to \cdots \to 6$ with root 6, with depths $6, 5, \ldots, 0$ and a sum of 21. FIND$(0)$ with splitting visits 0 to 5:

| visit | change | parents of 0 to 6 |
|---|---|---|
| start | | 1 2 3 4 5 6 6 |
| $x = 0$ | 0.p ← 2 | 2 2 3 4 5 6 6 |
| $x = 1$ | 1.p ← 3 | 2 3 3 4 5 6 6 |
| $x = 2$ | 2.p ← 4 | 2 3 4 4 5 6 6 |
| $x = 3$ | 3.p ← 5 | 2 3 4 5 5 6 6 |
| $x = 4$ | 4.p ← 6 | 2 3 4 5 6 6 6 |
| $x = 5$ | parent is the root, no change | 2 3 4 5 6 6 6 |

The path is now two paths into the root: $0 \to 2 \to 4 \to 6$ and $1 \to 3 \to 5 \to 6$. The depths are $3, 3, 2, 2, 1, 1, 0$, with a sum of 12, the same sum as [path halving](/path-halving/) gives, but each node of the path was changed.

### Where it is used

- The [disjoint-set forest](/disjoint-set-forest/) with union by rank or size, as a one-pass find with the same bounds as compression.
- [Kruskal's algorithm](/kruskal/), where a short find loop helps.
- [Weighted union-find](/weighted-union-find/), with the weight update in the hole.

## Variations

- **[Path halving](/path-halving/).** Change only every other node, and jump to the grandparent. Half the writes, the same bounds.
- **[Path compression](/path-compression/).** Point every node to the root, with two passes or recursion.
- **Splitting with no linking rule.** It still gives $O(\log n)$ amortized time per operation when there are at least $n$ finds.

## Pitfalls

- **Stepping to the new parent.** Line L5 must step to the saved old parent $y$. Code that steps with `x ← x.p` after line L4 jumps to the grandparent, which is path halving, and skips half of the updates that splitting makes.
- **Not saving the parent.** Without line L2, the code must read `x.p` after changing it, and it then loses the old parent. Save it first.
- **Updating the weight after the link.** In a weighted structure, line L3 must run before line L4, while $y$ is still the parent of $x$. After line L4, `w(x.p)` is the weight of a different edge.

## Exercises

1. Show that after a splitting find on a path of $k$ edges, the nodes at even positions and the nodes at odd positions form two paths, and give their lengths.
2. Prove that path splitting keeps the rank invariant of union by rank.
3. Compare the number of writes of halving, splitting and two-pass compression on a path of $k$ edges.

## References
