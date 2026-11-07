---
title: Correctness of Broyden's method
proves: [correctness, termination, convergence-rate]
status: full
---

Throughout, $\|\cdot\|$ is the Euclidean norm on $\mathbb{R}^n$ and the induced matrix norm, $\|\cdot\|_F$ the Frobenius norm, $J_* = J(x^*)$, $\beta = \|J_*^{-1}\|$, $E_k = B_k - J_*$, $s_k = x_{k+1} - x_k$ and $e_k = x_k - x^*$. Statements are in exact arithmetic. The implementation's step test uses the max-norm, which is equivalent and does not affect any statement below.

**Hypotheses (H).** $F$ is continuously differentiable on an open convex set $D$ containing $x^*$, $F(x^*) = 0$, $J_*$ is nonsingular, and $\|J(x) - J(z)\| \le \gamma\|x - z\|$ on $D$.

## Termination

Each pass of the loop L2 returns at L3, L4 or L8, or increases $k$; after $K$ passes L9 returns. The run uses at most $K + 1$ evaluations of $F$, plus $n$ for a difference Jacobian.

## Lemma 1 (least change secant update)

$B_{k+1}$ satisfies $B_{k+1}s_k = y_k$ and $B_{k+1}z = B_kz$ for $z \perp s_k$. Among all matrices $B$ with $Bs_k = y_k$ it minimizes $\|B - B_k\|_F$.

*Proof.* The first two facts are immediate from $B_{k+1} - B_k = (y_k - B_ks_k)s_k^T/(s_k^Ts_k)$. If $Bs_k = y_k$, then $(B_{k+1} - B_k) = (B - B_k)P$ with $P = s_ks_k^T/(s_k^Ts_k)$, and $\|(B - B_k)P\|_F \le \|B - B_k\|_F\|P\| = \|B - B_k\|_F$, since $P$ is an orthogonal projection. $\square$

## Lemma 2 (bounded deterioration)

Under (H), if the segment $[x_k, x_{k+1}]$ lies in $D$, then with $P_k = s_ks_k^T/(s_k^Ts_k)$ and $\eta_k = (\|e_k\| + \|e_{k+1}\|)/2$,
$$E_{k+1} = E_k(I - P_k) + (\bar A_k - J_*)P_k, \qquad \bar A_k = \int_0^1 J(x_k + ts_k)\,dt, \qquad \|\bar A_k - J_*\| \le \gamma\eta_k,$$
and therefore $\|E_{k+1}\|_F \le \|E_k\|_F + \gamma\eta_k$.

*Proof.* By the fundamental theorem of calculus $y_k = \bar A_ks_k$, so $y_k - B_ks_k = (\bar A_k - B_k)s_k$ and $B_{k+1} = B_k + (\bar A_k - B_k)P_k$. Subtracting $J_*$ gives the formula. Since $x_k + ts_k - x^* = (1 - t)e_k + te_{k+1}$, the Lipschitz condition gives $\|\bar A_k - J_*\| \le \gamma\int_0^1 ((1 - t)\|e_k\| + t\|e_{k+1}\|)\,dt = \gamma\eta_k$. Finally $\|E_k(I - P_k)\|_F \le \|E_k\|_F$ and $\|MP_k\|_F = \|Ms_k\|/\|s_k\| \le \|M\|$ for any $M$. $\square$

## Theorem 1 (local linear convergence)

Assume (H) and let $\eta \le 1/(12\beta)$ and $\varepsilon > 0$ satisfy $\gamma\varepsilon \le 1/(3\beta)$, $\varepsilon \le 2\eta/(3\gamma)$, and the ball $\{\|x - x^*\| \le \varepsilon\}$ lies in $D$. If $\|e_0\| \le \varepsilon$ and $\|E_0\|_F \le \eta$, then for every $k$: $B_k$ is nonsingular with $\|B_k^{-1}\| \le 3\beta/2$, $\|E_k\|_F \le 2\eta$, and $\|e_{k+1}\| \le \frac12\|e_k\|$.

*Proof.* Induction on $k$, with the hypothesis that $\|E_k\|_F \le 2\eta$ and $\|e_j\| \le 2^{-j}\varepsilon$ for $j \le k$. Then $\|J_*^{-1}E_k\| \le 2\beta\eta \le 1/6$, so by the Banach perturbation lemma $B_k = J_*(I + J_*^{-1}E_k)$ is nonsingular with $\|B_k^{-1}\| \le \beta/(1 - 1/6) \le 3\beta/2$. Next,
$$e_{k+1} = e_k - B_k^{-1}F(x_k) = B_k^{-1}\bigl(E_ke_k - (F(x_k) - F(x^*) - J_*e_k)\bigr),$$
and $\|F(x_k) - F(x^*) - J_*e_k\| \le \frac{\gamma}{2}\|e_k\|^2$ by the Lipschitz condition. Hence
$$\|e_{k+1}\| \le \tfrac{3\beta}{2}\bigl(2\eta + \tfrac{\gamma}{2}\varepsilon\bigr)\|e_k\| \le \bigl(\tfrac14 + \tfrac14\bigr)\|e_k\| = \tfrac12\|e_k\|,$$
using $3\beta\eta \le 1/4$ and $\frac34\beta\gamma\varepsilon \le 1/4$. The ball is convex, so the segment $[x_k, x_{k+1}]$ lies in it, and Lemma 2 applies to every step so far:
$$\|E_{k+1}\|_F \le \|E_0\|_F + \gamma\sum_{j=0}^{k}\eta_j \le \eta + \frac{\gamma}{2}\sum_{j \ge 0}\bigl(2^{-j} + 2^{-j-1}\bigr)\varepsilon = \eta + \frac{3\gamma\varepsilon}{2} \le 2\eta.$$
This completes the induction. $\square$

## Theorem 2 (superlinear convergence)

Under the hypotheses of Theorem 1, if no $e_k$ is $0$, then $\|e_{k+1}\|/\|e_k\| \to 0$.

*Proof.* Let $\theta_k = \|E_ks_k\|/\|s_k\|$. Because $P_k$ is an orthogonal projection, $\|E_k(I - P_k)\|_F^2 = \|E_k\|_F^2 - \|E_kP_k\|_F^2 = \|E_k\|_F^2 - \theta_k^2$. With Lemma 2,
$$\|E_{k+1}\|_F \le \sqrt{\|E_k\|_F^2 - \theta_k^2} + \gamma\eta_k \le \|E_k\|_F - \frac{\theta_k^2}{2\|E_k\|_F} + \gamma\eta_k$$
when $E_k \ne 0$ (when $E_k = 0$, $\theta_k = 0$). Since $\|E_k\|_F \le 2\eta$, this gives $\theta_k^2 \le 4\eta(\|E_k\|_F - \|E_{k+1}\|_F + \gamma\eta_k)$. Summing over $k$, the first two terms telescope and $\sum_k\eta_k \le 3\varepsilon/2$, so $\sum_k\theta_k^2 \le 4\eta(\eta + 3\gamma\varepsilon/2) < \infty$ and $\theta_k \to 0$.

Now $F(x_{k+1}) = F(x_k) + \bar A_ks_k$ and $B_ks_k = -F(x_k)$, so $F(x_{k+1}) = (\bar A_k - B_k)s_k = (\bar A_k - J_*)s_k - E_ks_k$ and
$$\|F(x_{k+1})\| \le (\gamma\eta_k + \theta_k)\|s_k\|.$$
On the other hand $F(x_{k+1}) = J_*e_{k+1} + r$ with $\|r\| \le \frac{\gamma}{2}\|e_{k+1}\|^2$, so $\|F(x_{k+1})\| \ge \|e_{k+1}\|(1/\beta - \gamma\varepsilon/2) \ge \|e_{k+1}\|/(2\beta)$. Also $\|s_k\| \le \|e_k\| + \|e_{k+1}\| \le 2\|e_k\|$. Together,
$$\frac{\|e_{k+1}\|}{\|e_k\|} \le 4\beta(\gamma\eta_k + \theta_k) \to 0. \qquad \square$$

The same computation shows $\|s_k\|/\|e_k\| \to 1$, since $s_k = e_{k+1} - e_k$. So near the root the step test at L8 measures the error up to a factor tending to 1, which justifies it locally. If some $F(x_k) = 0$, the method stops there with status "exact", which is correct.

## Remarks on what is not proved here

The order is not 2, and $B_k$ need not converge to $J_*$; neither is needed above. Gay's results (finite termination in $2n$ steps on affine problems, $2n$-step quadratic convergence) are cited, not proved, on the page; the tests check the first in exact rational arithmetic on small cases. Nothing is claimed for starts outside the ball of Theorem 1, and the effect of rounding on the update when $s_k$ is tiny is described on the page as observed behaviour.
