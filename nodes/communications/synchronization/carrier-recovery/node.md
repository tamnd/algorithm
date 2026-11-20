---
tag: 0GGVF6
kind: problem
slug: carrier-recovery
name: Carrier recovery
aliases:
- carrier synchronization
- carrier phase recovery
area: communications/synchronization
level: core
summary: Estimate and track the phase and frequency of the carrier, so that a coherent receiver can rotate the signal back to baseband.
prereqs: [phase-shift-keying, quadrature-amplitude-modulation, additive-white-gaussian-noise-channel]
see_also: [phase-locked-loop, costas-loop, squaring-loop, decision-directed-carrier-recovery, viterbi-viterbi-phase-estimation, cycle-slip, frequency-offset-estimation, modified-cramer-rao-bound]
sources:
  - book: isbn:9780306457258
    title: "Umberto Mengali and Aldo N. D'Andrea, Synchronization Techniques for Digital Receivers, Plenum Press, 1997"
    locator: "Chapter 5 (carrier phase recovery with linear modulations) and Chapter 3 (carrier frequency recovery with linear modulations)"
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Section 5.2 (carrier phase estimation: the maximum likelihood estimate, the phase-locked loop, decision-directed and non-decision-directed loops)"
  - book: isbn:9780471502753
    title: "Heinrich Meyr, Marc Moeneclaey and Stefan A. Fechtel, Digital Communication Receivers, Wiley, 1998"
    locator: "Section 6.4 (cycle slipping, pages 385 to 399)"
  - paper: doi:10.1109/TCOMM.1994.580247
    title: "A. N. D'Andrea, U. Mengali and R. Reggiannini, The modified Cramer-Rao bound and its application to synchronization problems, IEEE Transactions on Communications 42(2/3/4), 1994, pages 1391 to 1399"
    locator: "the modified Cramer-Rao bound for the carrier phase and frequency"
---

Carrier recovery is the problem of estimating the phase, and often the residual frequency, of the carrier of a received signal, so that a coherent receiver can rotate each sample back before it decides on the symbol. The problem is the same for all receivers; the algorithms differ in how they use the data. A [phase-locked loop](/phase-locked-loop/) tracks a pure carrier or a pilot tone with a feedback loop. The [Costas loop](/costas-loop/) and the [squaring loop](/squaring-loop/) are feedback loops that remove the modulation of PSK without knowing the data, and [decision-directed carrier recovery](/decision-directed-carrier-recovery/) removes it with the receiver's own decisions. [Viterbi and Viterbi phase estimation](/viterbi-viterbi-phase-estimation/) is a feedforward method that estimates the phase of each block of M-PSK symbols at once. A [cycle slip](/cycle-slip/) is not an algorithm but the main way all of them fail: a jump of the estimate by a symmetry angle of the constellation. The residual frequency is the subject of [frequency offset estimation](/frequency-offset-estimation/), and the [modified Cramer-Rao bound](/modified-cramer-rao-bound/) gives the variance that no method can beat.

## In plain words

The transmitter puts its data on a wave. The receiver has its own wave, made by a different oscillator, so the two never start at the same point and drift apart slowly. If the receiver does not correct this, every received symbol appears turned by some angle, and a large turn changes the symbol that the receiver reads. Carrier recovery measures that turn and how fast it changes, from the noisy signal, and undoes it. The receiver may know some symbols in advance, may use the symbols it has just read, or may use only the shape of the signal. When noise is strong, the measurement can jump to a wrong position that looks just as good.

## Definition

**Input.** Samples of the matched filter output at the correct symbol instants,
$$r_k = a_k e^{j(\theta + \omega k)} + w_k, \qquad k = 0, 1, \ldots,$$
where $a_k$ are the symbols of a constellation such as [PSK](/phase-shift-keying/) or [QAM](/quadrature-amplitude-modulation/), $\theta$ is the unknown carrier phase, $\omega$ is the residual frequency offset in radians per symbol, and $w_k \sim \mathcal{CN}(0, N_0)$ is white noise as in the [AWGN channel](/additive-white-gaussian-noise-channel/). In a channel with phase noise, $\theta$ is replaced by a random process $\theta_k$, often a Wiener process.

**Output.** Estimates $\hat\theta_k$ of the phase at each symbol, so that $r_k e^{-j\hat\theta_k} \approx a_k$ up to the noise. In the feedforward form, one estimate per block of $N$ symbols; in the feedback form, one updated estimate per symbol.

**Ambiguity.** If the data are not known and the constellation is invariant under rotation by $2\pi/M$ (M-PSK, or $M = 4$ for square QAM), then $\theta$ and $\theta + 2\pi/M$ give the same distribution of $r$. So a non-data-aided estimator can only find $\theta$ modulo $2\pi/M$ (theorem). The rest must come from known symbols or from differential encoding.

**Measures.** The mean square error $E(\hat\theta_k - \theta_k)^2$ in steady state, the acquisition time from a large initial error, the mean time between cycle slips, and the loss in symbol error rate against perfect synchronization.

## Variants

- **By the use of data.** Data-aided (known pilots or preamble), decision-directed (decided symbols) and non-data-aided (the statistics of the signal only). See [data-aided synchronization](/data-aided-synchronization/).
- **By structure.** Feedback (a loop with an error detector, a loop filter and a numerically controlled oscillator) or feedforward (an estimate computed from a block, then applied to it).
- **Phase only, or phase and frequency.** A loop of second order tracks a constant frequency offset with no steady-state phase error. A large offset is first removed by a separate frequency estimator, since a phase loop alone may not acquire it.
- **Continuous or burst mode.** Continuous links can use narrow loops and long acquisition. Burst modems need an estimate from a short preamble or from the burst itself, which favors feedforward estimators.
- **Analog and passband loops.** Older receivers recover the carrier at an intermediate frequency with an analog loop; digital receivers work on complex baseband samples with a free-running oscillator and a digital derotator.

## Examples

**Why the phase matters (theorem).** Without noise, a QPSK symbol is decided correctly as long as the phase error is below $\pi/4 = 45^\circ$. For 16-QAM with levels $\pm1, \pm3$, the corner point $3 + 3j$ crosses a decision boundary at an error of $0.2946$ rad, about $16.9^\circ$, so denser constellations need a more accurate phase.

**A frequency offset breaks a phase-only estimate (theorem).** An offset of $0.01$ cycles per symbol turns the phase by $2\pi \cdot 0.01 \cdot 31 = 1.95$ rad over 32 symbols. One phase estimate for the whole block can match the middle, but the first and last symbols then have errors of about $0.97$ rad, more than $\pi/4$, so QPSK decisions there are wrong even without noise.

**A data-aided and a non-data-aided estimate (measurement).** Eight QPSK symbols at $E_s/N_0 = 10$ dB with $\theta = 0.7$ rad (seed 5). With known symbols, the maximum likelihood estimate $\hat\theta = \arg\sum_k a_k^\ast r_k$ is $0.655$. Without them, the fourth-power estimate $\hat\theta = \frac14\arg\bigl(-\sum_k r_k^4\bigr)$ is $0.626$. The bound is a standard deviation of $\sqrt{1/(2 \cdot 8 \cdot 10)} = 0.079$ rad. The second estimate is correct only modulo $\pi/2$; it agrees with $\theta$ here because $\theta$ is within $\pm\pi/4$.

**The size of the bound.** For $N = 32$ symbols at $E_s/N_0 = 10$ dB, the MCRB of the phase is $1/(2 \cdot 32 \cdot 10) = 1.56 \times 10^{-3}$ rad$^2$, a standard deviation of $2.3^\circ$. On the Viterbi and Viterbi page, the measured mean square error of the estimator with these values is between 1.13 and 1.17 times this bound, depending on the nonlinearity.

## Known algorithms

| Algorithm | Data | Structure | Constellations | Note |
|---|---|---|---|---|
| [Phase-locked loop](/phase-locked-loop/) | pilot tone or known data | feedback | any, with known $a_k$ | the base of all loops |
| [Costas loop](/costas-loop/) | non-data-aided | feedback | BPSK, QPSK | the product of I and Q arms removes the data |
| [Squaring loop](/squaring-loop/) | non-data-aided | feedback | M-PSK | the M-th power removes the data, with a squaring loss |
| [Decision-directed carrier recovery](/decision-directed-carrier-recovery/) | decisions | feedback | PSK and QAM | at the bound at high SNR; false lock and error propagation at low SNR |
| [Viterbi and Viterbi phase estimation](/viterbi-viterbi-phase-estimation/) | non-data-aided | feedforward | M-PSK | block estimate, then unwrapping |
| Data-aided ML, $\arg\sum_k a_k^\ast r_k$ | known data | feedforward | any | reaches the MCRB above a low threshold |

For the frequency, see the [Kay](/kay-frequency-estimator/), [Rife and Boorstyn](/rife-boorstyn-frequency-estimator/) and [Luise and Reggiannini](/luise-reggiannini-estimator/) estimators on the [frequency offset estimation](/frequency-offset-estimation/) page. For QAM without known data, non-data-aided methods also use the fourth power of the symbols, or a blind phase search over test angles.

## Bounds

- **Lower bound (theorem).** Every unbiased phase estimator from $N$ symbols has a variance of at least the [MCRB](/modified-cramer-rao-bound/) $\frac{1}{2N\,E_s/N_0}$. With known data this is the true CRB; without known data the true CRB is larger at low SNR.
- **Loops (closed form under assumptions).** In the linear model, a data-aided or decision-directed loop with noise bandwidth $B_L T$ has the phase error variance $\frac{B_L T}{E_s/N_0}$, which equals the MCRB for $N = \frac{1}{2B_LT}$. Non-data-aided loops multiply this by a squaring loss above 1 that grows at low SNR.
- **Ambiguity (theorem).** Without known data, the phase can be found only modulo the symmetry angle $2\pi/M$ of the constellation.
- **Cycle slips (theorem for the first-order PLL, rule otherwise).** The mean time between slips grows about as $e^{2\rho}$ in the loop SNR $\rho$. Since the effective loop SNR of an $M$-fold loop is about $\rho/M^2$, slips set the lowest usable SNR, not the variance.

## Reductions

- **Known data to one tone.** With known symbols, $z_k = a_k^\ast r_k = |a_k|^2 e^{j(\theta + \omega k)} + a_k^\ast w_k$ is a tone in noise, so phase estimation becomes the estimation of the phase of a tone, and frequency estimation becomes [frequency offset estimation](/frequency-offset-estimation/) of a tone.
- **M-PSK to one tone.** For M-PSK, $r_k^M$ has the term $a_k^M e^{jM\theta} = \text{const} \cdot e^{jM\theta}$, so M-PSK carrier recovery reduces to tone phase estimation of $M\theta$, at the price of extra noise terms and the ambiguity of $2\pi/M$.
- **Decisions to known data.** At high SNR, decisions are almost always correct, and decision-directed recovery behaves like the data-aided case.
- **Coupling with timing.** The model assumes correct [symbol timing](/symbol-timing-recovery/). Many timing estimators do not need the carrier phase, so receivers usually recover the timing first, then the frequency, then the phase.

## Applications

- **Satellite and microwave modems.** Continuous links with PSK and APSK use Costas, squaring or decision-directed loops; standards such as DVB-S2 insert pilot blocks to support carrier recovery at low SNR.
- **Burst modems.** Short packets use a preamble and feedforward estimators of frequency and phase.
- **Coherent optical receivers.** Laser phase noise is large and fast, so feedforward estimators such as Viterbi and Viterbi for QPSK, or blind phase search for QAM, run on blocks of a few tens of symbols, with differential coding or pilots against slips.
- **OFDM.** Wi-Fi and LTE receivers track the common phase error of each OFDM symbol with pilot subcarriers, after the frequency offset is removed.
- **Navigation receivers.** GNSS receivers track the carrier with a Costas loop to measure carrier phase and Doppler.

## References
