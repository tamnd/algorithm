---
tag: WVGF17
kind: technique
slug: noncoherent-detection
name: Noncoherent detection
aliases:
- envelope detection
- square-law detection
area: communications/modulation-and-detection
level: core
summary: Detects orthogonal or differential signals from energies or envelopes without knowing the carrier phase, at a small loss in SNR.
prereqs: [symbol-detection, matched-filter, frequency-shift-keying]
see_also: [differential-phase-shift-keying, frequency-shift-keying, energy-detector, carrier-recovery, rayleigh-fading-channel, frequency-hopping-spread-spectrum, likelihood-ratio-test, bit-error-rate]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Section 4.5 (optimal detection in the presence of uncertainty, noncoherent detection), with Section 4.5-2 (optimal noncoherent detection of FSK), Section 4.5-3 (error probability of orthogonal signaling with noncoherent detection) and Section 4.5-5 (differential PSK)
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Chapter 3 (detection in a Rayleigh fading channel, with noncoherent detection of orthogonal signals)
---

Noncoherent detection decides which signal was sent without knowing the carrier phase. The receiver correlates the received signal with each candidate, takes the magnitude or the squared magnitude of each correlation, and picks the largest. A random phase rotates a complex correlation but does not change its magnitude, so no phase reference and no [carrier recovery](/carrier-recovery/) are needed. The price is a loss in SNR against coherent detection, about $0.75$ dB for binary FSK at a bit error rate of $10^{-5}$. The signals must be chosen for it: orthogonal tones as in [frequency-shift keying](/frequency-shift-keying/), or a phase difference over two symbols as in [differential phase-shift keying](/differential-phase-shift-keying/), which is the noncoherent detector for two symbols.

## In plain words

Imagine listening for which of two whistles was blown, when you do not know exactly when in its cycle each sound wave started. You cannot compare the waves peak by peak, but you can measure how loud each pitch is. The louder pitch is the answer. This works only if the two whistles never sound alike, whatever their timing. The method throws away the phase information that a fully synchronized receiver would use, so it needs a slightly stronger signal for the same number of mistakes. In return it is simple and it keeps working when the carrier drifts.

## When it applies

- The channel turns the signal by a phase $\theta$ that is unknown, uniformly distributed, and constant over one decision interval. The phase may change from one interval to the next.
- The signals stay distinguishable for every value of $\theta$: for $M$ equal-energy signals, $|\langle s_m, s_n\rangle|$ is small for $m \ne n$. Orthogonal signals in this sense have $\langle s_m, s_n\rangle = 0$, which for FSK means a tone spacing that is a multiple of $1/T$.
- Information is not in the absolute phase. PSK and QAM carry it there, so they need a coherent receiver, or a differential version.
- It is the natural choice when the phase changes too fast for a phase-locked loop, in frequency hopping, in short bursts with no time to lock, and in cheap receivers.

## The template

The received complex baseband signal is $r(t) = e^{j\theta}s_m(t) + w(t)$, where $j$ is the imaginary unit, $w$ is white Gaussian noise of density $N_0$, and $s_m$ has energy $E_m$. Write $z_m = \langle r, s_m\rangle = \int r(t)\, s_m^*(t)\, dt$.

1. **Average the likelihood over the phase.** Given $\theta$, the likelihood of $s_m$ is proportional to $\exp\big(-E_m/N_0 + 2\,\mathrm{Re}(e^{-j\theta}z_m)/N_0\big)$. The average over $\theta$ uniform on $[0, 2\pi)$ is

$$\Lambda_m = e^{-E_m/N_0}\, I_0\!\left(\frac{2|z_m|}{N_0}\right),$$

where $I_0$ is the modified Bessel function of order $0$, $I_0(x) = \frac{1}{2\pi}\int_0^{2\pi} e^{x\cos\phi}\, d\phi$. Only $|z_m|$ enters: the statistic is the envelope of the correlation.

2. **Decide.** For equal priors, choose the $m$ with the largest $\Lambda_m$. For equal energies, $I_0$ is increasing on $[0, \infty)$, so the rule is to choose the largest $|z_m|$, the **envelope receiver**, or equally the largest $|z_m|^2$, the **square-law receiver**. These two give the same decision because squaring is increasing on $[0, \infty)$. For unequal energies the full rule with $I_0$ and the term $E_m/N_0$ is needed.

3. **Build the correlations.** In passband, $z_m$ is the output of two correlators per signal, with the cosine and the sine of the carrier, or a [matched filter](/matched-filter/) followed by an envelope detector, sampled at the end of the symbol.

4. **Analyze the error.** For orthogonal equal-energy signals, the correlation with a wrong signal is pure noise, and $|z_n|^2$ is exponential with mean $E_s N_0$. The correlation with the right signal has a Rician magnitude. For $M = 2$, the probability that the wrong one is larger is a closed form:

$$P_b = \tfrac12\, e^{-E_b/(2N_0)}.$$

The $M$-ary symbol error rate is the alternating sum on the [FSK page](/frequency-shift-keying/).

## Classic examples

**Noncoherent binary FSK.** Tones $1/T$ apart, two square-law branches, decide the larger. At $E_b/N_0 = 10$ dB, $P_b = \tfrac12 e^{-5} = 3.369 \times 10^{-3}$, against $Q(\sqrt{10}) = 7.83 \times 10^{-4}$ for coherent BFSK. For $P_b = 10^{-5}$ the noncoherent receiver needs $E_b/N_0 = 2\ln(5 \times 10^4) = 21.64$, that is $13.35$ dB, and the coherent receiver $12.60$ dB: a loss of $0.75$ dB.

**DPSK.** Over two symbols, the binary DPSK signals $(1, 1)$ and $(1, -1)$ are orthogonal with energy $2E_b$. The square-law receiver compares $|r_{n-1} + r_n|^2$ with $|r_{n-1} - r_n|^2$, which is the sign of $\mathrm{Re}(r_n r_{n-1}^*)$, and the formula above with $2E_b$ in place of $E_b$ gives $P_b = \tfrac12 e^{-E_b/N_0}$. This is $3$ dB better than noncoherent BFSK.

**On-off keying.** One signal and silence, with an envelope detector and a threshold. The two energies differ, so the best threshold on $|z|$ depends on the SNR through the $I_0$ term. An [energy detector](/energy-detector/) for spectrum sensing is the same receiver with an unknown signal shape.

**Frequency hopping.** Each hop lands on a new carrier with a new random phase, and $M$-FSK with square-law detection inside each hop needs no phase tracking across hops. See [frequency-hopping spread spectrum](/frequency-hopping-spread-spectrum/).

## Variations

- **Multiple-symbol detection.** If the phase is constant over $N$ symbols, the receiver can decide $N - 1$ differential symbols jointly by maximizing $|\sum_n r_n s_n^*|$ over the candidate sequences. The loss to coherent detection falls as $N$ grows.
- **Square-law combining.** With $L$ diversity branches, each with its own unknown phase and gain, the receiver sums $|z_m^{(\ell)}|^2$ over the branches and picks the largest sum. Summing envelopes instead of squared envelopes now gives a different decision.
- **Rayleigh fading.** If the gain is complex Gaussian, the receiver cannot know the phase in any case. Noncoherent BFSK then has the closed form $P_b = 1/(2 + \bar\gamma_b)$, where $\bar\gamma_b$ is the average $E_b/N_0$: $9.8 \times 10^{-3}$ at $20$ dB. See [Rayleigh fading channel](/rayleigh-fading-channel/).
- **Partially coherent detection.** If a loop gives a noisy phase estimate, the likelihood uses the distribution of the residual phase, and the receiver lies between the coherent and the noncoherent one.
- **Noncoherent detection of CPM.** A receiver that observes several symbols of a CPM signal can decide the middle symbol from the magnitudes of correlations with all patterns, without a phase reference.

## Pitfalls

- **Tones at the coherent spacing.** At a spacing of $1/(2T)$, the noncoherent correlation between two tones is $2/\pi = 0.637$ of the energy. Square-law detection of MSK tones symbol by symbol performs badly.
- **A frequency offset.** An offset $\Delta f$ that the receiver does not remove reduces $|z_m|$ by the factor $|\mathrm{sinc}(\Delta f T)|$ and leaks energy into the other branches. At $\Delta f\, T = 0.1$ the power loss is $|\mathrm{sinc}(0.1)|^2 = 0.968$, that is $0.14$ dB, before the leakage.
- **A phase that changes inside the interval.** The model needs a constant phase over the correlation. Phase noise or a fast fading channel inside the symbol breaks it.
- **Unequal energies.** The rule "largest envelope" is optimal only for equal energies. For OOK or for amplitude levels, keep the $E_m/N_0$ term and the $I_0$ form.
- **Envelope or square law.** They agree for one decision on equal-energy signals, but not after combining across branches or symbols, and not in their error analysis. State which one a formula assumes.

## Exercises

1. Show that $\frac{1}{2\pi}\int_0^{2\pi}\exp\big(2\,\mathrm{Re}(e^{-j\theta}z)/N_0\big)\, d\theta = I_0(2|z|/N_0)$.
2. Let $X$ and $Y$ be independent, $X$ exponential with mean $\mu$ and $|Y|^2$ the squared magnitude of a complex Gaussian with mean $a$ and variance $\mu$. Show that $P(X > |Y|^2) = \tfrac12 e^{-|a|^2/(2\mu)}$, and derive the noncoherent BFSK formula from it.
3. Show that the DPSK detector $\mathrm{Re}(r_n r_{n-1}^*) \gtrless 0$ is the square-law receiver for the two signals $(1, 1)$ and $(1, -1)$.
4. For noncoherent 4-FSK at $E_b/N_0 = 10$ dB, compute $P_s$ and $P_b$. (Answer: $6.66 \times 10^{-5}$ and $4.44 \times 10^{-5}$.)
5. Find the frequency offset $\Delta f\,T$ at which the power loss of one correlator is $1$ dB.

## References
