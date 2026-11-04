---
tag: MK70WC
kind: data-structure
slug: tango-tree
name: Tango tree
area: data-structures/search-trees
level: research
summary: Online BST with O(log log n) competitive ratio against the best offline BST.
implements: [ordered-set]
model: pointer-machine
complexity:
  vars: {n: the number of keys, m: the number of accesses}
  time: {worst: O(log n log log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [dynamic-optimality-conjecture, red-black-tree, binary-search-tree]
see_also: [splay-tree, competitive-ratio, online-algorithm, working-set-theorem, static-optimality-theorem, treap-split, treap-merge, link-cut-tree]
sources:
  - paper: doi:10.1137/S0097539705447347
    title: Erik D. Demaine, Dion Harmon, John Iacono and Mihai Pătraşcu, Dynamic optimality, almost, SIAM Journal on Computing 37(1), 2007
    locator: the interleave lower bound, the tango tree, and its analysis
  - paper: doi:10.1137/0218004
    title: Robert Wilber, Lower bounds for accessing binary search trees with rotations, SIAM Journal on Computing 18(1), 1989
    locator: the first lower bound (the interleave bound)
---

A tango tree is an online binary search tree whose cost on each access sequence is at most $O(\log \log n)$ times the cost of the best offline BST algorithm for that sequence. Demaine, Harmon, Iacono and Pătraşcu introduced it in 2004 (journal version 2007). It was the first BST with a competitive ratio of $o(\log n)$, a step toward the [dynamic optimality conjecture](/dynamic-optimality-conjecture/). The idea is to keep a fixed balanced reference tree, split it into *preferred paths* that follow the most recent accesses, and store each path as a small balanced BST of $O(\log n)$ nodes. An access then costs $O(\log \log n)$ for each change of a preferred path, and the number of changes is Wilber's interleave lower bound on the optimum.

## In plain words

Picture a balanced search tree that never changes. At each node, remember which way the last search through that node went. Following these marks from the root gives a path, and the marks below split the tree into many such paths.

A search follows marks as long as they point the right way, and it has to leave a path only where a mark points the wrong way. Each such point is a place where every possible search tree must also pay something, as Wilber proved. A tango tree stores each path in a small tree of its own, so that it can jump along a path and repair the marks quickly. So it pays only a little more than the best possible tree, a factor that grows like $\log \log n$.

## The abstract type

A tango tree stores a fixed set of $n$ keys, here $1, \ldots, n$, and serves a sequence of accesses $x_1, \ldots, x_m$ (successful searches), in the BST model: each access starts at the root, and the structure may rotate. The aim is the cost bound relative to $\mathrm{OPT}$, the cost of the best offline BST algorithm for the sequence. Inserts and deletes are not part of the original structure.

## Representation

- **Reference tree.** $P$ is the perfectly balanced BST on the keys, of height $\lfloor \lg n \rfloor$. It does not change; it is used only to define the paths.
- **Preferred children.** Each node $y$ of $P$ has a preferred child: left if the most recent access in the subtree of $y$ was to $y$ or to its left subtree, right if it was to the right subtree, and none if there was no access in the subtree yet.
- **Preferred paths.** Following preferred children from a node whose parent does not prefer it gives a *preferred path*. The paths partition the nodes of $P$; each path has at most $\lfloor \lg n \rfloor + 1$ nodes.
- **Auxiliary trees.** Each path is stored as a red-black tree on its keys, an *auxiliary tree*, in which each node also stores its depth in $P$ and the minimum and maximum depth in its subtree. The auxiliary trees are hung below each other so that the whole is one BST on all keys: the auxiliary tree of a path hangs at the place, in the auxiliary tree of the path above, where its key interval falls.

**Invariant.** (T1) The preferred paths are the chains of preferred children, and each is stored, sorted by key, in its auxiliary tree. (T2) The top of each path other than the root is a child $c$ in $P$ whose parent does not prefer $c$.

The Python code keeps each path as a sorted list and the paths in a table by their top node; it does not build the red-black trees.

## Operations

```pseudo id=main
ACCESS(x)
L1  A ← the path that holds the root of P; S ← empty list
L2  loop
L3      search for x in the auxiliary tree of A
L4      if x is on A then exit the loop
L5      u ← the deeper, in P, of the predecessor and the successor of x on A
L6      c ← the child of u in P on the side of x; append (u, c) to S
L7      A ← the path whose top is c
L8  for each (u, c) in S, from the top down do
L9      CUT the path of u below u; the cut part becomes a path whose top is the old preferred child of u
L10     JOIN the path of u, which now ends at u, with the path whose top is c; make c the preferred child of u
L11 if the preferred child of x is not left then CUT below x, JOIN with the path of the left child of x, and make left the preferred child of x
```

**Where the search leaves a path.** If $x$ is not on the path $A$, the search for $x$ in $P$ leaves $A$ at the deepest node $u$ of $A$ whose subtree holds $x$. Every node of $A$ in the subtree of $u$, other than $u$, lies on the side away from $x$, so $u$ is the neighbour of $x$ among the keys of $A$ on one side, and the neighbour on the other side is an ancestor of $u$. So $u$ is the deeper of the two neighbours (line L5).

**Cut and join.** The nodes of the path of $u$ below $u$ are exactly the nodes of the path whose keys lie in the key interval of the old preferred child of $u$. In the auxiliary tree, this is a contiguous key range: CUT splits the red-black tree at the two ends of that range, and JOIN concatenates the path of $c$ into the gap at its key interval. With the depth fields, the range is found from the depths, and each split or concatenate of red-black trees of $O(\log n)$ nodes takes $O(\log \log n)$ time.

**Preferred child of $x$.** After the access, the most recent access in the subtree of $x$ is $x$ itself, so the preferred child of $x$ becomes left (line L11).

## Example

Take $n = 7$; $P$ has root 4, children 2 and 6, and leaves 1, 3, 5, 7. At first no node has a preferred child, and each node is a path of its own.

| access | paths visited | L-R switches | preferred children after | paths after |
|---|---|---|---|---|
| 1 | 3: $\{4\}$, $\{2\}$, $\{1\}$ | 0 | 4: L, 2: L, 1: L | $\{1, 2, 4\}$ and singletons |
| 3 | 2: $\{1, 2, 4\}$, $\{3\}$ | 1 (at 2) | 2: R, 3: L | $\{2, 3, 4\}$, $\{1\}$, ... |
| 6 | 2: $\{2, 3, 4\}$, $\{6\}$ | 1 (at 4) | 4: R, 6: L | $\{4, 5, 6\}$, $\{2, 3\}$, $\{1\}$, $\{7\}$ |
| 2 | 2: $\{4, 5, 6\}$, $\{2, 3\}$ | 2 (at 4, at 2) | 4: L, 2: L | $\{1, 2, 4\}$, $\{5, 6\}$, $\{3\}$, $\{7\}$ |
| 7 | 3: $\{1, 2, 4\}$, $\{5, 6\}$, $\{7\}$ | 2 (at 4, at 6) | 4: R, 6: R, 7: L | $\{4, 6, 7\}$, $\{1, 2\}$, $\{3\}$, $\{5\}$ |

In the access to 2, the search for 2 in the path $\{4, 5, 6\}$ finds the neighbours: none on the left, and 4 on the right, so $u = 4$ and the search goes to the path whose top is 2, where it finds 2. Then the path of 4 is cut below 4 (the part $\{5, 6\}$ becomes its own path) and joined with $\{2, 3\}$; at 2, the preferred child was right, so $\{3\}$ is cut off and $\{1\}$ is joined. The total of L-R switches over the five accesses is 6, which equals Wilber's interleave bound of the sequence $1, 3, 6, 2, 7$ on this reference tree.

## Correctness

Each access ends at $x$, because the loop of lines L2 to L7 moves to the path that holds the subtree of $P$ where $x$ lies, one level of paths at a time, and a path that holds $x$ ends the loop. The updates of lines L8 to L11 set the preferred children of all nodes on the root-to-$x$ path of $P$ to the side of $x$, and the preferred child of $x$ to left, which is the definition, and the cuts and joins change the paths exactly as the preferred children change, so (T1) and (T2) hold again. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $k_i$ be the number of nodes whose preferred child changes from left to right or from right to left during access $i$, and let $K = \sum_i k_i$.

- **Per access.** The access visits at most $k_i + 1$ paths plus the paths where a node gets its first preferred child, which happens at most once per node over the whole sequence. Each visited path costs a search, a cut and a join in a red-black tree of $O(\log n)$ nodes, so $O(\log \log n)$ time. So access $i$ costs $O((k_i + 1 + f_i)(1 + \log \log n))$, with $\sum_i f_i \le n$. In the worst case $k_i \le \lg n + 1$, so one access costs $O(\log n \log \log n)$.
- **Interleave bound.** $K$ is exactly the interleave bound $\mathrm{IB}(X)$ of Wilber for the reference tree $P$: for each node $y$, the preferred child of $y$ changes sides exactly when an access in the subtree of $y$ is on the other side of $y$ from the previous one.
- **Competitive ratio.** Wilber's theorem gives $\mathrm{OPT}(X) \ge \mathrm{IB}(X)/2 - n$, and $\mathrm{OPT}(X) \ge m$. So the total cost is $O((\mathrm{IB}(X) + m + n)(1 + \log \log n)) = O((\mathrm{OPT}(X) + n)\log \log n)$.

| quantity | bound |
|---|---|
| one access | $O((k + 1)(1 + \log \log n))$ plus first choices; $O(\log n \log \log n)$ worst |
| $m$ accesses | $O((\mathrm{OPT} + n) \log \log n)$ |
| space | $\Theta(n)$ |

The [complexity proof](proofs/complexity.md) counts the paths and the switches. In the Python code, the search in a path is a binary search with at most $\lceil \lg(\lg n + 2) \rceil$ comparisons, as in the real structure, but cut and join are list slices and cost $O(\log n)$ element moves, not $O(\log \log n)$.

## Variants

- **Multi-splay trees.** Wang, Derryberry and Sleator (2006) store each preferred path as a splay tree. They are also $O(\log \log n)$-competitive, and in addition they cost $O(\log n)$ amortized per access.
- **Chain-splay and other variants.** Later structures, such as the zipper tree, keep the $O(\log \log n)$ ratio and also have $O(\log n)$ worst-case access time.
- **Link-cut trees.** The [link-cut trees](/link-cut-tree/) of Sleator and Tarjan use the same decomposition into preferred paths, each stored in a splay tree, for dynamic trees.

## When to use it

Tango trees are a theoretical result: they show that an online BST can be within $O(\log \log n)$ of the offline optimum on every sequence. In practice the constant factors are large, and on typical sequences a [splay tree](/splay-tree/) or a balanced tree is faster. A tango tree can be worse than a balanced tree by a factor of $\Theta(\log \log n)$ on some sequences, for example random accesses.

## Pitfalls

- **The deeper neighbour.** The node where the search leaves a path is the *deeper* of the predecessor and the successor of $x$ on the path, not the nearer one by key. Choosing by key goes to a wrong subtree.
- **The preferred child of $x$.** Accessing $x$ itself counts as a left access in the subtree of $x$. Forgetting line L11 makes the count of switches differ from the interleave bound, and the paths go out of date.
- **Joining into the wrong path.** After the first join, the lower paths are part of the top path. All later cuts and joins of the same access act on that combined path, which is why lines L8 to L10 go from the top down.
- **Cut and join cost.** The $O(\log \log n)$ bound needs auxiliary trees with depth fields and split and concatenate in $O(\log \log n)$. A simple list, as in the Python code, makes them $O(\log n)$.

## Implementations

The Python class builds the reference tree on $1, \ldots, n$ and keeps the paths as sorted lists. `access` follows the main block and returns the number of paths visited and the number of L-R switches. The tests check that the paths are always the chains of preferred children, and that the total number of switches equals the interleave bound computed directly from the sequence, on random sequences and on the bit-reversal sequence.

## History

Demaine, Harmon, Iacono and Pătraşcu presented tango trees at FOCS 2004, with the journal version in 2007. Their analysis rests on the first lower bound of Wilber (1989), the interleave bound, which they restated in terms of preferred paths. Since then several $O(\log \log n)$-competitive BSTs have been found, but no $O(1)$-competitive one.

## References
