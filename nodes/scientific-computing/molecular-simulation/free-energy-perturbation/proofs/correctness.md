---
title: The Zwanzig identity, and the bias, consistency and error of the exponential average
proves: [correctness]
status: full
---

Let $\rho_0(x) = e^{-\beta U_0(x)} / Z_0$ be the canonical density of state 0, with $Z_j = \int e^{-\beta U_j(x)}\,dx$ finite and positive for $j = 0, 1$. Write $\Delta U = U_1 - U_0$, $w(x) = e^{-\beta \Delta U(x)}$ and $\Delta A = -\beta^{-1} \ln(Z_1 / Z_0)$.

**Claim 1 (Zwanzig identity).** If $e^{-\beta U_1(x)} > 0$ implies $e^{-\beta U_0(x)} > 0$, then $E_0[w] = Z_1 / Z_0$, so $\Delta A = -\beta^{-1} \ln E_0[w]$.

*Proof.* On the set where $e^{-\beta U_0} > 0$,
$$E_0[w] = \int \frac{e^{-\beta U_0(x)}}{Z_0} e^{-\beta (U_1(x) - U_0(x))}\,dx = \frac{1}{Z_0} \int e^{-\beta U_1(x)}\,dx = \frac{Z_1}{Z_0}.$$
The integral over the set where $e^{-\beta U_0} = 0$ is missing on the left, and by the hypothesis $e^{-\beta U_1}$ is 0 there too, so nothing is lost on the right. $\square$

If the hypothesis fails, the same computation gives $E_0[w] = Z_1' / Z_0$ with $Z_1'$ the integral over the support of state 0 only, which is smaller than $Z_1$. This is the support condition of importance sampling.

**Claim 2 (the shift).** For any real numbers $d_1, \dots, d_N$ and $m = \min_i d_i$,
$$m - \frac{1}{\beta} \ln \Bigl( \frac{1}{N} \sum_i e^{-\beta (d_i - m)} \Bigr) = -\frac{1}{\beta} \ln \Bigl( \frac{1}{N} \sum_i e^{-\beta d_i} \Bigr),$$
and every term $e^{-\beta (d_i - m)}$ lies in $(0, 1]$, with at least one equal to 1.

*Proof.* $\sum_i e^{-\beta d_i} = e^{-\beta m} \sum_i e^{-\beta (d_i - m)}$; take $-\beta^{-1} \ln$ of both sides divided by $N$. Since $d_i - m \ge 0$, each term is at most 1, and the index of the minimum gives 1. $\square$

So lines L2 to L4 compute the estimator $\widehat{\Delta A} = -\beta^{-1} \ln \overline{w}$ with $\overline{w} = N^{-1} \sum_i w(x_i)$, and the sum $s$ lies in $[1, N]$, so neither overflow nor a logarithm of 0 occurs.

**Claim 3 (consistency).** If $x_1, x_2, \dots$ are independent draws from $\rho_0$, or a chain that is ergodic for $\rho_0$, then $\widehat{\Delta A} \to \Delta A$ with probability 1 as $N \to \infty$.

*Proof.* $w \ge 0$ and $E_0[w] = Z_1/Z_0 < \infty$ by Claim 1. The strong law of large numbers (or the ergodic theorem for the chain) gives $\overline{w} \to Z_1 / Z_0 > 0$ almost surely, and $-\beta^{-1} \ln$ is continuous on $(0, \infty)$. $\square$

**Claim 4 (bounds and bias).** For every sample, $\min_i \Delta U(x_i) \le \widehat{\Delta A} \le N^{-1} \sum_i \Delta U(x_i)$. For independent draws and every $N$, $E[\widehat{\Delta A}] \ge \Delta A$.

*Proof.* The lower bound follows from Claim 2: $s \le N$, so $-\beta^{-1} \ln(s/N) \ge 0$. For the upper bound, the exponential is convex, so by Jensen's inequality for the uniform average over the sample, $\overline{w} = N^{-1} \sum_i e^{-\beta d_i} \ge e^{-\beta \bar d}$ with $\bar d$ the mean of the $d_i$; take $-\beta^{-1} \ln$, which reverses the order. For the bias, $\ln$ is concave, so Jensen's inequality for the expectation over samples gives $E[\ln \overline{w}] \le \ln E[\overline{w}] = \ln(Z_1/Z_0)$, and multiplying by $-\beta^{-1} < 0$ gives $E[\widehat{\Delta A}] \ge \Delta A$. $\square$

**Claim 5 (error and first-order bias).** Let the draws be independent with $\mu = E_0[w]$ and $\sigma^2 = \mathrm{var}_0(w) < \infty$. Then
$$\sqrt{N}\,(\widehat{\Delta A} - \Delta A) \to N\Bigl(0, \frac{\sigma^2}{\beta^2 \mu^2}\Bigr)$$
in distribution. If moreover $w$ takes its values in an interval $[c, C]$ with $c > 0$, the bias is $E[\widehat{\Delta A}] - \Delta A = \sigma^2 / (2 N \beta \mu^2) + O(N^{-3/2})$.

*Proof.* The central limit theorem gives $\sqrt{N}(\overline{w} - \mu) \to N(0, \sigma^2)$. The map $g(t) = -\beta^{-1} \ln t$ has $g'(\mu) = -1/(\beta \mu)$, and the delta method gives the first statement. For the bias, Taylor's theorem gives $g(\overline{w}) = g(\mu) + g'(\mu)(\overline{w} - \mu) + \frac12 g''(\mu)(\overline{w} - \mu)^2 + \frac16 g'''(\xi)(\overline{w} - \mu)^3$ with $\xi$ between $\mu$ and $\overline{w}$, so $\xi \in [c, C]$. Here $g''(\mu) = 1/(\beta \mu^2)$ and $|g'''(\xi)| = 2/(\beta \xi^3) \le 2/(\beta c^3)$. The linear term has mean 0, the quadratic term has mean $\sigma^2 / (2 N \beta \mu^2)$, and $E|\overline{w} - \mu|^3 \le (E(\overline{w} - \mu)^4)^{3/4} = O(N^{-3/2})$ for bounded $w$. $\square$

When $w$ is not bounded away from 0, as in the harmonic example, the same first-order term is the usual approximation; the page compares it with a measured bias.

The error bar of the code replaces $\sigma$ and $\mu$ by their sample values. It is valid only when $\sigma < \infty$ and $N$ is large enough that the rare large values of $w$ have been seen.

**Claim 6 (staging).** For $0 = \lambda_0 < \dots < \lambda_K = 1$ with finite $Z_{\lambda_k}$ and the support condition in each window,
$$\Delta A = \sum_{k=0}^{K-1} -\frac{1}{\beta} \ln \bigl\langle e^{-\beta (U_{\lambda_{k+1}} - U_{\lambda_k})} \bigr\rangle_{\lambda_k}.$$

*Proof.* By Claim 1 the $k$-th term is $-\beta^{-1} \ln(Z_{\lambda_{k+1}} / Z_{\lambda_k})$. The sum telescopes to $-\beta^{-1} \ln(Z_1 / Z_0)$. $\square$

With independent windows the estimate of the sum has the sum of the variances of the windows, which gives the error bar of STAGED-FEP. Claims 3 to 5 apply to each term, so the staged estimate is consistent and biased upward.

**Claim 7 (the examples).**

(a) For $U_0 = x^2/2$, $U_1 = x^2$ and $\beta = 1$: in the forward direction $E[w] = 1/\sqrt2$ and $E[w^2] = 1/\sqrt3$. In the reverse direction, with samples of state 1 and weight $e^{+\Delta U}$, the second moment is infinite.

(b) For $U_\lambda = (x - a\lambda)^2 / 2$ and $\beta = 1$, one window from $\lambda$ to $\lambda + \delta$ has $\mathrm{var}(w)/E[w]^2 = e^{a^2 \delta^2} - 1$. So $K$ equal windows with $N/K$ samples each give the large-$N$ variance $K^2 (e^{a^2/K^2} - 1) / N$.

*Proof.* (a) $w = e^{-x^2/2}$ and $x \sim N(0, 1)$, so $E[w] = (2\pi)^{-1/2} \int e^{-x^2}\,dx = 1/\sqrt2$ and $E[w^2] = (2\pi)^{-1/2} \int e^{-3x^2/2}\,dx = 1/\sqrt3$. In reverse, $x \sim N(0, 1/2)$ has density $\pi^{-1/2} e^{-x^2}$ and the weight is $e^{x^2/2}$, so $E[w^2] = \pi^{-1/2} \int e^{x^2} e^{-x^2}\,dx = \infty$.

(b) Shift $x$ so that the window starts at 0: $\Delta U = (x - b)^2/2 - x^2/2 = -bx + b^2/2$ with $b = a\delta$, and $x \sim N(0, 1)$. Then $w = e^{bx - b^2/2}$, $E[w] = 1$ and $E[w^2] = e^{-b^2} E[e^{2bx}] = e^{b^2}$. By Claim 5 one window has variance $(e^{b^2} - 1) / n$ with $n$ samples; with $\delta = 1/K$, $n = N/K$ and $K$ independent windows the total is $K \cdot K (e^{a^2/K^2} - 1) / N$. $\square$

For $a = 3$ and $N = 1200$ this is $(e^9 - 1)/1200 = 6.75$ for one window, a standard deviation of 2.60, and 0.0085 for six windows, a standard deviation of 0.092.
