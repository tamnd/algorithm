---
tag: TPV99M
kind: algorithm
slug: quick-union
name: Quick-union
aliases:
- lazy union-find
area: data-structures/disjoint-sets
level: intro
summary: Union-find that links one root to another on union and follows parent pointers on find.
solves: [dynamic-equivalence-problem]
model: word-ram
complexity:
  vars: {n: the number of elements, m: the number of operations, h: the height of the tree of the element}
  time: {init: Θ(n), find: Θ(h), union: Θ(h), worst: O(n), total: O(n + m·n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, online: true, recursive: false}
prereqs: [disjoint-set, rooted-tree]
see_also: [quick-find, disjoint-set-forest, union-by-size, union-by-rank, path-compression, dynamic-equivalence-problem, union-find-with-rollback]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.5, Case study, union-find (the quick-union implementation, its trace on tinyUF.txt, its worst case, and weighted quick-union)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 19.3, Disjoint-set forests (the forest without heuristics, and a sequence of n − 1 unions that makes a linear chain)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.3, Algorithm E (equivalence relations by parent pointers)
---

Quick-union solves the [dynamic equivalence problem](/dynamic-equivalence-problem/) with a forest of parent pointers: each element points to its parent, each root points to itself, and the root of a tree names its set. A find follows the pointers to the root. A union finds the two roots and makes the first a child of the second, which changes one entry. Each operation costs time in proportion to the height of the trees, and with no rule for the linking a tree can become a chain of height $n - 1$. So a sequence of $m$ operations can cost $\Theta(mn)$. It is the [disjoint-set forest](/disjoint-set-forest/) without [union by rank](/union-by-rank/) and without [path compression](/path-compression/), and it is the base that these two rules improve.

## In plain words

Each item knows one other item, its boss. A boss can have a boss too. The item at the top of a chain is its own boss, and it is the leader of the group. To find the leader of an item, you go from boss to boss until you reach the top.

To join two groups, you find both leaders, and the first leader takes the second leader as its boss. That is one change, so a join is cheap once you know the two leaders. The problem is that the chains can grow long, and then each walk to the top is slow.

## The problem

Keep $n$ elements $0$ to $n - 1$, each first in a set of its own. Support `find(p)`, which returns the representative of the set of $p$, `union(p, q)`, which merges the sets of $p$ and $q$, and `connected(p, q)`. This is the [disjoint-set](/disjoint-set/) type on a fixed range of elements, with a counter `count` of the sets.

## The algorithm

```pseudo id=main
INIT(n)
L1  for i ← 0 to n − 1 do parent[i] ← i
L2  count ← n

FIND(p)
L3  while p ≠ parent[p] do
L4      p ← parent[p]
L5  return p

UNION(p, q)
L6  i ← FIND(p); j ← FIND(q)
L7  if i = j then return                  ▷ already in one set
L8  parent[i] ← j                         ▷ link the root of p under the root of q
L9  count ← count − 1
```

**Init** (lines L1 and L2) makes $n$ trees of one node.

**Find** (lines L3 to L5) climbs from $p$ until it reaches a node that is its own parent, the root, and returns it. The loop runs once for each edge of the path, so the cost is the depth of $p$.

**Union** (lines L6 to L9) finds the roots $i$ and $j$. If they are equal, nothing changes. Otherwise line L8 makes $i$ a child of $j$, which hangs the whole tree of $p$ below the root of $q$. Only one entry of the array changes. Which root goes below the other is fixed by the order of the arguments, not by the shape of the trees, and this is the weak point of the method.

## Example

Take $n = 10$ and the eleven pairs of the file tinyUF.txt of Sedgewick and Wayne. Each row shows the array `parent[0..9]` after the union.

| union | roots found | parent after the union | sets |
|---|---|---|---|
| start | | 0 1 2 3 4 5 6 7 8 9 | 10 |
| (4, 3) | 4, 3 | 0 1 2 3 3 5 6 7 8 9 | 9 |
| (3, 8) | 3, 8 | 0 1 2 8 3 5 6 7 8 9 | 8 |
| (6, 5) | 6, 5 | 0 1 2 8 3 5 5 7 8 9 | 7 |
| (9, 4) | 9, 8 | 0 1 2 8 3 5 5 7 8 8 | 6 |
| (2, 1) | 2, 1 | 0 1 1 8 3 5 5 7 8 8 | 5 |
| (8, 9) | 8, 8 | no change | 5 |
| (5, 0) | 5, 0 | 0 1 1 8 3 0 5 7 8 8 | 4 |
| (7, 2) | 7, 1 | 0 1 1 8 3 0 5 1 8 8 | 3 |
| (6, 1) | 0, 1 | 1 1 1 8 3 0 5 1 8 8 | 2 |
| (1, 0) | 1, 1 | no change | 2 |
| (6, 7) | 1, 1 | no change | 2 |

The final sets are the same as with [quick-find](/quick-find/): $\{0, 1, 2, 5, 6, 7\}$ with root 1, and $\{3, 4, 8, 9\}$ with root 8. The depths of the elements $0$ to $9$ are $1, 0, 1, 1, 2, 2, 3, 1, 0, 1$. The find of 6 in the last union walks the path $6, 5, 0, 1$ of three edges.

**The worst case.** The unions $(0, 1), (0, 2), \ldots, (0, n - 1)$ build the chain $0 \to 1 \to 2 \to \cdots \to n - 1$. Before the union $(0, k)$, element 0 has depth $k - 1$, so this union walks $k - 1$ edges, and the whole sequence walks $\sum_{k=1}^{n-1} (k - 1) = (n - 1)(n - 2)/2$ edges, which is $\Theta(n^2)$.

## Correctness

The invariant is: *the parent pointers form a forest whose roots are exactly the elements with `parent[r] = r`, and two elements are in one set exactly when they have the same root*. Init makes $n$ roots. A find only reads, and it reaches the root because the forest has no cycle. A union links two different roots, so it joins two trees into one and makes no cycle: the root $i$ becomes a child of a node in another tree. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [word RAM](/word-ram/). Let the *depth* of $p$ be the number of edges from $p$ to its root.

- **Init.** $\Theta(n)$.
- **Find.** The loop runs once per edge of the path, so FIND$(p)$ costs $\Theta(1 + \mathrm{depth}(p))$. A tree with $s$ nodes has height at most $s - 1$, so the worst case is $\Theta(n)$.
- **Union and connected.** Two finds and $O(1)$ more work, so $O(1 + \mathrm{depth}(p) + \mathrm{depth}(q))$, which is $O(n)$ in the worst case. Line L8 changes one entry.
- **A sequence.** Each of $m$ operations costs $O(n)$, so the total is $O(n + mn)$. The chain of the example reaches $\Theta(n^2)$ with $n - 1$ unions, and then each further find of element 0 costs $\Theta(n)$.
- **Space.** One array of $n$ entries and the counter.

Compared with [quick-find](/quick-find/), a union no longer scans the whole array, but a find is no longer constant. On inputs where the trees stay shallow, quick-union is much faster than quick-find. Its worst case is no better.

## Properties

- **One write per union.** Line L8 is the only change, so an undo stack needs to store one entry per union. This is the base of [union-find with rollback](/union-find-with-rollback/).
- **Order matters.** The shape of the forest, and so the cost, depends on the order of the arguments of each union. The sets do not.
- **Online and deterministic.** Each answer is ready before the next operation.
- **No recursion.** The find is a loop, so a chain of $n$ nodes does not overflow a stack.

## Variants and improvements

- **[Union by size](/union-by-size/).** Keep the size of each tree and link the root of the smaller tree under the root of the larger. Each depth is then at most $\lg n$, so each operation costs $O(\log n)$. Sedgewick and Wayne call this weighted quick-union.
- **[Union by rank](/union-by-rank/).** The same with an upper bound on the height in place of the size.
- **[Path compression](/path-compression/), [path halving](/path-halving/) and [path splitting](/path-splitting/).** Shorten the path during each find. With a linking rule they give the $O(m\,\alpha(m, n))$ bound of [Tarjan's union-find bound](/union-find-amortized-bound/), and alone they give $O(\log n)$ amortized time per operation when there are at least $n$ finds.
- **[Randomized linking](/randomized-linking/).** Choose which root goes below by random priorities instead of by the argument order.
- The result of these changes is the [disjoint-set forest](/disjoint-set-forest/).

## When to use it

Use plain quick-union only as a step to the [disjoint-set forest](/disjoint-set-forest/), or where the input order is known to keep the trees shallow. Adding union by size costs one more array and two lines, and removes the $\Theta(n)$ worst case, so there is rarely a reason to leave it out. Use [quick-find](/quick-find/) when $n$ is small and finds must be $O(1)$ in the worst case.

## Pitfalls

- **Linking elements instead of roots.** Line L8 must set `parent[i] ← j` for the roots. Setting `parent[p] ← q` cuts $p$ out of its tree: the elements below $p$ go with it, but the rest of the old set of $p$ stays behind, so two elements that were in one set are now in different sets.
- **No test for one set.** Without line L7, a union of $p$ and $q$ in one set sets `parent[i] ← i`, which is harmless, but line L9 then counts a merge that did not happen.
- **Comparing parents.** `connected(p, q)` is `FIND(p) = FIND(q)`. A test `parent[p] = parent[q]` fails for two elements at different depths of one tree.
- **A recursive find.** A recursive form of lines L3 to L5 uses one stack frame per edge, and a chain of $10^5$ nodes overflows the default stack of Python. Keep the loop.

## Implementations

The Python class takes $n$ in its constructor. It has `find`, `union`, `connected`, a `count` attribute and a `depth` helper, and `check_invariant` tests that the parent pointers form a forest with `count` roots.

## History

Galler and Fischer (1964) introduced trees of parent pointers for equivalence classes, and Knuth gives the method as Algorithm E of Section 2.3.3. The weighted linking rule and path compression came soon after, as described on the [disjoint-set forest](/disjoint-set-forest/) page. Sedgewick and Wayne use the names quick-union and weighted quick-union.

## References
