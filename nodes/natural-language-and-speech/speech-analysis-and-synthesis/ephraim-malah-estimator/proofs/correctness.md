---
title: Correctness of the Ephraim-Malah estimator
proves: [correctness]
status: full
---

We prove that the gain gives the posterior mean of the amplitude, that the posterior mean is the estimate of least mean squared error, that the gain tends to the Wiener gain, and that the analysis and synthesis of the code are exact when the gain is 1.

## Setup

In one bin, $Y = X + D$ with $X = A e^{i\alpha}$ and $D$ independent complex Gaussians of mean 0 and variances $\lambda_x$ and $\lambda_d$. Write $R = |Y|$, $\xi = \lambda_x / \lambda_d$, $\gamma = R^2 / \lambda_d$ and $v = \xi\gamma / (1 + \xi)$. The modified Bessel function is $I_\nu(x) = \sum_{k \ge 0} (x/2)^{2k + \nu} / (k!\, (k + \nu)!)$ for $\nu = 0, 1$, and $I_0(x) = \frac{1}{2\pi} \int_0^{2\pi} e^{x \cos t}\, dt$.

## Lemma 1 (the posterior of the amplitude)

The posterior density of $A$ given $Y$ is proportional to $a\, e^{-c a^2} I_0(b a)$ on $a > 0$, with $c = 1/\lambda_x + 1/\lambda_d$ and $b = 2R / \lambda_d$.

*Proof.* A complex Gaussian $X$ of variance $\lambda_x$ has, in polar form, independent $A$ with the Rayleigh density $\frac{2a}{\lambda_x} e^{-a^2/\lambda_x}$ and $\alpha$ uniform on $[0, 2\pi)$. Given $A = a$ and $\alpha$, $Y$ has density $\frac{1}{\pi\lambda_d} e^{-|Y - a e^{i\alpha}|^2 / \lambda_d}$, and $|Y - a e^{i\alpha}|^2 = R^2 + a^2 - 2aR\cos(\alpha - \theta)$ with $\theta = \arg Y$. Integrating over $\alpha$ gives a factor $e^{-(R^2 + a^2)/\lambda_d} I_0(2aR / \lambda_d)$, by the integral form of $I_0$. Multiply by the prior and drop the factors that do not depend on $a$. $\square$

## Lemma 2 (two integrals)

For $c > 0$ and $b \ge 0$, with $z = b^2 / (4c)$,

$$\int_0^\infty a\, e^{-c a^2} I_0(b a)\, da = \frac{e^{z}}{2c}, \qquad \int_0^\infty a^2 e^{-c a^2} I_0(b a)\, da = \frac{\sqrt{\pi}}{4 c^{3/2}}\, {}_1F_1\!\left(\tfrac32; 1; z\right),$$

where ${}_1F_1(p; q; z) = \sum_k \frac{(p)_k}{(q)_k} \frac{z^k}{k!}$ is Kummer's function.

*Proof.* All terms are nonnegative, so the series of $I_0$ may be integrated term by term. With $\int_0^\infty a^{2k+1} e^{-ca^2} da = \frac{k!}{2 c^{k+1}}$, the first integral is $\sum_k \frac{(b/2)^{2k}}{(k!)^2} \frac{k!}{2c^{k+1}} = \frac{1}{2c} \sum_k \frac{z^k}{k!} = \frac{e^z}{2c}$. With $\int_0^\infty a^{2k+2} e^{-ca^2} da = \frac{\Gamma(k + 3/2)}{2 c^{k + 3/2}}$ and $\Gamma(k + 3/2) = \Gamma(3/2) (3/2)_k = \frac{\sqrt\pi}{2} (3/2)_k$, the second is $\frac{\sqrt\pi}{4 c^{3/2}} \sum_k \frac{(3/2)_k}{k!\, k!} z^k$, and $(1)_k = k!$. $\square$

## Theorem 1 (the gain is the posterior mean)

$E[A \mid Y] = G(\xi, \gamma)\, R$, with $G(\xi, \gamma) = \frac{\sqrt\pi}{2} \frac{\sqrt v}{\gamma} e^{-v/2} [(1 + v) I_0(v/2) + v I_1(v/2)]$.

*Proof.* By Lemmas 1 and 2, $E[A \mid Y] = \frac{\sqrt\pi}{2\sqrt c}\, e^{-z}\, {}_1F_1(\tfrac32; 1; z)$. We use two standard identities of Kummer's function: Kummer's transformation ${}_1F_1(p; q; z) = e^z {}_1F_1(q - p; q; -z)$, and ${}_1F_1(-\tfrac12; 1; -z) = e^{-z/2} [(1 + z) I_0(z/2) + z I_1(z/2)]$. Together they give $E[A \mid Y] = \frac{\sqrt\pi}{2\sqrt c} e^{-z/2} [(1 + z) I_0(z/2) + z I_1(z/2)]$. Now

$$z = \frac{b^2}{4c} = \frac{R^2 / \lambda_d^2}{(\lambda_x + \lambda_d) / (\lambda_x \lambda_d)} = \frac{R^2}{\lambda_d} \frac{\lambda_x}{\lambda_x + \lambda_d} = \gamma \frac{\xi}{1 + \xi} = v,$$

and $\frac{1}{\sqrt c} = \sqrt{\frac{\lambda_x \lambda_d}{\lambda_x + \lambda_d}} = \sqrt{\lambda_d \frac{v}{\gamma}}$. Dividing by $R = \sqrt{\gamma \lambda_d}$ gives $\frac{\sqrt\pi}{2} \frac{\sqrt{v}}{\gamma} e^{-v/2}[\dots] = G$. $\square$

The second identity of Kummer's function is the one step not derived here. The tests check the final formula against a direct numerical integration of the posterior of Lemma 1, by Simpson's rule, at six pairs $(\xi, \gamma)$, with agreement to 7 decimal places.

## Theorem 2 (the posterior mean minimizes the mean squared error)

For every measurable function $f$ of $Y$ with $E[f(Y)^2] < \infty$, $E[(A - f(Y))^2] \ge E[(A - E[A \mid Y])^2]$.

*Proof.* Let $m(Y) = E[A \mid Y]$. Then $E[(A - f)^2] = E[(A - m)^2] + 2E[(A - m)(m - f)] + E[(m - f)^2]$. The middle term is 0, because $E[(A - m)(m - f) \mid Y] = (m - f) E[A - m \mid Y] = 0$. The last term is nonnegative. $\square$

So $\hat A = G R$ is the estimate of least mean squared amplitude error for the model, and the code multiplies the complex bin by $G$, which gives this amplitude and keeps the phase of $Y$.

## Theorem 3 (the limit is the Wiener gain)

For fixed $\xi > 0$, $G(\xi, \gamma) = \frac{\xi}{1 + \xi} + \frac{1}{4\gamma} + O(\gamma^{-2})$ as $\gamma \to \infty$.

*Proof.* As $\gamma \to \infty$, $v \to \infty$. The standard asymptotic expansion $e^{-x} I_\nu(x) = \frac{1}{\sqrt{2\pi x}} \left(1 - \frac{4\nu^2 - 1}{8x} + O(x^{-2})\right)$ at $x = v/2$ gives $e^{-v/2} I_0(v/2) = \frac{1}{\sqrt{\pi v}} (1 + \frac{1}{4v} + O(v^{-2}))$ and $e^{-v/2} I_1(v/2) = \frac{1}{\sqrt{\pi v}} (1 - \frac{3}{4v} + O(v^{-2}))$. Then

$$G = \frac{1}{2\gamma} \left[(1 + v)\left(1 + \frac{1}{4v}\right) + v\left(1 - \frac{3}{4v}\right) + O(v^{-1})\right] = \frac{1}{2\gamma}\left[2v + \frac12 + O(v^{-1})\right] = \frac{v}{\gamma} + \frac{1}{4\gamma} + O\!\left(\frac{1}{v\gamma}\right).$$

Since $v / \gamma = \xi / (1 + \xi)$ and $v$ is proportional to $\gamma$, the claim follows. $\square$

## Theorem 4 (identity of the analysis and synthesis)

With the periodic Hann window $w[i] = \frac12 - \frac12 \cos(2\pi i / N)$, the hop $N/2$ and the gain 1 in every bin, the output equals the input at every sample covered by two frames.

*Proof.* For $0 \le i < N/2$, $w[i] + w[i + N/2] = 1 - \frac12(\cos(2\pi i/N) + \cos(2\pi i/N + \pi)) = 1$. With gain 1, the inverse DFT of frame $t$ is $w[i]\, y[tN/2 + i]$, and the overlap-add at a sample covered by frames $t$ and $t + 1$ gives $(w[i + N/2] + w[i])\, y = y$. $\square$

## Remarks

The function bessel_ie of the code returns $e^{-x} I_\nu(x)$ from the power series in log space for $x < 50$, and from five terms of the asymptotic series for $x \ge 50$; the tests compare both against the integral $\frac{1}{\pi}\int_0^\pi e^{x(\cos t - 1)} \cos(\nu t)\, dt$, with relative error below $10^{-9}$. The decision-directed $\xi$ is an estimate that depends on the data, so on real signals the optimality of Theorem 2 holds only for the model with $\xi$ given.
