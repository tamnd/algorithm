---
tag: TJB8Y5
kind: technique
slug: centroid-decomposition
name: Centroid decomposition
aliases:
- recursive centroid decomposition
area: graphs/tree-algorithms
level: advanced
summary: Recursively split a tree at centroids, giving a decomposition of depth O(log n).
prereqs: [centroid, subtree-sizes, divide-and-conquer-paradigm, breadth-first-search]
see_also: [centroid, heavy-light-decomposition, tree-path-queries, lowest-common-ancestor, distance-labeling, distance-oracle, dsu-on-tree, planar-separator-theorem]
sources:
  - url: https://usaco.guide/plat/centroid
    title: USACO Guide, Centroid Decomposition
    locator: the sections Centroids, Centroid decomposition and Solution - Xenia and Tree, and the problem list (Fixed-Length Paths, IOI 2011 Race)
  - paper: "Camille Jordan, Sur les assemblages de lignes, Journal fur die reine und angewandte Mathematik 70 (1869), 185-190"
    locator: the centroid of a tree and the bound of n/2 on the parts left by its removal
  - book: isbn:9780201027877
    title: Frank Harary, Graph Theory, Addison-Wesley, 1969
    locator: Chapter 4 (Trees), the centroid and the branch weight
---

Centroid decomposition is a divide-and-conquer technique for trees: find a [centroid](/centroid/) $c$ of the tree, handle every path that passes through $c$, remove $c$, and recurse on each of the parts that are left. Each part has at most half the vertices of its parent part, so the recursion is at most $\lfloor \log_2 n \rfloor + 1$ levels deep, and the parts of one level are disjoint. So if the work at a part is linear in its size, the total is $O(n \log n)$. The centroids, linked to the centroid of the part above, form the *centroid tree*, which has height $O(\log n)$ and the property that the path between any two vertices passes through their lowest common ancestor in the centroid tree. It counts paths with a given length, and it answers "nearest marked vertex" queries in $O(\log n)$ time per operation.

## In plain words

You have a big tree and a question about all its paths, for example how many pairs of points are exactly five steps apart. There are far too many pairs to check one by one.

Pick the middle point of the tree, the one whose removal leaves no piece bigger than half. Every path either goes through that middle point or stays inside one piece. Count the paths through the middle point now, in one sweep. Then cut the middle point out and repeat the same idea inside each piece. The pieces shrink by half or more each time, so each point is swept only a few times: about as many times as you can halve the number of points.

## When it applies

- The question is about **all paths** of a tree (count, minimum, maximum of a quantity over paths), and a path through a fixed vertex $c$ can be described by two "half paths" from $c$ that start in different parts of $T - c$. Then combining half paths is a counting, sorting or two-pointer problem.
- The question is **online about distances** to a changing set of vertices: mark a vertex, ask for the nearest marked vertex, or the sum of distances to marked vertices. Every path from $v$ to $u$ passes through some centroid ancestor of $v$ in the centroid tree, and $v$ has only $O(\log n)$ of them.
- The tree is **static**. Changing edges changes the centroids; dynamic trees need other tools such as [link-cut trees](/link-cut-tree/) or [top trees](/top-tree/).
- The tree is rooted or not; the technique ignores any root. Edge weights are allowed, and the vertices are numbered $0, \ldots, n-1$.

It does not fit questions about one root-to-vertex path or one $u$-$v$ path with updates on edges: [heavy-light decomposition](/heavy-light-decomposition/) is the tool for those.

## The template

The input is a tree on the vertices $0, \ldots, n-1$ given by adjacency lists, possibly with edge weights. Every step is iterative: a work list replaces the recursion, and each part is explored with an explicit stack or a BFS queue.

```pseudo id=main
CENTROID-DECOMPOSE(T)
L1  alive[v] ← true for every v;  W ← [(0, NIL)]          ▷ work list of (vertex of a part, centroid above)
L2  while W is not empty do
L3      (s, pc) ← pop W
L4      P ← the alive vertices reachable from s through alive vertices, in BFS order, with parents and sizes
L5      c ← s;  while c has a child u in P with size(u) > |P| / 2 do c ← u
L6      cpar[c] ← pc;  clevel[c] ← 0 if pc = NIL, else clevel[pc] + 1
L7      PROCESS(c, P)                                      ▷ hole: handle the paths of P through c
L8      alive[c] ← false
L9      for each neighbor u of c with alive[u] do push (u, c) on W
```

The one hole is PROCESS. It sees the part $P$ and its centroid $c$, can walk the alive vertices from $c$ by BFS, and must handle every path of $P$ that contains $c$. Paths that avoid $c$ lie inside one of the parts that line L9 puts on the work list, and are handled there.

Line L4 computes, in the BFS order from $s$, the parent of each vertex inside $P$ and, by a reverse pass, the size of each subtree. Line L5 is the walk from the [centroid](/centroid/) page: from $s$, move to a child whose subtree holds more than half of $P$. The part above the current vertex is always smaller than half, so the walk stops at a vertex whose removal leaves parts of at most $|P|/2$ vertices.

**Why it works.** Every path of $T$ has a first vertex $c$, in the order in which the centroids are removed, among its own vertices. Until $c$ is removed, the whole path is alive and connected, so it lies inside the part $P$ whose centroid is $c$, and it contains $c$. So PROCESS$(c, P)$ sees it, and no other call does: an earlier centroid is not on the path, and after $c$ is removed the path is split. So each path is handled exactly once, at the first of its vertices to be removed, and that vertex is the lowest common ancestor of its two ends in the centroid tree (the tree with the parent pointers $cpar$).

**Depth.** By line L5, every part that line L9 creates has at most $|P| / 2$ vertices. A part at level $\ell$ thus has at most $n / 2^\ell$ vertices, and since a part has at least one vertex, $\ell \le \lfloor \log_2 n \rfloor$. The centroid tree has height at most $\lfloor \log_2 n \rfloor$, so each vertex lies in at most $\lfloor \log_2 n \rfloor + 1$ parts.

### Cost

The parts of one level are disjoint, so lines L4 and L5 cost $O(n)$ per level, and $O(n \log n)$ in all. If PROCESS costs $O(|P|)$, the total stays $O(n \log n)$; if it sorts, $O(|P| \log |P|)$, the total is $O(n \log^2 n)$. The arrays $cpar$ and $clevel$ take $O(n)$ space; storing the distance from each vertex to each of its centroid ancestors takes $O(n \log n)$.

## Classic examples

The examples use the tree on $0, \ldots, 11$ with the parent array $[-, 0, 1, 2, 3, 4, 2, 6, 0, 8, 3, 7]$ with respect to vertex 0, unweighted:

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

**The decomposition.** The first part is the whole tree, and its centroid is 2: removing 2 leaves the parts $\{0, 1, 8, 9\}$, $\{3, 4, 5, 10\}$ and $\{6, 7, 11\}$, of sizes 4, 4 and 3, all at most 6. Their centroids are 0, 3 and 7. Removing 0 leaves $\{1\}$ and $\{8, 9\}$; removing 3 leaves $\{4, 5\}$ and $\{10\}$; removing 7 leaves $\{6\}$ and $\{11\}$. The part $\{8, 9\}$ has two centroids, and the walk from 8 stops at 8. The centroid tree:

```
2
├── 0
│   ├── 1
│   └── 8
│       └── 9
├── 3
│   ├── 4
│   │   └── 5
│   └── 10
└── 7
    ├── 6
    └── 11
```

$cpar = [2, 0, -, 2, 3, 4, 7, 2, 0, 8, 3, 7]$ and $clevel = [1, 2, 0, 1, 2, 3, 2, 1, 2, 3, 2, 2]$. The height is 3, within the bound $\lfloor \log_2 12 \rfloor = 3$. The path from 5 to 9 in $T$ is $5, 4, 3, 2, 1, 0, 8, 9$, and the lowest common ancestor of 5 and 9 in the centroid tree is 2, which is on that path.

**1. Count the pairs at distance $k$.** PROCESS does a BFS from $c$ over $P$, and for each child $u$ of $c$ in $P$ it collects the counts $cnt_u[d]$ of vertices of $u$'s branch at distance $d$ from $c$. A pair through $c$ is $c$ with a vertex at distance $k$, or two vertices in different branches with distances $d$ and $k - d$. Keep a running total $tot[d]$ over the branches done so far, and for each new branch add $\sum_d cnt_u[d] \cdot tot[k - d]$ before merging $cnt_u$ into $tot$. That costs $O(|P|)$. For $k = 3$ on the example, at $c = 2$:

| branch | distances from 2 |
|---|---|
| $\{1, 0, 8, 9\}$ | 1, 2, 3, 4 |
| $\{3, 4, 10, 5\}$ | 1, 2, 2, 3 |
| $\{6, 7, 11\}$ | 1, 2, 3 |

The pairs with 2 itself are $(2, 8)$, $(2, 5)$ and $(2, 11)$: 3 pairs. The pairs across branches use the distances $1 + 2$: the products $1 \cdot 2 + 1 \cdot 1$ (one 1 from the first branch with the 2s of the others), $1 \cdot 1 + 1 \cdot 1$ (from the second), $1 \cdot 1 + 1 \cdot 2$ (from the third), 8 pairs. So 11 pairs pass through 2. In the parts below, $(1, 9)$ passes through 0 and $(5, 10)$ through 3, and no other pair at distance 3 is left. The total is 13, which a BFS from every vertex confirms; the full distribution of the 66 pairs over the distances $1, \ldots, 7$ is $11, 12, 13, 12, 10, 6, 2$. This is the CSES problem Fixed-Length Paths I, and with weights and "fewest edges" it is IOI 2011 Race.

**2. Nearest marked vertex.** Keep $best[a]$ for every vertex $a$, the least distance from $a$ to a marked vertex in $a$'s part, initially $\infty$. During the decomposition, store $d(v, a)$ for every centroid ancestor $a$ of $v$, from the BFS of PROCESS. To mark $v$, set $best[a] \gets \min(best[a], d(v, a))$ for each centroid ancestor $a$ of $v$, including $v$. To ask for $v$, return $\min_a (best[a] + d(v, a))$ over the same ancestors. Both take $O(\log n)$ time. It is correct because the path from $v$ to the nearest marked $u$ passes through the centroid-tree LCA $a$ of $u$ and $v$, so $d(v, u) = d(v, a) + d(a, u)$, and every other ancestor term is the length of some walk, so it is at least the true distance. On the example, after marking 9, the query for 5 checks the ancestors 5, 4, 3, 2 of 5; only $best[2] = d(2, 9) = 4$ is finite, and the answer is $d(5, 2) + 4 = 7$. This is Codeforces Xenia and Tree, the focus problem of the USACO Guide.

**3. Sum of distances to marked vertices.** Like example 2, with sums instead of minima. Each ancestor $a$ keeps the number of marked vertices in its part and the sum of their distances to $a$, and the same for its part as seen from $cpar[a]$, to subtract the vertices counted twice. Each operation takes $O(\log n)$ time.

**4. Paths with a property of their edges.** Count the paths whose edge labels form a palindrome, or whose length is at most $k$ and weight at most $w$. PROCESS turns each half path into a key, and the pairs are found with a hash map, two pointers or a [Fenwick tree](/fenwick-tree/), with an extra $\log$ factor for sorting.

## Variations

- **Edge centroid decomposition.** Split at an edge instead of a vertex. In a tree whose degrees are at most a constant $d$, some edge leaves two sides that each hold a constant fraction, depending on $d$, of the vertices; with large degrees no such edge need exist, as a star shows. Trees of large degree are first made binary by adding dummy vertices.
- **The centroid tree as an index.** Keep $cpar$ and the $O(n \log n)$ ancestor distances and answer queries with no further decomposition; this is a [distance labeling](/distance-labeling/) with labels of $O(\log^2 n)$ bits.
- **Offline over queries.** Attach each query pair $(u, v)$ to the centroid-tree LCA of $u$ and $v$, and answer all queries of a part in its PROCESS.
- **Graphs other than trees.** The same divide and conquer works with balanced separators: planar graphs with the $O(\sqrt n)$-vertex separators of the [planar separator theorem](/planar-separator-theorem/), and graphs of small treewidth with their bags.

## Pitfalls

- **Recomputing sizes.** The sizes of line L4 are inside the current part, not in the whole tree. Using the sizes from one global DFS gives wrong centroids after the first level and loses the depth bound.
- **Double counting within one branch.** Two half paths from the same branch of $c$ do not form a simple path through $c$. Either merge branch by branch, as in example 1, or count all pairs and subtract the pairs inside each branch.
- **Forgetting the paths that end at $c$.** The pairs $(c, x)$ need their own count, or $cnt[0] = 1$ for $c$ itself in $tot$.
- **Recursion.** The natural recursive code is $O(\log n)$ deep in the decomposition, but its DFS inside a part is as deep as the part, which on a path of $10^5$ vertices fails in Python. Use BFS orders, as in the template.
- **Dead vertices.** Every walk inside a part must skip vertices with $alive = $ false; one missed check lets a BFS leak into another part, and the time grows to $\Theta(n^2)$.
- **Quadratic PROCESS.** Arrays sized $n$ and cleared in each call cost $O(n)$ per part, $O(n^2)$ in all. Size them by the depth of the part, or clear only the used entries.

## Exercises

1. Prove that the centroid-tree LCA of $u$ and $v$ lies on the path from $u$ to $v$ in $T$.
2. On a path $0 - 1 - \cdots - (n-1)$, describe the centroid tree. Show that it is the shape of a balanced binary search tree on $0, \ldots, n-1$, and that its height is $\lfloor \log_2 n \rfloor$.
3. On a star with center 0, show that the decomposition has two levels and that the template costs $O(n)$, not $O(n \log n)$.
4. Count the pairs of vertices at distance at most $k$ in $O(n \log^2 n)$ time, by sorting the distances in each PROCESS and using two pointers.
5. Show how to support "unmark $v$" in example 2 with a multiset of distances at each centroid, in $O(\log^2 n)$ time per operation.
6. For a tree with one vertex, what do lines L1 to L9 do? Check that $cpar[0] = $ NIL and that PROCESS is called once.

## References
