---
title: The regret bound of UCB1 (Auer, Cesa-Bianchi and Fischer 2002, Theorem 1)
proves: [correctness]
status: full
---

**Setting.** A stochastic bandit with $K \ge 2$ arms. The rewards of arm $i$ are i.i.d. with values in $[0,1]$ and mean $\mu_i$, and the arms are independent. Let $\mu^* = \max_i \mu_i$, $\Delta_i = \mu^* - \mu_i$, and fix an optimal arm $*$. We use the pseudocode of the page. Write $c_{u,s} = \sqrt{2\ln u / s}$, and let $\bar X_{i,s}$ be the mean of the first $s$ rewards of arm $i$. Round $t > K$ pulls the arm with the largest $\bar X_{i,N_i} + c_{t-1,N_i}$, where $N_i = T_i(t-1)$ is the number of pulls of arm $i$ before round $t$.

**Theorem.** For each $n \ge K$,

$$\mathbb{E}[T_i(n)] \le \frac{8\ln n}{\Delta_i^2} + 1 + \frac{\pi^2}{3} \quad \text{for each } i \text{ with } \Delta_i > 0,$$

and so the regret is at most $\sum_{i:\Delta_i>0} \frac{8\ln n}{\Delta_i} + \big(1 + \frac{\pi^2}{3}\big)\sum_{j=1}^{K}\Delta_j$.

**Tool.** The [Hoeffding inequality](/hoeffding-inequality/): if $Y_1, \ldots, Y_s$ are independent with values in $[0,1]$ and mean $\mu$, then for $a > 0$, $\Pr[\bar Y_s \le \mu - a] \le e^{-2sa^2}$ and $\Pr[\bar Y_s \ge \mu + a] \le e^{-2sa^2}$. With $a = c_{u,s}$ this gives $e^{-4\ln u} = u^{-4}$.

**The reward table.** Draw in advance, for each arm $i$, an i.i.d. sequence $Y_{i,1}, Y_{i,2}, \ldots$ of its rewards, and let the $s$-th pull of arm $i$ return $Y_{i,s}$. This gives the same law of the whole run as the bandit, so it is enough to prove the bound in this model. Now $\bar X_{i,s} = \frac1s\sum_{r \le s} Y_{i,r}$ is defined for each $s$, whatever the policy does.

*Proof.* Fix $i$ with $\Delta_i > 0$, and let $\ell = \lceil 8\ln n / \Delta_i^2 \rceil$.

*Step 1 (count the late pulls).* Arm $i$ is pulled once in rounds $1, \ldots, K$. After its first $\ell$ pulls, each further pull happens in a round $t$ with $T_i(t-1) \ge \ell$. So

$$T_i(n) \le \ell + \sum_{t=K+1}^{n} \mathbb{1}\{A_t = i,\ T_i(t-1) \ge \ell\}.$$

*Step 2 (what a pull of $i$ means).* If $A_t = i$, the index of $i$ is at least the index of $*$. With $u = t - 1$, $s = T_*(u)$ and $s_i = T_i(u)$, this reads $\bar X_{*,s} + c_{u,s} \le \bar X_{i,s_i} + c_{u,s_i}$, with $1 \le s \le u$ and $\ell \le s_i \le u$ on the event of Step 1. So

$$\mathbb{1}\{A_t = i,\ T_i(t-1) \ge \ell\} \le \sum_{s=1}^{u}\sum_{s_i=\ell}^{u} \mathbb{1}\{\bar X_{*,s} + c_{u,s} \le \bar X_{i,s_i} + c_{u,s_i}\}.$$

*Step 3 (three ways to fail).* If $\bar X_{*,s} + c_{u,s} \le \bar X_{i,s_i} + c_{u,s_i}$, then at least one of these holds:

- (a) $\bar X_{*,s} \le \mu^* - c_{u,s}$,
- (b) $\bar X_{i,s_i} \ge \mu_i + c_{u,s_i}$,
- (c) $\mu^* < \mu_i + 2c_{u,s_i}$.

Indeed, if all three fail, then $\bar X_{*,s} + c_{u,s} > \mu^* \ge \mu_i + 2c_{u,s_i} > \bar X_{i,s_i} + c_{u,s_i}$, a contradiction.

*Step 4 (rule out (c)).* For $s_i \ge \ell \ge 8\ln n/\Delta_i^2$ and $u \le n - 1 < n$, we have $2c_{u,s_i} = 2\sqrt{2\ln u / s_i} \le 2\sqrt{2\ln n \cdot \Delta_i^2 / (8\ln n)} = \Delta_i$. So $\mu_i + 2c_{u,s_i} \le \mu^*$, and (c) is false.

*Step 5 (bound (a) and (b)).* By Hoeffding, $\Pr[(a)] \le u^{-4}$ and $\Pr[(b)] \le u^{-4}$, for each fixed $u$, $s$ and $s_i$. Take expectations in Steps 1 and 2 and use the union bound over (a) and (b):

$$\mathbb{E}[T_i(n)] \le \ell + \sum_{u=K}^{n-1}\sum_{s=1}^{u}\sum_{s_i=\ell}^{u} 2u^{-4} \le \ell + \sum_{u=1}^{\infty} u^2 \cdot 2u^{-4} = \ell + 2\cdot\frac{\pi^2}{6}.$$

Since $\ell \le 8\ln n/\Delta_i^2 + 1$, this is the bound on $\mathbb{E}[T_i(n)]$.

*Step 6 (regret).* By the regret decomposition $R_n = \sum_i \Delta_i \mathbb{E}[T_i(n)]$ (see the [multi-armed bandit](/multi-armed-bandit/) page), $R_n \le \sum_{i:\Delta_i>0}\big(\frac{8\ln n}{\Delta_i} + (1 + \frac{\pi^2}{3})\Delta_i\big)$, and the terms with $\Delta_j = 0$ add nothing to the second sum. $\blacksquare$

**Remarks.**

- The bound holds for each $n$, not only in the limit, and the policy does not need $n$ or the gaps.
- The step $u < n$ in Step 4 is where the horizon enters: the threshold $\ell$ is set by $\ln n$, the largest $\ln u$ that can occur.
- The constant 8 is not tight. Lattimore and Szepesvari (Chapter 8) show that a variant with index $\bar X_i + \sqrt{2\ln f(t) / N_i}$ and $f(t) = 1 + t\ln^2 t$ has $\limsup_n \mathbb{E}[T_i(n)]/\ln n \le 2/\Delta_i^2$ for 1-subgaussian rewards; for rewards in $[0,1]$, which are $\frac12$-subgaussian, the matching index has a smaller bonus. The [Lai-Robbins lower bound](/lai-robbins-lower-bound/) shows what constant is optimal.
