---
tag: WXMG9W
kind: algorithm
slug: delay-locked-loop
name: Delay-locked loop
aliases:
- DLL
- code tracking loop
area: communications/multiple-access-and-spread-spectrum
level: core
summary: "Tracks the code delay of a spread-spectrum signal after acquisition. Early and late correlators give an error signal that is zero at the true delay, and a loop moves the local code replica."
model: real-ram
complexity:
  vars: {B: the number of blocks, M: the number of samples per block}
  time: {worst: Θ(B M)}
  space: {extra: Θ(1)}
properties: {deterministic: true, noncoherent: true, needs_acquisition: true, first_order_loop: true}
history:
  year: 1961
  people: [James J. Spilker Jr., D. T. Magill]
  note: Spilker and Magill presented the delay-lock discriminator in 1961, a feedback loop that tracks the delay of a received signal by correlation with delayed copies of a reference.
prereqs: [direct-sequence-spread-spectrum, maximal-length-sequence, autocorrelation, phase-locked-loop]
see_also: [early-late-gate-synchronizer, serial-search-code-acquisition, parallel-code-phase-search, symbol-timing-recovery, rake-receiver, kalman-filter, cramer-rao-bound, processing-gain]
sources:
  - paper: doi:10.1109/JRPROC.1961.287899
    title: J. J. Spilker, Jr. and D. T. Magill, The delay-lock discriminator, an optimum tracking device, Proceedings of the IRE 49(9), 1961
    locator: pp. 1403 to 1416
  - book: isbn:9780817643904
    title: Kai Borre, Dennis M. Akos, Nicolaj Bertelsen, Peter Rinder and Søren Holdt Jensen, A Software-Defined GPS and Galileo Receiver, Birkhäuser, 2007
    locator: Section 7.5, p. 96 (code tracking with early, prompt and late replicas half a chip apart); Table 7.2, p. 99 (the DLL discriminators)
---

A delay-locked loop (DLL) keeps the local copy of a spreading code aligned with the received code once [acquisition](/serial-search-code-acquisition/) has found the delay to within about half a chip. It computes two correlations, one with the replica a little **early** and one a little **late**. When the replica is aligned, the two have the same size. When the received code is later than the replica, the late correlation is larger, and the loop moves the replica later; when it is earlier, the loop moves it earlier. The difference of the two, normalized, is the **discriminator**, and its plot against the delay error is the **S-curve**. The DLL does for the code what a [phase-locked loop](/phase-locked-loop/) does for the carrier. A third, **prompt** correlator at the estimated delay gives the despread data and the carrier phase. The same early-late idea for symbol timing is the [early-late gate synchronizer](/early-late-gate-synchronizer/).

## In plain words

After the receiver has found roughly where the code starts, the signal keeps drifting, because the transmitter and the receiver move and their clocks differ. The receiver must follow the drift.

It listens with two copies of the code, one slightly ahead of its best guess and one slightly behind it. If the guess is right, both copies match the signal equally well. If the copy behind matches better, the true signal is later than the guess, so the receiver moves its guess later. If the copy ahead matches better, it moves the guess earlier.

It repeats this for each new piece of the signal. Each step moves the guess only part of the way, so that noise does not throw it around.

## The problem

The received signal is $A e^{j\phi} c(t - \tau_k) + w(t)$, where $c(t)$ is the code waveform with rectangular chips, time is in chips, the delay $\tau_k$ changes slowly from block to block, and the amplitude $A$ and the carrier phase $\phi$ are unknown. An initial estimate $\hat\tau_0$ with $|\tau_0 - \hat\tau_0|$ less than about half a chip comes from acquisition. The task is to produce estimates $\hat\tau_k$ that follow $\tau_k$, block by block, with small error.

## The algorithm

```pseudo id=main
DLL(blocks r_1, r_2, …, code c, τ̂_0, δ, g, k_d)
L1  τ̂ ← τ̂_0
L2  for each block r do
L3      E ← ⟨c(· - τ̂ + δ), r⟩;  L ← ⟨c(· - τ̂ - δ), r⟩    ▷ early and late correlators
L4      D ← (|L| - |E|) / (|L| + |E|)                      ▷ normalized early minus late envelope
L5      τ̂ ← τ̂ + g · D / k_d                              ▷ loop gain g, S-curve slope k_d
L6  return the estimates τ̂ after each block
```

Here $E$ is the correlation with the code delayed by $\hat\tau - \delta$ and $L$ with the code delayed by $\hat\tau + \delta$, so $E = A e^{j\phi} R(\varepsilon + \delta)$ and $L = A e^{j\phi} R(\varepsilon - \delta)$, where $\varepsilon = \tau - \hat\tau$ is the delay error and $R$ is the [autocorrelation](/autocorrelation/) of the code waveform. For an [m-sequence](/maximal-length-sequence/) of length $N$ with rectangular chips, $R(x) = 1 - |x|(N + 1)/N$ for $|x| \le 1$ and $-1/N$ beyond. The envelopes $|E|$ and $|L|$ do not depend on the carrier phase, so the loop works before the carrier is locked. The amplitude $A$ cancels in the ratio, so the loop gain does not depend on the signal level. Near lock, the S-curve is the line
$$D(\varepsilon) = k_d\, \varepsilon, \qquad k_d = \frac{N + 1}{N - (N + 1)\delta},$$
for $|\varepsilon| \le \min(\delta, N/(N + 1) - \delta)$. With $D/k_d = \varepsilon$, the update L5 is a first-order loop: $\varepsilon \leftarrow (1 - g)\, \varepsilon$.

## Example

**S-curve.** For the GPS C/A code, $N = 1023$, with $\delta = 1/2$ chip, the slope is $k_d = 2.0039$.

| $\varepsilon$ (chips) | 0 | 0.1 | 0.25 | 0.4 | 0.5 | 0.75 | 1.0 | 1.25 | 1.5 |
|---|---|---|---|---|---|---|---|---|---|
| $D(\varepsilon)$ | 0 | 0.2004 | 0.5010 | 0.8016 | 0.9980 | 0.9974 | 0.9961 | 0.9922 | 0 |

The curve is linear up to about half a chip, then stays near $1$, and drops to $0$ at $1.5$ chips, where both correlators see only the floor $1/N$. The output is odd: $D(-\varepsilon) = -D(\varepsilon)$. At lock, each correlator is half a chip from the peak and sees $R(1/2) = 0.4995$ of the peak amplitude, $6.03$ dB less than the prompt correlator.

**Pull-in.** Without noise and with $g = 1/2$, an initial error of $0.3$ chip becomes $0.15$, $0.075$, $0.0375$ and $0.01875$ chip after four blocks: the error halves at each block.

**Jitter.** For a code of length $N = 31$ sampled 127 times per period with noise variance $2$ per sample, the discriminator noise $D/k_d$ at zero error has a standard deviation of $0.0605$ chip. With $g = 0.2$, the linear theory $\sigma_\varepsilon^2 = g\sigma_v^2/(2 - g)$ gives $0.0202$ chip, and a simulation of the loop gives $0.0203$ chip.

**Drift.** If the delay grows by $0.004$ chip per block, a first-order loop with $g = 0.2$ follows it with a constant lag of $0.004/0.2 = 0.02$ chip.

## Correctness

The correlation of the code with a shifted copy of itself is $(1 - f)\rho(i) + f\rho(i + 1)$ for a shift $i + f$, where $\rho$ is the periodic autocorrelation of the chip sequence. This gives the triangle $R$ above. Inside the linear region both lags $\delta \pm \varepsilon$ fall on the rising part of the triangle, so $|L| - |E| = 2a\varepsilon$ and $|L| + |E| = 2(1 - a\delta)$ with $a = (N + 1)/N$, and $D = k_d \varepsilon$. Then L5 gives $\varepsilon_{k+1} = (1 - g)\varepsilon_k$, which goes to zero for $0 < g < 2$. Outside the linear region, a case analysis on the triangle shows that $D$ still has the sign of $\varepsilon$ for $0 < |\varepsilon| < \delta + (N - 1)/(N + 1)$, so the loop moves the right way. With independent noise $v_k$ per block, $\varepsilon_{k+1} = (1 - g)\varepsilon_k - g v_k$ has the stationary variance $g\sigma_v^2/(2 - g)$. The full proof is in the proofs folder.

## Complexity

In the [real RAM](/real-ram/) model, each block of $M$ samples costs two correlations of $M$ multiply-adds (L3) and a constant number of further operations (L4 and L5). Over $B$ blocks the cost is $\Theta(B M)$, with $\Theta(1)$ extra space. The prompt correlator, which every receiver also needs for the data, adds one more correlation per block.

## Properties

- **Odd S-curve with a stable zero.** $D(0) = 0$ and $D$ has the sign of $\varepsilon$ in the pull-in range, so the true delay is the only stable point near lock.
- **Carrier independent.** The envelope discriminator uses $|E|$ and $|L|$, so the carrier phase and small frequency errors do not affect it.
- **Normalized gain.** Dividing by $|L| + |E|$ removes the amplitude. Without the division, the loop gain changes with the signal level.
- **Bandwidth and noise.** The loop gain $g$ trades the speed of response against the jitter $g\sigma_v^2/(2 - g)$. A smaller $g$ gives less noise but a larger lag under drift.
- **Lag under drift.** A first-order loop follows a delay that changes at a constant rate with a constant error $v/g$. A second-order loop follows it with zero steady error.

## Variants and improvements

- **Other discriminators.** Borre and coauthors list the coherent $I_E - I_L$, the early minus late power $|E|^2 - |L|^2$, the normalized envelope used here, and the dot product of early minus late with prompt. The coherent form needs a locked carrier and has lower noise.
- **Narrow correlator.** A smaller spacing $\delta$, such as $0.1$ chip, lowers the noise and the error from multipath, since only reflections less than about $1 + \delta$ chips late move the zero of the S-curve. It needs a wide receiver bandwidth.
- **Carrier aiding.** The carrier loop measures the Doppler shift much more precisely than the code loop. Scaling it by the ratio of the chip rate to the carrier frequency and adding it to the code rate removes most of the drift, so the DLL can use a small gain.
- **Higher-order loop filters.** A loop filter with an integrator, as in a phase-locked loop, removes the lag under a constant drift.
- **Kalman tracking.** A [Kalman filter](/kalman-filter/) with a state of delay and delay rate can replace the fixed loop filter, with gains matched to the noise and the dynamics.

## When to use it

Use a DLL in every direct-sequence receiver after acquisition, to keep the code aligned while the delay changes. GNSS receivers use it for every satellite, together with a carrier loop. CDMA receivers use one per [rake finger](/rake-receiver/). The DLL needs an initial error inside the pull-in range, so it cannot replace acquisition, and when it loses lock the receiver must search again.

## Pitfalls

- **Starting too far away.** If the initial error is larger than about $1 + \delta$ chips, both correlators see only the floor, $D = 0$, and the loop does not move.
- **Wrong slope.** The update divides by $k_d$, which depends on $\delta$ and on the shape of the correlation. A band-limited receiver rounds the triangle and lowers the slope. A wrong $k_d$ changes the effective loop gain.
- **Multipath bias.** A reflected copy that arrives less than about $1 + \delta$ chips after the direct one changes the shape of the correlation, and the zero of the S-curve moves away from the true delay.
- **Gain too large.** For $g \ge 2$ the linear loop is unstable. Even for $g$ near $1$, the jitter is large, because the loop uses only the latest block.
- **Envelope at low SNR.** At low signal-to-noise ratio, noise biases $|E|$ and $|L|$ upward and flattens the S-curve, so the actual gain is lower than the design value.

## Implementations

## History

James Spilker and D. T. Magill presented the delay-lock discriminator in the Proceedings of the IRE in 1961, as a feedback loop that tracks the delay of a received signal by correlating it with delayed copies of a reference. With the development of spread-spectrum ranging and of GPS, the early-late code tracking loop became a standard part of direct-sequence and satellite navigation receivers; Borre and coauthors describe its form in a software GPS receiver.

## References
