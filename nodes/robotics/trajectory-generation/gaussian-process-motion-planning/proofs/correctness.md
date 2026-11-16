---
title: The prior factor is the minimum acceleration energy, the interpolation is the cubic Hermite curve, and every Levenberg-Marquardt step that is accepted lowers the cost
proves: [correctness]
status: full
---

We use the notation of the page and of the code. Each support state is $\theta = (p, v) \in \mathbb R^2 \times \mathbb R^2$. For an interval of length $s$,

$$\Phi_s = \begin{pmatrix} I & sI \\ 0 & I \end{pmatrix}, \qquad Q_s = Q_c \begin{pmatrix} \tfrac{s^3}{3} I & \tfrac{s^2}{2} I \\ \tfrac{s^2}{2} I & s I \end{pmatrix}.$$

For a path $p$ on an interval $[a, b]$ with square integrable second derivative, its energy is $E(p) = \frac{1}{2Q_c}\int_a^b \|p''(t)\|^2\,dt$. For two states $\theta, \theta'$ and a length $s$, let $E_s(\theta, \theta')$ be the smallest energy of a path of duration $s$ that starts in state $\theta$ and ends in state $\theta'$ (position and velocity).

## Lemma 1: the prior factor is the minimum energy

**Claim.** $E_s(\theta, \theta') = \frac12 e^{\mathsf T} Q_s^{-1} e$ with $e = \theta' - \Phi_s \theta$, and the unique path that attains it is the cubic Hermite curve with the given end positions and velocities.

*Proof.* The coordinates separate, so take one coordinate, with states $(p_0, v_0)$ and $(p_1, v_1)$ on $[0, s]$, and write $u = p''$. By Taylor's formula with integral remainder, the end conditions are

$$\int_0^s (s - t)\,u(t)\,dt = p_1 - p_0 - v_0 s = e_p, \qquad \int_0^s u(t)\,dt = v_1 - v_0 = e_v.$$

Put $k_1(t) = s - t$ and $k_2(t) = 1$. Their Gram matrix in $L^2(0, s)$ is $G = \begin{pmatrix} s^3/3 & s^2/2 \\ s^2/2 & s \end{pmatrix}$, which is positive definite (its determinant is $s^4/12$). Let $\lambda = G^{-1}(e_p, e_v)^{\mathsf T}$ and $u^* = \lambda_1 k_1 + \lambda_2 k_2$; then $u^*$ meets both conditions. For every $u$ that meets them, $u - u^*$ is orthogonal to $k_1$ and $k_2$, so it is orthogonal to $u^*$, and

$$\int_0^s u^2 = \int_0^s (u^*)^2 + \int_0^s (u - u^*)^2 \ge \int_0^s (u^*)^2 = \lambda^{\mathsf T} G \lambda = (e_p, e_v)\, G^{-1} (e_p, e_v)^{\mathsf T},$$

with equality only for $u = u^*$. Since $u^*$ is affine, the minimizing path is a cubic with the four given end values; the cubic Hermite curve is the only such cubic. Dividing by $2Q_c$ and adding the two coordinates gives $\frac12 e^{\mathsf T} Q_s^{-1} e$. $\square$

## Lemma 2: splitting an interval

**Claim.** For $0 < \tau < s$ and states $\theta_0, z, \theta_1$,

$$E_\tau(\theta_0, z) + E_{s - \tau}(z, \theta_1) \ge E_s(\theta_0, \theta_1),$$

with equality if and only if $z$ is the state at time $\tau$ of the cubic Hermite curve $H$ from $\theta_0$ to $\theta_1$.

*Proof.* Join the minimizing curve from $\theta_0$ to $z$ with the minimizing curve from $z$ to $\theta_1$. Position and velocity agree at $\tau$, so the joined path has a square integrable second derivative, starts in $\theta_0$ and ends in $\theta_1$; its energy is the left side, which is therefore at least $E_s(\theta_0, \theta_1)$. If $z = H(\tau)$, the two pieces of $H$ are admissible for the two short intervals, so the left side is at most $E(H) = E_s(\theta_0, \theta_1)$, and equality holds. If equality holds, the joined path attains the minimum on $[0, s]$, so by the uniqueness in Lemma 1 it is $H$, and $z = H(\tau)$. $\square$

## Theorem 1: the interpolation of the code is the cubic Hermite curve

The code uses $\Psi = Q_\tau \Phi_{s-\tau}^{\mathsf T} Q_s^{-1}$ and $\Lambda = \Phi_\tau - \Psi \Phi_s$ and sets $z^* = \Lambda\theta_0 + \Psi\theta_1$.

**Claim.** $z^* = H(\tau)$, so the obstacle factors between support states are evaluated on the cubic Hermite curve through the support states.

*Proof.* By Lemma 1, the left side of Lemma 2 is the quadratic function

$$J(z) = \tfrac12 (z - \Phi_\tau\theta_0)^{\mathsf T} Q_\tau^{-1} (z - \Phi_\tau\theta_0) + \tfrac12 (\theta_1 - B z)^{\mathsf T} Q_{s-\tau}^{-1} (\theta_1 - B z), \qquad B = \Phi_{s-\tau},$$

and by Lemma 2 its unique minimizer is $H(\tau)$. $J$ is strictly convex, so it is enough to check that $z^*$ satisfies $\nabla J(z^*) = 0$, that is, $Q_\tau^{-1}(z^* - \Phi_\tau\theta_0) = B^{\mathsf T} Q_{s-\tau}^{-1}(\theta_1 - B z^*)$.

Two identities are needed. First, $B\Phi_\tau = \Phi_s$. Second, $B Q_\tau B^{\mathsf T} + Q_{s-\tau} = Q_s$: per coordinate, with $a = \tau$ and $b = s - \tau$, the entries of $B Q_\tau B^{\mathsf T}$ are $a^3/3 + a^2 b + a b^2$, $a^2/2 + ab$ and $a$ (times $Q_c$), and adding $b^3/3$, $b^2/2$ and $b$ gives $(a+b)^3/3$, $(a+b)^2/2$ and $a + b$.

Put $r = \theta_1 - \Phi_s\theta_0$. Then $z^* - \Phi_\tau\theta_0 = \Psi r = Q_\tau B^{\mathsf T} Q_s^{-1} r$, so the left side is $B^{\mathsf T} Q_s^{-1} r$. For the right side, $\theta_1 - B z^* = \theta_1 - \Phi_s\theta_0 - B Q_\tau B^{\mathsf T} Q_s^{-1} r = r - (Q_s - Q_{s-\tau}) Q_s^{-1} r = Q_{s-\tau} Q_s^{-1} r$, so the right side is $B^{\mathsf T} Q_s^{-1} r$ as well. $\square$

In the language of Gaussian processes, $J$ is minus the logarithm of the density of the state at $\tau$ given the two support states, up to a constant, so $z^*$ is the conditional mean.

## Theorem 2: without obstacles, the result is the minimum energy cubic

**Claim.** With no obstacle factors, the prior cost $\sum_i \frac12 e_i^{\mathsf T} Q^{-1} e_i$ over the free support states $\theta_1, \dots, \theta_{N-1}$ has the unique minimizer $\theta_i = P(t_i)$, the states of the cubic $P$ of least energy from $\theta_0$ to $\theta_N$, and the minimum is $E(P)$. For $\theta_0 = (A, 0)$, $\theta_N = (B, 0)$ and total time $T$, $P(t) = A + (B - A)\bigl(3(t/T)^2 - 2(t/T)^3\bigr)$, and $E(P) = 6\|B - A\|^2/(Q_c T^3)$.

*Proof.* By Lemma 1 the prior cost is $\sum_i E_{\Delta t}(\theta_i, \theta_{i+1})$. Joining the minimizing pieces gives an admissible path on $[0, T]$, so the sum is at least $E_T(\theta_0, \theta_N)$; for $\theta_i = P(t_i)$ the pieces of $P$ show equality, and if equality holds the joined path is a minimizer, hence $P$, by uniqueness. For the given ends, the Hermite cubic is the stated $P$; $P''(t) = (B - A)(6 - 12t/T)/T^2$ and $\int_0^T (6 - 12 t/T)^2\,dt/T^4 = 12/T^3$, so $E(P) = 6\|B - A\|^2/(Q_c T^3)$. $\square$

For the example on the page ($A = (-1, 0)$, $B = (1, 0)$, $T = 1$, $Q_c = 1$) this is $24$.

## Theorem 3: the Levenberg-Marquardt loop

Write $F(x) = \frac12 \sum_f r_f(x)^{\mathsf T} W_f r_f(x)$ for the total cost, with residuals $r_f$ and weights $W_f$ (the matrices $Q^{-1}$ for the prior and $1/\sigma^2$ for each obstacle term). Each obstacle term is $\frac{1}{2\sigma^2}\max(0, \varepsilon - d)^2$, which is continuously differentiable wherever $d$ is, because the square of a hinge has a continuous derivative; for a disc this holds everywhere except at its center. Line L3 forms $H = \sum_f J_f^{\mathsf T} W_f J_f$ and $g = \sum_f J_f^{\mathsf T} W_f r_f = \nabla F(x)$.

**Claim.** Every step accepted by line L6 lowers $F$. If $F$ is continuously differentiable near $x$ and $g \ne 0$, then after finitely many increases of $\lambda$ in line L7 a step is accepted.

*Proof.* The first part is the test of line L6. For the second, $H$ is positive semidefinite, so $H + \lambda I$ is positive definite for $\lambda > 0$, and the step $\delta = -(H + \lambda I)^{-1} g$ of line L4 satisfies $\|\delta\| \le \|g\|/\lambda$ and $-g^{\mathsf T}\delta \ge \|g\|^2/(\|H\| + \lambda)$. Differentiability gives $F(x + \delta) = F(x) + g^{\mathsf T}\delta + o(\|\delta\|)$. So

$$F(x + \delta) - F(x) \le -\frac{\|g\|^2}{\|H\| + \lambda} + o\!\left(\frac{\|g\|}{\lambda}\right),$$

and the first term dominates as $\lambda \to \infty$, because $\lambda\|g\|^2/(\|H\| + \lambda) \to \|g\|^2 > 0$. Line L7 multiplies $\lambda$ by 10 at each rejection, so the right side becomes negative after finitely many rejections. $\blacksquare$

## Structure of the system

A prior factor involves the support states $i$ and $i + 1$, an obstacle factor at a support state involves one state, and an obstacle factor between support states $i$ and $i + 1$ involves exactly those two (Theorem 1). So $H$ has nonzero $4 \times 4$ blocks only on the diagonal and next to it, and line L4 solves the system by block elimination in $O(N)$ block operations.

## What is not proved

The cost values decrease, but nothing says that the limit is a global minimum or free of collision. The obstacle term is a soft cost: the result can stay inside the safety distance, as in the example, where the clearance ends below $\varepsilon$. The method is local, and a start on the other side of an obstacle leads to another answer.
