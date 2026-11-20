---
title: Proportional response is mirror descent on the Shmyrev potential and converges to the Fisher equilibrium
proves: [correctness, termination]
status: full
---

Fix $n$ buyers with budgets $e_i > 0$, $m$ goods with one unit each, and utilities $u_{ij} \ge 0$, where every buyer likes some good and every good is liked by some buyer. Let $E = \{(i, j) : u_{ij} > 0\}$. The bid set is
$$
S = \{b \ge 0 \text{ on } E : \textstyle\sum_j b_{ij} = e_i \text{ for every buyer}\},
$$
with $b_{ij} = 0$ off $E$. For $b \in S$ write $p_j(b) = \sum_i b_{ij}$, and let
$$
\Phi(b) = \sum_j p_j \log p_j - \sum_{(i, j) \in E} b_{ij} \log u_{ij}, \qquad \mathrm{KL}(a \| b) = \sum_{(i, j) \in E} a_{ij} \log \frac{a_{ij}}{b_{ij}},
$$
with $0 \log 0 = 0$. Let $S^+$ be the bids in $S$ that are positive on all of $E$. On $S^+$ every price is positive, because every good is liked by some buyer, and $\Phi$ is differentiable with $g_{ij} = \partial \Phi / \partial b_{ij} = \log p_j + 1 - \log u_{ij}$. The algorithm always terminates, since it runs $T$ rounds of finite work; the claims below are about the quality of the bids.

**Claim 1 (Shmyrev).** $\Phi$ is convex and continuous on $S$ and has a minimum there. A bid matrix $b \in S$ minimizes $\Phi$ if and only if the prices $p = p(b)$ and the allocation $x_{ij} = b_{ij} / p_j$ form a Fisher market equilibrium.

*Proof.* The function $t \log t$ is convex and continuous on $[0, \infty)$, $p_j$ is linear in $b$, and the second sum is linear, so $\Phi$ is convex and continuous on the compact set $S$ and has a minimum.

Let $b$ be a minimizer. Suppose some good $j$ has $p_j = 0$, and let $i$ like $j$. Move $\varepsilon$ from a positive bid $b_{ik}$ of buyer $i$ to $b_{ij}$. The term $p_j \log p_j$ changes by $\varepsilon \log \varepsilon$, and all other terms change by $O(\varepsilon)$, so for small $\varepsilon$ the potential goes down, which is impossible. So all prices are positive, $\Phi$ is differentiable near $b$ in $S$, and the constraints are linear, so $b$ minimizes $\Phi$ if and only if for each buyer $i$ there is $\lambda_i$ with $g_{ij} \ge \lambda_i$ for all $(i, j) \in E$, with equality when $b_{ij} > 0$. Since $g_{ij} = \log(p_j / u_{ij}) + 1$, this says that $u_{ij} / p_j \le e^{1 - \lambda_i}$ for all liked goods, with equality where buyer $i$ bids. So the condition says exactly that each buyer bids only on goods of maximum bang per buck.

If this holds, then with $x_{ij} = b_{ij} / p_j$ every good is fully allocated ($\sum_i x_{ij} = 1$), every buyer spends $\sum_j p_j x_{ij} = e_i$, and she spends only on goods of maximum bang per buck, so her bundle is optimal for her linear utility. That is an equilibrium. Conversely, at an equilibrium every price is positive (a good with price $0$ would have unbounded demand), the money $b_{ij} = p_j x_{ij}$ lies in $S$ (a buyer with positive maximum bang per buck never spends on a good she does not like) and satisfies the condition above, so it is a minimizer. $\square$

The equilibrium prices of a linear Fisher market are unique (Eisenberg and Gale). So all minimizers of $\Phi$ have the same prices $p^*$ and the same value $\Phi^*$.

**Claim 2 (one round is a mirror step).** If $b \in S^+$, the bids $b'$ of line L6 are in $S^+$, and $b'$ is the unique minimizer over $S$ of $\Psi(y) = g \cdot y + \mathrm{KL}(y \| b)$, where $g = \nabla \Phi(b)$. For every $z \in S$,
$$
g \cdot (b' - z) = \mathrm{KL}(z \| b) - \mathrm{KL}(z \| b') - \mathrm{KL}(b' \| b).
$$

*Proof.* With $p_j > 0$, line L4 gives $x_{ij} = b_{ij} / p_j > 0$ on $E$, so $v_i > 0$, and line L6 gives $b'_{ij} = e_i u_{ij} x_{ij} / v_i > 0$ on $E$ with $\sum_j b'_{ij} = e_i$. So $b' \in S^+$. $\Psi$ splits into one strictly convex function per buyer on her simplex of total $e_i$. Its minimizer satisfies $g_{ij} + \log(y_{ij} / b_{ij}) + 1 = \mu_i$ for a constant $\mu_i$ per buyer, so $y_{ij} \propto b_{ij} \exp(-g_{ij})$. Since $\exp(-g_{ij}) = \exp(-1) \, u_{ij} / p_j$, this is proportional to $u_{ij} b_{ij} / p_j = u_{ij} x_{ij}$, and after scaling to the total $e_i$ it is $b'_{ij}$. So $\log(b'_{ij} / b_{ij}) = c_i - g_{ij}$ for a constant $c_i$ per buyer. For $z \in S$,
$$
\mathrm{KL}(z \| b) - \mathrm{KL}(z \| b') - \mathrm{KL}(b' \| b) = \sum_{(i, j) \in E} (z_{ij} - b'_{ij}) \log \frac{b'_{ij}}{b_{ij}} = \sum_{(i, j) \in E} (z_{ij} - b'_{ij}) (c_i - g_{ij}) = g \cdot (b' - z),
$$
because $\sum_j (z_{ij} - b'_{ij}) = e_i - e_i = 0$ removes the constants $c_i$. $\square$

**Claim 3 (relative smoothness).** For $a \in S$ and $b \in S^+$,
$$
\Phi(a) \le \Phi(b) + \nabla \Phi(b) \cdot (a - b) + \mathrm{KL}(a \| b).
$$

*Proof.* The terms with $\log u_{ij}$ are linear and cancel in $\Phi(a) - \Phi(b) - \nabla \Phi(b) \cdot (a - b)$. Since $\sum_i (a_{ij} - b_{ij}) = p_j(a) - p_j(b)$, what remains is, with $P_j = p_j(a)$ and $Q_j = p_j(b)$,
$$
\sum_j \big(P_j \log P_j - Q_j \log Q_j - (\log Q_j + 1)(P_j - Q_j)\big) = \sum_j \Big(P_j \log \frac{P_j}{Q_j} - P_j + Q_j\Big) = \sum_j P_j \log \frac{P_j}{Q_j},
$$
because $\sum_j P_j = \sum_i e_i = \sum_j Q_j$. By the log sum inequality, $P_j \log (P_j / Q_j) \le \sum_i a_{ij} \log (a_{ij} / b_{ij})$ for each good, with $P_j = \sum_i a_{ij}$ and $Q_j = \sum_i b_{ij}$. Summing over goods gives $\mathrm{KL}(a \| b)$. $\square$

**Claim 4 (one-step inequality).** If $b \in S^+$ and $b'$ is the next bid matrix, then for every $z \in S$,
$$
\Phi(b') \le \Phi(b) + \nabla \Phi(b) \cdot (z - b) + \mathrm{KL}(z \| b) - \mathrm{KL}(z \| b').
$$

*Proof.* By Claim 3 with $a = b'$, $\Phi(b') \le \Phi(b) + g \cdot (b' - b) + \mathrm{KL}(b' \| b)$. Write $g \cdot (b' - b) = g \cdot (z - b) + g \cdot (b' - z)$ and use Claim 2; the terms $\mathrm{KL}(b' \| b)$ cancel. $\square$

**Claim 5 (monotonicity and rate).** Let $b^0 \in S^+$, for example the even split of line L1, and let $b^t$ be the bids after $t$ rounds. Then $\Phi(b^{t+1}) \le \Phi(b^t)$, and for every minimizer $b^*$ of $\Phi$, $\mathrm{KL}(b^* \| b^{t+1}) \le \mathrm{KL}(b^* \| b^t)$ and
$$
\Phi(b^T) - \Phi^* \le \frac{\mathrm{KL}(b^* \| b^0)}{T} \quad \text{for } T \ge 1 .
$$

*Proof.* By Claim 2, all $b^t$ are in $S^+$. Claim 4 with $z = b^t$ gives $\Phi(b^{t+1}) \le \Phi(b^t) - \mathrm{KL}(b^t \| b^{t+1}) \le \Phi(b^t)$. Claim 4 with $z = b^*$ and the convexity bound $\Phi(b^t) + \nabla \Phi(b^t) \cdot (b^* - b^t) \le \Phi^*$ give
$$
\Phi(b^{t+1}) - \Phi^* \le \mathrm{KL}(b^* \| b^t) - \mathrm{KL}(b^* \| b^{t+1}).
$$
The left side is at least $0$, so the KL divergence does not go up. Summing over $t = 0, \ldots, T - 1$, the right side telescopes to at most $\mathrm{KL}(b^* \| b^0)$, and since $\Phi(b^t)$ does not go up, $T (\Phi(b^T) - \Phi^*) \le \sum_{t=1}^{T} (\Phi(b^t) - \Phi^*) \le \mathrm{KL}(b^* \| b^0)$. $\square$

**Claim 6 (convergence).** The prices $p(b^t)$ converge to the equilibrium prices $p^*$, and the bids $b^t$ converge to equilibrium bids $\bar{b}$; so the allocations $x^t$ of line L4 converge to an equilibrium allocation.

*Proof.* The bids lie in the compact set $S$, and $\Phi(b^t) \to \Phi^*$ by Claim 5. Let $\bar{b}$ be a limit point, $b^{t_k} \to \bar{b}$. By continuity $\Phi(\bar{b}) = \Phi^*$, so $\bar{b}$ is a minimizer and, by Claim 1 and the uniqueness of the prices, $p(\bar{b}) = p^*$. Since every limit point of $b^t$ has the prices $p^*$ and $p$ is continuous, $p(b^t) \to p^*$.

For the bids, $\mathrm{KL}(\bar{b} \| b^{t_k}) \to 0$: the terms with $\bar{b}_{ij} = 0$ are $0$, and the others are continuous at $\bar{b}$ since $\bar{b}_{ij} > 0$. By Claim 5 with $b^* = \bar{b}$, $\mathrm{KL}(\bar{b} \| b^t)$ does not go up, so it tends to $0$. On each buyer's row, both bid vectors have the total $e_i$, and Pinsker's inequality gives $\|\bar{b}_i - b^t_i\|_1^2 \le 2 e_i \, \mathrm{KL}(\bar{b}_i \| b^t_i)$, so $b^t \to \bar{b}$. Then $x^t_{ij} = b^t_{ij} / p_j(b^t) \to \bar{b}_{ij} / p^*_j$, an equilibrium allocation by Claim 1. $\square$

**Claim 7 (the check value).** For $u_1 = (2, 1)$, $u_2 = (1, 2)$ and budgets $(1, 1)$, starting from the even split, the prices are $(1, 1)$ in every round and $b^t_{11} = 2^t / (2^t + 1)$.

*Proof.* By symmetry of the market and of the start, $b^t_{11} = b^t_{22} = a_t$ and $b^t_{12} = b^t_{21} = 1 - a_t$, so both prices are $a_t + (1 - a_t) = 1$ and $x^t = b^t$. Buyer 1 has $v_1 = 2 a_t + (1 - a_t) = 1 + a_t$, so $a_{t+1} = 2 a_t / (1 + a_t)$. With $a_0 = 1/2$ the formula holds at $t = 0$, and if $a_t = 2^t / (2^t + 1)$, then $a_{t+1} = (2^{t+1} / (2^t + 1)) / ((2^{t+1} + 1) / (2^t + 1)) = 2^{t+1} / (2^{t+1} + 1)$. $\blacksquare$

The implementation runs in floating point, so the tests compare the inequalities of Claim 5 with a small slack.
