---
title: Correctness of cyclostationary feature detection
proves: [correctness]
status: full
---

We prove that the statistic does not depend on the noise power, that under white circular Gaussian noise it tends in law to a unit exponential, so the threshold $-\ln P_{fa}$ gives false alarm rate $P_{fa}$ in the limit, that a signal with a nonzero cyclic autocorrelation is detected with probability tending to $1$, and that the DFT scan computes the same estimates at the grid frequencies.

**Setting.** For samples $y[0..N-1]$, a cycle frequency $\alpha$ and a lag $0 \le \tau < N$, let $M = N - \tau$ and
$$u_n = y[n + \tau]\, \tilde y[n]\, e^{-j2\pi\alpha n}, \qquad R = \frac1M \sum_{n < M} u_n, \qquad P = \frac1N \sum_{n < N} |y[n]|^2,$$
where $\tilde y[n] = y[n]$ in the conjugate form and $\tilde y[n] = y[n]^*$ in the non-conjugate form, which requires $\tau \ge 1$. The statistic is $T = M|R|^2/(cP^2)$, with $c = 2$ for the conjugate form at $\tau = 0$ and $c = 1$ otherwise, and $T = 0$ if $P = 0$.

## Lemma 1 (scale invariance)

For every complex $a \ne 0$, the samples $a\,y[n]$ give the same $T$.

*Proof.* Each $u_n$ is multiplied by $a^2$ (conjugate form) or by $|a|^2$ (non-conjugate form), so $|R|^2$ is multiplied by $|a|^4$. $P$ is multiplied by $|a|^2$, so $P^2$ is multiplied by $|a|^4$, and the ratio does not change. $\square$

So under $H_0$ the law of $T$ is the same for every noise power $\sigma^2$, and we may take $\sigma^2 = 1$.

## Lemma 2 (moments under noise)

Let the $y[n]$ be independent $\mathcal{CN}(0, 1)$. Then for all $n \ne m$ in $[0, M)$: $\mathbb E[u_n] = 0$, $\mathbb E[u_n u_m^*] = 0$, $\mathbb E[u_n u_m] = 0$, $\mathbb E[u_n^2] = 0$ and $\mathbb E|u_n|^2 = c$.

*Proof.* A circular variable $w \sim \mathcal{CN}(0, 1)$ has $\mathbb E[w] = 0$, $\mathbb E[w^2] = 0$, $\mathbb E|w|^2 = 1$, $\mathbb E[w^4] = \mathbb E[w^3 w^*] = 0$ and $\mathbb E|w|^4 = 2$. In general, a moment $\mathbb E[w^p (w^*)^q]$ is zero unless $p = q$, because $w$ and $e^{j\theta}w$ have the same law, which multiplies the moment by $e^{j(p - q)\theta}$ for every $\theta$.

Each expectation is a product, over the distinct indices involved, of such moments of independent variables. It is zero unless, at each index, the number of unconjugated factors equals the number of conjugated ones.

- $\mathbb E[u_n]$: for $\tau \ge 1$, the factor $y[n + \tau]$ is alone at its index. For $\tau = 0$ (conjugate form), the moment is $\mathbb E[y[n]^2] = 0$.
- $\mathbb E[u_n u_m^*]$ with $n \ne m$: the index $n + \tau$ carries an unconjugated factor from $u_n$. To balance it, $u_m^*$ must supply a conjugated factor at $n + \tau$. Its conjugated factors sit at $m + \tau \ne n + \tau$, and, in the conjugate form, at $m$. In the non-conjugate form, the factor of $u_m^*$ at $m$ is unconjugated. So balance needs the conjugate form and $m = n + \tau$ with $\tau \ge 1$. Then the index $n$ carries the unconjugated $y[n]$ from $u_n$, and $u_m^*$ has conjugated factors only at $m$ and $m + \tau$, both above $n$. So nothing balances it. For $\tau = 0$, $u_n$ has $y[n]^2$ and $u_m^*$ has no factor at $n$.
- $\mathbb E[u_n u_m]$ and $\mathbb E[u_n^2]$: in the conjugate form, all factors are unconjugated, so the moment is zero. In the non-conjugate form, $u_n u_m$ has unconjugated factors at $n + \tau$ and $m + \tau$, and conjugated ones at $n$ and $m$. Balance needs $\{n + \tau, m + \tau\} = \{n, m\}$ as multisets, which is impossible for $\tau \ge 1$ since the largest index $\max(n, m) + \tau$ appears only on the left.
- $\mathbb E|u_n|^2$: for $\tau \ge 1$, it is $\mathbb E|y[n + \tau]|^2\, \mathbb E|y[n]|^2 = 1$. For $\tau = 0$ (conjugate form), it is $\mathbb E|y[n]|^4 = 2$. $\square$

## Theorem 3 (false alarm rate)

Under $H_0$, as $N \to \infty$ with $\tau$ and $\alpha$ fixed, $T$ tends in law to a unit exponential, and $\Pr[T > -\ln P_{fa}] \to P_{fa}$.

*Proof.* By Lemma 1, take $\sigma^2 = 1$. Write $u_n = a_n + j b_n$. By Lemma 2, $\mathbb E[u_n u_m^*] = c\,\delta_{nm}$ and $\mathbb E[u_n u_m] = 0$ for all $n, m$, which gives $\mathbb E[a_n a_m] = \mathbb E[b_n b_m] = \frac c2 \delta_{nm}$ and $\mathbb E[a_n b_m] = 0$. The sequence $(a_n, b_n)$ is $\tau$-dependent, since $u_n$ is a function of $y[n]$ and $y[n + \tau]$ only, and its terms are bounded in fourth moment uniformly in $n$. The rotation $e^{-j2\pi\alpha n}$ changes neither the moments of Lemma 2 nor the dependence. By the central limit theorem for $m$-dependent sequences, applied to every fixed real combination $s\,a_n + t\,b_n$ and then by the Cramér-Wold device, the vector $\frac{1}{\sqrt{M c/2}}\big(\sum a_n, \sum b_n\big)$ tends to two independent standard normals. Hence $S = \sum_n u_n / \sqrt{Mc}$ tends to $\mathcal{CN}(0, 1)$, and $|S|^2$ tends to a unit exponential (Lemma 1 of the energy detector proof: $|w|^2$ for $w \sim \mathcal{CN}(0, 1)$ is a unit exponential).

Now $T = M|R|^2/(cP^2) = |S|^2 / P^2$. By the law of large numbers, $P \to 1$ almost surely, so by Slutsky's theorem $T$ tends in law to the same unit exponential. The exponential law is continuous, so $\Pr[T > \lambda] \to e^{-\lambda}$ for every $\lambda$, and $e^{-\lambda} = P_{fa}$ for $\lambda = -\ln P_{fa}$. $\square$

## Theorem 4 (detection)

Suppose that under $H_1$ the estimate converges, $R \to \rho \ne 0$, and $P \to \bar P > 0$, both in probability. Then $T \to \infty$ in probability, and the detection probability at any fixed threshold tends to $1$.

*Proof.* $T / M = |R|^2/(cP^2) \to |\rho|^2/(c\bar P^2) > 0$ in probability, and $M \to \infty$. $\square$

For BPSK, $y[n] = s[n] + w[n]$ with $s[n] = \sqrt S\, a[n] e^{j(2\pi f_c n + \phi)}$, $a[n] = \pm 1$, and $w$ independent $\mathcal{CN}(0, \sigma^2)$. Take the conjugate form, $\tau = 0$ and $\alpha = 2 f_c$. Then $y[n]^2 = s[n]^2 + 2 s[n] w[n] + w[n]^2$ and $s[n]^2 e^{-j 2\pi\alpha n} = S e^{j2\phi}$ for every $n$. The other two terms have mean zero and are independent over $n$ given $a$, with bounded variance, so their average tends to zero, and $R \to S e^{j2\phi}$, with $|\rho| = S > 0$. Also $P \to S + \sigma^2$. Theorem 4 applies.

**The large-$N$ detection probability used on the page.** Given $a$ and $\phi$, the sum $\sum_n y[n]^2 e^{-j2\pi\alpha n}$ is $N S e^{j2\phi}$ plus the sum of $2 s[n] w[n] + w[n]^2$, rotated. Those terms are circular, with variance $4 S\sigma^2 + 2\sigma^4$ each, and uncorrelated with each other, since $\mathbb E[s w \cdot (w^2)^*] = s\,\mathbb E[w (w^*)^2] = 0$. Approximating the noise sum by a complex Gaussian and $P$ by $S + \sigma^2$, with $\gamma = S/\sigma^2$,
$$T \approx \frac{(4\gamma + 2)}{2(1 + \gamma)^2}\, |Z|^2, \qquad Z \sim \mathcal{CN}\Big(\sqrt{\tfrac{N\gamma^2}{4\gamma + 2}}, 1\Big).$$
For $Z \sim \mathcal{CN}(\sqrt\mu, 1)$, $\Pr[|Z|^2 > x] = \sum_{j \ge 0} e^{-\mu}\frac{\mu^j}{j!}\Pr[\mathrm{Gamma}(j + 1, 1) > x]$ (Theorem 3 of the energy detector proof with $N = 1$). This is an approximation, not an exact law. The test file checks it against a simulation at $N = 64$ and $-5$ dB within a Wilson interval.

## Proposition 5 (the scan)

Let $v_n = y[n + \tau]\,\tilde y[n]$ for $n < M$ and $V = \mathrm{DFT}(v)$, so $V[k] = \sum_n v_n e^{-j2\pi k n/M}$. Then $V[k]/M$ is the estimate $R$ at $\alpha = k/M$, for every $k$.

*Proof.* Substitute $\alpha = k/M$ in the definition of $R$. $\square$

Under $H_0$, the $V[k]$ are uncorrelated with equal variance, since $\mathbb E[V[k] V[l]^*] = \sum_{n, m} \mathbb E[v_n v_m^*] e^{-j2\pi(kn - lm)/M} = cM\sigma^4 \delta_{kl}$ by Lemma 2 and the orthogonality of the DFT. If the $M$ statistics were independent unit exponentials, the largest would exceed $\lambda$ with probability $1 - (1 - e^{-\lambda})^M$, and setting this to $P_{fa}$ gives the scan threshold of the page. The bins are uncorrelated but only approximately independent and exponential at finite $M$, so this threshold is an approximation; the test file checks that the rate under noise does not exceed $P_{fa}$ for $M = 64$.

## The code

The code updates the rotation by multiplying by $e^{-j2\pi\alpha}$ at each step, which equals $e^{-j2\pi\alpha n}$ up to rounding that grows like $n$ times the unit roundoff. The test file checks the direct sum against the DFT at all grid frequencies to $10^{-12}$.
