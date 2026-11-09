---
title: The proximal gradient method decreases F and reaches the rate L_f R^2 / (2k)
proves: [correctness, convergence-rate]
status: full
---

**Assumptions.** $F = f + h$ on $\mathbb{R}^n$. The function $f$ is convex and differentiable, and $\nabla f$ is $L_f$-Lipschitz. The function $h$ is proper, closed and convex. The set of minimizers of $F$ is not empty; $x^*$ is one of them and $F^* = F(x^*)$. The step is a constant $t$ with $0 < t \le 1/L_f$, and $x_{k+1} = \operatorname{prox}_{th}(x_k - t\nabla f(x_k))$ (lines L2 and L3). For the strongly convex part, $f$ is also $\mu$-strongly convex with $\mu > 0$.

We use two facts.

- **Descent lemma.** If $\nabla f$ is $L_f$-Lipschitz, then $f(y) \le f(x) + \langle \nabla f(x), y - x\rangle + \frac{L_f}{2}\lVert y - x\rVert^2$ for all $x, y$ (the standard upper bound of an $L_f$-smooth function; see [smoothness](/smoothness/)).
- **Prox characterization.** $p = \operatorname{prox}_{th}(v)$ if and only if $(v - p)/t \in \partial h(p)$ (see [proximal operator](/proximal-operator/)).

**Lemma (one step).** Let $x \in \mathbb{R}^n$ and $x^+ = \operatorname{prox}_{th}(x - t\nabla f(x))$ with $0 < t \le 1/L_f$. Let $\mu \ge 0$ be a strong convexity constant of $f$ ($\mu = 0$ if $f$ is only convex). Then for every $z \in \mathbb{R}^n$,

$$F(x^+) \le F(z) + \frac{1}{2t}\Big( (1 - \mu t)\lVert x - z\rVert^2 - \lVert x^+ - z\rVert^2 \Big).$$

*Proof.* If $h(z) = +\infty$, the claim holds, so let $h(z)$ be finite. We bound the three parts of $F(x^+)$.

1. The descent lemma and $L_f \le 1/t$ give $f(x^+) \le f(x) + \langle \nabla f(x), x^+ - x\rangle + \frac{1}{2t}\lVert x^+ - x\rVert^2$.
2. Strong convexity (or convexity, when $\mu = 0$) at $x$ gives $f(x) \le f(z) - \langle \nabla f(x), z - x\rangle - \frac{\mu}{2}\lVert z - x\rVert^2$.
3. By the characterization, $g = (x - x^+)/t - \nabla f(x)$ is a subgradient of $h$ at $x^+$. So $h(z) \ge h(x^+) + \langle g, z - x^+\rangle$, that is, $h(x^+) \le h(z) + \frac{1}{t}\langle x - x^+, x^+ - z\rangle - \langle \nabla f(x), x^+ - z\rangle$.

Add the three lines. The gradient terms are $\langle \nabla f(x), x^+ - x\rangle - \langle \nabla f(x), z - x\rangle - \langle\nabla f(x), x^+ - z\rangle = 0$. What is left is

$$F(x^+) \le F(z) - \frac{\mu}{2}\lVert x - z\rVert^2 + \frac{1}{2t}\Big(2\langle x - x^+, x^+ - z\rangle + \lVert x^+ - x\rVert^2\Big).$$

With $a = x - x^+$ and $b = x^+ - z$, we have $a + b = x - z$, so $2\langle a, b\rangle + \lVert a\rVert^2 = \lVert a + b\rVert^2 - \lVert b\rVert^2 = \lVert x - z\rVert^2 - \lVert x^+ - z\rVert^2$. Put this in, and collect the two terms in $\lVert x - z\rVert^2$. $\square$

**Theorem 1 (monotone decrease).** $F(x_{k+1}) \le F(x_k) - \frac{1}{2t}\lVert x_{k+1} - x_k\rVert^2$ for each $k \ge 0$.

*Proof.* The lemma with $x = x_k$, $z = x_k$ and $\mu = 0$. $\square$

**Theorem 2 (Fejér monotonicity).** $\lVert x_{k+1} - x^*\rVert \le \lVert x_k - x^*\rVert$ for each $k \ge 0$.

*Proof.* The lemma with $z = x^*$ and $\mu = 0$ gives $0 \le F(x_{k+1}) - F^* \le \frac{1}{2t}(\lVert x_k - x^*\rVert^2 - \lVert x_{k+1} - x^*\rVert^2)$. $\square$

**Theorem 3 (sublinear rate).** For each $k \ge 1$,

$$F(x_k) - F^* \le \frac{\lVert x_0 - x^*\rVert^2}{2tk}, \qquad \text{and for } t = 1/L_f, \qquad F(x_k) - F^* \le \frac{L_f\lVert x_0 - x^*\rVert^2}{2k}.$$

*Proof.* By the proof of Theorem 2, for each $i \ge 0$, $F(x_{i+1}) - F^* \le \frac{1}{2t}(\lVert x_i - x^*\rVert^2 - \lVert x_{i+1} - x^*\rVert^2)$. Add these for $i = 0, \ldots, k-1$. The right side telescopes:

$$\sum_{i=1}^{k} \big(F(x_i) - F^*\big) \le \frac{1}{2t}\big(\lVert x_0 - x^*\rVert^2 - \lVert x_k - x^*\rVert^2\big) \le \frac{\lVert x_0 - x^*\rVert^2}{2t}.$$

By Theorem 1, $F(x_k) \le F(x_i)$ for each $i \le k$, so the left side is at least $k(F(x_k) - F^*)$. Divide by $k$. $\square$

**Theorem 4 (linear rate).** If $f$ is $\mu$-strongly convex with $\mu > 0$, then $\lVert x_k - x^*\rVert^2 \le (1 - \mu t)^k\lVert x_0 - x^*\rVert^2$ for each $k \ge 0$. For $t = 1/L_f$ the factor is $1 - \mu/L_f = 1 - 1/\kappa$.

*Proof.* The lemma with $x = x_k$ and $z = x^*$ gives $0 \le F(x_{k+1}) - F^* \le \frac{1}{2t}\big((1 - \mu t)\lVert x_k - x^*\rVert^2 - \lVert x_{k+1} - x^*\rVert^2\big)$. So $\lVert x_{k+1} - x^*\rVert^2 \le (1 - \mu t)\lVert x_k - x^*\rVert^2$, and $1 - \mu t \ge 0$ because $\mu \le L_f \le 1/t$. Induction on $k$ ends the proof. $\square$

**Fixed points.** If $x_{k+1} = x_k$, then $x_k$ is a minimizer: by the characterization, $-\nabla f(x_k) \in \partial h(x_k)$, so $0 \in \nabla f(x_k) + \partial h(x_k) = \partial F(x_k)$, and $F$ is convex. Conversely, a minimizer $x^*$ satisfies $-\nabla f(x^*) \in \partial h(x^*)$, so it is a fixed point of the step for every $t > 0$.
