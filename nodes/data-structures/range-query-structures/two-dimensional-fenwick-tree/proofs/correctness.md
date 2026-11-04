---
title: The two-dimensional Fenwick tree keeps its block sums and returns rectangle sums
proves: [correctness, termination]
status: full
---

We use 1-based table indices. For $x \ge 1$, $g(x)$ is the lowest set bit of $x$ and $R(x) = (x - g(x), x]$. Write $M'[a][b] = M[a - 1][b - 1]$ for $1 \le a \le n$, $1 \le b \le m$. The invariant is

$$\text{(F)} \qquad F[i][j] = \sum_{a \in R(i)} \sum_{b \in R(j)} M'[a][b] \quad \text{for } 1 \le i \le n,\ 1 \le j \le m.$$

**Lemma 1 (down chains).** Let $x \ge 0$ and $x_0 = x$, $x_{t+1} = x_t - g(x_t)$ while $x_t > 0$. The chain reaches 0 after at most $\lfloor \lg x \rfloor + 1$ steps when $x \ge 1$, and the ranges $R(x_t)$ over the nonzero $x_t$ are disjoint with union $\{1, \ldots, x\}$.

*Proof.* Subtracting $g(x_t)$ clears the lowest set bit, so each step lowers the number of set bits by one, and $x$ has at most $\lfloor \lg x \rfloor + 1$ of them. The range $R(x_t)$ is $(x_{t+1}, x_t]$. These intervals are adjacent and descend from $x$ to $0$, so they are disjoint and their union is $(0, x]$. $\square$

**Lemma 2 (up chains).** Let $1 \le p \le N$ and $p_0 = p$, $p_{s+1} = p_s + g(p_s)$. For $1 \le y \le N$: $p \in R(y)$ if and only if $y = p_s$ for some $s$. The chain has at most $\lfloor \lg N \rfloor + 1$ terms that are at most $N$.

*Proof.* First, $g(p_{s+1}) > g(p_s)$. Write $p_s = q \cdot 2^{k+1} + 2^k$ with $g(p_s) = 2^k$. Then $p_{s+1} = (q + 1) 2^{k+1}$, which is a multiple of $2^{k+1}$, so $g(p_{s+1}) = 2^{k'}$ with $k' \ge k + 1$. So the chain is strictly increasing, and the exponent of $g$ grows by at least 1 per step; since $g(y) \le y \le N$, at most $\lfloor \lg N \rfloor + 1$ terms are at most $N$.

*Every chain term covers $p$.* Clearly $p \in R(p_0)$. We show $R(p_s) \subseteq R(p_{s+1})$. With the notation above, $p_{s+1} - g(p_{s+1}) = (q + 1)2^{k+1} - 2^{k'} \le (q + 1) 2^{k+1} - 2^{k+1} = q \cdot 2^{k+1} = p_s - g(p_s)$, and $p_s < p_{s+1}$. So the interval $(p_s - g(p_s), p_s]$ lies inside $(p_{s+1} - g(p_{s+1}), p_{s+1}]$. By induction $p \in R(p_s)$ for every $s$.

*No other index covers $p$.* Let $p \in R(y)$, so $y \ge p = p_0$. Assume that $y$ is not a chain term. The chain is strictly increasing and unbounded, so there is an $s$ with $p_s < y < p_{s+1} = p_s + g(p_s)$. Write $y = p_s + t$ with $0 < t < g(p_s)$. Since $p_s$ is a multiple of $g(p_s) > t$, the lowest set bit of $y$ is that of $t$, so $g(y) = g(t) \le t$. Then $y - g(y) \ge y - t = p_s$, so $p_s \notin R(y)$. But $R(y)$ is an interval that ends at $y > p_s$ and holds $p \le p_s$, so it holds $p_s$. This is a contradiction. $\square$

**Lemma 3 (build).** After BUILD, (F) holds.

*Proof.* *Row pass.* Fix a row $i$ and write $v_j = M'[i][j]$ and $G_j = F[i][j]$. We show that after lines L2 and L3, $G_j = \sum_{b \in R(j)} v_b$ for all $j$. The loop pushes $G_j$ into $G_{j + g(j)}$ at step $j$. Call $j'$ a *child* of $j$ when $j' + g(j') = j$. Each child $j'$ of $j$ is less than $j$, and $G_{j'}$ receives pushes only from its own children, which are less than $j'$, so $G_{j'}$ is final when it is pushed. So at the end, $G_j = v_j + \sum_{j' \text{ child of } j} G_{j'}$, and by induction on $j$ it suffices that the ranges of the children of $j$ split $R(j) \setminus \{j\} = (j - g(j), j - 1]$. Let $g(j) = 2^k$ and $j = q \cdot 2^{k+1} + 2^k$. For $0 \le t < k$, the index $j - 2^t$ has $g(j - 2^t) = 2^t$, since $j$ is a multiple of $2^k > 2^t$, so it is a child of $j$. Conversely, let $j'$ be a child of $j$ with $g(j') = 2^t$. Adding $2^t$ to $j'$ clears bit $t$ with a carry, so $j = j' + 2^t$ is a multiple of $2^{t+1}$. Then $2^k = g(j) \ge 2^{t+1}$, so $t < k$ and $j' = j - 2^t$. So the children are $j - 2^t$ for $0 \le t < k$, with $R(j - 2^t) = (j - 2^{t+1}, j - 2^t]$. These intervals for $t = 0, \ldots, k - 1$ are adjacent and cover $(j - 2^k, j - 1]$, as required.

*Column pass.* Lines L4 and L5 do the same push over $i$, with the whole row $F[i][\cdot]$ as the value, and vectors add entry by entry. By the same argument, after the pass row $i$ is the sum of the rows $i'$ of the row pass with $i' \in R(i)$, entry by entry. With the row pass this gives (F). $\square$

**Lemma 4 (add).** If (F) holds before ADD$(r, c, \delta)$ with $0 \le r < n$ and $0 \le c < m$, it holds after it for the matrix with $M[r][c]$ increased by $\delta$.

*Proof.* The right side of (F) for $(i, j)$ grows by $\delta$ exactly when $r + 1 \in R(i)$ and $c + 1 \in R(j)$, and stays the same otherwise. By Lemma 2 with $N = n$ and $N = m$, these are exactly the pairs with $i$ on the up chain of $r + 1$ and $j$ on the up chain of $c + 1$. Lines L6 to L12 visit exactly these pairs, each once, since the outer loop runs over the up chain of $r + 1$ while $i \le n$, and line L8 restarts the inner loop over the up chain of $c + 1$ for each $i$. $\square$

**Lemma 5 (prefix).** If (F) holds, PREFIX$(r, c)$ with $0 \le r \le n$ and $0 \le c \le m$ returns $\sum_{a = 1}^{r} \sum_{b = 1}^{c} M'[a][b]$.

*Proof.* The loops add $F[i][j]$ for $i$ on the down chain of $r$ and $j$ on the down chain of $c$, both without 0. By (F) this is the sum of $M'$ over the union of the blocks $R(i) \times R(j)$. By Lemma 1, the sets $R(i)$ split $\{1, \ldots, r\}$ and the sets $R(j)$ split $\{1, \ldots, c\}$, so their products split $\{1, \ldots, r\} \times \{1, \ldots, c\}$, and each cell of the corner is counted once. If $r = 0$ or $c = 0$, a loop does not run and the result is the empty sum 0. $\square$

**Lemma 6 (query).** If (F) holds, QUERY$(r_1, c_1, r_2, c_2)$ returns $\sum_{r = r_1}^{r_2} \sum_{c = c_1}^{c_2} M[r][c]$.

*Proof.* Let $P(r, c)$ be the corner sum of Lemma 5. A cell $(a, b)$ of $M$, 0-based, with $a \le r_2$ and $b \le c_2$ is counted in $P(r_2 + 1, c_2 + 1)$, and is subtracted in $P(r_1, c_2 + 1)$ when $a < r_1$ and in $P(r_2 + 1, c_1)$ when $b < c_1$, and added back in $P(r_1, c_1)$ when both hold. Its weight is $(1 - [a < r_1])(1 - [b < c_1])$, which is 1 inside the rectangle and 0 outside. Cells with $a > r_2$ or $b > c_2$ are in no term. The group is commutative, so the order of the terms does not matter. $\square$

**Termination.** In BUILD all loops run over fixed finite ranges. In ADD, $i \ge 1$ and $j \ge 1$ at each step, so $g(i), g(j) \ge 1$ and the indices grow strictly up to the bounds $n$ and $m$. In PREFIX, the indices drop strictly to 0 by Lemma 1. So every operation ends.

**Theorem.** After BUILD on $M$ and any sequence of ADD calls, QUERY returns the sum of the current matrix over the given rectangle.

*Proof.* By Lemma 3, (F) holds after BUILD, and by Lemma 4 it holds after each ADD for the current matrix. By Lemma 6, QUERY then returns the rectangle sum, and every call ends by the termination argument. $\blacksquare$
