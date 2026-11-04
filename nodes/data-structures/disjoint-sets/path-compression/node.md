---
tag: 41H33R
kind: technique
slug: path-compression
name: Path compression
aliases:
- full path compression
area: data-structures/disjoint-sets
level: core
summary: During find, point every node on the path directly to the root.
prereqs: [disjoint-set-forest, rooted-tree]
see_also: [union-by-rank, path-halving, path-splitting, union-find-amortized-bound, inverse-ackermann-function, offline-subarray-painting, tarjan-offline-lca]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 19.3 (the path compression heuristic, the two-pass FIND-SET, and the bound for path compression alone) and Section 19.4
  - paper: doi:10.1145/62.2160
    title: "Robert E. Tarjan and Jan van Leeuwen, Worst-case analysis of set union algorithms, Journal of the ACM 31(2) (1984), 245-281"
    locator: the compaction rules (compression, splitting, halving) and their bounds with and without a linking rule
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.5, weighted quick-union with path compression
  - paper: doi:10.1145/321879.321884
    title: "Robert Endre Tarjan, Efficiency of a Good But Not Linear Set Union Algorithm, Journal of the ACM 22(2) (1975), 215-225"
    locator: the analysis of path compression with union by rank
---

Path compression is a rule for the find operation of a [disjoint-set forest](/disjoint-set-forest/): after the walk from a node $x$ to its root, make each node of the walk a child of the root. It does at most twice the work of the walk, keeps all sets the same, and makes later finds of these nodes take one step. With [union by rank](/union-by-rank/) it gives the bound $O(m\,\alpha(m, n))$ of [Tarjan's union-find bound](/union-find-amortized-bound/), where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/). Alone, with any linking, it gives $O(\log n)$ amortized time per operation when there are at least $n$ finds.

## In plain words

Each element points to another element, and the chain of pointers ends at the leader of the group. To find the leader, you follow the chain. The walk can be long.

Path compression says: once you know the leader, go back along the chain you just walked and make each element on it point straight at the leader. The groups do not change, only the shortcuts. The next time you ask about any of these elements, or about anything that hangs below them, the walk is much shorter.

The walk you pay for now saves time on later walks. Over many operations, the total work becomes almost linear.

## When it applies

- **Finds walk up a tree to a root.** The structure is a forest of parent pointers and the answer of a query is the root, or a value at the root.
- **Any node of a path may point to any later node.** The answer for a node does not depend on which node of its path is its parent. This is true for a plain forest. With [weighted union-find](/weighted-union-find/), it is true if the weight of the new edge is the sum of the weights along the old path.
- **Amortized bounds are good enough.** One find can still cost $\Theta(\log n)$ with union by rank, or $\Theta(n)$ without a linking rule. Only the total is small.
- **No undo.** Path compression changes many pointers in one find, so an undo stack would need to record them all. Structures that roll back, such as [union-find with rollback](/union-find-with-rollback/), leave it out.

## The template

```pseudo id=main
FIND(x)                                   ▷ recursive form
L1  if x.p ≠ x then
L2      x.p ← FIND(x.p)
L3  return x.p

FIND-ITERATIVE(x)                         ▷ two passes, no recursion
L4  r ← x
L5  while r.p ≠ r do r ← r.p              ▷ first pass: find the root
L6  while x.p ≠ r do                      ▷ second pass: repoint the path
L7      next ← x.p
L8      x.p ← r
L9      ⟨UPDATE⟩(x)                       ▷ hole: fix data stored on the edge, if any
L10     x ← next
L11 return r
```

The recursive form climbs to the root and sets each parent on the way back. Its depth is the length of the path, so with no linking rule it can overflow the stack. The iterative form does the same with two loops. The hole ⟨UPDATE⟩ is empty for a plain forest. For a [weighted union-find](/weighted-union-find/) it combines the weights of the old path, and then the two passes must run from the root down, so the recursive form or an explicit stack is simpler.

**Why it is safe.** Let $x_0, x_1, \ldots, x_k$ be the path from $x = x_0$ to the root $r = x_k$. The rule sets $x_i.p \leftarrow r$ for $0 \le i \le k - 2$. Each node $y$ of the tree reaches $r$ before and after, so each set keeps its members and its root. With union by rank, $x_i.rank < x_{i+1}.rank < \cdots < r.rank$, so the new parent has a larger rank than the node, and the rank invariant of [union by rank](/union-by-rank/) holds. No rank changes.

**Cost.** The two passes take $2k + O(1)$ steps for a path of $k$ edges, and they change $k - 1$ pointers when $k \ge 1$. So path compression changes the cost of one find by a constant factor at most, and saves work on all later finds of the $k - 1$ nodes and of their descendants.

### The bounds

Let $n$ be the number of elements, with $n$ MAKE-SET operations, at most $n - 1$ unions, and $f$ finds.

| linking rule | compaction | total time | source |
|---|---|---|---|
| any ([quick-union](/quick-union/)) | none | $O(n + nf)$, and a chain gives $\Theta(nf)$ | Sedgewick and Wayne, Section 1.5 |
| by rank or size | none | $\Theta(n + f \log n)$ | [union by rank](/union-by-rank/) |
| any | full path compression | $\Theta(n + f (1 + \log_{2 + f/n} n))$ | CLRS Section 19.3, Tarjan and van Leeuwen |
| by rank or size | full path compression | $\Theta(n + f\,\alpha(f + n, n))$ | Tarjan (1975) |

The third row says that compression alone is already good: for $f = n$ finds the cost is $\Theta(n \log n)$, so $O(\log n)$ amortized per operation, and for $f = n^{1 + \varepsilon}$ finds it is $O(f/\varepsilon)$, a constant per find for each fixed $\varepsilon > 0$. The last row is the inverse Ackermann bound. The same rows hold for [path halving](/path-halving/) and [path splitting](/path-splitting/) in place of full compression, by Tarjan and van Leeuwen.

## Classic examples

### One find on a binomial tree

Build a tree of 8 nodes with union by rank: link $0 \to 1$, $2 \to 3$, $4 \to 5$, $6 \to 7$, then $1 \to 3$, $5 \to 7$, and last $3 \to 7$. The parents of 0 to 7 are $[1, 3, 3, 7, 5, 7, 7, 7]$, and the depths are $[3, 2, 2, 1, 2, 1, 1, 0]$, with a sum of 12. FIND$(0)$ walks $0, 1, 3, 7$. Path compression sets $0.p \leftarrow 7$ and $1.p \leftarrow 7$; the parent of 3 is already 7. The parents become $[7, 7, 3, 7, 5, 7, 7, 7]$, and the depths $[1, 1, 2, 1, 2, 1, 1, 0]$, with a sum of 9. Node 2 keeps depth 2, because it is not on the path; it would gain from a find on 2.

### A chain

Without a linking rule, the unions $(0, 1), (1, 2), \ldots, (6, 7)$ that put the first root under the second make the chain $0 \to 1 \to \cdots \to 7$. FIND$(0)$ walks 7 edges and changes the parents of 0 to 5 to 7. After that each node is at depth 1, and each find costs at most 1 step until the next union.

### Where it is used

- [Disjoint-set forest](/disjoint-set-forest/) with union by rank or size, the standard union-find.
- [Painting subarrays offline](/offline-subarray-painting/): each cell points to the next unpainted cell, and compression makes the jumps over painted runs short.
- [Offline RMQ by Arpa's trick](/arpa-offline-rmq/): the links follow a stack, so no linking rule applies, and compression alone gives the bound.
- [Tarjan's offline LCA algorithm](/tarjan-offline-lca/) and [Kruskal's algorithm](/kruskal/).
- [Weighted union-find](/weighted-union-find/) and [union-find with distances](/dsu-with-distances-to-representative/): the edge data is combined while the path is compressed.

## Variations

- **[Path halving](/path-halving/).** Make every other node of the path point to its grandparent, in one pass. It changes about half as many pointers.
- **[Path splitting](/path-splitting/).** Make every node of the path point to its grandparent, in one pass.
- **Path reversal.** Make the node $x$ the new root and reverse the path. It is rarely used for union-find.
- **Compression on union only.** Some codes compress only in the finds that UNION calls. The bounds still hold, since those finds are part of the sequence, but the finds of `connected` then gain nothing.

## Pitfalls

- **Recursion on a long path.** The recursive form of lines L1 to L3 uses one stack frame per edge. Without union by rank, a chain of $10^5$ nodes overflows the default stack of Python. Use the two-pass loop.
- **Compression with rollback.** Rolling back a union restores an old shape, but a compressed path may point past the undone link. Either do not compress, or record every pointer change.
- **Compression without fixing edge data.** In a weighted structure, setting $x.p \leftarrow r$ without the hole ⟨UPDATE⟩ loses the weights of the skipped edges. The weight of $x$ must become the sum along its old path to $r$.
- **Changing ranks.** Path compression must not update ranks to the new heights. The analysis needs ranks that never fall, and the true heights cost too much to keep.
- **Expecting a worst-case bound.** One find after a sequence of unions can still cost $\Theta(\log n)$ with union by rank. Path compression does not improve the worst case of one operation.

## Exercises

1. Show that the two-pass form and the recursive form make the same changes of parents.
2. With no linking rule, give a sequence of $n - 1$ unions and $n$ finds on $n = 2^k$ elements that costs $\Omega(n \log n)$ with full path compression.
3. Prove that path compression keeps the rank invariant $x.rank < x.p.rank$.
4. Write the recursive form for a forest that stores a sum $w(x)$ on each edge from $x$ to $x.p$, so that after FIND$(x)$ the value $w(x)$ is the sum of the weights from $x$ to the root.

## References
