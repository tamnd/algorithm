---
title: Tanh-sinh quadrature computes truncated trapezoidal sums of the transformed integrand, which converge to the integral
proves: [correctness]
status: full
---

Let $a < b$ be finite, $c = (a + b)/2$, $r = (b - a)/2$, and let $f$ be continuous on $(a, b)$ with $\int_a^b |f| < \infty$. Write $u(t) = \frac{\pi}{2}\sinh t$,

$$\varphi(t) = c + r \tanh u(t), \qquad g(t) = f(\varphi(t))\, \varphi'(t), \qquad \varphi'(t) = r\, \frac{\frac{\pi}{2}\cosh t}{\cosh^2 u(t)},$$

$h_k = 2^{-k}$, and $T$ for `t_max`. Lines refer to the pseudocode TANH-SINH.

**Lemma 1 (the change of variables).** $\varphi$ is an infinitely differentiable, strictly increasing bijection of $\mathbb{R}$ onto $(a, b)$, and $\int_a^b f(x)\,dx = \int_{-\infty}^{\infty} g(t)\,dt$, both integrals converging absolutely.

*Proof.* $\varphi' > 0$ everywhere, and $\varphi(t) \to b$ as $t \to \infty$ and $\to a$ as $t \to -\infty$, since $u(t) \to \pm\infty$ and $\tanh u \to \pm 1$. The substitution rule for a $C^1$ increasing bijection holds on every compact $[\alpha, \beta] \subset (a, b)$; letting $\alpha \downarrow a$ and $\beta \uparrow b$ and using monotone convergence on $|f|$ gives the claim. $\square$

**Lemma 2 (nodes and weights without cancellation).** For $t \ge 0$, with $e = e^{-2u(t)} \in (0, 1]$,

$$b - \varphi(t) = r\,\delta(t), \quad \delta(t) = 1 - \tanh u = \frac{2e}{1 + e}, \qquad \frac{\varphi'(t)}{r} = \frac{\pi}{2}\cosh t \cdot \frac{4e}{(1 + e)^2},$$

and $\varphi(-t) - a = r\,\delta(t)$, $\varphi'(-t) = \varphi'(t)$.

*Proof.* $\tanh u = \frac{1 - e}{1 + e}$ and $\cosh^{-2} u = \frac{4e}{(1 + e)^2}$ for $e = e^{-2u}$. The rest follows from $\varphi(-t) - c = -(\varphi(t) - c)$. $\square$

Line L11 evaluates exactly these expressions, and line L12 sets $x = b - r\delta$ for $t \ge 0$ and $x = a + r\delta$ for $t < 0$, so in exact arithmetic $x = \varphi(t)$ and TERM$(t) = g(t)$. In floating point the formulas involve only products, quotients, one sum $1 + e \in [1, 2]$ and library $\exp$, $\sinh$, $\cosh$, so $\delta$ and the weight have relative errors of a few units in the last place for every $t$, including where $\delta$ is far below the machine epsilon; no subtraction of nearly equal numbers occurs. When `with_distances` is set, the distances $x - a$ and $b - x$ are passed to $f$ as $r\delta$ and $(b - a) - r\delta$, both with small relative error.

**Lemma 3 (nesting).** After line L3, and after line L7 at level $k \ge 1$, the running sum is $S_k = \sum_{|j h_k| \le T} g(j h_k)$, the sum over all integers $j$ with $|j| \le \lfloor T / h_k \rfloor$. So line L8 returns the truncated trapezoidal sum

$$Q_k = h_k \sum_{|j| \le \lfloor T/h_k \rfloor} g(j h_k).$$

*Proof.* Induction on $k$. Line L3 is the case $k = 0$. For $k \ge 1$, an integer $j$ is either even, $j = 2 j'$, with $j h_k = j' h_{k-1}$ and $|j| \le T/h_k \iff |j'| \le T/h_{k-1}$, so these terms are exactly $S_{k-1}$; or odd, and line L7 adds every odd $j$ with $|j| \le \lfloor T / h_k \rfloor$. Each point is evaluated once. $\square$

**Theorem (convergence).** Suppose moreover that $g \in C^1(\mathbb{R})$ with $\int_{\mathbb{R}} |g'| < \infty$. Then for every $k$,

$$\Big| Q_k - \int_a^b f \Big| \le h_k \int_{\mathbb{R}} |g'| + \int_{|t| > T - h_k} |g| + h_k \int_{|t| > T - h_k} |g'| .$$

*Proof.* Let $J$ be an interval of length $h$ with left end point $s$. Then $\big|h\, g(s) - \int_J g\big| \le \int_J |g(s) - g(t)|\,dt \le h \int_J |g'|$, and so also $h |g(s)| \le \int_J |g| + h \int_J |g'|$. Take $J_j = [jh, (j+1)h]$ for each node $s = jh$; these intervals tile $\mathbb{R}$. Summing the first inequality over all $j \in \mathbb{Z}$ gives $|h \sum_{j \in \mathbb{Z}} g(jh) - \int_{\mathbb{R}} g| \le h \int_{\mathbb{R}} |g'|$. For $|jh| > T$ the interval $J_j$ lies in $\{|t| > T - h\}$, so summing the second inequality over those $j$ bounds the omitted terms by $\int_{|t|>T-h} |g| + h\int_{|t| > T-h} |g'|$. Combine with Lemma 1 and Lemma 3. $\square$

So as $k \to \infty$ with $T$ fixed, $Q_k$ tends to $\int_a^b f$ up to the truncation error $\int_{|t| > T} |g|$, and with $T \to \infty$ as well it converges. For an integrand with $|f(x)| \le C\,(x - a)^{\alpha - 1}(b - x)^{\beta - 1}$, $\alpha, \beta > 0$, and a corresponding bound on $f'$, Lemma 2 gives $|g(t)| \le C' \cosh t\, \exp\!\big(-\min(\alpha, \beta)\, \pi \sinh |t|\big)$, so the hypotheses hold and the truncation error decays double exponentially in $T$.

**The fast rate (cited, not proved here).** The theorem gives only $O(h_k)$. If $f$ is analytic in a domain whose image under $\varphi^{-1}$ contains a strip $|\operatorname{Im} t| < d$ with $d \le \pi/2$ and $g$ is integrable along horizontal lines in it with bound $M$, the trapezoidal sum over all of $\mathbb{Z}$ has error at most $2M/(e^{2\pi d/h} - 1)$ (Trefethen and Weideman 2014, Theorem 5.1). Balancing this against the double exponential truncation error gives an error of order $\exp(-c N / \log N)$ with $N$ points (Takahasi and Mori 1974; Tanaka, Sugihara, Murota and Mori 2009).

**Orientation, empty and infinite intervals.** Line L1 returns 0 for $a = b$; for $b < a$ the implementation returns $-\mathrm{TANH\text{-}SINH}(f, b, a)$, which is correct since $\int_a^b = -\int_b^a$. For $[a, \infty)$, $x = a + u/(1 - u)$ is an increasing $C^\infty$ bijection of $[0, 1)$ onto $[a, \infty)$ with $dx = (1 - u)^{-2}\,du$, so $\int_a^\infty f = \int_0^1 f(a + \frac{u}{1-u})(1 - u)^{-2}\,du$, an integral of the kind covered above, with a possible singularity at $u = 1$; the implementation passes the accurate $1 - u$ from Lemma 2 and drops the part $x > a + 10^{150}$. $(-\infty, b]$ is symmetric and $(-\infty, \infty)$ is split at 0.

**Termination and cost.** The loop of line L5 runs at most $K$ = `max_level` times, and by Lemma 3 each point $j h_k$ is evaluated at most once, so a run that ends at level $K$ evaluates $f$ at most $2 \lfloor T 2^K \rfloor + 1 \le 2 T 2^K + 1$ times. The returned estimate $|Q_K - Q_{K-1}|$ is a heuristic, not a bound. $\blacksquare$
