---
title: The relative error of Laplace's method is O(1/n)
proves: [correctness, error]
status: full
---

We prove three facts. Theorem 1 is Laplace's method for an integral $\int g\, e^{n h}$ with a fixed $h$. Theorem 2 shows that the version of the page, which expands $\ell_n = n h + \log g$ at its own mode, has the same $O(1/n)$ relative error. Fact 3 is exactness for a Gaussian. Throughout, $\lvert \cdot \rvert$ is the Euclidean norm, and for a $k$-linear form $A$ we write $\lVert A \rVert = \sup_{\lvert u \rvert = 1} \lvert A[u, \ldots, u] \rvert$, so $\lvert A[u, \ldots, u] \rvert \le \lVert A \rVert\, \lvert u \rvert^k$.

## Theorem 1

**Hypotheses.** Let $\Theta \subseteq \mathbb{R}^d$ be open and $h, g : \Theta \to \mathbb{R}$ measurable.

- (A1) $h$ has a maximum at an interior point $\hat\theta$, and the maximum is well separated: for every $\delta > 0$, $\eta(\delta) = h(\hat\theta) - \sup_{\lvert \theta - \hat\theta \rvert \ge \delta} h(\theta) > 0$.
- (A2) $h$ is four times continuously differentiable on a closed ball $\bar B(\hat\theta, r_0) \subset \Theta$, and $H = -\nabla^2 h(\hat\theta)$ is positive definite. Let $\lambda > 0$ be its smallest eigenvalue.
- (A3) $g$ is twice continuously differentiable on $\bar B(\hat\theta, r_0)$ and $g(\hat\theta) \ne 0$.
- (A4) $\int_\Theta \lvert g \rvert\, e^{n_0 h}\, d\theta < \infty$ for some $n_0$.

**Claim.** As $n \to \infty$,

$$I_n = \int_\Theta g(\theta)\, e^{n h(\theta)}\, d\theta = e^{n h(\hat\theta)} \Big(\frac{2\pi}{n}\Big)^{d/2} \det(H)^{-1/2}\, g(\hat\theta)\, \big(1 + O(1/n)\big).$$

**Proof.** Translate so that $\hat\theta = 0$ and subtract a constant so that $h(0) = 0$. Then $h \le 0$ on $\Theta$ by (A1), and the claim is unchanged because both sides scale by the same factor $e^{n h(\hat\theta)}$.

*Constants.* Fix $\delta$ with $0 < \delta \le r_0$ and $\delta \le 3\lambda/(2 M_3)$, where $M_3 = \sup_{\lvert \theta \rvert \le r_0} \lVert \nabla^3 h(\theta) \rVert$ (if $M_3 = 0$ any $\delta \le r_0$ works). Let $M_4 = \sup_{\lvert \theta \rvert \le r_0} \lVert \nabla^4 h(\theta) \rVert$, $g_0 = g(0)$, $g_1 = \nabla g(0)$ and $G_2 = \sup_{\lvert \theta \rvert \le r_0} \lVert \nabla^2 g(\theta) \rVert$. All are finite because the derivatives are continuous on a compact ball.

*Step 1: the part outside the ball is exponentially small.* Let $\eta = \eta(\delta) > 0$. For $\lvert \theta \rvert \ge \delta$ we have $h(\theta) \le -\eta$, so for $n \ge n_0$

$$e^{n h(\theta)} = e^{n_0 h(\theta)}\, e^{(n - n_0) h(\theta)} \le e^{n_0 h(\theta)}\, e^{-(n - n_0)\eta}.$$

Hence $\big\lvert \int_{\lvert \theta \rvert \ge \delta} g\, e^{n h} \big\rvert \le e^{-(n - n_0)\eta} \int \lvert g \rvert e^{n_0 h} = O(e^{-n\eta})$ by (A4). The same bound with $h \le 0$ shows that $I_n$ exists for $n \ge n_0$.

*Step 2: rescale the ball.* Put $\theta = u/\sqrt n$. Then

$$\int_{\lvert \theta \rvert < \delta} g\, e^{n h}\, d\theta = n^{-d/2} \int_{\lvert u \rvert < \delta \sqrt n} g(u/\sqrt n)\, e^{-\frac12 u^\top H u}\, e^{\varphi_n(u)}\, du, \qquad \varphi_n(u) = n\, h(u/\sqrt n) + \tfrac12 u^\top H u.$$

Since $\nabla h(0) = 0$ and $\nabla^2 h(0) = -H$, Taylor's theorem with the Lagrange remainder gives, for $\lvert u \rvert < \delta\sqrt n$:

1. at order three, $\lvert \varphi_n(u) \rvert \le n \cdot M_3 \lvert u/\sqrt n \rvert^3/6 = M_3 \lvert u \rvert^3/(6\sqrt n)$;
2. at order four, $\varphi_n(u) = T(u)/(6\sqrt n) + R_n(u)$ with $T(u) = \nabla^3 h(0)[u, u, u]$ and $\lvert R_n(u) \rvert \le M_4 \lvert u \rvert^4/(24 n)$.

From item 1 and $\lvert u \rvert/\sqrt n < \delta$, $\lvert \varphi_n(u) \rvert \le M_3 \delta \lvert u \rvert^2/6 \le \lambda \lvert u \rvert^2/4$. Together with $u^\top H u \ge \lambda \lvert u \rvert^2$:

$$e^{-\frac12 u^\top H u}\, e^{\lvert \varphi_n(u) \rvert} \le e^{-\lambda \lvert u \rvert^2/4}. \tag{1}$$

For $g$: $g(u/\sqrt n) = g_0 + g_1 \cdot u/\sqrt n + \rho_n(u)$ with $\lvert \rho_n(u) \rvert \le G_2 \lvert u \rvert^2/(2n)$.

*Step 3: expand the integrand.* Write $e^{\varphi} = 1 + \varphi + r$ with $\lvert r \rvert \le \tfrac12 \varphi^2 e^{\lvert \varphi \rvert}$, and $e^{\varphi} - 1 = \varphi\, e^{\xi}$ for some $\xi$ between $0$ and $\varphi$, so $\lvert e^\varphi - 1 \rvert \le \lvert \varphi \rvert e^{\lvert \varphi \rvert}$. Then, dropping the argument $u$,

$$g(u/\sqrt n)\, e^{\varphi_n} = g_0 + \underbrace{\Big(\frac{g_0 T}{6\sqrt n} + \frac{g_1 \cdot u}{\sqrt n}\Big)}_{\text{odd in } u} + \underbrace{g_0 R_n + g_0 r + \frac{g_1 \cdot u}{\sqrt n}\big(e^{\varphi_n} - 1\big) + \rho_n e^{\varphi_n}}_{E_n(u)}.$$

The four terms of $E_n$ are bounded, with item 1 for $\varphi_n$, by

$$\lvert g_0 \rvert \frac{M_4 \lvert u \rvert^4}{24 n}, \quad \lvert g_0 \rvert \frac{M_3^2 \lvert u \rvert^6}{72 n} e^{\lvert \varphi_n \rvert}, \quad \lvert g_1 \rvert \frac{M_3 \lvert u \rvert^4}{6 n} e^{\lvert \varphi_n \rvert}, \quad \frac{G_2 \lvert u \rvert^2}{2 n} e^{\lvert \varphi_n \rvert}.$$

So $\lvert E_n(u) \rvert \le \frac{1}{n} P(\lvert u \rvert)\, e^{\lvert \varphi_n(u) \rvert}$ for a fixed polynomial $P$ that does not depend on $n$.

*Step 4: integrate.* The odd terms integrate to $0$ over the ball $\lvert u \rvert < \delta\sqrt n$, because the ball and $e^{-\frac12 u^\top H u}$ are symmetric under $u \mapsto -u$. By (1),

$$\Big\lvert \int_{\lvert u \rvert < \delta\sqrt n} E_n(u)\, e^{-\frac12 u^\top H u}\, du \Big\rvert \le \frac{1}{n} \int_{\mathbb{R}^d} P(\lvert u \rvert)\, e^{-\lambda \lvert u \rvert^2/4}\, du = \frac{C}{n}.$$

The constant term gives the Gaussian integral minus its tail:

$$g_0 \int_{\lvert u \rvert < \delta\sqrt n} e^{-\frac12 u^\top H u}\, du = g_0 (2\pi)^{d/2} \det(H)^{-1/2} - g_0 \int_{\lvert u \rvert \ge \delta\sqrt n} e^{-\frac12 u^\top H u}\, du,$$

and the tail is at most $\int_{\lvert u \rvert \ge \delta\sqrt n} e^{-\lambda \lvert u \rvert^2/2}\, du = O(e^{-\lambda \delta^2 n/4})$.

*Step 5: collect.* Steps 1 to 4 give

$$I_n = n^{-d/2}\Big(g_0 (2\pi)^{d/2} \det(H)^{-1/2} + O(1/n)\Big) + O(e^{-n\eta}).$$

The exponential terms are $o(n^{-d/2 - 1})$. Divide by $n^{-d/2} g_0 (2\pi)^{d/2}\det(H)^{-1/2}$, which is not zero by (A3). $\blacksquare$

## Theorem 2: the expansion at the mode of the log posterior

The page does not split the integrand into $g$ and $e^{nh}$. It takes $\ell_n = n h + \log g$ with $g > 0$, finds its mode $\tilde\theta_n$, and uses

$$A_n = e^{\ell_n(\tilde\theta_n)} (2\pi)^{d/2} \det\big(-\nabla^2 \ell_n(\tilde\theta_n)\big)^{-1/2}.$$

**Claim.** Under (A1) to (A4) and $g > 0$ on $\bar B(\hat\theta, r_0)$, for all large $n$ the function $\ell_n$ has exactly one critical point $\tilde\theta_n$ in the ball $\lvert \theta - \hat\theta \rvert \le K/n$ (for a constant $K$), it is a local maximum, and $A_n = I_n (1 + O(1/n))$.

**Proof.** Keep $\hat\theta = 0$, $h(0) = 0$ and the constants above. Let $G = \sup_{\lvert \theta \rvert \le r_0} \lvert \nabla \log g \rvert$ and $G' = \sup_{\lvert \theta \rvert \le r_0} \lVert \nabla^2 \log g \rVert$, finite by (A3) and $g > 0$.

*Existence and location.* For $\lvert \theta \rvert \le \delta$, Taylor at order three gives $h(\theta) \le -\frac12\theta^\top H \theta + M_3 \lvert \theta \rvert^3/6 \le -\lambda \lvert \theta \rvert^2/4$. Take $K = 8G/\lambda$ and $\rho = K/n$. On the sphere $\lvert \theta \rvert = \rho$,

$$\ell_n(\theta) - \ell_n(0) \le -\frac{n\lambda\rho^2}{4} + G\rho = \frac{K}{n}\Big(G - \frac{\lambda K}{4}\Big) = -\frac{GK}{n} < 0$$

(if $G = 0$, use any $K > 0$; the same steps give a strict inequality). So the maximum of the continuous $\ell_n$ on the closed ball $\lvert \theta \rvert \le \rho$ lies inside, and it is a critical point $\tilde\theta_n$ with $\lvert \tilde\theta_n \rvert < K/n$. On this ball $-\nabla^2 \ell_n = n(-\nabla^2 h) - \nabla^2 \log g$, and $-\nabla^2 h(\theta) \succeq (\lambda - M_3 \lvert \theta \rvert) I \succeq \frac{\lambda}{2} I$ for $\lvert \theta \rvert \le \lambda/(2 M_3)$, so $-\nabla^2 \ell_n \succeq (n\lambda/2 - G') I$ is positive definite for $n > 2G'/\lambda$. A strictly concave function has at most one critical point on a convex set, so $\tilde\theta_n$ is unique there.

*The value.* Since $\nabla \ell_n(\tilde\theta_n) = 0$, Taylor at order two around $\tilde\theta_n$ gives $\ell_n(0) = \ell_n(\tilde\theta_n) - \frac12 v^\top S v$ with $v = -\tilde\theta_n$ and $S = -\nabla^2 \ell_n$ at an intermediate point, $\lVert S \rVert \le n \sup \lVert \nabla^2 h \rVert + G' = O(n)$. Hence $\ell_n(\tilde\theta_n) - \ell_n(0) = O(n \cdot K^2/n^2) = O(1/n)$, and $e^{\ell_n(\tilde\theta_n)} = e^{n h(0)} g(0) (1 + O(1/n))$.

*The determinant.* $-\nabla^2 \ell_n(\tilde\theta_n)/n = H + \big(\nabla^2 h(0) - \nabla^2 h(\tilde\theta_n)\big) - \nabla^2 \log g(\tilde\theta_n)/n = H + O(M_3 K/n) + O(G'/n)$. The determinant is a polynomial in the entries, so $\det\big(-\nabla^2 \ell_n(\tilde\theta_n)\big) = n^d \det(H)\, (1 + O(1/n))$.

Multiply: $A_n = e^{n h(0)} g(0) (2\pi/n)^{d/2} \det(H)^{-1/2} (1 + O(1/n))$, which is $I_n(1 + O(1/n))$ by Theorem 1. $\blacksquare$

**Application to a posterior.** If the log-likelihood is $n h(\theta)$ for a fixed $h$ and the prior density is $g = \pi$, then $Z_n = \int \pi\, e^{n h} = I_n$ and $\hat Z_n = A_n$, so $\hat Z_n/Z_n = 1 + O(1/n)$. This covers $x = cn$ successes in $n$ Bernoulli trials with $c \in (0, 1)$ fixed: $h(p) = c\log p + (1 - c)\log(1 - p)$, maximized at $p = c$ with $H = 1/(c(1 - c))$. In the logit scale $\theta = \log(p/(1 - p))$ the same holds with $g(\theta) = \pi(p)\, p(1 - p)$. For data drawn at random, $h$ depends on $n$ through the data; then the same steps go through on the event that the derivative bounds and the separation hold uniformly in $n$. Kass, Tierney and Kadane (1990) give such conditions and prove $\hat Z_n/Z_n = 1 + O(1/n)$ under them. We cite that result and do not prove it here.

## Fact 3: exactness for a Gaussian

If $\ell(\theta) = c - \frac12(\theta - \mu)^\top Q (\theta - \mu)$ with $Q$ positive definite, then $\nabla \ell(\mu) = 0$, $-\nabla^2 \ell = Q$ everywhere, and

$$\int e^{\ell} d\theta = e^{c} (2\pi)^{d/2} \det(Q)^{-1/2} = e^{\ell(\hat\theta)} (2\pi)^{d/2} \det(-\nabla^2 \ell(\hat\theta))^{-1/2},$$

by the change of variables $\theta = \mu + Q^{-1/2} z$. So the approximation is exact. Newton's method reaches $\hat\theta = \mu$ in one full step from any start, because the quadratic model of $\ell$ is $\ell$ itself. $\blacksquare$
