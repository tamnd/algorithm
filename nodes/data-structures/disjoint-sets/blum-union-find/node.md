---
tag: YNSV90
kind: data-structure
slug: blum-union-find
name: Blum's disjoint-set structure
aliases:
- Blum union-find
area: data-structures/disjoint-sets
level: research
summary: Disjoint-set structure with logarithmic worst-case time per single operation.
implements: [disjoint-set]
model: word-ram
complexity:
  vars: {n: the number of elements}
  time: {worst: O(log n / log log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [disjoint-set-forest, union-by-rank, rooted-tree]
see_also: [disjoint-set-forest, union-by-rank, union-find-lower-bound, fredman-saks-lower-bound, dynamic-equivalence-problem, amortized-vs-worst-case, union-find-with-rollback]
sources:
  - paper: doi:10.1137/0215072
    title: "Norbert Blum, On the Single-Operation Worst-Case Time Complexity of the Disjoint Set Union Problem, SIAM Journal on Computing 15(4) (1986), 1021-1024"
    locator: the k-UF trees, the union and find procedures, the choice of k, and the lower bound for separable algorithms
  - paper: doi:10.1145/73007.73040
    title: "Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, Proceedings of the 21st Annual ACM Symposium on Theory of Computing (1989), 345-354"
    locator: Theorem 6, the cell-probe lower bound for the worst case of one operation
  - paper: "Stephen Alstrup, Amir M. Ben-Amram and Theis Rauhe, Worst-case and amortised optimality in union-find, Proceedings of the 31st Annual ACM Symposium on Theory of Computing (1999)"
    locator: the structure that is optimal both in the worst case and amortized
---

Blum's disjoint-set structure supports UNION and FIND in $O(\log n/\log\log n)$ time in the *worst case* for each single operation, not only amortized. It stores each set as a *$k$-UF tree*: the elements are the leaves, all at the same depth, the root has at least two children, and every other inner node has at least $k$ children. A find walks from a leaf to the root in $O(\log_k n)$ steps, and a union moves fewer than $k$ children or adds one edge, in $O(k)$ steps. With $k = \lceil \lg n/\lg\lg n \rceil$ both costs are $O(\log n/\log\log n)$. Blum (1986) proved this optimal for separable pointer algorithms, and Fredman and Saks (1989) proved it optimal in the cell-probe model. The [disjoint-set forest](/disjoint-set-forest/) with [path compression](/path-compression/) is faster on average, but a single find there can take $\Theta(\log n)$ time.

## In plain words

Each group is a tree, with the members at the bottom, all at the same level. Every branching point in the middle has many branches, at least $k$ of them. So the tree is very flat, and the walk from a member to the top is short.

To join two groups, put the flatter tree into the taller one at the right level, so that all members stay at the same level. If the top of the flatter tree has few branches, do not keep it: hand its few branches to a node of the other tree. Either way, the join moves only a few pointers.

Choosing $k$ well balances the two costs. No step is ever slow, not even once.

## The abstract type

The structure implements the [disjoint-set](/disjoint-set/) type on the elements $0, \ldots, n - 1$, which start as singletons: `find(x)` returns the name of the set of $x$, `union(x, y)` merges two sets, and `connected(x, y)` tests whether two elements are in one set. The point of the structure is the bound for each operation, as discussed under [amortized versus worst case](/amortized-vs-worst-case/).

## Representation

Each set is a rooted tree whose leaves are the elements of the set. Each node has a parent pointer, a list of children and a height, the length of its paths down to the leaves. The root stores the name of the set, an element of it. Fix an integer $k \ge 2$.

**Invariant (K), the $k$-UF tree.** In each tree:

1. all leaves have the same depth, the height $h$ of the root;
2. the root has at least 2 children, unless it is a leaf ($h = 0$);
3. every inner node that is not the root has at least $k$ children.

**Height bound.** A tree of height $h \ge 1$ has at least $2k^{h-1}$ leaves, by (K). So every tree has height at most $1 + \log_k(n/2)$.

## Operations

```pseudo id=main
FIND(x)
L1  while x.p ≠ NIL do x ← x.p
L2  return x.name

UNION(x, y)
L3  r ← ROOT(x); s ← ROOT(y); if r = s then return false
L4  if r.h < s.h then swap r and s                 ▷ now r is at least as tall
L5  if r.h = s.h then
L6      if r.h = 0 or (r.deg ≥ k and s.deg ≥ k) then
            make a new root t with the children r and s; t.h ← r.h + 1; t.name ← r.name; return true
L7      if r.deg < s.deg then swap r and s          ▷ now s.deg < k
L8      move every child of s to r; return true
L9  if s.h = 0 or s.deg ≥ k then
L10     v ← the node of height s.h + 1 on the leftmost path of r; make s a child of v
L11 else v ← the node of height s.h on the leftmost path of r; move every child of s to v
L12 return true
```

ROOT is lines L1 and L2 without the name. Here $s.deg$ is the number of children of $s$.

- **Equal heights** (lines L5 to L8). Two leaves, or two roots that both have at least $k$ children, go under a new root, and the height grows by one. Otherwise one root has fewer than $k$ children, and those children move to the other root; the emptied root is dropped.
- **Different heights** (lines L9 to L11). If $s$ may become an inner node, because it is a leaf or has at least $k$ children, it becomes a child of a node of $r$ one level above it. Otherwise its fewer than $k$ children move to a node of $r$ at the height of $s$. Either way, the leaves of $s$ end at the depth of the leaves of $r$.

## Example

Let $n = 9$ and $k = 3$. The inner nodes get the letters A to E in order of creation.

| step | case | trees after it |
|---|---|---|
| union(0, 1) | two leaves: new root A | A{0, 1} |
| union(2, 3) | two leaves: new root B | A{0, 1}, B{2, 3} |
| union(0, 2) | equal heights 1, degrees 2 and 2 below $k$: move the children of B to A | A{0, 1, 2, 3} |
| union(4, 5) | new root C | A{0, 1, 2, 3}, C{4, 5} |
| union(6, 4) | heights 1 and 0: leaf 6 becomes a child of C | A{0, 1, 2, 3}, C{4, 5, 6} |
| union(7, 8) | new root D | A, C, D{7, 8} |
| union(0, 4) | equal heights 1, degrees 4 and 3, both at least $k$: new root E | E{A, C}, D{7, 8} |
| union(7, 0) | heights 2 and 1, D has 2 children: move 7 and 8 to A, the node of height 1 on the leftmost path of E | E{A{0, 1, 2, 3, 7, 8}, C{4, 5, 6}} |

At the end, every leaf has depth 2, the root E has 2 children, and A and C have 6 and 3 children, at least $k = 3$. FIND(8) takes 2 steps, from 8 to A and from A to E.

## Correctness

Each union keeps (K), and the leaves of the new tree are the leaves of the two old trees. A find returns the name stored at the root, which is an element of the set. The case analysis:

- **Line L6.** Two trees of equal height $h$ go under a new root of height $h + 1$: the leaves are at depth $h + 1$, the new root has 2 children, and the old roots become inner non-root nodes, which is allowed because each has at least $k$ children, or they are leaves.
- **Line L8.** The children of $s$, at height $h - 1$, become children of $r$, at height $h$, so the leaves keep their depth $h$. The root $r$ keeps at least 2 children.
- **Line L10.** $s$ goes under a node of height $s.h + 1$, so its leaves get depth $r.h$. It is a leaf or has at least $k$ children, as an inner non-root must.
- **Line L11.** The children of $s$ go under a node of height $s.h$; their leaves get depth $r.h$. The node $v$ gains children, which keeps (K).

The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | worst case |
|---|---|
| find | $O(\log_k n)$ |
| union | $O(k + \log_k n)$: two root walks, one walk down, and fewer than $k$ moves |
| with $k = \lceil \lg n/\lg\lg n \rceil$ | $O(\log n/\log\log n)$ for each operation |
| space | $\Theta(n)$ |

A find walks the height, at most $1 + \log_k(n/2)$ edges. A union finds two roots, walks down the leftmost path of $r$ for at most its height, and then either links one node, $O(1)$, or moves fewer than $k$ children, $O(k)$. For $k = \lg n/\lg\lg n$, $\lg k = \lg\lg n - \lg\lg\lg n$, which is at least $\frac12 \lg\lg n$ for large $n$, so $\log_k n = \lg n/\lg k = O(\lg n/\lg\lg n)$, and $k$ has the same order. There are at most $n - 1$ new inner nodes in all, because each new root merges two trees, so the space is linear.

**Lower bounds.** Blum proved that each separable pointer algorithm needs $\Omega(\log n/\log\log n)$ time for some single operation, and Fredman and Saks proved the same bound in the [cell-probe model](/cell-probe-model/) with words of polylogarithmic size (see the [Fredman-Saks lower bound](/fredman-saks-lower-bound/)). So the structure is optimal for the worst case of one operation.

## Variants

- **Another value of $k$.** A larger $k$ makes finds faster and unions slower: $O(\log_k n)$ against $O(k)$. If finds are much more frequent, choose $k$ larger.
- **Optimal in both senses.** Alstrup, Ben-Amram and Rauhe (1999) gave a structure that keeps the worst case $O(\log n/\log\log n)$ for each operation and also has the amortized bound $O(\alpha)$ of path compression.
- **Union by rank alone.** The [disjoint-set forest](/disjoint-set-forest/) with [union by rank](/union-by-rank/) and no compression has worst case $O(\log n)$ per find and $O(1)$ per link; Blum's trees improve the worst case by a factor of $\log\log n$.
- **Undo.** Each union changes $O(k)$ pointers and could be recorded on a stack, as in [union-find with rollback](/union-find-with-rollback/).

## When to use it

Use it when each single operation has a deadline, as in real-time systems, or when the analysis of an algorithm needs a worst-case bound per operation. For total running time, the forest with union by rank and path compression is simpler and faster.

## Pitfalls

- **Children of mixed height.** A node of height $s.h + 1$ must be found on the tree $r$; linking $s$ to the root of $r$ when $r.h > s.h + 1$ breaks the equal depth of the leaves.
- **Linking a small root as an inner node.** A root with fewer than $k$ children must not become an inner non-root node. Move its children instead, which is what keeps the trees flat.
- **Choice of $k$ for small $n$.** For small $n$, $\lg n/\lg\lg n$ is below 2. Use $k \ge 2$, or the trees can be paths.
- **Names.** When children move from $s$ to $r$, the set takes the name of $r$; code that kept the name of $s$ must read the name again.

## Implementations

The Python class `BlumUnionFind(n, k=None)` keeps parent pointers, child lists and heights in arrays, with new inner nodes after the $n$ leaves. It chooses $k = \max(2, \lceil \lg n/\lg\lg n \rceil)$ by default. `check_invariant` checks (K), the links in both directions, the height bound and the names.

## History

Blum (1986) gave the $k$-UF trees and proved the matching lower bound for separable pointer algorithms. Fredman and Saks (1989) extended the lower bound to the cell-probe model. Alstrup, Ben-Amram and Rauhe (1999) combined the worst-case bound with the amortized inverse Ackermann bound.

## References
