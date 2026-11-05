---
tag: SKXZFC
kind: algorithm
slug: euler-tour-lca
name: LCA by Euler tour and RMQ
aliases:
- Euler tour LCA
area: graphs/tree-algorithms
level: advanced
summary: Reduce LCA to a range-minimum query on the Euler tour; constant time per query after preprocessing.
solves: [lowest-common-ancestor]
model: word-ram
complexity:
  vars: {n: the number of vertices of the tree}
  time: {build: Θ(n log n), query: O(1)}
  space: {extra: Θ(n log n)}
properties: {deterministic: true, online: true, recursive: false}
prereqs: [euler-tour-technique, lowest-common-ancestor, range-minimum-query, sparse-table]
see_also: [lca-binary-lifting, rmq-lca-equivalence, bender-farach-colton-rmq, tarjan-offline-lca, cartesian-tree, fischer-heun-rmq, segment-tree, tree-path-queries]
sources:
  - paper: doi:10.1007/10719839_9
    title: "Michael A. Bender and Martin Farach-Colton, The LCA Problem Revisited, LATIN 2000: Theoretical Informatics, LNCS 1776, 88-94"
    locator: Section 2 (the Euler tour, the level array and the reduction from LCA to RMQ) and Section 3 (the sparse table and the plus-minus-one RMQ with O(n) preprocessing)
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 18, Tree queries, Section 18.3 (Lowest common ancestor, the second method, with the tree traversal array and a range minimum query)
  - url: https://cp-algorithms.com/graph/lca.html
    title: cp-algorithms, Lowest Common Ancestor, O(sqrt(N)) and O(log N) with O(N) preprocessing
    locator: the sections Idea of the algorithm and Implementation (the Euler tour, the first occurrence array and a range minimum structure)
  - paper: "Omer Berkman and Uzi Vishkin, Recursive star-tree parallel data structure, SIAM Journal on Computing 22(2) (1993), 221-242"
    locator: the reduction of LCA to a range minimum on the Euler tour with levels that differ by one
  - paper: "Dov Harel and Robert E. Tarjan, Fast algorithms for finding nearest common ancestors, SIAM Journal on Computing 13(2) (1984), 338-355"
    locator: the first O(n) preprocessing and O(1) query algorithm, for comparison
---

LCA by Euler tour and RMQ answers the [lowest common ancestor](/lowest-common-ancestor/) query in a static rooted tree by turning it into a [range minimum query](/range-minimum-query/). A depth-first walk writes down a vertex each time it is entered or returned to, which gives a sequence of $2n - 1$ vertices, the [Euler tour](/euler-tour-technique/). Between the first visits of $u$ and $v$ the walk never leaves the subtree of their LCA and passes through the LCA itself, so the LCA is the vertex of least depth in that stretch. With a [sparse table](/sparse-table/) over the depths, preprocessing takes $\Theta(n \log n)$ time and each query takes $O(1)$; with the plus-minus-one RMQ of Bender and Farach-Colton, preprocessing drops to $O(n)$.

## In plain words

Walk around a family tree drawn on paper, keeping a hand on the lines, starting at the top person. Every time you pass a person, write down their name and their generation. You pass each person when you first reach them and again each time you come back from one of their children.

To find the closest shared ancestor of two people, look at your list between the first time you wrote one of them and the first time you wrote the other. Going from one to the other, the walk had to climb up to the shared ancestor and could not climb any higher. So the person with the oldest generation in that part of the list is the answer. A table built once in advance finds the oldest generation in any part of the list with two lookups.

## The problem

The input is a tree with vertices $0, \ldots, n - 1$, $n \ge 1$, given by its $n - 1$ undirected edges, and a root $r$. The tree is rooted at $r$ and unweighted; the depth of a vertex is its number of edges from $r$. After preprocessing, each query gives two vertices $u$ and $v$ and asks for $\mathrm{lca}(u, v)$, the deepest vertex that is an ancestor of both, where every vertex is an ancestor of itself. Queries arrive online, and the tree does not change.

## The algorithm

The tour $E[0 .. 2n - 2]$ is built by an iterative depth-first search, with children in a fixed order (here, by label). $first[v]$ is the index of the first occurrence of $v$ in $E$. The sparse table $M[k][i]$ holds the vertex of least depth among $E[i], \ldots, E[i + 2^k - 1]$.

```pseudo id=main
PREPROCESS(T, r)
L1  depth[r] ← 0; first[r] ← 0; E ← [r]; S ← stack holding r
L2  while S is not empty do
L3      v ← top of S
L4      if v has a child c that has not been entered then
L5          depth[c] ← depth[v] + 1; first[c] ← |E|; append c to E; push c on S
L6      else pop S; if S is not empty then append the new top of S to E
L7  for i ← 0 to |E| − 1 do M[0][i] ← E[i]
L8  for k ← 1 while 2^k ≤ |E| do for i ← 0 to |E| − 2^k do
L9      M[k][i] ← the shallower of M[k − 1][i] and M[k − 1][i + 2^(k−1)]

LCA(u, v)
L10 l ← min(first[u], first[v]); h ← max(first[u], first[v])
L11 k ← ⌊lg(h − l + 1)⌋
L12 return the shallower of M[k][l] and M[k][h − 2^k + 1]
```

Lines L1 to L6 are the Euler tour; each vertex is pushed once, and line L6 writes the parent again each time a child is finished. Lines L7 to L9 build the sparse table. A query reads two overlapping blocks of length $2^k$ that together cover $E[l .. h]$. Ties in "the shallower" may be broken either way, since the proof shows that the least depth in the range is reached only by the LCA.

## Example

Take the tree on $0, \ldots, 11$ rooted at 0 with the parent array $[-, 0, 1, 2, 3, 4, 2, 6, 0, 8, 3, 7]$ and children ordered by label:

```
0
├── 1
│   └── 2
│       ├── 3
│       │   ├── 4
│       │   │   └── 5
│       │   └── 10
│       └── 6
│           └── 7
│               └── 11
└── 8
    └── 9
```

The tour has $2 \cdot 12 - 1 = 23$ entries:

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $E[i]$ | 0 | 1 | 2 | 3 | 4 | 5 | 4 | 3 | 10 | 3 | 2 | 6 | 7 | 11 | 7 | 6 | 2 | 1 | 0 | 8 | 9 | 8 | 0 |
| depth | 0 | 1 | 2 | 3 | 4 | 5 | 4 | 3 | 4 | 3 | 2 | 3 | 4 | 5 | 4 | 3 | 2 | 1 | 0 | 1 | 2 | 1 | 0 |

The first occurrences are $first = [0, 1, 2, 3, 4, 5, 11, 12, 19, 20, 8, 13]$.

- $\mathrm{lca}(5, 11)$: the range is $E[5 .. 13] = 5, 4, 3, 10, 3, 2, 6, 7, 11$. Its length is 9, so $k = 3$ and the two blocks are $E[5 .. 12]$ and $E[6 .. 13]$; both have least depth 2, at vertex 2. The answer is 2.
- $\mathrm{lca}(9, 10)$: the range is $E[8 .. 20]$, of length 13, with $k = 3$ and blocks $E[8 .. 15]$ (least depth 2, vertex 2) and $E[13 .. 20]$ (least depth 0, vertex 0 at index 18). The answer is 0.
- $\mathrm{lca}(4, 10)$: the range $E[4 .. 8] = 4, 5, 4, 3, 10$ has least depth 3, at vertex 3.
- $\mathrm{lca}(5, 4) = 4$, from $E[4 .. 5]$: a vertex is the LCA of itself and any descendant.
- $\mathrm{lca}(7, 7)$: the range is the single entry $E[12] = 7$.

On a single-vertex tree, $E = [0]$, $first = [0]$ and every query returns 0. On a path $0 - 1 - \cdots - (n-1)$ rooted at 0, $E = 0, 1, \ldots, n - 1, n - 2, \ldots, 0$ and $\mathrm{lca}(u, v) = \min(u, v)$. On a star with center 0 and leaves $1, \ldots, n - 1$, $E = 0, 1, 0, 2, 0, \ldots, n - 1, 0$, and two different leaves have LCA 0 because a 0 lies between their first occurrences.

## Correctness

The full proof is in the proof file; this is its outline. Let $w = \mathrm{lca}(u, v)$ and assume $first[u] \le first[v]$.

1. **The tour.** Lines L1 to L6 append a vertex each time it is entered or returned to, so $E$ has $n + (n - 1) = 2n - 1$ entries, and consecutive entries are adjacent in the tree. The entries from $first[x]$ up to the moment $x$ is popped are exactly the visits to the subtree of $x$, and they form a contiguous block.
2. **The range stays in the subtree of $w$.** Both $u$ and $v$ are in the subtree of $w$, so $first[w] \le first[u] \le first[v]$, and $first[v]$ comes before $w$ is popped. The range $E[first[u] .. first[v]]$ is inside the block of $w$, so every vertex in it has depth at least $depth(w)$.
3. **The range contains $w$.** If $u = w$, $E[first[u]] = w$. Otherwise $u$ and $v$ are in the subtrees of two different children $c_1$ and $c_2$ of $w$, and $c_1$ comes first. When $c_1$ is popped, line L6 appends $w$, after $first[u]$ and before $c_2$, and hence $v$, is entered.
4. **Only $w$ has the least depth.** A vertex of the subtree of $w$ with depth $depth(w)$ is $w$ itself. So the shallowest entry of the range is $w$, whatever the tie-breaking.
5. **The sparse table.** By induction on $k$, $M[k][i]$ is a shallowest vertex of $E[i .. i + 2^k - 1]$. In line L12, $2^k \le h - l + 1 < 2^{k+1}$, so the blocks starting at $l$ and ending at $h$ lie inside the range and cover it. The shallower of their minima is a shallowest entry of the range, which is $w$.

The loop of lines L2 to L6 ends because each vertex is pushed once and popped once.

## Complexity

The tour takes $\Theta(n)$ time: each of the $2n - 1$ iterations of the loop either pushes a new vertex or pops one, provided each vertex keeps a pointer to its next unvisited child. The sparse table has $\lfloor \lg(2n - 1) \rfloor + 1$ levels of at most $2n - 1$ entries, so lines L7 to L9 take $\Theta(n \log n)$ time and space. A query is $O(1)$: two lookups of $first$, a floor of a logarithm (a table of $\lfloor \lg m \rfloor$ for $m \le 2n - 1$, or a leading-zero count on the [word RAM](/word-ram/)), two table lookups and one comparison of depths.

| | preprocessing | query | space |
|---|---|---|---|
| tour + sparse table (this page) | $\Theta(n \log n)$ | $O(1)$ | $\Theta(n \log n)$ |
| tour + [segment tree](/segment-tree/) | $\Theta(n)$ | $O(\log n)$ | $\Theta(n)$ |
| tour + plus-minus-one RMQ ([Bender and Farach-Colton](/bender-farach-colton-rmq/)) | $\Theta(n)$ | $O(1)$ | $\Theta(n)$ |
| [binary lifting](/lca-binary-lifting/) | $\Theta(n \log n)$ | $O(\log n)$ | $\Theta(n \log n)$ |

## Properties

- **Online and static.** Queries can come in any order after preprocessing, but a change to the tree needs a new tour and table.
- **Deterministic and non-recursive.** The tour uses an explicit stack, so a path of $10^5$ vertices needs no deep recursion.
- **Plus-minus-one depths.** Adjacent entries of the depth sequence differ by exactly 1. This is the property that the linear-time RMQ of Bender and Farach-Colton uses: there are only $O(\sqrt{n})$ different normalized blocks of length $\frac{1}{2} \lg n$, so the in-block answers can be tabulated.
- **Order of children.** Any fixed order of children gives a valid tour; the answers do not depend on it.
- **Equivalence with RMQ.** Together with the [Cartesian tree](/cartesian-tree/), which turns RMQ into LCA, this shows that the two problems are equivalent up to linear-time reductions ([RMQ and LCA equivalence](/rmq-lca-equivalence/)).

## Variants and improvements

- **Linear preprocessing.** Split the depth sequence into blocks of $\frac{1}{2} \lg n$ entries, build a sparse table over the block minima, and answer inside blocks with a table indexed by the pattern of $+1$ and $-1$ steps. This is the $O(n)$, $O(1)$ algorithm of Bender and Farach-Colton.
- **The $n$-entry order with RMQ.** Store, for each vertex in preorder, the depth of its parent. The LCA of $u \ne v$ with $tin(u) < tin(v)$ is the parent of the shallowest vertex among positions $tin(u) + 1, \ldots, tin(v)$ of the preorder. This halves the length of the array.
- **Offline queries.** If all queries are known first, [Tarjan's offline LCA](/tarjan-offline-lca/) with disjoint sets answers them in nearly linear total time without a table.
- **Range structures with updates.** A segment tree over the tour handles a static tree with $O(\log n)$ queries in $\Theta(n)$ space; the [Euler tour tree](/euler-tour-tree/) keeps tours of a forest under links and cuts.

## When to use it

Use it when there are many LCA queries, say $10^6$ or more, on a static tree, and $O(1)$ per query matters; the sparse table is easy to write and fast in practice. If memory is tight, or the tree is large and the queries few, binary lifting or a segment tree over the tour is simpler. If the queries are offline, Tarjan's algorithm avoids the table. If the same table should also give $k$-th ancestors and path aggregates, binary lifting covers all three.

## Pitfalls

- **Using the $n$-entry preorder instead of the $2n - 1$ tour.** The shallowest vertex between two preorder positions need not be on the path between them; the parent must be written again after each child.
- **Taking the minimum depth instead of its vertex.** The table must keep which vertex is the shallowest, not only its depth.
- **Off-by-one in the second block.** It starts at $h - 2^k + 1$, not at $h - 2^k$.
- **Reading $first$ in the wrong order.** If $first[u] > first[v]$ the range must be swapped; forgetting this gives an empty range.
- **Recursion.** A recursive DFS overflows the Python stack on a path of $10^5$ vertices; the explicit stack of lines L1 to L6 does not.
- **Memory.** The table has about $2n \lg(2n)$ entries, which is $3.6 \cdot 10^6$ for $n = 10^5$; in tight memory, store indices in compact arrays.

## Implementations

## History

The LCA problem was posed by Aho, Hopcroft and Ullman in 1973. Harel and Tarjan gave the first algorithm with $O(n)$ preprocessing and $O(1)$ queries in 1984, but it was complicated. The reduction to a range minimum over the Euler tour, whose levels change by one at each step, appears in the parallel algorithm of Berkman and Vishkin (1993). Bender and Farach-Colton (2000) gave the short sequential version presented here, with the sparse table as the $O(n \log n)$ step and the plus-minus-one RMQ as the linear one, and it became the standard textbook route to constant-time LCA.

## References
