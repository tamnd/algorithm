---
title: The Gaussian mechanism is (epsilon, delta)-DP under the analytic and the classical calibration
proves: [correctness]
status: full
---

We work in the real RAM, where line L4 draws an exact sample of $N(0, \sigma^2)$. Fix a neighbor relation $\sim$, a query $f$ with values in $\mathbb R^k$, a number $\Delta \ge \Delta_2 f = \max_{x \sim x'} \lVert f(x) - f(x') \rVert_2$, $\varepsilon \ge 0$ and $\delta \in (0, 1)$. Write $\Phi$ for the standard normal distribution function, $\bar\Phi = 1 - \Phi$, and $\varphi$ for the standard normal density. The output of line L6 is $M(x) = f(x) + Z$ with $Z \sim N(0, \sigma^2 I_k)$, because each pass of line L3 draws a fresh independent sample.

For $D > 0$ and $s > 0$ let

$$\delta_D(s) = \Phi\Big(\frac{D}{2s} - \frac{\varepsilon s}{D}\Big) - e^{\varepsilon}\, \Phi\Big(-\frac{D}{2s} - \frac{\varepsilon s}{D}\Big).$$

**Lemma 1 (the privacy loss is normal).** Fix $x \sim x'$ with $v = f(x) - f(x')$ and $D = \lVert v \rVert_2 > 0$, and let $\mu = D/\sigma$. Let $p$ and $q$ be the densities of $M(x)$ and $M(x')$, and $\ell(y) = \ln(p(y)/q(y))$. If $Y \sim M(x)$, then $\ell(Y) \sim N(\mu^2/2, \mu^2)$. If $Y' \sim M(x')$, then $\ell(Y') \sim N(-\mu^2/2, \mu^2)$.

*Proof.* The normalizing constants of $p$ and $q$ are equal, so $\ell(y) = (\lVert y - f(x') \rVert^2 - \lVert y - f(x) \rVert^2)/(2\sigma^2)$. For $Y = f(x) + Z$, we have $Y - f(x') = Z + v$, so

$$\ell(Y) = \frac{\lVert Z + v \rVert^2 - \lVert Z \rVert^2}{2\sigma^2} = \frac{D^2 + 2\langle Z, v \rangle}{2\sigma^2}.$$

The scalar $\langle Z, v \rangle$ is a linear combination of independent normal coordinates, so it is $N(0, \sigma^2 D^2)$. Hence $\ell(Y)$ is normal with mean $D^2/(2\sigma^2) = \mu^2/2$ and variance $4\sigma^2 D^2/(4\sigma^4) = \mu^2$. For $Y' = f(x') + Z$, $Y' - f(x) = Z - v$ and $\ell(Y') = (\lVert Z \rVert^2 - \lVert Z - v \rVert^2)/(2\sigma^2) = (2\langle Z, v\rangle - D^2)/(2\sigma^2)$, which is $N(-\mu^2/2, \mu^2)$. $\square$

**Lemma 2 (the tight delta of one pair).** For $x \sim x'$ as in Lemma 1,

$$\sup_S \big(\Pr[M(x) \in S] - e^{\varepsilon}\Pr[M(x') \in S]\big) = \delta_D(\sigma).$$

*Proof.* For any measurable $S$, $\Pr[M(x) \in S] - e^{\varepsilon}\Pr[M(x') \in S] = \int_S (p - e^{\varepsilon} q)$. This is largest for $S^* = \{y : p(y) > e^{\varepsilon} q(y)\} = \{y : \ell(y) > \varepsilon\}$, because $S^*$ holds every point where the integrand is positive and no other point. So the supremum is $\Pr[\ell(Y) > \varepsilon] - e^{\varepsilon}\Pr[\ell(Y') > \varepsilon]$. By Lemma 1,

$$\Pr[\ell(Y) > \varepsilon] = \bar\Phi\Big(\frac{\varepsilon - \mu^2/2}{\mu}\Big) = \Phi\Big(\frac{\mu}{2} - \frac{\varepsilon}{\mu}\Big), \qquad \Pr[\ell(Y') > \varepsilon] = \Phi\Big(-\frac{\mu}{2} - \frac{\varepsilon}{\mu}\Big).$$

With $\mu = D/\sigma$, $\mu/2 = D/(2\sigma)$ and $\varepsilon/\mu = \varepsilon\sigma/D$, which gives $\delta_D(\sigma)$. $\square$

The same value comes out for the pair in the other order, because the pair $(x', x)$ has the same $D$.

**Lemma 3 (monotonicity).** For fixed $\varepsilon \ge 0$, the function $g(\mu) = \Phi(\mu/2 - \varepsilon/\mu) - e^{\varepsilon}\Phi(-\mu/2 - \varepsilon/\mu)$ is strictly increasing on $\mu > 0$. Hence $\delta_D(\sigma) = g(D/\sigma)$ grows with $D$ and falls with $\sigma$.

*Proof.* Let $a = \mu/2 - \varepsilon/\mu$ and $b = -\mu/2 - \varepsilon/\mu$. Then $a^2 - b^2 = (a - b)(a + b) = \mu \cdot (-2\varepsilon/\mu) = -2\varepsilon$, so $\varphi(b) = \varphi(a)\, e^{(a^2 - b^2)/2} = e^{-\varepsilon}\varphi(a)$. The derivative is

$$g'(\mu) = \varphi(a)\Big(\frac12 + \frac{\varepsilon}{\mu^2}\Big) - e^{\varepsilon}\varphi(b)\Big(-\frac12 + \frac{\varepsilon}{\mu^2}\Big) = \varphi(a)\Big(\frac12 + \frac{\varepsilon}{\mu^2} + \frac12 - \frac{\varepsilon}{\mu^2}\Big) = \varphi(a) > 0. \quad \square$$

**Theorem 1 (analytic calibration; Balle and Wang 2018, Theorem 8).** If $\delta_\Delta(\sigma) \le \delta$, then $M$ is $(\varepsilon, \delta)$-DP. If some pair of neighbors has $D = \Delta$, the converse also holds.

*Proof.* For a pair with $D = 0$ the two output distributions are equal. For a pair with $0 < D \le \Delta$, Lemma 2 and Lemma 3 give $\Pr[M(x) \in S] - e^{\varepsilon}\Pr[M(x') \in S] \le \delta_D(\sigma) \le \delta_\Delta(\sigma) \le \delta$ for every $S$, which is the definition. Conversely, for a pair with $D = \Delta$, Lemma 2 gives a set $S^*$ with difference exactly $\delta_\Delta(\sigma)$, so $(\varepsilon, \delta)$-DP needs $\delta_\Delta(\sigma) \le \delta$. $\square$

**Lemma 4 (line L1 with the analytic bound).** The bisection of line L1 stops and returns a $\sigma$ with $\delta_\Delta(\sigma) \le \delta$, within relative distance $10^{-12}$ of the smallest such value.

*Proof.* As $s \to \infty$, $\delta_\Delta(s) \to 0$: for $\varepsilon > 0$ both arguments of $\Phi$ tend to $-\infty$, and for $\varepsilon = 0$ the value is $\Phi(\Delta/(2s)) - \Phi(-\Delta/(2s)) \to 0$. So the doubling loop stops with $\delta_\Delta(hi) \le \delta$. As $s \to 0$, the first argument tends to $+\infty$ and the second to $-\infty$, so $\delta_\Delta(s) \to 1 > \delta$, and the halving loop stops with $\delta_\Delta(lo) > \delta$. Each bisection step keeps the invariant $\delta_\Delta(lo) > \delta \ge \delta_\Delta(hi)$. By Lemma 3, the set $\{s : \delta_\Delta(s) \le \delta\}$ is an interval $[s^*, \infty)$, so $lo < s^* \le hi$ at every step. The loop stops when $hi - lo \le 10^{-12}\, hi$, and it returns $hi$. $\square$

**Theorem 2 (classical calibration; Dwork-Roth Theorem 3.22 and Theorem A.1).** Let $0 < \varepsilon < 1$, $0 < \delta < 1$, $c = \sqrt{2\ln(1.25/\delta)}$ and $\sigma \ge c\Delta/\varepsilon$. Then $M$ is $(\varepsilon, \delta)$-DP.

*Proof.* Fix a pair with $0 < D \le \Delta$ and let $\mu = D/\sigma \le \varepsilon/c$. By Lemma 2 the worst difference is at most $\Pr[\ell(Y) > \varepsilon] = \bar\Phi(t_\mu)$ with $t_\mu = \varepsilon/\mu - \mu/2$. The map $\mu \mapsto \varepsilon/\mu - \mu/2$ is decreasing, so $t_\mu \ge t = c - \varepsilon/(2c)$, and $\bar\Phi(t_\mu) \le \bar\Phi(t)$. We show $\bar\Phi(t) \le \delta$ in two cases. Since $\varepsilon < 1$ and $c - 1/(2c)$ is increasing in $c$, $t > c - 1/(2c)$.

*Case $\delta \ge 0.54$.* Then $c \ge \sqrt{2\ln 1.25} = 0.668047$, so $t > 0.668047 - 0.748450 = -0.080403$ and $\bar\Phi(t) < \Phi(0.080403) = 0.532041 < \delta$.

*Case $\delta < 0.54$.* Then $c > \sqrt{2\ln(1.25/0.54)} = 1.295623$, so $t > 1.295623 - 0.385915 = 0.909708 > 0$. The tail bound $\bar\Phi(t) \le \varphi(t)/t$ for $t > 0$ holds because $\int_t^\infty \varphi(u)\,du \le \int_t^\infty (u/t)\varphi(u)\,du = \varphi(t)/t$. Also $t^2 = c^2 - \varepsilon + \varepsilon^2/(4c^2) > c^2 - 1$, so $e^{-t^2/2} < e^{1/2} e^{-c^2/2} = e^{1/2}\delta/1.25 = 1.318977\,\delta$. Hence

$$\bar\Phi(t) \le \frac{e^{-t^2/2}}{t\sqrt{2\pi}} < \frac{1.318977\,\delta}{0.909708 \times 2.506628} = 0.578437\,\delta < \delta.$$

In both cases every pair has difference at most $\delta$ for every set $S$. $\square$

Dwork and Roth assume $c^2 > 2\ln(1.25/\delta)$; the proof above also covers equality, which is the value line L1 uses. The bound is far from tight: for $\Delta = 1$, $\varepsilon = 0.5$ and $\delta = 10^{-5}$, the exact $\delta_\Delta$ at the classical $\sigma = 9.6896$ is $1.6 \times 10^{-8}$.

**Theorem 3 (accuracy).** For $0 < \beta < 1$, with probability at least $1 - \beta$, $\max_i |y_i - f(x)_i| \le \sigma\sqrt{2\ln(2k/\beta)}$.

*Proof.* Each error $y_i - f(x)_i$ is $N(0, \sigma^2)$. For $u > 0$, $\bar\Phi(u) \le e^{-u^2/2}$: for $u \ge 1/\sqrt{2\pi}$ this follows from $\bar\Phi(u) \le \varphi(u)/u$, and for smaller $u$ we have $\bar\Phi(u) \le 1/2 < e^{-1/(4\pi)} \le e^{-u^2/2}$. So $\Pr[|y_i - f(x)_i| > \sigma u] = 2\bar\Phi(u) \le 2e^{-u^2/2}$. With $u = \sqrt{2\ln(2k/\beta)}$ this is $\beta/k$, and the [union bound](/union-bound/) over the $k$ coordinates gives total failure probability at most $\beta$. $\square$
