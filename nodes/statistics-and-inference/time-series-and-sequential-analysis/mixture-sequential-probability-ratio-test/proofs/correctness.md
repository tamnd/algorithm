---
title: The mSPRT has level alpha at every stopping time and its p-values are always valid
proves: [correctness]
status: full
---

Notation is that of the page. $X_1, X_2, \ldots$ are i.i.d. with density $f_\theta$ with respect to a measure $\nu$, $\mathcal F_n = \sigma(X_1, \ldots, X_n)$ with $\mathcal F_0$ trivial, and $\pi$ is a probability measure on the parameters, fixed before the data. We assume that every $f_\theta$ is positive wherever $f_{\theta_0}$ is, and that $(\theta, x) \mapsto f_\theta(x)$ is jointly measurable. Write
$$L_n(\theta) = \prod_{i=1}^n \frac{f_\theta(X_i)}{f_{\theta_0}(X_i)}, \qquad \Lambda_n = \int L_n(\theta)\,\pi(d\theta), \qquad L_0 = \Lambda_0 = 1.$$
All probabilities and expectations below are under $P_{\theta_0}$, written $P$ and $E$.

**Lemma 1 (closed form for the normal model).** If $f_\theta$ is the $N(\theta, \sigma^2)$ density and $\pi = N(\theta_0, \tau^2)$, then with $S_n = \sum_{i \le n}(X_i - \theta_0)$,
$$\Lambda_n = \sqrt{\frac{\sigma^2}{\sigma^2 + n\tau^2}}\,\exp\left(\frac{\tau^2 S_n^2}{2\sigma^2(\sigma^2 + n\tau^2)}\right).$$

*Proof.* Let $u = \theta - \theta_0$. Expanding the squares in the normal densities,
$$\log L_n(\theta) = \sum_{i=1}^n \frac{(X_i - \theta_0)^2 - (X_i - \theta_0 - u)^2}{2\sigma^2} = \frac{u S_n}{\sigma^2} - \frac{n u^2}{2\sigma^2}.$$
Let $c = n/\sigma^2 + 1/\tau^2 = (\sigma^2 + n\tau^2)/(\sigma^2\tau^2)$ and $m = S_n/(\sigma^2 c)$. Then
$$\Lambda_n = \int \frac{1}{\sqrt{2\pi}\tau}\exp\left(\frac{u S_n}{\sigma^2} - \frac{c u^2}{2}\right)du = \frac{1}{\sqrt{2\pi}\tau}\exp\left(\frac{c m^2}{2}\right)\int \exp\left(-\frac{c(u - m)^2}{2}\right)du = \frac{1}{\tau\sqrt c}\exp\left(\frac{S_n^2}{2\sigma^4 c}\right).$$
Here $\tau^2 c = (\sigma^2 + n\tau^2)/\sigma^2$, and $S_n^2/(2\sigma^4 c) = \tau^2 S_n^2/(2\sigma^2(\sigma^2 + n\tau^2))$. $\square$

**Lemma 2 (test martingale).** $(\Lambda_n)_{n \ge 0}$ is a nonnegative martingale under $P$ with $\Lambda_0 = 1$.

*Proof.* $\Lambda_n \ge 0$ since it is an integral of a nonnegative function, and it is $\mathcal F_n$-measurable by the joint measurability. For each $\theta$ and $n \ge 1$, $X_n$ is independent of $\mathcal F_{n-1}$ and
$$E\left[\frac{f_\theta(X_n)}{f_{\theta_0}(X_n)}\right] = \int_{\{f_{\theta_0} > 0\}} f_\theta\,d\nu \le 1,$$
with equality because $f_\theta$ is positive only where $f_{\theta_0}$ is. Hence $E[L_n(\theta) \mid \mathcal F_{n-1}] = L_{n-1}(\theta)$. For a nonnegative jointly measurable integrand, Tonelli's theorem lets us exchange the conditional expectation and the integral over $\pi$: for every bounded nonnegative $\mathcal F_{n-1}$-measurable $W$,
$$E[W\Lambda_n] = \int E[W L_n(\theta)]\,\pi(d\theta) = \int E[W L_{n-1}(\theta)]\,\pi(d\theta) = E[W\Lambda_{n-1}].$$
With $W = 1$ and induction, $E[\Lambda_n] = 1$, so $\Lambda_n$ is integrable, and the identity for all such $W$ is the statement $E[\Lambda_n \mid \mathcal F_{n-1}] = \Lambda_{n-1}$. $\square$

**Theorem 1 (level at every stopping time).** Let $T$ be any stopping time with respect to $(\mathcal F_n)$, possibly infinite. The probability that the mSPRT rejects $H_0$ at some $n \le T$ is at most $\alpha$.

*Proof.* The test rejects at some $n \le T$ only if $\Lambda_n \ge 1/\alpha$ for some $n \ge 1$. By Lemma 2 and Ville's inequality applied to the nonnegative martingale $\Lambda$,
$$P(\exists n \ge 1: \Lambda_n \ge 1/\alpha) \le \alpha\,E[\Lambda_0] = \alpha. \qquad \square$$

**Theorem 2 (always valid p-values).** Let $p_n = \min(1, 1/\max_{1 \le k \le n}\Lambda_k)$ for $n \ge 1$, the value kept by line L5, and $p_\infty = \lim_n p_n$, which exists because $p_n$ never increases. For every stopping time $T$, possibly infinite, and every $u \in [0, 1]$,
$$P(p_T \le u) \le u.$$

*Proof.* For $u = 1$ there is nothing to prove, and for $u = 0$ the event $\{p_T = 0\}$ is contained in $\{\sup_n \Lambda_n = \infty\}$, which has probability at most $\varepsilon$ for every $\varepsilon > 0$ by Ville's inequality at level $1/\varepsilon$. Let $0 < u < 1$. If $T < \infty$ and $p_T \le u$, then $\max_{k \le T}\Lambda_k \ge 1/u$. If $T = \infty$ and $p_\infty \le u$, then $\sup_k \Lambda_k \ge 1/u$. In both cases $\sup_k \Lambda_k \ge 1/u$, so by Ville's inequality the probability is at most $u$. $\square$

**Lemma 3 (the procedure).** After iteration $n$ of the loop of line L2, $S = S_n$, $\Lambda = \Lambda_n$ and $p = p_n$; the procedure rejects exactly at $N = \inf\{n : \Lambda_n \ge 1/\alpha\}$ if that is reached before the stream ends.

*Proof.* By induction on $n$. Line L1 sets $S = 0$, $n = 0$ and $p = 1$. Line L3 adds $X_n - \theta_0$ to $S$, line L4 evaluates the formula of Lemma 1, and line L5 sets $p = \min(p_{n-1}, 1/\Lambda_n)$, which is $p_n$ because $p_0 = 1$ makes the outer $\min$ with 1 automatic. Line L6 returns at the first $n$ with $\Lambda_n \ge 1/\alpha$. $\square$

**Theorem 3 (power one, normal model).** If the data are $N(\theta, \sigma^2)$ with $\theta \ne \theta_0$, then $\Lambda_n \to \infty$ almost surely, so the mSPRT rejects at a finite time with probability 1.

*Proof.* Let $\delta = \theta - \theta_0$. By the strong law of large numbers $S_n/n \to \delta$ almost surely. Then
$$\log\Lambda_n = \frac{\tau^2 S_n^2}{2\sigma^2(\sigma^2 + n\tau^2)} - \frac12\log\left(1 + \frac{n\tau^2}{\sigma^2}\right) = n\left(\frac{\tau^2 (S_n/n)^2}{2\sigma^2(\sigma^2/n + \tau^2)} - \frac{\log(1 + n\tau^2/\sigma^2)}{2n}\right),$$
and the bracket tends to $\delta^2/(2\sigma^2) > 0$. So $\log\Lambda_n \to \infty$ almost surely. $\square$

Theorems 1 and 2 with Lemma 3 give the guarantees of the page: the procedure has type I error at most $\alpha$ whenever and however the analyst stops it, and the p-value it reports at that time is valid. $\blacksquare$
