---
title: Stride scheduling keeps every pass within one stride of the minimum, so the pairwise error stays below one quantum
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page with fixed tickets $t_k \ge 1$, $T = \sum_k t_k$, $c$ clients and exact strides $s_k = S / t_k$, where $S = \mathit{stride1}$. Let $a_k$ be the number of quanta that client $k$ has run so far, and let $m = \min_k \mathit{pass}_k$. All statements are about the end of a quantum, and also about the start (no quantum yet).

**Lemma 1 (pass and runs).** $\mathit{pass}_k = a_k s_k$ at all times.

*Proof.* Line L1 sets $\mathit{pass}_k = 0$ with $a_k = 0$. Line L6 adds $s_k$ exactly when $k$ runs one more quantum. No other line changes a pass. $\square$

**Lemma 2 (the pass invariant).** $m \le \mathit{pass}_k \le m + s_k$ for every client $k$.

*Proof.* The left side is the definition of $m$. For the right side we prove $\mathit{pass}_k - s_k \le m$ by induction on the quanta. At the start all passes are 0 and $\mathit{pass}_k - s_k = -s_k < 0 = m$. Assume it holds before a quantum, with minimum $m$. Line L4 takes a client $j$ with $\mathit{pass}_j = m$, because the queue is keyed by the pass. After line L6, $\mathit{pass}_j = m + s_j$, so $\mathit{pass}_j - s_j = m$. The new minimum $m'$ is at least $m$, because the only pass that changed went up. So $\mathit{pass}_j - s_j = m \le m'$, and for $k \ne j$, $\mathit{pass}_k - s_k \le m \le m'$ by the assumption. $\square$

**Theorem 1 (pairwise error).** For any two clients $i$ and $j$, at the end of every quantum,

$$-t_i \le a_i t_j - a_j t_i \le t_j.$$

So $\left| a_i - (a_i + a_j) \frac{t_i}{t_i + t_j} \right| \le \frac{\max(t_i, t_j)}{t_i + t_j} < 1$.

*Proof.* Let $\mu = m / S$. By Lemmas 1 and 2, $m \le a_k S / t_k \le m + S / t_k$, so $\mu t_k \le a_k \le \mu t_k + 1$ for each $k$. Then

$$a_i t_j - a_j t_i \le (\mu t_i + 1) t_j - \mu t_j t_i = t_j,$$
$$a_i t_j - a_j t_i \ge \mu t_i t_j - (\mu t_j + 1) t_i = -t_i.$$

Divide by $t_i + t_j > 0$, and note $a_i - (a_i + a_j) t_i / (t_i + t_j) = (a_i t_j - a_j t_i) / (t_i + t_j)$. Both $t_i$ and $t_j$ are at least 1, so $\max(t_i, t_j) < t_i + t_j$. $\square$

**Theorem 2 (error against the total).** After $n$ quanta, $-c\, t_i / T \le a_i - n t_i / T \le 1$ for each client $i$.

*Proof.* Sum $\mu t_k \le a_k \le \mu t_k + 1$ over the $c$ clients: $\mu T \le n \le \mu T + c$. Then $a_i - n t_i / T \le (\mu t_i + 1) - \mu t_i = 1$, and $a_i - n t_i / T \ge \mu t_i - (\mu T + c) t_i / T = -c\, t_i / T$. $\square$

Since $t_i \le T$, the absolute error of each client is at most $c$ quanta for every $n$. For a lottery with the same tickets, the number of wins is binomial, with standard deviation $\sqrt{n p (1 - p)}$, which grows without bound.

**Theorem 3 (periodicity).** Let $g = \gcd_k t_k$. After $n = T / g$ quanta, $a_k = t_k / g$ for every $k$, and all passes are equal to $S / g$.

*Proof.* At $n = T/g$, $\sum_k a_k = T / g = \sum_k t_k / g$, and each $t_k / g$ is an integer. Suppose some $a_k \ne t_k / g$. Since the sums agree, some client $u$ has $a_u > t_u / g$ and some client $v$ has $a_v < t_v / g$; all $a$ are integers, so $a_u \ge t_u / g + 1$ and $a_v \le t_v / g - 1$. Then $\mathit{pass}_u \ge S / g + s_u$ and $\mathit{pass}_v \le S / g - s_v < S / g$. So $m < S / g$ and $\mathit{pass}_u > m + s_u$, against Lemma 2. Hence $a_k = t_k / g$ and $\mathit{pass}_k = S / g$ for all $k$. All passes are then equal, as at the start, and the tie rule depends only on the join order, so the next $T / g$ quanta repeat the first ones. $\square$

**Termination.** The loop of line L3 runs $n$ times, and each pass does one EXTRACT-MIN and one INSERT on a queue of $c$ clients. So the algorithm ends after $O(n \log c + c)$ steps. $\blacksquare$
