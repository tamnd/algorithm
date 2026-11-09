---
title: Natural gradient descent is invariant under linear changes of parameter, decreases L under bounded Fisher and a smooth L, and contracts exactly in mean parameters
proves: [correctness, convergence-rate]
status: full
---

**Setting.** $L : \Theta \to \mathbb{R}$, with $\Theta \subseteq \mathbb{R}^d$ open, is differentiable, and $F(\theta)$ is a symmetric positive definite matrix for each $\theta$ (the Fisher information, possibly with damping). The method is $\theta_{k+1} = \theta_k - \eta F(\theta_k)^{-1}\nabla L(\theta_k)$ with $\eta > 0$.

**Theorem 1 (linear invariance).** Let $\theta = B\xi + c$ with $B$ invertible, and define $\tilde{L}(\xi) = L(B\xi + c)$ and $\tilde{F}(\xi) = B^\top F(B\xi + c)B$, which is the Fisher information in the parameter $\xi$. Run the method on $(\tilde{L}, \tilde{F})$ from $\xi_0$ and on $(L, F)$ from $\theta_0 = B\xi_0 + c$, with the same $\eta$. Then $\theta_k = B\xi_k + c$ for every $k$.

*Proof.* By induction. If $\theta_k = B\xi_k + c$, then $\nabla\tilde{L}(\xi_k) = B^\top\nabla L(\theta_k)$ and

$$B\tilde{F}(\xi_k)^{-1}\nabla\tilde{L}(\xi_k) = B B^{-1}F(\theta_k)^{-1}B^{-\top}B^\top\nabla L(\theta_k) = F(\theta_k)^{-1}\nabla L(\theta_k).$$

So $B\xi_{k+1} + c = B\xi_k + c - \eta B\tilde{F}^{-1}\nabla\tilde{L} = \theta_k - \eta F(\theta_k)^{-1}\nabla L(\theta_k) = \theta_{k+1}$. $\blacksquare$

Plain gradient descent does not have this property: its step in $\xi$ maps to $-\eta BB^\top\nabla L(\theta_k)$, which depends on $B$. Damping $F + \lambda I$ also breaks it, because $\lambda I$ does not transform as $B^\top(\cdot)B$.

**Theorem 2 (nonlinear invariance of the direction).** Let $\theta = g(\xi)$ with $g$ a diffeomorphism and Jacobian $J(\xi)$, and $\tilde{F}(\xi) = J^\top F(g(\xi))J$. Then $J(\xi)\tilde{F}(\xi)^{-1}\nabla\tilde{L}(\xi) = F(\theta)^{-1}\nabla L(\theta)$ at $\theta = g(\xi)$.

*Proof.* The same computation as in Theorem 1, with $B$ replaced by $J(\xi)$. $\blacksquare$

So the continuous flow $\dot\theta = -F(\theta)^{-1}\nabla L(\theta)$ does not depend on the parameterization. A finite step does depend on it, at second order in $\eta$, because $g$ is curved.

**Theorem 3 (descent).** Assume $L$ is bounded below by $L_{\inf}$ and has an $\ell$-Lipschitz gradient on $\mathbb{R}^d$, and $mI \preceq F(\theta) \preceq MI$ for all $\theta$, with $0 < m \le M$. With the step $\eta = m/\ell$, each step satisfies

$$L(\theta_{k+1}) \le L(\theta_k) - \frac{m}{2\ell}\,\nabla L(\theta_k)^\top F(\theta_k)^{-1}\nabla L(\theta_k),$$

and for each $K \ge 1$

$$\min_{0 \le k < K}\lVert\nabla L(\theta_k)\rVert^2 \le \frac{2\ell M\big(L(\theta_0) - L_{\inf}\big)}{mK}.$$

*Proof.* Write $g = \nabla L(\theta_k)$, $F = F(\theta_k)$ and $d = F^{-1}g$. The descent lemma for an $\ell$-smooth function gives

$$L(\theta_k - \eta d) \le L(\theta_k) - \eta\langle g, d\rangle + \frac{\ell\eta^2}{2}\lVert d\rVert^2.$$

Here $\langle g, d\rangle = g^\top F^{-1}g$. Since $F \succeq mI$, $F^{-2} \preceq \frac{1}{m}F^{-1}$ (both sides have the same eigenvectors, with eigenvalues $1/\lambda^2 \le 1/(m\lambda)$), so $\lVert d\rVert^2 = g^\top F^{-2}g \le \frac{1}{m}g^\top F^{-1}g$. Therefore

$$L(\theta_{k+1}) \le L(\theta_k) - \eta\Big(1 - \frac{\ell\eta}{2m}\Big)g^\top F^{-1}g,$$

and $\eta = m/\ell$ gives the factor $\frac{m}{2\ell}$. Since $F \preceq MI$, $g^\top F^{-1}g \ge \lVert g\rVert^2/M$. Sum the first claim over $k < K$; the left side telescopes and is at least $-(L(\theta_0) - L_{\inf})$. So $\frac{m}{2\ell M}\sum_{k<K}\lVert\nabla L(\theta_k)\rVert^2 \le L(\theta_0) - L_{\inf}$, and the minimum is at most the average. $\blacksquare$

The bounds $m$ and $M$ hold with damping: if $0 \preceq F_0(\theta) \preceq CI$ and $F = F_0 + \lambda I$, then $m = \lambda$ and $M = C + \lambda$. Theorem 3 is a guarantee of the same kind as for gradient descent, and it does not show that natural gradient is faster. Its interest lies in the invariance and in the next result.

**Theorem 4 (exponential families in mean parameters).** Let $p(y;\eta) = h(y)\exp(\langle\eta, T(y)\rangle - A(\eta))$ be a minimal exponential family, so that $H(\eta) = \nabla^2A(\eta)$ is positive definite and $\mu = \nabla A(\eta)$ is a one-to-one map onto the open set $\mathcal{M}$ of mean parameters. Given data with $\bar{T} = \frac{1}{N}\sum_iT(y_i) \in \mathcal{M}$, let $L$ be the mean negative log-likelihood written as a function of $\mu$. Then the natural gradient step in $\mu$ is

$$\mu_{k+1} = \mu_k - \eta(\mu_k - \bar{T}), \qquad\text{so}\qquad \mu_k - \bar{T} = (1 - \eta)^k(\mu_0 - \bar{T}).$$

For $0 < \eta \le 1$ every iterate stays in $\mathcal{M}$, the error contracts by $1 - \eta$ in each step, and $\eta = 1$ gives the maximum likelihood estimate $\hat\mu = \bar{T}$ in one step.

*Proof.* In the natural parameter, $L(\eta) = A(\eta) - \langle\eta, \bar{T}\rangle$ up to a constant, so $\nabla_\eta L = \nabla A(\eta) - \bar{T} = \mu - \bar{T}$, and the Fisher information is $F_\eta = H$. The inverse map $\eta(\mu)$ has Jacobian $J = H^{-1}$ by the inverse function theorem. By the chain rule, $\nabla_\mu L = J^\top\nabla_\eta L = H^{-1}(\mu - \bar{T})$. By the change of parameters rule for the [Fisher information](/fisher-information-matrix/), $F_\mu = J^\top HJ = H^{-1}$. So $F_\mu^{-1}\nabla_\mu L = HH^{-1}(\mu - \bar{T}) = \mu - \bar{T}$. The iterate $\mu_{k+1} = (1 - \eta)\mu_k + \eta\bar{T}$ is a convex combination of two points of $\mathcal{M}$. For a regular family, $\mathcal{M}$ is the interior of the convex hull of the support of $T$, which is convex, so by induction all iterates lie in $\mathcal{M}$. For the families used here (Bernoulli, $\mathcal{M} = (0, 1)$; Poisson, $\mathcal{M} = (0, \infty)$) this is clear. $\blacksquare$

For the Bernoulli family, $\mu = q$, $\bar{T} = \bar{y}$, $\nabla_qL = (q - \bar{y})/(q(1 - q))$ and $F_q = 1/(q(1 - q))$, which the test file checks for several values of $\eta$.

**Theorem 5 (natural parameters: Newton's method).** In the natural parameter of an exponential family, and more generally for a generalized linear model with the canonical link, the Hessian of the mean negative log-likelihood equals the Fisher information, because $\nabla^2_\eta L = H$ does not depend on the data. Natural gradient descent with $\eta = 1$ is then exactly Newton's method, which for generalized linear models is called Fisher scoring.

*Proof.* For a canonical generalized linear model, $L(\theta) = \frac{1}{N}\sum_i(A(x_i^\top\theta) - y_ix_i^\top\theta)$, so $\nabla^2L(\theta) = \frac{1}{N}\sum_iA''(x_i^\top\theta)x_ix_i^\top$. The Fisher information of the conditional model is $\frac{1}{N}\sum_i\operatorname{Var}(y \mid x_i)x_ix_i^\top = \frac{1}{N}\sum_iA''(x_i^\top\theta)x_ix_i^\top$, the same matrix. $\blacksquare$
