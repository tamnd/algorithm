---
title: Rest points of tatonnement are equilibria, and when it converges
proves: [correctness]
status: full
---

Fix $m$ goods with supplies $s_j > 0$ and an excess demand function $z$ on positive price vectors with $z_j(p) \ge -s_j$. Line L5 of the algorithm maps $p$ to $F(p)$ with $F_j(p) = p_j (1 + \lambda \min(z_j(p)/s_j, 1))$ and $0 < \lambda < 1$.

**Claim 1 (positive prices).** If $p > 0$ then $F(p) > 0$. *Proof.* $z_j / s_j \ge -1$, so the factor $1 + \lambda \min(z_j/s_j, 1)$ is at least $1 - \lambda > 0$. $\square$

**Claim 2 (rest points).** For $p > 0$, $F(p) = p$ if and only if $z(p) = 0$. *Proof.* $F_j(p) = p_j$ with $p_j > 0$ holds exactly when $\min(z_j/s_j, 1) = 0$, that is, when $z_j = 0$. $\square$

**Claim 3 (output).** If line L4 returns at round $t$, then $|z_j(p)| \le \varepsilon s_j$ for every $j$, so $p$ is an $\varepsilon$-approximate equilibrium. If line L6 reports convergence, the same holds for the returned $p$. *Proof.* Both lines test exactly this condition on the returned vector. $\blacksquare$

The algorithm runs at most $T$ rounds, so it always stops. Whether it converges depends on the market, as the next claims show.

**Claim 4 (Cobb-Douglas Fisher markets).** Let buyer $i$ have budget $e_i > 0$ and spend the fixed share $a_{ij} \ge 0$ of it on good $j$, with $\sum_j a_{ij} = 1$, and let each good have supply $1$ and $c_j = \sum_i a_{ij} e_i > 0$. Then $z_j(p) = c_j / p_j - 1$, the unique equilibrium is $p = c$, and from any $p^0 > 0$ the iterates of line L5 converge to $c$. Once $p_j \ge c_j / 2$, $F_j(p) - c_j = (1 - \lambda)(p_j - c_j)$.

*Proof.* Buyer $i$ buys $a_{ij} e_i / p_j$ units of good $j$, so the demand for good $j$ is $c_j / p_j$ and $z_j = c_j / p_j - 1$, which is $0$ exactly when $p_j = c_j$. Each coordinate of $F$ depends only on its own price, so fix $j$.

If $p_j \ge c_j / 2$, then $z_j \le 1$ and $F_j(p) = p_j + \lambda p_j (c_j/p_j - 1) = p_j + \lambda (c_j - p_j)$, so $F_j(p) - c_j = (1 - \lambda)(p_j - c_j)$. The new price lies between $p_j$ and $c_j$, so it is again at least $c_j / 2$.

If $p_j < c_j / 2$, then $z_j > 1$ and $F_j(p) = (1 + \lambda) p_j$. After at most $\lceil \log_{1 + \lambda}(c_j / (2 p_j)) \rceil$ such rounds the price is at least $c_j / 2$, and it is then below $(1 + \lambda) c_j / 2 < c_j$.

After that, $|p_j - c_j|$ shrinks by the factor $1 - \lambda$ in every round, so it is at most $\varepsilon c_j$ after $O(\log(1/\varepsilon) / \lambda)$ more rounds. $\square$

**Claim 5 (the check value).** In the Fisher market with budgets $(1, 1)$, unit supplies and linear utilities $u_1 = (2, 1)$, $u_2 = (1, 2)$, with $\lambda = 1/2$ and $p^0 = (0.8, 1.4)$, the iterates are $p^t = (1 - 0.2/2^t, \; 1 + 0.4/2^t)$. *Proof.* While $1/2 < p_2 / p_1 < 2$, buyer 1 has bang per buck $2/p_1 > 1/p_2$ on good 1 and buyer 2 has $2/p_2 > 1/p_1$ on good 2, so each buyer spends her budget $1$ on her own good, and $z_j = 1/p_j - 1$. This is the case $c = (1, 1)$ of Claim 4, so $p^{t+1}_j - 1 = (p^t_j - 1)/2$ as long as $p^t_j \ge 1/2$. The formula holds at $t = 0$, and by induction for every $t$: the iterates have $p_1 \in [0.8, 1)$ and $p_2 \in (1, 1.4]$, so $p_2 / p_1 \in (1, 1.75]$ stays inside $(1/2, 2)$ and both prices stay above $1/2$. $\square$

**Claim 6 (Arrow, Block and Hurwicz).** Let $z$ be continuously differentiable on $\mathbb{R}^m_{> 0}$, homogeneous of degree $0$, satisfy Walras' law $p \cdot z(p) = 0$, and have strict gross substitutes: $\partial z_j / \partial p_k > 0$ for all $k \ne j$. Let $p^* > 0$ be an equilibrium. Then the equilibrium prices are exactly the multiples of $p^*$, and every solution of $\dot{p} = z(p)$ with $p(0) > 0$ converges to $c p^*$ with $c = \|p(0)\| / \|p^*\|$.

*Proof.* Step 1. Let $p > 0$ not be a multiple of $p^*$. Let $r = \max_j p_j / p^*_j$ and $J$ the set of goods that attain it. Then $z_j(p) < 0$ for every $j \in J$. Indeed, let $q = r p^*$, so $z(q) = z(p^*) = 0$ by homogeneity, $q_j = p_j$ for $j \in J$, and $q_k > p_k$ for $k \notin J$, a nonempty set. On the segment $q + \sigma (p - q)$, $\sigma \in [0, 1]$, the derivative of $z_j$ for $j \in J$ is $\sum_{k \notin J} (\partial z_j / \partial p_k)(p_k - q_k) < 0$, since every term has a positive derivative and a negative difference. So $z_j(p) < z_j(q) = 0$. In the same way, the goods with the smallest ratio $p_j / p^*_j$ have $z_j(p) > 0$. In particular $p$ is not an equilibrium, which proves the first statement.

Step 2. Let $V(p) = \max_j p_j / p^*_j$ and $W(p) = \min_j p_j / p^*_j$. Along a solution, $V(p(t))$ has the right derivative $\max_{j \in J} z_j(p(t)) / p^*_j$, the largest derivative among the coordinates that attain the maximum, and by Step 1 this is negative whenever $p(t)$ is not a multiple of $p^*$. So $V$ does not increase, and in the same way $W$ does not decrease. Also $\frac{d}{dt} \|p\|^2 = 2 p \cdot z(p) = 0$. Hence the solution stays in the compact set $K = \{p : W(p(0)) p^* \le p \le V(p(0)) p^*, \; \|p\| = \|p(0)\|\}$ of positive vectors, on which $z$ is $C^1$, so the solution exists for all $t \ge 0$.

Step 3. $V(p(t))$ is nonincreasing and bounded below, so it has a limit $V_\infty$. Let $\bar{p}$ be a limit point of $p(t_k)$ for some $t_k \to \infty$; it exists because $K$ is compact, and $V(\bar{p}) = V_\infty$ by continuity. Suppose $\bar{p}$ is not a multiple of $p^*$. By Step 2, the solution $\varphi$ that starts at $\bar{p}$ has $V(\varphi(\tau)) < V(\bar{p}) = V_\infty$ for some $\tau > 0$. Solutions depend continuously on the initial point, so $p(t_k + \tau) \to \varphi(\tau)$ and $V(p(t_k + \tau)) \to V(\varphi(\tau)) < V_\infty$, against $V(p(t)) \ge V_\infty$ for all $t$. So every limit point is a multiple of $p^*$ with norm $\|p(0)\|$, and the only such point is $c p^*$. A path in a compact set whose only limit point is $c p^*$ converges to it. $\square$

Discrete rules with a fixed step need more: a step that is too large can overshoot even under gross substitutes. Codenotti, McCune and Varadarajan (2005) and Cole and Fleischer (2008) prove convergence of discrete rules with suitable steps; the implementation only tests convergence on CES markets with a small step.

**Claim 7 (Scarf's economy cycles).** Let agent $j$ (indices mod 3) own one unit of good $j$ and have the Leontief utility $\min(x_j, x_{j+1})$. Then
$$
z_j(p) = \frac{p_{j-1}}{p_{j-1} + p_j} - \frac{p_{j+1}}{p_j + p_{j+1}},
$$
the equilibria are the multiples of $(1, 1, 1)$, both $\|p\|^2$ and $p_1 p_2 p_3$ are constant along $\dot{p} = z(p)$, and the additive rule $p \leftarrow p + \lambda z(p)$ satisfies $\|p + \lambda z\|^2 = \|p\|^2 + \lambda^2 \|z\|^2$.

*Proof.* Agent $j$ has income $p_j$ and buys $p_j / (p_j + p_{j+1})$ units of goods $j$ and $j + 1$. Good $j$ is bought by agents $j$ and $j - 1$, so its excess demand is $p_j / (p_j + p_{j+1}) + p_{j-1} / (p_{j-1} + p_j) - 1$, which is the formula above. For $p > 0$, $z_j(p) = 0$ means $p_{j-1}(p_j + p_{j+1}) = p_{j+1}(p_{j-1} + p_j)$, that is $p_{j-1} p_j = p_{j+1} p_j$, that is $p_{j-1} = p_{j+1}$. With three goods, these three equations say that all prices are equal. So the equilibria are exactly the multiples of $(1, 1, 1)$.

Walras' law: $p \cdot z = \sum_j p_j p_{j-1} / (p_{j-1} + p_j) - \sum_j p_j p_{j+1} / (p_j + p_{j+1}) = 0$, because the two sums are the same sum over the three pairs of neighbors. Then $\frac{d}{dt} \|p\|^2 = 2 p \cdot z = 0$, and $\|p + \lambda z\|^2 = \|p\|^2 + 2 \lambda p \cdot z + \lambda^2 \|z\|^2 = \|p\|^2 + \lambda^2 \|z\|^2$.

For the product, $\sum_j z_j / p_j = \sum_j \frac{p_{j-1}^2 - p_j^2}{p_{j-1} p_j (p_{j-1} + p_j)}$ after shifting the index of the second sum by one, and each term is $\frac{p_{j-1} - p_j}{p_{j-1} p_j} = \frac{1}{p_j} - \frac{1}{p_{j-1}}$, which sums to $0$ around the cycle. So $\frac{d}{dt} \sum_j \log p_j = \sum_j z_j / p_j = 0$.

On the sphere $\|p\| = R$ of positive vectors, the product $p_1 p_2 p_3$ has its unique maximum at the equilibrium $(R/\sqrt{3})(1, 1, 1)$, by the inequality of arithmetic and geometric means applied to $p_j^2$. A solution that starts at a positive point off the equilibrium ray keeps its norm and its smaller product, so it stays at a positive distance from every equilibrium and never converges. The additive rule increases $\|p\|^2$ by $\lambda^2 \|z\|^2 > 0$ in every round in which $p$ is not an equilibrium. $\square$
