---
title: Decoupled weight decay equals an L2 penalty for SGD but not for Adam
proves: [correctness]
status: full
---

We use the notation of the page. A run gets its gradients from an oracle $g(\theta, t)$, the minibatch gradient of the data loss at the point $\theta$ in step $t$; two runs that are at the same point in the same step get the same gradient. The L2 form adds $\lambda'\theta$ to the gradient, which is the gradient of $\frac{\lambda'}{2}\lVert\theta\rVert^2$. The decoupled form subtracts $\eta_t\lambda\theta$ from the weights. Here $\alpha > 0$, $\lambda, \lambda' \ge 0$, $\eta_t > 0$ and $\epsilon > 0$.

**Claim 1 (SGD).** Plain SGD with step $\alpha$ and L2 coefficient $\lambda'$, and SGD with decoupled decay $\lambda = \alpha\lambda'$ (with $\eta_t = 1$), give the same sequence $\theta_0, \theta_1, \ldots$ from the same start.

*Proof.* By induction on $t$. Both start at $\theta_0$. If both are at $\theta_t$ in step $t$, both get $g = g(\theta_t, t)$, and
$$\theta_t - \alpha\bigl(g + \lambda'\theta_t\bigr) = \theta_t - \alpha g - \alpha\lambda'\theta_t = \theta_t - \alpha g - \lambda\theta_t,$$
so both are at the same $\theta_{t+1}$. $\square$

With a schedule, the L2 run steps by $\eta_t\alpha(g + \lambda'\theta)$ and the decoupled run by $\eta_t(\alpha g + \lambda\theta)$; the same computation with $\lambda = \alpha\lambda'$ shows that they agree at every step.

**Claim 2 (SGD with momentum).** With the heavy ball buffer $b \leftarrow \beta b + \alpha(\cdot)$, the two forms are not the same, for any choice of $\lambda$ as a function of $\alpha$, $\beta$ and $\lambda'$.

*Proof.* Take $\theta_0 = (1, 2)$, the constant gradient $g = (\frac12, -1)$, $\alpha = \frac1{10}$, $\beta = \frac{9}{10}$ and $\lambda' = \frac1{10}$. After one step both forms are at $(\frac{47}{50}, \frac{52}{25})$ only if $\lambda = \alpha\lambda' = \frac1{100}$, since the first step of each form is the SGD step. After the second step, exact arithmetic gives $(\frac{4133}{5000}, \frac{2789}{1250})$ for the L2 form and $(\frac{2089}{2500}, \frac{5623}{2500})$ for the decoupled form. In the L2 form the term $\lambda'\theta_0$ of the first step stays in the buffer and is applied again with weight $\beta$; in the decoupled form it is not. $\square$

**Claim 3 (Adam).** For every $\alpha > 0$, $\lambda > 0$, $\beta_1, \beta_2 \in [0, 1)$ and $\epsilon > 0$, there is no $\lambda' \ge 0$ such that the first step of Adam with L2 coefficient $\lambda'$ equals the first step of AdamW with decay $\lambda$ (and $\eta_1 = 1$) for both starting points $\theta_0 = (1, 1)$ and $\theta_0 = (2, 2)$ with the data gradient $g = (1, 0)$.

*Proof.* In the first step the bias corrections give $\hat{m}_1 = \tilde{g}$ and $\hat{v}_1 = \tilde{g}^2$ coordinatewise, where $\tilde{g}$ is the gradient the method uses. So the first Adam step in coordinate $i$ is $\alpha\tilde{g}_i/(\lvert\tilde{g}_i\rvert + \epsilon)$.

Look at the second coordinate, whose data gradient is $0$, at the start $\theta_0 = (c, c)$ with $c \in \{1, 2\}$. AdamW uses $\tilde{g}_2 = 0$, so its Adam part is $0$ and its step is $\lambda c$. Adam with L2 uses $\tilde{g}_2 = \lambda' c$, so its step is $\alpha\lambda' c/(\lambda' c + \epsilon)$. Equality for $c = 1$ and $c = 2$ means
$$\lambda = \frac{\alpha\lambda'}{\lambda' + \epsilon} \quad\text{and}\quad 2\lambda = \frac{2\alpha\lambda'}{2\lambda' + \epsilon}.$$
If $\lambda' = 0$, the first equation gives $\lambda = 0$, a contradiction. If $\lambda' > 0$, both right sides are positive, and dividing gives $\lambda' + \epsilon = 2\lambda' + \epsilon$, so $\lambda' = 0$, again a contradiction. $\square$

The proof shows the reason. The L2 term of coordinate $i$ is divided by $\sqrt{\hat{v}_i} + \epsilon$, so its effect depends on the size of the gradients of that coordinate: for $\lambda'\theta_i \gg \epsilon$ the step of a weight with no data gradient is about $\alpha$, whatever $\lambda'$ is, and for a weight with large data gradients the decay is almost cancelled. Loshchilov and Hutter (2019) state the general form as their Proposition 2: for a preconditioner that is not a multiple of the identity, no L2 coefficient reproduces decoupled decay.

**Claim 4 (decay of an idle weight).** If coordinate $i$ has data gradient $0$ at every step, AdamW gives $\theta_{t,i} = \theta_{0,i}\prod_{s=1}^{t}(1 - \eta_s\lambda)$.

*Proof.* By induction, $m_i$ and $v_i$ stay $0$, so $\hat{m}_i/(\sqrt{\hat{v}_i} + \epsilon) = 0$ and line L8 reads $\theta_i \leftarrow \theta_i - \eta_t\lambda\theta_i = (1 - \eta_t\lambda)\theta_i$. $\square$

**Claim 5 (no decay).** With $\lambda = 0$ and $\lambda' = 0$, AdamW and Adam with L2 are both Adam and give the same sequence; this follows from lines L3 to L8 with $\lambda = 0$.
