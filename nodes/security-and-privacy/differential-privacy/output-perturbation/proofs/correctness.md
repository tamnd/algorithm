---
title: Output perturbation of regularized ERM is epsilon-DP
proves: [correctness]
status: full
---

The data is $D = ((x_1, y_1), \ldots, (x_n, y_n))$ with $\|x_i\| \le 1$ and $y_i \in \{-1, +1\}$. The neighbor relation is replace: $D'$ differs from $D$ in one example. The loss $\ell : \mathbb R \to \mathbb R$ is convex and differentiable with $|\ell'(z)| \le 1$ for all $z$; the logistic loss $\ell(z) = \ln(1 + e^{-z})$ has $\ell'(z) = -1/(1 + e^{z}) \in (-1, 0)$. Let

$$J_D(f) = \frac1n \sum_{i=1}^n \ell(y_i f^{\mathsf T} x_i) + \frac{\Lambda}{2}\|f\|^2, \qquad \Lambda > 0,$$

and $f_D = \arg\min_f J_D(f)$ (line L1). $J_D$ is $\Lambda$-strongly convex, so $f_D$ exists and is unique.

**Lemma 1 (sensitivity; Chaudhuri, Monteleoni and Sarwate, Corollary 8).** For replace neighbors $D, D'$, $\|f_D - f_{D'}\| \le 2/(n\Lambda)$.

*Proof.* Say $D'$ replaces example $n$ by $(x', y')$. Write $h(f) = \ell(y' f^{\mathsf T} x') - \ell(y_n f^{\mathsf T} x_n)$, so $J_{D'} = J_D + h/n$. The gradient of $f \mapsto \ell(y f^{\mathsf T} x)$ is $y\,\ell'(y f^{\mathsf T} x)\,x$, of norm at most $\|x\| \le 1$. So $\|\nabla h(f)\| \le 2$ for all $f$.

Let $f_1 = f_D$ and $f_2 = f_{D'}$. Then $\nabla J_D(f_1) = 0$ and $\nabla J_D(f_2) = \nabla J_{D'}(f_2) - \nabla h(f_2)/n = -\nabla h(f_2)/n$. A $\Lambda$-strongly convex differentiable function satisfies $(\nabla J_D(f_2) - \nabla J_D(f_1))^{\mathsf T}(f_2 - f_1) \ge \Lambda\|f_2 - f_1\|^2$. With the Cauchy-Schwarz inequality,

$$\Lambda\|f_2 - f_1\|^2 \le \frac{1}{n}\|\nabla h(f_2)\|\,\|f_2 - f_1\| \le \frac{2}{n}\|f_2 - f_1\|,$$

which gives the claim (it is trivial when $f_1 = f_2$). $\square$

**Lemma 2 (the noise).** Let $\beta > 0$. If $r$ is a sum of $d$ independent $\mathrm{Exp}(\beta)$ variables and $u$ is an independent uniform unit vector in $\mathbb R^d$, then $b = r u$ has the density $\nu(b) = \exp(-\beta\|b\|)/Z$ with $Z = 2\pi^{d/2}\Gamma(d)/(\Gamma(d/2)\beta^d)$. A Gaussian vector divided by its norm is a uniform unit vector.

*Proof.* A sum of $d$ independent $\mathrm{Exp}(\beta)$ variables has the Gamma density $\beta^d r^{d-1} e^{-\beta r}/\Gamma(d)$ on $r > 0$. In polar coordinates, the density $\nu$ is a function of $\|b\|$ only, so its direction is uniform and independent of the norm, and the norm has the density $\propto r^{d-1} e^{-\beta r}$, since the sphere of radius $r$ has area $r^{d-1} \cdot 2\pi^{d/2}/\Gamma(d/2)$. The two laws match. Integrating $e^{-\beta r}$ against this area gives $Z$. The standard Gaussian density on $\mathbb R^d$ depends only on the norm, so the direction of a Gaussian vector is uniform. $\square$

**Theorem 1 (privacy).** With $\beta = n\Lambda\varepsilon/2$ (line L2), the output $f_D + b$ (lines L3 and L4) is $\varepsilon$-DP under replace.

*Proof.* By Lemma 2 the output has the density $\nu(z - f_D)$ on $D$ and $\nu(z - f_{D'})$ on $D'$. For every $z$, by the triangle inequality and Lemma 1,

$$\frac{\nu(z - f_D)}{\nu(z - f_{D'})} = \exp\big(\beta(\|z - f_{D'}\| - \|z - f_D\|)\big) \le \exp(\beta\|f_D - f_{D'}\|) \le \exp\!\left(\frac{n\Lambda\varepsilon}{2}\cdot\frac{2}{n\Lambda}\right) = e^{\varepsilon}.$$

Integrating over an event $S$ gives $\Pr[f_D + b \in S] \le e^{\varepsilon}\Pr[f_{D'} + b \in S]$. $\square$

**Theorem 2 (an approximate minimizer).** Suppose line L1 is a deterministic solver whose output $\hat f_D$ satisfies $\|\hat f_D - f_D\| \le \tau$ for every $D$. Then the mechanism with $\hat f_D$ in place of $f_D$ is $\varepsilon(1 + n\Lambda\tau)$-DP. The gradient descent of the code stops at $\|\nabla J_D(\hat f_D)\| \le t$, which gives $\tau = t/\Lambda$.

*Proof.* The triangle inequality gives $\|\hat f_D - \hat f_{D'}\| \le 2/(n\Lambda) + 2\tau$, and the proof of Theorem 1 then gives $\beta(2/(n\Lambda) + 2\tau) = \varepsilon + n\Lambda\varepsilon\tau$. For the stopping rule, strong convexity gives $\Lambda\|\hat f_D - f_D\|^2 \le (\nabla J_D(\hat f_D) - \nabla J_D(f_D))^{\mathsf T}(\hat f_D - f_D) \le t\|\hat f_D - f_D\|$. $\square$

**Theorem 3 (the size of the noise).** $\mathbb E\|b\| = d/\beta = 2d/(n\Lambda\varepsilon)$.

*Proof.* By Lemma 2, $\|b\|$ is a sum of $d$ variables of mean $1/\beta$. $\square$

Theorem 1 is the privacy claim of the page. Theorem 2 shows that the claim survives an inexact solver only with a larger $\varepsilon$, and Theorem 3 gives the cost in accuracy. The code samples from floats, so it follows the analysis only up to floating-point effects; that is a limit of the code, not of the theorem. $\blacksquare$
