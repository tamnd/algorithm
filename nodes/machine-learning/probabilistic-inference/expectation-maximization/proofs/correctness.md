---
title: EM never decreases the likelihood, and its interior fixed points are stationary
proves: [correctness]
status: full
---

We write the hidden data $z$ as discrete; for a continuous $z$ replace each sum by an integral. Fix the observed data $x$, and assume $p(x \mid \theta) > 0$ for the parameters we use. Write $\ell(\theta) = \log p(x \mid \theta)$ and $p_\theta(z) = p(z \mid x, \theta) = p(x, z \mid \theta) / p(x \mid \theta)$.

**Lemma 1 (the decomposition).** For every distribution $q$ on $z$ whose support is in the support of $p_\theta$, with $F(q, \theta) = \sum_z q(z) \log p(x, z \mid \theta) - \sum_z q(z) \log q(z)$,
$$\ell(\theta) = F(q, \theta) + \mathrm{KL}(q \,\|\, p_\theta).$$
So $\ell(\theta) \ge F(q, \theta)$, with equality if and only if $q = p_\theta$.

*Proof.* For each $z$ with $q(z) > 0$, $\log p(x, z \mid \theta) = \ell(\theta) + \log p_\theta(z)$. Multiply by $q(z)$ and sum over $z$; since $\sum_z q(z) = 1$,
$$\sum_z q(z) \log p(x, z \mid \theta) = \ell(\theta) + \sum_z q(z) \log p_\theta(z).$$
Subtract $\sum_z q(z) \log q(z)$ from both sides. The left side becomes $F(q, \theta)$, and the right side becomes $\ell(\theta) - \sum_z q(z) \log \frac{q(z)}{p_\theta(z)} = \ell(\theta) - \mathrm{KL}(q \,\|\, p_\theta)$. The KL divergence is nonnegative, and it is 0 only when $q = p_\theta$, by [Jensen's inequality](/jensens-inequality/) for the strictly concave $\log$: $-\mathrm{KL}(q \,\|\, p_\theta) = \sum_z q(z) \log \frac{p_\theta(z)}{q(z)} \le \log \sum_z p_\theta(z) \le 0$. $\square$

If the support condition fails for some $\theta$, then some $z$ with $q(z) > 0$ has $p(x, z \mid \theta) = 0$, so $F(q, \theta) = -\infty$ and the inequality $\ell(\theta) \ge F(q, \theta)$ still holds.

**Theorem 1 (monotonicity).** Let $\theta^{(t+1)}$ satisfy $Q(\theta^{(t+1)} \mid \theta^{(t)}) \ge Q(\theta^{(t)} \mid \theta^{(t)})$, which holds for the EM step of line L4 and for every GEM step. Then $\ell(\theta^{(t+1)}) \ge \ell(\theta^{(t)})$.

*Proof.* Let $q_t = p_{\theta^{(t)}}$, the result of the E step of line L3. By definition, $F(q_t, \theta) = Q(\theta \mid \theta^{(t)}) + H(q_t)$, where $H(q_t) = -\sum_z q_t(z) \log q_t(z)$ does not depend on $\theta$. So
$$\ell(\theta^{(t+1)}) \ge F(q_t, \theta^{(t+1)}) = Q(\theta^{(t+1)} \mid \theta^{(t)}) + H(q_t) \ge Q(\theta^{(t)} \mid \theta^{(t)}) + H(q_t) = F(q_t, \theta^{(t)}) = \ell(\theta^{(t)}).$$
The first inequality is Lemma 1 for $\theta^{(t+1)}$. The second is the hypothesis on the M step. The last equality is the equality case of Lemma 1, since $q_t = p_{\theta^{(t)}}$. $\square$

**Corollary.** If $\ell$ is bounded above on $\Theta$, the sequence $\ell(\theta^{(t)})$ is nondecreasing and bounded, so it converges. The equality $\ell(\theta^{(t+1)}) = \ell(\theta^{(t)})$ forces both inequalities above to be equalities; in particular $q_t = p_{\theta^{(t+1)}}$ and $\theta^{(t)}$ is also a maximizer of $Q(\cdot \mid \theta^{(t)})$ when $\theta^{(t+1)}$ is.

**Lemma 2 (Fisher's identity).** Let $\Theta$ be open in $\mathbb{R}^r$ and let $\theta \mapsto p(x, z \mid \theta)$ be differentiable for each $z$, with a finite sum over $z$ (or with differentiation under the integral allowed). Then for each $\theta' \in \Theta$,
$$\nabla_\theta Q(\theta \mid \theta')\big|_{\theta = \theta'} = \nabla \ell(\theta').$$

*Proof.* $\nabla \ell(\theta') = \frac{\nabla_\theta p(x \mid \theta')}{p(x \mid \theta')} = \sum_z \frac{\nabla_\theta p(x, z \mid \theta')}{p(x \mid \theta')} = \sum_z \frac{p(x, z \mid \theta')}{p(x \mid \theta')} \nabla_\theta \log p(x, z \mid \theta') = \sum_z p_{\theta'}(z)\, \nabla_\theta \log p(x, z \mid \theta')$, where a term with $p(x, z \mid \theta') = 0$ contributes 0 to each side, because then its gradient is 0 at this minimum of a nonnegative function. The last sum is the gradient of $Q(\theta \mid \theta')$ at $\theta = \theta'$. $\square$

**Theorem 2 (fixed points are stationary).** Under the conditions of Lemma 2, if $\theta^\ast$ is a fixed point of EM, that is, $\theta^\ast$ maximizes $Q(\cdot \mid \theta^\ast)$ over the open set $\Theta$, then $\nabla \ell(\theta^\ast) = 0$.

*Proof.* An interior maximizer of the differentiable function $Q(\cdot \mid \theta^\ast)$ has gradient 0. By Lemma 2 this gradient at $\theta^\ast$ is $\nabla \ell(\theta^\ast)$. $\square$

**What these results do not give.** Theorem 1 and its corollary give the convergence of the values $\ell(\theta^{(t)})$, not of the iterates, and Theorem 2 says nothing about the type of a stationary point. Wu (1983) gives the conditions under which every limit point of the iterates is a stationary point; the two coin example of the page shows a stationary point that is a saddle and that EM keeps forever from a symmetric start.
