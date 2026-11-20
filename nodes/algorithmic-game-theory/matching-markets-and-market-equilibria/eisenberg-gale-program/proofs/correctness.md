---
title: The Eisenberg-Gale program gives the Fisher equilibrium, and the certified mirror ascent returns it exactly
proves: [correctness, termination]
status: full
---

Fix $n$ buyers with budgets $e_i > 0$ and $m$ goods with one unit each, and linear utilities $U_i(x) = \sum_j u_{ij} x_{ij}$ with $u_{ij} \ge 0$. Every buyer likes some good and every good is liked by some buyer. Let $E = \{(i, j) : u_{ij} > 0\}$ be the edges, $f(x) = \sum_i e_i \log U_i(x)$, and $X = \{x \ge 0 : \sum_i x_{ij} \le 1 \text{ for all } j\}$.

**Claim 1 (Eisenberg and Gale).** The program $\max_{x \in X} f(x)$ has an optimum. An allocation $x \in X$ is optimal if and only if there are prices $p$ such that $(p, x)$ is a Fisher market equilibrium. The optimal utilities are unique, and the equilibrium prices are unique: $p_j = \max_i e_i u_{ij} / U^*_i$.

*Proof.* The point $x^0$ that splits each good evenly among the buyers who like it has $U_i(x^0) > 0$ for all $i$. The set $\{x \in X : f(x) \ge f(x^0)\}$ is closed (on it every $U_i$ is bounded below by a positive number, since every other term of $f$ is bounded above) and bounded, and $f$ is continuous there, so an optimum exists. The constraints are linear, so the KKT conditions are necessary and sufficient for optimality of the concave objective: $x$ is optimal if and only if there is $p \ge 0$ with

(K1) $p_j > 0 \implies \sum_i x_{ij} = 1$; (K2) $e_i u_{ij} / U_i \le p_j$ for all $i, j$; (K3) $x_{ij} > 0 \implies e_i u_{ij} / U_i = p_j$.

*KKT implies equilibrium.* By (K2), $u_{ij} / p_j \le U_i / e_i$ for every good, so $\alpha_i = U_i / e_i$ bounds the bang per buck, and by (K3) every good that $i$ buys reaches it. Multiplying (K3) by $x_{ij}$ and summing gives $\sum_j p_j x_{ij} = (e_i / U_i) \sum_j u_{ij} x_{ij} = e_i$. A buyer with linear utility who spends her whole budget on goods of maximum bang per buck has an optimal bundle, since any bundle of cost at most $e_i$ gives utility at most $\alpha_i e_i$. Every good $j$ is liked by some $i$, so $p_j \ge e_i u_{ij} / U_i > 0$, and by (K1) it is sold completely. So $(p, x)$ is an equilibrium.

*Equilibrium implies KKT.* Let $(p, x)$ be an equilibrium. Every good is liked by someone, so every price is positive (a free good would be demanded without limit), and every good is sold completely, which is (K1). Buyer $i$ spends $e_i$ only on goods of maximum bang per buck $\alpha_i$, so $U_i = \alpha_i e_i$. Then $e_i u_{ij} / U_i = u_{ij} / \alpha_i \le p_j$, with equality when $x_{ij} > 0$; these are (K2) and (K3). So $x$ is optimal, with multipliers $p$.

*Uniqueness.* If $x$ and $x'$ are both optimal with $U(x) \ne U(x')$, then $(x + x')/2$ is feasible and, because $\log$ is strictly concave, has a strictly larger objective. So $U^* = U(x)$ is the same for all optimal $x$. For each good $j$, some buyer buys it, and by (K2) and (K3) $p_j = \max_i e_i u_{ij} / U^*_i$. $\square$

**Claim 2 (the step of line L5).** For $x > 0$ on $E$ and $\eta > 0$, the vector $y$ of line L5 is the unique maximizer of $\Psi(y) = g \cdot y - \mathrm{KL}(y \| x) / \eta$ over $\Delta = \{y \ge 0 \text{ on } E : \sum_i y_{ij} = 1 \text{ for all } j\}$, where $\mathrm{KL}(y \| x) = \sum_{(i, j) \in E} y_{ij} \log(y_{ij} / x_{ij})$, and for every $z \in \Delta$,
$$
g \cdot (z - y) \le \big(\mathrm{KL}(z \| x) - \mathrm{KL}(z \| y) - \mathrm{KL}(y \| x)\big) / \eta .
$$

*Proof.* $\Psi$ splits into one strictly concave function per good. Setting the derivative of the Lagrangian to $0$ gives $y_{ij} \propto x_{ij} e^{\eta g_{ij}}$, which is line L5; it is positive, so it is the maximizer. The first-order condition at $y$ is $g_{ij} - (\log(y_{ij}/x_{ij}) + 1)/\eta = \mu_j$ for a constant $\mu_j$ per good, so for $z \in \Delta$, $\eta g \cdot (z - y) = \sum_{ij} (z_{ij} - y_{ij}) \log(y_{ij} / x_{ij})$, since $\sum_i (z_{ij} - y_{ij}) = 0$ kills the constants. Expanding the three KL terms shows that the right side equals the same sum. $\square$

**Claim 3 (line L6 and monotonicity).** For each $x$ with all $U_i(x) > 0$, line L6 accepts every $\eta$ below some $\eta_0(x) > 0$, and $\eta_0$ can be chosen uniformly on the set $\{x : f(x) \ge f(x^0)\}$. If line L6 accepts, then $f(y) \ge f(x)$.

*Proof.* On $\{f \ge f(x^0)\}$ every $U_i \ge u_{\min} > 0$, and every gradient entry satisfies $0 \le g_{ij} \le G = \max_{i,j} e_i u_{ij} / u_{\min}$. By line L5, $y_{ij} / x_{ij} \in [e^{-\eta G}, e^{\eta G}]$, so $\|y - x\|_1 \le m (e^{\eta G} - 1)$, and for $\eta$ small every point between $x$ and $y$ has $U_i \ge u_{\min} / 2$. There the Hessian of $f$ in direction $d$ is $-\sum_i e_i (\sum_j u_{ij} d_{ij})^2 / U_i^2 \ge -L \|d\|_1^2$ with $L = 4 \max_{i,j} e_i u_{ij}^2 / u_{\min}^2$, so $f(y) \ge f(x) + g \cdot (y - x) - \frac{L}{2} \|y - x\|_1^2$. By Pinsker's inequality on each good and the Cauchy-Schwarz inequality over the $m$ goods, $\mathrm{KL}(y \| x) \ge \|y - x\|_1^2 / (2m)$. So line L6 holds once $\eta \le 1/(mL)$ and $\eta$ is small enough for the bound on $U_i$.

If line L6 accepts, then $f(y) \ge f(x) + \eta^{-1}(\eta g \cdot (y - x) - \mathrm{KL}(y \| x)) = f(x) + \Psi(y) - \Psi(x) \ge f(x)$, because $y$ maximizes $\Psi$ and $\mathrm{KL}(x \| x) = 0$. $\square$

So every iterate stays in $\{f \ge f(x^0)\}$, and the accepted steps satisfy $\eta_t \ge \eta_{\min} = \eta_0 / 2$.

**Claim 4 (convergence of the iterates).** In exact arithmetic, $x^t$ converges to an optimal allocation $\bar{x}$.

*Proof.* At an optimum all goods are sold (Claim 1), so the optimal allocations lie in $\Delta$; let $x^*$ be one. By concavity, $f(x^*) \le f(x) + g \cdot (x^* - x)$. Adding the acceptance test of line L6 and Claim 2 with $z = x^*$ gives
$$
f(x^*) - f(y) \le g \cdot (x^* - y) + \mathrm{KL}(y \| x)/\eta \le \big(\mathrm{KL}(x^* \| x) - \mathrm{KL}(x^* \| y)\big)/\eta .
$$
So $\mathrm{KL}(x^* \| x^t)$ is nonincreasing for every optimal $x^*$, and $\sum_t \eta_t (f^* - f(x^{t+1})) \le \mathrm{KL}(x^* \| x^0)$, so $f(x^t) \to f^*$. The iterates lie in a compact set, and every limit point is optimal because $f$ is continuous there. Let $\bar{x}$ be a limit point, $x^{t_k} \to \bar{x}$. Then $\mathrm{KL}(\bar{x} \| x^{t_k}) \to 0$ (the terms with $\bar{x}_{ij} = 0$ vanish, and the others are continuous at $\bar{x}$), and since $\mathrm{KL}(\bar{x} \| x^t)$ is nonincreasing in $t$, it tends to $0$. By Pinsker's inequality, $x^t \to \bar{x}$. $\square$

**Claim 5 (soundness of line L8).** If line L8 returns $(p, x)$, then $(p, x)$ is a Fisher market equilibrium, and $x$ is an optimal solution of the program.

*Proof.* The check accepts only positive prices with $\sum_j p_j = \sum_i e_i$ and a flow of value $\sum_i e_i$ in the network source $\to j$ (capacity $p_j$) $\to i$ (only on edges with $u_{ij} / p_j = \alpha_i$, the maximum bang per buck of $i$) $\to$ sink (capacity $e_i$). Both the source arcs and the sink arcs have total capacity $\sum_i e_i$, so all of them are saturated. Let $x_{ij}$ be the flow on $j \to i$ divided by $p_j$. Then buyer $i$ spends exactly $e_i$, only on goods of maximum bang per buck, so her bundle is optimal; and good $j$ receives $p_j$, so $\sum_i x_{ij} = 1$. All arithmetic is exact. By Claim 1, $x$ is optimal. $\square$

**Claim 6 (completeness of line L8).** Let $\bar{x}$ be the limit of Claim 4 and $\beta$ its smallest positive entry. If $\beta > 2 \cdot 10^{-14}$, line L8 returns after finitely many rounds.

*Proof.* $\bar{x}$ is optimal, so by Claim 1 it is an equilibrium allocation with the unique prices $p^*$. Let $S^* = \{(i, j) : \bar{x}_{ij} > 0\}$. On each connected part $C$ of $S^*$, every edge has $u_{ij} / p^*_j = \alpha_i$ (Claim 1, K3), so the ratios that line L8 computes along $S^*$ are consistent and proportional to $p^*$. The buyers of $C$ spend all their money on goods of $C$, and the goods of $C$ are paid for only by buyers of $C$, so the prices of $C$ add up to the budgets of its buyers. Every good is in some part, since it is sold. So the prices forced by $S^*$ are exactly $p^*$, and $p^*$ passes the check because the money flows of $\bar{x}$ saturate the network.

Pick the threshold $\delta = 10^{-k}$ with $k \le 14$ and $\delta < \beta / 2$; it exists because $\beta > 2 \cdot 10^{-14}$. By Claim 4, after some round $\|x^t - \bar{x}\|_\infty < \min(\delta, \beta - \delta)$. Then the entries of $x^t$ outside $S^*$ are below $\delta$ and those in $S^*$ are above $\beta - (\beta - \delta) = \delta$, so $\{x^t_{ij} > \delta\} = S^*$. At the next round divisible by 5, line L8 tries all thresholds from $10^{-2}$ down, and it returns at the latest at $\delta$, by Claim 5 with a correct answer. $\blacksquare$

The proofs assume exact arithmetic for the ascent. The implementation runs the ascent in floating point, with a relative slack of $10^{-12}$ in the test of line L6; this can only change which support is guessed and when, while Claim 5, which uses exact arithmetic, still guarantees that every returned answer is correct.
