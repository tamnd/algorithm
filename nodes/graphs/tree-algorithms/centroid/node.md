---
tag: MQ5GCC
kind: concept
slug: centroid
name: Tree centroid
aliases:
- centroid of a tree
area: graphs/tree-algorithms
level: intro
summary: A vertex whose removal leaves components of at most n/2 nodes each; always exists.
prereqs: [tree, subtree-sizes]
see_also: [centroid-decomposition, tree-center, eccentricity, subtree-sizes, tree-isomorphism, rerooting-technique, planar-separator-theorem, k-median-problem]
sources:
  - paper: "Camille Jordan, Sur les assemblages de lignes, Journal fur die reine und angewandte Mathematik 70 (1869), 185-190"
    locator: the centre of gravity of a tree (the branch weight), and the result that it is one vertex or two adjacent vertices
  - book: isbn:9780201027877
    title: Frank Harary, Graph Theory, Addison-Wesley, 1969
    locator: Chapter 4 (Trees), the section on centers and centroids, with the branch weight and the theorem that the centroid is one vertex or two adjacent vertices
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 14 (Tree algorithms) for subtree sizes and tree dynamic programming, used to find the centroid in linear time
---

A centroid of a tree with $n$ vertices is a vertex whose removal splits the tree into parts with at most $n/2$ vertices each. Every tree has one or two centroids, and when it has two they are adjacent and each side of the edge between them has exactly $n/2$ vertices. One pass that computes [subtree sizes](/subtree-sizes/) finds a centroid in $O(n)$ time. Because a centroid cuts a tree into parts of at most half the size, it is the standard split point for divide and conquer on trees, as in [centroid decomposition](/centroid-decomposition/), and a canonical root for comparing trees.

## In plain words

Think of a tree as a set of towns joined by roads with no loops. You close one town. The roads that met there are now cut, and the rest of the map falls into separate pieces. A centroid is a town to close so that no piece has more than half of the towns.

Such a town always exists. Start anywhere. If one piece is too big, step into it, one town toward its middle. Each step makes the big piece smaller, and you stop when no piece is bigger than half. Closing the centroid is the most even way to break a tree with one cut.

## The idea

**Definition.** Let $T$ be a [free tree](/free-tree-properties/) on the vertices $0, \ldots, n-1$, $n \ge 1$, unrooted and unweighted. For a vertex $v$, the *branch weight* $bw(v)$ is the largest number of vertices in a component of $T - v$, or 0 if $n = 1$. A vertex $c$ is a *centroid* if $bw(c) \le n/2$. Jordan (1869) defined the *centroid* of $T$ as the set of vertices of least branch weight; by the two facts below, that set is exactly the set of vertices with $bw \le n/2$.

**Existence.** Start at any vertex $v$. If $bw(v) > n/2$, let $C$ be the component of $T - v$ with more than $n/2$ vertices; there is only one such component, since two would hold more than $n$ vertices. Let $u$ be the neighbor of $v$ in $C$, and move to $u$. The components of $T - u$ are the parts of $C - u$, each smaller than $|C|$, and the part that contains $v$, which has $n - |C| < n/2$ vertices. So if $bw(u) > n/2$, the large component of $T - u$ is a part of $C - u$ and has fewer vertices than $C$. The size of the large component drops at each step, so the walk stops after at most $n - 1$ steps, at a vertex with $bw \le n/2$.

**At most two, and adjacent.** Let $c \ne c'$ be two centroids, and let $A$ be the component of $T - c$ that contains $c'$, so $|A| \le n/2$. The component of $T - c'$ that contains $c$ holds all $n - |A| \ge n/2$ vertices outside $A$, and also every vertex strictly between $c$ and $c'$ on the path joining them. Since it has at most $n/2$ vertices, $|A| = n/2$ and the path has no inner vertex: $c$ and $c'$ are adjacent and $n$ is even. Three centroids would be pairwise adjacent, which a tree does not allow.

**Linear-time search.** Root $T$ at any vertex $r$ and compute $size(v)$, the number of vertices in the subtree of $v$, by a post-order pass or a reverse [BFS](/breadth-first-search/) order. The components of $T - v$ are the subtrees of the children of $v$ and the rest of the tree, which has $n - size(v)$ vertices, so
$$bw(v) = \max\Big(n - size(v),\ \max_{c \text{ child of } v} size(c)\Big).$$
Evaluating this for every $v$ takes $O(n)$ time in total. The walk of the existence proof is the same search done top-down: from the root, move to a child with $size > n/2$ while one exists.

**The centroid is the median.** Let $D(v) = \sum_{u} d(v, u)$ be the sum of the distances from $v$. If $u$ is a neighbor of $v$ and $s$ is the number of vertices on $u$'s side of the edge $uv$, then moving from $v$ to $u$ brings $s$ vertices one step closer and $n - s$ one step farther, so $D(u) = D(v) + n - 2s$. So $D$ decreases along an edge exactly when it moves toward a side with more than $n/2$ vertices. A vertex that minimizes $D$ has no such neighbor, so it is a centroid. Conversely, each centroid has the least $D$: if there is one centroid it must be the minimizer, and if there are two, the edge between them has $s = n/2$ on each side, so they have equal $D$. A centroid is thus a 1-median of the tree, the best single site for a facility when the cost is the total distance.

**Centroid and center are different.** The [center](/tree-center/) minimizes the largest distance, the [eccentricity](/eccentricity/), and is the middle of a longest path. The centroid minimizes the largest part, and the total distance. On a path they coincide; on a tree with a long thin branch and a bushy part they can be far apart.

## Examples

The trees have vertices $0, \ldots, n-1$ and no weights.

**The 12-vertex tree.** The edges are given by the parent array $[-, 0, 1, 2, 3, 4, 2, 6, 0, 8, 3, 7]$ with respect to vertex 0:

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

Rooted at 0 the subtree sizes are $[12, 9, 8, 4, 2, 1, 3, 2, 2, 1, 1, 1]$. The table lists the components of $T - v$ for some $v$, the branch weight and the total distance $D(v)$:

| $v$ | sizes of the components of $T - v$ | $bw(v)$ | $D(v)$ |
|---|---|---|---|
| 0 | 9, 2 | 9 | 34 |
| 1 | 3, 8 | 8 | 28 |
| 2 | 4, 4, 3 | 4 | 24 |
| 3 | 8, 2, 1 | 8 | 28 |
| 6 | 9, 2 | 9 | 30 |
| 5 | 11 | 11 | 46 |

The only centroid is 2, with $bw(2) = 4 \le 6$. The top-down walk goes $0 \to 1$ (since $size(1) = 9 > 6$), $1 \to 2$ (since $size(2) = 8 > 6$), and stops at 2, whose children have sizes 4 and 3. Vertex 2 also has the least total distance, 24, as the median property says. The center of this tree is $\{1, 2\}$, since both have eccentricity 4, so here the center contains a vertex, 1, that is not a centroid.

Small shapes:

- **One vertex.** $T - 0$ is empty, $bw(0) = 0$, and 0 is the centroid.
- **A path** $0 - 1 - \cdots - (n-1)$. For odd $n$ the centroid is the middle vertex $(n-1)/2$. For even $n$ there are two centroids, $n/2 - 1$ and $n/2$, adjacent, and removing either leaves a part of exactly $n/2$ vertices. With $n = 4$: removing 1 leaves parts of sizes 1 and 2, and removing 2 leaves 2 and 1.
- **A star** with center 0 and $n - 1 \ge 2$ leaves. Removing 0 leaves $n - 1$ parts of size 1, so 0 is the centroid. Removing a leaf leaves one part of size $n - 1 > n/2$ when $n \ge 3$. For $n = 2$ both vertices are centroids.

## Where it is used

- **[Centroid decomposition](/centroid-decomposition/).** Remove a centroid, recurse on each part. Each part has at most half the vertices, so the recursion has depth at most $\lfloor \log_2 n \rfloor + 1$, which gives $O(n \log n)$ algorithms for path counting and for distance queries on trees.
- **Tree isomorphism.** An unrooted tree has one or two centroids, so to compare two free trees one roots each at its centroid (or tries both) and compares the rooted trees, as in [tree isomorphism](/tree-isomorphism/) and [tree hashing](/tree-hashing/). The [center](/tree-center/) is used the same way.
- **Separators.** A centroid is a one-vertex separator that leaves parts of at most $n/2$ vertices. It is the tree case of the [planar separator theorem](/planar-separator-theorem/), with a separator of one vertex instead of $O(\sqrt n)$ vertices.
- **Facility location.** The centroid is the 1-median of a tree with unit weights; with vertex weights, the same walk finds the weighted median by comparing weights instead of counts. The general [k-median problem](/k-median-problem/) on trees has polynomial algorithms that build on this property.
- **All branch weights at once.** The formula for $bw(v)$ is a simple case of the [rerooting technique](/rerooting-technique/): it reads, for each $v$, the size of the part "above" $v$ as $n - size(v)$.

## References
