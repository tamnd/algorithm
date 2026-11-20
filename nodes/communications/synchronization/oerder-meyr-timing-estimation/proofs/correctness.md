---
title: The spectral line of the squared signal has the mean (beta/8) N e^(-j 2 pi tau), so the Oerder and Meyr estimate is unbiased in phase and needs at least three samples per symbol
proves: [correctness]
status: full
---

Times are in symbol periods, $T = 1$. The input is $x[n] = y(n/L_s)$ for $n = 0, \ldots, N - 1$ with $N = L_0 L_s$, where $y(t) = e^{j\theta}\sum_m a_m g(t - m - \tau) + v(t)$. The pulse $g$ is a raised cosine with roll-off $0 < \beta < 1$, the data are independent with $E a_m = 0$ and $E|a_m|^2 = 1$ and extend beyond the window on both sides, and $v$ is stationary noise independent of the data with $E|v(t)|^2 = \sigma_v^2$. Lines L1 to L4 compute
$$X = \sum_{n=0}^{N-1}|x[n]|^2 e^{-j2\pi n/L_s},$$
and line L5 returns $\hat\tau = -\arg(X)/(2\pi)$.

**Lemma 1 (mean power).** $E|y(t)|^2 = 1 - \frac{\beta}{4} + \sigma_v^2 + \frac{\beta}{4}\cos(2\pi(t - \tau))$, for every $\theta$.

*Proof.* The factor $e^{j\theta}$ drops out of $|y|^2$. The cross terms between different symbols, and between data and noise, have mean zero. What remains is $\sum_m g(t - m - \tau)^2 + \sigma_v^2$, and the folded energy formula $\sum_m g(x + m)^2 = 1 - \frac{\beta}{4} + \frac{\beta}{4}\cos(2\pi x)$, proved on the [early-late gate](/early-late-gate-synchronizer/) proof page by Poisson summation, gives the result. $\square$

**Theorem 1 (mean of the spectral line).** If $L_s \ge 3$ and $N$ is a multiple of $L_s$, then
$$E[X] = \frac{\beta}{8}N e^{-j2\pi\tau}.$$
So $-\arg E[X]/(2\pi) = \tau$ modulo one symbol.

*Proof.* Write $\phi_n = 2\pi n/L_s$. By Lemma 1, $E[X] = \sum_n \bigl(c + \frac{\beta}{4}\cos(\phi_n - 2\pi\tau)\bigr)e^{-j\phi_n}$ with the constant $c = 1 - \frac{\beta}{4} + \sigma_v^2$. Over a whole number of periods, $\sum_n e^{-j\phi_n} = 0$, so the constant drops out. Expand the cosine:
$$\cos(\phi_n - 2\pi\tau)e^{-j\phi_n} = \frac12 e^{-j2\pi\tau} + \frac12 e^{j2\pi\tau}e^{-j2\phi_n}.$$
The first term sums to $\frac{N}{2}e^{-j2\pi\tau}$. The second sums to zero because $e^{-j2\phi_n} = e^{-j4\pi n/L_s}$ runs over whole periods of a nontrivial root of unity when $L_s \ge 3$. Multiply by $\frac{\beta}{4}$. $\square$

**Theorem 2 (why $L_s = 2$ fails).** For $L_s = 2$, the rotations are $e^{-j\pi n} = \pm1$, so $X$ is real and $\arg X \in \{0, \pi\}$ for every input. The estimate cannot show $\tau$.

*Proof.* Immediate. In Theorem 1, the second term then does not cancel: $e^{-j2\pi n} = 1$, and $E[X] = \frac{\beta}{8}N(e^{-j2\pi\tau} + e^{j2\pi\tau}) = \frac{\beta}{4}N\cos(2\pi\tau)$, which is real. This is aliasing: $|y|^2$ has a band up to $1 + \beta$ cycles per symbol, and sampling it at two per symbol folds the line at $+1$ onto the line at $-1$. $\square$

**Theorem 3 (exact for alternating data).** If $a_m = (-1)^m$ and there is no noise, then $X = \frac{N}{4}e^{-j2\pi\tau}$ exactly, for every window, so $\hat\tau = \tau$.

*Proof.* By Poisson summation, $y(t) = \pm e^{j\theta}\cos(\pi(t - \tau))$, as in the early-late gate proof. So $|y(t)|^2 = \frac12 + \frac12\cos(2\pi(t - \tau))$ with no random part, and the computation of Theorem 1 with $\frac12$ in place of $\frac{\beta}{4}$ gives $X$ itself, not only its mean. $\square$

**Theorem 4 (consistency).** As $L_0 \to \infty$, $X/N \to \frac{\beta}{8}e^{-j2\pi\tau}$ in mean square, so $\hat\tau \to \tau$ modulo one.

*Proof.* The sequence $|x[n]|^2$ is periodic in distribution with period $L_s$ and has a covariance that decays with the distance $|n - n'|$ in symbols, because $g(t)$ decays as $|t|^{-3}$ and the data are independent. So the covariances are summable and $\operatorname{Var}(X/N) = O(1/N)$. With Theorem 1 this gives convergence in mean square. The argument is a continuous function of $X$ away from $X = 0$, and the limit is not zero for $\beta > 0$. $\square$

Theorem 1 is a closed form under assumptions: raised cosine pulses, independent zero-mean data that fill the window and extend past it, stationary noise, and a constant delay. The variance of $\hat\tau$ for a finite $L_0$ comes from two sources, the noise and the data pattern (self-noise). It is not given in closed form here; the page reports measurements against the [MCRB](/modified-cramer-rao-bound/). The tests check Theorem 3 to $10^{-5}$ for $L_s \in \{3, 4, 5, 8\}$, and check that $\hat\tau$ equals the maximum of the grid search over $J(\tau_c) = \sum_n |x[n]|^2\cos(2\pi(n/L_s - \tau_c))$ to $10^{-7}$; this holds because $J(\tau_c) = \operatorname{Re}\{X e^{j2\pi\tau_c}\} = |X|\cos(\arg X + 2\pi\tau_c)$ is largest at $\tau_c = -\arg X/(2\pi)$.
