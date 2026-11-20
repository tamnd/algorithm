---
title: Massey's metric is a scaled log-likelihood of the sync word position, so the rule is maximum likelihood and minimizes the probability of a sync error for a uniform position
proves: [correctness]
status: full
---

The window holds $N$ real received symbols $y_0, \ldots, y_{N-1}$, read cyclically. A sync word $s_0, \ldots, s_{L-1} \in \{+1, -1\}$ starts at an unknown position $\mu \in \{0, \ldots, N - 1\}$, uniform. The other $N - L$ positions carry independent data $d_i \in \{+1, -1\}$, each value with probability $\frac12$. The channel is $y_i = \sqrt{E_s}\,d_i + n_i$, where $d_i$ is the sync or data symbol at position $i$, and the $n_i$ are independent $\mathcal{N}(0, N_0/2)$. Write $a = \sqrt{E_s}$. Lines L3 to L6 compute
$$M(\mu) = \sum_{i=0}^{L-1} s_i\,y_{\mu+i} - \frac{N_0}{2a}\sum_{i=0}^{L-1}\ln\cosh\frac{2a\,y_{\mu+i}}{N_0},$$
with indices mod $N$, and lines L1, L2 and L7 to L9 return the $\mu$ with the largest $M(\mu)$.

**Lemma 1 (one position).** For a position with a known symbol $s$, the density of $y$ is $\phi(y)\,e^{2asy/N_0}$, and for a data position it is $\phi(y)\cosh(2ay/N_0)$, where $\phi(y) = (\pi N_0)^{-1/2}e^{-(y^2 + a^2)/N_0}$.

*Proof.* The Gaussian density with mean $as$ and variance $N_0/2$ is $(\pi N_0)^{-1/2}e^{-(y - as)^2/N_0}$, and $(y - as)^2 = y^2 + a^2 - 2asy$ since $s^2 = 1$. For a data position, average the two cases $s = \pm1$ with weight $\frac12$: $\frac12(e^{2ay/N_0} + e^{-2ay/N_0}) = \cosh(2ay/N_0)$. $\square$

**Theorem 1 (log-likelihood).** For every $\mu$,
$$\ln p(y \mid \mu) = \frac{2a}{N_0}M(\mu) + C(y),$$
where $C(y)$ does not depend on $\mu$.

*Proof.* Given $\mu$, the positions are independent. Let $S_\mu$ be the set of the $L$ sync positions. By Lemma 1,
$$p(y \mid \mu) = \prod_{i=0}^{N-1}\phi(y_i)\cdot\prod_{i \notin S_\mu}\cosh\frac{2ay_i}{N_0}\cdot\prod_{i \in S_\mu}e^{2as_{i-\mu}y_i/N_0}.$$
Multiply and divide by $\prod_{i \in S_\mu}\cosh(2ay_i/N_0)$. Then the first two products become $\prod_{i}\phi(y_i)\cosh(2ay_i/N_0)$ over all $i$, which does not depend on $\mu$, and the rest is $\prod_{i \in S_\mu}e^{2as_{i-\mu}y_i/N_0}/\cosh(2ay_i/N_0)$. Its logarithm is $\frac{2a}{N_0}\sum_i s_i y_{\mu+i} - \sum_i\ln\cosh(2ay_{\mu+i}/N_0) = \frac{2a}{N_0}M(\mu)$. $\square$

**Corollary 1 (optimality).** Because $\frac{2a}{N_0} > 0$, the $\mu$ that maximizes $M$ maximizes the likelihood. With a uniform prior on $\mu$, the maximum likelihood rule is the maximum a posteriori rule, which minimizes the probability of a wrong $\mu$ among all rules that see $y$ (theorem: a MAP decision is optimal for the 0-1 loss).

**Theorem 2 (limits).** As $N_0 \to 0$ with $E_s$ fixed, $M(\mu) = \sum_i\bigl(s_i y_{\mu+i} - |y_{\mu+i}|\bigr) + \frac{LN_0}{2a}\ln 2 + o(1)$, uniformly for bounded $y$. For small $a\,|y_i|/N_0$, $M(\mu) = \sum_i s_i y_{\mu+i} - \frac{a}{N_0}\sum_i y_{\mu+i}^2$ plus terms of order $a^3 y_{\mu+i}^4/N_0^3$.

*Proof.* $\ln\cosh x = |x| - \ln 2 + \ln(1 + e^{-2|x|})$, and the last term goes to $0$ as $|x| \to \infty$. With $x = 2ay/N_0$, $\frac{N_0}{2a}\ln\cosh x = |y| - \frac{N_0}{2a}\ln 2 + \frac{N_0}{2a}\ln(1 + e^{-4a|y|/N_0})$; the last term is at most $\frac{N_0}{2a}\ln 2$ and goes to zero, and the constant does not depend on $\mu$. For small $x$, $\ln\cosh x = \frac{x^2}{2} - \frac{x^4}{12} + \ldots$, so $\frac{N_0}{2a}\ln\cosh\frac{2ay}{N_0} = \frac{a}{N_0}y^2 + O(a^3y^4/N_0^3)$. $\square$

The correction term penalizes positions where the received values are large in magnitude whatever their sign. Plain correlation lacks it, so a stretch of large data values that happens to agree with $s$ in sign can win. At high SNR the term becomes $\sum|y|$, so a window scores $\sum(s_iy_i - |y_i|) \le 0$, with zero only when every sign agrees with $s$. The tests check Theorem 1 against a direct sum of log densities to $10^{-9}$, Theorem 2 at $N_0 = 10^{-4}$, and the gain over correlation by simulation.
