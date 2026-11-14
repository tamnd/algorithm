---
title: The stopping rule of Monte Carlo power estimation from the normal confidence interval
proves: [correctness]
status: full
---

**Setting.** The samples $E_1, E_2, \ldots$ are independent with the same law, mean $\mu > 0$ and variance $\sigma^2 \in (0, \infty)$. After $N$ samples, $\eta_N$ is the sample mean, $s_N$ the sample standard deviation, $z$ the $1 - \alpha/2$ quantile of the standard normal law and $h_N = z s_N / \sqrt{N}$.

**Lemma 1 (Welford).** After line L5 has run $N$ times, mean $= \eta_N$ and $M2 = \sum_{k=1}^N (E_k - \eta_N)^2$, so line L6 sets $s = s_N$ and $h = h_N$.

*Proof.* By induction on $N$. For $N = 1$, mean $= E_1$ and $M2 = 0$. Suppose the claim holds for $N - 1$. With $\delta = E_N - \eta_{N-1}$, line L5 sets mean $= \eta_{N-1} + \delta / N = \eta_N$. Also $E_N - \eta_N = \delta (N - 1)/N$, and

$$ \sum_{k=1}^{N} (E_k - \eta_N)^2 = \sum_{k=1}^{N-1} (E_k - \eta_{N-1})^2 + (N - 1)(\eta_{N-1} - \eta_N)^2 + (E_N - \eta_N)^2, $$

since the cross term $\sum_{k < N} (E_k - \eta_{N-1})$ is 0. With $\eta_{N-1} - \eta_N = -\delta / N$ the last two terms are $\delta^2 (N - 1)/N^2 + \delta^2 (N-1)^2/N^2 = \delta^2 (N - 1)/N = \delta (E_N - \eta_N)$, which is the increment of line L5. $\square$

**Theorem 1 (relative error on the covering event).** Let $\varepsilon \in (0, 1)$. If the run stops by the rule $h_N < \varepsilon \eta_N$ and $|\eta_N - \mu| \le h_N$, then

$$ |\eta_N - \mu| < \varepsilon\, \eta_N \qquad\text{and}\qquad \frac{|\eta_N - \mu|}{\mu} < \frac{\varepsilon}{1 - \varepsilon}. $$

*Proof.* The first inequality is $|\eta_N - \mu| \le h_N < \varepsilon \eta_N$. It gives $\eta_N - \mu < \varepsilon \eta_N$, so $\eta_N (1 - \varepsilon) < \mu$ and $\eta_N < \mu / (1 - \varepsilon)$. Then $|\eta_N - \mu| < \varepsilon \eta_N < \varepsilon \mu / (1 - \varepsilon)$. $\square$

So the probability that the returned estimate has relative error below $\varepsilon / (1 - \varepsilon)$ is at least the probability that the interval $[\eta_N - h_N, \eta_N + h_N]$ at the stopping time contains $\mu$. The rest of the argument is about that probability.

**Theorem 2 (fixed $N$).** Let $N \ge 2$ be fixed.

1. If the $E_k$ are normal, then $P(|\eta_N - \mu| \le t\, s_N / \sqrt{N}) = 1 - \alpha$ for the $1 - \alpha/2$ quantile $t$ of the Student law with $N - 1$ degrees of freedom.
2. For any law with finite variance, $P(|\eta_N - \mu| \le h_N) \to 1 - \alpha$ as $N \to \infty$.

*Proof.* (1) For normal samples, $\eta_N$ and $s_N^2$ are independent, $\sqrt{N}(\eta_N - \mu)/\sigma$ is standard normal and $(N - 1) s_N^2 / \sigma^2$ is chi-square with $N - 1$ degrees of freedom, so $\sqrt{N} (\eta_N - \mu) / s_N$ has the Student law with $N - 1$ degrees of freedom. (2) By the central limit theorem $\sqrt{N}(\eta_N - \mu)/\sigma$ tends in law to the standard normal law, and $s_N \to \sigma$ almost surely by the law of large numbers, so by Slutsky's lemma $\sqrt{N} (\eta_N - \mu) / s_N$ tends in law to the standard normal law, whose probability of $[-z, z]$ is $1 - \alpha$. $\square$

**The stopping time.** At line L7 the number of samples is a random time $\tau$ that depends on $s_N$ and $\eta_N$, so Theorem 2 does not apply directly at $N = \tau$. As $\varepsilon \to 0$, $\tau \to \infty$ and $\tau\, \varepsilon^2 \mu^2 / (z^2 \sigma^2) \to 1$ almost surely, because $s_N / \eta_N \to \sigma / \mu$ almost surely. Chow and Robbins (1965) proved, for the fixed-width rule that stops when $h_N$ is below a given width $d$, that the coverage at the stopping time tends to $1 - \alpha$ as $d \to 0$; the proof uses Anscombe's theorem, which keeps the central limit theorem valid at a random index $\tau$ with $\tau / n_\varepsilon \to 1$ in probability for constants $n_\varepsilon \to \infty$. The same argument applies to the relative rule with $n_\varepsilon = z^2 \sigma^2 / (\varepsilon^2 \mu^2)$. This step is cited, not proved here. For fixed $\varepsilon$ the coverage is not exactly $1 - \alpha$, and the example of the page measures it.

**What is proved and what is measured.** Proved: lines L5 and L6 compute the sample mean and the half width exactly (Lemma 1); on the event that the interval covers $\mu$, the relative error is below $\varepsilon / (1 - \varepsilon)$ (Theorem 1); for fixed $N$ the coverage is exact with the $t$ quantile and normal samples, and asymptotic otherwise (Theorem 2). Cited: the asymptotic coverage under the stopping rule. Measured: the coverage of the rule for a given circuit, input model and $\varepsilon$.
