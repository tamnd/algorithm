---
tag: DQPSA5
kind: technique
slug: union-by-size
name: Union by size
aliases:
- weighted union
- weighted quick-union
area: data-structures/disjoint-sets
level: core
summary: On union, attach the root of the smaller set under the root of the larger set.
prereqs: [disjoint-set-forest, quick-union, logarithms]
see_also: [union-by-rank, path-compression, linked-list-disjoint-sets, union-find-amortized-bound, weighted-union-find, randomized-linking]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.5, Case study, union-find (weighted quick-union, its trace on tinyUF.txt and the bound lg N on the depth of a node)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 19.2 (the weighted-union heuristic for linked lists, and the bound O(m + n lg n)) and Section 19.3 (union by rank)
  - paper: doi:10.1145/62.2160
    title: "Robert E. Tarjan and Jan van Leeuwen, Worst-case analysis of set union algorithms, Journal of the ACM 31(2) (1984), 245-281"
    locator: linking by size and linking by rank, and the proof that each compaction rule has the same bounds with either
---

Union by size is the linking rule of a [disjoint-set forest](/disjoint-set-forest/) that makes the root of the tree with fewer nodes a child of the root of the tree with more nodes. Each root stores the size of its set, and the new root adds the size of the other. It keeps each node at depth at most $\lfloor \lg n \rfloor$, so a find costs $O(\log n)$ in the worst case, and with [path compression](/path-compression/) it has the same $O(m\,\alpha(m, n))$ bound as [union by rank](/union-by-rank/). Sedgewick and Wayne call the forest with this rule *weighted quick-union*.

## In plain words

When two groups merge, one leader must step down and join the other group. Union by size says: the leader of the smaller group steps down.

Each member of the smaller group is now one step further from the top. But that member is now in a group at least twice as big as before. A group cannot double in size more often than the number of times you can halve the total number of people. So no member is ever more than that many steps from the top.

The rule needs one number per leader: the size of the group. That number is often useful by itself, for example to report the largest group.

## When it applies

- **A merge-only forest.** As for [union by rank](/union-by-rank/): the sets are trees of parent pointers, and the new root of a union may be either old root.
- **The sizes are wanted anyway.** The program reports the size of a set, the largest set, or a count that depends on sizes, as in [percolation](/percolation/) or clustering. Union by size then costs nothing extra.
- **The same idea outside trees.** "Move the smaller one into the larger one" works for any merge in which the cost is the size of the moved part. It is the weighted union of [linked-list disjoint sets](/linked-list-disjoint-sets/), and the small-to-large merging of [DSU on tree](/dsu-on-tree/).

## The template

```pseudo id=main
MAKE-SET(x)
L1  x.p ← x; x.size ← 1

LINK(x, y)                                ▷ x and y are two different roots
L2  if x.size < y.size then swap x and y  ▷ now x has the larger set
L3  y.p ← x
L4  x.size ← x.size + y.size

UNION(x, y)
L5  rx ← ⟨FIND⟩(x); ry ← ⟨FIND⟩(y)
L6  if rx ≠ ry then LINK(rx, ry)
```

The hole ⟨FIND⟩ is any walk to the root: a plain walk, [path compression](/path-compression/), [path halving](/path-halving/) or [path splitting](/path-splitting/). The field $x.size$ is correct only at a root. When a root becomes a child, its old size is no longer used.

**The depth lemma.** With LINK as above and any compaction rule, each node has depth at most $\lfloor \lg n \rfloor$, where $n$ is the number of elements.

*Proof.* Fix a node $v$. A compaction rule moves a node to a later node of its own path, so it never makes the depth of $v$ larger. Line L3 changes the depth of $v$ only when the root of its tree becomes a child, and then it adds exactly 1. In that case the tree of $v$ is the tree of $y$, the smaller one, so the set of $v$ grows from $y.size$ to $x.size + y.size \ge 2\,y.size$: it at least doubles. The set of $v$ starts with 1 element and never has more than $n$, so it doubles at most $\lfloor \lg n \rfloor$ times, and the depth of $v$, which is at most the number of these steps, is at most $\lfloor \lg n \rfloor$. $\square$

The proof shows more: a node at depth $d$ in a forest without compaction is in a set of at least $2^d$ elements. For [union by rank](/union-by-rank/) the same counting runs on the rank instead.

## Classic examples

### The trace of Sedgewick and Wayne

Run weighted quick-union on 10 elements and the 11 pairs of the file tinyUF.txt: $(4,3)$, $(3,8)$, $(6,5)$, $(9,4)$, $(2,1)$, $(8,9)$, $(5,0)$, $(7,2)$, $(6,1)$, $(1,0)$, $(6,7)$. Here a tie puts the root of the second element under the root of the first, as in their code.

| pair | roots | what happens | parents of 0 to 9 |
|---|---|---|---|
| start | | | 0 1 2 3 4 5 6 7 8 9 |
| 4 3 | 4, 3 | tie, 3 under 4, size of 4 is 2 | 0 1 2 4 4 5 6 7 8 9 |
| 3 8 | 4, 8 | 8 under 4, size 3 | 0 1 2 4 4 5 6 7 4 9 |
| 6 5 | 6, 5 | tie, 5 under 6 | 0 1 2 4 4 6 6 7 4 9 |
| 9 4 | 9, 4 | 9 under 4, size 4 | 0 1 2 4 4 6 6 7 4 4 |
| 2 1 | 2, 1 | tie, 1 under 2 | 0 2 2 4 4 6 6 7 4 4 |
| 8 9 | 4, 4 | same set | 0 2 2 4 4 6 6 7 4 4 |
| 5 0 | 6, 0 | 0 under 6, size 3 | 6 2 2 4 4 6 6 7 4 4 |
| 7 2 | 7, 2 | 7 under 2, size 3 | 6 2 2 4 4 6 6 2 4 4 |
| 6 1 | 6, 2 | tie of 3 and 3, 2 under 6, size 6 | 6 2 6 4 4 6 6 2 4 4 |
| 1 0 | 6, 6 | same set | 6 2 6 4 4 6 6 2 4 4 |
| 6 7 | 6, 6 | same set | 6 2 6 4 4 6 6 2 4 4 |

There are two sets: $\{0, 1, 2, 5, 6, 7\}$ with root 6 and $\{3, 4, 8, 9\}$ with root 4. The deepest nodes, 1 and 7, have depth 2, below $\lfloor \lg 10 \rfloor = 3$.

### Where it is used

- [Percolation](/percolation/): the size of each cluster is needed, and the forest with union by size is the standard code.
- [Kruskal's algorithm](/kruskal/): the size lets the code stop when one tree has all $n$ vertices.
- [Linked-list disjoint sets](/linked-list-disjoint-sets/): appending the shorter list to the longer one gives $O(m + n \log n)$ for $m$ operations, by the same doubling argument.
- [Union-find with rollback](/union-find-with-rollback/): without compression the depth bound holds in the worst case, so each find costs $O(\log n)$ after any undo.

## Variations

- **[Union by rank](/union-by-rank/).** Compare ranks instead of sizes. A rank needs only $O(\log \log n)$ bits, a size needs $O(\log n)$ bits. Tarjan and van Leeuwen proved the same bounds for both rules with each compaction rule.
- **Size stored in the parent field.** A root needs no parent, so a common trick stores $-\text{size}$ in the parent array at each root. A negative entry marks a root. This saves the second array.
- **Size of other measures.** The rule works with any weight that adds under union and is at least 1 for each element, for example the number of edges plus vertices. The depth bound becomes $\lg W$ for the total weight $W$.
- **Small to large for other structures.** Merge two hash sets, heaps or maps by inserting each element of the smaller into the larger. Each element moves $O(\log n)$ times, which is [DSU on tree](/dsu-on-tree/) and its relatives.

## Pitfalls

- **Swapping without the sizes.** Line L2 must swap the roots, not only compare. Code that compares the sizes and then always does $y.p \leftarrow x$ is plain [quick-union](/quick-union/).
- **Adding the size to the wrong root.** Line L4 adds to the new root $x$. Adding to $y$ leaves the size of the root too small, and later links go the wrong way.
- **Reading the size of a non-root.** `size(v)` is the size field of FIND$(v)$, not of $v$. A non-root keeps a stale size from the time it was a root.
- **Counting a union of one set.** Line L6 tests $rx \ne ry$. Without the test, the size of the root doubles while the set stays the same.

## Exercises

1. Prove that weighted quick-union without compression builds a tree of height exactly $k$ from $2^k$ elements for some sequence of unions, so the depth lemma is tight.
2. Show that in a forest built by union by size without compression, a root of a tree of height $h$ has at least $2^h$ nodes in its tree.
3. Store $-\text{size}$ at each root in the parent array, and write MAKE-SET, FIND and LINK with one array only.
4. A union by size of linked lists moves the elements of the smaller list. Prove that each element moves at most $\lfloor \lg n \rfloor$ times.

## References
