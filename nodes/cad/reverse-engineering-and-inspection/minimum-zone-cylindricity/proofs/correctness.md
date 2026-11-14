---
title: The width for a fixed axis, the linearized radii, the feasible start of each linear program, the monotone decrease of the accepted widths, and why a step is found away from stationary axes
proves: [correctness, termination]
status: full
---

**Setup.** The data are points $q_1, \dots, q_n$ in $\mathbb{R}^3$. An axis is a line $L$ through a point $p$ with unit direction $u$. Let $\rho_i(L)$ be the distance from $q_i$ to $L$. The cylindricity in the minimum zone sense is
$$ C = \min_L W(L), \qquad W(L) = \max_i \rho_i(L) - \min_i \rho_i(L). $$
The method returns an axis $L$ and the value $W(L) \ge C$. What is proved below is that this value is the width of a true zone, that it decreases at each accepted step, and that a step is found from any axis that is not first-order stationary. That the value equals $C$ is not proved, and it is false in general.

**Lemma 1 (the zone of a fixed axis).** For a fixed axis $L$, the thinnest pair of coaxial cylinders with axis $L$ that holds the points has the radii $\min_i \rho_i(L)$ and $\max_i \rho_i(L)$, so its width is $W(L)$.

*Proof.* A point lies between the cylinders of radii $r \le R$ about $L$ exactly when $r \le \rho_i(L) \le R$. The constraints over all $i$ give $r \le \min_i \rho_i$ and $R \ge \max_i \rho_i$, and $R - r$ is least when both hold with equality. $\square$

So every value the method reports is the width of a zone that holds all points, and $W(L) \ge C$ for every $L$.

**Lemma 2 (the linearized radii).** Let $(e_1, e_2, u)$ be orthonormal, and let $q_i - p$ have the coordinates $(x_i, y_i, z_i)$ in this frame with $\rho_i = \sqrt{x_i^2 + y_i^2} > 0$. Let $L(\delta)$ be the line through $p + \delta_1 e_1 + \delta_2 e_2$ with the direction proportional to $u + \delta_3 e_1 + \delta_4 e_2$. Then
$$ \rho_i(L(\delta)) = \rho_i + g_i \cdot \delta + O(\lvert \delta \rvert^2), \qquad g_i = -\frac{1}{\rho_i} \bigl( x_i, \; y_i, \; z_i x_i, \; z_i y_i \bigr). $$

*Proof.* The plane $z = z_i$ meets $L(\delta)$ at the point $(\delta_1 + \delta_3 z_i, \delta_2 + \delta_4 z_i, z_i)$. The distance from $q_i$ to that point is $\sqrt{(x_i - \delta_1 - \delta_3 z_i)^2 + (y_i - \delta_2 - \delta_4 z_i)^2}$, and its first-order expansion is $\rho_i - (x_i (\delta_1 + \delta_3 z_i) + y_i (\delta_2 + \delta_4 z_i))/\rho_i$. The distance to the line differs from the distance to this point by $O(\lvert \delta \rvert^2)$: the line makes an angle $O(\lvert \delta \rvert)$ with $u$, so the segment in the plane $z = z_i$ is longer than the perpendicular by a factor $1/\cos$ of an angle of order $\lvert \delta \rvert$, which is $1 + O(\lvert \delta \rvert^2)$. The constants depend on $\max_i \lvert z_i \rvert$ and on $\min_i \rho_i$, and they are finite when $\rho_i > 0$ for all $i$. $\square$

**Lemma 3 (each linear program is feasible, bounded and solved).** For a box $\lvert \delta_k \rvert \le b_k$, the program
$$ \min \; R - r \quad \text{subject to} \quad r \le \rho_i + g_i \cdot \delta \le R \;\; (i = 1, \dots, n), \quad \lvert \delta_k \rvert \le b_k $$
is written in the code with $v = \delta + b \ge 0$, $R = U - P$ and $r = \Lambda + Q$ with $P, Q \ge 0$, where $U = \max_i (\rho_i + \sum_k \lvert g_{ik} \rvert b_k)$ and $\Lambda = \min_i (\rho_i - \sum_k \lvert g_{ik} \rvert b_k)$. Then the right-hand sides are $\ge 0$, so $v = 0, P = Q = 0$ is feasible; all variables are bounded; and the simplex method with Bland's least-index rule stops at an optimum.

*Proof.* The constraint $\rho_i + g_i \cdot (v - b) \le U - P$ becomes $g_i \cdot v + P \le U - \rho_i + g_i \cdot b$, and $U - \rho_i + g_i \cdot b \ge U - \rho_i - \sum_k \lvert g_{ik} \rvert b_k \ge 0$ by the choice of $U$. The other side is similar with $\Lambda$. The box gives $0 \le v_k \le 2 b_k$, and then $P \le U - \min_i (\rho_i + g_i \cdot \delta)$ and $Q \le \max_i(\rho_i + g_i \cdot \delta) - \Lambda$ are bounded. Since the origin is a basic feasible solution with the slacks as basis, the simplex method starts there, and with Bland's rule it does not cycle (Bland 1977), so it stops after finitely many pivots at a basis with no improving column, which is optimal. Maximizing $P + Q$ is minimizing $R - r = U - \Lambda - (P + Q)$. $\square$

The code clips the right-hand sides at $0$ to absorb rounding, and compares reduced costs and ratios with a tolerance of $10^{-11}$.

**Lemma 4 (monotone decrease and termination).** The accepted widths $W(L_0) > W(L_1) > \cdots$ strictly decrease, and the method stops.

*Proof.* A new axis is accepted only when its exact width, computed from Lemma 1, is below the current width. Each iteration either accepts a step or divides the box by $4$; the loop stops when the box is below a tolerance or after a fixed number of iterations. $\square$

**Lemma 5 (a step is found away from stationary axes).** Let all $\rho_i > 0$ at the current axis, and let $\Phi(\delta) = \max_i (\rho_i + g_i \cdot \delta) - \min_i (\rho_i + g_i \cdot \delta)$, a convex piecewise linear function with $\Phi(0) = W$. If $0$ does not minimize $\Phi$, then for every small enough box the accepted test succeeds.

*Proof.* $\Phi$ is convex, so if some $\hat\delta$ has $\Phi(\hat\delta) < \Phi(0)$, then along the segment $\Phi(t \hat\delta / \lvert \hat\delta \rvert) \le W - c t$ for $0 \le t \le \lvert \hat\delta \rvert$ with $c = (W - \Phi(\hat\delta))/\lvert \hat\delta \rvert > 0$. A box of size $t$ (scaled so that it contains that point) has an LP optimum $\delta^*$ with $\Phi(\delta^*) \le W - c' t$ for a constant $c' > 0$ that depends only on the box shape. By Lemma 2 and since a maximum and a minimum of functions each within $K t^2$ of their linearizations are within $K t^2$, $W(L(\delta^*)) \le \Phi(\delta^*) + 2 K t^2 \le W - c' t + 2 K t^2 < W$ for $t < c'/(2K)$. The box is divided by $4$ after each rejection, so it reaches this size. $\square$

So the method only stalls at an axis where $0$ minimizes the linearized width, which is the first-order condition for a local minimum of $W$. The proof does not show that the iterates converge to such an axis, and it does not show anything about the global minimum.

**Why there is no global guarantee.** $W$ is not convex in the axis parameters, so a descent method can stop at a local minimum that is not global, and the result depends on the start. This file does not give a proved instance of such a minimum; the claim is only that nothing here excludes it. Exact algorithms exist: Agarwal, Aronov and Sharir compute the minimum width cylindrical shell exactly in polynomial time of high degree, and approximate it within a constant factor faster. The tests check the local method against grids of axes and do not claim more.

**What the tests check.** Noise-free points on a cylinder give width below $10^{-8}$. Points that alternate between radii $4$ and $4.05$ give the width $0.05$ from a tilted and shifted start. On lobed parts, the result is at least as good as every axis of a grid of directions and positions around the true axis, and no axis of a fine grid around the result is better. The simplex code is compared with the enumeration of all vertices on random small programs.
