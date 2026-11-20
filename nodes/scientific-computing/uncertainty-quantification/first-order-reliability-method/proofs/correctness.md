---
title: The HL-RF fixed points are the design point conditions, FORM is exact for a linear limit state, and the reliability index depends only on the failure set
proves: [correctness, termination]
status: full
---

We assume exact arithmetic and an exact gradient. The limit state in standard normal space is $G(u) = g(T(u))$, continuously differentiable, and $U$ is a standard normal vector in $\mathbb{R}^d$. The HL-RF map of line L4 is

$$H(u) = \frac{\nabla G(u)^{\mathsf T} u - G(u)}{\|\nabla G(u)\|^2}\, \nabla G(u), \qquad \nabla G(u) \neq 0.$$

A design point is a solution $u^*$ of $\min \|u\|$ subject to $G(u) = 0$. Put $\beta = \operatorname{sign}(G(0)) \|u^*\|$ and $\alpha = -\nabla G(u^*) / \|\nabla G(u^*)\|$.

**Lemma 1 (the step is a projection).** $H(u)$ is the point of smallest norm on the hyperplane $P_u = \{v : G(u) + \nabla G(u)^{\mathsf T} (v - u) = 0\}$, where the linearization of $G$ at $u$ vanishes.

*Proof.* Write $a = \nabla G(u)$ and $c = a^{\mathsf T} u - G(u)$, so $P_u = \{v : a^{\mathsf T} v = c\}$. For $v \in P_u$, the Cauchy-Schwarz inequality gives $|c| = |a^{\mathsf T} v| \le \|a\| \|v\|$, so $\|v\| \ge |c| / \|a\|$. The point $c a / \|a\|^2 = H(u)$ lies in $P_u$ and has norm $|c| / \|a\|$. $\square$

**Lemma 2 (the design point conditions).** Let $u^*$ be a design point with $G(0) \neq 0$ and $\nabla G(u^*) \neq 0$. Then $u^* = \lambda \nabla G(u^*)$ for a real $\lambda$, and $u^* = \beta \alpha$.

*Proof.* The gradient of the constraint is not zero, so the constraint is regular, and the first-order conditions for $\min \frac{1}{2}\|u\|^2$ subject to $G(u) = 0$ (the [KKT conditions](/kkt-conditions/) with one equality constraint) give $u^* - \mu \nabla G(u^*) = 0$ for a multiplier $\mu$; put $\lambda = \mu$. Now fix the sign. Since $G(0) \neq 0$ and $G(u^*) = 0$, $u^* \neq 0$, so $\lambda \neq 0$. For $0 \le t < 1$ the point $t u^*$ has norm less than $\|u^*\|$, so $G(t u^*) \neq 0$ by minimality, and by continuity $G(t u^*)$ has the sign of $G(0)$ on $[0, 1)$. Suppose $G(0) > 0$. Then $G(t u^*) > 0 = G(u^*)$ for $t < 1$, so the derivative $\frac{d}{dt} G(t u^*)$ at $t = 1$, which is $\nabla G(u^*)^{\mathsf T} u^* = \lambda \|\nabla G(u^*)\|^2$, is at most 0. So $\lambda < 0$, and $u^* = \lambda \nabla G(u^*) = |\lambda| \|\nabla G(u^*)\| \alpha$. Taking norms, $|\lambda| \|\nabla G(u^*)\| = \|u^*\| = \beta$, so $u^* = \beta \alpha$. If $G(0) < 0$ the same argument gives $\lambda > 0$ and $u^* = -\|u^*\| \alpha = \beta \alpha$. $\square$

**Lemma 3 (fixed points).** A point $u$ with $\nabla G(u) \neq 0$ is a fixed point of $H$ if and only if $G(u) = 0$ and $u = \lambda \nabla G(u)$ for a real $\lambda$.

*Proof.* Write $a = \nabla G(u)$. If $H(u) = u$, then $u = \lambda a$ with $\lambda = (a^{\mathsf T} u - G(u)) / \|a\|^2$. Multiply the first equation by $a^{\mathsf T}$: $a^{\mathsf T} u = \lambda \|a\|^2 = a^{\mathsf T} u - G(u)$, so $G(u) = 0$. Conversely, if $G(u) = 0$ and $u = \lambda a$, then $(a^{\mathsf T} u - 0) / \|a\|^2 = \lambda$ and $H(u) = \lambda a = u$. $\square$

So every design point is a fixed point of HL-RF (Lemmas 2 and 3), and every fixed point satisfies the first-order conditions of the design point problem. A fixed point need not be the global minimizer: it can be a local minimizer or a saddle point of $\|u\|$ on the surface.

**Lemma 4 (linear limit states).** Let $G(u) = a_0 + a^{\mathsf T} u$ with $a \neq 0$. Then $H(u) = -a_0 a / \|a\|^2$ for every $u$, this point is the design point, $\beta = a_0 / \|a\|$, and $\mathbb{P}[G(U) \le 0] = \Phi(-\beta)$ exactly.

*Proof.* Here $\nabla G = a$ and $a^{\mathsf T} u - G(u) = -a_0$, so $H(u) = -a_0 a / \|a\|^2$, the same point for every $u$. The surface $G = 0$ is the hyperplane $P_u$ itself, so by Lemma 1 this point is the design point, and its norm is $|a_0| / \|a\|$; with the sign of $G(0) = a_0$, $\beta = a_0 / \|a\|$. The variable $a^{\mathsf T} U$ is normal with mean 0 and variance $\|a\|^2$, so $\mathbb{P}[a_0 + a^{\mathsf T} U \le 0] = \mathbb{P}[Z \le -a_0 / \|a\|] = \Phi(-\beta)$ for a standard normal $Z$. $\square$

**Lemma 5 (invariance).** Let $G$ and $\tilde G$ have the same zero set, $\{G = 0\} = \{\tilde G = 0\}$, and let $G(0)$ and $\tilde G(0)$ have the same sign. Then they have the same design points and the same $\beta$.

*Proof.* The design point problem uses only the set $\{G = 0\}$ and the sign of $G(0)$. $\square$

For example, with $R, S > 0$ the functions $R - S$, $\ln R - \ln S$ and $R / S - 1$ all vanish exactly when $R = S$, and all are positive exactly when $R > S$, so they give the same $\beta$. A mean value index, $\mathbb{E}[g] / \operatorname{sd}(g)$ of a linearization at the mean, does not have this property.

**Theorem.** FORM stops after at most max_iter iterations of the loop. If $\nabla G$ is continuous and the iterates converge to a point $\bar u$ with $\nabla G(\bar u) \neq 0$, then $G(\bar u) = 0$ and $\bar u = \lambda \nabla G(\bar u)$, and if $\bar u$ is a design point, the returned values satisfy $\bar u = \beta \alpha$, with $\beta$ the Hasofer-Lind index. If $G$ is linear in $u$, FORM returns the design point after its second iteration, and $\Phi(-\beta)$ is the exact failure probability.

*Proof.* Termination: the loop of lines L2 to L5 runs at most max_iter times; each pass either raises an error for a zero gradient, stops at line L5, or continues, and after max_iter passes the code raises an error. Each pass does a finite amount of work. Limit: $H$ is continuous where $\nabla G \neq 0$, so $u_{k+1} = H(u_k)$ and $u_k \to \bar u$ give $H(\bar u) = \bar u$. Lemma 3 gives the conditions, and Lemma 2 gives $\bar u = \beta \alpha$ when $\bar u$ is a design point. Linear case: by Lemma 4 the first iterate is the design point and the second iterate equals the first, so the stopping test of line L5 holds at the second iteration, and the probability is exact by Lemma 4. $\blacksquare$

The theorem does not claim that the iterates converge. For a curved limit state, the HL-RF map can cycle or diverge, which Liu and Der Kiureghian showed; a line search on a merit function fixes this. The theorem also does not bound the error of $\Phi(-\beta)$ for a nonlinear limit state. The asymptotic formula of Breitung, which the page uses as a correction, is quoted and not proved here. With finite difference gradients, as in the reference code, the fixed point conditions hold only up to the difference error, which is why the stopping tolerance is $10^{-8}$ and not smaller.
