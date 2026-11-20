---
title: Correctness of the energy detector
proves: [correctness]
status: full
---

We prove that the threshold of line L1 gives the false alarm rate exactly, derive the detection probability for a Gaussian signal and for a fixed signal, show that the energy detector is the most powerful test for a white Gaussian signal, and derive the normal-approximation sample count and the SNR wall.

**Setting.** The receiver has $y[0], \ldots, y[N-1]$. Under $H_0$, $y[n] = w[n]$ with the $w[n]$ independent and $\mathcal{CN}(0, \sigma^2)$. The statistic is $T = \sum_n |y[n]|^2 / \sigma^2$, and the detector declares a signal when $T > \lambda$. Write $G_N(x) = e^{-x} \sum_{k=0}^{N-1} x^k / k!$ for $x \ge 0$.

## Lemma 1 (one sample)

If $w \sim \mathcal{CN}(0, \sigma^2)$, then $|w|^2 / \sigma^2$ has the unit exponential law.

*Proof.* Write $w = \sigma(a + jb)/\sqrt 2$ with $a$ and $b$ independent standard normal. Then $|w|^2/\sigma^2 = (a^2 + b^2)/2$. The pair $(a, b)$ has density $\frac{1}{2\pi} e^{-r^2/2}$ in polar coordinates $(r, \theta)$, so $\Pr[a^2 + b^2 > s] = \int_{\sqrt s}^\infty r e^{-r^2/2}\,dr = e^{-s/2}$. Hence $\Pr[(a^2 + b^2)/2 > x] = e^{-x}$ for $x \ge 0$. $\square$

## Lemma 2 (the sum)

If $E_1, \ldots, E_N$ are independent unit exponentials, then $\Pr[E_1 + \cdots + E_N > x] = G_N(x)$ for all $x \ge 0$.

*Proof.* By induction on $N$. For $N = 1$, $G_1(x) = e^{-x}$. Suppose it holds for $N$, and let $S = E_1 + \cdots + E_N$, with density $f_N(s) = -G_N'(s)$. Differentiating, $G_N'(s) = -e^{-s} s^{N-1}/(N-1)!$, since the sum telescopes, so $f_N(s) = e^{-s} s^{N-1}/(N-1)!$. Then
$$\Pr[S + E_{N+1} > x] = \Pr[S > x] + \int_0^x f_N(s) e^{-(x - s)}\,ds = G_N(x) + e^{-x} \frac{x^N}{N!} = G_{N+1}(x). \qquad \square$$

## Theorem 1 (exact false alarm rate)

Under $H_0$, $\Pr[T > \lambda] = G_N(\lambda)$. The function $G_N$ is continuous and strictly decreasing on $[0, \infty)$, from $1$ to $0$, so for each $P_{fa} \in (0, 1)$ line L1 has exactly one root, and the detector has false alarm rate exactly $P_{fa}$.

*Proof.* The terms $|w[n]|^2/\sigma^2$ are independent unit exponentials by Lemma 1, so the first claim is Lemma 2. $G_N(0) = 1$, $G_N(x) \to 0$ as $x \to \infty$ because each term $e^{-x} x^k$ does, and $G_N'(x) = -e^{-x} x^{N-1}/(N-1)! < 0$ for $x > 0$. By the intermediate value theorem, $G_N(\lambda) = P_{fa}$ has exactly one root. $\square$

The bisection of the code keeps the invariant $G_N(\mathrm{lo}) > P_{fa} \ge G_N(\mathrm{hi})$, which holds at the start since $G_N(0) = 1$ and $\mathrm{hi} = N + 40\sqrt N + 100$ is far in the tail, so the root stays in $[\mathrm{lo}, \mathrm{hi}]$ as the interval halves.

## Theorem 2 (Gaussian signal)

Let $y[n] = s[n] + w[n]$ with $s[n]$ independent $\mathcal{CN}(0, \gamma\sigma^2)$, independent of the noise. Then $P_d = G_N(\lambda / (1 + \gamma))$.

*Proof.* A sum of independent circular complex Gaussian variables is circular complex Gaussian with the sum of the variances, so $y[n] \sim \mathcal{CN}(0, (1 + \gamma)\sigma^2)$, independent over $n$. By Lemmas 1 and 2 applied with $(1+\gamma)\sigma^2$, $T/(1 + \gamma)$ has tail $G_N$, and $\Pr[T > \lambda] = G_N(\lambda/(1 + \gamma))$. $\square$

Since $G_N$ decreases, $P_d$ increases in $\gamma$ and is above $P_{fa}$ for every $\gamma > 0$.

## Theorem 3 (fixed signal)

Let $y[n] = s[n] + w[n]$ with $s$ fixed and $\mu = \sum_n |s[n]|^2 / \sigma^2$. Then
$$P_d = \sum_{j \ge 0} e^{-\mu} \frac{\mu^j}{j!} G_{N+j}(\lambda).$$

*Proof.* Rotate the coordinates. Let $U$ be a unitary matrix whose first row is $s^H/\|s\|$ (if $\mu = 0$ the claim is Theorem 1). The noise is circular white, so $Uw$ has the same law as $w$, and $T = \|Uy\|^2/\sigma^2$ with $Uy = (\|s\|, 0, \ldots, 0) + Uw$. So $T = |\sqrt\mu + z_1|^2 + \sum_{n \ge 2} |z_n|^2$ with $z_n$ independent $\mathcal{CN}(0, 1)$, and the law of $T$ depends on $s$ only through $\mu$.

For the first term, write $z_1 = (a + jb)/\sqrt 2$. The density of $u = |\sqrt\mu + z_1|^2$ at $u > 0$ is, by integrating the Gaussian density over the circle of radius $\sqrt u$,
$$h(u) = e^{-u - \mu} I_0(2\sqrt{\mu u}) = \sum_{j \ge 0} e^{-\mu}\frac{\mu^j}{j!} \cdot e^{-u}\frac{u^j}{j!},$$
using $\frac{1}{2\pi}\int_0^{2\pi} e^{2\sqrt{\mu u}\cos\theta}\,d\theta = I_0(2\sqrt{\mu u}) = \sum_j (\mu u)^j/(j!)^2$. So $u$ is a Poisson mixture: given $J = j$ with $J \sim \mathrm{Poisson}(\mu)$, $u$ is $\mathrm{Gamma}(j + 1, 1)$. Adding the other $N - 1$ unit exponentials, independent of $u$, gives $T \mid J = j \sim \mathrm{Gamma}(N + j, 1)$ by Lemma 2, and the formula follows by total probability. $\square$

The code sums $j$ up to $\mu + 12\sqrt\mu + 40$; the Poisson weights beyond this are below $10^{-20}$, and each $G_{N+j} \le 1$. It updates $G_{N+j+1}(\lambda) = G_{N+j}(\lambda) + e^{-\lambda}\lambda^{N+j}/(N+j)!$, which is the definition of $G$.

## Theorem 4 (optimality for a Gaussian signal)

For a known $\gamma > 0$, the most powerful test of $H_0$ against the Gaussian signal of Theorem 2 at false alarm rate $P_{fa}$ is $T > \lambda$. Since this test does not depend on $\gamma$, it is uniformly most powerful over $\gamma > 0$.

*Proof.* The densities are $p_i(y) = \prod_n \frac{1}{\pi v_i} e^{-|y[n]|^2/v_i}$ with $v_0 = \sigma^2$ and $v_1 = (1 + \gamma)\sigma^2$. The log-likelihood ratio is
$$\ln\frac{p_1(y)}{p_0(y)} = -N\ln(1 + \gamma) + \frac{\gamma}{1 + \gamma} T,$$
a strictly increasing function of $T$. By the Neyman-Pearson lemma, the most powerful test at level $P_{fa}$ rejects $H_0$ when this ratio exceeds a constant, that is, when $T > \lambda'$, and the level fixes $\lambda' = \lambda$ by Theorem 1. Since $T$ has a continuous law, no randomization is needed. $\square$

## Proposition 5 (sample count by the normal approximation)

Under $H_0$, $T$ has mean $N$ and variance $N$; under the Gaussian signal of Theorem 2, mean $N(1 + \gamma)$ and variance $N(1 + \gamma)^2$. Approximating both laws by normal laws, the smallest $N$ that reaches $P_{fa}$ and $P_d$ is
$$N = \left(\frac{Q^{-1}(P_{fa}) - (1 + \gamma) Q^{-1}(P_d)}{\gamma}\right)^2.$$

*Proof.* A unit exponential has mean $1$ and variance $1$, so the moments follow from Theorem 2. With normal laws, the threshold for $P_{fa}$ is $\lambda = N + \sqrt N Q^{-1}(P_{fa})$, and $P_d = Q\big((\lambda - N(1+\gamma))/(\sqrt N(1 + \gamma))\big)$. Setting this to $P_d$ gives $N + \sqrt N Q^{-1}(P_{fa}) = N(1 + \gamma) + \sqrt N (1 + \gamma) Q^{-1}(P_d)$, and dividing by $\sqrt N$ gives $\sqrt N \gamma = Q^{-1}(P_{fa}) - (1 + \gamma)Q^{-1}(P_d)$. $\square$

For small $\gamma$, $N \approx (Q^{-1}(P_{fa}) - Q^{-1}(P_d))^2/\gamma^2$, which is the $1/\mathrm{SNR}^2$ law. This is an approximation; the test file checks that with the exact threshold these sample counts give $P_d$ within $0.005$ of the target at the four SNRs of the page.

## Proposition 6 (SNR wall)

Suppose the true noise power is only known to lie in $[\sigma^2/\rho, \rho\sigma^2]$ for some $\rho > 1$, and the threshold must keep the false alarm rate at most $P_{fa}$ for every noise power in that interval. Let the signal be Gaussian with power $P$. If $P < (\rho - 1/\rho)\sigma^2$, then $P_d \to 0$ as $N \to \infty$ when the true noise is $\sigma^2/\rho$; if $P > (\rho - 1/\rho)\sigma^2$, then $P_d \to 1$ for every noise power in the interval.

*Proof.* With the statistic normalized by the nominal $\sigma^2$, under $H_0$ with true noise $\eta\sigma^2$, $T/\eta \sim \mathrm{Gamma}(N, 1)$, and $\Pr[T > \lambda]$ is largest for $\eta = \rho$. So the threshold must be $\lambda = \rho\lambda_N$, where $\lambda_N$ is the root of Theorem 1, and $\lambda_N/N \to 1$ by the law of large numbers. With the signal and true noise $\eta\sigma^2$, $T/N \to \eta + P/\sigma^2$ almost surely, by the law of large numbers, while $\lambda/N \to \rho$. If $\eta + P/\sigma^2 < \rho$, then $P_d \to 0$; if it is $> \rho$, then $P_d \to 1$. The left side is smallest at $\eta = 1/\rho$, which gives the wall $P/\sigma^2 = \rho - 1/\rho$. $\square$

For $\rho = 10^{0.1}$ (1 dB), the wall is $0.4646$, or $-3.33$ dB. The test file checks the finite case $N = 10^5$, $P_{fa} = 0.1$: at $-4$ dB, below the wall, $P_d < 10^{-6}$ in the smallest noise, and at $-2.5$ dB, above it, $P_d > 0.999999$.

## The tail computation

The code computes $G_N(x) = \sum_{k < N} t_k$ with $t_k = e^{-x} x^k/k!$. The ratio $t_{k+1}/t_k = x/(k+1)$ is above $1$ for $k + 1 < x$ and below $1$ after, so the largest term with $k < N$ is at $m = \min(N - 1, \lfloor x \rfloor)$. The code computes $\ln t_m$ with the log-gamma function, sums the ratios $t_k/t_m$ outward from $m$ in both directions by the recurrence, and multiplies. Every ratio is at most $1$, so there is no overflow, and the walk stops when a ratio drops below $10^{-18}$ of the running sum. In each direction the step ratios $x/(k+1)$ and $k/x$ decrease, so the neglected terms are bounded by a geometric series that starts below $10^{-18}$ of the sum. For the sizes in the tests this is far below the rounding error of double precision.
