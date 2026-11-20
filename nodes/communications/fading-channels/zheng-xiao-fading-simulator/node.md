---
tag: 97VH88
kind: algorithm
slug: zheng-xiao-fading-simulator
name: Zheng and Xiao fading simulator
aliases:
- improved sum-of-sinusoids simulator
area: communications/fading-channels
level: advanced
summary: "A sum of M sinusoids with random arrival angles and phases. Its autocorrelation is exactly Omega J0(2 pi f_D tau) for any M; a phase per sinusoid also fixes the higher-order statistics."
model: real-ram
complexity:
  vars: {M: the number of sinusoids, T: the number of output samples}
  time: {worst: O(M T)}
  space: {extra: O(M)}
properties: {randomized: true, wide_sense_stationary: true, exact_second_order_statistics: true, gaussian_only_as_m_grows: true}
history:
  year: 2002
  people: [Yahong Rosa Zheng, Chengshan Xiao]
  note: "Xiao and Zheng gave the model at a 2002 conference, and Zheng and Xiao proved its statistics in 2003. In 2006, Xiao, Zheng and Beaulieu replaced the common phase by one phase per sinusoid, after the 2003 form was shown to be non-Gaussian over short times."
prereqs: [clarke-model, jakes-fading-simulator]
see_also: [clarke-model, jakes-fading-simulator, filtered-gaussian-fading-simulator, rayleigh-fading-channel, level-crossing-rate, central-limit-theorem, monte-carlo-integration, rician-fading-channel]
sources:
  - paper: doi:10.1109/TCOMM.2003.813259
    title: "Y. R. Zheng and C. Xiao, Simulation models with correct statistical properties for Rayleigh fading channels, IEEE Transactions on Communications 51(6), 2003, pages 920 to 928"
    locator: "Section III, eqs. (14) and (15) (the model) and Theorem 1 (its autocorrelation and cross-correlation functions)"
  - paper: doi:10.1109/TWC.2006.05068
    title: "C. Xiao, Y. R. Zheng and N. C. Beaulieu, Novel sum-of-sinusoids simulation models for Rayleigh and Rician fading channels, IEEE Transactions on Wireless Communications 5(12), 2006, pages 3667 to 3679"
    locator: "Section II (the remark that corrects eq. (14) of the 2003 paper with one phase per sinusoid, and Theorem 3) and Section III (the Rician model)"
  - paper: doi:10.1109/26.917776
    title: "M. F. Pop and N. C. Beaulieu, Limitations of sum-of-sinusoids fading channel simulators, IEEE Transactions on Communications 49(4), 2001, pages 699 to 708"
    locator: "the statistics of the Jakes simulator that the random model corrects"
---

The Zheng-Xiao simulator is a random generator of a fading gain $h(t)$ for [Clarke's model](/clarke-model/): it adds $M$ sinusoids whose arrival angles, gains and phases are drawn at random, once per channel. Clarke's model is the target, the autocorrelation $\Omega J_0(2\pi f_D\tau)$; the [Jakes simulator](/jakes-fading-simulator/) approximates it with fixed angles and is deterministic, while this simulator matches the second-order statistics of Clarke's model exactly, for any $M$, as an average over its random parameters. The [filtered Gaussian noise simulator](/filtered-gaussian-fading-simulator/) is the other common generator, a Gaussian process by construction. The 2003 form shares one phase among all sinusoids; Xiao, Zheng and Beaulieu (2006) showed that this form is not Gaussian over short times and use a phase per sinusoid, which is the form given here.

## In plain words

Picture the receiver of Clarke's model, with waves arriving from all directions. The Jakes simulator puts a fixed ring of waves around the receiver. This simulator spins the ring by a random angle, gives each wave a random strength split between the real and imaginary parts, and starts each wave at a random point of its cycle. One draw of these random numbers gives one fading channel. A new draw gives a new, independent channel. Because the spin covers every angle, the average correlation over many channels is exactly the one Clarke's model asks for, even with only a few waves. With few waves, one channel still looks less random than real fading.

## The problem

The input is the maximum Doppler shift $f_D$, the mean power $\Omega$, the number of sinusoids $M$, a source of random numbers, and $T$ times $t$. The output is one random realization $h(t) = \sqrt{2\Omega/M}\,(X_c(t) + j X_s(t))$ at the given times. The goal is a process whose ensemble statistics match Clarke's model: $E|h|^2 = \Omega$, $E[h(t+\tau)\overline{h(t)}] = \Omega J_0(2\pi f_D \tau)$, quadratures with equal autocorrelation and zero cross-correlation, and a distribution close to circular complex Gaussian, so that the envelope is Rayleigh. The model is flat time-correlated fading; the simulator gives the channel only, and the receiver's CSIR or CSIT is set by the simulation that uses it.

## The algorithm

```pseudo id=main
ZHENG-XIAO(M, f_D, Ω, t, rng)
L1  θ ← uniform on [-π, π)
L2  ψₙ ← uniform on [-π, π)  for n = 1 .. M          ▷ independent
L3  φₙ ← uniform on [-π, π)  for n = 1 .. M          ▷ one phase per sinusoid (2006)
L4  αₙ ← (2πn - π + θ) / (4M)  for n = 1 .. M
L5  X_c ← Σₙ cos ψₙ cos(2π f_D t cos αₙ + φₙ);  X_s ← Σₙ sin ψₙ cos(2π f_D t cos αₙ + φₙ)
L6  return √(2Ω/M) (X_c + j X_s)
```

Lines L1 to L4 are drawn once per channel and then kept for all times $t$. Line L4 places the $M$ angles at equal steps $\pi/(2M)$ inside $[0, \pi/2]$, shifted together by the random $\theta$. Only a quarter circle is needed, because waves at $\alpha$, $-\alpha$, $\pi - \alpha$ and $\pi + \alpha$ give the same Doppler frequency up to sign. Line L2 gives each sinusoid a random gain angle, which splits it between the two quadratures. Line L3 gives it a random Doppler phase. In eq. (14) of Zheng and Xiao (2003), line L3 is a single phase $\phi$ shared by all $n$; the per-sinusoid phases are the 2006 correction. Line L6 scales the sum so that $E|h|^2 = \Omega$.

## Example

Take $M = 8$ and $f_D = 1$. Line L4 gives eight angles spaced by $\pi/16 = 11.25$ degrees; for $\theta = 0$ they are 5.6, 16.9, 28.1, 39.4, 50.6, 61.9, 73.1 and 84.4 degrees, and the Doppler frequencies are $\cos\alpha_n$, from 0.995 down to 0.098.

The ensemble autocorrelation, averaged over $\theta$ alone with the other parameters averaged out, is $\frac{1}{M}\sum_n E_\theta \cos(x\cos\alpha_n)$ with $x = 2\pi f_D\tau$. A numerical integral over $\theta$ matches $J_0(x)$ within $10^{-9}$ at $f_D\tau = 0.1$, 0.38274, 1, 3 and 10, for $M = 1$, 2 and 8. Compare the [Jakes simulator](/jakes-fading-simulator/) with $M = 8$, whose time-average autocorrelation at $f_D\tau = 10$ is -0.049 instead of $J_0 = 0.071$.

The fourth moment shows the 2006 correction. A Rayleigh gain has $E|h|^4 = 2\Omega^2$.

| version | $E\lvert h(0) \rvert^4/\Omega^2$, formula | $M = 8$ | mean of 12000 draws |
|---|---|---|---|
| a phase per sinusoid (2006) | $2 - 1/(2M)$ | 1.9375 | 1.939 |
| one common phase (2003) | $3 - 3/(2M)$ | 2.8125 | 2.808 |

With one common phase, at $t = 0$ every sinusoid has the same phase, so $h(0) = \cos\phi \cdot \sqrt{2\Omega/M}\sum_n e^{j\psi_n}$, a Gaussian-like sum times a common random factor. Its distribution is far from Rayleigh for any $M$; as $t$ grows the Doppler terms spread the phases apart, so the statistics depend on $t$.

## Correctness

**Claim.** For any $M \ge 1$, with independent uniform $\theta$ and $\psi_n$, and phases that are independent of $\theta$ and $\psi$ (either one per sinusoid or shared): $E[h(t+\tau)\overline{h(t)}] = \Omega J_0(2\pi f_D\tau)$; the quadratures each have the autocorrelation $\frac{\Omega}{2} J_0(2\pi f_D \tau)$; and their cross-correlation is 0. With a phase per sinusoid, the $M$ terms are independent given $\theta$, so $h(t)$ tends to a circular complex Gaussian as $M$ grows, by the [central limit theorem](/central-limit-theorem/), and $E|h|^4/\Omega^2 = 2 - 1/(2M)$.

**Key step.** The random $\psi_n$ cancel all cross terms between different sinusoids and leave $\frac{1}{M}\sum_n E \cos(x\cos\alpha_n)$. As $\theta$ runs over $[-\pi, \pi)$, $\alpha_n$ runs over an interval of length $\pi/(2M)$, and the $M$ intervals tile $[0, \pi/2]$. So the average is $\frac{2}{\pi}\int_0^{\pi/2} \cos(x\cos\alpha)\, d\alpha = J_0(x)$. The second-order part is Theorem 1 of Zheng and Xiao (2003). The proof file gives the full argument and derives both fourth moments.

## Complexity

Lines L1 to L4 draw $2M + 1$ random numbers and compute $M$ cosines, $O(M)$ per channel. Each output sample costs $M$ cosines and $2M$ multiplications, so $T$ samples cost $O(M T)$ in the [real RAM](/real-ram/), with $O(M)$ extra space. A Monte Carlo study with many channels draws new parameters for each one.

## Properties

- **Exact second order.** The autocorrelations and the cross-correlation of Clarke's model hold exactly, for every $M$, over the ensemble. This is a theorem, not an approximation in $M$.
- **Wide-sense stationary.** The ensemble autocorrelation does not depend on $t$.
- **Not ergodic for small $M$.** One realization has the time-average autocorrelation $\frac{1}{M}\sum_n \cos(x\cos\alpha_n)$, a quadrature with $M$ points, which differs from $J_0$ at large lags. Statistics must be averaged over many draws, not over a long run of one draw.
- **Gaussian only in the limit.** For finite $M$ the gain is a sum of $M$ bounded terms, so it is not exactly Gaussian, and $|h|$ is bounded by $\sqrt{2\Omega M}$. The fourth moment is $2 - 1/(2M)$ instead of 2.
- **Higher-order statistics.** With one phase per sinusoid, the envelope distribution, the level crossing rate and the average fade duration approach those of Clarke's model as $M$ grows; $M = 8$ to 16 is common.

## Variants and improvements

- **The 2003 form with a common phase.** It has the same second-order statistics, but it is not Gaussian over short times and the autocorrelation of its squared envelope depends on $t$. The finding is credited to Sun, Ye and Choi and to Patel, Stuber and Pratt (2005); Xiao, Zheng and Beaulieu (2006) gave the correction.
- **The 2006 models.** Xiao, Zheng and Beaulieu (2006) also give a model with a random offset per sinusoid, $\alpha_n = (2\pi n + \theta_n)/N$, and a Rician model with a line-of-sight term; see [Rician fading](/rician-fading-channel/).
- **Several uncorrelated channels.** Separate parameters for each channel make the channels independent, which Zheng and Xiao (2003) use for multiple uncorrelated waveforms. Deterministic models need special angle sets for this.
- **Deterministic sum of sinusoids.** The [Jakes simulator](/jakes-fading-simulator/) uses fixed angles. It is cheaper to set up, but its statistics are only approximate.

## When to use it

Use it for Monte Carlo simulation of time-correlated Rayleigh fading when the channel must be evaluated at arbitrary times, for example with a Doppler that changes, or for channels in continuous time. Draw new parameters for each simulated channel and use the per-sinusoid phases. Use the [filtered Gaussian noise simulator](/filtered-gaussian-fading-simulator/) when an exactly Gaussian process on a fixed grid is needed, and an independent draw per block when the fading is block fading.

## Pitfalls

- **One long run instead of many draws.** The exact statistics are ensemble averages. One draw with small $M$ has the wrong time averages.
- **The common phase of 2003.** Copying eq. (14) as printed gives a process whose squared envelope is not stationary. Use one phase per sinusoid.
- **Too few sinusoids for tail statistics.** The envelope is bounded and its tails are lighter than Rayleigh. Deep fades, outage and error rates at high $\bar\gamma$ need $M$ large enough, or a Gaussian generator.
- **Normalization.** Each quadrature sum has variance $M/4$. Papers and codes use different scale factors; the factor $\sqrt{2\Omega/M}$ here gives $E|h|^2 = \Omega$. Check the scale before comparing $\bar\gamma$ across simulators.

## Implementations

## History

Pop and Beaulieu (2001) showed that the Jakes simulator is not wide-sense stationary and that random phases alone do not fix its higher-order statistics. Xiao and Zheng (2002) proposed a sum of sinusoids with random angles, gains and phases at a conference, and in 2003 Zheng and Xiao proved that the second-order statistics of their model match Clarke's model exactly for any number of sinusoids. Later work found that the 2003 model, with one phase for all sinusoids, is not Gaussian over short times and has a squared envelope whose autocorrelation is not stationary; Xiao, Zheng and Beaulieu (2006) corrected it with independent phases and gave new models for Rayleigh and Rician fading.

## References
