---
title: The PPM update keeps the density, the estimate is a mean of per-pass estimates, the radius goes to 0, and the error goes to 0
proves: [correctness]
status: full
---

Fix one hit point at $x$ on a flat surface, with the outgoing direction $\omega_o$. For a point $x'$ near $x$ let

$$e(x') = \int_{H^2} f_r(x, \omega, \omega_o)\, L_i(x', \omega) \cos\theta\, d\omega,$$

the reflected radiance at $x'$ with the BRDF of $x$. The target is $e(x)$. For $r > 0$ let $D_r$ be the disc of radius $r$ about $x$ and $\bar e(r) = \frac{1}{\pi r^2}\int_{D_r} e\, dA$, the mean over the disc.

A pass emits $M$ photons. We give each photon of a pass the power $\Phi/M$, so that the photons of one pass alone are an unbiased photon tracing with $M$ paths. Then line L11 is $\hat L_i = \tau_i / (\pi R_i^2\, i)$. In pass $j$ let $m_j$ be the number of photon hits in $D_{R_{j-1}}$ and $\Phi_j$ the sum of their BRDF-weighted powers. Let $N_0 = 0$, $\tau_0 = 0$, and let lines L8 to L10 give $N_j$, $R_j$ and $\tau_j$ from $N_{j-1}$, $R_{j-1}$, $\tau_{j-1}$, $m_j$ and $\Phi_j$. If $m_j = 0$ nothing changes, as in the code.

**Lemma 1 (the density is kept).** If $m_j > 0$, then $N_j / R_j^2 = (N_{j-1} + m_j)/R_{j-1}^2$. In all cases $N_j/R_j^2 = \sum_{k \le j} m_k / R_{k-1}^2$.

*Proof.* Line L9 gives $R_j^2 = R_{j-1}^2 (N_{j-1} + \alpha m_j)/(N_{j-1} + m_j)$ and line L8 gives $N_j = N_{j-1} + \alpha m_j$, so $N_j / R_j^2 = (N_{j-1} + m_j)/R_{j-1}^2$. If $m_j = 0$ the same equality holds because nothing changes. Sum over $j$ with $N_0 = 0$. $\square$

The test checks the first equality exactly with fractions.

**Lemma 2 (a mean of per-pass estimates).** For each $i \ge 1$,

$$\hat L_i = \frac{1}{i}\sum_{j=1}^{i} Y_j, \qquad Y_j = \frac{\Phi_j}{\pi R_{j-1}^2}.$$

*Proof.* Line L10 gives $\tau_j / R_j^2 = (\tau_{j-1} + \Phi_j)/R_{j-1}^2$, also when $m_j = 0$, since then $\Phi_j = 0$ and nothing changes. So $\tau_j/R_j^2 = \tau_{j-1}/R_{j-1}^2 + \Phi_j/R_{j-1}^2$, and with $\tau_0 = 0$ we get $\tau_i / R_i^2 = \sum_{j \le i} \Phi_j / R_{j-1}^2$. Divide by $\pi i$. $\square$

Each $Y_j$ is the fixed-radius photon mapping estimate of [photon mapping](/photon-mapping/) with the radius $R_{j-1}$ and the photons of pass $j$ only.

**Lemma 3 (conditional mean).** Let $\mathcal F_{j-1}$ hold the photons of passes 1 to $j - 1$. Then $E[Y_j \mid \mathcal F_{j-1}] = \bar e(R_{j-1})$.

*Proof.* $R_{j-1}$ is a function of the first $j - 1$ passes, and the photons of pass $j$ are independent of them. Given $\mathcal F_{j-1}$, apply the flux theorem of photon mapping (photon tracing is unbiased for flux) to the $M$ paths of pass $j$, with the weight $g(x', \omega) = f_r(x, \omega, \omega_o)$ on $D_{R_{j-1}}$ and $g = 0$ elsewhere. The expected value of $\Phi_j$ is $\int_{D_{R_{j-1}}} e\, dA = \pi R_{j-1}^2\, \bar e(R_{j-1})$. $\square$

So $E[\hat L_i] = \frac{1}{i}\sum_{j \le i} E[\bar e(R_{j-1})]$. Each term differs from $e(x)$ unless $e$ is constant on the disc, so the estimate is biased at each finite $i$.

**Lemma 4 (the radius goes to 0).** Suppose each photon path has at most one hit near $x$, and that a photon lands in $D_r$ with the probability $p(r)$, where $p(r) > 0$ for each $r > 0$. Then $R_i \to 0$ with probability 1.

*Proof.* The factor $(N + \alpha m)/(N + m)$ is at most 1, so $R_i$ does not increase and has a limit $R_\infty \ge 0$. Fix a rational $\rho > 0$ and let $A_\rho$ be the event $R_\infty \ge \rho$. Let $K_j$ be the number of photons of pass $j$ in $D_\rho$. The $K_j$ are independent with the binomial distribution of $M$ and $p(\rho)$, because they do not depend on the radii. On $A_\rho$ each $R_{j-1} \ge \rho$, so $m_j \ge K_j$.

Since $\log(1 - u) \le -u$ for $u \in [0, 1)$,

$$\log R_i^2 - \log R_0^2 = \sum_{j \le i} \log\left(1 - \frac{(1 - \alpha)\, m_j}{N_{j-1} + m_j}\right) \le -(1 - \alpha) \sum_{j \le i} \frac{m_j}{N_{j-1} + m_j},$$

where a term with $m_j = 0$ is 0. Also $N_{j-1} + m_j \le m_1 + \dots + m_j \le jM$, so on $A_\rho$ each term is at least $K_j/(jM)$. Let $S_n = K_1 + \dots + K_n$. By the strong law of large numbers $S_n / n \to M p(\rho) > 0$ with probability 1. Summation by parts gives $\sum_{j \le n} K_j / j = S_n/n + \sum_{j < n} S_j/(j(j+1))$, and $S_j/(j(j+1)) \ge Mp(\rho)/(2(j+1))$ for all large $j$. So $\sum_j K_j/j = \infty$ with probability 1. On $A_\rho$ this gives $\log R_i^2 \to -\infty$, which contradicts $R_\infty \ge \rho$. So $P(A_\rho) = 0$. The union over the rational $\rho$ has probability 0, so $R_\infty = 0$ with probability 1. $\square$

**Theorem 1 (asymptotically unbiased).** Under the conditions of Lemma 4, if $e$ is bounded near $x$ and continuous at $x$, then $E[\hat L_i] \to e(x)$.

*Proof.* $\bar e(r) \to e(x)$ as $r \to 0$, by continuity. By Lemma 4, $\bar e(R_{j}) \to e(x)$ with probability 1, and the values are bounded, so $E[\bar e(R_j)] \to e(x)$ by bounded convergence. A Cesàro mean of a convergent sequence converges to the same limit, so by Lemma 3 $E[\hat L_i] = \frac{1}{i}\sum_{j \le i} E[\bar e(R_{j-1})] \to e(x)$. $\square$

**Lemma 5 (the mean-field radius).** Suppose the photon density is a constant $c > 0$ near $x$, and replace each count $m_j$ by its expected value $c M R_{j-1}^2$. Then $R_j^2 = R_{j-1}^2 (j - 1 + \alpha)/j$ for each $j \ge 1$, so

$$R_j^2 = R_0^2 \prod_{k=0}^{j-1} \frac{k + \alpha}{k + 1} = R_0^2\, \frac{\Gamma(j + \alpha)}{\Gamma(\alpha)\,\Gamma(j + 1)} \sim R_0^2\, \frac{j^{\alpha - 1}}{\Gamma(\alpha)}.$$

*Proof.* By Lemma 1, $N_j / R_j^2 = \sum_{k \le j} cM = jcM$, so $N_{j-1} = (j - 1)\, cM R_{j-1}^2$. Then

$$\frac{R_j^2}{R_{j-1}^2} = \frac{N_{j-1} + \alpha m_j}{N_{j-1} + m_j} = \frac{(j - 1) + \alpha}{(j - 1) + 1}.$$

The product is a ratio of Gamma functions because $\Gamma(z + 1) = z\Gamma(z)$, and $\Gamma(j + \alpha)/\Gamma(j + 1) \sim j^{\alpha - 1}$. $\square$

This is the recursion $r_{i+1}^2 = r_i^2 (i + \alpha)/(i + 1)$ of Knaus and Zwicker, started at $i = 0$ instead of $i = 1$. Their form gives $r_i^2 = r_1^2\, \Gamma(i + \alpha)/(\Gamma(1 + \alpha)\Gamma(i + 1)) \sim r_1^2\, i^{\alpha - 1}/\Gamma(1 + \alpha)$, and the test checks both the Gamma form and the limit.

**Theorem 2 (consistency with the deterministic radius sequence).** Let $r_j^2 = r_0^2\, \Gamma(j + \alpha)/(\Gamma(\alpha)\Gamma(j + 1))$ with $0 < \alpha < 1$, and let $\hat L_i = \frac1i \sum_{j \le i} Y_j$ where the $Y_j$ are independent fixed-radius estimates with the radii $r_{j-1}$. Assume:

- $e$ is twice differentiable on $D_{r_0}$, and the norm of its Hessian is at most $K$;
- in one pass, each photon adds to $\Phi_j$ an independent term whose second moment is at most $C \pi r^2 / M^2$ for the disc of radius $r$. This holds when the weights are bounded by a multiple of $1/M$ and the photon density is bounded.

Then $|E[\hat L_i] - e(x)| = O(i^{\alpha - 1})$ and $\operatorname{Var}(\hat L_i) = O(i^{-\alpha}/M)$. So the mean squared error goes to 0, and $\hat L_i \to e(x)$ in probability.

*Proof.* Bias. By Taylor's theorem $e(x') = e(x) + \nabla e(x) \cdot (x' - x) + \rho(x')$ with $|\rho(x')| \le \frac{K}{2}|x' - x|^2$. The linear term has mean 0 over the disc, and the mean of $|x' - x|^2$ over $D_r$ is $r^2/2$. So $|\bar e(r) - e(x)| \le K r^2/4$. With $E[Y_j] = \bar e(r_{j-1})$,

$$|E[\hat L_i] - e(x)| \le \frac{K}{4i}\sum_{j=0}^{i-1} r_j^2.$$

From the Gamma form there is a constant $a$ with $r_j^2 \le a\, r_0^2\, j^{\alpha - 1}$ for $j \ge 1$. Then $\sum_{j=1}^{i-1} j^{\alpha - 1} \le 1 + \int_1^{i} t^{\alpha - 1} dt \le i^\alpha / \alpha + 1$, so the bias is $O(i^{\alpha - 1})$.

Variance. $\Phi_j$ is a sum of $M$ independent terms, so $\operatorname{Var}(\Phi_j) \le M \cdot C\pi r_{j-1}^2/M^2 = C\pi r_{j-1}^2/M$ and $\operatorname{Var}(Y_j) \le C/(\pi M r_{j-1}^2)$. The $Y_j$ are independent, so

$$\operatorname{Var}(\hat L_i) = \frac{1}{i^2}\sum_{j=0}^{i-1}\operatorname{Var}(Y_{j+1}) \le \frac{C}{\pi M i^2}\sum_{j=0}^{i-1}\frac{1}{r_j^2}.$$

There is a constant $b$ with $1/r_j^2 \le b\, j^{1 - \alpha}/r_0^2$ for $j \ge 1$, and $\sum_{j < i} j^{1-\alpha} \le i^{2 - \alpha}$. So the variance is $O(i^{-\alpha}/M)$.

The mean squared error is the squared bias plus the variance, $O(i^{2\alpha - 2}) + O(i^{-\alpha})$, which goes to 0. Chebyshev's inequality gives convergence in probability. $\square$

**Corollary (the best $\alpha$).** The exponent of the mean squared error is $\max(2\alpha - 2, -\alpha)$. It is smallest when $2\alpha - 2 = -\alpha$, that is $\alpha = 2/3$, with the rate $O(i^{-2/3})$.

**Remark.** Theorem 1 holds for the random radii of PPM itself. Theorem 2 is proved here for the deterministic sequence, which Lemma 5 shows to be the mean-field form of the PPM radius. For the random radii, Lemma 2 still makes $\hat L_i - \frac1i \sum_j \bar e(R_{j-1})$ a mean of martingale differences, and Knaus and Zwicker argue that the same rates hold. The test checks this case by simulation: at the foot of a point light, the error after 64 passes is about a third of the fixed-radius bias, and it agrees with the mean-field model.
