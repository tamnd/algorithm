---
tag: N5NH9D
kind: data-structure
slug: weighted-union-find
name: Weighted union-find
aliases:
- union-find with potentials
- union-find with parity
area: data-structures/disjoint-sets
level: advanced
summary: Union-find that stores a group-valued offset on each edge to the parent, answering relative-value queries.
implements: [disjoint-set]
model: word-ram
complexity:
  vars: {n: the number of elements, m: the number of operations}
  time: {worst: O(log n), amortized: O(α(n))}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [disjoint-set-forest, dsu-with-distances-to-representative, union-by-size]
see_also: [dsu-with-distances-to-representative, dsu-with-parity, disjoint-set-forest, path-compression, path-halving, difference-constraints, union-find-with-rollback]
sources:
  - url: https://cp-algorithms.com/data_structures/disjoint_set_union.html
    title: cp-algorithms, Disjoint Set Union
    locator: the sections Support distances up to representative and Support the parity of the path length
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 19.3 (disjoint-set forests with union by rank and path compression) and Section 19.4 (their analysis, which this structure keeps)
---

Weighted union-find is a [disjoint-set forest](/disjoint-set-forest/) in which each edge from a node to its parent carries a value of a group, such as an integer offset. The sum of the values on the path from $x$ to its root is the *potential* of $x$, its value relative to the root. The structure keeps a set of facts of the form $\mathrm{val}(x) - \mathrm{val}(y) = d$: a union adds a fact, tells whether it agrees with the facts so far, and a query returns $\mathrm{val}(x) - \mathrm{val}(y)$ for two elements of one set. With [union by size](/union-by-size/) and [path compression](/path-compression/), it keeps the bounds of the plain forest: $O(\log n)$ per operation in the worst case and $O(\alpha(n))$ amortized. The group of order 2 gives [union-find with parity](/dsu-with-parity/).

## In plain words

You have many unknown numbers. You learn facts like "the first number is 3 more than the second". You want to answer questions like "how much bigger is this number than that one?", or learn that a new fact cannot be true.

Each group of linked numbers has a leader. Every number remembers how much bigger it is than the leader. Two numbers in one group then differ by the difference of these two amounts. A new fact about two groups joins them, and the old leader of one group learns how much bigger it is than the new leader, which fixes all its members at once. A new fact inside one group is checked against what the group already knows.

## The abstract type

The structure implements the [disjoint-set](/disjoint-set/) type, where the sets are the groups of elements whose differences are known, and adds two operations. `union(x, y, d)` adds the fact $\mathrm{val}(x) - \mathrm{val}(y) = d$ and returns false when it contradicts the known facts. `diff(x, y)` returns $\mathrm{val}(x) - \mathrm{val}(y)$ when the facts fix it, that is, when $x$ and $y$ are in one set, and returns nothing otherwise. `find` and `connected` are as in the plain forest.

## Representation

Fix an abelian group $(G, +, 0)$, such as the integers, the rationals, or the bits with exclusive or. Each element $x$ has a parent $x.p$, a value $x.w \in G$ and, at a root, a size $x.size$. A root $r$ has $r.w = 0$.

The *potential* of $x$ is the sum of the values on the path from $x$ to its root $r$:
$$\mathrm{pot}(x) = x.w + x.p.w + \cdots, \text{ up to but not including } r, \qquad \mathrm{pot}(r) = 0.$$

**Invariant (W).** The parent pointers form a forest as in the [disjoint-set forest](/disjoint-set-forest/), with union by size. For each fact $\mathrm{val}(x) - \mathrm{val}(y) = d$ added so far, $x$ and $y$ are in one tree and $\mathrm{pot}(x) - \mathrm{pot}(y) = d$. Conversely, for $x$ and $y$ in one tree, $\mathrm{pot}(x) - \mathrm{pot}(y)$ is implied by the facts.

So the potential is one solution of all the facts, up to a constant per tree, and every solution differs from it by such constants.

## Operations

```pseudo id=main
MAKE-SET(x)
L1  x.p ← x; x.size ← 1
L2  x.w ← 0

FIND(x)                                   ▷ returns the root; afterwards x.w = pot(x)
L3  if x.p = x then return x
L4  r ← FIND(x.p)                         ▷ now x.p.w = pot(x.p)
L5  x.w ← x.w + x.p.w
L6  x.p ← r
L7  return r

DIFF(x, y)
L8  if FIND(x) ≠ FIND(y) then return NONE
L9  return x.w − y.w

UNION(x, y, d)                            ▷ add the fact val(x) − val(y) = d
L10 rx ← FIND(x); ry ← FIND(y)
L11 if rx = ry then return x.w − y.w = d  ▷ check against the known facts
L12 if rx.size > ry.size then swap (x, rx) with (y, ry); d ← −d
L13 rx.p ← ry; rx.w ← d + y.w − x.w
L14 ry.size ← ry.size + rx.size; return true
```

**Find** (lines L3 to L7) is the recursive find with path compression. After the recursive call, the old parent of $x$ points to the root and holds its own potential, so line L5 makes $x.w$ the potential of $x$, and line L6 points $x$ at the root without changing that potential. After FIND$(x)$, $x$ is the root or a child of the root, and $x.w = \mathrm{pot}(x)$ in both cases.

**Diff** (lines L8 and L9) finds both roots. If they differ, the facts do not fix the difference. Otherwise the potentials after the finds give it.

**Union** (lines L10 to L14) finds both roots, so that $x.w = \mathrm{pot}(x)$ and $y.w = \mathrm{pot}(y)$. In one tree, the new fact holds exactly when it agrees with the potentials. Otherwise line L12 swaps the roles so that the smaller tree goes below; the fact $\mathrm{val}(x) - \mathrm{val}(y) = d$ is the fact $\mathrm{val}(y) - \mathrm{val}(x) = -d$. Line L13 links $rx$ under $ry$ with the value that makes $\mathrm{pot}(x) - \mathrm{pot}(y) = d$: after the link, every node of the tree of $rx$ has its potential increased by $rx.w$, so $\mathrm{pot}(x)$ becomes $x.w + d + y.w - x.w = d + \mathrm{pot}(y)$.

Each operation costs the same as in the plain forest, plus $O(1)$ group operations per step.

## Example

Take the elements $0$ to $5$ with integer values. The arrays show the parents and the values $w$ of $0$ to $5$ after each operation.

| operation | what happens | parents | $w$ | result |
|---|---|---|---|---|
| union(0, 1, 3) | roots 0 and 1, sizes 1 and 1; 0.p ← 1, 0.w ← 3 | 1 1 2 3 4 5 | 3 0 0 0 0 0 | true |
| union(2, 3, −2) | 2.p ← 3, 2.w ← −2 | 1 1 3 3 4 5 | 3 0 −2 0 0 0 | true |
| union(1, 2, 4) | roots 1 and 3, sizes 2 and 2; 1.w ← 4 + (−2) − 0 | 1 3 3 3 4 5 | 3 2 −2 0 0 0 | true |
| union(0, 3, 5) | one root 3; find(0) sets 0.p ← 3, 0.w ← 3 + 2; check 5 − 0 = 5 | 3 3 3 3 4 5 | 5 2 −2 0 0 0 | true |
| union(0, 3, 6) | one root; 5 − 0 ≠ 6 | 3 3 3 3 4 5 | 5 2 −2 0 0 0 | false |
| union(4, 5, 1) | 4.p ← 5, 4.w ← 1 | 3 3 3 3 5 5 | 5 2 −2 0 1 0 | true |
| diff(0, 3) | | | | 5 |
| diff(1, 2) | | | | 4 |
| diff(0, 4) | different roots | | | none |

One solution of the facts is $\mathrm{val} = (5, 2, -2, 0)$ on the set $\{0, 1, 2, 3\}$ and $(1, 0)$ on the set $\{4, 5\}$. Any constant can be added to all values of one set.

## Correctness

Each operation keeps (W). MAKE-SET adds a root with potential 0 and no facts. FIND changes the parent of $x$ only to its root and sets $x.w$ to its full potential, so no potential changes. A union inside one tree adds the fact only when the potentials already satisfy it, and then the fact is implied by the earlier ones. A union of two trees adds the same value $rx.w$ to every potential in the tree of $rx$, which keeps the differences inside that tree, and the value of line L13 makes the new fact true. Conversely, each difference in the new tree is a sum of a difference in the old tree of $x$, the new fact, and a difference in the old tree of $y$, so it is implied by the facts. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The value fields do not change the shape of the forest: the parents change exactly as in a [disjoint-set forest](/disjoint-set-forest/) with union by size and path compression. Each step of a find or a union does $O(1)$ more group operations. So, when a group operation costs $O(1)$:

| operation | worst case | amortized |
|---|---|---|
| make-set | $O(1)$ | $O(1)$ |
| find, diff | $O(\log n)$ | $O(\alpha(n))$ |
| union | $O(\log n)$ | $O(\alpha(n))$ |
| space | $\Theta(n)$ elements of $G$ and $3n$ words | |

The amortized bound is [Tarjan's union-find bound](/union-find-amortized-bound/) with union by size in place of rank. With rationals or big integers, a group operation costs more, and the values on compressed edges can grow in size.

## Variants

- **Non-commutative groups.** For a group that is not abelian, such as permutations or rotations, write the value of the edge from $x$ to $x.p$ as $g_x$ with $\mathrm{val}(x) = g_x \cdot \mathrm{val}(x.p)$. The potential is the product along the path, from $x$ up, and line L13 becomes $g_{rx} = \mathrm{pot}(x)^{-1} \cdot d \cdot \mathrm{pot}(y)$ for the fact $\mathrm{val}(x) = d \cdot \mathrm{val}(y)$. The order of the factors matters.
- **[Union-find with parity](/dsu-with-parity/).** The group of bits with exclusive or. It tests whether a graph is bipartite while edges arrive.
- **[Union-find with distances](/dsu-with-distances-to-representative/).** The technique behind this structure, with a fixed direction of linking for problems such as stacks of cubes.
- **Multiplicative values.** With the positive rationals under multiplication, the facts are ratios, such as exchange rates or unit conversions.
- **Iterative find.** [Path halving](/path-halving/) with $x.w \leftarrow x.w + x.p.w$ before each skip gives a one-pass find with the same bounds.
- **Undo.** Without compression, a union changes $O(1)$ fields, and the structure supports [rollback](/union-find-with-rollback/).

## When to use it

Use weighted union-find when facts about differences, ratios or parities arrive online and each must be checked at once, or when differences of pairs must be answered between the facts. For a fixed list of equalities, a graph search that assigns potentials also takes linear time. For inequalities $\mathrm{val}(x) - \mathrm{val}(y) \le d$, union-find does not apply; that is a system of [difference constraints](/difference-constraints/), solved by shortest paths.

## Pitfalls

- **Linking with the values of the elements.** Line L13 needs $x.w$ and $y.w$ to be the potentials of $x$ and $y$. This is true only after the finds of line L10. Code that uses the values from before the finds links with the value of one edge instead of the whole path.
- **Forgetting to negate on a swap.** Line L12 must replace $d$ by $-d$ when it swaps $x$ and $y$. Without it, every union where the first tree is larger stores the fact with the wrong sign.
- **Compression without the sum.** In FIND, line L5 must run before line L6. Pointing $x$ at the root first leaves the value of the old edge on the new edge.
- **The wrong order for a non-commutative group.** With permutations or matrices, line L5 must multiply in the order of the path. Swapping the factors gives wrong answers that pass every test with an abelian group.

## Implementations

The Python class takes the group as three arguments, an addition, a negation and a zero, with integer addition as the default. Its `find` uses two loops, `union` returns whether the fact agrees with the earlier ones, and `diff` returns `None` for elements of different sets. `check_invariant` tests the forest, the sizes and the zero values at the roots.

## History

Storing a value on each edge of the forest and combining the values during path compression is a folklore extension of union-find. cp-algorithms describes the cases of distances and of parities, and competitive programmers also call the structure potentialized union-find. The bounds are those of the plain forest, by Tarjan (1975), because the values do not change the shape of the trees.

## References
