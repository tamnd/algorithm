---
title: The Horn-Schunck update solves the local equations, its error never grows, and a translated quadratic image has the exact constant flow as a fixed point
proves: [correctness]
status: full
---

Fix the derivative estimates $E_x(p), E_y(p), E_t(p)$ of line L1 at each flow point $p$, and $\alpha^2 > 0$. Write $g_p = (E_x(p), E_y(p))$, $D_p = \alpha^2 + |g_p|^2$, and $w(p) = (u(p), v(p))$. The mean of line L4 is $(Aw)(p) = \sum_q a_{pq} w(q)$, where the weights $a_{pq}$ are $1/6$ or $1/12$ for the 8 neighbors, with a neighbor outside the grid replaced by the nearest point inside, so $a_{pq} \ge 0$ and $\sum_q a_{pq} = 4 \cdot \frac{1}{6} + 4 \cdot \frac{1}{12} = 1$.

The discrete equations of Horn and Schunck ask, at every point $p$, with $(\bar u, \bar v) = (Aw)(p)$,

$$
(\alpha^2 + E_x^2)\,u + E_x E_y\, v = \alpha^2 \bar u - E_x E_t, \qquad E_x E_y\, u + (\alpha^2 + E_y^2)\, v = \alpha^2 \bar v - E_y E_t. \tag{1}
$$

**Claim 1 (the local solve).** For fixed $(\bar u, \bar v)$, the pair (1) has the unique solution $u = \bar u - E_x s / D_p$, $v = \bar v - E_y s / D_p$ with $s = E_x \bar u + E_y \bar v + E_t$, which is line L6. So a field $w$ is a fixed point of lines L4 to L6 exactly when it satisfies (1) at every point.

*Proof.* The determinant of the pair is $(\alpha^2 + E_x^2)(\alpha^2 + E_y^2) - E_x^2 E_y^2 = \alpha^2(\alpha^2 + E_x^2 + E_y^2) = \alpha^2 D_p > 0$, so the solution is unique. Substituting the proposed $u$ and $v$ into the left side of the first equation gives

$$
(\alpha^2 + E_x^2)\bar u + E_x E_y \bar v - E_x \frac{s}{D_p}\big(\alpha^2 + E_x^2 + E_y^2\big) = \alpha^2 \bar u + E_x (E_x \bar u + E_y \bar v) - E_x s = \alpha^2 \bar u - E_x E_t,
$$

since $E_x \bar u + E_y \bar v = s - E_t$. The second equation follows in the same way with the roles of $x$ and $y$ exchanged. A fixed point $w$ has $w(p) = $ line L6 applied to $(Aw)(p)$ at every $p$, which by the uniqueness is the same as (1) at every $p$. $\square$

**Claim 2 (the error does not grow).** Let $w^*$ be a fixed point and $w^k$ the field after $k$ iterations from any start. Then $\max_p |w^{k+1}(p) - w^*(p)| \le \max_p |w^k(p) - w^*(p)|$, with $|\cdot|$ the Euclidean length.

*Proof.* Line L6 can be written as $w^{k+1}(p) = P_p\,(Aw^k)(p) + c_p$ with the matrix $P_p = I - g_p g_p^{\mathsf T} / D_p$ and the vector $c_p = -E_t(p)\, g_p / D_p$. The fixed point satisfies $w^*(p) = P_p (Aw^*)(p) + c_p$. Subtracting, the error $e^k = w^k - w^*$ satisfies $e^{k+1}(p) = P_p (Ae^k)(p)$, because $A$ is linear.

The matrix $P_p$ is symmetric. If $g_p = 0$ it is $I$. Otherwise it maps $g_p$ to $g_p (1 - |g_p|^2/D_p) = \frac{\alpha^2}{D_p} g_p$ and a vector orthogonal to $g_p$ to itself, so its eigenvalues are $\alpha^2 / D_p \in (0, 1)$ and $1$, and $|P_p z| \le |z|$ for every $z$.

The mean satisfies $|(Ae^k)(p)| = |\sum_q a_{pq} e^k(q)| \le \sum_q a_{pq} |e^k(q)| \le \max_q |e^k(q)|$ by the triangle inequality and $\sum_q a_{pq} = 1$, $a_{pq} \ge 0$. So $|e^{k+1}(p)| \le |(Ae^k)(p)| \le \max_q |e^k(q)|$ for every $p$. $\square$

Claim 2 shows that the iteration is stable but not, alone, that the error goes to zero; the eigenvalue 1 of $P_p$ is the aperture direction, which only the averaging can correct. Convergence to the solution of (1) is proved by Mitiche and Mansouri (2004).

**Claim 3 (exact derivatives for quadratic brightness).** Let $E(x, y, t)$ be a polynomial of degree at most 2 in $x$, $y$ and $t$, sampled as $E^0(x, y) = E(x, y, 0)$ and $E^1(x, y) = E(x, y, 1)$. Then the cube estimates of line L1 for the cube with corner $(x, y)$ equal $E_x$, $E_y$ and $E_t$ at the center $(x + 1/2, y + 1/2, 1/2)$.

*Proof.* Take $E_x$. A first difference along $x$ is $E(x + 1, y', t') - E(x, y', t') = \int_0^1 \partial_x E(x + s, y', t')\, ds$. For a polynomial of degree at most 2, $\partial_x E$ is affine, and the mean of an affine function over $s \in [0, 1]$ is its value at $s = 1/2$. So the difference equals $\partial_x E(x + 1/2, y', t')$. Line L1 averages these over the four pairs $(y', t') \in \{y, y + 1\} \times \{0, 1\}$, and the mean of an affine function over the four corners of a square is its value at the center, so the estimate is $\partial_x E(x + 1/2, y + 1/2, 1/2)$. The same argument applies to $E_y$ and $E_t$. $\square$

**Consequence (the translated quadratic).** Let $f$ be a quadratic in $(x, y)$ and $E(x, y, t) = f(x - u_0 t, y - v_0 t)$, a quadratic in $(x, y, t)$. Its derivatives satisfy $E_x u_0 + E_y v_0 + E_t = f_x u_0 + f_y v_0 - u_0 f_x - v_0 f_y = 0$ at every point, so by Claim 3 the cube estimates satisfy it too. For the constant field $w \equiv (u_0, v_0)$, the mean is $(u_0, v_0)$ because the weights sum to 1, line L5 gives $r = 0$, and line L6 returns $(u_0, v_0)$. So the constant field is an exact fixed point, and by Claim 2 the largest error to it never grows from one iteration to the next.
