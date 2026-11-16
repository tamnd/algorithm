---
title: The dog leg step stays in the trust region, decreases the model at least as much as the Cauchy point, and accepted steps lower the cost
proves: [correctness]
status: full
---

We use the notation of the page. At the current point, $r$ is the residual, $J$ the Jacobian with full column rank, $A = J^{\mathsf T} J$ (positive definite), $g = J^{\mathsf T} r \ne 0$, and $L(h) = \tfrac12 \|r + J h\|^2 = L(0) + g^{\mathsf T} h + \tfrac12 h^{\mathsf T} A h$ is the model. The steepest descent step is $a = -\alpha g$ with $\alpha = \|g\|^2 / \|J g\|^2$ (line L5), the Gauss-Newton step is $b = -A^{-1} g$ (line L6), and $\Delta > 0$ is the radius. The Cauchy point $p^C$ is the minimizer of $L$ on the set $\{-t g : t \ge 0, \|t g\| \le \Delta\}$.

**Claim.** (a) The step $h$ of lines L7 to L9 satisfies $\|h\| \le \Delta$, with equality unless $h = b$. (b) $L(h) \le L(p^C)$. (c) $L(0) - L(h) \ge \tfrac12 \|g\| \min(\Delta, \|g\| / \|A\|) > 0$. (d) Every accepted step of line L12 lowers $F$ strictly.

**Lemma 1 (the first leg).** For $0 \le t \le \alpha$, $L(-t g)$ decreases in $t$, and $L(0) - L(-t g) \ge \tfrac12 t \|g\|^2$.

*Proof.* $\phi(t) = L(-t g) = L(0) - t \|g\|^2 + \tfrac12 t^2 \|J g\|^2$ is a convex quadratic with minimum at $t = \|g\|^2 / \|J g\|^2 = \alpha$, so it decreases on $[0, \alpha]$. For $t \le \alpha$, $t \|J g\|^2 \le \|g\|^2$, so $L(0) - \phi(t) = t \|g\|^2 - \tfrac12 t^2 \|J g\|^2 \ge t \|g\|^2 - \tfrac12 t \|g\|^2$. $\square$

So $p^C = -t^* g$ with $t^* = \min(\alpha, \Delta / \|g\|)$: it is $a$ if $\|a\| \le \Delta$ and $-\Delta g / \|g\|$ otherwise.

**Lemma 2 (the second leg).** Let $p(\beta) = a + \beta (b - a)$ for $\beta \in [0, 1]$. Then $\|p(\beta)\|$ is nondecreasing and $L(p(\beta))$ is nonincreasing in $\beta$.

*Proof.* $L(p(\beta))$ is a convex quadratic in $\beta$. Its derivative at $\beta = 1$ is $(b - a)^{\mathsf T} (g + A b) = 0$, because $A b = -g$. The derivative of a convex function is nondecreasing, so it is $\le 0$ on $[0, 1]$.

For the norm, $\tfrac{d}{d\beta} \tfrac12 \|p(\beta)\|^2 = a^{\mathsf T} (b - a) + \beta \|b - a\|^2 \ge a^{\mathsf T} b - \|a\|^2$. Now $a^{\mathsf T} b = \alpha\, g^{\mathsf T} A^{-1} g$ and $\|a\|^2 = \alpha^2 \|g\|^2$, so $a^{\mathsf T} b - \|a\|^2 = \alpha \left( g^{\mathsf T} A^{-1} g - \frac{(g^{\mathsf T} g)^2}{g^{\mathsf T} A g} \right)$. By the Cauchy-Schwarz inequality for $u = A^{1/2} g$ and $v = A^{-1/2} g$, $(g^{\mathsf T} g)^2 = (u^{\mathsf T} v)^2 \le (g^{\mathsf T} A g)(g^{\mathsf T} A^{-1} g)$, so the bracket is $\ge 0$. $\square$

**Proof of (a).** There are three cases. Line L7: $\|b\| \le \Delta$ and $h = b$. Line L8: $\|a\| \ge \Delta$ and $h = -\Delta g / \|g\|$, of length $\Delta$. Line L9: $\|a\| < \Delta < \|b\|$. Then $\|p(0)\| < \Delta < \|p(1)\|$, and by Lemma 2 and continuity there is exactly one $\beta \in (0, 1)$ with $\|p(\beta)\| = \Delta$ (the norm is nondecreasing and its square is a strictly convex quadratic in $\beta$, so it cannot stay constant on an interval). With $d = b - a$, $c = a^{\mathsf T} d$ and $\rho_0 = \Delta^2 - \|a\|^2 > 0$, the equation is $\|d\|^2 \beta^2 + 2 c \beta - \rho_0 = 0$. Its roots have product $-\rho_0 / \|d\|^2 < 0$, so exactly one is positive, namely $\beta = (-c + \sqrt{c^2 + \|d\|^2 \rho_0}) / \|d\|^2$. The code uses the equal form $\rho_0 / (c + \sqrt{c^2 + \|d\|^2 \rho_0})$ when $c > 0$, to avoid cancellation; this is the formula (3.20b) of Madsen, Nielsen and Tingleff. So $\|h\| = \Delta$. $\square$

**Proof of (b).** In the case of line L7, $b$ minimizes $L$ on all of $\mathbb{R}^n$, so $L(b) \le L(p^C)$. In the case of line L8, $\|a\| \ge \Delta$, so $t^* = \Delta / \|g\|$ and $h = p^C$. In the case of line L9, $\|a\| < \Delta$, so $p^C = a = p(0)$, and $L(h) = L(p(\beta)) \le L(p(0))$ by Lemma 2. $\square$

**Proof of (c).** By (b) and Lemma 1 with $t = t^* \le \alpha$, $L(0) - L(h) \ge L(0) - L(p^C) \ge \tfrac12 t^* \|g\|^2 = \tfrac12 \|g\|^2 \min(\alpha, \Delta / \|g\|)$. Since $\|J g\|^2 = g^{\mathsf T} A g \le \|A\| \|g\|^2$, $\alpha \ge 1 / \|A\|$. So the decrease is at least $\tfrac12 \|g\| \min(\Delta, \|g\| / \|A\|)$, which is positive because $g \ne 0$. $\square$

**Proof of (d).** Line L12 accepts the step when $\rho = (F(x) - F(x + h)) / (L(0) - L(h)) > 0$. The denominator is positive by (c), so $F(x + h) < F(x)$. The reference code computes the denominator as $-g^{\mathsf T} h - \tfrac12 \|J h\|^2$ and stops if rounding makes it nonpositive, which only happens when no decrease is left to find. $\square$

**Global convergence.** Claim (c) is the Cauchy decrease condition of trust region theory (Nocedal and Wright, Lemma 4.3). With it, a trust region method that accepts every step with $\rho > 0$ and shrinks the radius after poor steps has $\liminf_k \|g_k\| = 0$, if $F$ is bounded below on the level set of $x_0$, has a Lipschitz gradient near it, and the model Hessians are bounded (Nocedal and Wright, Theorem 4.5). With an acceptance threshold $\eta > 0$, the whole sequence $g_k$ tends to zero (Theorem 4.6). Those theorems use a radius rule with a fixed upper bound and fixed shrink and grow factors. The rule of lines L13 and L14 is the one of Madsen, Nielsen and Tingleff (Algorithm 3.21), which has no upper bound on the radius, so the theorems apply to it only after adding such a bound. We do not claim more for the code as written.
