---
title: The lottery draw is exact, wins are binomial, waits are geometric, and compensation tickets keep the share
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The effective tickets $e_c$ are non-negative rationals with a positive sum. Let $D$ be the least common multiple of their denominators, and let $E_c = D e_c$, an integer. The draw of line L4 picks $w$ uniformly from $[0, T)$ with $T = \sum_c E_c$.

**Claim 1 (the draw is exact).** Let the clients in list order be $c_1, \ldots, c_m$, and let $S_k = E_{c_1} + \cdots + E_{c_k}$, with $S_0 = 0$. Line L5 returns $c_k$ exactly when $S_{k-1} \le w < S_k$. So client $c_k$ wins with probability $E_{c_k} / T = e_{c_k} / \sum_c e_c$.

*Proof.* The sums $S_k$ do not fall, and $S_m = T > w$, so some first $k$ has $w < S_k$, and the walk stops there. For this first $k$, $w \ge S_{k-1}$. The intervals $[S_{k-1}, S_k)$ split $[0, T)$, and the $k$th has $E_{c_k}$ integers. Since $w$ is uniform on the $T$ integers of $[0, T)$, the probability is $E_{c_k} / T$. Scaling by $D$ does not change the ratio. $\square$

**Claim 2 (wins are binomial).** Assume that every client uses whole quanta, so $e_c = t_c$ at each lottery (line L8), and that the tickets do not change. Let $X$ be the number of wins of client $i$ in $n$ lotteries, and let $p = t_i / T$. Then $X \sim \mathrm{Bin}(n, p)$, $\mathbb{E}[X] = np$ and $\mathrm{Var}[X] = np(1 - p)$.

*Proof.* The draws use independent random numbers, and by Claim 1 each is won by $i$ with the same probability $p$. So $X = \sum_{r=1}^n B_r$ with independent Bernoulli($p$) variables $B_r$, which is the binomial distribution. By linearity of expectation $\mathbb{E}[X] = np$. Independent variables add their variances, and $\mathrm{Var}[B_r] = p - p^2$, so $\mathrm{Var}[X] = np(1 - p)$. $\square$

**Claim 3 (the wait is geometric).** Under the same assumptions, let $Y$ be the number of lotteries from a given lottery up to and including the next win of $i$. Then $\Pr[Y = m] = (1 - p)^{m-1} p$ for $m \ge 1$, $\mathbb{E}[Y] = 1/p$ and $\mathrm{Var}[Y] = (1 - p)/p^2$.

*Proof.* $Y = m$ exactly when $i$ loses $m - 1$ independent lotteries and wins the next one. The mean and variance are those of the geometric distribution: $\sum_{m \ge 1} m (1 - p)^{m-1} p = 1/p$, and $\mathbb{E}[Y^2] = (2 - p)/p^2$, so $\mathrm{Var}[Y] = (2 - p)/p^2 - 1/p^2 = (1 - p)/p^2$. $\square$

In particular $\Pr[Y > m] = (1 - p)^m \to 0$, so a client with $t_i \ge 1$ wins with probability 1 in finite time: it does not starve.

**Claim 4 (compensation keeps the share).** Assume each client $j$ uses the same part $f_j \in (0, 1]$ of every quantum it gets, and has run at least once. Then at each later lottery $e_j = t_j / f_j$, and the expected CPU time that client $i$ gets from one lottery is $t_i / T'$, with $T' = \sum_j t_j / f_j$. So the expected CPU rates are in the ratio of the base tickets.

*Proof.* After each run of $j$, line L7 (if $f_j < 1$) or line L8 (if $f_j = 1$) sets $e_j = t_j / f_j$, and nothing else changes $e_j$. So at each lottery the sum of the effective tickets is $T'$. By Claim 1, client $i$ wins with probability $(t_i / f_i) / T'$, and then it uses $f_i$ of a quantum. The expected CPU time is $(t_i / f_i) / T' \cdot f_i = t_i / T'$. $\square$

Without line L7, the same computation gives $f_i t_i / T$: a client that blocks early loses part of its share in proportion to $f_i$.

**Termination.** The loop of line L2 runs $n$ times. In each pass, the walk of line L5 visits at most $m$ clients and stops by Claim 1. So LOTTERY-SCHEDULE ends after $O(nm)$ steps. $\blacksquare$
