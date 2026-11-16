---
title: The trust region loop terminates with a merit that never increases, every step is accepted for convex obstacles, and a stop with zero predicted decrease is a stationary point
proves: [correctness]
status: full
---

We use the notation of the page and of the code. The free waypoints are $x = (x_1, \dots, x_n)$ with fixed ends $x_0 = q_0$ and $x_{n+1} = q_{n+1}$. The constraints are indexed by $k$; constraint $k$ asks $\mathrm{sd}_k(x_{t_k}) \ge d_{\text{safe}}$ for a waypoint $t_k$ and a signed distance function $\mathrm{sd}_k$. For a penalty weight $\mu > 0$ the merit is

$$\varphi(x) = f(x) + \mu \sum_k \max\bigl(0,\ d_{\text{safe}} - \mathrm{sd}_k(x_{t_k})\bigr), \qquad f(x) = \sum_{t=0}^n \|x_{t+1} - x_t\|^2.$$

At the current point $\bar x$, line L4 computes $v_k = \mathrm{sd}_k(\bar x_{t_k})$ and a vector $g_k$ (the gradient where it exists, and $0$ at the center of a disc). The model of line L5 is

$$\hat\varphi(\delta) = f(\bar x + \delta) + \mu \sum_k \max\bigl(0,\ d_{\text{safe}} - v_k - g_k^{\mathsf T}\delta_{t_k}\bigr),$$

a convex function of $\delta$: $f$ is a convex quadratic, and each penalty term is the maximum of $0$ and an affine function. Note $\hat\varphi(0) = \varphi(\bar x)$. Line L5 returns some $\delta$ with $\|\delta\|_\infty < \Delta$: the barrier method keeps its iterates strictly inside the box. Line L6 computes $\mathrm{pred} = \hat\varphi(0) - \hat\varphi(\delta)$ for this $\delta$, and line L7 computes the ratio $\rho = (\varphi(\bar x) - \varphi(\bar x + \delta))/\mathrm{pred}$. The arguments below use only these definitions; they do not need $\delta$ to be an exact minimizer, except in Theorem 3.

## Theorem 1: termination and monotone merit

**Claim.** For a fixed $\mu$, every step accepted by line L8 satisfies $\varphi(\bar x + \delta) \le \varphi(\bar x) - c\,\mathrm{xtol}$. The loop of lines L3 to L9 ends after finitely many passes, and the whole method ends after at most `outer` values of $\mu$.

*Proof.* A step is tried only if $\mathrm{pred} > \mathrm{xtol}$ (line L6), and accepted only if $\rho \ge c$ (line L8). Then $\varphi(\bar x) - \varphi(\bar x + \delta) = \rho\,\mathrm{pred} \ge c\,\mathrm{pred} > c\,\mathrm{xtol}$. So the merit drops by more than $c\,\mathrm{xtol}$ at each accepted step. The merit is a sum of nonnegative terms, so for a fixed $\mu$ the number $a$ of accepted steps is less than $\varphi(x^{\text{start}})/(c\,\mathrm{xtol}) + 1$.

Each rejected step multiplies $\Delta$ by $\tau_- = 1/2$, and each accepted step multiplies it by at most $\tau_+ = 3/2$. The loop continues only while $\Delta \ge \Delta_{\min}$. Let $\Delta_s$ be the value of $\Delta$ when the loop starts. If there were $r \ge 1$ rejections, then after the first $r - 1$ of them the loop was still running, so $\Delta_{\min} \le \Delta \le \Delta_s (3/2)^a 2^{-(r-1)}$, and $r \le 1 + a\log_2(3/2) + \log_2(\Delta_s/\Delta_{\min})$. Both counts are finite, so the inner loop ends. The outer loop of lines L2 to L11 runs at most `outer` times. $\square$

## Theorem 2: convex obstacles give a model that is an upper bound

**Claim.** If every $\mathrm{sd}_k$ is convex and $g_k$ is a subgradient of $\mathrm{sd}_k$ at $\bar x_{t_k}$, then $\varphi(\bar x + \delta) \le \hat\varphi(\delta)$ for every $\delta$. Hence $\rho \ge 1$ whenever $\mathrm{pred} > 0$, and with $c \le 1$ line L8 accepts every step that is tried.

*Proof.* The subgradient inequality gives $\mathrm{sd}_k(\bar x_{t_k} + \delta_{t_k}) \ge v_k + g_k^{\mathsf T}\delta_{t_k}$. The map $u \mapsto \max(0, d_{\text{safe}} - u)$ is nonincreasing, so each true penalty term is at most the model penalty term. The smoothness part is the same function $f(\bar x + \delta)$ in both. So $\varphi(\bar x + \delta) \le \hat\varphi(\delta)$, which gives $\varphi(\bar x) - \varphi(\bar x + \delta) \ge \hat\varphi(0) - \hat\varphi(\delta) = \mathrm{pred}$, that is, $\rho \ge 1$.

For a disc, $\mathrm{sd}(p) = \|p - o\| - r$ is convex as a norm minus a constant. Its gradient $(p - o)/\|p - o\|$ is a subgradient for $p \ne o$, and at $p = o$ the vector $0$ is a subgradient because $\|p' - o\| \ge 0$. The code uses exactly these vectors. $\square$

So for a point robot among disc obstacles, the trust region in this code never rejects a step; it only limits the step length. For constraints that are not convex, such as the inside of a circle (a concave $\mathrm{sd}$) or the distance between the links of a robot arm and an obstacle as a function of the joint angles, the model can be too optimistic and line L8 can reject steps. Theorem 1 covers that case too.

## Theorem 3: what a stop with no predicted decrease means

**Claim.** Suppose that line L5 returns an exact minimizer of $\hat\varphi$ over the box $\|\delta\|_\infty \le \Delta$ with $\Delta > 0$, that $\mathrm{pred} = 0$, and that each $\mathrm{sd}_k$ is differentiable at $\bar x_{t_k}$ with gradient $g_k$. Then the one-sided directional derivative of $\varphi$ at $\bar x$ is nonnegative in every direction $w$:

$$\varphi'(\bar x; w) = \lim_{s \downarrow 0} \frac{\varphi(\bar x + s w) - \varphi(\bar x)}{s} \ge 0.$$

*Proof.* $\mathrm{pred} = 0$ means that $\delta = 0$ minimizes $\hat\varphi$ over the box. For $s > 0$ small enough, $sw$ is in the box, so $\hat\varphi(sw) \ge \hat\varphi(0)$, and hence $\hat\varphi'(0; w) \ge 0$.

Now compare the directional derivatives term by term. The smoothness terms are the same differentiable function. Take one penalty term and put $a_k = d_{\text{safe}} - v_k$. In the model, the term is $h(s) = \max(0, a_k - s\, g_k^{\mathsf T} w_{t_k})$; in the merit it is $\tilde h(s) = \max(0, a_k - (\mathrm{sd}_k(\bar x_{t_k} + s w_{t_k}) - v_k))$, and $\mathrm{sd}_k(\bar x_{t_k} + s w_{t_k}) - v_k = s\, g_k^{\mathsf T} w_{t_k} + o(s)$. If $a_k > 0$, both terms are positive for small $s$, and both have the right derivative $-g_k^{\mathsf T} w_{t_k}$. If $a_k < 0$, both are zero for small $s$. If $a_k = 0$, then $h(s) = s \max(0, -g_k^{\mathsf T} w_{t_k})$ and $\tilde h(s) = s\max(0, -g_k^{\mathsf T} w_{t_k}) + o(s)$, since $u \mapsto \max(0, u)$ is 1-Lipschitz. So the right derivatives agree term by term, $\varphi'(\bar x; w) = \hat\varphi'(0; w) \ge 0$. $\blacksquare$

## What is not proved

Theorem 3 is a first-order condition for the penalized merit, not for the constrained problem. If the final point still violates a constraint, line L10 fails and line L11 increases $\mu$; with a large enough $\mu$, an $\ell_1$ penalty has the same local solutions as the constrained problem under standard regularity conditions, but this page does not prove that, and if no feasible trajectory is near, $\mu$ only grows until the outer limit. Nothing says that the stationary point is a global minimum: the method is local, and a start line on the other side of an obstacle leads to a different answer. Finally, the constraints hold at the waypoints only; the segments between waypoints can still cut into an obstacle.
