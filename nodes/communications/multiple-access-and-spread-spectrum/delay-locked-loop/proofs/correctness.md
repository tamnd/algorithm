---
title: The early-late discriminator is linear near lock, and the loop drives the delay error to zero
proves: [correctness]
status: full
---

**Model.** Time is in chips. The code is an m-sequence $c_0, \ldots, c_{N-1} \in \{+1, -1\}$ with periodic autocorrelation $\rho(0) = 1$ and $\rho(i) = -1/N$ for $i \not\equiv 0 \pmod N$, and $c(t) = c_{\lfloor t \rfloor \bmod N}$ is the code waveform with rectangular chips. One block is one code period of the received signal $A e^{j\phi} c(t - \tau)$. The correlator with a replica delayed by $d$ returns
$$\mathrm{corr}(d) = \frac{1}{N} \int_0^N A e^{j\phi}\, c(t - \tau)\, c(t - d)\, dt.$$
The implementation replaces the integral by the mean over $M$ samples at $t_k = k N / M$, a Riemann sum of the same integral. Write $\varepsilon = \tau - \hat\tau$ for the delay error, $a = (N + 1)/N$, and let $0 < \delta < N/(N + 1)$ be the early-late offset. The loop computes $E = \mathrm{corr}(\hat\tau - \delta)$ and $L = \mathrm{corr}(\hat\tau + \delta)$ (L3), the discriminator $D = (|L| - |E|)/(|L| + |E|)$ (L4), and the update $\hat\tau \leftarrow \hat\tau + g D / k_d$ (L5), with $k_d = a/(1 - a\delta)$.

**Lemma 1 (autocorrelation of the waveform).** $\mathrm{corr}(d) = A e^{j\phi} R(\tau - d)$, where $R$ is even, has period $N$, and on $[0, N/2]$ equals
$$R(x) = 1 - a x \quad (0 \le x \le 1), \qquad R(x) = -1/N \quad (1 \le x \le N/2).$$

*Proof.* Substitute $s = t - \tau$; by periodicity, $\mathrm{corr}(d) = A e^{j\phi} \frac{1}{N} \int_0^N c(s)\, c(s - x)\, ds$ with $x = \tau - d$. Write $x = i + f$ with an integer $i$ and $0 \le f < 1$. On the chip $[n, n + 1)$, $c(s) = c_n$, and $c(s - x)$ equals $c_{n - i}$ on a part of length $1 - f$ and $c_{n - i - 1}$ on a part of length $f$. Summing over the chips,
$$\frac{1}{N}\int_0^N c(s) c(s - x)\, ds = (1 - f)\, \rho(i) + f\, \rho(i + 1).$$
For $0 \le x < 1$ this is $(1 - x) \cdot 1 + x \cdot (-1/N) = 1 - a x$, and at $x = 1$ it is $-1/N = 1 - a$. For $1 \le x \le N/2$ both $\rho$ values are $-1/N$. The function is even because the integral is symmetric under exchanging the two factors. $\square$

So $|E| = |A|\, |R(\varepsilon + \delta)|$ and $|L| = |A|\, |R(\varepsilon - \delta)|$, and $D$ depends only on $\varepsilon$; call it $D(\varepsilon)$, the S-curve. The carrier phase $\phi$ and the amplitude $A$ cancel.

**Lemma 2 (linear region).** If $|\varepsilon| \le \ell = \min(\delta,\ N/(N + 1) - \delta)$, then $D(\varepsilon) = k_d\, \varepsilon$.

*Proof.* Since $|\varepsilon| \le \delta$, the two lags are $|\varepsilon - \delta| = \delta - \varepsilon$ and $|\varepsilon + \delta| = \delta + \varepsilon$, and both are at most $|\varepsilon| + \delta \le N/(N + 1) = 1/a$. On $[0, 1/a]$, $R(x) = 1 - a x \ge 0$, so the absolute values can be dropped:
$$|L| - |E| = (1 - a(\delta - \varepsilon)) - (1 - a(\delta + \varepsilon)) = 2 a \varepsilon, \qquad |L| + |E| = 2(1 - a\delta).$$
Their ratio is $a\varepsilon/(1 - a\delta) = k_d \varepsilon$. $\square$

**Lemma 3 (sign of the S-curve).** If $0 < |\varepsilon| < \delta + (N - 1)/(N + 1)$ and $|\varepsilon| + \delta \le N/2$, then $D(\varepsilon)$ is nonzero and has the sign of $\varepsilon$.

*Proof.* $R$ is even, so $D(-\varepsilon) = -D(\varepsilon)$, and it is enough to take $\varepsilon > 0$. Let $x_L = |\varepsilon - \delta|$ and $x_E = \varepsilon + \delta$; then $x_L < x_E \le N/2$. We show $|R(x_L)| > |R(x_E)|$, which gives $|L| > |E|$ and $D > 0$. By Lemma 1, $|R(x)| = 1 - a x$ on $[0, 1/a]$, $|R(x)| = a x - 1 \le 1/N$ on $[1/a, 1]$, and $|R(x)| = 1/N$ on $[1, N/2]$. Also, $|R(x)| > 1/N$ exactly when $x < (N - 1)/(N + 1)$.

- If $x_E \le 1/a$: $|R|$ is strictly decreasing on $[0, x_E]$, and $x_L < x_E$.
- If $x_E > 1/a$ and $\varepsilon \ge \delta$: then $|R(x_E)| \le 1/N$, and the hypothesis gives $x_L = \varepsilon - \delta < (N - 1)/(N + 1)$, so $|R(x_L)| > 1/N$.
- If $1/a < x_E \le 1$ and $\varepsilon < \delta$: then $x_L = \delta - \varepsilon < 1/a$ and $x_L + x_E = 2\delta$, so $|R(x_L)| - |R(x_E)| = 2 - a(x_L + x_E) = 2(1 - a\delta) > 0$.
- If $x_E > 1$ and $\varepsilon < \delta$: then $\varepsilon > 1 - \delta$, so $x_L = \delta - \varepsilon < 2\delta - 1 < 2N/(N + 1) - 1 = (N - 1)/(N + 1)$, and $|R(x_L)| > 1/N = |R(x_E)|$. $\square$

So the discriminator always pushes the estimate toward the true delay inside a pull-in range of about $1 + \delta$ chips. Outside it, both correlators see the floor $1/N$ and $D = 0$: the loop has lost lock.

**Theorem 1 (convergence without noise).** Let the delay $\tau$ be constant, $0 < g < 2$, and $|\varepsilon_0| \le \ell$. Then the error after $k$ blocks is $\varepsilon_k = (1 - g)^k \varepsilon_0$, which tends to $0$.

*Proof.* By L5, $\varepsilon_{k+1} = \tau - \hat\tau_{k+1} = \varepsilon_k - g D(\varepsilon_k)/k_d$. If $|\varepsilon_k| \le \ell$, Lemma 2 gives $\varepsilon_{k+1} = (1 - g)\varepsilon_k$, and $|1 - g| < 1$ keeps $|\varepsilon_{k+1}| \le \ell$. Induction on $k$ gives the formula, and $(1 - g)^k \to 0$. $\square$

**Theorem 2 (jitter in the linear model).** Suppose that near lock the discriminator output is $D/k_d = \varepsilon_k + v_k$, where the $v_k$ are independent with mean $0$ and variance $\sigma_v^2$, one per block. Then for $0 < g < 2$ the variance of $\varepsilon_k$ tends to
$$\sigma_\varepsilon^2 = \frac{g\, \sigma_v^2}{2 - g}.$$

*Proof.* The update gives $\varepsilon_{k+1} = (1 - g)\varepsilon_k - g v_k$. Since $v_k$ is independent of $\varepsilon_k$, which depends only on $v_0, \ldots, v_{k-1}$ and the start, the variances satisfy $s_{k+1} = (1 - g)^2 s_k + g^2 \sigma_v^2$. With $(1 - g)^2 < 1$, $s_k$ tends to the fixed point $g^2\sigma_v^2 / (1 - (1 - g)^2) = g^2 \sigma_v^2 / (g(2 - g))$, which is the stated value. $\square$

**Theorem 3 (lag under a constant drift).** If $\tau_k = \tau_0 + k v$ and the loop stays in the linear region, the error before the update tends to $v/g$.

*Proof.* With $e_k = \tau_k - \hat\tau_k$, L5 gives $\hat\tau_{k+1} = \hat\tau_k + g e_k$, so $e_{k+1} = \tau_k + v - \hat\tau_k - g e_k = (1 - g) e_k + v$. The fixed point is $v/g$, and the difference $e_k - v/g$ is multiplied by $1 - g$ at each step. $\square$

**Cost.** Each block needs two correlations of $M$ samples (L3) and $O(1)$ further operations (L4 and L5), so $B$ blocks cost $\Theta(B M)$ operations, with $\Theta(1)$ extra space beyond the replicas.
