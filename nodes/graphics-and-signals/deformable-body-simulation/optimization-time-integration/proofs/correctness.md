---
title: Correctness of optimization time integration
proves: [correctness]
status: full
---

Let $M$ be the diagonal mass matrix of the free coordinates, $\Phi$ the potential energy (springs plus gravity), $\hat x = x_n + \Delta t\, v_n$, and

$$E(z) = \frac{1}{2\Delta t^2}(z - \hat x)^T M (z - \hat x) + \Phi(z).$$

The step returns $x_{n+1} = z$ and $v_{n+1} = (z - x_n)/\Delta t$. Lines L1 to L11 refer to the template on the page. We assume that $\Phi$ is differentiable at every iterate (for springs with a positive rest length this means that no spring has length zero).

**Lemma 1 (stationary points are backward Euler steps).** $\nabla E(z) = 0$ if and only if $(x_{n+1}, v_{n+1}) = (z, (z - x_n)/\Delta t)$ satisfies $x_{n+1} = x_n + \Delta t\, v_{n+1}$ and $M(v_{n+1} - v_n) = -\Delta t\, \nabla\Phi(x_{n+1})$.

*Proof.* The first equation holds by the definition of $v_{n+1}$. Then $z - \hat x = \Delta t(v_{n+1} - v_n)$, so $\nabla E(z) = M(v_{n+1} - v_n)/\Delta t + \nabla\Phi(z)$. This is zero exactly when the second equation holds. $\square$

**Lemma 2 (E is bounded below).** If every spring energy is nonnegative and gravity is linear, $E$ is bounded below on the free coordinates.

*Proof.* The spring terms are at least $0$. The rest is $\frac{1}{2\Delta t^2}(z - \hat x)^T M (z - \hat x) - \sum_i m_i\, g \cdot z_i$, a strictly convex quadratic because $M$ is positive definite, and a strictly convex quadratic has a finite minimum. $\square$

**Lemma 3 (the direction is downhill).** Let $g = \nabla E(z) \neq 0$ and $0 < \kappa < 1$. After L7 and L8, the direction $d$ satisfies $d \cdot g < 0$.

*Proof.* If the Newton direction passes the test $d \cdot g < -\kappa |d||g|$, then $d \cdot g < 0$. Otherwise L7 tries $-d$, and if it passes, the same bound holds for $-d$. If both fail, or if $H$ is singular, L7 uses $d = -g$, and $d \cdot g = -|g|^2 < 0$. L8 multiplies $d$ by a positive number, which keeps the sign of $d \cdot g$. $\square$

**Lemma 4 (the line search ends).** If $d \cdot g < 0$ and $E$ is differentiable at $z$, then for each $c \in (0, 1)$ there is $t_0 > 0$ with $E(z + t d) \le E(z) + c\, t\, d \cdot g$ for all $t \in (0, t_0]$. So backtracking by halves from $t = 1$ stops after a finite number of halvings.

*Proof.* By differentiability, $E(z + t d) = E(z) + t\, d \cdot g + o(t)$. Since $(1 - c)\, d \cdot g < 0$, the term $o(t)$ is smaller than $-(1 - c)\, t\, d \cdot g$ for all small $t$, which gives the inequality. $\square$

In floating point the code also stops the search at $t < 10^{-14}$ and then keeps $z$ without an update.

**Theorem 5 (the objective never rises).** With the safeguards, the values of $E$ at the accepted iterates do not increase.

*Proof.* An iterate is accepted at L10 only after the Armijo test $E(z + t d) \le E(z) + 10^{-4}\, t\, d \cdot g$ with $t > 0$. By Lemma 3, $d \cdot g < 0$, so $E(z + t d) < E(z)$. When the test is not met, the code stops and keeps $z$, so no step raises $E$. $\square$

**Corollary 6.** By Lemma 2 and Theorem 5, the values of $E$ at the iterates converge. This does not prove that $\nabla E$ goes to zero: the spring energy with a positive rest length is not differentiable at length zero, so the usual global convergence theorems for line search methods do not apply without more assumptions.

**Theorem 7 (one Newton step solves a quadratic step).** Let $\Phi$ be a quadratic with a positive semidefinite Hessian $K$ (springs with rest length zero plus gravity), and let $H = M/\Delta t^2 + K$ have the condition number $\lambda_{\max}/\lambda_{\min} < 1/\kappa$. Then the first iteration takes the full Newton step and ends at the exact minimizer of $E$.

*Proof.* $H$ is positive definite, so $d = -H^{-1} g$ exists. Then $-d \cdot g = g^T H^{-1} g \ge |g|^2/\lambda_{\max}$ and $|d| \le |g|/\lambda_{\min}$, so $-d \cdot g \ge (\lambda_{\min}/\lambda_{\max}) |d||g| > \kappa |d||g|$ and L7 keeps $d$. Since $E$ is quadratic, $E(z + d) = E(z) + d \cdot g + \frac12 d^T H d = E(z) + \frac12 d \cdot g$, which meets the Armijo test with $c = 10^{-4} \le \frac12$, so $t = 1$. The point $z + d$ has $\nabla E = g + H d = 0$, and it is the unique minimizer because $H$ is positive definite. (L8 can shorten $d$ only if $|d| > \ell$; with $\ell = 10^3$ this does not occur in the tests.) $\square$

**Corollary 8 (free fall is symplectic Euler).** If $\Phi$ is only gravity, the initial guess at L2 is $z = \hat x + \Delta t^2 g$, and $\nabla E(z) = M(z - \hat x)/\Delta t^2 - M g = 0$, so L5 stops at once. Then $v_{n+1} = v_n + \Delta t\, g$ and $x_{n+1} = x_n + \Delta t\, v_{n+1}$, which is the symplectic Euler step. After 10 steps of $0.1$ from rest, $y = -9.81 \cdot 0.01 \cdot (1 + 2 + \cdots + 10) = -5.3955$. $\square$

**Theorem 9 (energy decay for a convex potential).** Let $\Phi$ be convex and differentiable and let $(x_{n+1}, v_{n+1})$ be an exact backward Euler step. With $\mathcal E = \frac12 v^T M v + \Phi(x)$,

$$\mathcal E_n - \mathcal E_{n+1} \ge \tfrac12 (v_{n+1} - v_n)^T M (v_{n+1} - v_n).$$

*Proof.* Write $v_0 = v_n$, $v_1 = v_{n+1}$, $x_0 = x_n$, $x_1 = x_{n+1}$. By Lemma 1, $M(v_1 - v_0) = -\Delta t\, \nabla\Phi(x_1)$. The identity $\frac12 v_1^T M v_1 - \frac12 v_0^T M v_0 = v_1^T M (v_1 - v_0) - \frac12 (v_1 - v_0)^T M (v_1 - v_0)$ and $\Delta t\, v_1 = x_1 - x_0$ give

$$K_1 - K_0 = -\nabla\Phi(x_1) \cdot (x_1 - x_0) - \tfrac12 (v_1 - v_0)^T M (v_1 - v_0).$$

Convexity gives $\Phi(x_0) \ge \Phi(x_1) + \nabla\Phi(x_1) \cdot (x_0 - x_1)$, that is $-\nabla\Phi(x_1) \cdot (x_1 - x_0) \le \Phi(x_0) - \Phi(x_1)$. Adding $\Phi(x_1) - \Phi(x_0)$ to both sides of the identity gives the claim. $\square$

The theorem needs convexity. Springs with a positive rest length have a nonconvex energy (the energy of a spring is not convex when it is compressed), so for them the decay of $\mathcal E$ is only measured, not proved. The code stops at $|\nabla E| < \tau$, so it satisfies the inequality only up to a term of order $\tau$; the test allows $10^{-9}$.
