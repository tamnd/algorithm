---
tag: 2KJSKH
kind: technique
slug: union-by-rank
name: Union by rank
aliases:
- linking by rank
area: data-structures/disjoint-sets
level: core
summary: On union, attach the root of smaller rank under the root of larger rank, keeping trees shallow.
prereqs: [disjoint-set-forest, rooted-tree, logarithms]
see_also: [union-by-size, path-compression, union-find-amortized-bound, randomized-linking, quick-union, union-find-with-rollback]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 19.3 (the union by rank heuristic and the procedure LINK), Section 19.4 (the properties of ranks)
  - paper: doi:10.1145/62.2160
    title: "Robert E. Tarjan and Jan van Leeuwen, Worst-case analysis of set union algorithms, Journal of the ACM 31(2) (1984), 245-281"
    locator: the linking rules (linking by rank and linking by size) and the bound for linking without compaction
  - book: isbn:9780898711875
    title: Robert Endre Tarjan, Data Structures and Network Algorithms, SIAM, 1983
    locator: Chapter 2, Disjoint sets (union by rank)
---

Union by rank is the linking rule of a [disjoint-set forest](/disjoint-set-forest/) that makes the root of smaller rank a child of the root of larger rank, and raises the rank of the new root by one when the two ranks are equal. The rank of a node is an upper bound on its height. The rule keeps each tree of $s$ nodes at height at most $\lfloor \lg s \rfloor$, so each find costs $O(\log n)$ in the worst case, and with [path compression](/path-compression/) the amortized cost falls to $O(\alpha(n))$, the [inverse Ackermann function](/inverse-ackermann-function/).

## In plain words

When two trees join, one root must go under the other. If the tall tree goes under the short one, every node of the tall tree gets one step further from the top, and the tree grows taller. If the short tree goes under the tall one, the height does not change at all.

So each root keeps a number, its rank, which tells how tall its tree is, or was before some shortcuts. The root with the smaller number goes under the root with the larger number. Only when the two numbers are equal does the joined tree get taller, and then the new root's number goes up by one.

A tree can only reach a given height by joining two trees that each reached the height below. So a tall tree must have very many nodes, and the height stays small.

## When it applies

- **A forest of parent pointers that only merges.** The data structure stores sets as rooted trees, and the only change of shape, apart from shortcuts on paths, is to make one root a child of another.
- **The choice of the new root is free.** The caller does not care which root represents the merged set, or stores the name it needs at the root, so the structure may choose.
- **Finds walk to the root.** The cost of an operation is the length of a path to a root, so the height of the trees is the cost to control.
- **A worst-case bound per operation is needed.** Union by rank gives $O(\log n)$ per find without any amortization. This matters when amortized bounds fail, as in [union-find with rollback](/union-find-with-rollback/), or in real-time code.

## The template

```pseudo id=main
MAKE-SET(x)
L1  x.p ← x; x.rank ← 0

LINK(x, y)                                ▷ x and y are two different roots
L2  if x.rank > y.rank then
L3      y.p ← x
L4  else
L5      x.p ← y
L6      if x.rank = y.rank then y.rank ← y.rank + 1

UNION(x, y)
L7  rx ← ⟨FIND⟩(x); ry ← ⟨FIND⟩(y)
L8  if rx ≠ ry then LINK(rx, ry)
```

The hole ⟨FIND⟩ is the walk to the root. It can be a plain walk, [path compression](/path-compression/), [path halving](/path-halving/) or [path splitting](/path-splitting/). A rank changes only at line L6, and only at a root. The ranks of non-roots never change again, even when path compression later makes the trees shorter.

**The rank lemma.** Without any change of shape other than LINK, the rank of each node is its height. With any of the path compaction rules, these facts hold:

1. If $x$ is not a root, $x.rank < x.p.rank$.
2. A root of rank $r$ has at least $2^r$ nodes in its tree.
3. For each $r \ge 0$, at most $n/2^r$ nodes have rank $r$, where $n$ is the number of elements.
4. Each rank is at most $\lfloor \lg n \rfloor$, and each tree has height at most $\lfloor \lg n \rfloor$.

*Proof.* Facts 1 and 2 hold for a new node of rank 0. LINK makes a root of smaller or equal rank a child of the other root. If the ranks differ, fact 1 holds for the new edge, and the root keeps its rank while its tree grows. If both ranks are $r$, the new root has rank $r + 1$ and at least $2^r + 2^r = 2^{r+1}$ nodes. A compaction rule only moves a node to a later node of its own path, whose rank is larger by fact 1, and it keeps the set of nodes of each tree. So facts 1 and 2 hold after each operation. For fact 3, when a node $x$ gets rank $r$, it is a root whose tree has at least $2^r$ nodes, by fact 2; label each of these nodes with $x$. Suppose a node $z$ gets the labels of two nodes $x \ne x'$ of rank $r$, with $x$ first. A rank only grows, so $x$ keeps rank $r$ from then on, and $x$ stays in one set with $z$. When line L6 raises $x'$ from rank $r - 1$ to $r$, $z$ is in one of the two trees that LINK joins, and so is $x$. The root of that tree has rank $r - 1$, and $x \ne x'$ has rank $r$, so $x$ is a non-root below a root of smaller rank, against fact 1. So each node has at most one label of rank $r$, and at most $n/2^r$ nodes ever have rank $r$. Fact 4: a node of rank $r$ needs $2^r \le n$ nodes, and the ranks increase strictly along a path, so a path has at most $\lfloor \lg n \rfloor$ edges. $\square$

The same argument with the number of nodes in place of $2^r$ is the proof for [union by size](/union-by-size/).

## Classic examples

### Height on a worst case

Take $16$ elements and join them as a tournament: $(0, 1)$, $(2, 3)$, ..., $(14, 15)$, then the 4 pairs of pairs, then the 2 pairs of quadruples, then the last two trees. Each union joins two trees of equal rank, so the final root has rank $4 = \lg 16$, and the tree is a binomial tree of height 4. This is the tallest tree that union by rank can build from 16 elements. Without a rule, the 15 unions $(0, 1)$, $(1, 2)$, ..., $(14, 15)$ with the first root put under the second make a chain of height 15.

In general, the tournament on $2^k$ elements builds a tree of height $k$ with a leaf at depth $k$. Then $m$ finds of that leaf, without path compression, cost $k = \lg n$ steps each. So union by rank alone costs $\Theta(m \log n)$ in the worst case for $m \ge n$ operations, and fact 4 is tight.

### Rank and size disagree

Let tree $A$ be a star with 5 nodes: a root of rank 1 with four children. Let tree $B$ have 4 nodes built from two pairs, so its root has rank 2 and height 2. Union by rank puts $A$ under $B$: the result has 9 nodes and height $\max(2, 1 + 1) = 2$. [Union by size](/union-by-size/) puts $B$ under $A$, because $B$ has fewer nodes: the height is $\max(1, 2 + 1) = 3$. Both rules keep the height at most $\lfloor \lg 9 \rfloor = 3$. Neither is better on every input, and both give the same bounds.

### Where it is used

- [Disjoint-set forest](/disjoint-set-forest/) with [path compression](/path-compression/): $O(m\,\alpha(m, n))$ for $m$ operations on $n$ elements, [Tarjan's union-find bound](/union-find-amortized-bound/).
- [Kruskal's algorithm](/kruskal/) for the [minimum spanning tree](/minimum-spanning-tree/): one find per edge and one union per tree edge.
- [Union-find with rollback](/union-find-with-rollback/) and the offline [dynamic connectivity](/offline-dynamic-connectivity/) built on it: union by rank without compression keeps each find at $O(\log n)$ in the worst case, which survives an undo.
- [Tarjan's offline LCA algorithm](/tarjan-offline-lca/), which merges each finished subtree into its parent.

## Variations

- **[Union by size](/union-by-size/).** Compare the numbers of nodes instead of the ranks. The bounds are the same, and the size field is often useful by itself.
- **Union by height.** Without path compression, the rank is the exact height, so union by rank is union by height. With path compression the true height is costly to keep, which is why the rank is only an upper bound.
- **Rank in a few bits.** A rank is at most $\lfloor \lg n \rfloor$, so it needs only $\lceil \lg(\lfloor \lg n \rfloor + 1) \rceil$ bits; 6 bits suffice for $n < 2^{64}$. Some codes store the rank of a root in its parent field as a negative number, because a root needs no parent.
- **[Randomized linking](/randomized-linking/).** Give each node a random priority once, and link by priority. It needs no rank updates, and its expected cost matches union by rank.
- **Linking by index.** Always put the root with the smaller index under the other. This is not a balancing rule: the unions $(0, 1)$, $(1, 2)$, ... make a chain. It is fine only when the indices are a random permutation, which is randomized linking.

## Pitfalls

- **Raising the rank of the child.** Line L6 raises the rank of the new root $y$. Raising $x.rank$ instead breaks fact 1 and the height bound.
- **Raising the rank on each union.** The rank grows only when the two ranks are equal. Code that adds one on each link makes the rank of a root count its unions, and the comparison then means little.
- **Updating ranks during path compression.** Path compression lowers heights but must not change ranks. The analysis of the combined rules needs ranks that never fall.
- **Comparing ranks of non-roots.** LINK must get two roots. Linking $x$ and $y$ themselves, before line L7 finds their roots, cuts a subtree out of its set.
- **Rank as the height.** After path compression, the rank of a root can exceed the height of its tree. Code that reports the rank as the depth of the tree is wrong.

## Exercises

1. Show that, without path compression, the rank of each node equals its height, and that the tree of a root of rank $r$ is a binomial tree when it has exactly $2^r$ nodes.
2. Give a sequence of unions on $n = 2^k$ elements, and a sequence of $m$ finds, such that union by rank without compression does $\Theta(m \log n)$ steps.
3. Prove that union by rank keeps the sum of all ranks below $n$. (Hint: fact 3.)
4. Show that with union by rank the number of roots of rank at least $r$ is at most $n/2^r$ at any time.
5. Find two trees for which union by rank and union by size give trees of different heights after one union, other than the example above.

## References
