---
title: TrustRank has a unique fixed point, its iteration converges at rate alpha, and trust stays near the seeds
proves: [correctness]
status: full
---

Let $V = \{0, \ldots, n-1\}$ be the pages and $E$ the links, with self links removed and repeated links counted once. Let $\omega(q)$ be the out-degree of $q$. The matrix $T$ has $T_{pq} = 1/\omega(q)$ for each link $(q, p) \in E$ and $0$ elsewhere. The seed vector $d$ has $d(s) = 1/|S|$ for each good seed $s \in S$ and $0$ elsewhere, with $S \neq \emptyset$. Fix $\alpha \in [0, 1)$. Line L6 of the algorithm computes $t_0 = d$ and $t_{k+1} = \alpha T t_k + (1 - \alpha) d$. For a vector $x$, $\lVert x \rVert_1 = \sum_p |x_p|$ and $\mathbf{1}^\top x = \sum_p x_p$.

**Lemma 1 (leaky columns).** Column $q$ of $T$ sums to $1$ if $\omega(q) > 0$ and to $0$ if $\omega(q) = 0$. So $\lVert T x \rVert_1 \le \lVert x \rVert_1$ for every real vector $x$, and $\mathbf{1}^\top T x = \sum_{q : \omega(q) > 0} x_q$.

*Proof.* Column $q$ has the entry $1/\omega(q)$ in the $\omega(q)$ rows $p$ with $(q, p) \in E$, and no other nonzero entry. Then $\lVert T x \rVert_1 = \sum_p \lvert \sum_q T_{pq} x_q \rvert \le \sum_q |x_q| \sum_p T_{pq} \le \lVert x \rVert_1$ by the triangle inequality, and $\mathbf{1}^\top T x = \sum_q x_q \sum_p T_{pq}$ is the sum over the pages with an out-link. $\square$

**Theorem 1 (fixed point).** The equation $t = \alpha T t + (1 - \alpha) d$ has exactly one solution,

$$t^* = (1 - \alpha) \sum_{k \ge 0} \alpha^k T^k d,$$

and $t^* \ge 0$ entrywise.

*Proof.* By Lemma 1, $\lVert \alpha^k T^k d \rVert_1 \le \alpha^k$, so the series converges absolutely. Put $t^*$ into the right side: $\alpha T t^* + (1 - \alpha) d = (1 - \alpha) \sum_{k \ge 0} \alpha^{k+1} T^{k+1} d + (1 - \alpha) d = t^*$. If $t$ and $u$ are two solutions, then $t - u = \alpha T (t - u)$, so $\lVert t - u \rVert_1 \le \alpha \lVert t - u \rVert_1$ by Lemma 1, and $\alpha < 1$ forces $t = u$. Each term of the series has nonnegative entries, because $T$ and $d$ do. $\square$

The same argument shows that $I - \alpha T$ is invertible: if $(I - \alpha T) x = 0$ then $\lVert x \rVert_1 \le \alpha \lVert x \rVert_1$, so $x = 0$. So the exact solver of the implementation, which solves $(I - \alpha T) t = (1 - \alpha) d$ by Gaussian elimination in rational numbers, always finds a pivot and returns $t^*$.

**Theorem 2 (rate).** After $M$ rounds, $\lVert t_M - t^* \rVert_1 \le \alpha^M \lVert d - t^* \rVert_1 \le 2 \alpha^M$.

*Proof.* Subtract the fixed point equation from the update: $t_{k+1} - t^* = \alpha T (t_k - t^*)$. By Lemma 1 and induction, $\lVert t_M - t^* \rVert_1 \le \alpha^M \lVert t_0 - t^* \rVert_1$, and $t_0 = d$. Both $d$ and $t^*$ are nonnegative with sums at most $1$ (Theorem 4 below), so $\lVert d - t^* \rVert_1 \le \mathbf{1}^\top d + \mathbf{1}^\top t^* \le 2$. $\square$

With $\alpha = 0.85$ and $M = 20$, as in the paper, the bound is $2 \cdot 0.85^{20} \approx 0.078$. This is a worst-case bound on the sum of the errors; the error is often much smaller, but the bound is what the method guarantees.

**Theorem 3 (support and dampening).** $t^*(p) > 0$ if and only if a directed path leads from some seed to $p$ (a seed is reached by the empty path). If the shortest such path has $k$ links, then $t^*(p) \le \alpha^k$.

*Proof.* Expand $(T^j d)(p) = \sum_{q_0, \ldots, q_j} d(q_0) T_{q_1 q_0} \cdots T_{q_j q_{j-1}}$ over the sequences with $q_j = p$. A term is positive exactly when $q_0$ is a seed and each $(q_{i-1}, q_i)$ is a link, so $(T^j d)(p) > 0$ exactly when a walk of $j$ links leads from a seed to $p$. All terms of the series of Theorem 1 are nonnegative and each $(1 - \alpha)\alpha^j$ is positive, so $t^*(p) > 0$ exactly when such a walk exists for some $j$, that is, when $p$ is reachable. If no walk shorter than $k$ links reaches $p$, the terms with $j < k$ are $0$ at $p$, and by Lemma 1 $(T^j d)(p) \le \mathbf{1}^\top T^j d \le 1$, so $t^*(p) \le (1 - \alpha) \sum_{j \ge k} \alpha^j = \alpha^k$. $\square$

**Theorem 4 (total trust).** $\mathbf{1}^\top t^* \le 1$, with equality if and only if no page reachable from the seeds is dangling (has no out-link).

*Proof.* Let $m_j = \mathbf{1}^\top T^j d$. By Lemma 1, $m_{j+1} = m_j - \sum_{q : \omega(q) = 0} (T^j d)(q) \le m_j$, and $m_0 = 1$. So $\mathbf{1}^\top t^* = (1 - \alpha) \sum_j \alpha^j m_j \le 1$. If no reachable page is dangling, then by the proof of Theorem 3 the vector $T^j d$ is $0$ outside the reachable pages, so the subtracted sum is $0$, every $m_j = 1$, and the total is $1$. If a reachable page $q$ is dangling, then $(T^j d)(q) > 0$ for some $j$ by Theorem 3, so $m_{j+1} < m_j \le 1$, hence $m_i < 1$ for all $i > j$ and the total is less than $1$. $\square$

**Theorem 5 (leak into a set).** Let $U \subseteq V$ contain no seed, and let $X = \sum_{(q, p) \in E,\ q \notin U,\ p \in U} t^*(q)/\omega(q)$ be the trust that links from outside bring into $U$. Then $\sum_{p \in U} t^*(p) \le \frac{\alpha}{1 - \alpha} X$.

*Proof.* For $p \in U$, $d(p) = 0$, so the fixed point equation gives $t^*(p) = \alpha \sum_{(q, p) \in E} t^*(q)/\omega(q)$. Sum over $p \in U$ and split the links by whether $q \in U$. The links from outside give $X$. A page $q \in U$ sends $t^*(q)/\omega(q)$ along each of its $\omega(q)$ links, so the links inside $U$ give at most $\sum_{q \in U} t^*(q)$. Write $t_U$ for this sum. Then $t_U \le \alpha (X + t_U)$, so $t_U \le \alpha X / (1 - \alpha)$. $\square$

For $\alpha = 0.85$ the factor is $17/3 \approx 5.67$. A link farm with no link from a reachable page has $X = 0$ and so no trust (Theorem 3 says the same). A farm that gets links from good pages can hold at most $17/3$ times the trust that those links carry in, however many pages it has.

**Seed selection.** Lines L1 to L4 only choose $d$: they rank the pages by inverse PageRank (Theorem 1 applies to it with the reversed links and $d$ uniform), take the first $L$ pages in that order with ties to the smaller page, and keep those that the oracle calls good. The results above hold for every nonempty seed set, so they do not depend on how good the seed choice is. How well the seeds cover the good part of the web is a measured property; the paper notes that an exact choice of the seeds that reach the most pages is a hard combinatorial problem, and uses inverse PageRank as a heuristic.
