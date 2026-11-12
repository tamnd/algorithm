---
title: The SAM perturbation maximizes the linearized loss, its error is second order, and its gradient on a quadratic
proves: [correctness]
status: full
---

**Setting.** $L$ is a differentiable loss on $\mathbb{R}^d$, $g = \nabla L(w) \ne 0$, $\rho > 0$, $1 < p \le \infty$ and $q$ the dual exponent, $1/p + 1/q = 1$. The SAM objective is $L^{\text{SAM}}(w) = \max_{\lVert\epsilon\rVert_p \le \rho} L(w + \epsilon)$. SAM uses
$$\hat{\epsilon} = \rho\,\operatorname{sign}(g)\,\lvert g\rvert^{q-1}\big/\bigl(\lVert g\rVert_q^q\bigr)^{1/p}$$
(entrywise), which for $p = 2$ is $\rho g/\lVert g\rVert_2$ and for $p = \infty$ is $\rho\operatorname{sign}(g)$, and it steps along $g^{\text{SAM}} = \nabla L(w + \hat{\epsilon})$.

**Claim 1 (maximizer of the linearization).** $\hat{\epsilon}$ maximizes $g^\top\epsilon$ over $\lVert\epsilon\rVert_p \le \rho$, with $\lVert\hat{\epsilon}\rVert_p = \rho$ and $g^\top\hat{\epsilon} = \rho\lVert g\rVert_q$.

*Proof.* By Hölder's inequality, $g^\top\epsilon \le \lVert g\rVert_q\lVert\epsilon\rVert_p \le \rho\lVert g\rVert_q$ for every feasible $\epsilon$. For $p < \infty$, $(q - 1)p = q$, so $\sum_i\lvert\hat{\epsilon}_i\rvert^p = \rho^p\sum_i\lvert g_i\rvert^q/\lVert g\rVert_q^q = \rho^p$. Also $g^\top\hat{\epsilon} = \rho\sum_i\lvert g_i\rvert^q/\lVert g\rVert_q^{q/p} = \rho\lVert g\rVert_q^{q - q/p} = \rho\lVert g\rVert_q$, since $q(1 - 1/p) = 1$. For $p = \infty$, $\hat{\epsilon} = \rho\operatorname{sign}(g)$ has $\lVert\hat{\epsilon}\rVert_\infty = \rho$ and $g^\top\hat{\epsilon} = \rho\lVert g\rVert_1$. So the bound is attained. $\square$

**Claim 2 (error of the approximation).** Let $p = 2$ and let $\nabla L$ be $\beta$-Lipschitz. Then
$$0 \le L^{\text{SAM}}(w) - L(w + \hat{\epsilon}) \le \beta\rho^2.$$

*Proof.* The lower bound holds because $\hat{\epsilon}$ is feasible. For the upper bound, smoothness gives $L(w + \epsilon) \le L(w) + g^\top\epsilon + \tfrac{\beta}{2}\lVert\epsilon\rVert^2 \le L(w) + \rho\lVert g\rVert + \tfrac{\beta}{2}\rho^2$ for every feasible $\epsilon$, by Claim 1, and $L(w + \hat{\epsilon}) \ge L(w) + g^\top\hat{\epsilon} - \tfrac{\beta}{2}\rho^2 = L(w) + \rho\lVert g\rVert - \tfrac{\beta}{2}\rho^2$. Subtract. $\square$

So replacing the inner maximization by one gradient evaluation loses only a term of order $\rho^2$ in the objective.

**Claim 3 (the dropped term).** If $L$ is twice differentiable and $g \ne 0$, the gradient of $w \mapsto L(w + \hat{\epsilon}(w))$ is $(I + D\hat{\epsilon}(w))^\top\nabla L(w + \hat{\epsilon})$, where for $p = 2$, $D\hat{\epsilon}(w) = \rho\bigl(I/\lVert g\rVert - gg^\top/\lVert g\rVert^3\bigr)\nabla^2L(w)$. SAM uses only the first term, $\nabla L(w + \hat{\epsilon})$.

*Proof.* The chain rule, with $D(g/\lVert g\rVert) = (I/\lVert g\rVert - gg^\top/\lVert g\rVert^3)\,Dg$ and $Dg = \nabla^2L(w)$. $\square$

The paper (Eq. 3) drops the second term to avoid Hessian vector products, and reports that keeping it made the results worse in their experiments.

**Claim 4 (quadratic loss).** For $L(w) = \tfrac12w^\top Hw + b^\top w$ with $H$ symmetric and $p = 2$, $g^{\text{SAM}} = g + \rho Hg/\lVert g\rVert$.

*Proof.* $\nabla L(w + \hat{\epsilon}) = H(w + \rho g/\lVert g\rVert) + b = (Hw + b) + \rho Hg/\lVert g\rVert$. $\square$

**Claim 5 (sharpness at a minimum).** If $H$ is positive semidefinite and $w^*$ minimizes the quadratic $L$, then $L^{\text{SAM}}(w^*) - L(w^*) = \tfrac12\rho^2\lambda_{\max}(H)$ for $p = 2$.

*Proof.* $L(w^* + \epsilon) - L(w^*) = \tfrac12\epsilon^\top H\epsilon$ because $\nabla L(w^*) = 0$, and the maximum of $\epsilon^\top H\epsilon$ over $\lVert\epsilon\rVert \le \rho$ is $\rho^2\lambda_{\max}(H)$ by the Rayleigh quotient. $\square$

So among minima of equal loss, the SAM objective is smaller at the one whose Hessian has the smaller top eigenvalue. The generalization bound of the paper (Theorem 1, a PAC-Bayes argument) is cited, not proved here.
