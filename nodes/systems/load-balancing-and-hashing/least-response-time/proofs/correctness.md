---
title: Least response time picks the smallest estimated time to finish, its estimate is a convex average, and a burst is split near the speed shares
proves: [correctness, termination]
status: full
---

We use the pseudocode LRT-PICK and LRT-DONE of the page, with $0 < \alpha \le 1$. A backend is *eligible* if $up[j]$ holds and $w[j] > 0$. The caller runs LRT-DONE$(j, x)$ once for each request to $j$ that ends, with its measured time $x \ge 0$.

**Claim 1 (exact counters).** Between calls, $a[j]$ is the number of requests to $j$ in flight. The proof is the induction of [least connections](/least-connections/): line L7 adds 1 for each request sent, line L9 subtracts 1 for each request that ends, and nothing else changes $a[j]$.

**Claim 2 (the choice).** LRT-PICK returns none if no backend is eligible. Otherwise it returns the smallest index among the eligible backends with the smallest value of $e[j] / w[j]$, where $e[j] = L[j]\,(a[j] + 1)$.

*Proof.* For eligible $i$ and $j$, $w[i]\,w[j] > 0$, so $e[j]\,w[i] < e[i]\,w[j]$ holds if and only if $e[j]/w[j] < e[i]/w[i]$. With this, the invariant of the loop of line L2 is the one of [weighted least connections](/weighted-least-connections/): before the pass for index $j$, $best$ is the smallest index of an eligible backend in $0, \ldots, j-1$ with the smallest ratio there, or none if there is no eligible backend there. Line L3 skips the backends that are not eligible, line L5 replaces $best$ only on a strictly smaller ratio, and the loop ends after $n$ passes. $\square$

**Claim 3 (the estimate is an average).** Let $L_0$ be the value of $L[j]$ after its first sample (or a given start value), and let $x_1, \ldots, x_k$ be the samples that follow, in order. Then after them

$$L[j] = (1 - \alpha)^k L_0 + \sum_{i=1}^{k} \alpha (1 - \alpha)^{k-i} x_i ,$$

and $\min(L_0, x_1, \ldots, x_k) \le L[j] \le \max(L_0, x_1, \ldots, x_k)$.

*Proof.* By induction on $k$. For $k = 0$ the formula gives $L_0$. If it holds for $k$, line L11 gives $L + \alpha(x_{k+1} - L) = (1 - \alpha) L + \alpha x_{k+1}$. Multiplying every term of the formula for $k$ by $1 - \alpha$ and adding $\alpha x_{k+1} = \alpha(1-\alpha)^0 x_{k+1}$ gives the formula for $k + 1$. The coefficients are $\ge 0$, because $0 \le 1 - \alpha < 1$, and they add up to $(1-\alpha)^k + \alpha \sum_{i=0}^{k-1} (1-\alpha)^i = (1-\alpha)^k + 1 - (1-\alpha)^k = 1$ by the geometric sum. A weighted average with non-negative weights that add up to 1 lies between the smallest and the largest of the averaged values. $\square$

**Claim 4 (step response).** If $x_1 = \cdots = x_k = y$, then $L[j] - y = (1 - \alpha)^k (L_0 - y)$. So the distance to $y$ halves after $\lceil \ln 2 / (-\ln(1 - \alpha)) \rceil$ samples when $\alpha < 1$.

*Proof.* Put $x_i = y$ in Claim 3. The sum of the coefficients of the samples is $1 - (1 - \alpha)^k$, so $L[j] = (1-\alpha)^k L_0 + (1 - (1-\alpha)^k)\, y$, and subtracting $y$ gives the formula. The factor $(1-\alpha)^k$ is at most $1/2$ exactly when $k \ge \ln 2 / (-\ln(1-\alpha))$. $\square$

**Claim 5 (a burst).** Suppose $k$ requests arrive before any of them ends, all flags and weights stay fixed, every eligible backend has $L[j] > 0$, and all counters are 0 at the start of the burst. Let $u_j = w[j] / L[j]$ for each eligible $j$, $U = \sum_j u_j$, and let $c_j$ be the number of the $k$ requests that go to $j$. If there are $e$ eligible backends, then

$$\frac{k\, u_j}{U} - 1 \le c_j \le \frac{k\, u_j}{U} + (e - 1).$$

*Proof.* No request ends, so line L11 never runs during the burst and every $L[j]$ is fixed. The quantity that LRT-PICK minimizes is $e[j]/w[j] = (c_j + 1)/u_j$, so each pick goes to a backend with the largest value of $s_j = u_j / (c_j + 1)$, where $c_j$ is the count so far. Let $m_t$ be the largest $s_j$ after $t$ picks. A pick lowers the $s_j$ of the picked backend and changes no other, so $m_t$ never grows. Look at the end of the burst and set $m = m_k > 0$. Take a backend $i$ with $c_i \ge 1$, and look at its last pick, at some time $t < k$. Before that pick its count was $c_i - 1$, its value was $u_i / c_i$, and that value was the largest, so $u_i / c_i = m_t \ge m$. Hence $c_i \le u_i / m$, and this also holds when $c_i = 0$. Summing over the eligible backends gives $k \le U / m$, so $m \le U/k$. For every eligible $j$, $u_j/(c_j + 1) \le m \le U/k$, which gives the lower bound $c_j \ge k u_j / U - 1$. For the upper bound, $c_j = k - \sum_{i \ne j} c_i \le k - \sum_{i \ne j} (k u_i / U - 1) = k u_j / U + (e - 1)$. $\square$

**Claim 6 (herding of the latency-only rule).** Under the hypotheses of Claim 5, the rule that ranks by $L[j]/w[j]$ alone sends all $k$ requests of the burst to the same backend.

*Proof.* The rank does not depend on $a[j]$, and no $L[j]$ changes during the burst, so each pick sees the same values and, by the argument of Claim 2, returns the same index. $\square$

**Termination.** LRT-PICK makes $n$ passes of constant work, and LRT-DONE makes a constant number of steps. $\blacksquare$

Claims 5 and 6 explain the factor $a[j] + 1$: it turns a burst that the latency estimate cannot see into a split close to the measured speeds, while the estimate alone sends the burst to one backend. The bounds say nothing about response times in a queueing model; the policy is a heuristic there.
