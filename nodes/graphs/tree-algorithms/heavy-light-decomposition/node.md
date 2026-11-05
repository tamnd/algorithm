---
tag: NVB7AP
kind: technique
slug: heavy-light-decomposition
name: Heavy-light decomposition
aliases:
- HLD
area: graphs/tree-algorithms
level: advanced
summary: Split a tree into heavy paths so any root path crosses O(log n) light edges.
prereqs: [rooted-tree, subtree-sizes, segment-tree, euler-tour-technique]
see_also: [tree-path-queries, lowest-common-ancestor, link-cut-tree, euler-tour-subtree-queries, dsu-on-tree, centroid-decomposition, lazy-propagation, dynamic-tree-path-queries]
sources:
  - paper: doi:10.1016/0022-0000(83)90006-5
    title: "Daniel D. Sleator and Robert E. Tarjan, A data structure for dynamic trees, Journal of Computer and System Sciences 26(3) (1983), 362-391"
    locator: the partition of a tree into heavy and light edges, and the bound of lg n light edges on any path to the root
  - paper: "Dov Harel and Robert E. Tarjan, Fast algorithms for finding nearest common ancestors, SIAM Journal on Computing 13(2) (1984), 338-355"
    locator: the use of a heavy path decomposition of the tree in the linear-time nearest common ancestor algorithm
  - url: https://cp-algorithms.com/graph/hld.html
    title: cp-algorithms, Heavy-light decomposition
    locator: sections Description, Proof of correctness, Applications (sum and maximum on a path, assignment on a path) and Implementation
---

Heavy-light decomposition (HLD) splits a [rooted tree](/rooted-tree/) into vertex-disjoint paths, the *heavy paths*, such that the path from any vertex to the root meets at most $\lfloor \log_2 n \rfloor + 1$ of them. For each vertex, the edge to a child with the largest subtree is *heavy*, and the other child edges are *light*; going up a light edge at least doubles the subtree size. If the vertices are numbered so that each heavy path is a contiguous range, any path $u \to v$ in the tree is the union of $O(\log n)$ ranges, so a [segment tree](/segment-tree/) over that numbering answers path sums, maxima and updates in $O(\log^2 n)$ time. The same numbering is an [Euler tour](/euler-tour-technique/) order, so subtree queries work on the same array. Sleator and Tarjan introduced the heavy and light edges for their dynamic trees.

## In plain words

A big tree has many paths, and some are very long, so walking a path step by step is slow. HLD cuts the tree into long straight chains in a smart way. At each point, the line to the biggest branch stays in the same chain; the lines to the smaller branches start new chains.

Now go from any point up to the top. Each time you switch to a new chain, you have come out of a smaller branch, so the part of the tree below you at least doubles. That can happen only a few times. So any path in the tree is made of a few pieces of chains. Lay all chains one after the other in one long list, and each piece becomes a stretch of that list, which known tools handle fast.

## When it applies

- The tree is static: its shape does not change. The values on the vertices or edges can change.
- The queries are about paths $u \to v$: sum, minimum, maximum, or any associative aggregate, with point or path updates. The tree is rooted at a fixed vertex, any one will do; the vertices are numbered $0, \ldots, n-1$.
- Edge values are handled by storing the value of the edge from $v$ to its parent at $v$, and leaving out the LCA on each path.
- It is not needed for path queries with no updates and an invertible aggregate (sum, xor): prefix values from the root and the [LCA](/lowest-common-ancestor/) answer those in $O(1)$ after the LCA. It is not enough when edges are added and removed; then [link-cut trees](/link-cut-tree/) are the tool.

## The template

```pseudo id=main
BUILD(T, r)
L1  B ← BFS order from r, with parent p(v) and depth d(v)
L2  for v in B in reverse order do size[v] ← 1 + Σ size[c] over the children c of v
L3  heavy[v] ← a child of v with the largest size, or NIL if v is a leaf
L4  t ← 0;  S ← [r]                                   ▷ stack of heads of heavy paths
L5  while S is not empty do
L6      h ← pop S;  v ← h
L7      while v ≠ NIL do                               ▷ walk down the heavy path of h
L8          head[v] ← h;  pos[v] ← t;  t ← t + 1
L9          push the light children of v on S
L10         v ← heavy[v]

PATH-QUERY(u, v)                                       ▷ hole: the range query Q and the operation ⊕
L11 res ← the identity of ⊕
L12 while head[u] ≠ head[v] do
L13     if d(head[u]) < d(head[v]) then swap u and v
L14     res ← res ⊕ Q(pos[head[u]], pos[u]);  u ← p(head[u])
L15 res ← res ⊕ Q(min(pos[u], pos[v]), max(pos[u], pos[v]))
L16 return res                                         ▷ the shallower of u and v is now lca(u, v)
```

The holes are the range structure $Q$ over the array $A[pos[v]] = $ value of $v$, usually a segment tree, and its operation $\oplus$. A path update is the same loop with a range update in place of $Q$. For a non-commutative $\oplus$, collect the pieces from the $u$ side and the $v$ side separately and join them in path order.

Lines L1 to L3 compute the sizes and heavy children with no recursion. Lines L4 to L10 walk each heavy path from its head and number its vertices consecutively. Pushing the light children and popping them later is a depth-first order that visits the heavy child first, so each heavy path is a range of $pos$, and each subtree is also a range: $\mathrm{sub}(v) = [pos[v], pos[v] + size[v] - 1]$.

**Why paths are few.** If $c$ is a light child of $v$, then $size[v] \ge size[c] + size[heavy[v]] \ge 2\, size[c]$. On the path from a vertex $x$ to the root, the subtree size at least doubles at each light edge and is at most $n$, so there are at most $\lfloor \log_2 n \rfloor$ light edges, and the path meets at most $\lfloor \log_2 n \rfloor + 1$ heavy paths.

**Why PATH-QUERY is right.** Let $w = \mathrm{lca}(u, v)$, and suppose $head[u] \ne head[v]$ and $d(head[u]) \ge d(head[v])$ after line L13. Then $head[u]$ is a strict descendant of $w$. Otherwise $head[u]$ is an ancestor of $w$, the heavy path from $head[u]$ down to $u$ passes through $w$, and $head[w] = head[u]$. Now $v$ is a descendant of $w$: if $head[v]$ is strictly below $w$, then $d(head[v]) > d(w) \ge d(head[u])$, against line L13; if not, the heavy path of $v$ also passes through $w$ and $head[v] = head[w] = head[u]$, against the loop test. So the piece $head[u], \ldots, u$ lies on the $u$ side of the path, strictly below $w$; line L14 takes it and moves $u$ to the parent of the head, which is still a descendant of $w$. No vertex of the $u$-$v$ path is skipped or taken twice. When the two are on the same heavy path, the rest of the path is the range between them, which line L15 takes, and the shallower one is $w$. Each iteration of line L14 crosses a light edge on the path from $u$ or $v$ to the root, so there are at most $2 \lfloor \log_2 n \rfloor$ of them.

### Cost

BUILD takes $O(n)$ time and memory. PATH-QUERY makes $O(\log n)$ range queries, each $O(\log n)$ in a segment tree, so $O(\log^2 n)$ per query or update, in the worst case. With a [sparse table](/sparse-table/) and no updates, each range query is $O(1)$ and a path query $O(\log n)$. The LCA alone, by lines L12 to L16 with no $Q$, costs $O(\log n)$ after $O(n)$ preprocessing.

## Classic examples

The examples use the tree on $0, \ldots, 11$ rooted at 0, with the parent array $[-, 0, 1, 2, 3, 4, 2, 6, 0, 8, 3, 7]$, children ordered by label, and the vertex values $a = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8]$:

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

The sizes are $[12, 9, 8, 4, 2, 1, 3, 2, 2, 1, 1, 1]$, so the heavy children are $1, 2, 3, 4, 5$ along the left spine, $7$ under 6, $11$ under 7 and $9$ under 8. The heavy paths are $0, 1, 2, 3, 4, 5$ (head 0); $10$ (head 10); $6, 7, 11$ (head 6); and $8, 9$ (head 8). BUILD gives

| $v$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $head[v]$ | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 6 | 8 | 8 | 10 | 6 |
| $pos[v]$ | 0 | 1 | 2 | 3 | 4 | 5 | 7 | 8 | 10 | 11 | 6 | 9 |

and the array $A = [3, 1, 4, 1, 5, 9, 5, 2, 6, 8, 5, 3]$.

**1. Path sum.** The path from 5 to 11 is $5, 4, 3, 2, 6, 7, 11$, with sum $9 + 5 + 1 + 4 + 2 + 6 + 8 = 35$. PATH-QUERY: $head[5] = 0$ at depth 0, $head[11] = 6$ at depth 3, so line L14 takes $A[7..9] = 2 + 6 + 8 = 16$ for the vertices 6, 7, 11 and moves to $p(6) = 2$. Now 5 and 2 share the head 0, and line L15 takes $A[2..5] = 4 + 1 + 5 + 9 = 19$. The total is 35, and the LCA is 2. The path from 9 to 10 needs three ranges: $A[6..6] = 5$ for 10, then $A[10..11] = 5 + 3 = 8$ for 8 and 9, then $A[0..3] = 9$ for 0 to 3; the total is 22 and the LCA is 0.

**2. Path maximum with point updates.** Store $A$ in a segment tree for maximum. Changing $a_v$ is one point update at $pos[v]$; a path maximum is PATH-QUERY with $\oplus = \max$. Both take $O(\log^2 n)$. This is the standard solution of the CSES problem Path Queries II and of the maximum-edge-on-a-path queries used in [second-best minimum spanning trees](/second-best-mst/) with updates.

**3. Path assignment.** "Set every value on the path $u \to v$ to $x$" is a range assignment on each of the $O(\log n)$ ranges, with [lazy propagation](/lazy-propagation/).

**4. Subtree and path together.** The subtree of $v$ is the range $[pos[v], pos[v] + size[v] - 1]$: the subtree of 2 is $A[2..9]$, with sum 40. So one segment tree serves both "add $x$ to the subtree of $v$" and "sum on the path $u \to w$", which neither the Euler tour alone nor a plain LCA method can do.

**5. LCA.** Lines L12 to L16 with no range queries find $\mathrm{lca}(u, v)$ in $O(\log n)$ time, with $O(n)$ memory, less than the $O(n \log n)$ of [binary lifting](/lca-binary-lifting/).

## Variations

- **Edge values.** Put the value of the edge $(v, p(v))$ at $pos[v]$, and in line L15 take the range from $\min(pos[u], pos[v]) + 1$, so the LCA's own entry, which belongs to the edge above the LCA, is left out.
- **Heavy by depth: long-path decomposition.** Choosing the child with the deepest subtree instead of the largest gives the long-path decomposition used by [ladder decomposition](/ladder-decomposition/). A path to the root may then cross $\Theta(\sqrt n)$ paths, but each long path is at least as long as the part of the tree below its top.
- **Dynamic trees.** Sleator and Tarjan's [link-cut trees](/link-cut-tree/) keep a heavy-light structure of preferred paths under link and cut, with each path in a splay tree, in $O(\log n)$ amortized time per operation.
- **One segment tree per heavy path.** Building a separate balanced structure for each heavy path, weighted by the sizes of the light subtrees, brings the path query down to $O(\log n)$; this is the idea of biased search trees in the original paper.
- **[DSU on tree](/dsu-on-tree/)** uses the same heavy children to answer offline subtree questions in $O(n \log n)$.

## Pitfalls

- **Recursion.** The usual code uses two recursive DFS passes; on a path of $10^5$ vertices this fails in Python. BFS order for the sizes and an explicit stack of heads, as in lines L1 to L10, avoid it.
- **Comparing the wrong depths.** Line L13 must compare the depths of the heads, not of $u$ and $v$. Comparing $u$ and $v$ can jump past the LCA and give wrong answers.
- **Non-commutative operations.** For a path "string", matrix product or "the first vertex with value above $x$ from $u$ to $v$", the pieces from the $u$ side come in the order up the tree, and those from the $v$ side must be reversed and appended at the end.
- **Edge values at the LCA.** With values on edges, forgetting the $+1$ in line L15 adds the edge above the LCA, which is not on the path.
- **Light children order.** Any order of the light children is correct, but heavy must be visited first, or heavy paths are not contiguous.

## Exercises

1. Show that a path $0 - 1 - \cdots - (n-1)$ rooted at 0 is one heavy path, and that every path query uses one range.
2. Show that a star rooted at its center has $n - 1$ heavy paths, and that every path query uses at most three ranges.
3. For the single-vertex tree, check that BUILD gives $pos[0] = 0$ and that PATH-QUERY$(0, 0)$ returns $a_0$.
4. Build a tree in which some root path crosses exactly $\lfloor \log_2 n \rfloor$ light edges. (Hint: a perfect binary tree.)
5. Prove that the vertices of every subtree get consecutive $pos$ values.
6. Use HLD to support "add $x$ to every vertex on the path $u \to v$" and "sum of the subtree of $w$" in $O(\log^2 n)$ time each.

## References
