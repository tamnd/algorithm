---
tag: 1DZ4K1
kind: model
slug: swerling-target-models
name: Swerling target models
aliases:
- Swerling models
area: communications/radar-waveforms
level: core
summary: "Four models of a fluctuating radar cross section: chi-squared with 2 or 4 degrees of freedom, constant over a scan or new on each pulse. With case 0, a steady target, they set the SNR a radar needs."
prereqs: [radar-range-equation, signal-detection]
see_also: [albersheim-equation, cell-averaging-cfar, cfar-detection, rayleigh-fading-channel, rician-fading-channel, nakagami-m-fading-channel, maximal-ratio-combining, energy-detector]
sources:
  - paper: doi:10.1109/TIT.1960.1057561
    title: Probability of detection for fluctuating targets
    locator: "P. Swerling, IRE Transactions on Information Theory 6(2), 1960, pp. 269 to 308 (the four fluctuation cases and their detection probabilities)"
  - paper: doi:10.1109/TIT.1960.1057560
    title: A statistical theory of target detection by pulsed radar
    locator: "J. I. Marcum, IRE Transactions on Information Theory 6(2), 1960, pp. 59 to 267 (the steady target, case 0, with noncoherent integration)"
  - book: isbn:9780071444743
    title: "Mark A. Richards, Fundamentals of Radar Signal Processing, McGraw-Hill, 2005"
    locator: "Chapter 2, Sections 2.2.5 and 2.2.6 (the Swerling models), and Chapter 6, Section 6.3 (the detection probability of steady and fluctuating targets, with Albersheim's and Shnidman's equations)"
  - book: isbn:9780072881387
    title: "Merrill I. Skolnik, Introduction to Radar Systems, third edition, McGraw-Hill, 2001"
    locator: "Chapter 2, The Radar Equation (the fluctuations of the radar cross section and the Swerling models)"
---

The Swerling target models describe how the radar cross section $\sigma$ of a target changes from one look to the next. A real target, such as an aircraft, is made of many scattering parts, and its echo changes strongly with a small change of aspect. Swerling (1960) gave four cases. In cases 1 and 2, $\sigma$ is exponential, which is a chi-squared variable with 2 degrees of freedom: many scatterers of similar size. In cases 3 and 4, $\sigma$ is chi-squared with 4 degrees of freedom: one large scatterer and many small ones. In cases 1 and 3, $\sigma$ stays the same over the pulses of one scan and changes from scan to scan; in cases 2 and 4, it changes from pulse to pulse. Case 0, also called case 5, is the steady target of Marcum. The models turn the [radar range equation](/radar-range-equation/), which gives the mean SNR, into a probability of detection.

## The machine

**The input.** The radar sends $N$ pulses to a target and integrates them noncoherently. The mean radar cross section is $\bar{\sigma}$, which gives the mean SNR per pulse $\bar{S}$ through the radar range equation.

**The output.** The complex sample of pulse $n = 1, \dots, N$ at the target's range cell is

$$r_n = \sqrt{S_n}\, e^{j\phi_n} + w_n, \qquad S_n = \bar{S}\, \sigma_n / \bar{\sigma},$$

with the noise $w_n \sim \mathcal{CN}(0, 1)$ independent from pulse to pulse, and a phase $\phi_n$ uniform on $[0, 2\pi)$ and unknown. The detector forms $z = \sum_n |r_n|^2$ (a square-law detector) and decides "target" when $z > T$.

**The parameters.** $\bar{S}$ is a ratio, not in dB. $N \ge 1$ is an integer. The threshold $T$ is set by the false alarm probability: with noise only, $z$ is a gamma variable of shape $N$ and scale 1, so $P_{fa} = P(\Gamma(N, 1) > T)$, and $T = \ln(1/P_{fa})$ for $N = 1$.

**The fluctuation.** The cross section $\sigma_n$ follows one of five cases.

| case | density of $\sigma$ | correlation over the $N$ pulses |
|---|---|---|
| 0 (or 5) | $\sigma = \bar{\sigma}$, constant | |
| 1 | $\frac{1}{\bar\sigma} e^{-\sigma/\bar\sigma}$ | the same for all $N$ pulses (scan to scan) |
| 2 | $\frac{1}{\bar\sigma} e^{-\sigma/\bar\sigma}$ | independent from pulse to pulse |
| 3 | $\frac{4\sigma}{\bar\sigma^2} e^{-2\sigma/\bar\sigma}$ | the same for all $N$ pulses (scan to scan) |
| 4 | $\frac{4\sigma}{\bar\sigma^2} e^{-2\sigma/\bar\sigma}$ | independent from pulse to pulse |

**The standing assumptions.** The target is a point target in the sense of the radar range equation. The noise is white and Gaussian. Pulse-to-pulse independence needs a change of frequency between pulses (frequency agility) or a fast change of aspect, because the echo of a rigid body over a few milliseconds is usually correlated.

## What it counts

The model predicts the probability of detection $P_d$ as a function of $\bar{S}$, $N$ and $P_{fa}$, or, inverted, the SNR per pulse that is needed for a given $P_d$ and $P_{fa}$. These are the closed forms for one pulse ($N = 1$), with $T = \ln(1/P_{fa})$:

- **Case 0.** $P_d = Q_1(\sqrt{2\bar{S}}, \sqrt{2T})$, with the Marcum Q function. There is no closed form for the inverse, and the [Albersheim equation](/albersheim-equation/) is a fit to it.
- **Cases 1 and 2.** $|r|^2$ is exponential with mean $1 + \bar{S}$, so $P_d = e^{-T/(1 + \bar{S})} = P_{fa}^{1/(1 + \bar{S})}$.
- **Cases 3 and 4.** $P_d = e^{-T/(1 + \bar{S}/2)} \left(1 + \dfrac{(\bar{S}/2)\, T}{(1 + \bar{S}/2)^2}\right)$.

For $N > 1$, case 2 has the simple form $P_d = P\big(\Gamma(N, 1) > T/(1 + \bar{S})\big)$, because each $|r_n|^2$ is exponential with mean $1 + \bar{S}$. Cases 0, 1, 3 and 4 have series forms, given by Swerling and in the textbooks.

**Check values** (the SNR per pulse in dB for $P_d = 0.9$ and $P_{fa} = 10^{-6}$, computed from these formulas and their series forms):

| $N$ | case 0 | case 1 | case 2 | case 3 | case 4 |
|---|---|---|---|---|---|
| 1 | 13.18 | 21.14 | 21.14 | 17.30 | 17.30 |
| 10 | 5.27 | 13.50 | 6.29 | 9.60 | 5.81 |

At 13 dB with $N = 1$, $P_d$ is 0.874 for case 0, 0.517 for cases 1 and 2 and 0.609 for cases 3 and 4.

## Relation to other models

- **Fading channels.** An exponential $\sigma$ is a Rayleigh envelope, the same model as the [Rayleigh fading channel](/rayleigh-fading-channel/): the sum of many echoes with random phases. The chi-squared law with 4 degrees of freedom has the same mean and a smaller spread, and it approximates a [Rician](/rician-fading-channel/) envelope with one strong part. Both are gamma laws, the power form of the [Nakagami-m model](/nakagami-m-fading-channel/) with $m = 1$ and $m = 2$.
- **Diversity.** Pulse-to-pulse fluctuation (cases 2 and 4) is diversity, as in [maximal ratio combining](/maximal-ratio-combining/) over independent fading branches: the integrated sum fluctuates less than one term. Scan-to-scan fluctuation (cases 1 and 3) gives no diversity within a dwell.
- **Generalizations.** The chi-squared family with $2K$ degrees of freedom contains cases 1 to 4 ($K = 1$ and $K = 2$) and tends to case 0 as $K \to \infty$. Shnidman fitted a closed form, like Albersheim's, that covers these cases.
- **CFAR.** With an unknown noise power, the threshold comes from a [CFAR detector](/cfar-detection/), and the Swerling 1 model gives the simple closed forms for [cell-averaging CFAR](/cell-averaging-cfar/) and ordered-statistic CFAR.

## Known results in the model

- **The fluctuation loss (closed form).** For $N = 1$, $P_{fa} = 10^{-6}$ and $P_d = 0.9$, a Swerling 1 target needs 21.14 dB against 13.18 dB for a steady target: 7.96 dB more. Swerling 3 needs 17.30 dB. At high $P_d$ the loss is large, because a fluctuating target is sometimes very weak and nothing makes up for that within one scan.
- **The gain of pulse-to-pulse fluctuation.** With $N = 10$, case 2 needs 6.29 dB and case 1 needs 13.50 dB: independence across pulses saves 7.21 dB. Case 4 needs 5.81 dB, close to the 5.27 dB of case 0. Radars use frequency agility to turn case 1 targets into case 2 targets.
- **Fluctuation can help at low $P_d$.** For small $P_d$, a fluctuating target needs less SNR than a steady one, because its rare strong peaks cross the threshold.
- **Exact detection with CA-CFAR.** For Swerling 1 and $N = 1$, [cell-averaging CFAR](/cell-averaging-cfar/) with $N_r$ reference cells gives $P_d = (1 + \tau/(1 + \bar{S}))^{-N_r}$, and CA-CFAR is the uniformly most powerful CFAR test in this case. With 16 reference cells it needs 23.15 dB for $P_d = 0.9$ at $P_{fa} = 10^{-6}$.
- **The Swerling 1 closed form follows from one line.** Given $\sigma$, $|r|^2$ is a noncentral chi-squared variable. Averaged over an exponential $\sigma$, it is exponential with mean $1 + \bar{S}$, which gives $P_{fa}^{1/(1+\bar{S})}$ at once.

## References
