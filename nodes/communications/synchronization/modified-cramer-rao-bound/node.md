---
tag: TKCKPY
kind: theorem
slug: modified-cramer-rao-bound
name: Modified Cramer-Rao bound
aliases:
- MCRB
area: communications/synchronization
level: advanced
summary: A lower bound on the variance of synchronization estimates that treats the data as known, looser but easy to compute.
prereqs: [cramer-rao-bound, fisher-information-matrix, additive-white-gaussian-noise-channel]
see_also: [data-aided-synchronization, carrier-recovery, frequency-offset-estimation, symbol-timing-recovery, kay-frequency-estimator, rife-boorstyn-frequency-estimator, luise-reggiannini-estimator, viterbi-viterbi-phase-estimation]
sources:
  - paper: doi:10.1109/TCOMM.1994.580247
    title: "A. N. D'Andrea, U. Mengali and R. Reggiannini, The modified Cramer-Rao bound and its application to synchronization problems, IEEE Transactions on Communications 42(2/3/4), 1994, pages 1391 to 1399"
    locator: "the definition of the MCRB, the proof that it is a lower bound below the true CRB, and the bounds for phase, frequency and timing"
  - paper: "M. Moeneclaey, On the true and the modified Cramer-Rao bounds for the estimation of a scalar parameter in the presence of nuisance parameters, IEEE Transactions on Communications 46(11), 1998, pages 1536 to 1544"
    locator: "the comparison of the true CRB and the MCRB, and their equality in the high-SNR limit"
  - paper: "F. Gini, R. Reggiannini and U. Mengali, The modified Cramer-Rao bound in vector parameter estimation, IEEE Transactions on Communications 46(1), 1998, pages 52 to 60"
    locator: "the extension of the MCRB to several parameters estimated jointly"
  - book: isbn:9780306457258
    title: "Umberto Mengali and Aldo N. D'Andrea, Synchronization Techniques for Digital Receivers, Plenum Press, 1997"
    locator: "Chapter 2 (basic principles, the modified Cramer-Rao bound)"
---

The modified Cramer-Rao bound (MCRB) is a lower bound on the variance of any unbiased estimator of a synchronization parameter, such as a carrier phase, a frequency offset or a symbol timing, when the received signal also depends on unknown data. The true [Cramer-Rao bound](/cramer-rao-bound/) needs the likelihood with the data averaged out, which is hard to compute. The MCRB instead averages the Fisher information of the model with known data over the data. The theorem says that this gives a valid lower bound for every unbiased estimator, data-aided or not, and that it is never larger than the true CRB. For the additive white Gaussian noise channel it has simple closed forms: $\frac{1}{2N\,E_s/N_0}$ for the phase and $\frac{6}{(E_s/N_0)\,N(N^2-1)}$ for the frequency in radians per symbol. With known data, as in [data-aided synchronization](/data-aided-synchronization/), the MCRB is the true CRB. Without known data it is looser at low SNR and becomes tight at high SNR. It is the usual yardstick for [carrier recovery](/carrier-recovery/) and [frequency offset estimation](/frequency-offset-estimation/): the [Kay](/kay-frequency-estimator/), [Rife and Boorstyn](/rife-boorstyn-frequency-estimator/) and [Luise and Reggiannini](/luise-reggiannini-estimator/) estimators reach it above their thresholds.

## Statement

**Model.** The observation $r$ has the density $p(r \mid u, \lambda)$, where $\lambda$ is a scalar parameter to estimate and $u$ is a nuisance vector (data symbols, other parameters) with a prior density $p(u)$ that does not depend on $\lambda$. The density of $r$ is $p(r \mid \lambda) = E_u\, p(r \mid u, \lambda)$. Assume the usual regularity: $p(r \mid u, \lambda)$ is differentiable in $\lambda$, and differentiation under the integrals over $r$ and $u$ is allowed.

**Definitions.** The true Fisher information is $J(\lambda) = E_r\bigl[\bigl(\partial_\lambda \ln p(r \mid \lambda)\bigr)^2\bigr]$. The modified Fisher information is
$$J_M(\lambda) = E_{r,u}\Bigl[\bigl(\partial_\lambda \ln p(r \mid u, \lambda)\bigr)^2\Bigr],$$
and the MCRB is $1/J_M(\lambda)$.

**Theorem (D'Andrea, Mengali and Reggiannini, 1994).** For every estimator $\hat\lambda(r)$ with $E\hat\lambda = \lambda$ for all $\lambda$,
$$\operatorname{var}\hat\lambda \;\ge\; \mathrm{CRB}(\lambda) = \frac{1}{J(\lambda)} \;\ge\; \mathrm{MCRB}(\lambda) = \frac{1}{J_M(\lambda)}.$$

**Closed forms for the AWGN channel.** Let $r_k = s_k(u, \lambda) + w_k$, $k = 0, \ldots, N - 1$, with $w_k \sim \mathcal{CN}(0, N_0)$ white. Then
$$J_M(\lambda) = \frac{2}{N_0}\, E_u \sum_k \Bigl|\frac{\partial s_k}{\partial\lambda}\Bigr|^2.$$
With independent data of energy $E_s = E|a_k|^2$:

- **Phase**, $s_k = a_k e^{j\theta}$: $\mathrm{MCRB}(\theta) = \dfrac{1}{2N\,E_s/N_0}$.
- **Frequency**, $s_k = a_k e^{j(\omega k + \theta)}$ with $\theta$ also unknown: $\mathrm{MCRB}(\omega) = \dfrac{6}{(E_s/N_0)\,N(N^2-1)}$ in radians per symbol, or $\dfrac{3}{2\pi^2 (E_s/N_0) N(N^2-1)}$ in cycles per symbol.
- **Timing**, $s(t) = \sum_i a_i g(t - iT - \tau)$ with zero-mean data, observed over $N$ symbols: $\mathrm{MCRB}(\tau) = \dfrac{T^2}{8\pi^2 \xi N\,E_s/N_0}$, where $\xi = T^2 \int f^2|G(f)|^2 df \big/ \int |G(f)|^2 df$. For a raised-cosine $|G(f)|^2$ with roll-off $\alpha$, $\xi = \frac{1}{12} + \alpha^2\bigl(\frac14 - \frac{2}{\pi^2}\bigr)$.

The frequency bound with the phase unknown is the entry of the inverse of a $2 \times 2$ modified Fisher matrix, as in the vector form of Gini, Reggiannini and Mengali. The timing form ignores the edge effects of a finite record. For $N = 32$ and $E_s/N_0 = 10$, the frequency bound is $6/(10 \cdot 32 \cdot 1023) = 1.833 \times 10^{-5}$ rad$^2$.

## In plain words

A receiver must measure a property of the signal, such as its phase, while it does not know the data that the signal carries. Not knowing the data can only make the measurement harder. The modified bound pretends that the receiver knows the data and asks how well it could measure then, on average over all possible data. That is a limit that no real receiver can beat. It is easy to compute, because with known data the signal is fully specified. It can be too optimistic when noise is strong, since then not knowing the data really does hurt. When noise is weak, the data can almost be read from the signal, and the limit is close to the real one.

## Proof

**Step 1 (the score of the marginal density).** Since $p(u)$ does not depend on $\lambda$,
$$\partial_\lambda p(r \mid \lambda) = \int p(u)\, \partial_\lambda p(r \mid u, \lambda)\, du = \int p(u)\, p(r \mid u, \lambda)\, \partial_\lambda \ln p(r \mid u, \lambda)\, du.$$
Dividing by $p(r \mid \lambda)$, and using the posterior $p(u \mid r, \lambda) = p(u)\,p(r \mid u, \lambda)/p(r \mid \lambda)$, gives
$$\partial_\lambda \ln p(r \mid \lambda) = E\bigl[S \mid r\bigr], \qquad S = \partial_\lambda \ln p(r \mid u, \lambda).$$

**Step 2 ($J \le J_M$).** By the conditional form of Jensen's inequality, $(E[S \mid r])^2 \le E[S^2 \mid r]$. Taking the expectation over $r$ gives $J = E\bigl[(E[S \mid r])^2\bigr] \le E[S^2] = J_M$. So $1/J \ge 1/J_M$.

**Step 3 (the CRB).** The inequality $\operatorname{var}\hat\lambda \ge 1/J$ for unbiased estimators is the [Cramer-Rao bound](/cramer-rao-bound/) for the density $p(r \mid \lambda)$. Together with Step 2 this proves the theorem. $\square$

**The AWGN forms.** With $\ln p(r \mid u, \lambda) = -\frac{1}{N_0}\sum_k |r_k - s_k|^2 + c$, the score is $S = \frac{2}{N_0}\sum_k \operatorname{Re}\bigl(\overline{w_k}\,\partial_\lambda s_k\bigr)$. Given $u$, each term is Gaussian with variance $\frac{N_0}{2}\bigl|\partial_\lambda s_k\bigr|^2 \cdot \frac{4}{N_0^2}$, and the terms are independent, so $E[S^2 \mid u] = \frac{2}{N_0}\sum_k |\partial_\lambda s_k|^2$. Average over $u$.

- Phase: $|\partial_\theta s_k|^2 = |a_k|^2$, so $J_M = 2N E_s/N_0$.
- Frequency and phase together: $\partial_\omega s_k = jk\,s_k$ and $\partial_\theta s_k = j s_k$. The modified Fisher matrix is $\frac{2E_s}{N_0}\begin{pmatrix}\sum k^2 & \sum k\\ \sum k & N\end{pmatrix}$, with $\sum_{k=0}^{N-1} k = \frac{N(N-1)}{2}$ and $\sum k^2 = \frac{N(N-1)(2N-1)}{6}$. Its determinant over $\left(\frac{2E_s}{N_0}\right)^2$ is $N\sum k^2 - (\sum k)^2 = \frac{N^2(N^2-1)}{12}$, and the $(\omega, \omega)$ entry of the inverse is $\frac{N}{(2E_s/N_0)\,N^2(N^2-1)/12} = \frac{6}{(E_s/N_0)N(N^2-1)}$. That this entry of the inverse of the modified matrix bounds the variance is the vector theorem of Gini, Reggiannini and Mengali, proved in the same way.
- Timing: $E\int |\partial_\tau s|^2 dt = \sum_i E|a_i|^2 \int |g'(t)|^2 dt$, since the cross terms vanish for independent zero-mean data, and $\int |g'|^2 = 4\pi^2 \int f^2 |G(f)|^2 df$ by Parseval. So $J_M = \frac{2N}{N_0} E_s \cdot 4\pi^2 \xi/T^2$, with $E_s = \int|G|^2$ for unit-energy symbols.

## Consequences

- **A bound for every synchronizer.** Data-aided, decision-directed and non-data-aided estimators are all unbiased estimators of $\lambda$ from $r$, so none can beat the MCRB. This is why measured mean square errors are compared with it.
- **Equality with known data.** If $u$ is known (pilots, a preamble), $p(r \mid \lambda)$ is $p(r \mid u, \lambda)$, $S$ is a function of $r$, Step 2 holds with equality, and MCRB $=$ CRB.
- **Rules of thumb for design.** The phase bound falls as $1/N$, the frequency bound as $1/N^3$, both inversely with $E_s/N_0$. A loop with noise bandwidth $B_L T$ has the linear variance $B_L T/(E_s/N_0)$, which equals the MCRB for an averaging window of $N = 1/(2B_L T)$ symbols.
- **Estimators that reach it.** Above their thresholds, the data-aided phase estimator, the [Kay estimator](/kay-frequency-estimator/), the [Rife and Boorstyn estimator](/rife-boorstyn-frequency-estimator/) and the [Luise and Reggiannini estimator](/luise-reggiannini-estimator/) with $L$ near $N/2$ have a mean square error within a few percent to about 20 percent of it in measurements. [Viterbi and Viterbi phase estimation](/viterbi-viterbi-phase-estimation/) approaches it at high SNR.

## Tightness

The MCRB equals the true CRB when the nuisance is known, so in that case it is tight and is reached, at high SNR, by the maximum likelihood estimator. When the data are unknown, the gap is the loss of information caused by the conditional variance of the score in Step 2. For the phase of BPSK with unknown, equally likely data, the true per-symbol Fisher information is $\frac{2}{N_0}E\bigl[\tanh^2(2x/N_0)\bigr]$ with $x \sim \mathcal{N}(\pm1, N_0/2)$ and $E_s = 1$, while the MCRB uses $\frac{2}{N_0}$. A numerical integration of this expectation gives the ratio CRB over MCRB as $2.42$ at $E_s/N_0 = -5$ dB, $1.30$ at 0 dB, $1.019$ at 5 dB and $1.00001$ at 10 dB (a computation, not a closed form). So at low SNR the MCRB can be far from what any non-data-aided estimator can reach, and at high SNR it is tight, which Moeneclaey proved in general for a scalar parameter in 1998. The bound is also not reached below the threshold of nonlinear estimators, where outliers dominate; there, bounds of the Barankin or Ziv-Zakai type are tighter.

## History

The Cramer-Rao bound dates from the 1940s. For synchronization with unknown data, the true bound needs the likelihood averaged over the data, which is hard to compute. Aldo N. D'Andrea, Umberto Mengali and Ruggero Reggiannini named the modified bound, proved that it is a lower bound on the variance of every unbiased estimator and that it is below the true CRB, and computed it for phase, frequency and timing in the IEEE Transactions on Communications in 1994. In 1998, Gini, Reggiannini and Mengali extended it to vector parameters, and Moeneclaey studied when the true CRB and the MCRB agree, showing that they coincide in the high-SNR limit. The bound is a central tool of Mengali and D'Andrea's book of 1997.

## References
