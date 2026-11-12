---
title: The clipped objective matches the surrogate to first order and removes the incentive past the clip range
proves: [correctness]
status: full
---

Notation is that of the page. Fix a batch of samples $(S_t, A_t, \hat A_t)$ collected with $\pi_{\text{old}} = \pi_{\theta_{\text{old}}}$, with $\pi_{\text{old}}(A_t \mid S_t) > 0$, and $0 < \epsilon < 1$. For one sample write $r = r_t(\theta)$, $\hat A = \hat A_t$ and $\ell(r) = \min(r \hat A, \mathrm{clip}(r, 1-\epsilon, 1+\epsilon) \hat A)$. $\hat{\mathbb{E}}_t$ is the mean over the batch or a minibatch.

**Claim 1 (closed form).** If $\hat A > 0$, $\ell(r) = \min(r, 1+\epsilon) \hat A$. If $\hat A < 0$, $\ell(r) = \max(r, 1-\epsilon) \hat A$. If $\hat A = 0$, $\ell = 0$.

*Proof.* Let $\hat A > 0$. Then $\ell(r) = \hat A \min(r, \mathrm{clip}(r, 1-\epsilon, 1+\epsilon))$. If $r < 1 - \epsilon$, $\mathrm{clip}(r) = 1 - \epsilon > r$, so the minimum is $r$. If $1 - \epsilon \le r \le 1 + \epsilon$, both equal $r$. If $r > 1 + \epsilon$, the minimum is $1 + \epsilon$. In all cases the minimum is $\min(r, 1+\epsilon)$. For $\hat A < 0$, multiplying by $\hat A$ reverses the order, so $\ell(r) = \hat A \max(r, \mathrm{clip}(r))$, and the same case analysis gives $\max(r, 1-\epsilon)$. $\square$

**Claim 2 (pessimistic bound).** $\ell(r) \le r \hat A$ for every $r \ge 0$, with equality if $r \in [1-\epsilon, 1+\epsilon]$, or if $\hat A > 0$ and $r \le 1 + \epsilon$, or if $\hat A < 0$ and $r \ge 1 - \epsilon$. Hence $L^{\text{CLIP}}(\theta) \le L^{\text{CPI}}(\theta)$ for every $\theta$.

*Proof.* For $\hat A > 0$, $\min(r, 1+\epsilon) \le r$ with equality if and only if $r \le 1 + \epsilon$. For $\hat A < 0$, $\max(r, 1-\epsilon) \ge r$ and multiplying by $\hat A < 0$ gives $\ell(r) \le r\hat A$, with equality if and only if $r \ge 1 - \epsilon$. Averaging over samples gives the bound for the objectives. $\square$

**Claim 3 (slope).** Away from the kink $r = 1 + \epsilon$ (for $\hat A > 0$) or $r = 1 - \epsilon$ (for $\hat A < 0$), $\ell$ is differentiable with $\ell'(r) = \hat A$ if $\hat A > 0$ and $r < 1 + \epsilon$, or $\hat A < 0$ and $r > 1 - \epsilon$, and $\ell'(r) = 0$ otherwise. The gradient in $\theta$ is $\ell'(r)\, r\, \nabla_\theta \log \pi_\theta(A_t \mid S_t)$.

*Proof.* By Claim 1, $\ell$ is linear with slope $\hat A$ on one side of the kink and constant on the other. The chain rule and $\nabla_\theta r = \nabla_\theta \pi_\theta(A_t \mid S_t) / \pi_{\text{old}}(A_t \mid S_t) = r \nabla_\theta \log \pi_\theta(A_t \mid S_t)$ give the gradient. $\square$

**Claim 4 (first-order match).** At $\theta = \theta_{\text{old}}$, $L^{\text{CLIP}} = L^{\text{CPI}} = \hat{\mathbb{E}}_t[\hat A_t]$, and $\nabla_\theta L^{\text{CLIP}} = \nabla_\theta L^{\text{CPI}} = \hat{\mathbb{E}}_t[\hat A_t \nabla_\theta \log \pi_\theta(A_t \mid S_t)]$.

*Proof.* At $\theta_{\text{old}}$ every ratio is 1, which lies in the open interval $(1-\epsilon, 1+\epsilon)$. So by Claim 2 the two objectives agree on a neighbourhood of $\theta_{\text{old}}$ (the ratios are continuous in $\theta$), so their values and gradients agree there. By Claim 3 with $r = 1$, each sample contributes $\hat A_t \nabla \log \pi_\theta(A_t \mid S_t)$. $\square$

With $\hat A_t$ an unbiased estimate of the advantage, as in GAE with $\lambda = 1$ or with an exact critic, the expectation of the gradient in Claim 4 is the policy gradient by the policy gradient theorem; so the first update of each iteration is an unbiased policy gradient step.

**Claim 5 (no push past the clip range).** If a sample has $\hat A > 0$ and $r > 1 + \epsilon$, or $\hat A < 0$ and $r < 1 - \epsilon$, its gradient is 0. If a batch has a single sample in a state $s$ with tabular parameters for $s$, then once its ratio passes the clip range in this way, further updates leave the parameters of $s$ unchanged.

*Proof.* The first sentence is Claim 3. For the second, with tabular parameters the gradient of the objective with respect to the parameters of $s$ is the sum of the gradients of the samples in $s$, which here is the gradient of the single sample, which is 0. So line L7 does not change those parameters, the ratio does not change, and the same holds at every later update. $\square$

Claims 2 to 5 are the properties that the page uses: the clipped objective is a lower bound of the TRPO surrogate that agrees with it near the old policy, has the policy gradient as its initial gradient, and gives no reward for moving a ratio past $1 \pm \epsilon$ in the direction that its advantage favours. $\blacksquare$
