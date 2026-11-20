---
title: The RLTV step is a scaled gradient step, its positive fixed points minimize the regularized Poisson objective, and it keeps the estimate nonnegative for lam < 1/4
proves: [correctness]
status: full
---

**Setting.** Images have $n$ pixels on a periodic grid. The blur is periodic convolution $Ax = h \ast x$ with $h \ge 0$ and $\sum h = 1$, and the adjoint $A^\ast$ is correlation, $A^\ast v = \tilde h \ast v$ with $\tilde h(r) = h(-r)$. The data $y \ge 0$ are counts. For $x > 0$ with $Ax > 0$ define

$$L(x) = \sum_i \big[(Ax)_i - y_i \log (Ax)_i\big], \qquad T_\varepsilon(x) = \sum_i \sqrt{(\nabla_1 x)_i^2 + (\nabla_2 x)_i^2 + \varepsilon^2}, \qquad J(x) = L(x) + \lambda T_\varepsilon(x),$$

with forward differences $(\nabla_1 x)_{i,j} = x_{i+1,j} - x_{i,j}$ and $(\nabla_2 x)_{i,j} = x_{i,j+1} - x_{i,j}$, and $\operatorname{div}$ the backward difference operator, so that $\langle \nabla x, p\rangle = -\langle x, \operatorname{div} p\rangle$. Write

$$c = A^\ast\!\left(\frac{y}{Ax}\right), \qquad \kappa = \operatorname{div}\!\left(\frac{\nabla x}{|\nabla x|_\varepsilon}\right), \qquad |g|_\varepsilon = \sqrt{g_1^2 + g_2^2 + \varepsilon^2}.$$

Lines L3 to L6 compute $x^+ = x\, c / (1 - \lambda\kappa)$, entry by entry, with $\lambda \ge 0$ and $\varepsilon > 0$.

**Claim 1 (gradients).** $\nabla L(x) = \mathbf 1 - c$ and $\nabla T_\varepsilon(x) = -\kappa$.

*Proof.* $\partial L/\partial x_j = \sum_i A_{ij}(1 - y_i/(Ax)_i) = (A^\ast \mathbf 1)_j - c_j$, and $A^\ast \mathbf 1 = \sum h = 1$ at every pixel. For $T_\varepsilon$, the derivative of $\sqrt{|g|^2 + \varepsilon^2}$ in $g$ is $g/|g|_\varepsilon$, so by the chain rule $\nabla T_\varepsilon = \nabla^\ast(\nabla x / |\nabla x|_\varepsilon) = -\operatorname{div}(\nabla x/|\nabla x|_\varepsilon) = -\kappa$. $\square$

**Claim 2 (a scaled gradient step).** If $1 - \lambda\kappa > 0$ at every pixel, then

$$x^+ - x = -\frac{x}{1 - \lambda\kappa}\, \nabla J(x).$$

*Proof.* By Claim 1, $\nabla J = \mathbf 1 - c - \lambda\kappa$. So $x\,c/(1 - \lambda\kappa) - x = x\,(c - 1 + \lambda\kappa)/(1 - \lambda\kappa) = -x \nabla J/(1 - \lambda\kappa)$. $\square$

This is the one-step-late form of Green (1990): the derivative of the prior is taken at the current estimate and placed in the denominator of the EM step.

**Claim 3 (fixed points).** Let $x > 0$ at every pixel with $1 - \lambda\kappa > 0$. Then $x^+ = x$ if and only if $\nabla J(x) = 0$, and then $x$ is a global minimizer of $J$ over the set $\{x \ge 0,\ Ax > 0\}$.

*Proof.* The scale $x/(1 - \lambda\kappa)$ in Claim 2 is positive, so $x^+ = x$ exactly when $\nabla J(x) = 0$. $L$ is convex, because $-\log$ is convex and $Ax$ is linear in $x$. $T_\varepsilon$ is convex, because $g \mapsto |g|_\varepsilon$ is a norm of $(g_1, g_2, \varepsilon)$ composed with an affine map. So $J$ is convex, and a point where its gradient is zero is a global minimizer on the convex domain where $J$ is defined. $\square$

**Claim 4 (the denominator is positive for lam < 1/4).** Every entry of $\kappa$ lies in $[-4, 4]$. So for $0 \le \lambda < 1/4$, $1 - \lambda\kappa \ge 1 - 4\lambda > 0$ at every pixel and every $x$.

*Proof.* Let $p = \nabla x / |\nabla x|_\varepsilon$. Then $|p_1| \le 1$ and $|p_2| \le 1$, because $|g_1| \le |g|_\varepsilon$. The entry $\kappa_{i,j} = p_{1;i,j} - p_{1;i-1,j} + p_{2;i,j} - p_{2;i,j-1}$ is a sum of four terms of modulus at most $1$. $\square$

In $d$ dimensions the same argument gives $|\kappa| \le 2d$, so $\lambda < 1/(2d)$; for 3D stacks, $\lambda < 1/6$.

**Claim 5 (nonnegativity).** If $x \ge 0$, $Ax > 0$ where $y > 0$, and $1 - \lambda\kappa > 0$, then $x^+ \ge 0$. A pixel with $x_j = 0$ stays $0$.

*Proof.* $c = A^\ast(y/Ax)$ is a sum of nonnegative terms, so $c \ge 0$. The factors $x$, $c$ and $1/(1 - \lambda\kappa)$ are nonnegative. $\square$

With Claim 4, the iteration started from a positive image never leaves the nonnegative orthant when $\lambda < 1/4$, without any clipping. For larger $\lambda$ the denominator can become zero or negative at a local minimum of $x$, where $\kappa > 0$; the code raises an error then.

**Claim 6 (lam = 0 is Richardson-Lucy).** For $\lambda = 0$, $x^+ = x\, A^\ast(y/Ax)$, the EM step for Poisson data with $A^\ast\mathbf 1 = \mathbf 1$. Then $L(x^+) \le L(x)$ (the EM monotonicity theorem), and $\sum_j x^+_j = \sum_{i:\,y_i > 0} y_i$.

*Proof.* The first part is the EM update with column sums $1$. For the sum, $\sum_j x_j c_j = \sum_j x_j \sum_i h_{i-j}\, y_i/(Ax)_i = \sum_{i:\, y_i > 0} y_i\, (Ax)_i/(Ax)_i$. $\square$

**What is not claimed.** For $\lambda > 0$ the step is not an EM step, and Claim 2 does not give a descent: the scaled gradient step has no step size control. $J$ need not decrease, and the iterates need not converge. A measurement in the page shows both effects. $\blacksquare$
