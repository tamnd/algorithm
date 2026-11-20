---
title: "The van de Beek statistic is the log-likelihood ratio of the Gaussian model, and it finds the exact timing and offset without noise"
proves: [correctness]
status: full
---

Notation. $N$ is the DFT size, $N_{cp}$ the prefix length, and $j$ the imaginary unit. The receiver observes a window $r(0), \ldots, r(M - 1)$ with $M \ge 2N + N_{cp}$, and a prefix starts at the unknown index $\theta$, so for $k \in I = \{\theta, \ldots, \theta + N_{cp} - 1\}$ the sent sample $s(k + N)$ equals $s(k)$. The channel adds white noise only, and the carrier offset is $\varepsilon$ subcarrier spacings:

$$r(k) = s(k)\, e^{j 2\pi \varepsilon k / N} + n(k).$$

Lines L1 to L3 compute, for each candidate $\theta$,

$$\gamma(\theta) = \sum_{k = \theta}^{\theta + N_{cp} - 1} r(k)\, r^*(k + N), \qquad \Phi(\theta) = \frac12 \sum_{k = \theta}^{\theta + N_{cp} - 1} \left( |r(k)|^2 + |r(k + N)|^2 \right).$$

**Lemma 1 (running sums).** If $\gamma(0)$ and $\Phi(0)$ are the direct sums, the updates of lines L2 and L3 give the sums above for every $\theta \ge 1$.

*Proof.* Going from $\theta - 1$ to $\theta$, the sum loses the term $k = \theta - 1$ and gains the term $k = \theta - 1 + N_{cp}$. Line L2 adds $r(b)\, r^*(b + N)$ with $b = \theta - 1 + N_{cp}$ and subtracts $r(a)\, r^*(a + N)$ with $a = \theta - 1$; line L3 does the same for the energies. $\square$

**The model.** As in the paper of van de Beek, Sandell and Börjesson, model the sent samples as independent zero-mean circular complex Gaussian with variance $\sigma_s^2$, apart from the prefix copies, and the noise as independent $\mathcal{CN}(0, \sigma_n^2)$. Let $\sigma^2 = \sigma_s^2 + \sigma_n^2$ and $\rho = \sigma_s^2 / \sigma^2 = \text{SNR} / (\text{SNR} + 1)$. For a random OFDM symbol with many subcarriers, the time samples are close to Gaussian; for $\mathcal{CN}(0, 1)$ subcarrier values and the unitary inverse DFT they are exactly independent $\mathcal{CN}(0, 1)$.

**Lemma 2 (the pairs).** For $k \in I$, the pair $a = r(k)$, $b = r(k + N)$ has $E|a|^2 = E|b|^2 = \sigma^2$ and $E[a b^*] = \sigma^2 \rho\, e^{-j 2\pi \varepsilon}$. Every other pair of samples in the window is uncorrelated.

*Proof.* $E[a b^*] = E[s(k) s^*(k + N)]\, e^{j 2\pi \varepsilon k / N} e^{-j 2\pi \varepsilon (k + N) / N} = \sigma_s^2 e^{-j 2\pi\varepsilon}$, because $s(k + N) = s(k)$ and the noise terms are independent of each other and of the signal. Two samples that are not a prefix pair use independent sent samples and independent noise. $\square$

**Theorem 1 (the log-likelihood).** Under the model, the log-likelihood of $(\theta, \varepsilon)$ is

$$\log f(r \mid \theta, \varepsilon) = C + \frac{2\rho}{\sigma^2 (1 - \rho^2)} \left[ \operatorname{Re}\left( e^{j 2\pi\varepsilon} \gamma(\theta) \right) - \rho\, \Phi(\theta) \right],$$

with $C$ independent of $\theta$ and $\varepsilon$. Its maximum over $\varepsilon$ is at $\varepsilon = -\angle\gamma(\theta) / (2\pi)$ modulo 1, where the bracket equals $\Lambda(\theta) = |\gamma(\theta)| - \rho\, \Phi(\theta)$. So lines L4 to L6 return the joint maximum likelihood estimate.

*Proof.* By Lemma 2, the window splits into the $N_{cp}$ correlated pairs and independent single samples, so

$$f(r \mid \theta, \varepsilon) = \prod_{k} f(r(k)) \prod_{k \in I} \frac{f(r(k), r(k + N))}{f(r(k))\, f(r(k + N))},$$

and the first product does not depend on $(\theta, \varepsilon)$, because every sample has the same marginal $\mathcal{CN}(0, \sigma^2)$. For one pair, the covariance matrix is $\sigma^2 \begin{pmatrix} 1 & c \\ c^* & 1 \end{pmatrix}$ with $c = \rho e^{-j 2\pi\varepsilon}$, its inverse is $\frac{1}{\sigma^2 (1 - \rho^2)} \begin{pmatrix} 1 & -c \\ -c^* & 1 \end{pmatrix}$, and the quadratic form is $\frac{|a|^2 + |b|^2 - 2 \operatorname{Re}(c\, a^* b)}{\sigma^2 (1 - \rho^2)}$. With $\operatorname{Re}(c\, a^* b) = \rho \operatorname{Re}(e^{j 2\pi\varepsilon} a b^*)$, the log of the ratio is

$$-\log(1 - \rho^2) + \frac{2\rho \operatorname{Re}\left(e^{j 2\pi\varepsilon} a b^*\right) - \rho^2 \left(|a|^2 + |b|^2\right)}{\sigma^2 (1 - \rho^2)},$$

because $-\frac{|a|^2 + |b|^2}{\sigma^2 (1 - \rho^2)} + \frac{|a|^2 + |b|^2}{\sigma^2} = -\frac{\rho^2 (|a|^2 + |b|^2)}{\sigma^2 (1 - \rho^2)}$. Summing over $k \in I$ gives the stated form with $\sum a b^* = \gamma(\theta)$ and $\sum (|a|^2 + |b|^2) = 2\Phi(\theta)$. Finally $\operatorname{Re}(e^{j 2\pi\varepsilon} \gamma) = |\gamma| \cos(2\pi\varepsilon + \angle\gamma)$, which is largest, and equal to $|\gamma|$, when $2\pi\varepsilon = -\angle\gamma$ modulo $2\pi$. The factor in front of the bracket is positive, so maximizing the bracket over $\theta$ after the maximization over $\varepsilon$ is maximizing $\Lambda$. $\square$

**Theorem 2 (exact without noise).** Without noise, take $\rho = 1$. Let the window contain a full prefix start $\theta_0$, so $\theta_0 + N_{cp} - 1 + N \le M - 1$. Then $\Lambda(\theta) \le 0$ for every $\theta$, $\Lambda(\theta_0) = 0$, and $-\angle\gamma(\theta_0) / (2\pi) = \varepsilon$ modulo 1. If $|\varepsilon| < 1/2$, the wrap after line L6 returns $\varepsilon$ exactly. If no other $\theta$ ties, line L5 returns $\theta_0$.

*Proof.* For any $\theta$, the triangle inequality and $xy \le \frac12 (x^2 + y^2)$ give

$$|\gamma(\theta)| \le \sum_k |r(k)|\, |r(k + N)| \le \frac12 \sum_k \left( |r(k)|^2 + |r(k + N)|^2 \right) = \Phi(\theta),$$

so $\Lambda(\theta) \le 0$. At $\theta_0$, $r(k + N) = e^{j 2\pi\varepsilon} r(k)$ for $k \in I$, so $\gamma(\theta_0) = e^{-j 2\pi\varepsilon} \sum_k |r(k)|^2$ and $\Phi(\theta_0) = \sum_k |r(k)|^2$. Both inequalities are equalities, $\Lambda(\theta_0) = 0$, and the angle of $\gamma(\theta_0)$ is $-2\pi\varepsilon$ modulo $2\pi$. $\square$

A tie needs $|r(k)| = |r(k + N)|$ for all $N_{cp}$ pairs at some other $\theta$, with a common phase difference. For samples with a continuous distribution this has probability zero. With constant-modulus time samples it can happen, so the tests build the symbols from 4-QAM subcarrier values through an inverse DFT, whose time samples do not have a constant modulus.

**The variance of the offset estimate (a closed form at high SNR).** Fix the sent symbol, let $E = \sum_{k \in I} |s(k)|^2$ be the energy of the prefix, and take $\theta = \theta_0$ with noise $\mathcal{CN}(0, N_0)$. Then

$$e^{j 2\pi\varepsilon} \gamma(\theta_0) = E + Z, \qquad Z = \sum_k s(k)\, n'^*(k) + \sum_k n(k)\, s^*(k) + \sum_k n(k)\, n'^*(k),$$

where $n'$ is the rotated noise of the second sample, again $\mathcal{CN}(0, N_0)$. The three sums are uncorrelated with zero mean and have variances $E N_0$, $E N_0$ and $N_{cp} N_0^2$. For a small $Z$, the angle error is $\operatorname{Im}(Z) / E$, and $\operatorname{Im}(Z)$ has half the variance of $Z$, so

$$\operatorname{var}(\hat\varepsilon) \approx \frac{1}{4\pi^2} \cdot \frac{2 E N_0 + N_{cp} N_0^2}{2 E^2} = \frac{1}{4\pi^2} \cdot \frac{N_0}{E} \left( 1 + \frac{N_{cp} N_0}{2E} \right).$$

With the mean energy $E = N_{cp} E_s$ and $\text{SNR} = E_s / N_0$ this is $\frac{1}{4\pi^2 N_{cp}\, \text{SNR}} \left( 1 + \frac{1}{2\,\text{SNR}} \right)$, which is $1.6623 \times 10^{-4}$ for $N_{cp} = 16$ at 10 dB. The tests measure the variance for a fixed symbol within 15 percent of the first form. The estimate uses only the $N_{cp}$ prefix pairs, so its variance is $N / N_{cp}$ times larger than that of an estimator that correlates two repeated symbols of $N$ samples.
