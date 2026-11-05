---
tag: VJP1A9
kind: algorithm
slug: ladder-decomposition
name: Ladder decomposition
aliases:
- ladder algorithm
- long-path decomposition
area: graphs/tree-algorithms
level: research
summary: Answer level ancestor queries in O(1) with long-path ladders and jump pointers.
solves: [level-ancestor-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices of the tree}
  time: {build: Θ(n log n), query: O(1)}
  space: {extra: Θ(n log n)}
properties: {deterministic: true, online: true, recursive: false}
prereqs: [level-ancestor-problem, binary-lifting, rooted-tree, breadth-first-search]
see_also: [level-ancestor-problem, binary-lifting, heavy-light-decomposition, lca-binary-lifting, four-russians-method, bender-farach-colton-rmq, dsu-on-tree, tree-path-queries]
sources:
  - paper: doi:10.1016/j.tcs.2003.05.002
    title: "Michael A. Bender and Martin Farach-Colton, The level ancestor problem simplified, Theoretical Computer Science 321(1) (2004), 5-12"
    locator: the long-path decomposition, the ladder algorithm (O(n) preprocessing, O(log n) query), the jump-pointer plus ladder algorithm (O(n log n) preprocessing, O(1) query) and the macro-micro tree algorithm (O(n) preprocessing, O(1) query)
  - paper: "Omer Berkman and Uzi Vishkin, Finding level-ancestors in trees, Journal of Computer and System Sciences 48(2) (1994), 214-230"
    locator: the first O(n) preprocessing and O(1) query algorithm, which the ladder method simplifies
  - paper: "Paul F. Dietz, Finding level-ancestors in dynamic trees, Algorithms and Data Structures (WADS 1991), LNCS 519, 32-40"
    locator: the earlier level ancestor structures that Bender and Farach-Colton compare against
---

The ladder decomposition answers [level ancestor](/level-ancestor-problem/) queries, "which ancestor of $v$ is at depth $d$", in $O(1)$ time. It cuts a rooted tree into vertex-disjoint *long paths*, each going down from a vertex through the child with the tallest subtree, and stores each path as an array. Each path of $k$ vertices is then extended upward by up to $k$ more ancestors into a *ladder*, which at most doubles the total size. A query takes one jump of [binary lifting](/binary-lifting/) by the largest power of two not exceeding the distance, and the vertex reached has a subtree tall enough that its ladder already contains the answer. With jump pointers for every vertex, preprocessing takes $\Theta(n \log n)$; Bender and Farach-Colton reduce it to $O(n)$ by keeping jump pointers only for a few vertices and using tables for small subtrees.

## In plain words

Picture a family tree drawn as ladders. Starting at the top person, always follow the child with the longest line of descendants below them, all the way down: that line is one ladder. Every person not yet on a ladder starts a new one the same way.

Now make each ladder longer at the top by as many rungs as it already has, copying in the people above it. To find someone's ancestor many generations up, first take one big jump up, a power of two generations, as large as possible without overshooting. The person you land on has a long line of descendants below, so their ladder is long, and it reaches far enough up to read off the answer in one step.

## The problem

The input is a tree with vertices $0, \ldots, n - 1$, $n \ge 1$, given by its $n - 1$ undirected edges, and a root $r$. The tree is rooted at $r$ and unweighted; $depth(v)$ is the number of edges from $r$ to $v$. After preprocessing, a query $\mathrm{LA}(v, d)$ asks for the ancestor of $v$ at depth $d$, which exists for $0 \le d \le depth(v)$; for other $d$ the answer is none. The $k$-th ancestor query is $\mathrm{LA}(v, depth(v) - k)$. Queries are online, and the tree is static.

## The algorithm

Let $h(v)$ be the number of vertices on a longest downward path from $v$, so $h(\text{leaf}) = 1$. The *long child* of $v$ is a child with the largest $h$ (ties broken by the smallest label). A *head* is the root or a vertex that is not the long child of its parent; the *long path* of a head $t$ follows long children from $t$ down to a leaf and has exactly $h(t)$ vertices. The long paths partition the vertices.

```pseudo id=main
PREPROCESS(T, r)
L1  BFS from r: parent, depth and the BFS order; up[0][v] ← parent(v), with up[0][r] ← r
L2  for v in reverse BFS order do h(v) ← 1 + max h over the children (1 for a leaf); long(v) ← the child with the largest h
L3  for each head t, in BFS order, do
L4      P ← t, long(t), long(long(t)), ... down to a leaf; k ← |P|
L5      A ← the min(k, depth(t)) nearest proper ancestors of t, topmost first; ladder ← A followed by P
L6      for each x in P do lad(x) ← ladder; top(x) ← depth(t) − |A|
L7  for j ← 1 to ⌈lg n⌉ − 1 do for each v do up[j][v] ← up[j − 1][up[j − 1][v]]

LEVEL-ANCESTOR(v, d)
L8  if d < 0 or d > depth(v) then return none
L9  k ← depth(v) − d; if k = 0 then return v
L10 i ← ⌊lg k⌋; u ← up[i][v]                 ▷ the ancestor 2^i levels up
L11 return lad(u)[d − top(u)]                 ▷ the entry of u's ladder at depth d
```

Each ladder is an array indexed by depth, offset by $top$, the depth of its first entry. Line L11 is valid because $u$ has a descendant, $v$, $2^i$ levels below, so $h(u) > 2^i$, and the ladder through $u$ reaches at least $h(u)$ levels above the head of its path, while the answer is fewer than $2^i$ levels above $u$.

## Example

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

The heights are $h = [6, 5, 4, 3, 2, 1, 3, 2, 2, 1, 1, 1]$, and the long children are $long = [1, 2, 3, 4, 5, -, 7, 11, 9, -, -, -]$; at vertex 2, the children 3 and 6 both have height 3 and the smaller label wins. The heads are 0, 6, 8 and 10:

| head $t$ | long path $P$ | $k$ | ancestors $A$ added | ladder | $top$ |
|---|---|---|---|---|---|
| 0 | 0, 1, 2, 3, 4, 5 | 6 | none ($depth = 0$) | 0, 1, 2, 3, 4, 5 | 0 |
| 6 | 6, 7, 11 | 3 | 0, 1, 2 | 0, 1, 2, 6, 7, 11 | 0 |
| 8 | 8, 9 | 2 | 0 (only one exists) | 0, 8, 9 | 0 |
| 10 | 10 | 1 | 3 | 3, 10 | 3 |

The ladders have $6 + 6 + 3 + 2 = 17 \le 2n = 24$ entries.

- $\mathrm{LA}(11, 2)$: $depth(11) = 5$, $k = 3$, $i = 1$, and $u = up[1][11] = 6$. The ladder of 6 is $0, 1, 2, 6, 7, 11$ with $top = 0$; entry $2 - 0 = 2$ is vertex 2. The answer lies above the head 6, in the part added by the extension.
- $\mathrm{LA}(10, 1)$: $k = 3$, $i = 1$, $u = up[1][10] = 2$. Its ladder is the first one; entry 1 is vertex 1.
- $\mathrm{LA}(10, 3)$: $k = 1$, $u = 3$, entry 3 of the first ladder, vertex 3.
- $\mathrm{LA}(9, 3)$: $3 > depth(9) = 2$, so there is no answer.

On the single-vertex tree, there is one ladder $[0]$ and the only query $\mathrm{LA}(0, 0)$ returns 0 at line L9. On a path $0 - 1 - \cdots - (n-1)$ rooted at 0, there is one long path, the whole tree, and every query reads one entry of it. On a star with center 0, the long path of the root is $0, 1$, and each other leaf is its own head with the ladder $0, v$.

## Correctness

The full proof is in the proof file. Its steps:

1. **Long paths partition the tree.** Every vertex is on the path of exactly one head: walk up from it while the current vertex is the long child of its parent.
2. **Path length.** The long path of a head $t$ has exactly $h(t)$ vertices, since following long children follows a longest downward path.
3. **Ladders are vertical.** A ladder lists consecutive ancestors, one per depth, from depth $top$ down to the leaf at the bottom of the path, so entry $d - top$ is the ancestor at depth $d$ of every vertex of $P$ deep enough.
4. **The ladder of $u$ reaches depth $d$.** Let $t$ be the head of $u$'s path. Then $h(t) \ge h(u) \ge 2^i + 1$, so the ladder starts at depth $\max(0, depth(t) - h(t))$. Since $depth(t) - d \le depth(u) - d = k - 2^i < 2^i < h(t)$, it starts at depth at most $d$, and $d \le depth(u)$, so entry $d - top(u)$ exists and is the ancestor of $u$, hence of $v$, at depth $d$.
5. **Jump pointers.** $up[i][v]$ is the $2^i$-th ancestor of $v$, by induction on $i$, as in binary lifting; $2^i \le k \le depth(v)$ keeps the jump inside the tree.

## Complexity

Lines L1 and L2 take $\Theta(n)$. In lines L3 to L6, each long path of $k$ vertices costs $O(k)$ for $P$ and $O(k)$ for $A$, and the paths partition the vertices, so the ladders take $\Theta(n)$ time and at most $2n$ entries. Line L7 builds $\lceil \lg n \rceil$ arrays of $n$ entries in $\Theta(n \log n)$ time and space. A query does a constant number of array lookups and one $\lfloor \lg k \rfloor$, a leading-bit computation on the [word RAM](/word-ram/).

| method | preprocessing | query | space |
|---|---|---|---|
| ladders alone | $\Theta(n)$ | $O(\log n)$ | $\Theta(n)$ |
| jump pointers alone ([binary lifting](/binary-lifting/)) | $\Theta(n \log n)$ | $O(\log n)$ | $\Theta(n \log n)$ |
| jump pointers and ladders (this page) | $\Theta(n \log n)$ | $O(1)$ | $\Theta(n \log n)$ |
| macro-micro trees | $\Theta(n)$ | $O(1)$ | $\Theta(n)$ |

## Properties

- **Online and static.** Any query order is fine, but the tree cannot change.
- **Deterministic and non-recursive.** BFS and loops only; a path of $10^5$ vertices is handled without recursion.
- **Small ladders.** The ladders have at most $2n$ entries, whatever the shape of the tree.
- **Doubling.** If the ladder of a long path with $k$ vertices does not start at the root, its top vertex has height at least $2k$. So each ladder climbed at least doubles the height, which is why ladders alone give $O(\log n)$ queries.

## Variants and improvements

- **Ladders alone.** Without jump pointers, climb from $v$ to the top of its ladder and continue; each step at least doubles the height, so a query takes $O(\log n)$ steps after $O(n)$ preprocessing.
- **Jump pointers only at leaves.** A query may start its jump from any leaf below $v$ that is deep enough. Storing, for each vertex, one leaf of its subtree at maximum depth, and jump pointers only for the $L$ leaves, uses $O(n + L \log n)$ space.
- **Macro-micro trees.** Split the tree into a macro tree of vertices with large subtrees, whose $O(n / \log n)$ leaves get jump pointers, and small micro trees of $O(\log n)$ vertices, which are answered with precomputed tables over all small tree shapes, a [Four Russians](/four-russians-method/) argument. This gives $O(n)$ preprocessing and $O(1)$ query, the result of Bender and Farach-Colton.
- **Long-path decomposition for depth DP.** The same decomposition merges depth-indexed arrays of subtrees in $O(n)$ total, by inheriting the array of the long child, much as [DSU on tree](/dsu-on-tree/) inherits the data of the heavy child.
- **Heavy-light instead of long paths.** [Heavy-light decomposition](/heavy-light-decomposition/) chooses children by size, not height, and gives $O(\log n)$ level ancestor queries in $O(n)$ space.

## When to use it

Use it when there are very many $k$-th ancestor or level ancestor queries on a large static tree and $O(1)$ per query matters, for example inside another algorithm that calls them in an inner loop. If $O(\log n)$ per query is enough, plain binary lifting is shorter. If the queries are offline, a DFS that keeps the current root path in an array answers each in $O(1)$ with no preprocessing beyond the walk.

## Pitfalls

- **Choosing the long child by size.** The bound needs the child with the largest height; with the largest subtree, a path may be short while the subtree is wide, and line L11 can fall off the top of the ladder.
- **Forgetting the extension.** Without the ancestors $A$, the ladder of $u$ may stop below depth $d$.
- **Off-by-one in heights.** Here $h$ counts vertices, so a leaf has height 1 and a path of $k$ vertices is extended by $k$; with heights counted in edges the inequalities shift by one.
- **Jumping too far.** The jump is $2^{\lfloor \lg k \rfloor}$, not the next power of two above $k$, which can overshoot the root.
- **Recursion.** Computing heights by a recursive DFS overflows the Python stack on a path of $10^5$ vertices; the reverse BFS order of line L2 does not.

## Implementations

## History

Level ancestors were first solved with $O(n)$ preprocessing and $O(1)$ query by Berkman and Vishkin, and Dietz studied them in trees that grow by adding leaves (1991). Bender and Farach-Colton (2004) gave the simple route presented here: the table, jump-pointer and ladder algorithms, their combination, and the macro-micro refinement to linear preprocessing. The long-path decomposition has since become a standard tool in competitive programming as well, where it is used for depth-indexed dynamic programming on trees.

## References
