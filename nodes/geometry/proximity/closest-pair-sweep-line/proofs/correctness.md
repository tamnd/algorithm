---
title: The plane sweep returns a closest pair
proves: [correctness, termination]
status: full
---

**Setting.** After line L2 the items are $P[0], \ldots, P[n-1]$ in $(x, y)$-order, so $P[a].x \le P[b].x$ for $a < b$. Equal points are different items. For $k \ge 0$ let $D_k = \min\{\|P[a] - P[b]\|^2 : 0 \le a < b < k\}$, with $D_k = \infty$ for $k \le 1$.

**Invariant.** At the start of step $k$ (line L5), (I1) $\delta^2 = D_k$ and $best$ is a pair reaching it when $k \ge 2$; (I2) $T$ holds exactly $P[\mathit{left}], \ldots, P[k-1]$; (I3) for every $j < \mathit{left}$ and every $k' \ge k$, $(P[k'].x - P[j].x)^2 \ge D_k$.

At $k = 0$: $\delta^2 = \infty = D_0$, $T$ is empty and $\mathit{left} = 0$, so all three hold.

**Lemma 1 (removal is safe).** Lines L6 and L7 keep (I2) and (I3) with the same $\delta^2 = D_k$.

*Proof.* Each iteration deletes $P[\mathit{left}]$ from $T$ and increases $\mathit{left}$, so (I2) holds. The removed item $P[j]$ satisfies $(P[k].x - P[j].x)^2 \ge D_k$; for $k' \ge k$, $P[k'].x \ge P[k].x \ge P[j].x$, so $(P[k'].x - P[j].x)^2 \ge (P[k].x - P[j].x)^2 \ge D_k$. This is (I3) for the new $\mathit{left}$. $\square$

**Lemma 2 (the walks find every better pair).** Let $\delta^2_{\mathrm{end}}$ be the value of $\delta^2$ after line L15 of step $k$. If some $j < k$ has $\|P[k] - P[j]\|^2 < D_k$, then $\delta^2_{\mathrm{end}} \le \|P[k] - P[j]\|^2$.

*Proof.* Let $d^2 = \|P[k] - P[j]\|^2 < D_k$. Then $(P[k].x - P[j].x)^2 \le d^2 < D_k$, so $j \ge \mathit{left}$ by (I3), and $P[j] \in T$ by (I2). Say the key of $P[j]$ is larger than the key of $P[k]$ (the other case is symmetric with lines L12 to L15). The upward walk of lines L8 to L11 visits the elements of $T$ above $P[k]$ in increasing key order. Suppose it stops before it reaches $P[j]$, at an element $q$ with $(q.y - P[k].y)^2 \ge \delta^2$, where $\delta^2$ is the current value. Since keys are ordered by $y$ first, $P[k].y \le q.y \le P[j].y$, so $(q.y - P[k].y)^2 \le (P[j].y - P[k].y)^2 \le d^2$. Hence the current $\delta^2 \le d^2$, and since $\delta^2$ never increases, $\delta^2_{\mathrm{end}} \le d^2$. If the walk reaches $P[j]$, line L10 compares $d^2$ with $\delta^2$ and afterwards $\delta^2 \le d^2$. In both cases the claim holds. $\square$

**Lemma 3 (the step keeps the invariant).** After step $k$, (I1), (I2) and (I3) hold for $k + 1$.

*Proof.* Every value stored by lines L10 and L14 is $\|P[k] - q\|^2$ for some $q \in T$, an item with index less than $k$, so $\delta^2_{\mathrm{end}} \ge D_{k+1}$. On the other hand $D_{k+1} = \min(D_k, \min_{j < k} \|P[k] - P[j]\|^2)$. If $D_{k+1} = D_k$, then $\delta^2_{\mathrm{end}} \le D_k$ since $\delta^2$ never grows. Otherwise some $j < k$ has $\|P[k] - P[j]\|^2 = D_{k+1} < D_k$, and Lemma 2 gives $\delta^2_{\mathrm{end}} \le D_{k+1}$. So $\delta^2 = D_{k+1}$, and $best$ is the pair that set it, which is (I1). Line L16 inserts $P[k]$, which is (I2) for $k + 1$. For (I3): every $j < \mathit{left}$ and $k' \ge k + 1$ has $(P[k'].x - P[j].x)^2 \ge D_k \ge D_{k+1}$ by Lemma 1. $\square$

**Termination.** Each loop of lines L6 to L7 increases $\mathit{left}$, which is at most $k$. Each walk moves to a strictly larger (or smaller) key of the finite set $T$. So every step ends, and there are $n$ steps.

**Conclusion.** For $n \ge 2$, after step $n - 1$ the invariant for $k = n$ gives $\delta^2 = D_n = \delta^2(P)$ and $best$ is a pair of different items at that squared distance, which line L17 returns. For $n < 2$, line L1 returns none. $\blacksquare$
