---
title: Delta tracking samples the exact free-flight distance, and both transmittance estimators are unbiased
proves: [correctness]
status: full
---

Fix the segment $[0, s)$, a measurable extinction coefficient $\sigma_t$ with $0 \le \sigma_t(t) \le \mu$ on the segment, and $\mu > 0$. Write $\tau(x, y) = \int_x^y \sigma_t(u)\,du$. All random numbers are independent and uniform on $[0, 1)$.

**Lemma 1 (one step).** If the walk is at the point $x$, then the next tentative point $x + E$ of line L3 has $P(E > h) = e^{-\mu h}$ for $h \ge 0$, and it is independent of the past.

*Proof.* $E = -\ln(1 - \xi)/\mu$ and $P(E > h) = P(1 - \xi < e^{-\mu h}) = e^{-\mu h}$, because $1 - \xi$ is uniform on $(0, 1]$. The number $\xi$ is new, so $E$ is independent of the past. $\square$

**Lemma 2 (termination).** The walk stops with probability 1, and the number of tentative points before it stops has a finite mean.

*Proof.* The tentative points are partial sums of independent exponential gaps with rate $\mu$. The number of partial sums less than $s$ is Poisson with mean $\mu s$, so it is finite with probability 1 and has mean $\mu s$. The walk examines no more points than this and then stops at line L4 or line L6. $\square$

For $0 \le x \le y \le s$ let $Q(x, y)$ be the probability that a walk started at $x$ has no real collision in $[x, y)$. This is the probability that its returned value is ESCAPE or a number at least $y$.

**Lemma 3 (integral equation).** $Q$ satisfies

$$Q(x, y) = e^{-\mu(y - x)} + \int_x^y \mu e^{-\mu(t - x)} \left(1 - \frac{\sigma_t(t)}{\mu}\right) Q(t, y)\,dt.$$

*Proof.* Condition on the first tentative point $x + E$. If $E \ge y - x$, which has probability $e^{-\mu(y - x)}$ by Lemma 1, there is no collision in $[x, y)$. Otherwise the first tentative point $t = x + E$ has the density $\mu e^{-\mu(t - x)}$ on $[x, y)$. Line L6 makes it a null collision with probability $1 - \sigma_t(t)/\mu$, using a new random number. After a null collision the walk is at $t$ and uses only new random numbers, so it is a new walk from $t$, and it has no real collision in $[t, y)$ with probability $Q(t, y)$. A real collision at $t < y$ gives no contribution. Adding the cases gives the equation. $\square$

**Lemma 4 (uniqueness).** For a fixed $y$, the equation of Lemma 3 has at most one bounded solution $x \mapsto Q(x, y)$ on $[0, y]$.

*Proof.* Let $D(x)$ be the difference of two bounded solutions and $M = \sup_{[0, y]} |D|$. The kernel $k(x, t) = \mu e^{-\mu(t - x)}(1 - \sigma_t(t)/\mu)$ satisfies $0 \le k \le \mu$. So $|D(x)| \le \mu \int_x^y |D(t)|\,dt$. By induction on $j$, $|D(x)| \le M (\mu (y - x))^j / j!$ for each $j \ge 0$: the case $j = 0$ is the definition of $M$, and the step is $\mu \int_x^y M(\mu(y - t))^j/j!\,dt = M(\mu(y - x))^{j+1}/(j+1)!$. The right side goes to 0 as $j \to \infty$, so $D = 0$. $\square$

**Theorem 1 (exact free flight).** For $0 \le x \le y \le s$, $Q(x, y) = e^{-\tau(x, y)}$. In particular a walk from 0 returns a value at least $t$, or ESCAPE, with probability $T(t) = e^{-\tau(0, t)}$, and it returns ESCAPE with probability $T(s)$.

*Proof.* Let $g(t) = e^{-\mu(t - x)} e^{-\tau(t, y)}$ for $t \in [x, y]$. It is absolutely continuous, and $g'(t) = (-\mu + \sigma_t(t))\,g(t)$ almost everywhere, because $\frac{d}{dt}\tau(t, y) = -\sigma_t(t)$ almost everywhere. Put $e^{-\tau(t, y)}$ for $Q(t, y)$ in the right side of Lemma 3:

$$e^{-\mu(y - x)} + \int_x^y (\mu - \sigma_t(t))\, g(t)\,dt = e^{-\mu(y - x)} - [g(t)]_x^y = e^{-\mu(y - x)} - e^{-\mu(y - x)} + e^{-\tau(x, y)} = e^{-\tau(x, y)}.$$

So $e^{-\tau(\cdot, y)}$ is a bounded solution, and by Lemma 4 it is $Q(\cdot, y)$. The probability that the walk from 0 has no real collision in $[0, t)$ is $Q(0, t)$. The walk returns ESCAPE exactly when it has no real collision in $[0, s)$, which has probability $Q(0, s) = T(s)$. $\square$

**Corollary 1 (track-length estimator).** The indicator of ESCAPE has mean $T(s)$ and variance $T(s)(1 - T(s))$. This follows from Theorem 1.

**Theorem 2 (ratio tracking is unbiased).** Let $W$ be the value of RATIO-TRACKING. Then $E[W] = T(s)$ and $E[W^2] = e^{-\int_0^s (2\sigma_t - \sigma_t^2/\mu)}$.

*Proof.* By Lemma 1 the tentative points of lines L10 and L11 are the points of a Poisson process of rate $\mu$ on $[0, s)$. Given that there are $k$ points, which has probability $e^{-\mu s}(\mu s)^k/k!$, the points are distributed as $k$ independent uniform points on $[0, s)$, in sorted order. The product $W = \prod_i (1 - \sigma_t(t_i)/\mu)$ does not depend on the order. So

$$E[W] = \sum_{k \ge 0} e^{-\mu s} \frac{(\mu s)^k}{k!} \left(\frac{1}{s}\int_0^s \left(1 - \frac{\sigma_t(t)}{\mu}\right) dt\right)^k = e^{-\mu s} \sum_{k \ge 0} \frac{1}{k!}\left(\int_0^s (\mu - \sigma_t)\right)^k = e^{-\mu s} e^{\mu s - \tau(0, s)} = T(s).$$

The same computation with the squared factors $(1 - \sigma_t/\mu)^2$ gives $E[W^2] = e^{-\mu s} \exp\left(\int_0^s \mu (1 - \sigma_t/\mu)^2\right) = \exp\left(-\int_0^s (2\sigma_t - \sigma_t^2/\mu)\right)$. $\square$

**Corollary 2 (the variance of ratio tracking).** $\operatorname{Var}[W] \le T(s)(1 - T(s))$.

*Proof.* Each factor is in $[0, 1]$, so $0 \le W \le 1$ and $W^2 \le W$. Then $\operatorname{Var}[W] = E[W^2] - T^2 \le E[W] - T^2 = T(1 - T)$. $\square$

**Theorem 3 (the expected number of steps).** The expected number of tentative points that delta tracking examines at line L6 is $\int_0^s \mu\,T(t)\,dt \le \mu s$.

*Proof.* The tentative points form a Poisson process of rate $\mu$, by Lemma 1, if we let the walk generate them past its stop. A point at $t$ is examined if and only if the walk has had no real collision in $[0, t)$, and this event depends only on the points before $t$ and their accept numbers. By Theorem 1 it has probability $T(t)$. Campbell's formula for a Poisson process gives the expected number of examined points as $\int_0^s \mu\,T(t)\,dt$. Since $T \le 1$, this is at most $\mu s$. $\square$
