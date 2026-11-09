---
title: SAGA with step 1/(6L) converges linearly in expectation for strongly convex composite finite sums
proves: [correctness, convergence-rate]
status: full
---

**Setting.** Minimize $F(x) + \psi(x)$ over $\mathbb{R}^d$, where $F = \frac{1}{n}\sum_{i=1}^nf_i$, each $f_i$ is convex and differentiable with an $L$-Lipschitz gradient, $F$ is $\mu$-strongly convex, and $\psi$ is closed, convex and proper (possibly $0$). Let $x^*$ be the minimizer. The state at step $k$ is the point $x_k$, a table $g_1, \dots, g_n$ with $g_i = \nabla f_i(\phi_i)$ for stored points $\phi_i$, and the average $\bar{g} = \frac{1}{n}\sum_ig_i$. Initially $\phi_i = x_0$ for all $i$. A step draws $j$ uniformly and independently of the past and sets

$$u = \nabla f_j(x_k), \quad v = u - g_j + \bar{g}, \quad g_j \leftarrow u, \quad x_{k+1} = \operatorname{prox}_{\gamma\psi}(x_k - \gamma v).$$

Write $\mathbb{E}_k$ for the expectation over $j$ given the state, and

$$B(x) = F(x) - F(x^*) - \langle\nabla F(x^*), x - x^*\rangle \ge 0, \qquad D = \frac{1}{n}\sum_i\lVert g_i - \nabla f_i(x^*)\rVert^2.$$

$B$ is the [Bregman divergence](/bregman-divergence/) of $F$ from $x^*$. When $\psi = 0$, $\nabla F(x^*) = 0$ and $B(x) = F(x) - F^*$.

**Invariant.** After every step, $\bar{g} = \frac{1}{n}\sum_i\nabla f_i(\phi_i)$, where $\phi_j$ is now $x_k$. *Proof.* The update $\bar{g} \leftarrow \bar{g} + (u - g_j)/n$ changes the sum $\sum_ig_i$ by exactly $u - g_j$, the change of entry $j$. $\square$

**Lemma 1 (unbiased).** $\mathbb{E}_kv = \nabla F(x_k)$. *Proof.* $\mathbb{E}_k\nabla f_j(x_k) = \nabla F(x_k)$ and $\mathbb{E}_kg_j = \bar{g}$. $\square$

**Lemma 2.** For every $x$, $\frac{1}{n}\sum_i\lVert\nabla f_i(x) - \nabla f_i(x^*)\rVert^2 \le 2L\,B(x)$.

*Proof.* $\phi_i(x) = f_i(x) - f_i(x^*) - \langle\nabla f_i(x^*), x - x^*\rangle$ is convex, $L$-smooth and minimized at $x^*$ with value $0$, so the descent lemma gives $\lVert\nabla\phi_i(x)\rVert^2 \le 2L\phi_i(x)$. Average over $i$; the average of the $\phi_i$ is $B$. $\square$

**Lemma 3 (variance).** $\mathbb{E}_k\lVert v - \nabla F(x^*)\rVert^2 \le 4L\,B(x_k) + 2D$.

*Proof.* $v - \nabla F(x^*) = a - (z - \mathbb{E}_kz)$ with $a = \nabla f_j(x_k) - \nabla f_j(x^*)$ and $z = g_j - \nabla f_j(x^*)$, because $\mathbb{E}_kz = \bar{g} - \nabla F(x^*)$. So $\lVert v - \nabla F(x^*)\rVert^2 \le 2\lVert a\rVert^2 + 2\lVert z - \mathbb{E}_kz\rVert^2$. Lemma 2 bounds $\mathbb{E}_k\lVert a\rVert^2$ by $2LB(x_k)$, and $\mathbb{E}_k\lVert z - \mathbb{E}_kz\rVert^2 \le \mathbb{E}_k\lVert z\rVert^2 = D$. $\square$

**Lemma 4 (distance).** $\mathbb{E}_k\lVert x_{k+1} - x^*\rVert^2 \le (1 - \gamma\mu)\lVert x_k - x^*\rVert^2 - 2\gamma(1 - 2L\gamma)B(x_k) + 2\gamma^2D$.

*Proof.* Optimality of $x^*$ gives $-\nabla F(x^*) \in \partial\psi(x^*)$, so $x^* = \operatorname{prox}_{\gamma\psi}(x^* - \gamma\nabla F(x^*))$. The [proximal operator](/proximal-operator/) is nonexpansive, so

$$\lVert x_{k+1} - x^*\rVert^2 \le \lVert x_k - x^* - \gamma(v - \nabla F(x^*))\rVert^2 = \lVert x_k - x^*\rVert^2 - 2\gamma\langle v - \nabla F(x^*), x_k - x^*\rangle + \gamma^2\lVert v - \nabla F(x^*)\rVert^2.$$

Take $\mathbb{E}_k$. By Lemma 1 the middle term becomes $-2\gamma\langle\nabla F(x_k) - \nabla F(x^*), x_k - x^*\rangle$. Strong convexity gives $F(x^*) \ge F(x_k) + \langle\nabla F(x_k), x^* - x_k\rangle + \frac{\mu}{2}\lVert x_k - x^*\rVert^2$, which rearranges to $\langle\nabla F(x_k) - \nabla F(x^*), x_k - x^*\rangle \ge B(x_k) + \frac{\mu}{2}\lVert x_k - x^*\rVert^2$. Use Lemma 3 for the last term. $\square$

**Lemma 5 (table).** $\mathbb{E}_kD_{k+1} \le (1 - \frac{1}{n})D_k + \frac{2L}{n}B(x_k)$.

*Proof.* Only entry $j$ changes, from $g_j$ to $\nabla f_j(x_k)$. Averaging over $j$, $\mathbb{E}_kD_{k+1} = D_k - \frac{1}{n}D_k + \frac{1}{n}\cdot\frac{1}{n}\sum_j\lVert\nabla f_j(x_k) - \nabla f_j(x^*)\rVert^2$. Apply Lemma 2. $\square$

**Theorem.** Let $0 < \gamma \le \frac{1}{6L}$ and $\Psi_k = \lVert x_k - x^*\rVert^2 + 4\gamma^2n\,D_k$. Then

$$\mathbb{E}_k\Psi_{k+1} \le \rho\,\Psi_k, \qquad \rho = 1 - \min\Big(\gamma\mu,\ \frac{1}{2n}\Big),$$

so $\mathbb{E}\lVert x_k - x^*\rVert^2 \le \rho^k\Psi_0$, with $\Psi_0 \le \lVert x_0 - x^*\rVert^2 + 8\gamma^2nL\,B(x_0)$.

*Proof.* Add Lemma 4 and $c = 4\gamma^2n$ times Lemma 5:

$$\mathbb{E}_k\Psi_{k+1} \le (1 - \gamma\mu)\lVert x_k - x^*\rVert^2 + \Big(2\gamma^2 + c\big(1 - \tfrac{1}{n}\big)\Big)D_k - \Big(2\gamma(1 - 2L\gamma) - \frac{2Lc}{n}\Big)B(x_k).$$

The coefficient of $D_k$ is $c(\frac{1}{2n} + 1 - \frac{1}{n}) = c(1 - \frac{1}{2n})$. The coefficient of $B(x_k)$ is $-2\gamma(1 - 2L\gamma) + 8L\gamma^2 = -2\gamma(1 - 6L\gamma) \le 0$, and $B \ge 0$, so that term can be dropped. Each remaining coefficient is at most $\rho$ times the matching term of $\Psi_k$. Take full expectations and use induction. At $k = 0$ all $\phi_i = x_0$, so Lemma 2 gives $D_0 \le 2LB(x_0)$. $\blacksquare$

**Corollary (cost).** With $\gamma = \frac{1}{6L}$, $1 - \rho = \min(\frac{1}{6\kappa}, \frac{1}{2n})$ with $\kappa = L/\mu$, so $\mathbb{E}\lVert x_k - x^*\rVert^2 \le \varepsilon$ after $k \ge \max(6\kappa, 2n)\ln(\Psi_0/\varepsilon)$ steps. Each step costs one component gradient, plus $n$ for the initial table: $O((n + \kappa)\log(1/\varepsilon))$ in total.

**Remarks.** This Lyapunov argument is ours; it gives the same order as Theorem 1 of Defazio, Bach and Lacoste-Julien (2014), who state the rate $1 - \min(\frac{1}{4n}, \frac{\mu}{3L})$ for the step $1/(3L)$ with a different Lyapunov function. The tests check the invariant at every step, Lemma 1 as an identity, and the Theorem's one-step inequality $\mathbb{E}_k\Psi_{k+1} \le \rho\Psi_k$ by enumeration over all $j$ at random states, on least squares problems with and without an $\ell_1$ term, whose solutions are known from the KKT conditions. They also check $\mathbb{E}\lVert x_k - x^*\rVert^2 \le \rho^k\Psi_0$ by Monte Carlo over 60 seeds.
