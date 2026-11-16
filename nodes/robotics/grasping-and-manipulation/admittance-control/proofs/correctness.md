---
title: Admittance control integrates the target dynamics and gives the series rest force
proves: [correctness]
status: full
---

We treat one axis; with diagonal targets the axes are independent, and the same arguments apply to each. Write $m = M_a$, $d = D_a$, $k = K_a$, all positive, and $h = \Delta t$. The goal $x_0$ is fixed in Parts 1 and 3 and has a bounded speed $\dot x_0$ in Part 2.

**Part 1 (rest relation).** Let $F$ and $x_0$ be constant, with $\dot x_0 = 0$. A pair $(x_c, v_c)$ is a fixed point of ADMITTANCE-STEP if and only if $v_c = 0$ and $k(x_c - x_0) = F$.

*Proof.* If the pair is fixed, line L3 gives $x_c = x_c + h v_c'$ where $v_c'$ is the new speed, so $v_c' = 0$, and since the speed is also fixed, $v_c = 0$. Line L2 then gives $h a_c = 0$, so $a_c = 0$, and line L1 gives $F - k(x_c - x_0) = 0$. The converse follows by putting $v_c = 0$ and $k(x_c - x_0) = F$ into lines L1 to L3. $\square$

**Theorem 1 (rest force against a spring wall).** Let the position loop act on the tool as a spring of stiffness $K_p$ toward $x_c$, and let the wall push with $F = -k_e(x - x_w)$ for $x > x_w$ and $F = 0$ otherwise, with $x_0 > x_w$. At a rest point of the whole loop, $x > x_w$ and the force on the wall is

$$\frac{x_0 - x_w}{1/k_e + 1/K_p + 1/k}.$$

*Proof.* At rest, the tool is in equilibrium: $K_p(x_c - x) + F = 0$. The controller is at a fixed point, so $k(x_c - x_0) = F$ by Part 1. If $x \le x_w$, then $F = 0$, so $x_c = x_0$ and $x = x_c = x_0 > x_w$, which is a contradiction. So $x > x_w$, and with $P = -F = k_e(x - x_w) > 0$, the force on the wall,

$$x_0 - x_w = (x_0 - x_c) + (x_c - x) + (x - x_w) = \frac{P}{k} + \frac{P}{K_p} + \frac{P}{k_e}.$$

Solving for $P$ gives the formula. $\square$

**Part 2 (first-order accuracy).** Let $F(t)$ and $\dot x_0(t)$ be Lipschitz functions and $x_0(t)$ their integral, and let $(x(t), v(t))$ solve $m\dot v = F - d(v - \dot x_0) - k(x - x_0)$, $\dot x = v$, with $x(0) = x_c^0$, $v(0) = v_c^0$. Let $(x_c^j, v_c^j)$ be the values after $j$ steps, where step $j$ uses $F(jh)$, $x_0(jh)$ and $\dot x_0(jh)$. Then for each $T > 0$ there are constants $h_T > 0$ and $K_T$ with $|x_c^j - x(jh)| + |v_c^j - v(jh)| \le K_T h$ for all $h \le h_T$ and $jh \le T$.

*Proof.* Write $z = (x, v)$ and $\dot z = f(t, z)$ with $f(t, z) = (v,\ (F(t) - d(v - \dot x_0(t)) - k(x - x_0(t)))/m)$. The function $f$ is Lipschitz in $z$ with some constant $L$, and the exact solution has a Lipschitz derivative, so $z((j+1)h) = z(jh) + h f(jh, z(jh)) + r_j$ with $|r_j| \le c h^2$ for a constant $c$ on $[0, T]$. The step of lines L1 to L3 is $v^{j+1} = v^j + h\,a(jh, z^j)$ and $x^{j+1} = x^j + h v^j + h^2 a(jh, z^j)$, where $a$ is the second component of $f$. So it equals the explicit Euler step plus the term $h^2 a(jh, z^j)$ in the first component. Let $\varepsilon_j = |z^j - z(jh)|$ in the sum norm. Subtracting,

$$\varepsilon_{j+1} \le (1 + hL)\varepsilon_j + c h^2 + h^2|a(jh, z^j)|.$$

As long as $\varepsilon_j \le 1$, $z^j$ stays in a bounded set, where $|a| \le A$ for a constant $A$. Then $\varepsilon_{j+1} \le (1 + hL)\varepsilon_j + (c + A)h^2$, and with $\varepsilon_0 = 0$ the discrete Gronwall bound gives $\varepsilon_j \le (c + A)h\,(e^{LT} - 1)/L$ for $jh \le T$. Choose $h_T$ so that this bound is at most 1 for $h \le h_T$. Then, by induction on $j$, the assumption $\varepsilon_j \le 1$ holds at every step, and $K_T = (c + A)(e^{LT} - 1)/L$ works. $\square$

**Theorem 2 (discrete stability of the virtual dynamics).** With $F = 0$ and a fixed goal $x_0 = 0$, the iteration of lines L1 to L3 tends to $(0, 0)$ from every start if and only if $2dh + kh^2 < 4m$.

*Proof.* Let $\alpha = dh/m > 0$ and $\beta = kh^2/m > 0$. One step maps $(x, v)$ to $v' = (1 - \alpha)v - (\beta/h)x$ and $x' = x + hv' = (1 - \beta)x + h(1 - \alpha)v$. This is the linear map with matrix

$$A = \begin{bmatrix} 1 - \beta & h(1 - \alpha) \\ -\beta/h & 1 - \alpha \end{bmatrix},$$

with trace $2 - \alpha - \beta$ and determinant $(1 - \beta)(1 - \alpha) + \beta(1 - \alpha) = 1 - \alpha$. The iteration tends to zero from every start if and only if both roots of $p(z) = z^2 - (2 - \alpha - \beta)z + (1 - \alpha)$ have modulus less than 1. By the Jury (Schur-Cohn) test for a real monic quadratic $z^2 + a_1 z + a_0$, this holds if and only if $|a_0| < 1$, $p(1) > 0$ and $p(-1) > 0$. Here $p(1) = \beta > 0$ always holds. $p(-1) = 4 - 2\alpha - \beta > 0$ is the condition $2dh + kh^2 < 4m$. Given this, $\alpha < 2 - \beta/2 < 2$, so $a_0 = 1 - \alpha$ lies in $(-1, 1)$. So the three conditions together are equivalent to $2dh + kh^2 < 4m$. $\blacksquare$

The theorem is about the virtual dynamics alone. The whole loop, with the force feedback through the environment and the position loop, has further conditions that depend on $k_e$, $K_p$ and the loop delay, and it can fail even when this condition holds.
