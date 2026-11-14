---
title: The DLM sensitivities are the exact first derivatives, and the worst-case and RSS results follow with a second-order error
proves: [correctness]
status: full
---

**Setting.** The loops give $m$ equations $h(x, u) = 0$, with $x \in \mathbb{R}^n$ the manufactured variables and $u \in \mathbb{R}^m$ the kinematic variables. Each component of $h$ is a sum of terms $\pm L \cos\theta$ or $\pm L \sin\theta$, where $L$ is a constant or a variable and $\theta$ is an affine function of the variables, so $h$ is infinitely differentiable. Let $h(x_0, u_0) = 0$, and let $A = \partial h / \partial x$ and $B = \partial h / \partial u$ at $(x_0, u_0)$. The output is one kinematic variable $u_k$.

**Claim.**

1. The partial derivatives that lines L2 and L4 use are exact.
2. If $B$ is nonsingular, then near $x_0$ there is a unique smooth solution $u(x)$ with $u(x_0) = u_0$, and the vector $S$ of line L5 is the gradient of $u_k(x)$ at $x_0$.
3. For a change $\delta$ of $x$, $u_k(x_0 + \delta) = u_k(x_0) + S \cdot \delta + r(\delta)$ with $|r(\delta)| \le \tfrac12 M |\delta|^2$, where $M$ bounds the norm of the Hessian of $u_k$ on the segment from $x_0$ to $x_0 + \delta$.
4. If $|\delta_j| \le T_j$ for all $j$, the linear part $S \cdot \delta$ ranges exactly over $[-W, W]$ with $W = \sum_j |S_j| T_j$ (line L6). So the true output lies in $u_k(x_0) \pm (W + \tfrac12 M |T|^2)$.
5. If the $\delta_j$ are independent with mean $0$ and standard deviations $\sigma_j = T_j / 3$, the linear part has standard deviation exactly $\tfrac13 \sqrt{\sum_j S_j^2 T_j^2}$, one third of line L7. If the $\delta_j$ are also normal, the linear part is normal and lies within $\pm$ the RSS value with probability $0.9973$.
6. If every angle is a constant, and every variable is a length, then $u(x)$ is affine and $r \equiv 0$: DLM is exact for any size of change.

**Proof of 1.** A term $s L (\cos\theta, \sin\theta)$ with $\theta = \theta_0 + \sum_j c_j y_j$ has the partial derivative $s (\cos\theta, \sin\theta)$ with respect to $L$ when $L$ is a variable, and $s L c_j (-\sin\theta, \cos\theta)$ with respect to $y_j$, by the chain rule. The function loop_jacobian adds exactly these terms, and a variable that occurs in several terms gets the sum of their derivatives. $\square$

**Proof of 2.** This is the implicit function theorem (Rudin, Principles of Mathematical Analysis, Theorem 9.28): $h$ is continuously differentiable, $h(x_0, u_0) = 0$ and $B$ is invertible, so there are neighborhoods $U$ of $x_0$ and $V$ of $u_0$ and a unique continuously differentiable $u : U \to V$ with $h(x, u(x)) = 0$. Here $h$ is smooth, so $u$ is smooth too. Differentiate $h(x, u(x)) = 0$ at $x_0$: $A + B\, Du(x_0) = 0$, so $Du(x_0) = -B^{-1} A$. Line L4 solves $B s_j = -A_j$ for each column $j$ of $A$, so $s_j$ is column $j$ of $-B^{-1} A$, and line L5 takes its component $k$, which is $\partial u_k / \partial x_j$. $\square$

**Proof of 3.** Let $\phi(\tau) = u_k(x_0 + \tau \delta)$ for $\tau \in [0, 1]$, assuming the segment lies in $U$. Taylor's theorem with the Lagrange remainder gives $\phi(1) = \phi(0) + \phi'(0) + \tfrac12 \phi''(\tau^*)$ for some $\tau^* \in (0, 1)$. Here $\phi'(0) = S \cdot \delta$ and $\phi''(\tau) = \delta^{\mathsf T} H(x_0 + \tau \delta)\, \delta$, with $H$ the Hessian of $u_k$, so $|\phi''(\tau^*)| \le M |\delta|^2$. $\square$

**Proof of 4.** The linear function $S \cdot \delta$ is separable, so its maximum over the box $|\delta_j| \le T_j$ is $\sum_j \max_{|\delta_j| \le T_j} S_j \delta_j = \sum_j |S_j| T_j$, at $\delta_j = T_j \operatorname{sign}(S_j)$. Its minimum is $-W$ by symmetry, and every value between is taken because the box is connected. Adding the bound of part 3, with $|\delta| \le |T|$, gives the range of the true output. $\square$

This is the worst-case formula of tolerance stack-up applied to the sensitivities. It is exact for the linear part only. The true range can be larger or smaller than $\pm W$ by up to $\tfrac12 M |T|^2$, and it need not be symmetric.

**Proof of 5.** By linearity of expectation $E[S \cdot \delta] = 0$, and by independence the variances add: $\operatorname{Var}(S \cdot \delta) = \sum_j S_j^2 \sigma_j^2 = \tfrac19 \sum_j S_j^2 T_j^2$. A linear combination of independent normal variables is normal, and a normal variable lies within 3 standard deviations of its mean with probability $2\Phi(3) - 1 \approx 0.9973$. $\square$

This is the RSS formula of tolerance stack-up. Independence is needed for the variance, and normality only for the probability. The remainder $r$ adds a bias: $E[r(\delta)] = \tfrac12 \sum_j H_{jj} \sigma_j^2 + O(\sigma^3)$ for smooth $u_k$ and symmetric $\delta_j$, which shifts the mean of the output away from $u_k(x_0)$. DLM does not see this shift.

**Proof of 6.** With constant angles, $h(x, u) = P x + Q u + c$ for constant matrices $P$ and $Q$ and a constant vector $c$, and then $A = P$ and $B = Q$ at every point. If $Q$ is invertible, $u(x) = -Q^{-1}(P x + c)$, which is affine, so its Hessian is zero and $M = 0$ in part 3. $\square$

**Line L1 and the Newton loop.** Lines L9 to L12 are Newton's method for $h(x_0, u) = 0$. The implementation returns only when the last step is below the tolerance and the residual is below $10^{-9}$, and otherwise raises an error, so every returned $u_0$ satisfies the loops to that accuracy. Newton's method converges quadratically from a start close enough to a solution with nonsingular $B$; from a poor start it can fail or reach another assembly branch, such as the crossed form of a four-bar. That is why the caller supplies the starting guess.
