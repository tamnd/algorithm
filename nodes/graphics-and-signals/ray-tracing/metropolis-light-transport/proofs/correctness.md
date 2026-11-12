---
title: Unbiasedness of Metropolis light transport with start-up bias elimination
proves: [correctness]
status: full
---

**Setting.** $\mathcal P$ is the space of paths with the measure $\mu$, $f \ge 0$ is the scalar contribution, and $b = \int f\, d\mu$ is finite and positive. For a pixel $j$ let $g_j(\bar x) = \mathbf 1[j(\bar x) = j]$, so that $I_j = \int f g_j\, d\mu$. $T$ is a probability density on $\mathcal P$ with $T > 0$ wherever $f > 0$. The small change has a density $S(x \to y)$ with $S(x \to y) = S(y \to x)$.

**The kernel.** For $x$ with $f(x) > 0$, one pass of lines L4 to L7 moves to $y \ne x$ with the density

$$k(x, y) = p\, T(y)\, a_T(x, y) + (1 - p)\, S(x \to y)\, a_S(x, y),$$

$$a_T(x, y) = \min\Big(1, \frac{f(y) T(x)}{f(x) T(y)}\Big), \qquad a_S(x, y) = \min\Big(1, \frac{f(y)}{f(x)}\Big),$$

and stays at $x$ with the remaining probability $r(x) = 1 - \int k(x, y)\, d\mu(y)$. Write $K g(x) = \int k(x, y) g(y)\, d\mu(y) + r(x) g(x)$.

**Lemma 1 (detailed balance).** For $x \ne y$ with $f(x), f(y) > 0$, $f(x) k(x, y) = f(y) k(y, x)$.

*Proof.* $f(x)\, T(y)\, a_T(x, y) = \min(f(x) T(y), f(y) T(x))$ and $f(x)\, S(x \to y)\, a_S(x, y) = \min(f(x), f(y))\, S(x \to y)$. Both are symmetric in $x$ and $y$, the second because $S$ is. Add them with the weights $p$ and $1 - p$. If $f(y) = 0$ then $k(x, y) = 0$, so the chain never leaves the set $\{f > 0\}$. $\square$

**Lemma 2 (stationarity).** For every bounded $g$, $\int f\, K g\, d\mu = \int f g\, d\mu$.

*Proof.* By Lemma 1 and Fubini,

$$\int f(x) \int k(x, y) g(y)\, d\mu(y)\, d\mu(x) = \int g(y) \int f(y) k(y, x)\, d\mu(x)\, d\mu(y) = \int f(y) g(y) (1 - r(y))\, d\mu(y).$$

Adding $\int f r g\, d\mu$ for the rejections gives $\int f g\, d\mu$. $\square$

**Lemma 3 (the resampled start).** Let $y_1, \dots, y_n$ be independent with the density $T$, $w_i = f(y_i) / T(y_i)$, $\hat b = \frac1n \sum_i w_i$, and let $x_0 = y_I$ with $P(I = i) = w_i / \sum_l w_l$ (and $\hat b = 0$ if all $w_i$ are $0$). Then for every bounded $h$, $E[\hat b\, h(x_0)] = \int f h\, d\mu$.

*Proof.* Given the $y_i$, $E[\hat b\, h(x_0) \mid y_1, \dots, y_n] = \hat b \sum_i \frac{w_i}{\sum_l w_l} h(y_i) = \frac1n \sum_i w_i h(y_i)$, also when all $w_i$ are $0$. Each term has the mean $\int T \cdot \frac{f}{T} \cdot h\, d\mu = \int f h\, d\mu$, using $T > 0$ where $f > 0$. $\square$

**Claim.** Let $x_0, x_1, \dots, x_M$ be the states of the chain, and let $R_j$ be the value that line L8 gives for pixel $j$. Then $E[R_j] = I_j$ for every $M \ge 1$.

**Proof.** At step $m + 1$, line L6 adds $a\, g_j(y) + (1 - a)\, g_j(x_m)$, where $y$ is the proposal and $a$ its acceptance. Given $x_m$, the mean of this value over $y$ is

$$\int k(x_m, y) g_j(y)\, d\mu(y) + r(x_m) g_j(x_m) = K g_j(x_m),$$

because the two proposals together propose $y$ with the density $p T(y) + (1 - p) S(x_m \to y)$, and $a$ times that density is $k(x_m, y)$. This is also the mean of $g_j(x_{m+1})$, so the expected value recording does not change the mean.

The value $\hat b$ is fixed once the bootstrap is done, and the chain from $x_0$ on is a Markov chain with the kernel $K$. So $E[\hat b\, K g_j(x_m)] = E[\hat b\, (K^{m+1} g_j)(x_0)]$, and by Lemma 3 with $h = K^{m+1} g_j$, which is bounded by $1$,

$$E[\hat b\, K g_j(x_m)] = \int f\, K^{m+1} g_j\, d\mu = \int f g_j\, d\mu = I_j,$$

where the middle step applies Lemma 2 $m + 1$ times. Line L8 gives $R_j = \frac{\hat b}{M} \sum_{m=0}^{M-1} [a_m g_j(y_m) + (1 - a_m) g_j(x_m)]$, whose mean is $\frac1M \sum_m I_j = I_j$. $\square$

**Consistency.** The large step proposes every path in $\{f > 0\}$ with a positive density, so the chain is irreducible there, and it is aperiodic because each step can reject. By the ergodic theorem for such chains, $\frac1M \sum_m g_j(x_m) \to I_j / b$ almost surely for almost every start, and $\hat b \to b$ as $n \to \infty$ by the law of large numbers. Without the large step, irreducibility can fail, and then the chain may never reach parts of $\{f > 0\}$; the image is then wrong even in the limit.

**The independent chains.** Different chains use independent random numbers, so their values $R_j$ are independent and have the same distribution with mean $I_j$. The mean of $R$ chains has the variance $\mathrm{Var}(R_j) / R$, which the sample variance over the chains estimates without bias. This is the standard error that the tests use.
