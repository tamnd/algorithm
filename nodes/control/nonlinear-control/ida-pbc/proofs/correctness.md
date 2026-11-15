---
title: The IDA-PBC control solves the matching equation exactly when the residual is zero, and the target port-Hamiltonian system makes the minimum of the assigned energy asymptotically stable
proves: [correctness]
status: full
---

The plant is $\dot x = (J(x) - R(x)) \nabla H(x) + g(x) u$ with $x \in \mathbb{R}^n$, $u \in \mathbb{R}^m$ and $g(x)$ of full column rank $m$. The target is $\dot x = (J_d(x) - R_d(x)) \nabla H_d(x)$ with $J_d = -J_d^T$ and $R_d = R_d^T \succeq 0$. Lines L1 to L7 compute, at one point $x$,

$$w = (J_d - R_d) \nabla H_d - (J - R) \nabla H, \qquad u = (g^T g)^{-1} g^T w, \qquad \rho = w - g u,$$

and return $u$ if $\rho = 0$. Here $\|\cdot\|$ is the Euclidean norm.

## Theorem 1: the matching step

At a point $x$, the matching equation $g u = w$ has a solution if and only if $\rho = 0$, and then the solution is unique and equals the $u$ of line L4. If $u(x)$ solves it at every $x$ of an open set, the closed loop equals the target system on that set.

*Proof.* $g^T g$ is invertible because $g$ has full column rank. Let $\Pi = g (g^T g)^{-1} g^T$. Then $\Pi^2 = \Pi$, $\Pi^T = \Pi$, and $\Pi g = g$, so $\Pi$ is the orthogonal projection onto the range of $g$, and $\rho = (I - \Pi) w$. If $g u' = w$ for some $u'$, then $w$ is in the range of $g$, so $\rho = 0$, and $g^T g u' = g^T w$ gives $u' = u$. If $\rho = 0$, then $g u = \Pi w = w$. For the last claim, substitute $g u = w$ into the plant: $\dot x = (J - R) \nabla H + w = (J_d - R_d) \nabla H_d$. $\square$

Let $g^\perp(x)$ be a full rank left annihilator of $g$, so $g^\perp g = 0$. Then $\rho = 0$ is the same as

$$g^\perp \left( (J_d - R_d) \nabla H_d - (J - R) \nabla H \right) = 0.$$

For fixed $J_d$ and $R_d$ this is a system of partial differential equations in $H_d$, the matching PDE (Ortega, van der Schaft, Maschke and Escobar 2002, Section 3.2).

## Theorem 2: the target system

Let the closed loop be the target system, with $H_d$ of class $C^2$ and $\nabla H_d(x^*) = 0$, $\nabla^2 H_d(x^*) \succ 0$. Then

(a) $\dot H_d = -\nabla H_d^T R_d \nabla H_d \le 0$ along the motion;

(b) $x^*$ is a stable equilibrium in the sense of Lyapunov;

(c) if $\Omega$ is a compact set that is positively invariant, and the only solution in $\Omega$ along which $\nabla H_d^T R_d \nabla H_d \equiv 0$ is $x(t) \equiv x^*$, then every motion that starts in $\Omega$ converges to $x^*$, and $x^*$ is asymptotically stable.

*Proof.* (a) $\dot H_d = \nabla H_d^T (J_d - R_d) \nabla H_d$, and $v^T J_d v = 0$ for every $v$ because $J_d$ is skew. (b) $H_d - H_d(x^*)$ is positive definite near $x^*$ by the second-order condition, and its derivative is nonpositive by (a); this is a Lyapunov function, and the [Lyapunov direct method](/lyapunov-direct-method/) gives stability. (c) This is the [LaSalle invariance principle](/lasalle-invariance-principle/) applied with the function $H_d$ on $\Omega$ (Khalil 2002, Section 4.2): the motion converges to the largest invariant set in $\{x \in \Omega : \dot H_d = 0\}$, which is $\{x^*\}$ by assumption. $\square$

This is the content of Proposition 1 of Ortega et al. (2002), stated here for the target system.

## The magnetic levitation example

The state is $x = (\lambda, \theta, p)$: the flux of the coil, the position of the ball, and its momentum. With constants $k, m, g_0, r > 0$,

$$H = \frac{(1 - \theta) \lambda^2}{2k} + \frac{p^2}{2m} + m g_0 \theta, \qquad J - R = \begin{pmatrix} -r & 0 & 0 \\ 0 & 0 & 1 \\ 0 & -1 & 0 \end{pmatrix}, \qquad g = \begin{pmatrix} 1 \\ 0 \\ 0 \end{pmatrix}.$$

So $\dot \lambda = -r (1 - \theta) \lambda / k + u$, $\dot \theta = p / m$, $\dot p = \lambda^2 / (2k) - m g_0$. For a target $\theta^*$, the equilibrium needs $p = 0$ and $\lambda^* = \sqrt{2 k m g_0}$.

**Solving the matching PDE.** Take $J_d - R_d$ with rows $(-r_d, 0, -\alpha)$, $(0, 0, 1)$, $(\alpha, -1, 0)$, for constants $\alpha \neq 0$ and $r_d > 0$. The annihilator is $g^\perp = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}$, and the matching PDE has two rows:

$$\frac{\partial H_d}{\partial p} = \frac{p}{m}, \qquad \alpha \frac{\partial H_d}{\partial \lambda} - \frac{\partial H_d}{\partial \theta} = \frac{\lambda^2}{2k} - m g_0.$$

The first gives $H_d = p^2 / (2m) + V(\lambda, \theta)$. In the second, the function $\lambda^3 / (6 k \alpha) - m g_0 \lambda / \alpha$ is a particular solution, and $\alpha \partial_\lambda \Phi - \partial_\theta \Phi = 0$ holds for every $\Phi(\theta + \lambda / \alpha)$, because $\alpha \cdot \Phi' / \alpha - \Phi' = 0$. Choose $\Phi(z) = (b/2)(z - z^*)^2$ with $b > 0$ and $z^* = \theta^* + \lambda^* / \alpha$:

$$H_d = \frac{p^2}{2m} + \frac{\lambda^3}{6 k \alpha} - \frac{m g_0}{\alpha} \lambda + \frac{b}{2} \left( \theta + \frac{\lambda}{\alpha} - z^* \right)^2.$$

The first row of the matching equation then gives the control, by Theorem 1:

$$u = \frac{r (1 - \theta) \lambda}{k} - \frac{\alpha p}{m} - r_d \frac{\partial H_d}{\partial \lambda}.$$

The tests check, exactly in Fraction at 150 random points, that lines L1 to L7 return this $u$ and that the closed loop equals the target system, and that a $J_d$ with the wrong $\alpha$ makes the residual nonzero.

**Lemma 3: the minimum.** $\nabla H_d(x^*) = 0$ at $x^* = (\lambda^*, \theta^*, 0)$, and for $\lambda > 0$ the Hessian of $H_d$ is positive definite. If $\alpha > 0$, then for $\lambda \ge 0$ it is positive semidefinite.

*Proof.* $\partial_\theta H_d = b(\theta + \lambda / \alpha - z^*)$ and $\partial_\lambda H_d = \lambda^2 / (2 k \alpha) - m g_0 / \alpha + \partial_\theta H_d / \alpha$, both $0$ at $x^*$ since $(\lambda^*)^2 = 2 k m g_0$. The Hessian is block diagonal with the block $1/m$ for $p$ and

$$\nabla^2 V = \begin{pmatrix} \lambda / (k \alpha) + b / \alpha^2 & b / \alpha \\ b / \alpha & b \end{pmatrix}, \qquad \det \nabla^2 V = \frac{b \lambda}{k \alpha}.$$

With $b > 0$ and $\alpha > 0$, the diagonal entry $b$ is positive and the determinant is positive for $\lambda > 0$ and $0$ at $\lambda = 0$. $\square$

**Lemma 4: a compact invariant set.** Let $\alpha > 0$, $H_d^* = H_d(x^*)$ and $c^* = 2 m g_0 \lambda^* / (3 \alpha)$. For $0 < c < c^*$, the set $\Omega_c = \{x : \lambda \ge 0,\ H_d(x) - H_d^* \le c\}$ is compact, lies in $\{\lambda > 0\}$, and is positively invariant for the closed loop.

*Proof.* Let $D = \{x : \lambda \ge 0\}$, a convex set. By Lemma 3, $H_d$ is convex on $D$, so $x^*$, where the gradient is $0$, is a minimum of $H_d$ on $D$. It is the only one: if $x_1 \neq x^*$ were another, $H_d$ would be constant on the segment from $x^*$ to $x_1$, which lies in $D$, against the positive definite Hessian at $x^*$. Let $S$ be the sphere of radius $1$ around $x^*$, and $\mu = \min_{S \cap D} (H_d - H_d^*) > 0$ (a minimum of a continuous positive function on a compact set). For $x \in D$ with $\|x - x^*\| = t \ge 1$, the point $y = x^* + (x - x^*)/t$ is in $S \cap D$, and convexity gives $H_d(y) - H_d^* \le (H_d(x) - H_d^*)/t$, so $H_d(x) - H_d^* \ge t \mu$. Hence $\Omega_c$ lies in the ball of radius $\max(1, c / \mu)$, and it is closed, so it is compact.

On $\lambda = 0$, $H_d = p^2/(2m) + (b/2)(\theta - z^*)^2 \ge 0$, while $H_d^* = (\lambda^*)^3 / (6 k \alpha) - m g_0 \lambda^* / \alpha = -2 m g_0 \lambda^* / (3 \alpha) = -c^*$, using $(\lambda^*)^2 = 2 k m g_0$. So $H_d - H_d^* \ge c^* > c$ on $\lambda = 0$, and $\Omega_c$ does not meet it. A motion that starts in $\Omega_c$ has $H_d$ nonincreasing (Theorem 2(a)) while it exists; it cannot reach $\lambda = 0$, where $H_d - H_d^* > c$, without first leaving $\{H_d - H_d^* \le c\}$, which it cannot do. So it stays in the compact set $\Omega_c$, and therefore exists for all $t \ge 0$. $\square$

**Lemma 5: the LaSalle condition.** Let $\alpha > 0$. The only solution in $\Omega_c$ with $r_d (\partial_\lambda H_d)^2 \equiv 0$ is $x(t) \equiv x^*$.

*Proof.* Suppose $\partial_\lambda H_d \equiv 0$ along a solution. Then $\dot \lambda = -\alpha p / m$ and $\dot \theta = p / m$, and

$$0 = \frac{d}{dt} \partial_\lambda H_d = \left( \frac{\lambda}{k \alpha} + \frac{b}{\alpha^2} \right) \left( -\frac{\alpha p}{m} \right) + \frac{b}{\alpha} \cdot \frac{p}{m} = -\frac{\lambda p}{k m}.$$

Since $\lambda > 0$ in $\Omega_c$, $p \equiv 0$. Then $\dot p = \alpha \partial_\lambda H_d - \partial_\theta H_d = 0$ gives $\partial_\theta H_d \equiv 0$. So $\nabla H_d = 0$ along the solution, and $x = x^*$, the only critical point of $H_d$ in $D$ (Lemma 4). $\square$

**Theorem 6.** For the magnetic levitation plant with $\alpha, b, r_d > 0$ and the control above, $x^*$ is asymptotically stable, and every motion that starts in $\Omega_c$ with $c < 2 m g_0 \lambda^* / (3 \alpha)$ converges to $x^*$.

*Proof.* Theorem 2 with Lemmas 3, 4 and 5. $\square$

For the page example, $k = m = r = 1$, $g_0 = 2$, $\theta^* = 1/2$, $\lambda^* = 2$, $\alpha = 2$, $b = 1$, $r_d = 2$: $c^* = 4/3$, and the initial state $(2, 0.3, 0)$ has $H_d - H_d^* = 0.02$, so it is in $\Omega_{0.02}$ and Theorem 6 applies. The tests check Lemma 3 and the identity of Lemma 5 exactly, and measure $\dot H_d \le 0$ along the RK4 solution and the balance $H_d(T) - H_d(0) = -r_d \int_0^T (\partial_\lambda H_d)^2 dt$ within $10^{-8}$.

The model of the plant is valid only for $\theta < 1$, where the inductance $k / (1 - \theta)$ is positive. Theorem 6 is a statement about the model; in the example the position stays in $[0.3, 0.5]$.
