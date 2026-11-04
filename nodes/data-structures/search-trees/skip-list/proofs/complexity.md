---
title: The expected cost of a skip list search is O(log n)
proves: [expected-time, space]
status: full
---

Fix a set of $n \ge 1$ keys and a key $k$. The levels $\ell(x)$ of the nodes are independent, with $\Pr[\ell(x) \ge i] = p^{i-1}$ for $1 \le i \le M$ and a constant $0 < p < 1$. Ignore the cap $M$ first; it only makes levels smaller. The cost of a search is the number of moves: the moves to the right in line L3 and the moves down in line L2. Insert and delete do one search and then $O(\ell(z))$ or $O(\ell(x))$ more work, and $\mathbb{E}[\ell(x)] = 1/(1-p)$, so it is enough to bound the search.

**Space.** The node $x$ has $\ell(x)$ pointers, and $\mathbb{E}[\ell(x)] = \sum_{i \ge 1} \Pr[\ell(x) \ge i] = \sum_{i \ge 1} p^{i-1} = 1/(1-p)$. So the expected number of pointers is $n/(1-p)$.

**Number of levels.** Let $N_i$ be the number of nodes with level $\ge i$, so $\mathbb{E}[N_i] = n p^{i-1}$. The top level $S.level$ is at most $L + \sum_{i > L} [N_i \ge 1]$ for each $L$, and $[N_i \ge 1] \le N_i$.

**The backward walk.** Reverse the search path: start at the node where the search ends at level 1, and walk back to the header at level $S.level$. At a node $y$ on level $i$ of the path, the previous step of the search was either a move down into level $i$ at $y$, which happens exactly when $\ell(y) > i$ or $y$ is the header, or a move right into $y$ along level $i$. For $y$ a node, the backward walk at $y$ has seen only the fact that $\ell(y) \ge i$ (and facts about other nodes), so, by independence, $\Pr[\ell(y) > i \mid \text{the walk so far}] = p$. So each backward step is a move up with probability at least $p$ (exactly $p$ at a node, 1 at the header), independent of the past.

**Climbing to level $L$.** Let $L = \lceil \log_{1/p} n \rceil$, so $p^{L} \le 1/n$ and $n p^{L-1} \le 1/p$. The backward steps taken while the walk is below level $L$ are dominated by the number of trials needed to get $L - 1$ successes, each trial a success with probability $p$. This number has expectation $(L - 1)/p$.

**The levels from $L$ up.** On level $i \ge L$, the moves to the right are at most $N_i$, since each visits a different node of level $\ge i$. The moves down from levels above $L$ are at most the number of levels above $L$, which is at most $\sum_{i > L} N_i$. So the expected number of steps at levels $\ge L$ is at most
$$\sum_{i \ge L} \mathbb{E}[N_i] + \sum_{i > L} \mathbb{E}[N_i] \le 2 \sum_{i \ge L} n p^{i-1} = \frac{2 n p^{L-1}}{1-p} \le \frac{2}{p(1-p)}.$$

**Total.** The expected cost of a search is at most
$$\frac{L - 1}{p} + \frac{2}{p(1-p)} \le \frac{\log_{1/p} n}{p} + \frac{2}{p(1-p)} = O(\log n)$$
for constant $p$. For $p = 1/2$ this is $2 \lg n + 8$. The cap $M$ can only lower the levels; if $M \ge L$, the bound on the climb holds unchanged, and the steps at levels $\ge L$ are bounded as before. $\blacksquare$

**Remarks.** The bound holds for each set of keys and each query, because the only randomness is in the levels. With $p = 1/4$ the bound is $4 \log_4 n + 32/3 = 2 \lg n + O(1)$, the same leading term as $p = 1/2$, with $4/3$ instead of $2$ pointers per node on average.
