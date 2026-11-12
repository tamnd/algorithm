---
title: The LAMB step of each layer has norm eta_t phi(||x||) and is invariant to the scale of a normalized layer
proves: [correctness]
status: full
---

**Setting.** The parameters are split into layers $x^{(1)}, \ldots, x^{(h)}$. At step $t$, LAMB computes Adam's moments $m_t, v_t$ coordinatewise, the bias-corrected $\hat{m}_t = m_t/(1 - \beta_1^t)$ and $\hat{v}_t = v_t/(1 - \beta_2^t)$, the ratio $r_t = \hat{m}_t/(\sqrt{\hat{v}_t} + \epsilon)$, and for each layer $u^{(i)} = r_t^{(i)} + \lambda x_t^{(i)}$ and
$$x_{t+1}^{(i)} = x_t^{(i)} - \eta_t\,\frac{\phi(\lVert x_t^{(i)}\rVert)}{\lVert u^{(i)}\rVert}\,u^{(i)},$$
with the convention that the ratio is $1$ when $\lVert u^{(i)}\rVert = 0$ or $\phi(\lVert x_t^{(i)}\rVert) = 0$.

**Claim 1 (step norm).** If $u^{(i)} \ne 0$ and $\phi(\lVert x_t^{(i)}\rVert) > 0$, then $\lVert x_{t+1}^{(i)} - x_t^{(i)}\rVert = \eta_t\,\phi(\lVert x_t^{(i)}\rVert)$. With $\phi$ the identity and $x_t^{(i)} \ne 0$, every layer changes by the same relative amount $\lVert x_{t+1}^{(i)} - x_t^{(i)}\rVert/\lVert x_t^{(i)}\rVert = \eta_t$.

*Proof.* The step is $\eta_t\phi(\lVert x_t^{(i)}\rVert)$ times the unit vector $u^{(i)}/\lVert u^{(i)}\rVert$, and the norm is positively homogeneous. Divide by $\lVert x_t^{(i)}\rVert$ for the second statement. $\square$

The norm of the step does not depend on the gradient at all: the gradient, through Adam's moments, sets only the direction. With $\phi(z) = \min(\max(z, \gamma_l), \gamma_u)$ the step norm lies in $[\eta_t\gamma_l, \eta_t\gamma_u]$.

**Claim 2 (scale invariance of a normalized layer).** Take $\epsilon = 0$ and $\lambda = 0$. Suppose two runs on one layer differ by a factor $c > 0$: the second starts at $c\,x_1$, and whenever its iterate is $c\,x_t$ its gradient is $g_t/c$, where $g_t$ is the gradient of the first run at $x_t$. Then the second run's iterates are $c\,x_t$ for all $t$. This is the situation of a layer followed by batch or layer normalization, whose loss satisfies $\ell(cx) = \ell(x)$, so that $\nabla\ell(cx) = \nabla\ell(x)/c$, and $\phi$ the identity.

*Proof.* By induction on $t$. If the iterates are $x_t$ and $c\,x_t$ and all earlier gradients differ by the factor $1/c$, then the second run's $m_t$ is $m_t/c$ and its $v_t$ is $v_t/c^2$, since $m$ is linear and $v$ is quadratic in the gradients, so its ratio is $(\hat{m}_t/c)/\sqrt{\hat{v}_t/c^2} = r_t$, the same as the first run's. With $\lambda = 0$, $u$ is $r_t$ in both runs, and the step of the second run is $\eta_t\,c\lVert x_t\rVert\,r_t/\lVert r_t\rVert$, $c$ times the step of the first run. So the next iterate is $c\,x_{t+1}$, and by the assumption its gradient is $g_{t+1}/c$. $\square$

For [Adam](/adam/) the same two runs take the same steps, not steps scaled by $c$, so the relative change of the second layer is $1/c$ times that of the first: a layer with small weights changes by a large fraction. LAMB removes this dependence on the weight scale.

**Claim 3 (gradient scale).** With $\epsilon = 0$, multiplying all gradients of a coordinate by a constant $c > 0$ does not change $r_t$, and so does not change the iterates.

*Proof.* $\hat{m}_t$ scales by $c$ and $\sqrt{\hat{v}_t}$ by $c$. $\square$

**Convergence.** Theorem 3 of You and others (2020) bounds the expected gradient norm of LAMB on smooth nonconvex losses, under $\beta_1 = 0$, $\lambda = 0$, batch size $b = T$, a constant step size and $\alpha_l \le \phi \le \alpha_u$. With $\beta_2 = 0$ the bound is $O\bigl((f(x_1) - f(x^*))L_{\text{avg}}/T + \lVert\tilde{\sigma}\rVert_1^2/(Th)\bigr)$, where $L_{\text{avg}}$ is the average of the per layer smoothness constants; for SGD the comparable bound has the largest constant $L_\infty$. These theorems are cited, not proved here; the claims above are what the implementation tests check.
