---
title: Volumetric path tracing is an unbiased estimator of the radiative transfer equation
proves: [correctness]
status: full
---

We take a medium with $0 \le \sigma_s \le \sigma_t \le \mu$, vacuum boundaries that emit nothing, no emission in the medium, and light sources whose direct contribution at a point $y$ for the view direction $\omega$ is

$$D(y, \omega) = \int p(\omega, \omega_l)\, \Lambda(y, \omega_l)\, T(y, y_l)\, d\lambda,$$

an integral over the points or directions of the lights, with $\Lambda \ge 0$ the unoccluded incident radiance or irradiance of the light. Next event estimation draws one light sample $(\omega_l, y_l)$ from a density $q_l$ and returns $p\,\Lambda\,\hat T / q_l$, with $\hat T$ an independent unbiased estimate of $T(y, y_l)$. We assume $E[p \Lambda T / q_l] = D(y, \omega)$, which holds when $q_l > 0$ wherever $p\Lambda T > 0$.

Let $\mathcal{K}$ be the transport operator

$$(\mathcal{K} f)(x, \omega) = \int_0^{s(x, \omega)} T(x, x_t)\, \sigma_s(x_t) \int_{S^2} p(\omega, \omega')\, f(x_t, \omega')\, d\omega'\, dt,$$

and $(\mathcal{T} g)(x, \omega) = \int_0^{s} T(x, x_t)\,\sigma_s(x_t)\, g(x_t, \omega)\, dt$. The radiance with the direct light separated is $L = \mathcal{T} D + \mathcal{K} L$, and its Neumann series is $L = \sum_{j \ge 1} L_j$ with $L_1 = \mathcal{T} D$ and $L_{j+1} = \mathcal{K} L_j$. Each $L_j \ge 0$, and we assume that the series converges, which holds when $\alpha \le c < 1$ or when the medium has a finite optical size.

**Lemma 1 (one collision).** Let $x$ and $\omega$ be given, and let $t$ be drawn by line L3. For each nonnegative measurable $g$,

$$E\left[\mathbf{1}\{t \ne \text{ESCAPE}\}\, \alpha(x_t)\, g(x_t)\right] = \int_0^s T(x, x_t)\, \sigma_s(x_t)\, g(x_t)\, dt.$$

*Proof.* By Theorem 1 of the proof for [delta tracking](/delta-tracking/), $t$ has the density $\sigma_t(x_t) T(x, x_t)$ on $[0, s)$ and the rest of the mass on ESCAPE. So the left side is $\int_0^s \sigma_t T \cdot (\sigma_s/\sigma_t)\, g\, dt$, which is the right side. Points with $\sigma_t = 0$ have density 0 and do not matter. $\square$

**Lemma 2 (Russian roulette).** Let $Y \ge 0$ be a random variable that is independent of the roulette number, and let $0 < q \le 1$. Then the variable that is $Y/q$ with probability $q$ and 0 otherwise has the mean $E[Y]$.

*Proof.* $E = q \cdot E[Y]/q + (1 - q) \cdot 0$. $\square$

Let $C_j$ be the value added in line L7 at the $j$-th collision, and 0 if the path has fewer than $j$ collisions. Let $G_j(x, \omega) = E[C_j]$ for a path that starts at $x$ in the direction $\omega$ with $\beta = 1$.

**Lemma 3 (one order).** With no cap, for each $j \ge 1$, $G_j = L_j$.

*Proof.* By induction on $j$. For $j = 1$: the first collision is at $x_t$ with weight $\beta = \alpha(x_t)$, and line L7 adds $\beta$ times a light sample with mean $D(x_t, \omega)$, independent of $t$ given $x_t$. By Lemma 1 with $g = D(\cdot, \omega)$, $E[C_1] = \mathcal{T} D = L_1$. Roulette in line L9 acts after line L7, so it does not change $C_1$.

For $j + 1$: after the first collision the path is at $x_t$ with weight $\alpha(x_t)$. Line L8 draws $\omega'$ with density $p(\omega, \omega')$, and the weight $p/\text{pdf}$ is 1. Line L9 multiplies the weight by $1/q$ and keeps the path with probability $q$. From there, the path is a new path from $(x_t, \omega')$ multiplied by its current weight, and its $j$-th collision is the $(j+1)$-th collision of the whole path. The weight factors multiply, so by the induction hypothesis and Lemma 2,

$$E[C_{j+1} \mid x_t, \omega'] = \alpha(x_t)\, G_j(x_t, \omega') = \alpha(x_t)\, L_j(x_t, \omega').$$

Taking the expectation over $\omega'$ gives $\alpha(x_t) \int p(\omega, \omega') L_j(x_t, \omega')\, d\omega'$, and by Lemma 1 the expectation over $t$ gives $(\mathcal{K} L_j)(x, \omega) = L_{j+1}$. $\square$

**Theorem 1.** Without a cap, $E[\sum_j C_j] = \sum_j L_j = L(x, \omega)$. With a cap of $K$ collisions, the expectation is $\sum_{j \le K} L_j$.

*Proof.* Each $C_j \ge 0$, so by the monotone convergence theorem $E[\sum_j C_j] = \sum_j E[C_j]$, and Lemma 3 gives $\sum_j L_j$. With a cap, $C_j = 0$ for $j > K$, and Lemma 3 holds unchanged for $j \le K$. $\square$

**Theorem 2 (finite variance).** Let $\alpha \le 1$, $q = \min(1, \beta)$ in line L9, and let the light term be bounded, $p \Lambda \hat T / q_l \le M$. Then the variance of one path is finite if the number of collisions has a finite second moment, for example when the probability of a further collision is at most $c < 1$ at each step.

*Proof.* Before roulette $\beta \le 1$, because each factor of line L6 is at most 1 and line L8 has the weight 1. If $\beta < 1$ then $q = \beta$, and a path that survives has $\beta = 1$. So $\beta \le 1$ at each line L7, and $C_j \le M$. The total is at most $M$ times the number of collisions $J$, so $E[(\sum C_j)^2] \le M^2 E[J^2] < \infty$. $\square$
