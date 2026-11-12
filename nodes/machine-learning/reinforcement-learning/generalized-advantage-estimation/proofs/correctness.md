---
title: The GAE recursion, its limits and its bias
proves: [correctness]
status: full
---

Notation is that of the page. The segment is $S_0, A_0, R_1, \ldots, S_T$ inside one episode; if the episode ends at step $T$, $V(S_T) = 0$. Let $\delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t)$, $m = T - t$, and let $G_t^{(n)} = \sum_{j=0}^{n-1} \gamma^j R_{t+j+1} + \gamma^n V(S_{t+n})$ for $1 \le n \le m$.

**Claim 1 (recursion).** After lines L1 to L5, $\hat A_t = \sum_{l=0}^{m-1} (\gamma\lambda)^l \delta_{t+l}$.

*Proof.* By downward induction on $t$. For $t = T - 1$, line L4 runs with $\hat A = 0$ and gives $\delta_{T-1}$, which is the sum with one term. If $\hat A_{t+1} = \sum_{l=0}^{m-2} (\gamma\lambda)^l \delta_{t+1+l}$, line L4 gives $\delta_t + \gamma\lambda \hat A_{t+1} = \delta_t + \sum_{l=1}^{m-1} (\gamma\lambda)^{l} \delta_{t+l}$. $\square$

**Lemma (telescoping).** $\sum_{l=0}^{n-1} \gamma^l \delta_{t+l} = G_t^{(n)} - V(S_t)$ for $1 \le n \le m$.

*Proof.* $\sum_{l=0}^{n-1} \gamma^l (R_{t+l+1} + \gamma V(S_{t+l+1}) - V(S_{t+l})) = \sum_{l=0}^{n-1} \gamma^l R_{t+l+1} + \sum_{l=1}^{n} \gamma^l V(S_{t+l}) - \sum_{l=0}^{n-1} \gamma^l V(S_{t+l})$, and the last two sums cancel except for $\gamma^n V(S_{t+n}) - V(S_t)$. $\square$

**Claim 2 (the λ-return and the limits).** $\hat A_t + V(S_t) = (1 - \lambda) \sum_{n=1}^{m-1} \lambda^{n-1} G_t^{(n)} + \lambda^{m-1} G_t^{(m)}$. In particular $\lambda = 0$ gives $\hat A_t = \delta_t$ (with $0^0 = 1$) and $\lambda = 1$ gives $\hat A_t = G_t^{(m)} - V(S_t)$.

*Proof.* Write $D_n = G_t^{(n)} - V(S_t) = \sum_{l=0}^{n-1} \gamma^l \delta_{t+l}$ by the lemma, and $D_0 = 0$. Then $\gamma^l \delta_{t+l} = D_{l+1} - D_l$, and by Claim 1, $\hat A_t = \sum_{l=0}^{m-1} \lambda^l (D_{l+1} - D_l)$. Summation by parts gives $\sum_{l=0}^{m-1} \lambda^l D_{l+1} - \sum_{l=1}^{m-1} \lambda^l D_l = \sum_{n=1}^{m-1} (\lambda^{n-1} - \lambda^n) D_n + \lambda^{m-1} D_m$. Since $(1 - \lambda)\sum_{n=1}^{m-1} \lambda^{n-1} + \lambda^{m-1} = 1$, adding $V(S_t)$ turns each $D_n$ into $G_t^{(n)}$. For $\lambda = 0$ only $n = 1$ remains, $G^{(1)}_t - V(S_t) = \delta_t$; for $\lambda = 1$ only $n = m$ remains. $\square$

For the next two claims, the segment is drawn from $\pi$, $\mathbb{E}[R_{t+1} \mid S_t = s, A_t = a] = r(s,a)$, and $Q^\pi(s, a) = r(s, a) + \gamma \sum_{s'} P(s' \mid s, a) V^\pi(s')$ with $V^\pi = 0$ at the end. Write $e = V - V^\pi$ (with $e = 0$ at the end) and $\mathcal{F}_t$ for the history up to $(S_t, A_t)$.

**Claim 3 (exact critic).** If $V = V^\pi$, then $\mathbb{E}[\hat A_t \mid S_t, A_t] = A^\pi(S_t, A_t)$ for every $\lambda \in [0, 1]$.

*Proof.* $\mathbb{E}[\delta_t \mid S_t = s, A_t = a] = r(s, a) + \gamma \sum_{s'} P(s' \mid s, a) V^\pi(s') - V^\pi(s) = Q^\pi(s, a) - V^\pi(s)$. For $l \ge 1$, condition on $S_{t+l}$ (on the event that the episode is still running; otherwise $\delta_{t+l}$ is not in the sum): $A_{t+l}$ has the law $\pi(\cdot \mid S_{t+l})$, so $\mathbb{E}[\delta_{t+l} \mid S_{t+l}] = \sum_a \pi(a \mid S_{t+l}) Q^\pi(S_{t+l}, a) - V^\pi(S_{t+l}) = 0$. By the tower rule $\mathbb{E}[\delta_{t+l} \mid S_t, A_t] = 0$. Claim 1 and linearity of expectation finish the proof. $\square$

**Claim 4 (approximate critic).** For any $V$, $\mathbb{E}[\hat A_t \mid S_t, A_t] = A^\pi(S_t, A_t) - e(S_t) + (1 - \lambda) \sum_{l=1}^{m-1} \gamma^l \lambda^{l-1} \mathbb{E}[e(S_{t+l}) \mid S_t, A_t] + (\gamma\lambda)^{m-1} \gamma\, \mathbb{E}[e(S_T) \mid S_t, A_t]$. If the episode ends at $T$, the last term is 0, and for $\lambda = 1$ the result is $Q^\pi(S_t, A_t) - V(S_t)$.

*Proof.* Write $\delta_k = \delta^\pi_k + \gamma e(S_{k+1}) - e(S_k)$, where $\delta^\pi_k$ is the TD error of $V^\pi$. By Claim 3 the $\delta^\pi$ part of $\hat A_t$ has mean $A^\pi(S_t, A_t)$. The $e$ part is $\sum_{l=0}^{m-1} (\gamma\lambda)^l (\gamma e(S_{t+l+1}) - e(S_{t+l}))$. Collect the coefficient of each $e(S_{t+l})$: for $l = 0$ it is $-1$; for $1 \le l \le m - 1$ it is $(\gamma\lambda)^{l-1}\gamma - (\gamma\lambda)^l = \gamma^l \lambda^{l-1}(1 - \lambda)$; for $l = m$ it is $(\gamma\lambda)^{m-1}\gamma$. Take conditional expectations. If the episode ends at $T$, $e(S_T) = 0$. For $\lambda = 1$ all middle coefficients vanish and what remains is $A^\pi(S_t, A_t) - e(S_t) = Q^\pi(S_t, A_t) - V(S_t)$. $\square$

**Consequence for the policy gradient.** For $\lambda = 1$ and a segment that ends with the episode, the error term $-e(S_t)$ depends on $S_t$ only, so $\mathbb{E}[e(S_t) \nabla \log \pi(A_t \mid S_t) \mid S_t] = e(S_t) \sum_a \nabla \pi(a \mid S_t) = 0$, and the policy gradient estimate is unbiased. For $\lambda < 1$ the terms $\mathbb{E}[e(S_{t+l}) \mid S_t, A_t]$ depend on $A_t$ through the transitions, so they do not cancel in general. $\blacksquare$
