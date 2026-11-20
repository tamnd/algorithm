---
title: The VV estimate maximizes sum rho^p cos(M(psi - phi - phase0)), is exact modulo 2 pi/M without noise, is unbiased modulo 2 pi/M in circular noise, and reaches the MCRB at high SNR
proves: [correctness]
status: full
---

The input is $r_k = a_k e^{j\theta} + w_k$, $k = 0, \ldots, N - 1$, where $a_k = e^{j(2\pi i_k/M + \varphi_0)}$ with $i_k$ independent and uniform on $\{0, \ldots, M - 1\}$, the offset $\varphi_0$ is known, and $w_k \sim \mathcal{CN}(0, N_0)$ is white, $\mathrm{SNR} = 1/N_0$. Lines L2 to L4 form $S = \sum_k \rho_k^p e^{jM\psi_k}$, where $r_k = \rho_k e^{j\psi_k}$. Line L5 sets $\hat\theta = (\arg S - M\varphi_0)/M$, and line L6 reduces it to $[-\pi/M, \pi/M)$. Write $\equiv$ for equality modulo $2\pi/M$.

**Lemma 1 (the data is removed).** For every data symbol, $M \arg a_k \equiv M\varphi_0 \pmod{2\pi}$.

*Proof.* $M(2\pi i_k/M + \varphi_0) = 2\pi i_k + M\varphi_0$. $\square$

**Theorem 1 (what the estimate maximizes).** For every $\phi$, let $J(\phi) = \sum_k \rho_k^p \cos(M(\psi_k - \phi - \varphi_0))$. Then $\hat\theta$ is a maximizer of $J$, and the set of maximizers is $\hat\theta + \frac{2\pi}{M}\mathbb{Z}$ when $S \ne 0$.

*Proof.* $J(\phi) = \operatorname{Re}\bigl(S e^{-jM(\phi + \varphi_0)}\bigr) = |S| \cos\bigl(\arg S - M(\phi + \varphi_0)\bigr)$. This is at most $|S|$, with equality exactly when $M(\phi + \varphi_0) \equiv \arg S \pmod{2\pi}$, that is $\phi \equiv (\arg S - M\varphi_0)/M$. Line L6 picks the representative in $[-\pi/M, \pi/M)$. $\square$

For $p = M$, $J(\phi) = \operatorname{Re}\bigl(e^{-jM(\phi+\varphi_0)} \sum_k r_k^M\bigr)$, which is the first nonconstant term of the low-SNR expansion of the non-data-aided log-likelihood of M-PSK. Other $p$ trade that low-SNR form against a smaller noise enhancement at moderate SNR.

**Theorem 2 (exact without noise).** If $w_k = 0$ for all $k$ and $N \ge 1$, then $\hat\theta \equiv \theta$, for every $p$.

*Proof.* $\rho_k = 1$ and $\psi_k \equiv \arg a_k + \theta \pmod{2\pi}$, so by Lemma 1 $e^{jM\psi_k} = e^{j(M\varphi_0 + M\theta)}$ for every $k$ and $S = N e^{jM(\theta + \varphi_0)} \neq 0$. Line L5 gives $\hat\theta \equiv \theta$. $\square$

So the estimate can only find $\theta$ modulo $2\pi/M$; this is the phase ambiguity of M-PSK, and an unwrapping step or differential encoding resolves it.

**Theorem 3 (unbiased modulo $2\pi/M$).** Let $\epsilon$ be the representative of $\hat\theta - \theta$ in $[-\pi/M, \pi/M)$. Then $\epsilon$ has a distribution symmetric about $0$, so $E\epsilon = 0$.

*Proof.* Let $u_k = a_k e^{-j\varphi_0}$, an $M$th root of unity, and $v_k = w_k e^{-j(\theta + \varphi_0)}$, again $\mathcal{CN}(0, N_0)$ and independent of the data. Then $r_k = (u_k + v_k) e^{j(\theta + \varphi_0)}$, and $S e^{-jM(\theta + \varphi_0)} = \sum_k |u_k + v_k|^p e^{jM\arg(u_k + v_k)} =: S'$, so $M\epsilon \equiv \arg S' \pmod{2\pi}$. Complex conjugation maps the set of $M$th roots of unity onto itself and preserves the uniform law, and it preserves the law of circular Gaussian noise. So $(\bar u_k, \bar v_k)$ has the same joint law as $(u_k, v_k)$, and $\overline{S'}$ has the same law as $S'$. Hence $\arg S'$ and $-\arg S'$ have the same law on $(-\pi, \pi]$, up to the null event $\arg S' = \pi$, and so do $\epsilon$ and $-\epsilon$. $\square$

**Theorem 4 (high-SNR variance).** As $N_0 \to 0$, $\operatorname{var}\epsilon = \frac{N_0}{2N}(1 + o(1)) = \frac{1}{2N\,\mathrm{SNR}}(1 + o(1))$, the modified Cramer-Rao bound, for every fixed $p$.

*Proof.* Write $u_k + v_k = u_k(1 + \bar u_k v_k)$, and $\bar u_k v_k = x_k + j y_k$ with $x_k, y_k$ independent $\mathcal{N}(0, N_0/2)$. To first order in the noise, $\arg(u_k + v_k) = \arg u_k + y_k + O(N_0)$ and $|u_k + v_k|^p = 1 + O(\sqrt{N_0})$. With $e^{jM\arg u_k} = 1$, $S' = \sum_k (1 + O(\sqrt{N_0}))(1 + jMy_k + O(N_0)) = N + jM\sum_k y_k + O(N_0)$ in mean square, so $M\epsilon = \arg S' = \frac{M}{N}\sum_k y_k + O(N_0)$ and $\epsilon = \frac1N \sum_k y_k + O(N_0)$. Its variance is $\frac{1}{N^2} \cdot N \cdot \frac{N_0}{2} + o(N_0)$. Outliers, where the noise moves $\arg S'$ by more than $\pi/2$, need a noise sample of size of order $1$; for fixed $N$ their probability is bounded by a Gaussian tail $e^{-c/N_0}$, which is $o(N_0)$, and $|\epsilon| \le \pi/M$ is bounded, so they do not change the leading term. $\square$

This is a closed form under assumptions (high SNR). At moderate SNR the noise terms of higher order, enhanced by the power $M$, raise the variance above the bound; the tests measure this, for QPSK with $N = 32$, at 5 and 10 dB.

**Complexity.** Lines L2 to L4 run $N$ times with $O(1)$ work each; lines L1, L5 and L6 are $O(1)$. The total is $O(N)$ time and $O(1)$ extra space.
