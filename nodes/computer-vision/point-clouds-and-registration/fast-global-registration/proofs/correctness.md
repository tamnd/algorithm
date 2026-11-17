---
title: The line process gives the Geman-McClure cost, and the FGR step is a descent direction
proves: [correctness]
status: full
---

We use the notation of the page. There are $m$ correspondences $(p_k, q_k)$ in $\mathbb{R}^3$, the current pose is $T = (R, t)$, $x_k = T p_k = R p_k + t$ and $r_k = x_k - q_k$. For $\mu > 0$ the cost is

$$E(T) = \sum_{k=1}^{m} \rho(|r_k|^2), \qquad \rho(s) = \frac{\mu s}{\mu + s},$$

where we write $\rho$ as a function of the squared residual $s = |r|^2$. A small motion $\xi = (\omega, v) \in \mathbb{R}^6$ moves the pose to $T_\xi$, with $T_\xi p = \exp(\omega)(R p + t) + v$, where $\exp(\omega)$ is the rotation by the vector $\omega$. We prove three facts. They show that each step of FGR is a correct line process step and a descent direction. They do not show that the full step lowers $E$, and they do not show that FGR finds the global minimum.

## Lemma 1: the line process

For $s \ge 0$ and $\mu > 0$, the function $h(l) = l s + \mu (\sqrt l - 1)^2$ on $l \ge 0$ has the unique minimizer $l^\star = (\mu / (\mu + s))^2$, and $h(l^\star) = \rho(s)$.

*Proof.* Put $u = \sqrt l \ge 0$. Then $h = u^2 s + \mu (u - 1)^2$, a strictly convex quadratic in $u$ because its leading coefficient $s + \mu$ is positive. Its derivative $2 u s + 2 \mu (u - 1)$ is zero at $u^\star = \mu / (\mu + s)$, which lies in $(0, 1]$, so it is the minimizer over $u \ge 0$, and $l^\star = (u^\star)^2$. With $1 - u^\star = s / (\mu + s)$,

$$h(l^\star) = \frac{\mu^2 s}{(\mu + s)^2} + \frac{\mu s^2}{(\mu + s)^2} = \frac{\mu s (\mu + s)}{(\mu + s)^2} = \rho(s). \qquad \square$$

So $\min_L E(T, L) = E(T)$ for the joint cost $E(T, L) = \sum_k l_k |r_k|^2 + \sum_k \mu(\sqrt{l_k} - 1)^2$, and line L3 computes the minimizing $L$ for the current $T$.

## Lemma 2: the gradient

Let $J_k = [-[x_k]_\times \mid I]$, so that $J_k \xi = \omega \times x_k + v$, and let $g = \sum_k l_k J_k^{\mathsf T} r_k$ with $l_k = l^\star(|r_k|^2)$. Then $\frac{d}{d\varepsilon} E(T_{\varepsilon \xi}) \big|_{\varepsilon = 0} = 2 g^{\mathsf T} \xi$ for every $\xi$.

*Proof.* The rotation by $\varepsilon \omega$ is $I + \varepsilon [\omega]_\times + O(\varepsilon^2)$, so $T_{\varepsilon \xi} p_k = x_k + \varepsilon(\omega \times x_k + v) + O(\varepsilon^2)$, and the derivative of $r_k$ along $\varepsilon$ is $J_k \xi$. The derivative of $\rho$ is $\rho'(s) = \mu^2 / (\mu + s)^2 = l^\star(s)$. By the chain rule, the derivative of $\rho(|r_k|^2)$ is $l_k \cdot 2 r_k^{\mathsf T} J_k \xi$. Summing over $k$ gives $2 g^{\mathsf T} \xi$. $\square$

## Lemma 3: the matrix of the step

Let $H = \sum_k l_k J_k^{\mathsf T} J_k$. Then $H$ is positive semidefinite, and it is positive definite if and only if the points $x_1, \ldots, x_m$ do not all lie on one line.

*Proof.* $\xi^{\mathsf T} H \xi = \sum_k l_k |\omega \times x_k + v|^2 \ge 0$, and every $l_k > 0$ because $l^\star(s) > 0$ for finite $s$. So $\xi^{\mathsf T} H \xi = 0$ exactly when $\omega \times x_k + v = 0$ for all $k$. If $\omega = 0$, this forces $v = 0$. If $\omega \ne 0$, the solutions $x$ of $\omega \times x = -v$ form a line parallel to $\omega$ or the empty set. So a nonzero $\xi$ with $\xi^{\mathsf T} H \xi = 0$ exists if and only if all $x_k$ lie on one line. $\square$

## Theorem

Assume that the points $x_k$ do not all lie on one line. Then the step $\xi = -H^{-1} g$ of line L5:

1. minimizes the linearized cost $\sum_k l_k |r_k + J_k \xi|^2$ of the joint cost with $L$ fixed;
2. is zero if and only if $T$ is a stationary point of $E$ (in the sense that every directional derivative of Lemma 2 is zero);
3. is a descent direction when it is not zero: there is $\varepsilon_0 > 0$ such that $E(T_{\varepsilon \xi}) < E(T)$ for all $0 < \varepsilon < \varepsilon_0$.

*Proof.* (1) The linearized cost is $\sum_k l_k |r_k|^2 + 2 g^{\mathsf T} \xi + \xi^{\mathsf T} H \xi$, a strictly convex quadratic by Lemma 3; its minimizer solves $H \xi = -g$. (2) $H$ is invertible, so $\xi = 0$ if and only if $g = 0$, and by Lemma 2 $g = 0$ if and only if every directional derivative is zero. (3) By Lemma 2 the derivative of $E(T_{\varepsilon \xi})$ at $\varepsilon = 0$ is $2 g^{\mathsf T} \xi = -2 g^{\mathsf T} H^{-1} g$, which is negative when $g \ne 0$, because $H^{-1}$ is positive definite. A function with a negative derivative at 0 is below its value at 0 on a small interval $(0, \varepsilon_0)$. $\square$

## What this does not prove

- FGR takes the full step $\varepsilon = 1$. For this step, the theorem gives no decrease. A line search on $\varepsilon$ would give a monotone method at a fixed $\mu$; the paper and the reference code do not use one. In tests the full step decreased $E$ at a fixed $\mu$, but this is not a proof.
- Each change of $\mu$ changes the cost, so $E$ values at different $\mu$ are not comparable.
- A stationary point of $E$ need not be the global minimum. The large first $\mu$ makes the first cost close to least squares, which is easy to minimize, and the later costs are reached gradually; this is the idea of graduated non-convexity, and it helps in practice, but it is not a guarantee.
