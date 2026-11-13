---
title: At one level UCT is UCB1, and it tries a worse action O(log n) times in expectation
proves: [correctness]
status: full
---

We use the pseudocode of the page with $C_p = 1/\sqrt2$, so the bias term of line L5 is $2C_p\sqrt{\ln t/s} = \sqrt{2\ln t/s}$, where $t = N(s)$ is the number of earlier visits of the node and $s = N(s, a)$ the number of earlier tries of the action.

**At one level UCT is UCB1.** Let the root have $K$ children that are leaves, and let a leaf $j$ give independent rewards in $[0, 1]$ with mean $\mu_j$. In iteration $t + 1$ (with $t = 0, 1, \ldots$) the root has $N = t$. Line L4 tries the actions $1, \ldots, K$ in order in the first $K$ iterations. After that, line L5 picks the action with the largest $\bar X_j + \sqrt{2 \ln t / N_j}$, where $\bar X_j$ is the mean reward and $N_j$ the count of action $j$ (line L8). This is the rule of UCB1 of Auer, Cesa-Bianchi and Fischer (2002), with the same order of draws, so the two produce the same sequence of actions. The tests check this on 300 random bandits.

**Theorem.** Let $\mu^* = \max_j \mu_j$ and let $j$ be an action with $\Delta_j = \mu^* - \mu_j > 0$. After $n$ iterations, the expected number of tries of $j$ satisfies

$$\mathbb E[N_j(n)] \le \frac{8 \ln n}{\Delta_j^2} + 1 + \frac{\pi^2}{3}.$$

*Proof.* Fix an optimal action $*$. Write $\bar X_{i,s}$ for the mean of the first $s$ rewards of action $i$ and $c_{t,s} = \sqrt{2\ln t/s}$. Let $\ell = \lceil 8\ln n/\Delta_j^2\rceil$. Action $j$ is tried at most $\ell$ times while $N_j < \ell$, and each later try at a time $t + 1$ with $K \le t < n$ needs $\bar X_{*,N_*} + c_{t,N_*} \le \bar X_{j,N_j} + c_{t,N_j}$ with $N_j \ge \ell$. So

$$N_j(n) \le \ell + \sum_{t=K}^{n-1} \mathbb 1\Big[\min_{1 \le s < t+1} \big(\bar X_{*,s} + c_{t,s}\big) \le \max_{\ell \le s' < t+1} \big(\bar X_{j,s'} + c_{t,s'}\big)\Big] \le \ell + \sum_{t \ge 1}\sum_{s=1}^{t}\sum_{s'=\ell}^{t} \mathbb 1\big[\bar X_{*,s} + c_{t,s} \le \bar X_{j,s'} + c_{t,s'}\big].$$

If $\bar X_{*,s} + c_{t,s} \le \bar X_{j,s'} + c_{t,s'}$, then at least one of these holds:

(a) $\bar X_{*,s} \le \mu^* - c_{t,s}$; (b) $\bar X_{j,s'} \ge \mu_j + c_{t,s'}$; (c) $\mu^* < \mu_j + 2c_{t,s'}$.

Indeed, if all three fail, then $\bar X_{*,s} + c_{t,s} > \mu^* \ge \mu_j + 2c_{t,s'} > \bar X_{j,s'} + c_{t,s'}$. For $s' \ge \ell$ and $t \le n$, $2c_{t,s'} = 2\sqrt{2\ln t/s'} \le 2\sqrt{2\ln n/\ell} \le \Delta_j$, so (c) fails. By Hoeffding's inequality ([Hoeffding inequality](/hoeffding-inequality/)) for $s$ independent rewards in $[0, 1]$,

$$\Pr[\text{(a)}] \le e^{-2 s c_{t,s}^2} = e^{-4\ln t} = t^{-4}, \qquad \Pr[\text{(b)}] \le t^{-4}.$$

Taking expectations,

$$\mathbb E[N_j(n)] \le \ell + \sum_{t \ge 1} \sum_{s=1}^{t}\sum_{s'=1}^{t} 2t^{-4} \le \frac{8\ln n}{\Delta_j^2} + 1 + \sum_{t\ge1} 2t^{-2} = \frac{8\ln n}{\Delta_j^2} + 1 + \frac{\pi^2}{3}. \qquad \blacksquare$$

**Consequences at the root.** The expected regret after $n$ iterations, $\sum_j \Delta_j\,\mathbb E[N_j(n)]$, is $O(\sum_{j:\Delta_j>0} \ln n/\Delta_j)$. And since the tries of every worse action are $O(\ln n)$ in expectation, the mean reward of the root, $\sum_j N_j \bar X_j / n$, converges to $\mu^*$.

**Deeper trees.** Below the root the rewards that a node passes to its parent are not identically distributed, because the policy below it keeps changing. Kocsis and Szepesvári (2006) handle this drift (their Theorems 1 to 5) and obtain Theorem 6 for trees of depth $D$; this file does not reprove it. For a finite tree with fixed payoffs, a complete proof that the search returns a minimax move once $n$ is large enough is on the page [Monte Carlo tree search](/monte-carlo-tree-search/): the same argument applies here, since this UCT stores every node on its path, tries new actions in a fixed order and is then deterministic. The only change is that every visit of a node continues to a child, so $N(u) = \sum_c N(c)$ replaces equation (1) there.
