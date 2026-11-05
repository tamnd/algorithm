---
tag: KYP442
kind: technique
slug: subtree-sizes
name: Subtree sizes
area: graphs/tree-algorithms
level: intro
summary: Computing the number of nodes in the subtree of every vertex of a rooted tree with one depth-first traversal.
prereqs: [rooted-tree, postorder-traversal]
see_also: [tree-dynamic-programming, centroid, heavy-light-decomposition, euler-tour-subtree-queries, dsu-on-tree, order-statistic-tree, rerooting-technique, tree-rooting]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 14, Tree algorithms, Section 14.1 (Tree traversal, dynamic programming that counts the nodes of each subtree), and Chapter 18, Section 18.2 (Subtrees and paths, the tree traversal array)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 17.1 (Dynamic order statistics), the size attribute x.size = x.left.size + x.right.size + 1 and its upkeep
  - paper: doi:10.1016/0022-0000(83)90006-5
    title: Daniel D. Sleator and Robert E. Tarjan, A data structure for dynamic trees, Journal of Computer and System Sciences 26(3), 362 to 391 (1983)
    locator: the partition of the tree edges into heavy and light edges by subtree size, and the bound on the number of light edges on a path
---

The subtree-sizes technique computes, for every vertex $v$ of a [rooted tree](/rooted-tree/), the number $s(v)$ of vertices in the subtree of $v$, in one bottom-up pass. It uses the recurrence $s(v) = 1 + \sum_{c} s(c)$ over the children $c$ of $v$, evaluated in [postorder](/postorder-traversal/) or in any order that puts each vertex after its children. It takes $\Theta(n)$ time, and the sizes it gives are the input of many tree methods: the [centroid](/centroid/), [heavy-light decomposition](/heavy-light-decomposition/), [Euler tour subtree queries](/euler-tour-subtree-queries/), [DSU on tree](/dsu-on-tree/) and edge-counting arguments.

## In plain words

Each person in a family tree wants to know how many people are in their own branch: themselves plus all their descendants. A person cannot count their branch until their children have counted theirs. So you start at the people with no children, who each count one. Then each person adds one to the counts of their children. The counts flow upward, and at the top the count is the whole family.

The only care is the order. Every child must be done before its parent. A depth-first walk that handles a node when it leaves it gives this order, and so does a list of the nodes from the bottom level up.

## When it applies

- The tree is rooted, or can be rooted at any vertex, and each vertex needs a quantity of its whole subtree: a count, a sum of weights, a maximum, a parity.
- An argument counts pairs of vertices on the two sides of an edge. Removing the edge from $v$ to its parent splits the tree into $s(v)$ and $n - s(v)$ vertices.
- A method wants to split a tree in a balanced way, or to prefer a largest child.
- A data structure must answer "how many keys are below this node" or "what is the $k$-th key", as in an [order-statistic tree](/order-statistic-tree/).

The tree may be weighted or not. For a vertex-weighted tree, replace the count by the sum of the weights. Edge weights do not enter the sizes.

## The template

The input is a rooted tree with the vertices $0, \ldots, n-1$, given by a parent array $p$ with $p(r) = -1$, and a list $\mathit{order}$ of all vertices in which each vertex comes before its children. A preorder, a BFS order, or the order $0, 1, \ldots, n-1$ when each parent has a smaller number than its children, all qualify.

```pseudo id=main
SUBTREE-AGGREGATE(p, order)
L1  for each vertex v do
L2      a[v] ← INIT(v)                         ▷ subtree sizes: INIT(v) = 1
L3  for v in order, from the last to the first do
L4      if p[v] ≠ −1 then
L5          a[p[v]] ← COMBINE(a[p[v]], a[v])   ▷ subtree sizes: COMBINE(x, y) = x + y
L6  return a
```

The holes are INIT, the value of a vertex alone, and COMBINE, an associative and commutative way to merge a child's value into its parent's. With INIT$= 1$ and COMBINE$=+$, the result is $a[v] = s(v)$.

**Why it is right.** Read $\mathit{order}$ backwards. Each descendant $u \ne v$ of $v$ comes after $v$ in $\mathit{order}$, because its parent does and by induction on the depth. So when line L3 reaches $v$, every child $c$ of $v$ has already passed line L5 and has already received all its own children. By strong induction on the height of $v$: when $v$ is read at line L3, $a[v]$ equals $\mathrm{INIT}(v)$ combined with $a[c]$ for each child $c$, and each $a[c]$ is complete. So for sizes, $a[v] = 1 + \sum_c s(c) = s(v)$ at that moment, and $a[v]$ never changes afterwards, because only the children of $v$ write to it, and they all come before $v$ in the backward scan.

**Cost.** Lines L1 and L2 take $\Theta(n)$ time, and the loop of line L3 runs $n$ times with $O(1)$ work, if INIT and COMBINE take $O(1)$. The extra space is the array $a$. Without a ready order, one [preorder traversal](/preorder-traversal/) with an explicit stack builds it in $\Theta(n)$ time, or the sizes can be summed at the pop step of a [postorder traversal](/postorder-traversal/). Both avoid recursion, which matters on a path of $10^5$ vertices.

### Facts about the sizes

- $s(r) = n$, $s(v) = 1$ exactly when $v$ is a leaf, and $s(v) > s(c)$ for each child $c$.
- $\sum_v s(v) = \sum_v (d(v) + 1) = n + \sum_v d(v)$, where $d(v)$ is the depth: each vertex $u$ is counted once in the size of each of its $d(u) + 1$ ancestors.
- In preorder, the subtree of $v$ is the block of positions $\mathrm{tin}(v)$ to $\mathrm{tin}(v) + s(v) - 1$, where $\mathrm{tin}(v)$ is the position of $v$.
- **Light edges.** Call a child $c$ of $v$ *light* if $2 s(c) \le s(v)$. Along each path from the root down, there are at most $\lfloor \log_2 n \rfloor$ light children, since the size at least halves at each one and stays at least 1. This is the bound behind [heavy-light decomposition](/heavy-light-decomposition/) and [DSU on tree](/dsu-on-tree/).

### Example

Take the tree on $\{0, \ldots, 7\}$ rooted at $0$ with $p = [-1, 0, 0, 1, 1, 2, 4, 4]$. The order $0, 1, \ldots, 7$ puts each parent first.

| $v$ read at L3 | change | $a$ after the step |
|---|---|---|
| start | all 1 | 1 1 1 1 1 1 1 1 |
| 7 | $a[4] = 2$ | 1 1 1 1 2 1 1 1 |
| 6 | $a[4] = 3$ | 1 1 1 1 3 1 1 1 |
| 5 | $a[2] = 2$ | 1 1 2 1 3 1 1 1 |
| 4 | $a[1] = 4$ | 1 4 2 1 3 1 1 1 |
| 3 | $a[1] = 5$ | 1 5 2 1 3 1 1 1 |
| 2 | $a[0] = 3$ | 3 5 2 1 3 1 1 1 |
| 1 | $a[0] = 8$ | 8 5 2 1 3 1 1 1 |
| 0 | none (root) | 8 5 2 1 3 1 1 1 |

The sizes are $s = [8, 5, 2, 1, 3, 1, 1, 1]$. Their sum is $22$, and the depths are $[0, 1, 1, 2, 2, 2, 3, 3]$ with sum $14$, so $22 = 8 + 14$ as the second fact says.

The small cases: the single vertex has $s = [1]$. The path $0, 1, \ldots, n-1$ rooted at $0$ has $s(v) = n - v$. The star rooted at its centre has $s = [n, 1, \ldots, 1]$; rooted at a leaf, the centre has size $n - 1$.

## Classic examples

- **Centroid.** A vertex $v$ is a [centroid](/centroid/) when $\max(n - s(v), \max_c s(c)) \le n/2$. In the example, the largest parts after removing $0, 1, 4$ are $5, 3, 5$, so $1$ is the centroid. One pass of sizes finds it in $O(n)$ time, and [centroid decomposition](/centroid-decomposition/) repeats this on the parts.
- **Sum of all distances.** The edge from $v$ to its parent lies on the paths of exactly $s(v)(n - s(v))$ pairs of vertices. So the sum of the distances over all unordered pairs, the Wiener index, is $\sum_{v \ne r} s(v)(n - s(v))$. In the example this is $15 + 12 + 7 + 15 + 7 + 7 + 7 = 70$.
- **Heavy-light decomposition.** The heavy child of $v$ is a child of largest size. By the light-edge fact, each root path meets $O(\log n)$ heavy paths, which gives $O(\log^2 n)$ [path queries](/tree-path-queries/) with a segment tree.
- **Euler tour subtree queries.** With $\mathrm{tin}$ and $s$, a subtree is an interval of the preorder, so a [Fenwick tree](/fenwick-tree/) answers subtree sums, as on [Euler tour subtree queries](/euler-tour-subtree-queries/).
- **Small to large.** [DSU on tree](/dsu-on-tree/) keeps the data of the heavy child and merges the light children into it, $O(n \log n)$ moves in all.
- **Order statistics.** The [order-statistic tree](/order-statistic-tree/) stores $s(v)$ at each node of a balanced search tree and keeps it up to date in rotations, to find the $k$-th key in $O(\log n)$ time.

## Variations

- **Weighted sizes.** INIT$(v) = w(v)$ gives the weight of each subtree.
- **Other monoids.** COMBINE $= \max$ with INIT$(v) = \mathit{key}(v)$ gives the largest key in each subtree. With INIT$(v) = 0$ and COMBINE$(x, y) = \max(x, y + 1)$ it gives the height of each vertex.
- **All roots.** The size of the side of $u$ when the tree is rooted at a neighbour $v$ is $s(u)$ if $u$ is a child of $v$, and $n - s(v)$ if $u$ is the parent of $v$. This is the first step of the [rerooting technique](/rerooting-technique/).
- **Dynamic trees.** When edges are added and removed, the sizes are kept in a [link-cut tree](/link-cut-tree/) or an [Euler tour tree](/euler-tour-tree/), with $O(\log n)$ time per change.

## Pitfalls

- **Wrong order.** Scanning a preorder or BFS order from the front adds a child to its parent before the child has received its own children. The scan of line L3 must go from the last vertex to the first, or the order must put children first.
- **Deep recursion.** The recursive form $s(v) = 1 + \sum s(c)$ needs a call stack as deep as the tree. On a path of $10^5$ vertices this overflows in Python. Use the backward scan or an explicit stack.
- **Unrooted input.** On an edge list, the parent of each vertex must be fixed first. Treating each neighbour as a child counts the parent too and loops.
- **Off by one.** The size includes the vertex itself. Forgetting INIT$(v) = 1$ gives the number of proper descendants, $s(v) - 1$.

## Exercises

1. Prove that a tree has one centroid or two adjacent centroids, using only the sizes $s$ for a root at one centroid.
2. Give an $O(n)$ algorithm for the sum of the distances from each vertex to all others, for every vertex at once. (Hint: compute it for the root, then move the root along an edge and use $s$.)
3. In a tree with $n$ vertices, count in $O(n)$ time the pairs of vertices whose path has even length.
4. Show that the bound of $\lfloor \log_2 n \rfloor$ light children on a root path is tight: in a perfect binary tree with $n = 2^{k+1} - 1$ vertices, every child is light, and each path from the root to a leaf has $k$ of them.

## References
