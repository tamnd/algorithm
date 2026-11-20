---
title: The Kurganov-Tadmor scheme is conservative and consistent, and for a scalar law with one global speed and the minmod-theta slope it is TVD under a Courant condition
proves: [correctness]
status: full
---

**Setting.** The scheme stores cell averages $u_j$ on a uniform grid with width $\Delta x$. Lines L2 to L6 of the page compute the slope $s_j = \mathrm{minmod}\big(\theta\Delta_{j-1/2}, \tfrac12(\Delta_{j-1/2} + \Delta_{j+1/2}), \theta\Delta_{j+1/2}\big)$ with $\Delta_{j+1/2} = u_{j+1} - u_j$ and $1 \le \theta \le 2$, the face values $u^-_{j+1/2} = u_j + \frac12 s_j$ and $u^+_{j+1/2} = u_{j+1} - \frac12 s_{j+1}$, a speed $a_{j+1/2}$, the face flux

$$H_{j+1/2} = \tfrac12\big(f(u^+_{j+1/2}) + f(u^-_{j+1/2})\big) - \tfrac12 a_{j+1/2}\big(u^+_{j+1/2} - u^-_{j+1/2}\big),$$

and the rate $L_j(u) = -(H_{j+1/2} - H_{j-1/2})/\Delta x$. Line L7 advances $du/dt = L(u)$ with forward Euler $u + \Delta t L(u)$, Heun's method or the SSP RK3 of Shu and Osher. For systems, the same lines act componentwise and $a_{j+1/2}$ is the larger spectral radius of the flux Jacobian at the two face values.

**Lemma 1 (conservation and consistency).** On a periodic grid $\sum_j L_j(u) = 0$, so each Runge-Kutta stage and the step keep $\sum_j u_j$. If $u_{j-1} = u_j = u_{j+1} = u_{j+2} = \bar u$, then $H_{j+1/2} = f(\bar u)$.

*Proof.* Each $H_{j+1/2}$ enters $L_j$ with the factor $-1/\Delta x$ and $L_{j+1}$ with $+1/\Delta x$, so the sum telescopes. Each stage is a combination of $u$ and $\Delta t L(\cdot)$ with weights that sum to 1 on the $u$ terms, so the sum of the cells is kept. For the constant data, $s_j = s_{j+1} = 0$, both face values are $\bar u$, and the diffusion term is zero. $\square$

The test checks Lemma 1 exactly in `Fraction` arithmetic for Burgers' equation with all three time steppers. By the [Lax-Wendroff theorem](/lax-wendroff-theorem/), bounded $L^1_{loc}$ limits of the scheme are weak solutions.

**Lemma 2 (the slope as a fraction of each difference).** Let $\varphi(r) = \max\big(0, \min(\theta r, \tfrac12(1 + r), \theta)\big)$. If $\Delta_{j-1/2} \ne 0$, then $s_j = \varphi(r_j)\Delta_{j-1/2}$ with $r_j = \Delta_{j+1/2}/\Delta_{j-1/2}$. In every case $s_j = p_j\Delta_{j-1/2} = q_j\Delta_{j+1/2}$ with $p_j, q_j \in [0, \theta]$, where we set $p_j = 0$ or $q_j = 0$ when the difference is zero.

*Proof.* The minmod function is odd and positively homogeneous, so dividing its three arguments by $\Delta_{j-1/2}$ gives $\varphi(r_j)$. If $r_j \le 0$, the arguments do not all have one sign and $s_j = 0$. If $r_j > 0$, then $0 < \varphi(r_j) \le \theta$, and by symmetry of the three arguments $s_j = \varphi(1/r_j)\Delta_{j+1/2}$ with $0 < \varphi(1/r_j) \le \theta$. If one difference is zero, $s_j = 0$. $\square$

**Lemma 3 (Harten 1983).** Suppose that on a periodic grid $u_j^{new} = u_j - C_{j-1/2}\Delta_{j-1/2} + D_{j+1/2}\Delta_{j+1/2}$ with $C_{j+1/2} \ge 0$, $D_{j+1/2} \ge 0$ and $C_{j+1/2} + D_{j+1/2} \le 1$ for all $j$. Then $TV(u^{new}) \le TV(u)$, where $TV(u) = \sum_j |\Delta_{j+1/2}|$. If also $C_{j-1/2} + D_{j+1/2} \le 1$ for all $j$, then $\min_k u_k \le u_j^{new} \le \max_k u_k$.

*Proof.* Subtract the formulas for cells $j + 1$ and $j$:

$$u_{j+1}^{new} - u_j^{new} = (1 - C_{j+1/2} - D_{j+1/2})\Delta_{j+1/2} + C_{j-1/2}\Delta_{j-1/2} + D_{j+3/2}\Delta_{j+3/2}.$$

All three coefficients are nonnegative. Take absolute values, sum over $j$ and shift the indices of the last two sums. The coefficients of each $|\Delta_{j+1/2}|$ add up to 1. For the second claim, $u_j^{new} = (1 - C_{j-1/2} - D_{j+1/2})u_j + C_{j-1/2}u_{j-1} + D_{j+1/2}u_{j+1}$ is a convex combination. $\square$

**Theorem 1 (TVD with one global speed).** Let $f$ be a scalar flux and let $a_{j+1/2} = a$ for all faces, with $a \ge |f'(v)|$ for all $v$ between the smallest and the largest cell value. Let $\lambda = \Delta t/\Delta x$ and $1 \le \theta \le 2$. If $\lambda a \le 1/(2 + \theta)$, one forward Euler step is TVD and makes no new extrema. If $f(u) = cu$ with $a = |c|$, the bound $\lambda a \le 2/(2 + \theta)$ is enough. The same holds for Heun's method and for SSP RK3.

*Proof.* The face values lie between neighbor cell values, because $|s_j| \le 2\min(|\Delta_{j-1/2}|, |\Delta_{j+1/2}|)$ by Lemma 2 with $\theta \le 2$, so the face value moves at most to the neighbor. Write $g^\pm(v) = \frac12(f(v) \pm av)$. Then $H_{j+1/2} = g^+(u^-_{j+1/2}) + g^-(u^+_{j+1/2})$. On the range of the data $g^+$ has slope in $[0, a]$ and $g^-$ has slope in $[-a, 0]$. By the mean value theorem,

$$H_{j+1/2} - H_{j-1/2} = c_j\big(u^-_{j+1/2} - u^-_{j-1/2}\big) - d_j\big(u^+_{j+1/2} - u^+_{j-1/2}\big)$$

with $c_j, d_j \in [0, a]$. By Lemma 2,

$$u^-_{j+1/2} - u^-_{j-1/2} = \Delta_{j-1/2} + \tfrac12(s_j - s_{j-1}) = \Delta_{j-1/2}\big(1 + \tfrac12(p_j - q_{j-1})\big) = \beta_j\Delta_{j-1/2},$$

$$u^+_{j+1/2} - u^+_{j-1/2} = \Delta_{j+1/2} - \tfrac12(s_{j+1} - s_j) = \Delta_{j+1/2}\big(1 - \tfrac12(p_{j+1} - q_j)\big) = \gamma_j\Delta_{j+1/2},$$

with $\beta_j, \gamma_j \in [1 - \theta/2, 1 + \theta/2] \subset [0, 2]$. So the forward Euler step has the form of Lemma 3 with $C_{j-1/2} = \lambda c_j\beta_j \ge 0$ and $D_{j+1/2} = \lambda d_j\gamma_j \ge 0$. Each is at most $\lambda a(1 + \theta/2)$, so every sum of one $C$ and one $D$ is at most $\lambda a(2 + \theta) \le 1$. For $f(u) = cu$ with $c > 0$ and $a = c$, $g^- = 0$, so $D = 0$ and only $C \le \lambda a(1 + \theta/2) \le 1$ is needed; $c < 0$ is the mirror image. Lemma 3 gives both claims for forward Euler. Heun's step is $\frac12 u + \frac12\big(u^{(1)} + \Delta t L(u^{(1)})\big)$ with $u^{(1)} = u + \Delta tL(u)$, and the SSP RK3 step is built in the same way from forward Euler steps with convex weights $\frac34, \frac14$ and $\frac13, \frac23$. The total variation is convex and each forward Euler step does not raise it or the bounds, so the combinations do not either. $\square$

For linear advection the code's local speed is the constant $|c|$, so Theorem 1 covers the test `test_tvd_and_no_new_extrema_for_advection`. That test runs $\theta = 1, 1.5, 2$ at $\lambda a = 0.2$ and at the bound $2/(2 + \theta)$, with forward Euler and with Heun's method.

**What is not proved here.** With local speeds $a_{j+1/2}$ that change from face to face, the two terms of $H_{j+1/2} - H_{j-1/2}$ use different $a$, and the mean value argument above does not apply as written. The page checks TVD for Burgers' equation with local speeds on one step problem, which is a measurement. Second order accuracy for smooth solutions and the claim that the numerical viscosity does not grow as $\Delta t \to 0$ are results of Kurganov and Tadmor (2000); the tests measure both: an $L^1$ order near 2 on a smooth Euler wave, and an advection error that changes by about 1 percent when $\Delta t$ falls by a factor of 8. Positivity for the Euler equations is not proved.
