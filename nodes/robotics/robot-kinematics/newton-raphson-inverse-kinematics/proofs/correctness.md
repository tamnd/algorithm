---
title: Newton-Raphson inverse kinematics converges quadratically near a solution with an invertible body Jacobian
proves: [correctness]
status: full
---

We use the notation of the page, in exact arithmetic.
The arm has $n = 6$ joints, $T(\theta) = Me^{[\mathcal B_1]\theta_1}\cdots e^{[\mathcal B_6]\theta_6}$, and $J_b(\theta)$ is its body Jacobian.
Norms of matrices are the operator norms of the vector norms.

**Claim 1 (output).** If the algorithm returns $\theta$, then $\mathcal V_b = \log(T(\theta)^{-1}T_d)$ satisfies $|\omega_b| \le \varepsilon_\omega$ and $|v_b| \le \varepsilon_v$, and $T(\theta)e^{[\mathcal V_b]} = T_d$.

*Proof.*
The only return of a $\theta$ is at L4, after the test on $\mathcal V_b$.
The logarithm returns a twist with $e^{[\mathcal V_b]} = T(\theta)^{-1}T_d$, so $T(\theta)e^{[\mathcal V_b]} = T_d$.
$\square$

## The derivative of the error

Let $g(\theta) = \log(T(\theta)^{-1}T_d)$, defined and smooth on the set of $\theta$ where the rotation angle of $T(\theta)^{-1}T_d$ is less than $\pi$.
This set is open and contains every solution $\theta^*$, since there $T(\theta^*)^{-1}T_d = I$.

**Lemma 1.** On this set, $Dg(\theta) = -A(g(\theta))J_b(\theta)$, where $A$ is a smooth $6 \times 6$ matrix function on the twists with rotation angle less than $\pi$, and $A(0) = I$.

*Proof.*
Write $X(\theta) = T(\theta)^{-1}T_d$.
By the definition of the body Jacobian, $T^{-1}\partial T/\partial\theta_i = [J_{b,i}]$, the twist of column $i$ in matrix form.
Differentiating $T^{-1}T = I$ gives $\partial T^{-1}/\partial\theta_i = -T^{-1}(\partial T/\partial\theta_i)T^{-1} = -[J_{b,i}]T^{-1}$.
So $\partial X/\partial\theta_i = -[J_{b,i}]X$, a perturbation of $X$ on the left by the twist $-J_{b,i}$.
The exponential map $V \mapsto e^{[V]}$ is a local diffeomorphism at every twist with rotation angle less than $\pi$, so its inverse $\log$ is smooth there.
The derivative of $\log$ at $X = e^{[V]}$ along a left perturbation $\delta X = [W]X$ is a linear map $W \mapsto A(V)W$, smooth in $V$.
At $V = 0$, $e^{[V]} = I + [V] + O(|V|^2)$, so $\log(I + [W]) = W + O(|W|^2)$ and $A(0) = I$.
The chain rule gives $\partial g/\partial\theta_i = A(g(\theta))(-J_{b,i})$.
$\square$

## Local quadratic convergence

**Claim 2.** Let $\theta^*$ be a solution with $J_b(\theta^*)$ invertible.
There are $r > 0$ and $K \ge 0$ such that, for every $\theta$ with $|\theta - \theta^*| \le r$, the matrix $J_b(\theta)$ is invertible and the step $\theta^+ = \theta + J_b(\theta)^{-1}g(\theta)$ of L6 and L8 satisfies $|\theta^+ - \theta^*| \le K|\theta - \theta^*|^2$.

*Proof.*
Since $J_b$ is continuous and $J_b(\theta^*)$ is invertible, there are $r_0 > 0$ and $\beta$ such that, for $|\theta - \theta^*| \le r_0$, $\theta$ is in the domain of $g$, $J_b(\theta)$ is invertible and $|J_b(\theta)^{-1}| \le \beta$.
On the compact ball $B$ of radius $r_0$, the smooth functions $g$, $Dg$, $D^2g$, $J_b$ and $A \circ g$ are bounded, so there are constants $\gamma$, $\mu$ and $\nu$ with the three bounds below for $\theta \in B$ and $e = \theta - \theta^*$.

1. Taylor's theorem at $\theta$, applied to $g(\theta^*) = 0$, gives $0 = g(\theta) - Dg(\theta)e + R$ with $|R| \le \gamma|e|^2$.
2. Since $g(\theta^*) = 0$ and $Dg$ is bounded on $B$, $|g(\theta)| \le \mu|e|$.
3. Since $A$ is smooth with $A(0) = I$, $|I - A(g(\theta))| \le \nu|g(\theta)|$, and $|J_b(\theta)| \le \nu$.

By Lemma 1 and bound 1, $g(\theta) = -A(g(\theta))J_b(\theta)e - R$.
So
$$\theta^+ - \theta^* = e + J_b^{-1}g(\theta) = J_b^{-1}\bigl(I - A(g(\theta))\bigr)J_be - J_b^{-1}R.$$
By bounds 2 and 3, the first term has norm at most $\beta \cdot \nu\mu|e| \cdot \nu|e| = \beta\nu^2\mu|e|^2$, and the second at most $\beta\gamma|e|^2$.
So the claim holds with $r = r_0$ and $K = \beta(\nu^2\mu + \gamma)$.
$\square$

**Corollary.** If $|\theta^0 - \theta^*| \le \min(r, 1/(2K))$, then every iterate stays in the ball, and $|\theta^k - \theta^*| \le 2^{1 - 2^k}/K$ for $k \ge 1$.

*Proof.*
Put $d_k = K|\theta^k - \theta^*|$.
Then $d_0 \le 1/2$ and Claim 2 gives $d_{k+1} \le d_k^2$, so $d_k \le d_0^{2^k} \le 2^{-2^k}$ by induction.
Each $d_k \le d_0$, so $|\theta^k - \theta^*| \le |\theta^0 - \theta^*| \le r$ and Claim 2 applies again at every step.
So $|\theta^k - \theta^*| \le 2^{-2^k}/K \le 2^{1 - 2^k}/K$.
Since $g$ is continuous with $g(\theta^*) = 0$, $\mathcal V_b \to 0$, so the test of L4 succeeds after finitely many steps for any positive tolerances, and the algorithm returns a $\theta$ as in Claim 1.
$\square$

## The position task

For $g(\theta) = x_d - x(\theta)$ with a square Jacobian $J$, $Dg = -J$, so $A = I$ and the first term in the proof of Claim 2 is zero.
The step is the exact Newton step, and the claim and the corollary hold with $K = \beta\gamma$.

## Limits of the result

The result is local.
It says nothing about starts outside the ball, where the examples of the page show growth of the error and convergence to another solution.
If $J_b(\theta^*)$ is singular, $\beta$ does not exist, and the iteration can converge slowly or fail.
