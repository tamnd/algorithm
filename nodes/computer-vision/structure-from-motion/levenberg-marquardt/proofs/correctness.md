---
title: The Levenberg-Marquardt step always exists, its model decrease is positive, accepted steps lower the cost and a rejected step is followed by an accepted one
proves: [correctness]
status: full
---

We use the notation of the page. The residual is $r: \mathbb{R}^n \to \mathbb{R}^m$, $F(x) = \tfrac12 \|r(x)\|^2$, $J$ is the Jacobian at the current point $x$, $A = J^{\mathsf T} J$, $g = J^{\mathsf T} r$, and $L(h) = \tfrac12 \|r + J h\|^2$ is the linear model. $D$ is the scaling matrix: $D = I$ (Levenberg) or $D = \operatorname{diag}(A)$ (Marquardt). For the Marquardt form we assume that no column of $J$ is zero, so $D$ has a positive diagonal.

**Claim.** (a) For every $\mu > 0$ the matrix $A + \mu D$ is positive definite, so line L6 has a unique solution $h$, also when $J$ is rank deficient. (b) If $g \ne 0$, the predicted reduction of line L8 is $L(0) - L(h) = \tfrac12 h^{\mathsf T} (\mu D h - g) > 0$. (c) Every accepted step lowers $F$ strictly, so the stored costs decrease strictly. (d) If $g \ne 0$ and $r$ is continuously differentiable near $x$, then after finitely many rejections at the same $x$ a step is accepted. So the loop of lines L4 to L12 cannot reject forever at a point that is not stationary.

**Proof of (a).** $A$ is positive semidefinite, since $v^{\mathsf T} A v = \|J v\|^2 \ge 0$. $\mu D$ is positive definite. So $v^{\mathsf T} (A + \mu D) v \ge \mu v^{\mathsf T} D v > 0$ for $v \ne 0$. A positive definite matrix has a Cholesky factorization, and the system of line L6 has one solution. $\square$

**Proof of (b).** Expand $L(h) = L(0) + h^{\mathsf T} g + \tfrac12 h^{\mathsf T} A h$. Line L6 gives $A h = -g - \mu D h$, so $h^{\mathsf T} A h = -h^{\mathsf T} g - \mu h^{\mathsf T} D h$. Then
$$L(0) - L(h) = -h^{\mathsf T} g - \tfrac12 h^{\mathsf T} A h = -\tfrac12 h^{\mathsf T} g + \tfrac12 \mu\, h^{\mathsf T} D h = \tfrac12 h^{\mathsf T} (\mu D h - g).$$
If $g \ne 0$ then $h \ne 0$, so $\mu h^{\mathsf T} D h > 0$. Also $-h^{\mathsf T} g = h^{\mathsf T} (A + \mu D) h > 0$ by (a). Both terms are positive. $\square$

**Proof of (c).** Line L9 accepts the step only when $\rho = (F(x) - F(x + h)) / (L(0) - L(h)) > 0$. The denominator is positive by (b), because line L5 has already stopped the loop if $g = 0$ (in exact arithmetic). So $F(x + h) < F(x)$. Line L10 stores the new cost, so the stored costs decrease strictly. $\square$

**Proof of (d).** Each rejection in line L12 multiplies $\mu$ by $\nu \ge 2$ and doubles $\nu$, so after $j$ rejections $\mu \ge 2^j \mu_0$ and $\mu \to \infty$. Write $h_\mu$ for the step. From $(A + \mu D) h_\mu = -g$,
$$\mu h_\mu = -(D + A / \mu)^{-1} g \to -D^{-1} g \quad (\mu \to \infty),$$
so $\|h_\mu\| = O(1/\mu)$. Put $c = g^{\mathsf T} D^{-1} g > 0$. Then $-g^{\mathsf T} h_\mu = (c + o(1))/\mu$ and $\mu h_\mu^{\mathsf T} D h_\mu = (c + o(1))/\mu$, so by (b) the predicted reduction is $(c + o(1))/\mu$. Because $F$ is differentiable at $x$ with gradient $g$, $F(x) - F(x + h_\mu) = -g^{\mathsf T} h_\mu + o(\|h_\mu\|) = (c + o(1))/\mu$. Hence $\rho \to 1$ as $\mu \to \infty$, and for $\mu$ large enough $\rho > 0$, which is an accepted step. $\square$

**The step as a trust region step.** By (a) the step of line L6 minimizes $L(h) + \tfrac12 \mu h^{\mathsf T} D h$. So it is also the minimizer of $L$ over the ellipsoid $h^{\mathsf T} D h \le \Delta^2$ with $\Delta^2 = h^{\mathsf T} D h$: if some $h'$ in that set had $L(h') < L(h)$, then $L(h') + \tfrac12 \mu h'^{\mathsf T} D h' < L(h) + \tfrac12 \mu h^{\mathsf T} D h$, which contradicts the minimality. This is why a large $\mu$ gives a short step, and why the method is a trust region method with the radius controlled through $\mu$.

**What this proof does not show.** It shows monotone decrease and that the method never stalls in rejections at a non-stationary point. It does not show that the iterates converge. Moré (1978) proves, for a version that controls a trust region radius $\Delta$ and computes $\mu$ from it, that the gradients $g_k$ tend to zero at least along a subsequence when $r$ is continuously differentiable, and that the iterates converge to a stationary point under further conditions stated there. The $\mu$ update of line L11 follows Madsen, Nielsen and Tingleff (2004, Algorithm 3.16); they report its good behavior in tests, which is a benchmark result, not a theorem.

**The example of the page.** For $r(x) = (x + 1, -2x^2 + x - 1)$ the Gauss-Newton matrix at $x^* = 0$ is $A_* = 2$ and the second derivative term is $S_* = 4$. With a fixed $\mu$, the step near $0$ is $h = -(A + \mu)^{-1} g$ with $g = (A_* + S_*) e + O(e^2)$, so $e_+ = \frac{\mu - S_*}{A_* + \mu}\, e + O(e^2) = \frac{\mu - 4}{\mu + 2}\, e + O(e^2)$. For $\mu \approx 2.74$, the value of the run on the page, the factor is about $-0.266$, which explains the linear convergence with alternating signs that the run shows.
