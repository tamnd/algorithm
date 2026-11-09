---
title: The randomized grid algorithm always returns a closest pair
proves: [correctness, termination]
status: full
---

**Setting.** After line L2 the items are $P[0], \ldots, P[n-1]$ (equal points are different items). For $k \ge 2$ let $D_k = \min\{\|P[a] - P[b]\|^2 : 0 \le a < b < k\}$. The cell of a point $p$ for side $s$ is $c_s(p) = (\lfloor p.x/s \rfloor, \lfloor p.y/s \rfloor)$.

**Invariant.** At the start of step $k \ge 2$ of line L6, $\delta^2 = D_k > 0$, $best$ is a pair of items among $P[0], \ldots, P[k-1]$ at squared distance $D_k$, and $G$ maps each cell $c$ to the list of items $P[j]$, $j < k$, with $c_s(P[j]) = c$, where $s \le \delta < 2s$.

*Start.* Line L3 sets $\delta^2 = D_2$. If it is $0$, line L4 returns a pair at distance $0$, which is optimal. Otherwise line L5 builds $G$ for $P[0], P[1]$ with a valid $s$.

**Lemma 1 (the block holds every close point).** If $s \le \delta < 2s$ and $\|p - q\| < \delta$, then each coordinate of $c_s(q) - c_s(p)$ is in $\{-2, \ldots, 2\}$.

*Proof.* $|p.x - q.x| \le \|p - q\| < \delta < 2s$, so $|p.x/s - q.x/s| < 2$. For reals $u, v$ with $|u - v| < 2$, $\lfloor u \rfloor - \lfloor v \rfloor < u - (v - 1) < 3$, and the difference is an integer, so it is at most $2$; by symmetry it is at least $-2$. The same holds for $y$. $\square$

**Lemma 2 (one step).** If the invariant holds at the start of step $k$, then after the step either the algorithm has returned a pair at squared distance $D_{k+1} = 0$, or the invariant holds at the start of step $k + 1$.

*Proof.* Let $m = \min_{j < k} \|P[k] - P[j]\|^2$, so $D_{k+1} = \min(D_k, m)$. Line L8 computes the minimum $d^2$ over the items in the $5 \times 5$ block, so $d^2 \ge m$ (with $d^2 = \infty$ if the block is empty).

If $m < D_k$, the item $P[j]$ reaching $m$ has $\|P[k] - P[j]\| < \delta$, so by Lemma 1 and the invariant on $G$ it is in the block, and $d^2 = m$. Line L9 then holds, line L10 sets $\delta^2 = m = D_{k+1}$ and records a pair reaching it. If this is $0$, the algorithm returns an optimal pair. Otherwise line L11 picks a valid $s$ for the new $\delta$ and rebuilds $G$ from $P[0], \ldots, P[k]$, so the invariant holds for $k + 1$.

If $m \ge D_k$, then $d^2 \ge m \ge D_k = \delta^2$, so line L9 fails, $\delta^2 = D_k = D_{k+1}$ stays with its pair, and line L12 adds $P[k]$ to its own cell, so $G$ holds exactly $P[0], \ldots, P[k]$ for the same $s$. $\square$

**Termination.** There are $n - 2$ steps; each looks at $25$ cells, each holding finitely many items, and a rebuild inserts $k + 1$ items. So the algorithm stops for every order produced by line L2.

**Conclusion.** For $n < 2$ line L1 returns none. Otherwise, by induction with Lemma 2, either the algorithm returns early with an optimal pair at distance $0$, or after the last step $\delta^2 = D_n = \delta^2(P)$ and line L13 returns a pair reaching it. This holds for every outcome of the random order in line L2, so the algorithm is a Las Vegas algorithm. $\blacksquare$
