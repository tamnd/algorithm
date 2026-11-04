---
tag: 1C9B9K
kind: theorem
slug: kd-tree-range-query-complexity
name: k-d tree range query complexity
aliases:
- Lee-Wong bound
area: data-structures/spatial-structures
level: advanced
summary: An orthogonal range query on n points in d dimensions visits O(n^(1-1/d) + k) nodes, where k is the output size.
prereqs: [kd-tree, orthogonal-range-searching]
see_also: [kd-tree-range-search, range-tree, range-searching-lower-bound, partition-tree, orthogonal-range-reporting, curse-of-dimensionality, kd-b-tree, quadtree]
sources:
  - paper: doi:10.1007/BF00263763
    title: D. T. Lee and C. K. Wong, Worst-case analysis for region and partial region searches in multidimensional binary search trees and balanced quad trees, Acta Informatica 9(1), 1977
    locator: pages 23 to 29 (the O(k N^(1-1/k)) worst-case bound for region search in a balanced k-d tree, and the matching bound for balanced quad trees)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 5, Orthogonal Range Searching, Section 5.2 Kd-Trees (the O(√n + k) query time in the plane through the count of regions that a vertical line meets, and the O(n^(1-1/d) + k) bound in d dimensions)
  - paper: doi:10.1145/361002.361007
    title: Jon Louis Bentley, Multidimensional binary search trees used for associative searching, Communications of the ACM 18(9), 1975
    locator: the k-d tree and its region search
---

In a balanced [k-d tree](/kd-tree/) on $n$ points in $k \ge 2$ dimensions, an orthogonal range query visits $O(n^{1 - 1/k} + r)$ nodes in the worst case, where $r$ is the number of points it reports; in the plane this is $O(\sqrt n + r)$. The proof counts the nodes whose region meets the boundary of the query box: a hyperplane that is perpendicular to an axis meets only one child region at each level that splits on that axis, so it meets about $2^{t(1 - 1/k)}$ regions at depth $t$. The bound is tight: a query that reports nothing can visit $\Omega(n^{1 - 1/k})$ nodes. Lee and Wong proved it in 1977.

## Statement

Let $P$ be a set of $n$ points in $\mathbb{R}^k$, $k \ge 2$, in which no two points have the same coordinate on any axis. Let $T$ be the k-d tree that BUILD of the [k-d tree](/kd-tree/) page makes on $P$: each node holds one point, a node at depth $t$ splits on axis $t \bmod k$, and its point is the median of its subtree on that axis, with the $\lfloor s/2 \rfloor$ smaller points of a subtree of size $s$ on the left and the other $\lceil s/2 \rceil - 1$ on the right. The region $R(u)$ of a node is a closed box: $R(\text{root}) = \mathbb{R}^k$, and a node $t$ with axis $a$ and point $p$ gives its left child $R(t) \cap \{x_a \le p_a\}$ and its right child $R(t) \cap \{x_a \ge p_a\}$. RANGE-SEARCH visits a child when the query box can meet its side of the split.

**Theorem.** For every closed box $Q = \prod_{i}[\ell_i, h_i]$, RANGE-SEARCH on $T$ visits at most
$$28\,k\, n^{1 - 1/k} + r$$
nodes, where $r = |P \cap Q|$. For $k = 2$ this is $56\sqrt n + r$. Conversely, for every $H \ge 1$ and every such set of $n = 2^H - 1$ points, there is a box $Q$ with $r = 0$ for which the search visits at least $2^{(H-1) - \lceil (H-1)/k \rceil} \ge \tfrac12 \big(\tfrac{n+1}{2}\big)^{1 - 1/k}$ nodes.

## In plain words

A range query looks for all points inside a box. The tree has cut space into smaller and smaller boxes, one per node, and the search opens a node only when its box touches the query box.

Two kinds of node get opened. Some have boxes that lie fully inside the query box; each of these holds a point that the search reports, so there are no more of them than answers. The others have boxes that cross a side of the query box.

So count the boxes that one flat side can cross. On the levels that cut along the side's own direction, the side passes on only one of the two halves. On the other levels it passes on both. In two dimensions this gives about the square root of $n$ boxes, which is far fewer than $n$.

## Proof

**Step 1: the visited nodes.** RANGE-SEARCH visits exactly the nodes $u$ with $R(u) \cap Q \ne \emptyset$. The root region meets $Q$. Let $t$ be visited, with $R(t) = \prod_i [\alpha_i, \beta_i]$ (ends may be infinite) meeting $Q$, axis $a$ and point $p$. Since $p \in R(t)$, $\alpha_a \le p_a \le \beta_a$. The left region $R(t) \cap \{x_a \le p_a\}$ meets $Q$ exactly when $\max(\alpha_a, \ell_a) \le \min(p_a, h_a)$, given the other axes, which already meet. Since $R(t)$ meets $Q$, $\alpha_a \le h_a$ and $\ell_a \le \beta_a$; together with $\alpha_a \le p_a$ and $\ell_a \le h_a$, this holds exactly when $\ell_a \le p_a$, which is the test of the search for going left. The right side is the mirror case. A child region lies in its parent region, so by induction on depth the claim holds.

**Step 2: two kinds of visited node.** If $R(u) \subseteq Q$, then the point of $u$, which lies in $R(u)$, is in $Q$ and is reported; distinct nodes have distinct points, so there are at most $r$ such nodes. Otherwise $R(u)$ has a point $x \in Q$ and a point $y \notin Q$. The segment from $x$ to $y$ lies in the convex set $R(u)$ and leaves $Q$ at a point of the boundary of $Q$. The boundary lies in the $2k$ hyperplanes $x_i = \ell_i$ and $x_i = h_i$. So $R(u)$ meets one of these hyperplanes.

**Step 3: one hyperplane.** Fix a hyperplane $\Pi = \{x : x_a = c\}$, and let $N_t$ be the number of nodes at depth $t$ whose region meets $\Pi$. A child region lies in the parent region, so these nodes form a subtree that contains the parent of each of its nodes. Let $t$ be such a node, with axis $b$ and point $p$.

- If $b \ne a$, both children may meet $\Pi$.
- If $b = a$ and $c < p_a$, only the left child region can meet $\Pi$, since the right one has $x_a \ge p_a > c$; if $c > p_a$, only the right one. Both can meet $\Pi$ only if $p_a = c$, and since no two points share a coordinate on axis $a$, this happens at no more than one node of the whole tree.

Let $c_a(t)$ be the number of depths among $0, \ldots, t - 1$ whose axis is $a$, and let $E_t$ be 1 if the special node with $p_a = c$ exists at a depth less than $t$, else 0. We show $N_t \le (1 + E_t) \cdot 2^{t - c_a(t)}$ by induction. At $t = 0$, $N_0 \le 1$. If depth $t$ has an axis other than $a$, then $N_{t+1} \le 2N_t$ and the exponent grows by 1. If depth $t$ has axis $a$ and holds no special node, $N_{t+1} \le N_t$ and the exponent does not change. If depth $t$ has axis $a$ and holds the special node, then $E_t = 0$, $E_{t+1} = 1$, and $N_{t+1} \le N_t + 1 \le 2^{t - c_a(t)} + 1 \le 2 \cdot 2^{(t+1) - c_a(t+1)}$. So the claim holds, and $N_t \le 2 \cdot 2^{t - c_a(t)}$.

Each $k$ consecutive depths contain one with axis $a$, so $c_a(t) \ge \lfloor t/k \rfloor > t/k - 1$, and
$$N_t \le 2 \cdot 2^{t - \lfloor t/k \rfloor} < 4 \cdot \rho^{t}, \qquad \rho = 2^{1 - 1/k}.$$

**Step 4: the height.** A subtree of size $s$ has children of size at most $\lfloor s/2 \rfloor$, so a node at depth $t$ has a subtree of at most $n / 2^t$ nodes, and the depths go from 0 to $D \le \lfloor \lg n \rfloor$. Then $\rho^{D+1} \le \rho \cdot \rho^{\lg n} = \rho\, n^{1 - 1/k}$. Summing,
$$\sum_{t=0}^{D} N_t < 4 \sum_{t=0}^{D} \rho^t < \frac{4\rho^{D+1}}{\rho - 1} \le \frac{4\rho}{\rho - 1}\, n^{1 - 1/k}.$$
For $k \ge 2$, $\rho \ge \sqrt 2$, and $\rho/(\rho - 1)$ falls as $\rho$ grows, so $\rho / (\rho - 1) \le \sqrt 2/(\sqrt 2 - 1) = 2 + \sqrt 2 < 3.5$. So one hyperplane meets fewer than $14\, n^{1 - 1/k}$ regions.

**Step 5: the total.** By Step 2, the visited nodes are at most $r$ nodes of the first kind plus the nodes whose region meets one of $2k$ hyperplanes, fewer than $2k \cdot 14\, n^{1 - 1/k}$ by Steps 3 and 4. This gives the bound $28 k\, n^{1 - 1/k} + r$.

**Step 6: the lower bound.** Let $n = 2^H - 1$. A subtree of size $2^j - 1$ splits into two of size $2^{j-1} - 1$, so $T$ is a complete binary tree with depths $0$ to $H - 1$. Pick $c$ that is not the first coordinate of any point, and $M$ larger than every coordinate in absolute value, and let $Q = [c, c] \times [-M, M]^{k-1}$. No point lies in $Q$, so $r = 0$. A region $R(u)$ contains the point of $u$, whose other coordinates lie in $[-M, M]$; so $R(u)$ meets $Q$ exactly when its interval on axis 0 contains $c$. At a node whose axis is not 0, both children keep the interval of the parent on axis 0. At a node with axis 0 and point $p$, exactly one child keeps $c$ in its interval, since $c \ne p_0$. So the number of visited nodes at depth $t$ is exactly $2^{t - c_0(t)}$, with $c_0(t) = \lceil t/k \rceil$, the number of multiples of $k$ in $0, \ldots, t-1$. At depth $H - 1$ alone this is $2^{(H-1) - \lceil (H-1)/k \rceil} \ge 2^{(H-1)(1 - 1/k) - 1} = \tfrac12 \big(\tfrac{n+1}{2}\big)^{1 - 1/k}$. $\blacksquare$

## Consequences

- **Range reporting in the plane.** A k-d tree with linear space answers orthogonal range reporting on $n$ points in $O(\sqrt n + r)$ time, and in $k$ dimensions in $O(n^{1-1/k} + r)$ time, for fixed $k$. For $k = 2$ this is the bound in Section 5.2 of de Berg and others, there stated for the form with points in the leaves.
- **Counting.** If each node also stores the size of its subtree, a node whose region lies inside $Q$ adds that size and stops. The search then visits only the nodes whose region meets the boundary of $Q$, and their parents, so it counts the points in $Q$ in $O(n^{1 - 1/k})$ time, with no $r$ term.
- **Partial match.** A query that fixes $s$ of the $k$ coordinates and leaves the others free asks for the points on a flat of dimension $k - s$. The argument of Step 3, with $s$ of each $k$ levels passing on only one child, bounds the visited nodes by $O(n^{1 - s/k} + r)$.
- **Comparison.** A [range tree](/range-tree/) answers the same query in $O(\log^{k-1} n + r)$ time with $O(n \log^{k-1} n)$ space. For linear space, the bound of the k-d tree is close to the best possible: in the model of the [range searching lower bound](/range-searching-lower-bound/), structures of near linear size need time polynomial in $n$.
- **High dimensions.** When $k$ grows like $\lg n$, the bound $n^{1 - 1/k}$ is no better than a scan of all points, which is one face of the [curse of dimensionality](/curse-of-dimensionality/).

## Tightness

The lower bound of Step 6 shows that the term $n^{1 - 1/k}$ cannot be removed, even for queries with no answer: for $k = 2$, a thin vertical slab that holds no point visits $\sum_{t=0}^{H-1} 2^{\lfloor t/2 \rfloor}$ nodes. For $n = 63, 255, 1023, 4095, 16383$ this is $14, 30, 62, 126, 254$, which is about $2\sqrt n$. The constant $28k$ of the upper bound is not tight, and its growth with $k$ comes from the $2k$ faces of the box. The theorem needs a balanced tree: on a tree built by insertions in sorted order, which is a path, the same slab visits all $n$ nodes. It also uses distinct coordinates on each axis; with many equal coordinates, the special nodes of Step 3 can be many, and a splitting rule that handles ties must be analyzed apart.

## History

Bentley defined the k-d tree and its region search in 1975. D. T. Lee and C. K. Wong proved the worst-case bound $O(k\, n^{1 - 1/k})$ for region search in a balanced k-d tree in 1977, together with the same bound for balanced quad trees and bounds for partial region queries. The proof through the regions that a line meets became the standard textbook argument, as in Chapter 5 of de Berg and others.

## References
