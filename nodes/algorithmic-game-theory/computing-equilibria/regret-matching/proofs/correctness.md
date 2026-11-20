---
title: Regret matching is well defined, its regrets are the exact equilibrium gaps of the empirical distribution, and the unconditional version has regret at most delta sqrt(k t)
proves: [correctness]
status: full
---

Let $G$ be a finite game with players $1, \ldots, n$, pure strategy sets $S_i$ with $k_i = |S_i|$, utilities $u_i$ (maximized) and payoff ranges $\Delta_i = \max_s u_i(s) - \min_s u_i(s)$. Let $s^1, s^2, \ldots$ be the profiles that the algorithm plays, and $D^t_i(j, l) = \sum_{\tau \le t,\ s^\tau_i = j} [u_i(l, s^\tau_{-i}) - u_i(s^\tau)]$ for $j \ne l$. This file proves four claims. The almost sure convergence of the regrets of the conditional rule to 0 is the Main Theorem of Hart and Mas-Colell (2000); its proof is in their Appendix 1 and is not repeated here.

**Claim 1 (the invariant).** After line L6 of round $t$, the stored value $D_i(j, l)$ equals $D^t_i(j, l)$ for every player $i$ and every $j \ne l$.

*Proof.* By induction on $t$. Before round 1 all stored values are 0 (line L1), and $D^0_i(j, l)$ is an empty sum. Suppose the claim holds after round $t - 1$. In round $t$, line L6 adds $u_i(l, s^t_{-i}) - u_i(s^t)$ to $D_i(j, l)$ for $j = s^t_i$ and every $l \ne j$, and changes no other entry. By definition, $D^t_i(j, l) - D^{t-1}_i(j, l)$ is exactly this term when $j = s^t_i$ and 0 otherwise. $\square$

**Claim 2 (line L8 gives a distribution).** If $\mu > (k_i - 1)\Delta_i$, then in every round the vector $p_i$ of lines L7 and L8 is a probability distribution on $S_i$ with $p_i(j) > 0$, where $j = s^t_i$.

*Proof.* Each term of $D^t_i(j, l)$ is a difference of two payoffs of player $i$, so it is at most $\Delta_i$, and there are at most $t$ terms. So $0 \le \max(D^t_i(j, l), 0) / (t\mu) \le \Delta_i / \mu$ for each $l \ne j$, and by Claim 1 these are the values $p_i(l)$ of line L7. Their sum is at most $(k_i - 1)\Delta_i / \mu < 1$, so $p_i(j) = 1 - \sum_{l \ne j} p_i(l) > 0$, and all entries are nonnegative and sum to 1. $\square$

**Claim 3 (the exact gap).** Let $z_T$ be the empirical distribution returned in line L10. For every player $i$ and $j \ne l$,

$$\sum_{s \in S : s_i = j} z_T(s)\,\big[u_i(l, s_{-i}) - u_i(s)\big] = \frac{D^T_i(j, l)}{T}.$$

So $z_T$ is a correlated $\varepsilon$-equilibrium if and only if $D^T_i(j, l) \le \varepsilon T$ for all $i$ and $j \ne l$; in particular it is a correlated equilibrium if and only if all these regrets are at most 0. The same computation with $E^T_i(l) = \sum_{\tau \le T} [u_i(l, s^\tau_{-i}) - u_i(s^\tau)]$ shows that $z_T$ is a coarse correlated $\varepsilon$-equilibrium if and only if $E^T_i(l) \le \varepsilon T$ for all $i$ and $l$.

*Proof.* By definition $z_T(s) = \frac{1}{T} |\{\tau \le T : s^\tau = s\}|$. So

$$\sum_{s : s_i = j} z_T(s)\,[u_i(l, s_{-i}) - u_i(s)] = \frac{1}{T} \sum_{s : s_i = j} \ \sum_{\tau \le T : s^\tau = s} [u_i(l, s^\tau_{-i}) - u_i(s^\tau)] = \frac{1}{T} \sum_{\tau \le T : s^\tau_i = j} [u_i(l, s^\tau_{-i}) - u_i(s^\tau)],$$

because each round $\tau$ with $s^\tau_i = j$ appears exactly once, under $s = s^\tau$. The last sum is $D^T_i(j, l)$. The correlated $\varepsilon$-equilibrium condition is that the left side is at most $\varepsilon$ for all $i$ and $j \ne l$, which proves the equivalence. For the coarse version, the left side becomes $\sum_s z_T(s)[u_i(l, s_{-i}) - u_i(s)]$, and the same exchange of sums gives $E^T_i(l)/T$. $\square$

**Claim 4 (the unconditional bound).** Fix a player with $k$ actions. In each round $t$ an adversary picks a payoff vector $u_t \in \mathbb{R}^k$ whose entries lie in an interval of length $\Delta$. The player plays $p_t(l) = R_{t-1}(l)^+ / \sum_{l'} R_{t-1}(l')^+$, or the uniform distribution if all $R_{t-1}(l) \le 0$, and then sets $R_t = R_{t-1} + r_t$ with $r_t(l) = u_t(l) - \langle p_t, u_t \rangle$ and $R_0 = 0$. Then for every $t$,

$$\max_l R_t(l) = \max_l \sum_{\tau \le t} u_\tau(l) - \sum_{\tau \le t} \langle p_\tau, u_\tau \rangle \le \Delta \sqrt{k t}.$$

*Proof.* Write $x = R_{t-1}$ and $r = r_t$. First, $(x_l + r_l)^+ \le |x_l^+ + r_l|$ for each $l$: if $x_l \ge 0$ then $x_l^+ = x_l$ and $(x_l + r_l)^+ \le |x_l + r_l|$; if $x_l < 0$ then $(x_l + r_l)^+ \le r_l^+ \le |r_l| = |x_l^+ + r_l|$. Squaring and adding over $l$,

$$\|R_t^+\|^2 \le \|x^+ + r\|^2 = \|x^+\|^2 + 2\langle x^+, r \rangle + \|r\|^2 .$$

Second, $\langle x^+, r \rangle = 0$. If $x^+ = 0$ this is clear. Otherwise $p_t = x^+ / c$ with $c = \sum_l x_l^+ > 0$, and $\langle x^+, r \rangle = \sum_l x_l^+ u_t(l) - c \langle p_t, u_t \rangle = c\langle p_t, u_t \rangle - c\langle p_t, u_t \rangle = 0$. Third, $\langle p_t, u_t \rangle$ is an average of the entries of $u_t$, so it lies in the same interval of length $\Delta$, and $|r_l| \le \Delta$; so $\|r\|^2 \le k\Delta^2$. Together, $\|R_t^+\|^2 \le \|R_{t-1}^+\|^2 + k\Delta^2$, and by induction from $R_0 = 0$, $\|R_t^+\|^2 \le t k \Delta^2$. Finally $\max_l R_t(l) \le \max_l R_t(l)^+ \le \|R_t^+\| \le \Delta\sqrt{kt}$. $\square$

**Corollary (self-play with expected payoffs).** Suppose every player $i$ runs the rule of Claim 4 with $u_t(l) = u_i(l, \sigma^t_{-i})$, where $\sigma^t$ is the profile of mixed strategies of round $t$, so that $\langle p_t, u_t \rangle = u_i(\sigma^t)$. Let $\nu_T = \frac{1}{T}\sum_{t \le T} \sigma^t_1 \times \cdots \times \sigma^t_n$. Then $\nu_T$ is a coarse correlated $\varepsilon$-equilibrium with $\varepsilon = \max_i \Delta_i \sqrt{k_i / T}$.

*Proof.* The entries of $u_t$ are averages of payoffs of player $i$, so they lie in an interval of length $\Delta_i$. By linearity of expectation, $\mathbb{E}_{s \sim \nu_T}[u_i(b, s_{-i}) - u_i(s)] = \frac{1}{T} \sum_{t \le T} [u_i(b, \sigma^t_{-i}) - u_i(\sigma^t)] = R_T(b) / T$, which is at most $\Delta_i \sqrt{k_i T} / T$ by Claim 4. $\blacksquare$
