---
tag: 43NN0S
kind: algorithm
slug: jakes-fading-simulator
name: Jakes fading simulator
aliases:
- Jakes model
- sum-of-sinusoids fading simulator
area: communications/fading-channels
level: core
summary: "Generates a fading waveform for Clarke's model as a fixed sum of M + 1 sinusoids. It is cheap and smooth, but deterministic and not stationary, and its correlation leaves J0 at large lags."
model: real-ram
complexity:
  vars: {M: the number of oscillators minus one, T: the number of output samples}
  time: {worst: O(M T)}
  space: {extra: O(M)}
properties: {deterministic: true, wide_sense_stationary: false, exact_clarke_statistics: false, kind_of_claim: heuristic}
history:
  year: 1974
  people: [William C. Jakes]
  note: "Jakes described the simulator with N = 4M + 2 equally spaced plane waves, reduced by symmetry to M + 1 low-frequency oscillators, in the Bell Labs book Microwave Mobile Communications."
prereqs: [clarke-model, rayleigh-fading-channel, doppler-spread]
see_also: [clarke-model, zheng-xiao-fading-simulator, filtered-gaussian-fading-simulator, level-crossing-rate, coherence-time, walsh-hadamard-transform, trapezoidal-rule, rayleigh-fading-channel]
sources:
  - book: isbn:9780780310698
    title: "William C. Jakes (editor), Microwave Mobile Communications, Wiley, 1974; reissued by IEEE Press, 1994"
    locator: Chapter 1 (the laboratory simulation of multipath fading with equally spaced oscillators)
  - paper: doi:10.1109/26.917776
    title: "M. F. Pop and N. C. Beaulieu, Limitations of sum-of-sinusoids fading channel simulators, IEEE Transactions on Communications 49(4), 2001, pages 699 to 708"
    locator: "the proof that the Jakes simulator is not wide-sense stationary, and the variant with random oscillator phases"
  - paper: doi:10.1109/TCOMM.2003.813259
    title: "Y. R. Zheng and C. Xiao, Simulation models with correct statistical properties for Rayleigh fading channels, IEEE Transactions on Communications 51(6), 2003, pages 920 to 928"
    locator: "eqs. (6) and (7) (the Jakes simulator in the form used here) and its statistics against Clarke's model"
  - paper: doi:10.1049/el:19930777
    title: "P. Dent, G. E. Bottomley and T. Croft, Jakes fading model revisited, Electronics Letters 29(13), 1993, pages 1162 to 1163"
    locator: "the variant with Walsh-Hadamard weights for several uncorrelated waveforms"
---

The Jakes simulator is a deterministic generator of a complex fading gain $h(t)$ that approximates [Clarke's model](/clarke-model/): it adds $M + 1$ sinusoids whose frequencies are the Doppler shifts $f_D \cos(2\pi n/N)$ of $N = 4M + 2$ plane waves at equally spaced angles. Clarke's model is the target statistics, the autocorrelation $\Omega J_0(2\pi f_D \tau)$ and the U-shaped Doppler spectrum; this page is about one way to produce a waveform with those statistics. The [Zheng-Xiao simulator](/zheng-xiao-fading-simulator/) adds random angles and phases and gets the second-order statistics exactly, and the [filtered Gaussian noise simulator](/filtered-gaussian-fading-simulator/) shapes Gaussian noise with the spectrum instead of adding sinusoids. The Jakes simulator is a heuristic: it is smooth and cheap, but one run is a fixed function of time, not a random process with the statistics of Clarke's model.

## In plain words

A receiver moving through a city gets the same signal along many paths. Each path arrives from its own direction, so the motion shifts its frequency by a different amount, and the paths add up to a gain that rises and falls in time. Jakes imagined a ring of equally spaced paths around the receiver. By symmetry, many of them have the same frequency shift, so only a few oscillators are needed. Each oscillator is a cosine at one Doppler shift, and fixed weights spread the oscillators over the real and imaginary parts of the gain. The sum fades in a way that looks like real fading over short times. But nothing in it is random: every run starts with the same high peak and gives the same waveform.

## The problem

The input is the maximum Doppler shift $f_D$ in Hz, the mean power $\Omega$, the number of oscillators $M + 1$, and a list of $T$ times $t$. The output is the gain $h(t) = h_c(t) + j h_s(t)$ at each time. The goal is that the time-average power is $\Omega$ and that the time-average autocorrelation $\langle h(t + \tau)\, \overline{h(t)} \rangle$ is close to $\Omega J_0(2\pi f_D \tau)$, the autocorrelation of Clarke's model. The model is flat fading that varies in time (time-correlated fading); the simulator produces the channel only and says nothing about CSIR or CSIT.

## The algorithm

```pseudo id=main
JAKES(M, f_D, Ω, t)
L1  N ← 4M + 2
L2  ν₀ ← 1;  νₙ ← cos(2πn/N)  for n = 1 .. M            ▷ ωₙ = 2π f_D νₙ
L3  β₀ ← π/4;  βₙ ← πn/M  for n = 1 .. M
L4  a₀ ← √2 cos β₀, b₀ ← √2 sin β₀;  aₙ ← 2 cos βₙ, bₙ ← 2 sin βₙ
L5  c ← Σ_{n=0}^{M} aₙ cos(ωₙ t)
L6  s ← Σ_{n=0}^{M} bₙ cos(ωₙ t)
L7  return √(2Ω/N) (c + j s)
```

Line L1 fixes the number of plane waves. The wave at angle $2\pi n/N$ has the Doppler shift $f_D \cos(2\pi n/N)$. Because $N/2$ is odd, the waves at angles $\pm 2\pi n/N$ and $\pi \pm 2\pi n/N$ give the same cosine up to sign, so the $N$ waves fold into the $M$ oscillators of line L2 plus the oscillator at $f_D$ itself. Lines L3 and L4 are the gains of Jakes, in the form of eqs. (6) and (7) of Zheng and Xiao (2003). The angles $\beta_n$ are chosen so that the two quadratures $c$ and $s$ have equal power: $\sum a_n^2 = \sum b_n^2 = N/2$ for $M \ge 2$. Lines L5 and L6 add the oscillators, and line L7 scales the sum so that the time-average power is $\Omega$.

## Example

Take $M = 8$, so $N = 34$, and $f_D = 1$. The normalized frequencies $\nu_n$ are 1, 0.983, 0.9325, 0.8502, 0.739, 0.6026, 0.4457, 0.2737 and 0.0923. The gains are $a = (1, 1.848, 1.414, 0.765, 0, -0.765, -1.414, -1.848, -2)$ and $b = (1, 0.765, 1.414, 1.848, 2, 1.848, 1.414, 0.765, 0)$.

The time-average autocorrelation of the output, divided by $\Omega$, is

$$R(\tau) = \frac{2}{N}\Big[\cos x + 2\sum_{n=1}^{M} \cos(x \nu_n)\Big], \qquad x = 2\pi f_D \tau .$$

| $f_D \tau$ | 0.1 | 0.25 | 0.5 | 1 | 2 | 3 | 5 | 10 |
|---|---|---|---|---|---|---|---|---|
| $J_0(2\pi f_D\tau)$ | 0.90371 | 0.47200 | -0.30424 | 0.22028 | 0.15751 | 0.12906 | 0.10025 | 0.07103 |
| Jakes, $R(\tau)$ | 0.90371 | 0.47200 | -0.30424 | 0.22028 | 0.15751 | 0.12906 | -0.00301 | -0.04948 |

Up to $f_D\tau = 3$ the two agree to five digits. The first lag where they differ by more than 0.01 is $f_D \tau = 4.4$, and at $f_D\tau = 5$ the simulator has lost the correlation completely. With $M = 4$ the same error appears at $f_D \tau = 2.04$, and with $M = 16$ at $9.28$.

The quadratures are worse. At $f_D\tau = 0.38274$, the first zero of $J_0$, each of $h_c$ and $h_s$ should have zero correlation with itself and with the other. The simulator gives 0.173 for $h_c$, -0.173 for $h_s$ and -0.346 between them. Even at $\tau = 0$ the quadratures are correlated, with coefficient $2/N = 0.059$.

At $t = 0$ every cosine equals 1, so $|h(0)|^2/\Omega = (2/N)[(\sum a_n)^2 + (\sum b_n)^2]$. Here $\sum a_n = -1$ and $\sum b_n = 1 + 2\cot(\pi/16) = 11.055$, so $|h(0)|^2 = 7.25\,\Omega$, a peak that a Rayleigh gain reaches with probability $e^{-7.25} = 7 \cdot 10^{-4}$. Every run starts with it.

## Correctness

**Claim.** The time-average power of the output is $\Omega$, and its time-average autocorrelation is $R(\tau)$ above. $R$ is the $N$-point trapezoid rule for $J_0$, and $R(\tau) = J_0(x) + 2\sum_{m \ge 1} (-1)^m J_{mN}(x)$ exactly. So the error is small while $x = 2\pi f_D \tau$ is well below $N$.

**Key step.** For distinct frequencies the time average of $\cos(\omega_n t)\cos(\omega_k (t + \tau))$ is $\frac12 \cos(\omega_n \tau)$ if $n = k$ and 0 otherwise, and $a_n^2 + b_n^2$ is 2 for $n = 0$ and 4 otherwise. By the Jacobi-Anger expansion, $\cos(x \cos\theta)$ is $J_0(x)$ plus harmonics $\cos(2k\theta)$ with weights $2(-1)^k J_{2k}(x)$. The average over $N$ equally spaced angles keeps only the harmonics that are multiples of $N$, and the folding of line L2 turns that average into $R$. The full proof is in the proofs folder. It also shows why the simulator is not wide-sense stationary: nothing in it is random, so the only "expectation" of $h(t+\tau)\overline{h(t)}$ is the product itself, and that product depends on $t$.

## Complexity

Lines L1 to L4 cost $O(M)$ once. Each output sample costs $M + 1$ cosines and $2(M + 1)$ multiplications, so $T$ samples cost $O(M T)$ in the [real RAM](/real-ram/), with $O(M)$ extra space. In hardware, each oscillator is a phase accumulator and a table lookup, which is why the method was popular for fading hardware.

## Properties

- **Not random.** One run is a fixed function of time. Averages over a run converge to the values above, but there is no ensemble to average over, and the run is not wide-sense stationary (Pop and Beaulieu 2001).
- **Second-order statistics.** The complex autocorrelation matches $J_0$ for small lags only. The quadrature autocorrelations and the cross-correlation do not match Clarke's model at any $M$.
- **Higher-order statistics.** The envelope is not exactly Rayleigh, and the level crossing rate and the fade durations are only close to those of [Clarke's model](/level-crossing-rate/) for large $M$.
- **Smooth output.** Unlike a filtered noise generator, it can be evaluated at any real time, and the waveform has no edge effects or periodic wrap.
- **Equal power in each quadrature.** The choice of $\beta_n$ gives $\sum a_n^2 = \sum b_n^2$, which is the purpose of line L3.

## Variants and improvements

- **Random phases.** Pop and Beaulieu add a random phase $\phi_n$ to each oscillator. Over the random phases, the process is wide-sense stationary with the autocorrelation $R(\tau)$, but its higher-order statistics remain wrong.
- **Several uncorrelated waveforms.** Jakes shifted the angles $\beta_n$ for each waveform to get several fading gains from one set of oscillators, but these waveforms are not uncorrelated. Dent, Bottomley and Croft (1993) take the gains from the rows of a Walsh-Hadamard matrix, as in the [Walsh-Hadamard transform](/walsh-hadamard-transform/), and change the arrival angles, so that the waveforms are uncorrelated.
- **Random angles.** The [Zheng-Xiao simulator](/zheng-xiao-fading-simulator/) draws the arrival angles and phases at random. Its second-order statistics equal those of Clarke's model exactly, for any $M$.
- **Filtered noise.** The [filtered Gaussian noise simulator](/filtered-gaussian-fading-simulator/) gives a Gaussian process with a spectrum close to Clarke's, at the cost of a block length fixed in advance.

## When to use it

Use the Jakes simulator for a quick, smooth fading waveform, to look at fades or to drive hardware, when exact statistics are not important. Do not use it for Monte Carlo estimates of error rates or outage, which average over many independent channels: one run has no randomness, and runs that differ only in the start time are strongly dependent. For those, use the Zheng-Xiao simulator with a new draw per channel, or the filtered Gaussian noise simulator.

## Pitfalls

- **Calling it Clarke's model.** The name "Jakes model" is used both for this generator and for the spectrum of Clarke's model. The spectrum is exact physics under its assumptions; the generator is an approximation.
- **Averaging over runs.** Running the simulator twice gives the same waveform. Shifting the start time gives different numbers, but not independent channels.
- **The peak at $t = 0$.** Every run starts with $|h|^2 = 7.25\,\Omega$ for $M = 8$. Discard the start, or use random phases.
- **Long records.** For $2\pi f_D \tau$ near $N$ the correlation is wrong, and the waveform is almost periodic. Long simulations need larger $M$.
- **Quadrature statistics.** Code that uses $h_c$ and $h_s$ as two independent real Gaussian processes, for example for two branches of a diversity system, gets correlated branches.

## Implementations

## History

Jakes and his colleagues at Bell Labs built fading simulators from banks of oscillators in the early 1970s, and the 1974 book Microwave Mobile Communications, which Jakes edited, gave the design with $N = 4M + 2$ waves and $M + 1$ oscillators. It became the standard way to simulate fading for two decades. Dent, Bottomley and Croft (1993) changed the gains to produce several uncorrelated waveforms. Pop and Beaulieu (2001) showed that the simulator and its variants are not wide-sense stationary and proposed random phases. Zheng and Xiao (2002, 2003) then gave statistical sum-of-sinusoids models with random angles, whose second-order statistics match Clarke's model.

## References
