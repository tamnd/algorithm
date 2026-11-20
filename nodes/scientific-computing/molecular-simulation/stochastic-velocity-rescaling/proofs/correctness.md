---
title: The rescaling draws the exact solution of the kinetic energy equation and keeps the canonical distribution
proves: [correctness]
status: full
---

Let $K_0 = N_f k_B T / 2$, $c = e^{-h/\tau}$ and $\sigma^2 = (1 - c) K_0 / N_f$. The thermostat of Bussi, Donadio and Parrinello (2007) lets $K$ follow the stochastic differential equation
$$dK = \frac{K_0 - K}{\tau}\, dt + 2 \sqrt{\frac{K K_0}{N_f \tau}}\, dW. \qquad (1)$$

**Claim 1 (a representation of (1)).** Let $y_1, \ldots, y_{N_f}$ be independent Ornstein-Uhlenbeck processes $dy_a = -\frac{y_a}{2\tau} dt + \sqrt{\frac{K_0}{N_f \tau}}\, dB_a$. Then $K = \sum_a y_a^2$ solves (1) in law.

*Proof.* By the Ito formula,
$$dK = \sum_a \bigl(2 y_a\, dy_a + \tfrac{K_0}{N_f \tau} dt\bigr) = \frac{K_0 - K}{\tau} dt + 2\sqrt{\frac{K_0}{N_f \tau}} \sum_a y_a\, dB_a.$$
The martingale $\sum_a y_a\, dB_a$ has quadratic variation $\sum_a y_a^2\, dt = K\, dt$, so it is $\sqrt{K}\, dW$ for a Brownian motion $W$ (Levy's characterization). This gives (1). The coefficients of (1) satisfy the Yamada-Watanabe condition, so the solution is unique in law. $\square$

**Claim 2 (the exact step).** Given $K(0) = K$, the law of $K(h)$ is the law of
$$K' = \bigl(\sqrt{cK} + \sigma R_1\bigr)^2 + \sigma^2 S,$$
with $R_1$ standard normal and $S$ chi-squared with $N_f - 1$ degrees of freedom, independent. Lines L8 to L10 draw $K'$ this way.

*Proof.* The law of $(y_a)$ is invariant under rotations of $\mathbb{R}^{N_f}$, so we may start from $y(0) = (\sqrt K, 0, \ldots, 0)$. The exact Ornstein-Uhlenbeck step is $y_a(h) = e^{-h/(2\tau)} y_a(0) + s R_a$, with $s^2 = \frac{K_0}{N_f \tau} \cdot \tau (1 - e^{-h/\tau}) = \sigma^2$ and independent standard normals $R_a$. So $K(h) = (\sqrt{c K} + \sigma R_1)^2 + \sigma^2 \sum_{a \ge 2} R_a^2$, and $\sum_{a \ge 2} R_a^2$ is chi-squared with $N_f - 1$ degrees of freedom. Line L9 draws it as $2\,\Gamma((N_f - 1)/2, 1)$, which has this law. $\square$

So the rescaling has no time step error: for any $h$ and $\tau$ it draws the solution of (1) at time $h$. From Claim 2, $\mathbb{E}[K'] = cK + (1 - c)K_0$ and $\operatorname{Var}[K'] = 4cK\sigma^2 + 2N_f\sigma^4$, the values the tests check.

**Claim 3 (the canonical law of $K$ is stationary).** If $K$ has the gamma law with shape $N_f/2$ and scale $k_B T$, so does $K'$.

*Proof.* The stationary law of each $y_a$ is normal with variance $\frac{K_0/(N_f\tau)}{2 \cdot 1/(2\tau)} = K_0/N_f = k_B T/2$. So the stationary law of $K = \sum_a y_a^2$ is $\frac{k_B T}{2} \chi^2_{N_f}$, the gamma law with shape $N_f/2$ and scale $k_B T$. Under the canonical distribution, $u_{ia} = \sqrt{m_i/2}\, v_{ia}$ are independent normals with variance $k_B T/2$, and $K = \sum u_{ia}^2$ has this law. $\square$

**Claim 4 (the canonical distribution is kept).** If $(x, v)$ has the canonical density before line L7, then after line L12 it still has it.

*Proof.* Write $u$ for the vector of the $u_{ia}$, of dimension $N_f$. Under the canonical density, $x$ is independent of $u$, and $u$ is a centered normal vector with covariance $\frac{k_B T}{2} I$. So $|u|^2 = K$ and the direction $u / |u|$ are independent, and the direction is uniform on the sphere. Line L12 multiplies $u$ by $\alpha$ with $\alpha^2 = K'/K$, so the direction stays the same up to a sign that does not depend on the direction, and $K$ becomes $K'$. By Claim 3, $K'$ has the gamma law, and it is independent of the direction and of $x$. So the new $u$ has the same law as before. $\square$

The velocity Verlet part keeps the canonical density only up to its $O(h^2)$ energy error. So the sampled distribution is canonical up to the integrator error, as for the other thermostats with a Verlet step.

**Claim 5 (the effective energy).** Let $Q_n = \sum_{k \le n} (K'_k - K_k)$ be the sum of the changes of $K$ made by the thermostat in the first $n$ steps (line L13). Then $\tilde H_n = K + U - Q_n$ (line L14) changes only in the Verlet parts: $\tilde H_n - \tilde H_{n-1}$ is the change of $K + U$ in the Verlet part of step $n$.

*Proof.* In step $n$ the thermostat changes $K$ by $K'_n - K_n$ and adds the same amount to $Q$. $\square$

So a drift of $\tilde H$ measures the integration error alone, as the drift of $H$ does in a run without a thermostat.

**Claim 6 (the sign).** The sign of $\alpha$ is the sign of $\sqrt{cK} + \sigma R_1$, the first component of $y(h)$ in Claim 2. The law of $K'$ does not depend on this choice, and Claim 4 holds for either sign; the sign keeps the velocity path continuous in the limit $h \to 0$. $\square$
