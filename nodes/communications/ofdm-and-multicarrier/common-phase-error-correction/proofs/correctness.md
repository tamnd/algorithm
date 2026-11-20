---
title: "Phase noise scales every subcarrier by the same factor I_0, the pilot correlation points in its direction on average, and a constant phase is removed exactly"
proves: [correctness]
status: full
---

Notation. $N$ subcarriers, $j$ the imaginary unit, the unitary DFT pair $x = F^H X$ with $F[k, n] = e^{-j 2\pi k n / N} / \sqrt N$, and $H[k] = \sum_l h_l e^{-j 2\pi l k / N}$. The cyclic prefix covers the channel, so inside the DFT window the channel output is the circular convolution $c$ of the taps with the symbol $x$. The oscillator adds the phase $\varphi[n]$ to sample $n$, and the noise $w[n]$ is white $\mathcal{CN}(0, N_0)$, so the window holds $e^{j\varphi[n]} c[n] + w[n]$. Let

$$I_q = \frac1N \sum_{n=0}^{N-1} e^{j\varphi[n]} e^{-j 2\pi q n / N}.$$

The pilots are the subcarriers $p \in \mathcal P$ with known values $X_p$, and the receiver knows $H$. Lines L1 and L2 compute $C = \sum_{p \in \mathcal P} Y[p] \left( H[p] X_p \right)^*$ and $\hat\varphi = \angle C$.

**Lemma 1 (the received subcarriers).** $Y[k] = I_0 H[k] X[k] + \sum_{m \ne k} I_{k - m} H[m] X[m] + W[k]$, with indices modulo $N$ and $W = F w$ white $\mathcal{CN}(0, N_0)$.

*Proof.* By the convolution theorem for the unitary pair, $c[n] = \frac{1}{\sqrt N} \sum_m H[m] X[m] e^{j 2\pi m n / N}$. Then

$$Y[k] = \frac{1}{\sqrt N} \sum_n e^{j\varphi[n]} c[n] e^{-j 2\pi k n / N} + W[k] = \sum_m H[m] X[m] \cdot \frac1N \sum_n e^{j\varphi[n]} e^{-j 2\pi (k - m) n / N} + W[k],$$

and the inner sum is $I_{k - m}$. A unitary map keeps white Gaussian noise white with the same variance. $\square$

The factor $I_0$ is the same for every subcarrier. Its angle is the common phase error, and its size is at most 1 by the triangle inequality. The sum over $m \ne k$ is inter-carrier interference.

**Lemma 2 (Parseval for the factors).** $\sum_{q=0}^{N-1} |I_q|^2 = 1$.

*Proof.* $(I_0, \ldots, I_{N-1})$ is $\frac{1}{\sqrt N} F$ applied to the vector $e^{j\varphi[n]}$, whose squared norm is $N$. A unitary map keeps the norm, so the squared norm of $I$ is $N / N = 1$. $\square$

So with $|H[m]| = 1$ and independent unit-energy data, the interference on a subcarrier has the power $\sum_{q \ne 0} |I_q|^2 = 1 - |I_0|^2$, which a common rotation cannot remove.

**Theorem 1 (a constant phase is removed exactly).** If $\varphi[n] = \theta$ for all $n$, $\theta \in (-\pi, \pi]$, there is no noise, and $H[p] X_p \ne 0$ for some pilot, then $\hat\varphi = \theta$, and line L3 returns $X[k]$ on every subcarrier with $H[k] \ne 0$.

*Proof.* $I_0 = e^{j\theta}$ and $I_q = \frac{e^{j\theta}}{N} \sum_n e^{-j 2\pi q n / N} = 0$ for $q \ne 0$. By Lemma 1, $Y[k] = e^{j\theta} H[k] X[k]$, so $C = e^{j\theta} \sum_p |H[p] X_p|^2$ with a positive sum, and $\angle C = \theta$. Line L3 computes $Y[k] e^{-j\theta} / H[k] = X[k]$. $\square$

**Theorem 2 (the pilot sum points at I_0 on average).** Fix $\varphi$. Let all subcarrier values, the pilot values included, be independent with zero mean, and let $|X[k]| = 1$. Then

$$E[C] = I_0 \sum_{p \in \mathcal P} |H[p]|^2,$$

so $\angle E[C] = \angle I_0$.

*Proof.* By Lemma 1, $C = \sum_p \left( I_0 |H[p]|^2 |X_p|^2 + \sum_{m \ne p} I_{p - m} H[m] H[p]^* X[m] X_p^* + W[p] H[p]^* X_p^* \right)$. The first term is $I_0 |H[p]|^2$. In the second, $E[X[m] X_p^*] = E[X[m]]\, E[X_p]^* = 0$ for $m \ne p$ by independence and zero mean. In the third, $W$ has zero mean and is independent of the data. $\square$

Theorem 2 says that the estimate is aimed at the right angle; the spread around it comes from the interference and the noise on the pilots, and it shrinks as the number of pilots grows, because $C$ adds the pilots coherently and the disturbances incoherently. This is a heuristic statement about the spread; the tests measure its effect on symbol errors.

**Theorem 3 (the power left in I_0 for Wiener phase noise).** Let $\varphi[n + 1] - \varphi[n]$ be independent $\mathcal N(0, \sigma^2)$, the Wiener model of an oscillator. Then

$$E|I_0|^2 = \frac{1}{N^2} \sum_{n=0}^{N-1} \sum_{m=0}^{N-1} e^{-\sigma^2 |n - m| / 2} = 1 - \frac{\sigma^2 (N^2 - 1)}{6N} + O\left( (\sigma^2 N)^2 \right).$$

*Proof.* $|I_0|^2 = \frac{1}{N^2} \sum_{n, m} e^{j(\varphi[n] - \varphi[m])}$, and $\varphi[n] - \varphi[m]$ is a sum of $|n - m|$ independent steps, so it is $\mathcal N(0, \sigma^2 |n - m|)$, whose characteristic function at 1 is $e^{-\sigma^2 |n - m| / 2}$. For the expansion, $e^{-x} = 1 - x + O(x^2)$ and $\sum_{n, m} |n - m| = (N^3 - N)/3$, so the sum is $1 - \frac{\sigma^2}{2N^2} \cdot \frac{N^3 - N}{3} + O((\sigma^2 N)^2)$. $\square$

For $N = 64$ and $\sigma^2 = 0.002$, the closed form is close to $1 - \sigma^2 N / 6 = 0.979$, so about 2 percent of the power becomes interference that line L3 cannot remove, and the rest is the common rotation that it does remove.
