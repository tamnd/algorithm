---
tag: T1VPR2
kind: algorithm
slug: lca-binary-lifting
name: LCA by binary lifting
aliases:
- jump-pointer LCA
area: graphs/tree-algorithms
level: core
summary: Precompute 2^k ancestors, then answer each query in O(log n).
solves: [lowest-common-ancestor]
model: word-ram
complexity:
  vars: {n: the number of vertices of the tree}
  time: {build: Θ(n log n), query: O(log n)}
  space: {extra: Θ(n log n)}
properties: {deterministic: true, online: true, recursive: false}
prereqs: [binary-lifting, lowest-common-ancestor, breadth-first-search]
see_also: [euler-tour-lca, tarjan-offline-lca, level-ancestor-problem, heavy-light-decomposition, tree-path-queries, second-best-mst]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 18, Tree queries, Section 18.1 (Finding ancestors) and Section 18.3 (Lowest common ancestor, the first method)
  - url: https://cp-algorithms.com/graph/lca_binary_lifting.html
    title: cp-algorithms, Lowest Common Ancestor, Binary Lifting
    locator: sections Algorithm and Implementation
  - paper: doi:10.1016/j.tcs.2003.05.002
    title: "Michael A. Bender and Martin Farach-Colton, The level ancestor problem simplified, Theoretical Computer Science 321(1) (2004), 5-12"
    locator: the jump-pointer algorithm (O(n log n) preprocessing and O(log n) query)
  - paper: "Dov Harel and Robert E. Tarjan, Fast algorithms for finding nearest common ancestors, SIAM Journal on Computing 13(2) (1984), 338-355"
    locator: the whole paper (O(n) preprocessing and O(1) query time on a RAM)
  - paper: "Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, On finding lowest common ancestors in trees, SIAM Journal on Computing 5(1) (1976), 115-132; first in STOC 1973"
    locator: the statement of the problem and its online and offline versions
---

LCA by binary lifting answers the [lowest common ancestor](/lowest-common-ancestor/) query in a static rooted tree with the jump table of [binary lifting](/binary-lifting/). It stores, for each vertex, its ancestors at distances $1, 2, 4, \ldots$ in $\Theta(n \log n)$ time and memory. A query lifts the deeper vertex to the depth of the other, then lifts both together by the longest jumps that keep them apart, in $O(\log n)$ time. It is short to write, it works online, and the same table gives [level ancestors](/level-ancestor-problem/) and path aggregates, so it is the usual first choice when $O(\log n)$ per query is fast enough.

## In plain words

Two people in a family tree want their closest shared ancestor. First, the person further from the top climbs until both are the same number of generations from the top. If they now stand on the same person, that is the answer.

If not, they climb together, always by the same number of steps, so they stay level. They try a very long climb first. If the long climb would put them on the same person, they might overshoot the closest shared ancestor, so they do not take it. If it leaves them on different people, they take it, because the answer is still above them. Then they try a climb half as long, and so on. At the end they stand just below the answer, on two different children of it, and one more step up reaches it.

## The problem

The input is a tree on the vertices $0, \ldots, n-1$ with $n \ge 1$, given by its $n - 1$ undirected edges, and a root $r$. The tree is rooted at $r$ and unweighted. A query is a pair $(u, v)$ of vertices, and its answer is $\mathrm{lca}(u, v)$, the deepest vertex that is an ancestor of both (a vertex is an ancestor of itself). The queries come online: each answer is due before the next query is read.

## The algorithm

The table $up[k][v]$ is the ancestor of $v$ at distance $2^k$, or the root when $2^k > depth(v)$.

```pseudo id=main
PREPROCESS(T, r)
L1  BFS from r: parent p(v) and depth(v) of each v; p(r) ← r
L2  K ← max(1, ⌈lg n⌉)                          ▷ 2^K > n − 1 ≥ each depth
L3  for each v do up[0][v] ← p(v)
L4  for k ← 1 to K − 1 do for each v do up[k][v] ← up[k − 1][up[k − 1][v]]

LCA(u, v)
L5  if depth(u) < depth(v) then swap u and v
L6  d ← depth(u) − depth(v)
L7  for each k with bit k of d equal to 1 do u ← up[k][u]
L8  if u = v then return u
L9  for k ← K − 1 down to 0 do
L10     if up[k][u] ≠ up[k][v] then u ← up[k][u]; v ← up[k][v]
L11 return up[0][u]
```

Line L1 uses [BFS](/breadth-first-search/), not a recursive DFS, so a path of $10^5$ vertices does not overflow a call stack. Lines L3 and L4 are the build of binary lifting, with the loop over $k$ outside. Lines L5 to L7 lift the deeper vertex by exactly $d$ levels. If it lands on $v$, then $v$ is an ancestor of $u$ and the answer (line L8). Otherwise lines L9 and L10 lift both vertices by the same amount each time, so they stay at equal depth, and take a jump only when its two targets differ. Line L11 returns the common parent.

## Example

The tree has the vertices $0, \ldots, 11$, root 0, and the parent array $p = [0, 0, 1, 2, 3, 4, 2, 6, 0, 8, 3, 7]$. The depths are $[0, 1, 2, 3, 4, 5, 3, 4, 1, 2, 4, 5]$, and $K = 4$.

| $k$ | $up[k][0..11]$ |
|---|---|
| 0 | 0, 0, 1, 2, 3, 4, 2, 6, 0, 8, 3, 7 |
| 1 | 0, 0, 0, 1, 2, 3, 1, 2, 0, 0, 2, 6 |
| 2 | 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1 |
| 3 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 |

The query LCA(5, 11): both have depth 5, so $d = 0$ and line L7 does nothing.

| $k$ | $up[k][u]$ | $up[k][v]$ | action | $(u, v)$ after |
|---|---|---|---|---|
| start | | | | (5, 11) |
| 3 | 0 | 0 | equal, stay | (5, 11) |
| 2 | 1 | 1 | equal, stay | (5, 11) |
| 1 | 3 | 6 | differ, jump | (3, 6) |
| 0 | 2 | 2 | equal, stay | (3, 6) |

Line L11 returns $up[0][3] = 2$. The paths $5, 4, 3, 2$ and $11, 7, 6, 2$ meet at 2 first, so 2 is right.

The query LCA(10, 9): depth 4 and 2, so $d = 2 = 10_2$ and line L7 moves $u = 10$ to $up[1][10] = 2$. Then $u = 2 \ne 9$. For $k = 3, 2, 1$ both targets are 0. For $k = 0$ the targets 1 and 8 differ, so $(u, v) = (1, 8)$. The answer is $up[0][1] = 0$.

The query LCA(7, 2): $d = 2$ lifts 7 to $up[1][7] = 2$, which equals $v$, so line L8 returns 2.

Three small shapes. With one vertex, $K = 1$ and LCA(0, 0) returns 0 at line L8. On a path $0 - 1 - \cdots - (n-1)$ rooted at 0, LCA$(u, v) = \min(u, v)$: line L7 lifts the larger one onto the smaller, and line L8 returns. On a star with center 0 and root 0, two distinct leaves have equal depth 1, all jumps of $k \ge 1$ give 0 and 0, the jump of $k = 0$ gives 0 and 0 as well, and line L11 returns $up[0][u] = 0$.

## Correctness

The table is correct by induction on $k$, as shown on the [binary lifting](/binary-lifting/) page. After line L7, $u$ is the ancestor of the original deeper vertex at the depth of $v$, and the LCA is unchanged. The key invariant of the loop of lines L9 and L10 is: $u \ne v$, $depth(u) = depth(v)$, the LCA is unchanged, and before the step for $k$ the distance from $u$ to the child of the LCA on its path is less than $2^{k+1}$. After $k = 0$ that distance is 0, so $p(u)$ is the LCA. The full proof is in the proof file below.

## Complexity

- **Preprocessing.** The BFS of line L1 takes $\Theta(n)$ time. Lines L3 and L4 fill $nK$ cells, each in $O(1)$ time, with $K = \lceil \lg n \rceil$ for $n \ge 2$. So the time and the memory are $\Theta(n \log n)$ in the word RAM.
- **Query.** Line L7 makes at most $K$ jumps and the loop of line L9 makes exactly $K$ steps. So a query takes $\Theta(\log n)$ time in the worst case, and $O(\log n)$ in each case.
- **Total.** For $q$ queries, $\Theta(n \log n + q \log n)$ time.

For $n = 10^5$, $K = 17$ and the table has $1.7 \times 10^6$ entries.

## Properties

- **Online.** Each query is answered from the table alone, in any order.
- **Static.** The tree must not change. A new leaf can be added in $O(\log n)$ time by filling its row from its parent's row, but a deleted or moved subtree needs a rebuild.
- **Extra uses of the same table.** The $d$-th ancestor (lines L6 and L7 alone), the distance $depth(u) + depth(v) - 2\, depth(\mathrm{lca}(u, v))$, and with a second table the maximum or sum of the edge weights on the path.

## Variants and improvements

- **Lift by depth comparison.** Instead of the bits of $d$ in line L7, run $k$ from $K - 1$ down and jump when $depth(up[k][u]) \ge depth(v)$. Both take $O(\log n)$.
- **Ancestor test by DFS times.** With [discovery and finish times](/discovery-and-finish-times/), $x$ is an ancestor of $y$ if and only if $tin(x) \le tin(y)$ and $tout(y) \le tout(x)$. Then the query lifts only $u$: for $k$ from $K - 1$ down, jump when $up[k][u]$ is not an ancestor of $v$. This removes lines L5 to L8 and is the form of cp-algorithms.
- **Path aggregates.** Keep $agg[k][v]$, the maximum (or sum, or any associative product) of the weights of the $2^k$ edges above $v$. The same two phases return the aggregate on the path $u \to v$.
- **Faster LCA.** The [Euler tour and RMQ](/euler-tour-lca/) method answers in $O(1)$ after $O(n \log n)$ or $O(n)$ preprocessing. [Tarjan's offline LCA](/tarjan-offline-lca/) answers a batch of $q$ queries in $O((n + q)\, \alpha(n))$ time. [Heavy-light decomposition](/heavy-light-decomposition/) answers in $O(\log n)$ with $O(n)$ memory.

## When to use it

Use binary lifting for online LCA queries when $n \log n$ words of memory fit and $O(\log n)$ per query is fast enough, or when the same program also needs $d$-th ancestors or path maxima. Use the Euler tour method when the queries are many and must take $O(1)$. Use Tarjan's offline method when all queries are known in advance. Use heavy-light decomposition when memory is tight or when the path queries also need updates with a [segment tree](/segment-tree/).

## Pitfalls

- **The root's parent set to $-1$.** Then line L4 reads $up[k-1][-1]$, which in Python is the last vertex. Line L1 must set $p(r) = r$.
- **Too few levels.** Line L2 needs $2^K > $ the maximum depth. With $K = \lfloor \lg n \rfloor$, a path of $2^j + 1$ vertices has depth $2^j$ and line L7 cannot lift by it.
- **Jumping when the targets are equal.** If line L10 jumps when $up[k][u] = up[k][v]$, the two vertices can land on a common ancestor above the LCA. The test must be $\ne$, and the answer is the parent in line L11.
- **Skipping line L8.** If $v$ is an ancestor of $u$, then after line L7 $u = v$, and lines L9 to L11 return $p(v)$, which is wrong.
- **A recursive DFS for line L1.** On a path of $10^5$ vertices, Python's recursion limit stops it. Use BFS or an explicit stack.

## Implementations

## History

Aho, Hopcroft and Ullman posed the lowest common ancestor problem in 1973. Harel and Tarjan gave the first method with $O(n)$ preprocessing and $O(1)$ query time in 1984. The jump-pointer table is a standard tool for level ancestor queries, and Bender and Farach-Colton describe it as the "jump pointer algorithm" in their 2004 paper on the level ancestor problem. Its use for LCA queries is a folklore method of programming contests and textbooks for competitive programming.

## References
