---
title: TR-BDF2 with gamma = 2 - sqrt(2) shares one matrix between its stages, is second order and is L-stable
proves: [correctness]
status: full
---

We use the notation of the page. For the analysis we take the scalar test equation $y' = \lambda y$ of [Dahlquist](/dahlquist-test-equation/), written in circuit form with $q(y) = y$, $f(y) = -\lambda y$, $u = 0$, and we put $z = h\lambda$. One step maps $y_n$ to $y_{n+1} = R(z)\, y_n$; $R$ is the *stability function*. For a linear circuit $C\dot x + Gx = u(t)$ with nonsingular $C$, the same results hold for each eigenvalue $\lambda$ of $-C^{-1}G$ when $C^{-1}G$ is diagonalizable, because the step is linear and commutes with the change of basis.

**Coefficients.** The BDF2 formula through the three points $t_n$, $t_n + \gamma h$, $t_n + h$ is the derivative at $t_n + h$ of the quadratic that interpolates $q$ at those points. Writing it as $q_{n+1} - d h\, q'_{n+1} = a\, q_{n+\gamma} - b\, q_n$ and asking that it be exact for $q = 1$, $q = t - t_{n+1}$ and $q = (t - t_{n+1})^2$ gives

$$a - b = 1, \qquad d = a(1 - \gamma) - b, \qquad a(1 - \gamma)^2 = b,$$

whose solution is $a = 1/(\gamma(2 - \gamma))$, $b = (1 - \gamma)^2/(\gamma(2 - \gamma))$, $d = (1 - \gamma)/(2 - \gamma)$.

**Lemma 1 (one matrix for both stages).** $d = \gamma / 2$ if and only if $\gamma^2 - 4\gamma + 2 = 0$, that is $\gamma = 2 \pm \sqrt 2$; the root in $(0, 1)$ is $\gamma = 2 - \sqrt 2$. Then the Newton matrices of the two stages, $C + (\gamma h / 2) G$ and $C + d h\, G$, are equal.

*Proof.* $(1 - \gamma)/(2 - \gamma) = \gamma/2$ is $2 - 2\gamma = 2\gamma - \gamma^2$. The Newton matrix of a stage $q(x) + \beta (f(x) - u) = \text{const}$ is $C(x) + \beta G(x)$, with $\beta = \gamma h/2$ for the trapezoidal stage and $\beta = d h$ for the BDF2 stage. $\square$

From now on $\gamma = 2 - \sqrt 2$, and $c = \gamma / 2 = 1 - 1/\sqrt 2$. Then $a = (\sqrt 2 + 1)/2$ and $b = (\sqrt 2 - 1)/2$, so $a - b = 1$ and $a + b = \sqrt 2$.

**Theorem 1 (stability function).**

$$R(z) = \frac{1 + (\sqrt 2 - 1) z}{(1 - c z)^2}, \qquad c = \frac{2 - \sqrt 2}{2}.$$

*Proof.* The trapezoidal stage gives $y_{n+\gamma} = \frac{1 + cz}{1 - cz}\, y_n$, because $\gamma z / 2 = cz$. The BDF2 stage gives $(1 - cz)\, y_{n+1} = a\, y_{n+\gamma} - b\, y_n$. So

$$R(z) = \frac{a(1 + cz) - b(1 - cz)}{(1 - cz)^2} = \frac{(a - b) + (a + b) c z}{(1 - cz)^2} = \frac{1 + \sqrt 2 c\, z}{(1 - cz)^2},$$

and $\sqrt 2\, c = \sqrt 2 - 1$. $\square$

**Theorem 2 (second order on the test equation).** $R(z) - e^z = \frac{3\sqrt 2 - 4}{6} z^3 + O(z^4)$. So the local error of one step is $\frac{3\sqrt 2 - 4}{6} h^3 y''' + O(h^4) \approx 0.0404\, h^3 y'''$ (numerical minus exact), and the error constant of the page is $k = -(3\sqrt 2 - 4)/6 \approx -0.0404$ in the convention exact minus numerical.

*Proof.* Expand $(1 - cz)^{-2} = 1 + 2cz + 3c^2 z^2 + 4c^3 z^3 + O(z^4)$ and multiply by $1 + pz$ with $p = \sqrt 2 - 1$. Use $c^2 = (3 - 2\sqrt 2)/2$ and $c^3 = (10 - 7\sqrt 2)/4$. The coefficient of $z$ is $p + 2c = (\sqrt 2 - 1) + (2 - \sqrt 2) = 1$. The coefficient of $z^2$ is $2cp + 3c^2 = (3\sqrt 2 - 4) + (9 - 6\sqrt 2)/2 = 1/2$. The coefficient of $z^3$ is $3c^2 p + 4c^3 = (15\sqrt 2 - 21)/2 + (10 - 7\sqrt 2) = (\sqrt 2 - 1)/2$. The coefficients of $e^z$ are $1, 1, 1/2, 1/6$, and $(\sqrt 2 - 1)/2 - 1/6 = (3\sqrt 2 - 4)/6$. For $y' = \lambda y$, $z^3 y_n = h^3 y'''(t_n)$. $\square$

**Theorem 3 (second order on smooth ODEs).** For $y' = F(t, y)$ with $F$ smooth and $C$ nonsingular in the circuit form, the local error of one step is $O(h^3)$, so the global error on a fixed interval is $O(h^2)$.

*Proof.* Start the step from the exact value $y(t_n)$. The trapezoidal rule has local error $O(h^3)$ for a step of $\gamma h$, so $y_{n+\gamma} = y(t_n + \gamma h) + O(h^3)$. The BDF2 formula is exact for quadratics, so with the exact values $y(t_n)$, $y(t_n + \gamma h)$ its residual at $y(t_n + h)$ is $O(h^3)$. The stage 2 equation $y_{n+1} - dh F(t_{n+1}, y_{n+1}) = a y_{n+\gamma} - b y_n$ has a Jacobian $I - dh F_y$ with a bounded inverse for small $h$, so the $O(h^3)$ perturbations in the residual and in $y_{n+\gamma}$ (multiplied by the fixed $a$) change $y_{n+1}$ by $O(h^3)$. A one-step method with local error $O(h^{p+1})$ and a Lipschitz increment has global error $O(h^p)$, see [order of accuracy](/order-of-accuracy/). $\square$

For index-1 DAEs, which is the usual case of MNA with a singular $C$, the second order of the differential and algebraic parts is shown by Bank et al. (1985) and Hosea and Shampine (1996); it is not proved here.

**Theorem 4 (L-stability).** TR-BDF2 with $\gamma = 2 - \sqrt 2$ is [A-stable](/a-stability/): $|R(z)| \le 1$ for $\operatorname{Re} z \le 0$. It is also [L-stable](/l-stability/): $R(z) \to 0$ as $z \to \infty$.

*Proof.* The only pole of $R$ is $z = 1/c > 0$, so $R$ is analytic on the closed left half plane. On the imaginary axis, $z = iy$:

$$|R(iy)|^2 = \frac{1 + p^2 y^2}{(1 + c^2 y^2)^2}.$$

With $p^2 = 3 - 2\sqrt 2$ and $c^2 = p^2/2$, put $s = (3 - 2\sqrt 2) y^2 \ge 0$; then $|R(iy)|^2 = (1 + s)/(1 + s/2)^2$, and $(1 + s/2)^2 = 1 + s + s^2/4 \ge 1 + s$. So $|R| \le 1$ on the imaginary axis. The numerator has degree 1 and the denominator degree 2, so $R(z) \to 0$ as $|z| \to \infty$, and in fact $z R(z) \to p/c^2 = 2(\sqrt 2 + 1)$. By the maximum modulus principle on the left half plane (bounded, analytic, at most 1 on the boundary and tending to 0 at infinity), $|R(z)| \le 1$ for all $\operatorname{Re} z \le 0$. $\square$

**Theorem 5 (the trapezoidal rule is A-stable but not L-stable).** The trapezoidal rule has $R_T(z) = (1 + z/2)/(1 - z/2)$, with $|R_T(z)| \le 1$ for $\operatorname{Re} z \le 0$ and $R_T(z) \to -1$ as $z \to -\infty$.

*Proof.* With $w = z/2$, $|1 + w|^2 - |1 - w|^2 = 4 \operatorname{Re} w \le 0$, so $|R_T| \le 1$. The limit is $\lim (1 + z/2)/(1 - z/2) = -1$. $\square$

So for a stiff component, $z = h\lambda \ll -1$, the trapezoidal rule multiplies the error by a number close to $-1$ at each step: the error changes sign at each step and decays slowly. This is the ringing of the page's example, where $z = -10$ gives $R_T = -2/3$ and $R = -0.2036$.

**Theorem 6 (the error estimate).** Let $F = u - f$, which equals $\dot q$ on a solution. For a smooth solution, the quantity

$$E = 2 k h \left( \frac{F_n}{\gamma} - \frac{F_{n+\gamma}}{\gamma(1 - \gamma)} + \frac{F_{n+1}}{1 - \gamma} \right)$$

equals $k h^3 \dddot q + O(h^4)$, the leading term of the local error.

*Proof.* The second divided difference of $F$ at $t_n$, $t_n + \gamma h$, $t_n + h$ is

$$F[t_n, t_n + \gamma h, t_n + h] = \frac{1}{h^2} \left( \frac{F_n}{\gamma} - \frac{F_{n+\gamma}}{\gamma(1 - \gamma)} + \frac{F_{n+1}}{1 - \gamma} \right),$$

by the formula $\sum_i F_i / \prod_{j \ne i} (t_i - t_j)$. For a smooth function it equals $\ddot F(\xi)/2 = \dddot q(\xi)/2$ for some $\xi$ in the step, so $E = 2 k h \cdot h^2 \cdot \dddot q/2 + O(h^4)$. The stage values differ from the exact ones by $O(h^3)$, so each $F_i$ and the bracket change by $O(h^3)$, and $E$, which is $2kh$ times the bracket, changes by $O(h^4)$. $\square$

The value of $k$ for general nonlinear systems, and the use of this estimate for step size control, are due to Bank et al. (1985) and analysed by Hosea and Shampine (1996). The test on this page measures the ratio of the estimate to the true error of one step on $y' = -y$; it is within 10 percent of 1 for $h \le 0.1$.
