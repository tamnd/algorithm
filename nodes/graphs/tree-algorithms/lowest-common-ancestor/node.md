---
tag: HDPHEH
kind: problem
slug: lowest-common-ancestor
name: Lowest common ancestor
aliases:
- LCA
area: graphs/tree-algorithms
level: core
summary: Find the deepest node that is an ancestor of two given nodes.
prereqs: [rooted-tree]
see_also: [lca-binary-lifting, euler-tour-lca, tarjan-offline-lca, range-minimum-query, rmq-lca-equivalence, level-ancestor-problem, tree-path-queries, virtual-tree]
sources:
  - paper: "Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, On finding lowest common ancestors in trees, SIAM Journal on Computing 5(1) (1976), 115-132; first in STOC 1973"
    locator: the statement of the problem, with its online and offline versions
  - paper: "Dov Harel and Robert E. Tarjan, Fast algorithms for finding nearest common ancestors, SIAM Journal on Computing 13(2) (1984), 338-355"
    locator: the whole paper (O(n) preprocessing and O(1) query on a RAM, and the lower bound for pointer machines)
  - paper: "Baruch Schieber and Uzi Vishkin, On finding lowest common ancestors: simplification and parallelization, SIAM Journal on Computing 17(6) (1988), 1253-1262"
    locator: the whole paper (a simpler O(n), O(1) method based on inorder numbers of a complete binary tree)
  - paper: doi:10.1007/10719839_9
    title: "Michael A. Bender and Martin Farach-Colton, The LCA Problem Revisited, LATIN 2000: Theoretical Informatics, LNCS 1776, 88-94"
    locator: Section 2 (the reduction from LCA to RMQ by the Euler tour) and Section 4 (the O(n), O(1) solution)
  - paper: "Robert E. Tarjan, Applications of path compression on balanced trees, Journal of the ACM 26(4) (1979), 690-715"
    locator: the offline LCA algorithm with disjoint set union
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 18, Tree queries, Section 18.3 (Lowest common ancestor) and Section 18.4 (Offline algorithms)
---

The lowest common ancestor (LCA) of two vertices $u$ and $v$ of a [rooted tree](/rooted-tree/) is the deepest vertex that is an ancestor of both. The LCA problem asks to preprocess a tree so that LCA queries are fast. On a word RAM it is solved with $O(n)$ preprocessing and $O(1)$ time per query, and it is equivalent, up to linear-time reductions, to the [range minimum query](/range-minimum-query/) problem. The LCA gives tree distances and splits each tree path into two vertical paths, so it is the first step of most [path queries on trees](/tree-path-queries/).

## In plain words

Take a family tree with one person at the top. Pick two people. Follow the line of parents up from each of them. The two lines meet at some person and stay together from there to the top. The first person where they meet is the lowest common ancestor. If one of the two people is an ancestor of the other, the answer is that person.

The problem is to answer this question many times on the same tree. Walking up the lines each time can take as long as the tree is tall. Good methods do some work on the tree first, and then answer each question in a few steps.

## Definition

**Input.** A tree $T$ on the vertices $\{0, \ldots, n-1\}$, $n \ge 1$, with a root $r$. The tree is unweighted; edge weights, if any, play no role in the answer. Each vertex $x \ne r$ has a parent $p(x)$, and $depth(r) = 0$, $depth(x) = depth(p(x)) + 1$. A vertex $a$ is an *ancestor* of $x$ if $a$ lies on the path from $x$ to $r$; each vertex is an ancestor of itself. Then a sequence of queries $(u_1, v_1), \ldots, (u_q, v_q)$.

**Output.** For each query, $\mathrm{lca}(u_i, v_i)$, the unique vertex $a$ such that $a$ is an ancestor of both $u_i$ and $v_i$, and $depth(a) \ge depth(b)$ for each common ancestor $b$.

The answer exists because $r$ is a common ancestor. It is unique because all common ancestors of $u$ and $v$ lie on the path from $u$ to $r$, which holds one vertex of each depth. The common ancestors of $u$ and $v$ are exactly the ancestors of $\mathrm{lca}(u, v)$.

## Variants

- **Online.** Each answer is due before the next query is known. This is the usual form.
- **Offline (batch).** All $q$ queries are known in advance, so they can be answered in any order.
- **Dynamic trees.** Edges are added and removed between queries. [Link-cut trees](/link-cut-tree/) support LCA in a forest that changes by links and cuts, in $O(\log n)$ amortized time per operation.
- **A changing root.** For an unrooted tree, the query $\mathrm{lca}_w(u, v)$ asks for the LCA when the tree is rooted at $w$. With a fixed root $r$, it is the deepest of $\mathrm{lca}(u, v)$, $\mathrm{lca}(u, w)$ and $\mathrm{lca}(v, w)$, so three fixed-root queries answer it.
- **The LCA of a set.** For a set $S$ of vertices, $\mathrm{lca}(S)$ is the deepest common ancestor of all of $S$. If $a$ and $b$ are the vertices of $S$ with the smallest and the largest DFS [discovery time](/discovery-and-finish-times/), then $\mathrm{lca}(S) = \mathrm{lca}(a, b)$.
- **Distance queries.** In a weighted tree, $dist(u, v) = dist(r, u) + dist(r, v) - 2\, dist(r, \mathrm{lca}(u, v))$.

## Examples

The tree has the vertices $0, \ldots, 11$, root 0, and the parent array $[-, 0, 1, 2, 3, 4, 2, 6, 0, 8, 3, 7]$:

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

| $u$ | $v$ | $\mathrm{lca}(u, v)$ | why |
|---|---|---|---|
| 5 | 11 | 2 | the paths up are 5, 4, 3, 2 and 11, 7, 6, 2 |
| 10 | 5 | 3 | 10 and 4 are children of 3 |
| 11 | 9 | 0 | they are in different subtrees of the root |
| 7 | 2 | 2 | 2 is an ancestor of 7 |
| 4 | 4 | 4 | each vertex is its own ancestor |

With the root moved to $w = 5$, $\mathrm{lca}_5(10, 11)$ is the deepest of $\mathrm{lca}(10, 11) = 2$, $\mathrm{lca}(10, 5) = 3$ and $\mathrm{lca}(11, 5) = 2$, which is 3. In the tree rooted at 5, the paths from 10 and 11 to 5 meet first at 3.

For the set $S = \{4, 10, 7\}$, the DFS that visits children in increasing order discovers 4 at time 4, 10 at time 6 and 7 at time 8, so $\mathrm{lca}(S) = \mathrm{lca}(4, 7) = 2$.

Three small shapes:

- **One vertex.** The only query is $\mathrm{lca}(0, 0) = 0$.
- **A path** $0 - 1 - \cdots - (n-1)$ rooted at 0: $\mathrm{lca}(u, v) = \min(u, v)$. A naive walk up takes $n - 1$ steps here.
- **A star** with center 0, rooted at 0: $\mathrm{lca}(u, v) = 0$ for distinct leaves. Rooted at a leaf $w$ instead, $\mathrm{lca}_w(u, v) = 0$ for two other leaves, and $\mathrm{lca}_w(u, w) = w$.

## Known algorithms

| algorithm | preprocessing | query | notes |
|---|---|---|---|
| naive walk up | $O(n)$ | $O(h)$ | $h$ is the height, up to $n - 1$ |
| [LCA by binary lifting](/lca-binary-lifting/) | $O(n \log n)$ | $O(\log n)$ | online, also gives level ancestors |
| [Heavy-light decomposition](/heavy-light-decomposition/) | $O(n)$ | $O(\log n)$ | online, $O(n)$ memory |
| [Euler tour and RMQ](/euler-tour-lca/) with a [sparse table](/sparse-table/) | $O(n \log n)$ | $O(1)$ | online |
| [Bender-Farach-Colton](/bender-farach-colton-rmq/) | $O(n)$ | $O(1)$ | online, $\pm 1$ RMQ with blocks |
| [Tarjan's offline LCA](/tarjan-offline-lca/) | | $O((n + q)\, \alpha(n))$ total | offline, union-find |

The naive walk lifts the deeper vertex to the depth of the other, then lifts both one step at a time until they meet. Harel and Tarjan (1984) gave the first method with $O(n)$ preprocessing and $O(1)$ query time; Schieber and Vishkin (1988) simplified it.

## Bounds

- **Upper bound.** $O(n)$ preprocessing time and $O(1)$ query time in the word RAM with words of $\Theta(\log n)$ bits (Harel and Tarjan; Schieber and Vishkin; Bender and Farach-Colton). This is optimal up to constant factors, because the input has size $\Theta(n)$ and each answer needs at least one step.
- **Offline.** $O((n + q)\, \alpha(n))$ time with Tarjan's algorithm and general union-find, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/).
- **Pointer machine.** Harel and Tarjan show that on a pointer machine, without address arithmetic, an online query needs $\Omega(\log \log n)$ time in the worst case, so the $O(1)$ bound needs the RAM.

## Reductions

- **LCA to RMQ.** Write the [Euler tour](/euler-tour-technique/) of the tree, $2n - 1$ vertices, with their depths. Then $\mathrm{lca}(u, v)$ is the vertex of minimum depth between the first visits of $u$ and $v$. The depth sequence changes by $\pm 1$ at each step, which lets a block method reach $O(n)$ preprocessing. See [LCA by Euler tour](/euler-tour-lca/).
- **RMQ to LCA.** The minimum of $A[i \ldots j]$ is the LCA of $i$ and $j$ in the [Cartesian tree](/cartesian-tree/) of $A$, which is built in $O(n)$ time. Together, the two reductions give the [RMQ-LCA equivalence](/rmq-lca-equivalence/).
- **Distance to LCA.** As above, a distance query is one LCA query plus three lookups.

## Applications

- **Tree distances and path queries.** Each path $u \to v$ is $u \to \mathrm{lca} \to v$, two vertical paths, on which [binary lifting](/binary-lifting/) or [heavy-light decomposition](/heavy-light-decomposition/) works. See [path queries on trees](/tree-path-queries/).
- **[Virtual trees](/virtual-tree/).** For a set of $k$ key vertices, the key vertices and the LCAs of the pairs that are adjacent in DFS order form a tree with fewer than $2k$ vertices.
- **Strings.** The longest common prefix of two suffixes is the string depth of the LCA of their leaves in a suffix tree.
- **Phylogenetics.** [LCA reconciliation](/lca-reconciliation/) maps each node of a gene tree to the LCA of its species in the species tree.
- **[Second-best MST](/second-best-mst/) and [MST verification](/mst-verification/).** The heaviest edge on a tree path, found with an LCA.

## References
