---
title: The priority search tree answers three-sided queries exactly in O(log n + k) time with O(n) space
proves: [correctness, termination, complexity]
status: full
---

**Setting.** The points of $P$, $n \ge 1$, are at positions $0, \dots, n - 1$ of the order of $(p_x, p_y, \text{index})$; the key of position $j$ is $\kappa(j) = (p_y, p_x, j)$, and keys are distinct. The tree $T$ is the balanced binary tree over the positions in which a node $v$ covers a block $\beta(v)$, children split it at the middle, and the height is $H = \lceil \log_2 n \rceil$. BUILD stores $\mathrm{pt}(v)$ as described on the page. The query is THREE-SIDED$(x_1, x_2, y_0)$, closed, with $lo$ the first position with $p_x \ge x_1$ and $hi$ the last with $p_x \le x_2$.

**Claim.** (a) BUILD satisfies invariants (1) to (3). (b) THREE-SIDED reports each point with $x_1 \le p_x \le x_2$ and $p_y \le y_0$ exactly once and no other point. (c) It visits at most $4H + 2k + 5$ nodes. (d) The space is $O(n)$ and BUILD takes $O(n \log n)$ time.

**Step 1 (what BUILD stores).** Let $R(v)$ be the set passed to $v$. By induction on depth, $R(v)$ is the set of positions of $\beta(v)$ not stored at a proper ancestor: true at the root with $R = [0, n)$, and line L5 passes to each child the part of $R(v) \setminus \{\mathrm{pt}(v)\}$ in the child's block. So $\mathrm{pt}(v) \in \beta(v)$, and a position $j$ is stored at the first node on the path from the root to the leaf of $j$ at which it has the smallest key in $R$; it is stored at a node because the leaf block $\{j\}$ has $R \subseteq \{j\}$, and if $j$ is still in $R$ there, it is stored there. It is stored only once, since it is removed from $R$ below. This is invariant (1). If $R(v)$ is empty, the children get empty sets, which is (3).

**Step 2 (heap order).** If $w$ is a child of $v$ and $w$ is not empty, then $\mathrm{pt}(w) \in R(w) \subseteq R(v)$ and $\mathrm{pt}(w) \neq \mathrm{pt}(v)$, so $\kappa(\mathrm{pt}(v)) < \kappa(\mathrm{pt}(w))$ by the choice at line L4. This is invariant (2). By induction down the subtree, every point stored in the subtree of $v$ has key at least $\kappa(\mathrm{pt}(v))$, hence $p_y \ge \mathrm{pt}(v)_y$.

**Step 3 (positions and the $x$-range).** The $x$-coordinates do not decrease along the positions, so $x_1 \le p_x \le x_2$ holds exactly for the positions in $[lo, hi]$.

**Step 4 (no false report, no duplicate).** Line L10 reports $\mathrm{pt}(v)$ only if its position is in $[lo, hi]$ and, by line L9, its $y$ is at most $y_0$; by Step 3 the point is in the range. Each node is visited at most once, because the walk is a traversal of a tree from its root, and each point is stored at one node.

**Step 5 (no point is missed).** Let $j$ be a position in $[lo, hi]$ whose point has $p_y \le y_0$, stored at node $u$, and let $v$ be any node on the path from the root to $u$. Then $\beta(v) \ni j$ meets $[lo, hi]$, $v$ is not empty since it is an ancestor of the nonempty node $u$ (invariant (3)), and by Step 2 $\mathrm{pt}(v)_y \le p_y \le y_0$. So neither line L8 nor line L9 skips $v$, and line L11 continues to its children. By induction along the path the walk reaches $u$, and line L10 reports $j$. Steps 4 and 5 prove (b).

**Step 6 (visits).** Call a node *active* if it passes lines L8 and L9. An active node $v$ with $\beta(v) \subseteq [lo, hi]$ has its stored point in $[lo, hi]$ and reports it, so there are at most $k$ such nodes. Any other active node has a block that meets $[lo, hi]$ without lying inside it, so it contains $lo - 1$ and $lo$, or $hi$ and $hi + 1$; at each depth the blocks are disjoint, so there are at most two such nodes per depth, $2(H + 1)$ in all. Every visited node is the root or a child of an active node, so the number of visits is at most $1 + 2(2(H + 1) + k) = 4H + 2k + 5$. Each visit costs $O(1)$ and the two binary searches cost $O(\log n)$, so THREE-SIDED takes $O(\log n + k)$ time. This proves (c).

**Step 7 (space and build).** The tree has at most $2n - 1$ nodes, each storing one position or nothing, so the space is $O(n)$. At each depth the sets $R(v)$ are disjoint subsets of $[0, n)$, and line L4 and line L5 take time linear in $|R(v)|$, so BUILD does $O(n)$ work per depth after the $O(n \log n)$ sort, $O(n \log n)$ in all. This proves (d). $\blacksquare$
