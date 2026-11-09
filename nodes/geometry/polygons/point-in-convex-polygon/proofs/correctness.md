---
title: The fan binary search classifies every point exactly against a strictly convex polygon
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The polygon $V = v_0, \ldots, v_{n-1}$, $n \ge 3$, is strictly convex and counterclockwise, with closed region $R$. Write $o(p, q, r) = (q - p) \times (r - p)$, and let $a = o(v_0, v_1, q)$ and $b = o(v_0, v_{n-1}, q)$ be the two values of line L1. For an edge $v_i v_{i+1}$ let $H_i = \{p : o(v_i, v_{i+1}, p) \ge 0\}$, the closed half-plane to its left.

**Facts about strictly convex polygons.** These are on the page [convex polygon](/convex-polygon/).

- (F1) $R = H_0 \cap \cdots \cap H_{n-1}$.
- (F2) The vertices are the extreme points of $R$, so no vertex lies on the segment between two others, and no three vertices are collinear.
- (F3) $o(v_i, v_{i+1}, v_j) > 0$ for every edge $v_i v_{i+1}$ and every $j \ne i, i+1$: it is $\ge 0$ by (F1), and $\ne 0$ by (F2).

**Claim.** The algorithm stops after at most $\lceil \log_2(n - 2) \rceil$ iterations of the loop. It returns OUTSIDE if $q \notin R$, BOUNDARY if $q$ is on the boundary $\partial R$, and INSIDE if $q$ is in the interior of $R$.

**Step 1 (line L1).** By (F1), $R \subseteq H_0 \cap H_{n-1}$. Now $H_0 = \{p : o(v_0, v_1, p) \ge 0\}$ and $H_{n-1} = \{p : o(v_{n-1}, v_0, p) \ge 0\} = \{p : o(v_0, v_{n-1}, p) \le 0\}$, because $o(v_{n-1}, v_0, p) = o(v_0, p, v_{n-1}) = -o(v_0, v_{n-1}, p)$. So if $a < 0$ or $b > 0$, then $q \notin R$, and OUTSIDE is right. From now on $a \ge 0$ and $b \le 0$.

**Step 2 (loop invariant and termination).** Before each test of line L3 the following hold.

- (I1) $1 \le lo < hi \le n - 1$.
- (I2) $o(v_0, v_{lo}, q) \ge 0$.
- (I3) $o(v_0, v_{hi}, q) < 0$, or $hi = n - 1$.

Line L2 sets $lo = 1$ and $hi = n - 1$; (I1) holds as $n \ge 3$, (I2) is $a \ge 0$, and (I3) holds by its second case. In an iteration $hi - lo \ge 2$, so $lo < mid < hi$. If $o(v_0, v_{mid}, q) \ge 0$, line L5 sets $lo \leftarrow mid$, which keeps (I2); otherwise it sets $hi \leftarrow mid$, which keeps (I3). In both cases (I1) holds and $hi - lo$ becomes $\lceil d/2 \rceil$ or $\lfloor d/2 \rfloor$ of its old value $d$, and the new value is at least 1 and less than $d$. It starts at $n - 2$, so the loop stops after at most $\lceil \log_2(n - 2) \rceil$ iterations, with $hi = lo + 1$.

**Step 3 ($q$ is in the wedge of one fan triangle).** After the loop, let $i = lo$ and $j = hi = i + 1$, so $v_i v_j$ is an edge of the polygon. By (I2), $o(v_0, v_i, q) \ge 0$. By (I3), $o(v_0, v_j, q) < 0$, or $j = n - 1$ and then $o(v_0, v_j, q) = b \le 0$. So $q$ is in

$$S = \{p : o(v_0, v_i, p) \ge 0 \text{ and } o(v_0, v_j, p) \le 0\}.$$

As $1 \le i < j \le n - 1$, the vertex $v_0$ is not an endpoint of the edge $v_i v_j$, so by (F3) $o(v_i, v_j, v_0) > 0$, which equals $o(v_0, v_i, v_j)$. Hence the triangle $T = v_0 v_i v_j$ is counterclockwise with positive area, $S$ is the closed angle of $T$ at $v_0$, and

$$T = S \cap \{p : o(v_i, v_j, p) \ge 0\}.$$

**Step 4 (inside the wedge, the polygon is the triangle).** $R \cap S = T$. The vertices of $T$ are in $R$, and $R$ is convex, so $T \subseteq R$; also $T \subseteq S$. Conversely, $R \subseteq H_i = \{p : o(v_i, v_j, p) \ge 0\}$ by (F1), so $R \cap S \subseteq S \cap H_i = T$.

**Step 5 (lines L6 and L7).** As $q \in S$, Step 4 gives $q \in R$ if and only if $q \in T$, and by Step 3 that holds if and only if $s = o(v_i, v_j, q) \ge 0$. So line L7 returns OUTSIDE exactly when $q \notin R$. From now on $q \in T$.

**Step 6 (which points of $T$ are on the boundary).** We show that a point of $T$ is on $\partial R$ if and only if it is on the side $v_i v_j$ of $T$, or on the side $v_0 v_1$ when $i = 1$, or on the side $v_{n-1} v_0$ when $j = n - 1$. These sides are edges of the polygon, so their points are on $\partial R$. For the converse, the other points of $T$ are of two kinds.

- *Interior points of $T$.* They are interior points of $R$, as $T \subseteq R$.
- *Points on a side $v_0 v_k$ of $T$ that is a diagonal*, that is, $k = i \ge 2$ or $k = j \le n - 2$, other than its endpoints. Suppose such a point $m$ is on $\partial R$. Then $m$ is on some edge, so $o(v_\ell, v_{\ell+1}, m) = 0$ for some $\ell$. The function $p \mapsto o(v_\ell, v_{\ell+1}, p)$ is affine, $\ge 0$ at $v_0$ and $v_k$ by (F1), and $0$ at the point $m$ strictly between them, so it is $0$ at $v_0$ and $v_k$. Then $v_0, v_k, v_\ell, v_{\ell+1}$ are collinear, and by (F2) $\{v_0, v_k\} = \{v_\ell, v_{\ell+1}\}$, so $v_0 v_k$ is an edge and $k \in \{1, n - 1\}$, a contradiction. So $m \in R$ is not on $\partial R$, and it is an interior point of $R$.

The endpoints $v_i$ and $v_j$ of the diagonals are on the side $v_i v_j$. The endpoint $v_0$ needs care: it is on the boundary, and it is on the side $v_0 v_1$ or $v_{n-1} v_0$ of $T$ only if $i = 1$ or $j = n - 1$. If $q = v_0$, every test in line L5 gives $o(v_0, v_{mid}, v_0) = 0 \ge 0$, so $lo$ only grows, the loop ends with $j = n - 1$, and $v_0$ is on the side $v_{n-1} v_0$ of $T$. So for every $q \in T$ the statement holds.

**Step 7 (line L8).** For $q \in T$: $q$ is on the side $v_i v_j$ if and only if $s = 0$ (a point of $T$ on the line of that side is on the side). It is on the side $v_0 v_1$, when $i = 1$, if and only if $a = 0$, and on the side $v_{n-1} v_0$, when $j = n - 1$, if and only if $b = 0$, for the same reason. By Step 6, line L8 returns BOUNDARY exactly when $q \in \partial R$, and line L9 returns INSIDE exactly when $q$ is an interior point of $R$. With Steps 1 and 5, this proves the claim. $\blacksquare$
