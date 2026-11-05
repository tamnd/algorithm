---
title: The RP-tree partitions the points, has logarithmic depth with distinct projections, and its branch and bound search is exact
proves: [correctness]
status: full
---

We use the names of the pseudocode on the page. Fix the points $P = \{x_0, \ldots, x_{n-1}\} \subset \mathbb{R}^D$, the leaf size $n_0 \ge 1$, and any sequence of directions, each normalized to unit length. Ties in distance are broken by index, so "the $k$ nearest" means the $k$ smallest pairs $(\|q - x_i\|, i)$.

**Lemma 1 (structure).** BUILD$(S)$ terminates, and the tree it returns satisfies (I1) to (I3) for $S$.

*Proof.* By induction on $|S|$. If line L1 or line L5 returns a leaf, (I1) holds, (I2) is empty, and (I3) holds: either $|S| \le n_0$, or line L5 found $R = \emptyset$, so every $v \cdot x \le t$; since $t$ is one of the projections and is their lower median, and no projection exceeds it, all projections equal $t$. Otherwise $R \ne \emptyset$, and $L \ne \emptyset$ since the point of rank $\lceil |S|/2 \rceil$ has projection $t$ and goes to $L$. So both $L$ and $R$ are smaller than $S$, the recursive calls terminate and satisfy the invariants for $L$ and $R$ by induction, $L$ and $R$ partition $S$, and line L4 defines them by $v \cdot x \le t$ and $v \cdot x > t$. This gives (I1) and (I2) at the new node, and (I3) at its leaves. $\square$

**Lemma 2 (depth).** If, at every node, the projections of its points are distinct, then every leaf has at most $n_0$ points and the depth is $0$ for $n \le n_0$ and $\lceil \log_2(n/n_0) \rceil$ for $n > n_0$.

*Proof.* With distinct projections, $L$ consists of the points of rank $1, \ldots, \lceil m/2 \rceil$ of a set of size $m$, so $|L| = \lceil m/2 \rceil \ge 1$ and $|R| = \lfloor m/2 \rfloor \ge 1$ when $m \ge 2$; in particular line L5 never fires, so a node becomes a leaf exactly when $m \le n_0$. By induction every node at depth $j$ has at most $\lceil n/2^j \rceil$ points, using $\lceil \lceil a \rceil / 2 \rceil = \lceil a/2 \rceil$, and the leftmost node at depth $j$ has exactly that many. So a leaf appears on every path once $\lceil n/2^j \rceil \le n_0$, and the leftmost path continues while $\lceil n/2^j \rceil > n_0$. Since $n_0$ is an integer, $\lceil n/2^j \rceil \le n_0$ iff $n/2^j \le n_0$ iff $j \ge \log_2(n/n_0)$. The depth is the least such $j$, which is $\lceil \log_2(n/n_0) \rceil$. $\square$

**Lemma 3 (the pruning bound).** Let a node have direction $v$, $\|v\| = 1$, and threshold $t$, and let $g = v \cdot q - t$. If $g \le 0$, every point $x$ of the right subtree has $\|q - x\| > |g|$. If $g > 0$, every point $x$ of the left subtree has $\|q - x\| \ge |g|$.

*Proof.* By Cauchy-Schwarz, $\|q - x\| \ge |v \cdot (q - x)|$. If $g \le 0$ and $x$ is on the right, $v \cdot x > t$ by (I2), so $v \cdot x - v \cdot q > t - v \cdot q = |g|$. If $g > 0$ and $x$ is on the left, $v \cdot x \le t$, so $v \cdot q - v \cdot x \ge v \cdot q - t = |g|$. $\square$

**Theorem (exact search).** QUERY$(root, q, k, \emptyset)$ leaves in $H$ the $\min(k, n)$ smallest pairs $(\|q - x_i\|, i)$.

*Proof.* $H$ keeps, by the offers of line L7, the $k$ smallest pairs among the points evaluated so far, and every evaluated point is a point of $P$. So it suffices to show that every point among the true $\min(k, n)$ nearest is evaluated, or that the final $H$ holds $k$ pairs all at most the pairs of the unevaluated points. Take any point $x$ that is not evaluated. Then some call skipped a far subtree containing $x$ at line L11, at a time when $|H| = k$ and $|g|$ was larger than the largest distance $\beta$ in $H$. By Lemma 3, $\|q - x\| \ge |g| > \beta$. The largest pair of $H$ never increases after $H$ is full, so at the end every pair of $H$ has distance at most $\beta < \|q - x\|$, and $x$ does not belong to the $k$ smallest pairs. Hence the $k$ smallest pairs of $P$ are all evaluated, and $H$ holds them. If $k > n$ then $|H| < k$ at every test of line L11, nothing is skipped, all $n$ points are evaluated, and $H$ holds all of them. $\blacksquare$
