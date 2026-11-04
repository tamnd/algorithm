---
tag: B24A25
kind: data-structure
slug: disjoint-set-forest
name: Disjoint-set forest
aliases:
- union-find forest
- rooted-tree disjoint sets
area: data-structures/disjoint-sets
level: core
summary: Representation of disjoint sets as rooted trees, with a parent pointer per element and a root as representative.
implements: [disjoint-set]
model: word-ram
prereqs: [disjoint-set, rooted-tree, amortized-cost]
see_also: [union-by-rank, path-compression, union-find-amortized-bound, quick-union, path-halving, union-by-size, inverse-ackermann-function, kruskal]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 19, Section 19.3 (Disjoint-set forests, the procedures MAKE-SET, UNION, LINK and FIND-SET) and Section 19.4 (Analysis of union by rank with path compression, the properties of ranks)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.5, Case study, union-find (quick-union, weighted quick-union and path compression)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.3, Algorithm E (equivalence relations by parent pointers)
  - paper: doi:10.1145/62.2160
    title: "Robert E. Tarjan and Jan van Leeuwen, Worst-case analysis of set union algorithms, Journal of the ACM 31(2) (1984), 245-281"
    locator: the linking rules (by rank, by size) and the compaction rules (compression, splitting, halving), with their bounds
  - paper: "Bernard A. Galler and Michael J. Fischer, An improved equivalence algorithm, Communications of the ACM 7(5) (1964), 301-303"
    locator: the tree representation of equivalence classes
---

A disjoint-set forest stores each set of a [disjoint-set](/disjoint-set/) structure as a [rooted tree](/rooted-tree/): each element has a pointer to its parent, and the root of each tree is the representative of its set. `find` follows the parent pointers to the root, and `union` makes one root a child of the other. With the two rules [union by rank](/union-by-rank/) and [path compression](/path-compression/), a sequence of $m$ operations on $n$ elements takes $O(m\,\alpha(n))$ time, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/), and each single operation takes $O(\log n)$ time. It is the union-find of [Kruskal's algorithm](/kruskal/), of [connected component labeling](/connected-component-labeling/), and of most code that merges classes.

## In plain words

Each element holds the name of one other element, its parent. If you follow parents from any element, you always end at an element that names itself. That element is the leader of the group. Two elements are in the same group when they reach the same leader.

To join two groups, find both leaders and make one leader point at the other. The walk to the leader gets long when the trees get tall, so two rules keep it short. First, the shorter tree goes under the taller tree, so the height grows only when two trees of equal height join. Second, after each walk, every element that you passed now points straight at the leader. The next walk from any of them takes one step.

## The abstract type

The forest implements the [disjoint-set](/disjoint-set/) type: `make-set(x)` adds $x$ as a set of its own, `find(x)` returns the representative of the set of $x$, and `union(x, y)` merges the sets of $x$ and $y$. `connected(x, y)` is a comparison of two finds. The code of this page keeps a counter of the sets, which gives `count` in $O(1)$ time.

## Representation

Each element $x$ has two fields: a parent $x.p$, which is an element, and a rank $x.rank$, which is a non-negative integer. With elements $0$ to $n - 1$, the fields are two integer arrays of length $n$. The parent pointers form a graph with one edge from each $x$ to $x.p$. An element with $x.p = x$ is a *root*.

**Invariant (F).** Following parent pointers from any element reaches a root after finitely many steps, so the graph is a forest of rooted trees with a self-loop at each root. The sets of the structure are the node sets of the trees, and the representative of a set is its root.

**Invariant (R).** For each element $x$ that is not a root, $x.rank < x.p.rank$. A root of rank $r$ has at least $2^r$ nodes in its tree.

(R) gives the height bound. Along a path from $x$ to its root the ranks increase strictly, so a path from $x$ to its root has at most $r - x.rank$ edges, where $r$ is the rank of the root. A root of rank $r$ has at least $2^r$ of the $n$ nodes, so $r \le \lfloor \lg n \rfloor$, and each tree has height at most $\lfloor \lg n \rfloor$.

Rank is an upper bound on the height of a node, not the height itself. Before any path compression, the rank of each node equals its height. Path compression lowers heights but never changes a rank.

## Operations

```pseudo id=main
MAKE-SET(x)
L1  x.p ← x
L2  x.rank ← 0

FIND(x)                                   ▷ returns the root, and compresses the path
L3  if x.p ≠ x then
L4      x.p ← FIND(x.p)
L5  return x.p

UNION(x, y)
L6  x ← FIND(x); y ← FIND(y)
L7  if x = y then return                  ▷ already in one set
L8  if x.rank > y.rank then y.p ← x
L9  else x.p ← y
L10     if x.rank = y.rank then y.rank ← y.rank + 1
```

**Make-set** (lines L1 and L2) makes a tree of one node, with rank 0. It costs $O(1)$.

**Find** (lines L3 to L5) climbs from $x$ to the root, and on the way back down it sets the parent of each node of the path to the root. This is [path compression](/path-compression/). The recursion depth is the length of the path, which is at most $\lfloor \lg n \rfloor$ by (R). The Python code does the same in two loops: one climbs to the root, and the second walks the path again and resets each parent. [Path halving](/path-halving/) and [path splitting](/path-splitting/) do the work in one pass with the same bounds.

**Union** (lines L6 to L10) finds both roots. If they are equal, the elements are in one set and nothing changes. Otherwise the root of smaller rank becomes a child of the root of larger rank, which is [union by rank](/union-by-rank/). When the ranks are equal, $x$ goes under $y$, and the rank of $y$ grows by one. CLRS calls lines L8 to L10 the procedure LINK.

## Example

Make the sets $0$ to $7$. Then do seven unions and one find. The parent array lists $0.p$ to $7.p$, and the rank array lists the ranks in the same order.

| step | what happens | parents | ranks |
|---|---|---|---|
| start | eight roots | 0 1 2 3 4 5 6 7 | 0 0 0 0 0 0 0 0 |
| union(0, 1) | equal ranks, 0 goes under 1 | 1 1 2 3 4 5 6 7 | 0 1 0 0 0 0 0 0 |
| union(2, 3) | 2 goes under 3 | 1 1 3 3 4 5 6 7 | 0 1 0 1 0 0 0 0 |
| union(0, 2) | roots 1 and 3, rank 1 each, 1 goes under 3 | 1 3 3 3 4 5 6 7 | 0 1 0 2 0 0 0 0 |
| union(4, 5) | 4 goes under 5 | 1 3 3 3 5 5 6 7 | 0 1 0 2 0 1 0 0 |
| union(6, 7) | 6 goes under 7 | 1 3 3 3 5 5 7 7 | 0 1 0 2 0 1 0 1 |
| union(4, 6) | roots 5 and 7, 5 goes under 7 | 1 3 3 3 5 7 7 7 | 0 1 0 2 0 1 0 2 |
| union(0, 4) | find(0) sets 0.p to 3, find(4) sets 4.p to 7; roots 3 and 7 have rank 2, 3 goes under 7 | 3 3 3 7 7 7 7 7 | 0 1 0 2 0 1 0 3 |
| find(0) | path 0, 3, 7; 0.p becomes 7 | 7 3 3 7 7 7 7 7 | 0 1 0 2 0 1 0 3 |

At the end there is one tree with root 7 and rank $3 = \lg 8$. Its height is 2, less than its rank, because the finds compressed two paths. A further `union(2, 6)` finds the root 7 twice and does nothing.

## Correctness

Each operation keeps (F) and (R), and the sets that the trees represent change exactly as the [disjoint-set](/disjoint-set/) type says. MAKE-SET adds a new root. FIND changes parents only to the root of the same tree, so the trees keep their node sets, and the new parent of a node has a rank at least that of the old parent, so (R) stays true. UNION adds one edge from a root to the root of another tree, which joins the two trees and keeps (F). The rank rule keeps (R): a rank grows only when two trees of rank $r$, each with at least $2^r$ nodes, join into one tree with at least $2^{r+1}$ nodes. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $n$ be the number of elements and $m$ the number of operations.

- **Height.** By (R), each tree has height at most $\lfloor \lg n \rfloor$. So FIND and UNION take $O(\log n)$ time in the worst case, even without path compression.
- **Rank counts.** At most $n/2^r$ nodes ever have rank $r$: each such node was a root of rank $r$ with at least $2^r$ nodes below it at that time, and two such nodes have disjoint sets of descendants then. So the sum of all ranks is less than $n$.
- **Amortized cost.** With both rules, $m$ operations of which $n$ are MAKE-SET take $O(m\,\alpha(n))$ time. Tarjan (1975) proved the sharper bound $O(m\,\alpha(m, n))$. The proof is on the page [Tarjan's union-find bound](/union-find-amortized-bound/). The bound is tight for this structure, and the [union-find lower bound](/union-find-lower-bound/) shows that it is tight for every structure.
- **Space.** Two fields per element: $n$ parents and $n$ ranks. Ranks are at most $\lfloor \lg n \rfloor$, so a rank fits in one byte for each $n < 2^{256}$.

| operation | worst case | amortized (both rules) |
|---|---|---|
| make-set | $O(1)$ | $O(1)$ |
| find | $O(\log n)$ | $O(\alpha(n))$ |
| union | $O(\log n)$ | $O(\alpha(n))$ |
| connected | $O(\log n)$ | $O(\alpha(n))$ |
| space | $2n$ words | |

Each rule alone gives a weaker bound. Union by rank alone gives $\Theta(m \log n)$ in the worst case, and path compression alone gives $\Theta(m \log_{1 + m/n} n)$ for $n - 1$ unions and $m \ge n$ finds (Tarjan and van Leeuwen, 1984). Without either rule, a chain of $n$ nodes makes each find cost $\Theta(n)$, which is the worst case of [quick-union](/quick-union/).

## Variants

- **[Union by size](/union-by-size/).** Keep the number of nodes of each tree instead of the rank, and put the smaller tree under the larger. The bounds are the same. The size is often useful to the caller too.
- **[Path halving](/path-halving/) and [path splitting](/path-splitting/).** Point each node of the path at its grandparent, in one pass and without recursion. Tarjan and van Leeuwen proved that each gives the same $O(m\,\alpha(m, n))$ bound with union by rank or size.
- **[Randomized linking](/randomized-linking/).** Give each element a random priority once, and put the root of lower priority under the other. The expected bounds are those of union by rank.
- **Extra data at the roots.** A root can hold the size of its set, a minimum, a name, or any value that merges in $O(1)$ time.
- **Data on the edges.** [Weighted union-find](/weighted-union-find/) stores a group element on each edge to the parent, for relative values, and [union-find with parity](/dsu-with-parity/) is the case of the group of order 2.
- **Undo.** Without path compression, a union changes $O(1)$ fields, which a stack can restore. This is [union-find with rollback](/union-find-with-rollback/).

## When to use it

Use the forest as the default union-find. It has the best known amortized bound, which no structure can beat, and it fits in two arrays. Use [quick-find](/quick-find/) only when the number of elements is small and finds dominate. Use [linked lists](/linked-list-disjoint-sets/) when the program must list the members of a set often. Use [Blum's structure](/blum-union-find/) only when each single operation needs a worst-case bound below $O(\log n)$. When all unions are known in advance, the [Gabow-Tarjan](/gabow-tarjan-union-find/) algorithm is linear, but it is more complex and rarely faster in practice.

## Pitfalls

- **Union of elements, not roots.** Line L6 replaces $x$ and $y$ by their roots. Code that sets $x.p \leftarrow y$ on the elements cuts $x$ from its tree and loses the rest of its old set.
- **No test for one set.** Without line L7, a union of two elements of one set makes the root its own child twice and may raise its rank for no reason. With union by size, it doubles the size field.
- **The rank on the wrong root.** Line L10 raises the rank of the new root $y$. Raising the rank of $x$, which is now a child, breaks (R).
- **Recursion depth.** Without union by rank, a tree can be a chain of $n$ nodes, and the recursive FIND of line L4 then overflows the stack. Use the loop form of the Python code, or path halving.
- **Comparing elements instead of roots.** `connected(x, y)` is `find(x) = find(y)`, not `x.p = y.p`. Two nodes of one tree can have different parents.

## Implementations

The Python class keys its two maps by any hashable element. Its `find` uses two loops instead of recursion, and `check_invariant` tests (F) and (R).

## History

Galler and Fischer (1964) introduced the representation of equivalence classes by trees of parent pointers. Knuth gives it as Algorithm E in Section 2.3.3. Linking by size or rank and path compression were in use by the early 1970s. Path compression is usually credited to McIlroy and Morris, and Tarjan and van Leeuwen survey the early history of the rules. Hopcroft and Ullman (1973) proved the bound $O(m \lg^* n)$, see the [Hopcroft-Ullman bound](/hopcroft-ullman-log-star-bound/), and Tarjan (1975) proved the tight bound $\Theta(m\,\alpha(m, n))$. Tarjan and van Leeuwen (1984) analyzed the combinations of linking and compaction rules.

## References
