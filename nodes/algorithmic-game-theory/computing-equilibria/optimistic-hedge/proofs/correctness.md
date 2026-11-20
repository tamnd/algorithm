---
title: Optimistic Hedge satisfies the RVU bound, and in self-play the sum of the regrets is at most n ln k / eta + n eta
proves: [correctness]
status: full
---

There are $k$ actions and loss vectors $\ell_1, \ell_2, \ldots \in [0, 1]^k$, and $\ell_0 = 0$. Write $L_t = \ell_1 + \cdots + \ell_t$ and $L_0 = 0$. Let $\Delta$ be the simplex of distributions on the actions and $R(x) = \sum_a x(a) \ln x(a)$ the negative entropy, with $0 \ln 0 = 0$. For a vector $c$, let $\operatorname{sm}(c)$ be the distribution with $\operatorname{sm}(c)(a) \propto e^{-c(a)}$.

**Claim 1 (closed form).** The distribution $x_t$ played in round $t$ is $x_t = \operatorname{sm}(\eta(L_{t-1} + \ell_{t-1}))$.

*Proof.* By induction on $t$. For $t = 1$, line L1 gives the uniform distribution, which is $\operatorname{sm}(0)$. Line L6 multiplies the weight of $a$ by $e^{-\eta(2\ell_t(a) - \ell_{t-1}(a))}$ (line L8 makes $m = \ell_{t-1}$), and line L7 rescales all weights by the same factor, which does not change $\operatorname{sm}$. The exponent becomes $\eta(L_{t-1} + \ell_{t-1} + 2\ell_t - \ell_{t-1}) = \eta(L_t + \ell_t)$. $\square$

**Claim 2 (softmax is the regularized minimizer).** For every vector $c$, $\operatorname{sm}(c)$ is the unique minimizer over $\Delta$ of $\varphi(x) = \langle x, c \rangle + R(x)$, and for every $y \in \Delta$, $\varphi(y) - \varphi(\operatorname{sm}(c)) \ge \frac{1}{2}\|y - \operatorname{sm}(c)\|_1^2$.

*Proof.* Let $x^* = \operatorname{sm}(c)$, so $x^*(a) = e^{-c(a)}/Z$ with $Z = \sum_b e^{-c(b)}$, and $c(a) = -\ln x^*(a) - \ln Z$. Then for $y \in \Delta$,
$$\varphi(y) = \sum_a y(a)\big(-\ln x^*(a) - \ln Z\big) + \sum_a y(a) \ln y(a) = \mathrm{KL}(y \,\|\, x^*) - \ln Z,$$
and $\varphi(x^*) = -\ln Z$. So $\varphi(y) - \varphi(x^*) = \mathrm{KL}(y \,\|\, x^*) \ge \frac{1}{2}\|y - x^*\|_1^2$ by Pinsker's inequality, and the difference is 0 only for $y = x^*$. $\square$

Define the Hedge iterates $y_t = \operatorname{sm}(\eta L_{t-1})$, and the functions $\Phi_t(x) = \eta \langle x, L_t \rangle + R(x)$ and $\Psi_t(x) = \eta\langle x, L_{t-1} + \ell_{t-1} \rangle + R(x)$. By Claims 1 and 2, $y_{t+1}$ minimizes $\Phi_t$ and $x_t$ minimizes $\Psi_t$. Note $\Phi_t = \Psi_t + \eta\langle \cdot, \ell_t - \ell_{t-1}\rangle$ and $\Psi_t = \Phi_{t-1} + \eta\langle \cdot, \ell_{t-1}\rangle$.

**Claim 3 (one step).** For every $t \ge 1$,
$$\eta\big(\langle x_t - y_{t+1}, \ell_{t-1} \rangle + \langle y_{t+1}, \ell_t \rangle\big) \le \Phi_t(y_{t+1}) - \Phi_{t-1}(y_t) - \tfrac{1}{2}\|x_t - y_t\|_1^2 - \tfrac{1}{2}\|y_{t+1} - x_t\|_1^2 .$$

*Proof.* By Claim 2 applied to $\Psi_t$ with minimizer $x_t$, and to $\Phi_{t-1}$ with minimizer $y_t$,
$$\Phi_t(y_{t+1}) = \Psi_t(y_{t+1}) + \eta\langle y_{t+1}, \ell_t - \ell_{t-1} \rangle \ge \Psi_t(x_t) + \tfrac{1}{2}\|y_{t+1} - x_t\|_1^2 + \eta\langle y_{t+1}, \ell_t - \ell_{t-1} \rangle,$$
$$\Psi_t(x_t) = \Phi_{t-1}(x_t) + \eta\langle x_t, \ell_{t-1}\rangle \ge \Phi_{t-1}(y_t) + \tfrac{1}{2}\|x_t - y_t\|_1^2 + \eta\langle x_t, \ell_{t-1}\rangle.$$
Combine the two lines and rearrange; $\langle x_t, \ell_{t-1}\rangle + \langle y_{t+1}, \ell_t - \ell_{t-1}\rangle$ is the left side divided by $\eta$. $\square$

**Claim 4 (the RVU bound).** For every $T \ge 1$ and every action $u$,
$$\sum_{t=1}^T \langle x_t, \ell_t \rangle - L_T(u) \le \frac{\ln k}{\eta} + \eta \sum_{t=1}^T \|\ell_t - \ell_{t-1}\|_\infty^2 - \frac{1}{8\eta}\sum_{t=2}^T \|x_t - x_{t-1}\|_1^2,$$
and also the regret is at most $\ln k/\eta + (\eta/2)\sum_{t=1}^T \|\ell_t - \ell_{t-1}\|_\infty^2$.

*Proof.* Split $\langle x_t, \ell_t \rangle = \langle x_t - y_{t+1}, \ell_t - \ell_{t-1}\rangle + \langle x_t - y_{t+1}, \ell_{t-1} \rangle + \langle y_{t+1}, \ell_t \rangle$. Sum Claim 3 over $t = 1, \ldots, T$; the right side telescopes to $\Phi_T(y_{T+1}) - \Phi_0(y_1) \le \Phi_T(e_u) - \min R = \eta L_T(u) - \min R$, where $e_u$ is the point mass on $u$, $R(e_u) = 0$, and $\Phi_0 = R$. Since $\min_\Delta R = -\ln k$,
$$\sum_t \langle x_t, \ell_t \rangle - L_T(u) \le \frac{\ln k}{\eta} + \sum_t \langle x_t - y_{t+1}, \ell_t - \ell_{t-1}\rangle - \frac{1}{2\eta}\sum_t \big(\|x_t - y_t\|_1^2 + \|y_{t+1} - x_t\|_1^2\big).$$
By Hoelder, $\langle x_t - y_{t+1}, \ell_t - \ell_{t-1} \rangle \le \|x_t - y_{t+1}\|_1 \|\ell_t - \ell_{t-1}\|_\infty$. With $ab \le \frac{\eta}{2}b^2 + \frac{1}{2\eta}a^2$ this gives the second bound at once. With $ab \le \eta b^2 + \frac{1}{4\eta}a^2$ instead, the regret is at most
$$\frac{\ln k}{\eta} + \eta\sum_t \|\ell_t - \ell_{t-1}\|_\infty^2 - \frac{1}{4\eta}\sum_{t=1}^T\big(\|x_t - y_t\|_1^2 + \|y_{t+1} - x_t\|_1^2\big).$$
For $t \ge 2$, $\|x_t - x_{t-1}\|_1^2 \le 2\|x_t - y_t\|_1^2 + 2\|y_t - x_{t-1}\|_1^2$, and summing over $t = 2, \ldots, T$ uses each term of the last sum at most once. So the last sum is at least $\frac{1}{2}\sum_{t=2}^T \|x_t - x_{t-1}\|_1^2$, which gives the RVU bound. $\square$

**Claim 5 (adversarial losses).** Against every adversary, the regret is at most $\ln k / \eta + \eta T/2$; for $\eta = \sqrt{2 \ln k / T}$ it is at most $\sqrt{2 T \ln k}$.

*Proof.* The losses are in $[0, 1]$, so $\|\ell_t - \ell_{t-1}\|_\infty \le 1$. Use the second bound of Claim 4. $\square$

**Claim 6 (self-play).** Let $n \ge 2$ players of a finite game, each with at most $k$ strategies, run optimistic Hedge with the same $\eta \le 1/(\sqrt{8}(n-1))$, where player $i$ gets the loss vector $\ell^i_t(a) = (M_i - u_i(a, x^{-i}_t))/\Delta_i$, with $M_i$ the largest utility, $\Delta_i > 0$ the range of $u_i$, and $x^{-i}_t$ the product of the other players' distributions. Then for every $T$, $\sum_i \text{Reg}^i_T \le n \ln k/\eta + n\eta$.

*Proof.* The losses are in $[0, 1]$. For a function $f$ with values in $[0, 1]$ and two distributions $p, q$, $|\mathbb{E}_p f - \mathbb{E}_q f| \le \|p - q\|_1$. Change the opponents' distributions one at a time from round $t - 1$ to round $t$: each change of a product in one coordinate $j$ changes $\ell^i(a)$ by at most $\|x^j_t - x^j_{t-1}\|_1$. So $\|\ell^i_t - \ell^i_{t-1}\|_\infty \le \sum_{j \ne i}\|x^j_t - x^j_{t-1}\|_1$ for $t \ge 2$, and by the Cauchy-Schwarz inequality its square is at most $(n-1)\sum_{j \ne i}\|x^j_t - x^j_{t-1}\|_1^2$. For $t = 1$, $\|\ell^i_1 - \ell^i_0\|_\infty^2 \le 1$. Sum Claim 4 over the players:
$$\sum_i \text{Reg}^i_T \le \frac{n \ln k}{\eta} + n\eta + \sum_{t=2}^T \Big(\eta(n-1)^2 - \frac{1}{8\eta}\Big)\sum_j \|x^j_t - x^j_{t-1}\|_1^2,$$
since each $j$ appears for $n - 1$ players $i$. For $\eta \le 1/(\sqrt{8}(n-1))$ the bracket is at most 0. $\square$

**Claim 7 (zero-sum games).** In a two-player game with $u_2 = -u_1$, the sum of the two regrets equals $T/\Delta$ times the duality gap $\max_a u_1(a, \bar{x}^2) - \min_b u_1(\bar{x}^1, b)$ of the average distributions $\bar{x}^i = \frac{1}{T}\sum_t x^i_t$, where $\Delta$ is the range of $u_1$. So the averages form a $\Delta(2\ln k/\eta + 2\eta)/T$ equilibrium.

*Proof.* Write $u = u_1$, with largest value $M$ and smallest value $m = M - \Delta$. Player 2 has $M_2 = -m$. So $\Delta\,\text{Reg}^1_T = \sum_t (M - u(x^1_t, x^2_t)) - \min_a \sum_t (M - u(a, x^2_t)) = \max_a T u(a, \bar{x}^2) - \sum_t u(x^1_t, x^2_t)$, and $\Delta\,\text{Reg}^2_T = \sum_t u(x^1_t, x^2_t) - \min_b T u(\bar{x}^1, b)$, by linearity of $u$ in each distribution. Add the two lines, and use Claim 6 with $n = 2$. The duality gap is at least 0, because $\max_a u(a, \bar{x}^2) \ge u(\bar{x}^1, \bar{x}^2) \ge \min_b u(\bar{x}^1, b)$. $\square$

**Conclusion.** Lines L1 to L8 play $x_t = \operatorname{sm}(\eta(L_{t-1} + \ell_{t-1}))$ (Claim 1), the RVU bound holds after every round (Claim 4), the regret is $O(\sqrt{T \log k})$ against any adversary (Claim 5), and in self-play with $\eta \le 1/(\sqrt{8}(n-1))$ the sum of the regrets stays bounded by $n \ln k/\eta + n\eta$ for all $T$ (Claim 6). $\blacksquare$
