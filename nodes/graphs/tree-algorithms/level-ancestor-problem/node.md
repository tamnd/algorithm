---
tag: HM9FRT
kind: problem
slug: level-ancestor-problem
name: Level ancestor problem
aliases:
- level ancestor query
area: graphs/tree-algorithms
level: advanced
summary: Find the ancestor of a node at a given depth.
prereqs: [rooted-tree]
see_also: [ladder-decomposition, binary-lifting, lca-binary-lifting, lowest-common-ancestor, heavy-light-decomposition, tree-path-queries, euler-tour-technique, suffix-tree]
sources:
  - paper: doi:10.1016/j.tcs.2003.05.002
    title: "Michael A. Bender and Martin Farach-Colton, The level ancestor problem simplified, Theoretical Computer Science 321(1) (2004), 5-12"
    locator: the whole paper (the table, jump-pointer, ladder and macro-micro algorithms, ending with O(n) preprocessing and O(1) query)
  - paper: "Omer Berkman and Uzi Vishkin, Finding level-ancestors in trees, Journal of Computer and System Sciences 48(2) (1994), 214-230"
    locator: the whole paper (O(n) preprocessing and O(1) query, through a reduction to the Euler tour)
  - paper: "Paul F. Dietz, Finding level-ancestors in dynamic trees, Algorithms and Data Structures (WADS 1991), LNCS 519, 32-40"
    locator: the whole paper (level ancestors in a tree that grows by adding leaves)
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 18, Tree queries, Section 18.1 (Finding ancestors, the k-th ancestor with ancestor tables)
---

The level ancestor problem asks to preprocess a [rooted tree](/rooted-tree/) so that, given a vertex $v$ and a depth $d$, the ancestor of $v$ at depth $d$ can be found quickly. Equivalently, it asks for the $k$-th ancestor of $v$, with $k = depth(v) - d$. Walking up the parent pointers takes time proportional to $k$; [binary lifting](/binary-lifting/) takes $O(\log n)$; and the [ladder decomposition](/ladder-decomposition/) with jump pointers, refined by a split into macro and micro trees, reaches $O(n)$ preprocessing and $O(1)$ time per query on a word RAM. Level ancestors are the vertical half of most path queries, next to the [lowest common ancestor](/lowest-common-ancestor/).

## In plain words

In a family tree, someone asks: "who was my ancestor four generations back?" or "who in my line belonged to the second generation?" Climbing one parent at a time works, but in a long family line it takes many steps for every question.

If many such questions will be asked, it pays to write some notes once in advance, so that each answer takes only a few steps. The level ancestor problem is about how little preparation is needed so that every such question can be answered in a fixed number of steps, no matter how tall the tree is.

## Definition

The input is a tree with vertices $0, \ldots, n - 1$, $n \ge 1$, rooted at a vertex $r$, given by a parent array or by its $n - 1$ edges. The tree is unweighted; $depth(v)$ is the number of edges from $r$ to $v$. For a vertex $v$ and an integer $d$ with $0 \le d \le depth(v)$, the *level ancestor* $\mathrm{LA}(v, d)$ is the unique vertex at depth $d$ on the path from $v$ to $r$. For $d > depth(v)$ or $d < 0$ there is no answer, and an implementation reports that.

The *$k$-th ancestor* is $\mathrm{anc}(v, k) = \mathrm{LA}(v, depth(v) - k)$ for $0 \le k \le depth(v)$; $\mathrm{anc}(v, 0) = v$ and $\mathrm{anc}(v, 1)$ is the parent.

The problem asks for a structure, built once, that answers online queries $\mathrm{LA}(v, d)$; it is measured by the preprocessing time, the space and the query time.

## Variants

- **$k$-th ancestor queries.** The same problem, indexed by distance instead of depth; one subtraction converts between them.
- **Offline queries.** All queries are known first. A single depth-first search that keeps the current root path in an array answers $\mathrm{LA}(v, d)$ as entry $d$ of that array when it reaches $v$, in $O(n + q)$ total time.
- **Weighted level ancestors.** Edges have positive weights, and the query asks for the highest ancestor whose weighted depth is at least $d$. This is the version used on [suffix trees](/suffix-tree/), where the weight is the string depth. It is harder: it needs a predecessor search on the path, see the [predecessor problem](/predecessor-problem/).
- **Dynamic trees.** Leaves are added (Dietz 1991; Alstrup and Holm 2000), or the tree changes by links and cuts, where a [link-cut tree](/link-cut-tree/) answers in $O(\log n)$ amortized time.
- **The $k$-th vertex on a path.** Given $u$, $v$ and $k$, return the $k$-th vertex on the path from $u$ to $v$. With $w = \mathrm{lca}(u, v)$, it is $\mathrm{anc}(u, k)$ if $k \le depth(u) - depth(w)$ and otherwise $\mathrm{anc}(v, \mathrm{dist}(u, v) - k)$.

## Examples

Take the tree on $0, \ldots, 11$ rooted at 0 with the parent array $[-, 0, 1, 2, 3, 4, 2, 6, 0, 8, 3, 7]$:

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

The depths are $[0, 1, 2, 3, 4, 5, 3, 4, 1, 2, 4, 5]$.

| query | root path | answer |
|---|---|---|
| $\mathrm{LA}(11, 2)$ | $11, 7, 6, 2, 1, 0$ | 2 |
| $\mathrm{LA}(5, 3)$ | $5, 4, 3, 2, 1, 0$ | 3 |
| $\mathrm{LA}(10, 4)$ | $10, 3, 2, 1, 0$ | 10, the vertex itself |
| $\mathrm{LA}(9, 0)$ | $9, 8, 0$ | 0, the root |
| $\mathrm{anc}(11, 4)$ | $11, 7, 6, 2, 1, 0$ | 1 |
| $\mathrm{LA}(9, 3)$ | $9, 8, 0$ | none, since $depth(9) = 2$ |

The 3rd vertex on the path from 5 to 11 (counting 5 as the 0th) is found from $w = \mathrm{lca}(5, 11) = 2$: $depth(5) - depth(2) = 3$, so it is $\mathrm{anc}(5, 3) = 2$; the 4th is $\mathrm{anc}(11, 6 - 4) = 6$, since $\mathrm{dist}(5, 11) = 6$ and the path is $5, 4, 3, 2, 6, 7, 11$.

Small trees show the extremes. On the single-vertex tree the only query is $\mathrm{LA}(0, 0) = 0$. On a path $0 - 1 - \cdots - (n-1)$ rooted at 0, $\mathrm{LA}(v, d) = d$: the answer is easy, but the naive walk takes $v - d$ steps, up to $n - 1$. On a star rooted at its center, every query has $d \le 1$ and the naive walk takes at most one step.

## Known algorithms

| algorithm | preprocessing | query | notes |
|---|---|---|---|
| walk up the parents | $O(n)$ | $O(k)$ | $k = depth(v) - d$, up to $n - 1$ |
| table of all ancestors | $O(n^2)$ | $O(1)$ | the table method of Bender and Farach-Colton |
| [binary lifting](/binary-lifting/) (jump pointers) | $O(n \log n)$ | $O(\log n)$ | also gives the LCA, see [LCA by binary lifting](/lca-binary-lifting/) |
| [heavy-light decomposition](/heavy-light-decomposition/) | $O(n)$ | $O(\log n)$ | jump to path heads, then index into the path |
| ladders alone | $O(n)$ | $O(\log n)$ | climb ladder by ladder |
| [jump pointers and ladders](/ladder-decomposition/) | $O(n \log n)$ | $O(1)$ | one jump, then one ladder lookup |
| macro-micro trees (Bender and Farach-Colton) | $O(n)$ | $O(1)$ | jump-ladder on the $O(n / \log n)$ macro vertices, tables for small subtrees |
| offline DFS with a path array | $O(n + q)$ total | | all queries known first |

With heavy-light decomposition, vertices are numbered so that each heavy path occupies consecutive positions $pos$. A query jumps from $v$ to the parent of its path head while the head is deeper than $d$, then returns the vertex at position $pos[head] + d - depth(head)$ of the current path. Each jump crosses a light edge, so there are $O(\log n)$ jumps.

The jump-ladder algorithm stores, for each vertex, its ancestors at distances $2^i$ (jump pointers), and for each path of a longest-path decomposition, the path extended upward by its own length (ladders). A query takes the largest jump $2^i \le k$; the vertex reached has height at least $2^i$, so its ladder reaches $2^i \ge k - 2^i$ more levels up, and one lookup in that ladder gives the answer.

## Bounds

- **Upper bound.** $O(n)$ preprocessing, $O(n)$ space and $O(1)$ query time on a word RAM with $\Theta(\log n)$-bit words (Berkman and Vishkin 1994; Bender and Farach-Colton 2004). This is optimal up to constant factors, since the tree must be read and each answer takes at least one step.
- **Trade-offs.** Without table lookups on words, the jump-ladder method still gives $O(1)$ queries, with $O(n \log n)$ preprocessing.
- **Offline.** $O(n + q)$ total time, which is linear in the input and output.

## Reductions

- **$k$-th ancestor to level ancestor and back.** One subtraction with the stored depth.
- **LCA from level ancestors.** $\mathrm{lca}(u, v)$ is $\mathrm{LA}(u, d^*)$ for the largest $d^*$ with $\mathrm{LA}(u, d^*) = \mathrm{LA}(v, d^*)$, after both are brought to the same depth; a binary search on $d^*$ finds it with $O(\log n)$ level ancestor queries. This is the second half of [LCA by binary lifting](/lca-binary-lifting/).
- **Path $k$-th vertex to LCA and LA.** As in the Variants section, one LCA query and one level ancestor query.
- **Level ancestor to the Euler tour.** In the [Euler tour](/euler-tour-technique/) of $2n - 1$ entries, $\mathrm{LA}(v, d)$ is the last entry at depth $d$ at or before the first occurrence of $v$. Berkman and Vishkin solve the problem through this view.

## Applications

- **Path queries on trees.** The $k$-th vertex on a path, splitting paths at given depths, and walking up by a given distance, see [path queries on trees](/tree-path-queries/).
- **Strings.** On a suffix tree, the weighted version finds the locus of a substring $S[i .. j]$ from the leaf of suffix $i$: it is the highest ancestor of that leaf with string depth at least $j - i + 1$.
- **Binary search over the root path.** Any monotone property of ancestors, such as "the first ancestor whose value exceeds $x$", becomes a binary search with level ancestor queries.
- **Building block for LCA.** Binary lifting answers level ancestors and LCAs with the same table.

## References
