---
title: The discrete Gaussian sampler is exact and the mechanism is zCDP
proves: [correctness]
status: full
---

We work in the word RAM with exact rational arithmetic and assume a source of independent uniform random integers: a call with argument $d \ge 1$ returns each of $0, \ldots, d-1$ with probability $1/d$. For rational $p = n/d \in [0, 1]$, the draw "a uniform integer in $\{0, \ldots, d-1\}$ is below $n$" is a Bernoulli$(p)$ draw. For $\sigma^2 > 0$ write $w(y) = e^{-y^2/(2\sigma^2)}$ and $Z_\sigma = \sum_{y \in \mathbb Z} w(y)$, so that $N_{\mathbb Z}(0, \sigma^2)$ has mass $w(y)/Z_\sigma$ at $y$.

A loop whose rounds are independent and succeed with the same probability $s > 0$ stops with probability 1, after a geometric number of rounds with mean $1/s$, and its output has the law of one round conditioned on success. We use this fact for each rejection loop.

**Lemma 1 (BERNOULLI-EXP, $0 \le \gamma \le 1$).** The procedure that sets $K = 1$, increases $K$ while a Bernoulli$(\gamma/K)$ draw is 1, and returns 1 if $K$ is odd, stops with probability 1 and returns 1 with probability $e^{-\gamma}$.

*Proof.* Each $\gamma/K \le 1$, so each draw is valid. The event $K > k$ is that the first $k$ draws are 1, so $\Pr[K > k] = \prod_{j=1}^{k}\gamma/j = \gamma^k/k!$, which tends to 0; the procedure stops with probability 1. Then $\Pr[K = k] = \gamma^{k-1}/(k-1)! - \gamma^k/k!$, and
$$\Pr[K \text{ odd}] = \sum_{k \text{ odd}}\left(\frac{\gamma^{k-1}}{(k-1)!} - \frac{\gamma^k}{k!}\right) = \sum_{j \ge 0}\frac{(-\gamma)^j}{j!} = e^{-\gamma},$$
where the series converges absolutely. The expected number of draws is $E[K] = \sum_{k \ge 0}\Pr[K > k] = e^{\gamma} \le e$. $\square$

**Lemma 2 (BERNOULLI-EXP, $\gamma > 1$).** For rational $\gamma > 1$, running the case $\gamma = 1$ up to $\lfloor\gamma\rfloor$ times, returning 0 at the first 0, and else returning BERNOULLI-EXP$(\gamma - \lfloor\gamma\rfloor)$, returns 1 with probability $e^{-\gamma}$.

*Proof.* The result is 1 exactly when all $\lfloor\gamma\rfloor + 1$ independent calls return 1. By Lemma 1 this has probability $(e^{-1})^{\lfloor\gamma\rfloor}e^{-(\gamma - \lfloor\gamma\rfloor)} = e^{-\gamma}$. $\square$

**Lemma 3 (DISCRETE-LAPLACE).** For an integer $t \ge 1$, DISCRETE-LAPLACE$(t)$ stops with probability 1 and returns $Y$ with $\Pr[Y = y] = \frac{1 - e^{-1/t}}{1 + e^{-1/t}}e^{-|y|/t}$ for $y \in \mathbb Z$.

*Proof.* Consider one round. $U$ is uniform in $\{0, \ldots, t-1\}$ and is kept with probability $e^{-U/t}$ (Lemma 1), so $\Pr[U = u, \text{kept}] = e^{-u/t}/t$. $V$ counts the 1s before the first 0 of independent Bernoulli$(e^{-1})$ draws, so $\Pr[V = v] = (1 - e^{-1})e^{-v}$. Every $x \ge 0$ is $u + tv$ for exactly one pair with $0 \le u < t$, so
$$\Pr[X = x, \text{kept}] = \frac{1 - e^{-1}}{t}e^{-u/t - v} = c\,e^{-x/t}, \qquad c = \frac{1 - e^{-1}}{t}.$$
The sign $B$ is fair and independent. The round fails when $B = 1$ and $X = 0$. For $y > 0$ the round returns $y$ when $X = y$ and $B = 0$; for $y < 0$, when $X = -y$ and $B = 1$; for $y = 0$, when $X = 0$ and $B = 0$. In all three cases $\Pr[\text{round returns } y] = \frac c2 e^{-|y|/t}$. This is positive and summable, so the round succeeds with a fixed probability $s > 0$, and the output of the loop has mass proportional to $e^{-|y|/t}$. Normalizing, $\sum_y e^{-|y|/t} = (1 + e^{-1/t})/(1 - e^{-1/t})$. $\square$

**Lemma 4 (lines L1 to L6 sample exactly).** DISCRETE-GAUSSIAN-MECHANISM$(v, \sigma^2)$ stops with probability 1 and returns $v + Y$ with $Y \sim N_{\mathbb Z}(0, \sigma^2)$.

*Proof.* Line L1 gives an integer $t \ge 1$; the argument below works for every such $t$. In one round, line L3 gives $Y = y$ with probability $c_t e^{-|y|/t}$ by Lemma 3, and lines L4 and L5 accept it with probability $e^{-\gamma(y)}$ by Lemmas 1 and 2, where $\gamma(y) = (|y| - \sigma^2/t)^2/(2\sigma^2) \ge 0$ is rational. Expanding the square,
$$\frac{|y|}{t} + \gamma(y) = \frac{|y|}{t} + \frac{y^2}{2\sigma^2} - \frac{|y|}{t} + \frac{\sigma^2}{2t^2} = \frac{y^2}{2\sigma^2} + \frac{\sigma^2}{2t^2}.$$
So $\Pr[\text{round returns } y] = c_t e^{-\sigma^2/(2t^2)}w(y)$, a constant times $w(y)$. The success probability of a round is $c_t e^{-\sigma^2/(2t^2)}Z_\sigma > 0$, so the loop stops with probability 1, and the accepted $Y$ has mass $w(y)/Z_\sigma$. Line L6 returns $v + Y$. $\square$

**Lemma 5 (theta sums).** For every real $c$, $\sum_{y \in \mathbb Z} w(y - c) \le \sum_{y \in \mathbb Z} w(y)$, with equality when $c$ is an integer.

*Proof.* The Fourier transform of $w$ is $\hat w(\xi) = \sqrt{2\pi}\sigma\,e^{-2\pi^2\sigma^2\xi^2}$. By the Poisson summation formula, which applies because $w$ and $\hat w$ decay faster than any power,
$$\sum_{y \in \mathbb Z} w(y - c) = \sqrt{2\pi}\sigma\sum_{k \in \mathbb Z}e^{-2\pi^2\sigma^2k^2}\cos(2\pi kc).$$
Every term is at most its value at $c = 0$, because $\cos(2\pi kc) \le 1$ and the weights are positive. For integer $c$ all cosines are 1. $\square$

**Lemma 6 (Renyi divergence).** Let $P = \mu + N_{\mathbb Z}(0, \sigma^2)$ and $Q = N_{\mathbb Z}(0, \sigma^2)$ for an integer $\mu$. Then $D_\alpha(P\|Q) \le \alpha\mu^2/(2\sigma^2)$ for every $\alpha > 1$, with equality when $\alpha\mu$ is an integer.

*Proof.* For each $y$, completing the square gives $\alpha(y - \mu)^2 + (1 - \alpha)y^2 = (y - \alpha\mu)^2 - \alpha(\alpha - 1)\mu^2$. Hence
$$\sum_y P(y)^{\alpha}Q(y)^{1-\alpha} = \frac{1}{Z_\sigma}\sum_y w(y - \mu)^{\alpha}w(y)^{1-\alpha} = e^{\alpha(\alpha - 1)\mu^2/(2\sigma^2)}\,\frac{\sum_y w(y - \alpha\mu)}{Z_\sigma}.$$
Take $\frac{1}{\alpha - 1}\ln$ of both sides. The ratio is at most 1 by Lemma 5, with equality when $\alpha\mu$ is an integer. $\square$

**Theorem.** DISCRETE-GAUSSIAN-MECHANISM is exact, and for a query $f$ with integer values and sensitivity $\Delta$ it is $\Delta^2/(2\sigma^2)$-zCDP. For neighbors with $|f(x) - f(x')| = \Delta$, its smallest $\delta$ at $\varepsilon \ge 0$ is
$$\delta(\varepsilon) = \Pr\left[Y > \frac{\varepsilon\sigma^2}{\Delta} - \frac{\Delta}{2}\right] - e^{\varepsilon}\Pr\left[Y > \frac{\varepsilon\sigma^2}{\Delta} + \frac{\Delta}{2}\right], \qquad Y \sim N_{\mathbb Z}(0, \sigma^2).$$

*Proof.* Exactness is Lemma 4. For neighbors $x, x'$, let $d = f(x) - f(x')$, an integer with $|d| \le \Delta$. The output laws are $f(x') + d + N_{\mathbb Z}(0, \sigma^2)$ and $f(x') + N_{\mathbb Z}(0, \sigma^2)$. A shift of both laws by $-f(x')$ does not change the divergence, so by Lemma 6, $D_\alpha(M(x)\|M(x')) \le \alpha d^2/(2\sigma^2) \le \alpha\Delta^2/(2\sigma^2)$ for all $\alpha > 1$. The other order has shift $-d$, and the same bound holds. This is the definition of $\Delta^2/(2\sigma^2)$-zCDP with $\xi = 0$.

For the $\delta$ curve, take the case $f(x') = f(x) + \Delta$ and shift so that $M(x)$ has law $p(y) = w(y)/Z_\sigma$ and $M(x')$ has law $q(y) = p(y - \Delta)$; the case $f(x') = f(x) - \Delta$ is the mirror image under $y \mapsto -y$. The smallest $\delta$ is the hockey-stick divergence $\sum_y (p(y) - e^{\varepsilon}q(y))_+$, reached at the set where the privacy loss $\ell(y) = \ln(p(y)/q(y))$ is above $\varepsilon$. Here
$$\ell(y) = \frac{(y - \Delta)^2 - y^2}{2\sigma^2} = \frac{\Delta^2 - 2\Delta y}{2\sigma^2},$$
so $\ell(y) > \varepsilon$ exactly when $y < a$ with $a = \Delta/2 - \varepsilon\sigma^2/\Delta$. Then
$$\delta(\varepsilon) = \Pr[Y < a] - e^{\varepsilon}\Pr[Y + \Delta < a] = \Pr[Y > -a] - e^{\varepsilon}\Pr[Y > \Delta - a],$$
by the symmetry of $Y$, and $-a = \varepsilon\sigma^2/\Delta - \Delta/2$ and $\Delta - a = \varepsilon\sigma^2/\Delta + \Delta/2$. Canonne, Kamath and Steinke (Theorem 7) also show that pairs with $|d| < \Delta$ do not need a larger $\delta$, so this curve is the tight guarantee of the mechanism whenever a pair with $|d| = \Delta$ exists. $\blacksquare$
