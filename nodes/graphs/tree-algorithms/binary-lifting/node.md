---
tag: BSW47R
kind: technique
slug: binary-lifting
name: Binary lifting
aliases:
- jump pointers
- doubling on trees
area: graphs/tree-algorithms
level: core
summary: Precompute 2^k-th ancestors so any ancestor is reached in O(log n) jumps.
prereqs: [rooted-tree, depth-first-search]
see_also: [lca-binary-lifting, lowest-common-ancestor, level-ancestor-problem, ladder-decomposition, pointer-jumping, sparse-table, functional-graph, second-best-mst]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 18, Tree queries, Section 18.1 (Finding ancestors) and Section 18.3 (Lowest common ancestor, the first method)
  - url: https://cp-algorithms.com/graph/lca_binary_lifting.html
    title: cp-algorithms, Lowest Common Ancestor, Binary Lifting
    locator: sections Algorithm and Implementation (the table up[v][j] and the query from the deeper vertex)
  - paper: doi:10.1016/j.tcs.2003.05.002
    title: "Michael A. Bender and Martin Farach-Colton, The level ancestor problem simplified, Theoretical Computer Science 321(1) (2004), 5-12"
    locator: the jump-pointer algorithm (O(n log n) preprocessing, O(log n) query) and its use with ladders
---

Binary lifting is a technique for [rooted trees](/rooted-tree/): for each vertex $v$ and each $k$ it stores $up[k][v]$, the ancestor of $v$ at distance $2^k$. The table has $n \lceil \lg n \rceil$ entries and takes $O(n \log n)$ time to build. Then the ancestor of $v$ at any distance $d$ is found in $O(\log n)$ jumps, one for each one bit of $d$. The same table carries an aggregate of an associative operation along each jump, and it supports a binary search over the ancestors of a vertex. Its best-known use is the [lowest common ancestor by binary lifting](/lca-binary-lifting/).

## In plain words

To go up a tall family tree one parent at a time is slow. Binary lifting prepares shortcuts. For each person it writes down the parent, the grandparent, the ancestor four steps up, eight steps up, sixteen steps up, and so on, each time twice as far. Each new row is quick to fill: eight steps up from you is four steps up from the person who is four steps up from you.

To go up thirteen steps, write thirteen as eight plus four plus one. Take the eight-step shortcut, then the four-step one from where you land, then the one-step one. Any distance is a sum of a few such pieces, so a few jumps reach any ancestor. To find the highest ancestor that still has some property, try the long jumps first and keep each jump that does not go too far.

## When it applies

- **A static rooted tree, or any function from a set to itself.** Each vertex has one parent (one successor). The tree does not change between queries. The same table works on a [functional graph](/functional-graph/), where the "ancestor at distance $d$" is the $d$-th successor.
- **The queries ask to move up by a given distance.** For example "the ancestor of $v$ at depth $h$" (the [level ancestor problem](/level-ancestor-problem/)), or "bring two vertices to the same depth" in the [LCA](/lowest-common-ancestor/) query.
- **The queries ask for an aggregate on a vertical path.** The aggregate is an associative operation $\oplus$, such as the maximum edge weight on the path to an ancestor. This is how [second-best MST](/second-best-mst/) and [MST verification](/mst-verification/) find the heaviest edge on a tree path.
- **The queries ask for the highest (or lowest) ancestor that meets a monotone condition.** A condition is monotone on the path from $v$ to the root if, once it fails, it stays failed further up. Then the long-jumps-first search finds the boundary in $O(\log n)$ steps.
- **Memory of $n \lg n$ words is acceptable.** If it is not, see the variations.

## The template

The input is a rooted tree on the vertices $0, \ldots, n-1$, given as a parent array: $p(v)$ is the parent of $v$, and $p(r) = r$ for the root $r$. The tree may be weighted: $w(v)$ is the weight of the edge from $v$ to $p(v)$, in a set with an associative operation $\oplus$. Let $K = \max(1, \lceil \lg n \rceil)$, so that $2^K > n - 1 \ge$ each depth.

```pseudo id=main
BUILD(p, w)                                  ▷ hole: the operation ⊕ and the weights w
L1  for each vertex v do
L2      up[0][v] ← p(v);  agg[0][v] ← w(v)    ▷ the root points to itself
L3  for k ← 1 to K − 1 do                     ▷ level k − 1 is complete here
L4      for each vertex v do
L5          up[k][v] ← up[k − 1][up[k − 1][v]]
L6          agg[k][v] ← agg[k − 1][v] ⊕ agg[k − 1][up[k − 1][v]]

JUMP(v, d)                                    ▷ 0 ≤ d ≤ depth(v)
L7  acc ← the identity of ⊕
L8  for k ← 0 to K − 1 do
L9      if bit k of d is 1 then
L10         acc ← acc ⊕ agg[k][v];  v ← up[k][v]
L11 return (v, acc)

CLIMB(v, P)                                   ▷ hole: a condition P, false on a prefix of the path from v up
L12 for k ← K − 1 down to 0 do
L13     if not P(up[k][v]) then v ← up[k][v]
L14 return v                                  ▷ the highest vertex on the path with P false, if P(v) is false
```

The holes are the operation $\oplus$ with its weights (leave them out when only ancestors are needed) and the condition $P$ of CLIMB.

Lines L1 and L2 fill level 0 from the parent array. Lines L3 to L6 fill level $k$ from level $k - 1$ by two jumps of length $2^{k-1}$. The outer loop runs over $k$, so the full level $k - 1$ exists before level $k$ starts, and the order of the vertices does not matter. JUMP reads the bits of $d$ from the lowest; each set bit $k$ moves $v$ up by $2^k$. CLIMB tries the long jumps first and takes a jump only if it lands on a vertex where $P$ is still false.

**Why it works.** By induction on $k$, $up[k][v]$ is the ancestor of $v$ at distance $2^k$ when $2^k \le depth(v)$, and the root otherwise. Level 0 is the parent. For $k \ge 1$, a jump of $2^{k-1}$ followed by a jump of $2^{k-1}$ is a jump of $2^k$; when the first or second jump passes the root, the root's self-loop keeps the result at the root. In the same way, when $2^k \le depth(v)$, $agg[k][v]$ is the $\oplus$-product of the weights of the $2^k$ edges on the path up from $v$, in order from the bottom. JUMP is correct because $d = \sum_{k : \text{bit } k = 1} 2^k$: after the loop has handled bits $0, \ldots, k$, $v$ has moved up by $d \bmod 2^{k+1}$ and $acc$ holds the product of the weights of those edges. Since $d \le depth(v)$, no jump passes the root. Here $\oplus$ need not be commutative, because the pieces are taken from the bottom up.

For CLIMB, assume that $P(v)$ is false and that $P$ is false on a prefix of the path from $v$ to the root and true above it. Let $u$ be the highest vertex with $P(u)$ false, and let $R$ be the distance from the current vertex $x$ to $u$. At the start $x = v$ and $R = depth(v) - depth(u) < 2^K$. Before the step for $k$, $P(x)$ is false and $R < 2^{k+1}$. If $R \ge 2^k$, then $up[k][x]$ lies on the path at distance $R - 2^k$ below $u$ or at $u$, so $P$ is false there and line L13 jumps; the new $R$ is less than $2^k$. If $R < 2^k$, then $up[k][x]$ is a strict ancestor of $u$ (or the root, which is then also a strict ancestor of $u$ unless $u$ is the root and the jump lands on $u$), so either $P$ is true there and $x$ stays, or the jump lands on $u$ and $R$ becomes 0. In each case $R < 2^k$ after the step. After the step for $k = 0$, $R = 0$, so CLIMB returns $u$.

### Cost

BUILD fills $nK$ cells of each table with $O(1)$ work each, so it takes $\Theta(n \log n)$ time and $\Theta(n \log n)$ words, when $\oplus$ costs $O(1)$. JUMP and CLIMB each make $K = O(\log n)$ steps. In the word RAM a JUMP can skip the zero bits of $d$, so it makes one jump for each one bit of $d$.

## Classic examples

The examples use this tree on the vertices $0, \ldots, 11$, rooted at 0, with the parent array $p = [0, 0, 1, 2, 3, 4, 2, 6, 0, 8, 3, 7]$ (the root points to itself). So $n = 12$ and $K = 4$.

| $k$ | $up[k][0..11]$ |
|---|---|
| 0 | 0, 0, 1, 2, 3, 4, 2, 6, 0, 8, 3, 7 |
| 1 | 0, 0, 0, 1, 2, 3, 1, 2, 0, 0, 2, 6 |
| 2 | 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1 |
| 3 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 |

The ancestor of 5 at distance 3 is JUMP(5, 3): $3 = 2 + 1$, so $5 \to up[0][5] = 4 \to up[1][4] = 2$. The ancestor of 11 at distance 5: $5 = 4 + 1$, so $11 \to 7 \to up[2][7] = 0$, the root, at depth $5 - 5 = 0$.

Three small shapes:

- **One vertex.** $K = 1$ and $up[0][0] = 0$. The only valid JUMP has $d = 0$.
- **A path** $0 - 1 - \cdots - (n-1)$ rooted at 0. Then $up[k][v] = \max(v - 2^k, 0)$, and JUMP$(v, d) = v - d$. This is the deepest tree, and it is the case where $K$ must reach $\lceil \lg n \rceil$.
- **A star** with center 0 and leaves $1, \ldots, n-1$. Each row is the same: $up[k][v] = 0$ for all $k$ and $v$. Here the table wastes memory, since the depth is 1.

Uses, from simple to hard:

1. **[Level ancestor](/level-ancestor-problem/).** The ancestor of $v$ at depth $h$ is JUMP$(v, depth(v) - h)$, in $O(\log n)$ time.
2. **[LCA by binary lifting](/lca-binary-lifting/).** Lift the deeper vertex to the depth of the other with JUMP. Then lift both with CLIMB, where $P(x)$ is "$x$ is an ancestor of the other vertex too", in the form "the two jump targets are equal".
3. **Path maximum.** With $\oplus = \max$ and edge weights, the maximum weight on the path from $u$ to $v$ is the maximum of two JUMP aggregates, from $u$ and from $v$ up to their LCA. [Second-best MST](/second-best-mst/) uses it to find the heaviest edge on the cycle that a new edge closes, and [MST verification](/mst-verification/) uses it to compare each non-tree edge with that cycle.
4. **The $k$-th successor in a [functional graph](/functional-graph/).** Each vertex has one outgoing edge; the same doubling table gives the vertex after $d$ steps, for $d$ up to $2^K - 1$, even with cycles.
5. **First ancestor with a large value.** If each vertex has a value that does not decrease from a vertex to its parent, the highest ancestor with value at most $x$ is CLIMB with $P(u) = (value(u) > x)$.

## Variations

- **Layout $up[v][k]$.** Store the $K$ jumps of a vertex together. JUMP then reads one short row, which is better for the cache when $n$ is large.
- **Build in parent-first order.** With the loop over vertices outside and the loop over $k$ inside, each vertex must come after its ancestors, for example in BFS or DFS preorder. This lets the table grow as leaves are added to the tree: a new leaf fills its own row in $O(\log n)$ time.
- **Jump pointers with ladders.** Bender and Farach-Colton combine jump pointers with a long-path (ladder) decomposition: one jump of at least half the remaining distance, then one ladder step. This gives $O(1)$ query time, and with a micro-tree trick, $O(n)$ preprocessing. See [ladder decomposition](/ladder-decomposition/).
- **Skew-binary jump pointers.** Each vertex keeps only its parent and one jump pointer, chosen so that a query takes $O(\log n)$ steps with $O(n)$ memory. This uses the structure of skew-binary numbers, as in [skew-binary random access lists](/skew-binary-random-access-list/).
- **[Pointer jumping](/pointer-jumping/).** The parallel form: each processor replaces its pointer by its pointer's pointer, $\lceil \lg n \rceil$ times. It is the base of [list ranking](/list-ranking/).
- **[Sparse table](/sparse-table/).** The same doubling on an array instead of a tree: $ST[k][i]$ covers $2^k$ items from $i$.

## Pitfalls

- **The root's parent is $-1$.** If $up[0][r] = -1$, line L5 reads $up[k-1][-1]$. In Python this is the last vertex, not an error, and the answers become wrong without a warning. Set $p(r) = r$, as in line L2.
- **Too few levels.** With $K = \lfloor \lg n \rfloor$ instead of $\lceil \lg n \rceil$, a path with $n = 2^j + 1$ vertices has a vertex at depth $2^j$, and the jump of $2^j$ is missing. Take $K$ with $2^K > n - 1$, or with $2^K$ more than the maximum depth.
- **Wrong loop order.** If the vertex loop is outside and the $k$ loop inside, line L5 reads $up[k-1][x]$ of an ancestor $x$ whose row may not be filled yet. Either keep $k$ outside, as in lines L3 and L4, or visit vertices in parent-first order.
- **A distance larger than the depth.** JUMP$(v, d)$ with $d > depth(v)$ returns the root, not an error, and the aggregate then counts the root's self-loop weight. Check $d \le depth(v)$ first, or make $w(r)$ the identity.
- **A non-commutative operation.** In line L6, the bottom part comes first. Swapping the two operands gives the product in the wrong order for an operation such as matrix product or string concatenation.
- **Deep recursion.** Computing depths and parents with a recursive DFS fails on a path of $10^5$ vertices in Python. Use an iterative DFS or a BFS.

## Exercises

1. Show that BUILD fills the same table when the loop of line L3 and the loop of line L4 are swapped, if the vertex loop visits the vertices in BFS order from the root.
2. Given values on the vertices that increase from each vertex to its parent, find for a query $(v, x)$ the deepest ancestor of $v$ with value at least $x$ in $O(\log n)$ time.
3. Extend JUMP so that it returns the sum and the maximum of the edge weights on the path at the same time, with one table for each.
4. A tree grows by adding leaves one at a time. Keep the table so that each new leaf costs $O(\log n)$ time, and answer LCA queries between the additions.

## References
