---
title: The binary tree counter is exact without noise, epsilon-DP, and has polylog error
proves: [correctness]
status: full
---

We use the pseudocode of the page. The stream is $\sigma(1), \ldots, \sigma(T)$ with $\sigma(t) \in \{0, 1\}$, and $L = \lfloor \log_2 T \rfloor + 1$ is the number of bits of $T$. Two streams are neighbors if they have the same length $T$ and differ at one time step (event-level, replace one item). The stream is fixed before the run starts. For $u \ge 1$ let $\mathrm{low}(u)$ be the value of the lowest one bit of $u$, and let the node closed at time $u$ be the interval $I(u) = (u - \mathrm{low}(u), u]$ of time steps. Its exact value is $n_u = \sum_{s \in I(u)} \sigma(s)$.

**Claim 1 (the count without noise).** If the noise in line L6 is 0, the output at time $t$ is $c_t = \sum_{s \le t} \sigma(s)$.

*Proof.* For $t \ge 0$ and a bit $j$ of $t$ equal to 1, let $t_j$ be $t$ with its bits below $j$ set to 0. Then the intervals $I(t_j)$, for the one bits $j$ of $t$, are disjoint and their union is $(0, t]$: going from the highest one bit down, each $I(t_j)$ starts where the one before it ends.

*Invariant.* After step $t$ (and before step 1 for $t = 0$), for each $j < L$: if bit $j$ of $t$ is 1, then $a_j = n_{t_j}$; if bit $j$ of $t$ is 0, then $a_j = 0$.

*Base.* For $t = 0$ all bits are 0, and all $a_j$ start at 0.

*Step.* Let $i$ be the lowest one bit of $t$ (line L3). Then $t - 1$ has bits $0, \ldots, i-1$ equal to 1, bit $i$ equal to 0, and the same higher bits as $t$. By the invariant at $t - 1$, the values $a_0, \ldots, a_{i-1}$ are the exact values of the nodes for these low bits, and by the first paragraph their intervals partition $(t - 2^i, t - 1]$. So line L4 sets $a_i = \sigma(t) + \sum_{s \in (t - 2^i, t-1]} \sigma(s) = n_t$, and $t_i = t$. Line L5 sets $a_j = 0$ for $j < i$, where the bits of $t$ are 0. For $j > i$ the bits of $t$ and $t - 1$ are the same, and so are $t_j$ and $(t-1)_j$, so $a_j$ stays correct. This proves the invariant.

Line L7 sums $a_j$ over the one bits $j$ of $t$, which is $\sum_j n_{t_j} = c_t$ by the partition. $\square$

With noise, line L6 adds a fresh draw $\eta_t$ to the node closed at time $t$, one time, and lines L5 and L7 only move or reuse these values. So by the same invariant, the output at time $t$ is

$$s_t = c_t + \sum_{j : \text{bit } j \text{ of } t \text{ is } 1} \eta_{t_j},$$

a sum of $\mathrm{popcount}(t)$ independent noise draws. Each output is a fixed function of the noisy node values $\hat n_u = n_u + \eta_u$ for $u \le t$.

**Claim 2 (privacy).** With $\eta_u \sim \mathrm{Lap}(L/\varepsilon)$ independent, the sequence of outputs $(s_1, \ldots, s_T)$ is $\varepsilon$-DP for event-level neighbors.

*Proof.* Let $N(\sigma) = (n_1, \ldots, n_T)$. Fix a time $s$. The nodes $u$ with $\mathrm{low}(u) = 2^i$ have disjoint intervals of length $2^i$, so $s$ lies in at most one node of each level $i$. The levels that occur for $u \le T$ are $i = 0, \ldots, L - 1$, because $2^i \le T$. So $s$ lies in at most $L$ nodes. If $\sigma$ and $\sigma'$ differ only at time $s$, then $|\sigma(s) - \sigma'(s)| \le 1$ and

$$\|N(\sigma) - N(\sigma')\|_1 = \sum_{u : s \in I(u)} |\sigma(s) - \sigma'(s)| \le L.$$

So $N$ has $\ell_1$ sensitivity at most $L$. The vector $N(\sigma) + (\eta_1, \ldots, \eta_T)$ is the Laplace mechanism with scale $L/\varepsilon$ on a function of sensitivity $L$. For each point $z \in \mathbb{R}^T$, the triangle inequality gives

$$\frac{\prod_u \exp(-|z_u - n_u(\sigma)| \varepsilon / L)}{\prod_u \exp(-|z_u - n_u(\sigma')| \varepsilon / L)} \le \exp\Big(\frac{\varepsilon}{L} \|N(\sigma) - N(\sigma')\|_1\Big) \le e^{\varepsilon},$$

so the noisy node vector is $\varepsilon$-DP. The outputs are a fixed function of it (Claim 1), so they are $\varepsilon$-DP by post-processing. $\square$

The bound $L$ is reached: for $T = 2^m$ the time $s = 1$ lies in the $L = m + 1$ nodes $I(1), I(2), I(4), \ldots, I(2^m)$.

**Claim 3 (error).** The error $s_t - c_t$ has mean 0 and variance $2\,\mathrm{popcount}(t)\,L^2/\varepsilon^2 \le 2L^3/\varepsilon^2$. For each $\beta \in (0, 1)$:

1. for one fixed $t$, $|s_t - c_t| \le L^2 \ln(L/\beta)/\varepsilon$ with probability at least $1 - \beta$;
2. for all $t \le T$ at the same time, $|s_t - c_t| \le L^2 \ln(T/\beta)/\varepsilon$ with probability at least $1 - \beta$.

*Proof.* The error is a sum of $\mathrm{popcount}(t) \le L$ independent $\mathrm{Lap}(b)$ draws with $b = L/\varepsilon$, each of mean 0 and variance $2b^2$. This gives the mean and the variance. For a Laplace draw, $P(|\eta| > b \ln(1/p)) = p$. For item 1, take $p = \beta/L$ and the union bound over the at most $L$ draws in $s_t$: with probability at least $1 - \beta$ each of them is at most $b \ln(L/\beta)$, and the sum is at most $L b \ln(L/\beta)$. For item 2, take $p = \beta/T$ and the union bound over all $T$ draws. $\square$

Chan, Shi and Song give the sharper bound $O(\varepsilon^{-1} (\log T)^{1.5} \log(1/\beta))$ for one time step, with a concentration bound for sums of Laplace variables in place of the union bound.

**Cost.** Line L4 adds at most $L$ values and line L7 adds at most $L$ values, so each step costs $O(L) = O(\log T)$ operations and one Laplace draw. The state is the $2L$ values $a_j$ and $\hat a_j$, so the extra space is $O(\log T)$. Over the whole stream the time is $O(T \log T)$.
