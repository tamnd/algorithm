---
tag: C4FMNP
kind: problem
slug: channel-estimation
name: Channel estimation
aliases:
- channel identification
area: communications/channel-estimation-and-equalization
level: intro
summary: "Estimate the taps h of a channel from y = X h + w, where X holds known pilot symbols and w is noise, so as to minimize the mean squared error E||h_est - h||^2. Solved by LS, LMMSE and their variants."
prereqs: [least-squares-problem, additive-white-gaussian-noise-channel, tapped-delay-line-channel-model]
see_also: [least-squares-channel-estimation, lmmse-channel-estimation, pilot-symbol-assisted-modulation, sparse-channel-estimation, comb-pilot-channel-estimation, kalman-channel-tracking, blind-equalization, cramer-rao-bound]
sources:
  - book: isbn:9780133457117
    title: "Steven M. Kay, Fundamentals of Statistical Signal Processing, Volume I: Estimation Theory, Prentice Hall, 1993"
    locator: "Chapter 4 (the linear model), Chapter 12 (linear Bayesian estimators) and Chapter 15 (extensions for complex data)"
  - paper: doi:10.1109/TSP.2005.863008
    title: "Mehrzad Biguesh and Alex B. Gershman, Training-based MIMO channel estimation: a study of estimator tradeoffs and optimal training signals, IEEE Transactions on Signal Processing 54(3), 2006, pages 884 to 893"
    locator: "the LS and LMMSE estimators and the optimal training signals"
  - paper: doi:10.1109/25.108378
    title: "James K. Cavers, An analysis of pilot symbol assisted modulation for Rayleigh fading channels, IEEE Transactions on Vehicular Technology 40(4), 1991, pages 686 to 693"
    locator: "channel estimation from pilots inserted in the data and interpolation between them"
---

Channel estimation is the problem of finding the response of a communication channel from what the receiver sees. The transmitter sends known symbols, called pilots or a training sequence, and the receiver compares what it receives with what it knows was sent. For a channel with $L$ taps, the received pilot samples are $y = X h + w$, a linear model in the unknown taps $h$, with a matrix $X$ built from the pilots and noise $w$. The error measure is the mean squared error $E\|\hat h - h\|^2$. Two answers cover most uses: [least squares](/least-squares-channel-estimation/), which needs no knowledge of the channel statistics, and [LMMSE estimation](/lmmse-channel-estimation/), which uses the channel covariance and the noise level to do better. The estimate feeds the equalizer, the coherent detector and the precoder. The alias "channel identification" is also the name of the same task in [system identification](/system-identification/); there the input is chosen freely, and here it is a pilot pattern that costs data rate.

## In plain words

A radio channel changes the signal: it delays it, scales it, and adds echoes. To undo this, the receiver must know what the channel did. So the sender puts symbols that the receiver already knows into the stream. The receiver sees how these known symbols arrived and works out the channel from them. Noise makes this a guess, not an exact answer, and more known symbols make the guess better but leave less room for data. If the receiver also knows how strong the echoes usually are and how loud the noise is, it can use that knowledge to make a better guess. When the channel changes over time, the known symbols must come often enough to follow it.

## Definition

**Input.** A pilot matrix $X \in \mathbb{C}^{m \times L}$ and the received vector $y = X h + w \in \mathbb{C}^m$, where $h \in \mathbb{C}^L$ is the unknown channel and $w \sim \mathcal{CN}(0, N_0 I)$. For an FIR channel and a training sequence $x[0], \ldots, x[m + L - 2]$, row $i$ of $X$ is $(x[i + L - 1], x[i + L - 2], \ldots, x[i])$, the samples that are in the channel memory at time $i + L - 1$. In the Bayesian form of the problem, $h$ is random with mean zero and covariance $R_h$, independent of $w$.

**Output.** An estimate $\hat h = \hat h(y)$.

**Goal.** In the deterministic form, an unbiased estimate with the smallest covariance. In the Bayesian form, the smallest mean squared error $E\|\hat h - h\|^2$, averaged over the channel and the noise. The design of $X$, the pilot pattern, is part of the problem when the system can choose it.

**Identifiability.** The channel is determined by noiseless pilots if and only if $X$ has full column rank $L$. This needs $m \ge L$ observations and a pilot sequence rich enough; a constant sequence, for example, cannot separate the taps.

## Variants

- **Time domain, single carrier.** The FIR model above, with a training sequence in each burst, as in GSM.
- **Frequency domain, OFDM.** With a [cyclic prefix](/cyclic-prefix/), each subcarrier sees $Y_k = X_k H_k + W_k$, and the problem is to estimate $H_k$ on all subcarriers from pilots on some of them; see [comb pilot channel estimation](/comb-pilot-channel-estimation/), [DFT-based channel estimation](/dft-based-channel-estimation/) and [two-dimensional Wiener pilot interpolation](/two-dimensional-wiener-pilot-interpolation/).
- **Time-varying channels.** The channel changes from symbol to symbol, and pilots inserted at a fixed rate are interpolated, as in [pilot symbol assisted modulation](/pilot-symbol-assisted-modulation/), or the channel is tracked with a state model, as in [Kalman channel tracking](/kalman-channel-tracking/).
- **MIMO.** $Y = H X + W$ with a matrix channel; orthogonal pilots from the transmit antennas keep the estimates separate. In multi-cell systems, reused pilots cause [pilot contamination](/pilot-contamination/).
- **Sparse channels.** Only a few of many taps are nonzero, and [sparse channel estimation](/sparse-channel-estimation/) uses [compressed sensing](/compressed-sensing/) to need fewer pilots.
- **Blind and semi-blind.** No pilots, or few: the channel is found from the statistics of the data, as in [blind equalization](/blind-equalization/) and [subspace channel identification](/subspace-channel-identification/). Decision-directed estimation uses detected data as extra pilots.

## Examples

**A small LS estimate.** Let $L = 2$, the pilots $x = (1, -1, 1, 1)$ and the true channel $h = (1, 0.5)$. The rows are $(x[1], x[0]) = (-1, 1)$, $(x[2], x[1]) = (1, -1)$ and $(x[3], x[2]) = (1, 1)$, so

$$X = \begin{pmatrix} -1 & 1 \\ 1 & -1 \\ 1 & 1 \end{pmatrix}, \qquad X^H X = \begin{pmatrix} 3 & -1 \\ -1 & 3 \end{pmatrix}, \qquad (X^H X)^{-1} = \frac{1}{8} \begin{pmatrix} 3 & 1 \\ 1 & 3 \end{pmatrix}.$$

Without noise, $y = X h = (-0.5, 0.5, 1.5)$, and $\hat h = (X^H X)^{-1} X^H y = (1, 0.5)$, the true taps. With noise, the LS error is $N_0\, \mathrm{tr}((X^H X)^{-1}) = 0.75\, N_0$. Three orthogonal pilot rows of the same energy would give $X^H X = 3I$ and the error $2N_0/3$, which is the best possible for this energy.

**LMMSE with a prior.** Let the taps be independent with variances $R_h = \mathrm{diag}(1, 0.25)$ and $N_0 = 0.1$. The LMMSE error covariance is $(R_h^{-1} + X^H X/N_0)^{-1}$. Here $R_h^{-1} + X^H X / N_0 = \begin{pmatrix} 31 & -10 \\ -10 & 34 \end{pmatrix}$, with determinant 954, so the error is $(34 + 31)/954 = 0.0681$, against $0.075$ for LS.

**Non-example.** With the pilots $x = (1, 1, 1, 1)$, every row of $X$ is $(1, 1)$, so $X$ has rank 1 and only $h_0 + h_1$ can be estimated. No estimator can separate the two taps.

## Known algorithms

- **[Least squares](/least-squares-channel-estimation/).** $\hat h = (X^H X)^{-1} X^H y$, unbiased, with the error $N_0\, \mathrm{tr}((X^H X)^{-1})$. $O(m L^2 + L^3)$ per pilot block, or $O(m L)$ if $X^H X$ is fixed and factored once.
- **[LMMSE](/lmmse-channel-estimation/).** $\hat h = R_h X^H (X R_h X^H + N_0 I)^{-1} y$, the [Wiener filter](/wiener-filter/) for the channel. It needs $R_h$ and $N_0$.
- **Pilot interpolation.** [PSAM](/pilot-symbol-assisted-modulation/) in time, [comb pilots](/comb-pilot-channel-estimation/) in frequency, [2D Wiener interpolation](/two-dimensional-wiener-pilot-interpolation/) in both, and the [DFT-based estimator](/dft-based-channel-estimation/), which denoises an OFDM LS estimate by keeping only the first taps in the time domain.
- **Tracking.** [Kalman channel tracking](/kalman-channel-tracking/) with an [autoregressive model](/autoregressive-model/) of the fading, and the [LMS](/lms-algorithm/) and [RLS](/rls-algorithm/) algorithms for slowly varying channels.
- **Sparse recovery.** [Orthogonal matching pursuit](/orthogonal-matching-pursuit/) and [basis pursuit](/basis-pursuit/) on the same linear model; see [sparse channel estimation](/sparse-channel-estimation/).
- **Blind methods.** [Subspace identification](/subspace-channel-identification/) and the [Tong-Xu-Kailath method](/tong-xu-kailath-identification/) from second-order statistics of oversampled data.

## Bounds

**Cramer-Rao bound.** For a deterministic $h$ and Gaussian noise, every unbiased estimator has the covariance at least $N_0 (X^H X)^{-1}$, in the order of positive semidefinite matrices; see the [Cramer-Rao bound](/cramer-rao-bound/). LS attains it, so it is efficient, and its error $N_0\, \mathrm{tr}((X^H X)^{-1})$ is the smallest among unbiased estimators.

**Pilot design.** For pilots of total energy $\mathrm{tr}(X^H X) = E$, $\mathrm{tr}((X^H X)^{-1}) \ge L^2 / E$, with equality if and only if $X^H X = (E/L) I$. So orthogonal training is optimal for LS, and the best LS error is $N_0 L^2 / E$: it grows with the square of the number of taps for a fixed pilot energy.

**Bayesian bound.** If $h \sim \mathcal{CN}(0, R_h)$, the LMMSE estimate is the conditional mean, so its error $\mathrm{tr}((R_h^{-1} + X^H X / N_0)^{-1})$ is the minimum over all estimators, linear or not. It is always at most the LS error, and it tends to it as $N_0 \to 0$.

**Pilot rate.** A channel that changes in time with Doppler spread $f_D$ must be sampled by pilots at least at the Nyquist rate of the fading, at most $1/(2 f_D T)$ symbols apart, as in PSAM.

## Reductions

- **Channel estimation is linear regression.** The pilot model $y = X h + w$ is a [least squares problem](/least-squares-problem/), and the Bayesian form is [ridge regression](/ridge-regression/) with a general prior covariance. Every tool of [linear regression](/linear-regression/) applies.
- **To Wiener filtering.** The LMMSE estimate is the Wiener filter for the vector $h$ from $y$; the [MMSE linear equalizer](/mmse-linear-equalizer/) solves the same kind of equation for the symbols.
- **OFDM to many scalar problems.** With a cyclic prefix, the DFT turns the FIR model into one scalar model per subcarrier, plus the knowledge that $H_k$ is the DFT of a short impulse response.
- **Sparse channels to compressed sensing.** With few nonzero taps, the problem is a sparse recovery problem with the measurement matrix $X$.

## Applications

The estimate is used by the [channel equalization](/channel-equalization/) step (the ZF, MMSE and Viterbi equalizers all need $h$), by coherent detection on a fading channel, by the one-tap equalizers of [OFDM](/orthogonal-frequency-division-multiplexing/), by MIMO detectors and precoders, and by link adaptation, which picks a rate from the estimated SNR. Cellular standards carry dedicated pilots for this: training sequences in GSM bursts and reference signals in LTE and 5G grids. In [massive MIMO](/massive-mimo/), the base station estimates the uplink channels from pilots and uses them for the downlink by reciprocity.

## References
