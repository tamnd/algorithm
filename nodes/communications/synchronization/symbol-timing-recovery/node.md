---
tag: 1RDGYZ
kind: problem
slug: symbol-timing-recovery
name: Symbol timing recovery
aliases:
- clock recovery
- timing synchronization
area: communications/synchronization
level: core
summary: "Estimate and track the instants at which the receiver should sample the matched filter output, from the received signal, so that each sample is read at the peak of its pulse."
prereqs: [matched-filter, nyquist-isi-criterion, pulse-shaping]
see_also: [early-late-gate-synchronizer, gardner-timing-error-detector, mueller-muller-timing-recovery, oerder-meyr-timing-estimation, farrow-interpolator, modified-cramer-rao-bound, eye-diagram, carrier-recovery]
sources:
  - book: isbn:9780306457258
    title: "Umberto Mengali and Aldo N. D'Andrea, Synchronization Techniques for Digital Receivers, Plenum Press, 1997"
    locator: "Chapter 7 (timing recovery with baseband signals), Chapter 8 (timing recovery with linear modulations) and Chapter 2 (the modified Cramer-Rao bound)"
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Section 5.3 (symbol timing estimation)"
  - book: isbn:9780471502753
    title: "Heinrich Meyr, Marc Moeneclaey and Stefan A. Fechtel, Digital Communication Receivers, Wiley, 1998"
    locator: "Chapter 5 (synthesis of synchronization algorithms, including timing estimators) and Chapter 9 (interpolation)"
  - paper: doi:10.1109/TCOMM.1994.580247
    title: "A. N. D'Andrea, U. Mengali and R. Reggiannini, The modified Cramer-Rao bound and its application to synchronization problems, IEEE Transactions on Communications 42(2/3/4), 1994, pages 1391 to 1399"
    locator: "the modified Cramer-Rao bound for the timing delay"
  - paper: doi:10.1109/26.221081
    title: "Floyd M. Gardner, Interpolation in digital modems, Part I, Fundamentals, IEEE Transactions on Communications 41(3), 1993, pages 501 to 507"
    locator: "timing correction in all-digital receivers by interpolation with a free-running sampling clock"
---

Symbol timing recovery is the problem of finding the instants $kT + \tau$ at which a receiver should sample the output of its [matched filter](/matched-filter/), so that each sample is read where the pulse of symbol $k$ has its peak and the pulses of the other symbols cross zero. The transmitter's symbol clock is not sent, so the delay $\tau$ and its slow drift must be estimated from the signal. A sample at the wrong instant has [intersymbol interference](/intersymbol-interference/) and a smaller useful part, which raises the error rate. Feedback methods use a timing error detector in a loop: the [early-late gate](/early-late-gate-synchronizer/), the [Gardner detector](/gardner-timing-error-detector/) and the decision-directed [Mueller and Müller detector](/mueller-muller-timing-recovery/). Feedforward methods estimate $\tau$ for a block at once, as the [Oerder and Meyr estimator](/oerder-meyr-timing-estimation/) does. In all-digital receivers the sampling clock is free-running, and the strobes at the estimated instants are computed by an interpolator such as the [Farrow interpolator](/farrow-interpolator/). The [modified Cramer-Rao bound](/modified-cramer-rao-bound/) gives the variance that no unbiased estimator can beat.

## In plain words

A receiver reads one number for each symbol from a smooth received wave. Each symbol makes a bump in the wave, and the bumps overlap. If the receiver reads at the top of a bump, the other bumps add nothing there. If it reads too early or too late, it gets less of the right symbol and some of its neighbours, so mistakes become more likely. The receiver does not know where the tops are, because its clock is not the same as the sender's clock. Timing recovery finds the tops from the wave itself and follows them as the two clocks drift apart.

## Definition

**Input.** The matched filter output of a linearly modulated signal, with $T = 1$,
$$y(t) = e^{j\theta}\sum_m a_m\,g(t - m - \tau) + v(t),$$
where $g$ is the overall pulse, usually a [raised cosine](/raised-cosine-filter/) with roll-off $\beta$ that satisfies the [Nyquist ISI criterion](/nyquist-isi-criterion/), the symbols $a_m$ are from a constellation such as [PSK](/phase-shift-keying/) or QAM with $E|a_m|^2 = 1$, $\theta$ is the carrier phase, and $v$ is filtered white noise with $E_s/N_0$ per symbol. The receiver has samples of $y$ at a known rate, usually one, two or four per symbol, taken by its own clock.

**Output.** Estimates $\hat\tau_k$, so that the strobes $y(k + \hat\tau_k)$ are close to $e^{j\theta}a_k$ plus noise. The delay is defined modulo one symbol. Which symbol a strobe belongs to is a question of [frame synchronization](/frame-synchronization/).

**Measures.** The timing jitter $E(\hat\tau_k - \tau)^2$ in steady state, the bias, the acquisition time from a large initial error, the rate of slips by one symbol, and the loss in error rate against perfect timing.

## Variants

- **By the use of data.** Non-data-aided (the statistics of the signal only), decision-directed (the receiver's decisions) or data-aided (a known preamble or pilots). See [data-aided synchronization](/data-aided-synchronization/).
- **By structure.** Feedback, with a timing error detector, a loop filter and a numerically controlled oscillator, or feedforward, with an estimate from a block of samples.
- **By the samples per symbol.** One sample per symbol at the strobe instant (Mueller and Müller), two (Gardner) or more (Oerder and Meyr, early-late gate).
- **Analog or digital correction.** Older receivers adjust the phase of a voltage-controlled sampling clock. All-digital receivers keep a fixed clock and interpolate.
- **With or without carrier recovery.** Detectors that use $|y|^2$ or $\operatorname{Re}\{\bar y\,y\}$ products work before carrier recovery. Decision-directed detectors need the carrier phase.

## Examples

**Why the timing matters (closed form under assumptions).** For BPSK with a raised cosine pulse with $\beta = 0.5$ and no noise, the worst-case eye opening at an offset $\Delta$, $g(\Delta) - \sum_{m \ne 0}|g(\Delta + m)|$, is:

| offset $\Delta$ | 0 | 0.1 | 0.2 | 0.25 | 0.3 | 0.5 |
|---|---|---|---|---|---|---|
| eye opening | 1 | 0.785 | 0.535 | 0.400 | 0.261 | $-0.300$ |

At half a symbol the eye is closed, so some data patterns are decided wrongly even without noise. See also the [eye diagram](/eye-diagram/).

**The size of the bound (closed form under assumptions).** For a raised cosine spectrum with $\beta = 0.5$, the normalized mean square bandwidth is $\xi = \frac{1}{12} + \beta^2\bigl(\frac14 - \frac{2}{\pi^2}\bigr) = 0.0952$. At $E_s/N_0 = 10$ dB, the MCRB for a block of 100 symbols is $1.33 \times 10^{-4}$, a standard deviation of $0.0115$ symbol, and a loop with noise bandwidth $B_LT = 0.01$ has the bound $2.66 \times 10^{-4}$.

**How close the methods come (measurement).** With these values and QPSK, the measured jitter of loops with $B_LT = 0.01$ was 1.4 to 2.1 times the bound for the Gardner detector, 2.0 to 2.8 times for the early-late gate and 2.8 to 3.6 times for Mueller and Müller, and 1.9 times for the Oerder and Meyr estimator on blocks of 100 symbols. The details are on the pages of each method.

## Known algorithms

| Algorithm | Data | Structure | Samples per symbol | Note |
|---|---|---|---|---|
| [Early-late gate](/early-late-gate-synchronizer/) | non-data-aided | feedback | 3 | compares the power before and after the strobe |
| [Gardner detector](/gardner-timing-error-detector/) | non-data-aided | feedback | 2 | independent of the carrier phase; needs $\beta > 0$ |
| [Mueller and Müller](/mueller-muller-timing-recovery/) | decision-directed | feedback | 1 | no self-noise at lock; needs the carrier phase |
| [Oerder and Meyr](/oerder-meyr-timing-estimation/) | non-data-aided | feedforward | 4 | phase of the spectral line of $\lvert y\rvert^2$ |
| Data-aided ML | known symbols | feedforward or feedback | 2 or more | correlation with the known waveform |

The [Farrow interpolator](/farrow-interpolator/) is not an estimator. It computes the strobes at the estimated instants from the fixed-rate samples, for all of the methods above. In spread spectrum, the [delay-locked loop](/delay-locked-loop/) tracks the timing of a spreading code with the same early-late idea.

## Bounds

- **Lower bound (theorem).** Every unbiased estimator of $\tau$ from $L_0$ symbols has a variance of at least the MCRB $\frac{1}{8\pi^2\xi L_0\,E_s/N_0}$ in symbol periods squared. With known data this is the true CRB. Without known data, the true CRB is larger at low SNR.
- **Loops (closed form under assumptions).** In the linear model, a loop with noise bandwidth $B_LT$ is compared with the bound for $L_0 = 1/(2B_LT)$ symbols.
- **Self-noise (measurement and theorem).** Non-data-aided detectors have a jitter from the data pattern even without noise, which sets a floor at high SNR. The Mueller and Müller detector has none at lock with correct decisions (theorem).
- **Excess bandwidth.** The timing information of non-data-aided methods comes from the band edges, so it vanishes as $\beta \to 0$ (closed form: the spectral line of $|y|^2$ has amplitude $\beta/4$ for a raised cosine).
- **Ambiguity (theorem).** The delay can be found only modulo one symbol from a stationary signal.

## Reductions

- **Timing from a tone.** The power $|y(t)|^2$ has a mean with a sinusoid at the symbol rate whose phase is $\tau$, so non-data-aided timing reduces to estimating the phase of a tone, as in the Oerder and Meyr estimator.
- **Timing to fractional delay.** Once $\hat\tau$ is known, producing the strobes is a [sample rate conversion](/sample-rate-conversion/) problem, solved by interpolation.
- **Known data to delay estimation.** With known symbols, timing is the estimation of the delay of a known waveform in noise, the problem of a [matched filter](/matched-filter/) peak, as in ranging.
- **Order with the carrier.** Many timing detectors are insensitive to the carrier phase, so receivers usually recover the timing first and then the [carrier](/carrier-recovery/).

## Applications

- **Wired and wireless modems.** Every digital receiver of single-carrier signals, from telephone line modems to satellite and microwave links, recovers the symbol timing. A Gardner loop with a Farrow interpolator is a common all-digital design.
- **Burst receivers.** Satellite return links and packet radios estimate the timing of each burst with a feedforward estimator or from a preamble.
- **Serial data links.** Clock and data recovery circuits in wired serial links recover the bit clock from the data transitions.
- **Optical coherent receivers.** Digital signal processors after the analog-to-digital converters recover the timing at about two samples per symbol before equalization.

## References
