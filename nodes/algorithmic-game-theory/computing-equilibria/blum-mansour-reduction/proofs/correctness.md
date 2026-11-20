---
title: The swap regret of the Blum-Mansour reduction is at most the sum of the external regrets of its copies, and at most k ln k / eta + eta T / 2 with Hedge copies
proves: [correctness]
status: full
---

There are $k$ actions and $T$ rounds, and the loss vectors are $\ell_1, \ldots, \ell_T \in [0, 1]^k$, chosen by an adversary who may see the current distribution. In round $t$, copy $j$ proposes $q_{t,j}$ (line L3), the learner plays $p_t$ with $p_t = p_t Q_t$ (line L5), where row $j$ of $Q_t$ is $q_{t,j}$, and copy $j$ receives the loss vector $m_{t,j} = p_t(j)\,\ell_t$ (line L7). Let $R^j = \sum_t q_{t,j} \cdot m_{t,j} - \min_a \sum_t m_{t,j}(a)$ be the external regret of copy $j$.

**Claim 1 (line L5 is well defined).** Every row-stochastic matrix $Q$ has a distribution $p$ with $p = pQ$. If all entries of $Q$ are positive, $p$ is unique.

*Proof.* The map $p \mapsto pQ$ sends the simplex of distributions to itself and is continuous, so it has a fixed point by Brouwer's theorem; a direct proof is that $Q - I$ has zero row sums, so $Q^\top - I$ is singular, and the Perron-Frobenius theorem gives a nonnegative null vector. If all entries are positive, the chain with transition matrix $Q$ is irreducible, and an irreducible finite chain has exactly one stationary distribution. $\square$

**Claim 2 (the split).** In every round, $p_t \cdot \ell_t = \sum_{j} q_{t,j} \cdot m_{t,j}$.

*Proof.* By line L5, $p_t(a) = \sum_j p_t(j)\, q_{t,j}(a)$ for every action $a$. So $p_t \cdot \ell_t = \sum_a \sum_j p_t(j)\, q_{t,j}(a)\, \ell_t(a) = \sum_j \sum_a q_{t,j}(a)\, m_{t,j}(a)$. $\square$

**Claim 3 (the reduction).** For every map $\delta$ from actions to actions, $R_T(\delta) = \sum_t \sum_j p_t(j)\,[\ell_t(j) - \ell_t(\delta(j))] \le \sum_j R^j$. So the swap regret is at most $\sum_j R^j$.

*Proof.* By Claim 2, $\sum_t p_t \cdot \ell_t = \sum_j \sum_t q_{t,j} \cdot m_{t,j}$. Also $\sum_t \sum_j p_t(j)\,\ell_t(\delta(j)) = \sum_j \sum_t m_{t,j}(\delta(j))$, and for each $j$ this inner sum is the total loss of the fixed action $\delta(j)$ on the losses of copy $j$, so it is at least $\min_a \sum_t m_{t,j}(a)$. Subtract the two lines: $R_T(\delta) \le \sum_j \big(\sum_t q_{t,j} \cdot m_{t,j} - \min_a \sum_t m_{t,j}(a)\big) = \sum_j R^j$. $\square$

**Claim 4 (Hedge on bounded losses).** Let Hedge with rate $\eta > 0$ play $q_t(a) \propto e^{-\eta L_{t-1}(a)}$, where $L_{t-1}(a) = \sum_{\tau < t} m_\tau(a)$, on losses $m_t \in [0, c_t]^k$. Then its external regret is at most $\ln k / \eta + (\eta / 2)\sum_t c_t^2$.

*Proof.* Let $W_t = \sum_a e^{-\eta L_t(a)}$, so $W_0 = k$. For $x \ge 0$, $e^{-x} \le 1 - x + x^2/2$. So
$$\frac{W_t}{W_{t-1}} = \sum_a q_t(a)\, e^{-\eta m_t(a)} \le 1 - \eta\, q_t \cdot m_t + \frac{\eta^2}{2} \sum_a q_t(a)\, m_t(a)^2 \le \exp\Big(-\eta\, q_t \cdot m_t + \frac{\eta^2 c_t^2}{2}\Big),$$
using $1 + y \le e^y$. Multiply over $t = 1, \ldots, T$: $W_T \le k \exp(-\eta \sum_t q_t \cdot m_t + (\eta^2/2)\sum_t c_t^2)$. Also $W_T \ge e^{-\eta L_T(a)}$ for every $a$. Take logarithms and divide by $\eta$: $\sum_t q_t \cdot m_t - L_T(a) \le \ln k/\eta + (\eta/2)\sum_t c_t^2$ for every $a$. $\square$

**Claim 5 (the bound with Hedge copies).** If every copy is Hedge with rate $\eta$, then after every round $T$ the swap regret is at most $k \ln k / \eta + \eta T / 2$. For $\eta = \sqrt{2 k \ln k / T}$ this is $\sqrt{2 T k \ln k}$.

*Proof.* Copy $j$ gets losses in $[0, p_t(j)]$, so by Claim 4, $R^j \le \ln k / \eta + (\eta/2)\sum_t p_t(j)^2$. Sum over $j$ and use $\sum_j p_t(j)^2 \le \sum_j p_t(j) = 1$: $\sum_j R^j \le k \ln k / \eta + \eta T / 2$. Claim 3 finishes the bound. With the given $\eta$, both terms equal $\sqrt{T k \ln k / 2}$. $\square$

**Claim 6 (correlated equilibria in self-play).** Let a finite game be played for $T$ rounds, let $\sigma_t$ be the profile of the distributions in round $t$, and let player $i$, with utility range $\Delta_i > 0$ and maximum utility $M_i$, receive the losses $\ell_{t}(a) = (M_i - u_i(a, \sigma_{t,-i}))/\Delta_i$. Let $z = \frac{1}{T}\sum_t \sigma_{t,1} \times \cdots \times \sigma_{t,n}$. Then for every map $\delta$ on the strategies of $i$,
$$\sum_s z(s)\,\big[u_i(\delta(s_i), s_{-i}) - u_i(s)\big] = \frac{\Delta_i}{T}\, R^i_T(\delta).$$
So if every player has swap regret at most $\varepsilon T / \Delta_i$, then $z$ is a correlated $\varepsilon$-equilibrium.

*Proof.* Under the product $\sigma_t$, the strategy of player $i$ is independent of the others, so $\sum_s \sigma_t(s)\,[u_i(\delta(s_i), s_{-i}) - u_i(s)] = \sum_j \sigma_{t,i}(j)\,[u_i(\delta(j), \sigma_{t,-i}) - u_i(j, \sigma_{t,-i})] = \Delta_i \sum_j \sigma_{t,i}(j)\,[\ell_t(j) - \ell_t(\delta(j))]$. Average over $t$. $\square$

**Conclusion.** The distributions of lines L3 to L5 are well defined (Claim 1), the swap regret is at most the sum of the copies' external regrets (Claim 3), and with Hedge copies it is at most $\sqrt{2 T k \ln k}$ (Claim 5). In self-play, the empirical distribution is a correlated $\varepsilon$-equilibrium with $\varepsilon = \max_i \Delta_i \sqrt{2 k \ln k / T}$, where $k$ is the largest number of strategies (Claim 6). $\blacksquare$
