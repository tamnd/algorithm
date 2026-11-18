---
title: The ring search returns the exact k nearest feature distances
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page, in two dimensions. Arithmetic is exact (real-ram). The cells are the unit squares $[i, i+1) \times [j, j+1)$ for integer $i, j$. Each cell holds a finite set of feature points inside it, which depends only on the seed and the cell. The distance $\delta$ is the Euclidean, the Manhattan or the Chebyshev distance. All three satisfy $\delta(x, p) \ge |x_a - p_a|$ for each axis $a$.

Let $c = \lfloor x \rfloor$ be the cell of the query $x$, and let $f = x - c \in [0, 1)^2$. Line L1 sets $m = \min(f_1, 1 - f_1, f_2, 1 - f_2)$. Let $B_r$ be the set of cells $b$ with $\max(|b_1 - c_1|, |b_2 - c_2|) \le r$. Ring $r$ is $B_r \setminus B_{r-1}$, with $B_{-1} = \emptyset$.

**Lemma 1 (the rings).** The code function `ring(c, r)` lists each cell of ring $r$ exactly once. So after the loop of lines L4 to L6 has run for $r = 0, \dots, R$, it has visited each cell of $B_R$ exactly once.

*Proof.* For $r = 0$ it lists $c$ only. For $r \ge 1$ it lists the two rows $b_2 = c_2 \pm r$ with $b_1$ from $c_1 - r$ to $c_1 + r$, and the two columns $b_1 = c_1 \pm r$ with $b_2$ strictly between $c_2 - r$ and $c_2 + r$. A cell has Chebyshev distance exactly $r$ from $c$ if and only if one of its coordinates differs by exactly $r$ and the other by at most $r$, so these lists cover ring $r$. The rows and the columns do not share a cell, so no cell repeats. There are $2(2r + 1) + 2(2r - 1) = 8r$ cells, which the code test `test_ring_enumerates_each_cell_once` checks. $\square$

**Lemma 2 (points outside the block are far).** If a feature point $p$ lies in a cell outside $B_r$, then $\delta(x, p) \ge r + m$.

*Proof.* The cells of $B_r$ cover the square $Q = [c_1 - r, c_1 + r + 1) \times [c_2 - r, c_2 + r + 1)$, and the cells are disjoint, so $p \notin Q$. So for some axis $a$, either $p_a < c_a - r$ or $p_a \ge c_a + r + 1$. In the first case $x_a - p_a > x_a - c_a + r = f_a + r \ge r + m$. In the second case $p_a - x_a \ge c_a + r + 1 - x_a = (1 - f_a) + r \ge r + m$. So $\delta(x, p) \ge |x_a - p_a| \ge r + m$. $\square$

**Invariant.** After lines L4 to L6 have run for ring $r$, the list `best` is the sorted list of the $\min(k, n_r)$ smallest distances from $x$ to the feature points in the cells of $B_r$, counted with multiplicity, where $n_r$ is the number of those points.

*Proof.* By Lemma 1, line L5 sees each point of $B_r$ exactly once. Line L6 keeps a sorted list of at most $k$ values. A new distance $d$ enters when the list is short or $d$ is less than the largest kept value. Then the largest value drops off if the list grows past $k$. This is the standard way to keep the $k$ smallest of a stream: a value that drops off has $k$ kept values at most as large as it, so it is not among the $k$ smallest of the stream so far, and it never returns. $\square$

**Theorem 1 (exactness).** If line L8 returns, its list is $(F_1(x), \dots, F_k(x))$, the sorted distances from $x$ to its $k$ nearest feature points among all cells.

*Proof.* Line L7 holds, so `best` has $k$ entries and its largest is at most $r + m$. By the invariant, `best` lists the $k$ smallest distances to points in $B_r$. By Lemma 2, every other point has a distance of at least $r + m \ge$ `best`$[k]$. So no point outside $B_r$ can take a place among the $k$ smallest with a smaller value, and the sorted list of the $k$ smallest values over all points is `best`. $\square$

**Theorem 2 (the loop stops).** If at least $k$ feature points exist, line L8 returns. It returns no later than at ring $R = \max(r_k, \lceil F_k(x) \rceil)$, where $r_k$ is the ring of a $k$-th nearest point.

*Proof.* After ring $R \ge r_k$, the block $B_R$ holds the $k$ nearest points, so `best` has $k$ entries with the largest equal to $F_k(x)$. Since $R \ge F_k(x)$ and $m \ge 0$, the test $F_k(x) \le R + m$ of line L7 holds. $\square$

The point of the margin $m$ is that the search can stop at ring $\lceil F_k - m \rceil$ in place of $\lceil F_k \rceil$, which saves a full ring in many queries.

**Theorem 3 (the 1-Lipschitz bound).** For the Euclidean distance, $|F_k(x) - F_k(y)| \le |x - y|$ for every $k$.

*Proof.* Each point $p$ has $|x - p| \le |y - p| + |x - y|$ by the triangle inequality. So the $k$ nearest points of $y$ are $k$ points within the distance $F_k(y) + |x - y|$ of $x$, and $F_k(x) \le F_k(y) + |x - y|$. The same holds with $x$ and $y$ swapped. $\square$

**Expected cost.** Assume the ideal model: the counts of the cells are independent Poisson variables with mean $\lambda$, and the points are uniform in their cells, so the points form a Poisson process of intensity $\lambda$. Then $\lambda \pi F_k^2$ has the Gamma distribution with shape $k$, and $E[F_k^2] = k / (\pi \lambda)$. A point at Euclidean distance $F_k$ lies in a ring at most $F_k + 1$, so by Theorem 2 the search visits at most $(2 F_k + 3)^2 \le 8 F_k^2 + 18$ cells, and the expected number of cells is at most $8k / (\pi \lambda) + 18 = O(1 + k / \lambda)$. Whether ring $r$ is visited depends only on the rings before it, and the count of ring $r$ is independent of them, so by Wald's identity the expected number of points seen is $\lambda$ times the expected number of cells, which is $O(\lambda + k)$. Each point costs $O(k)$ in line L6. The expected time per query is $O(1 + k / \lambda + (\lambda + k) k)$, which is $O(1)$ for fixed $k$ and $\lambda$.
