---
tag: 6ECXVW
kind: theorem
slug: albersheim-equation
name: Albersheim equation
aliases:
- Albersheim approximation
area: communications/radar-waveforms
level: core
summary: "An empirical fit for the SNR per pulse that a nonfluctuating target needs with a linear detector and N pulses, for Pfa 1e-7 to 1e-3 and Pd 0.1 to 0.9, stated to be within 0.2 dB."
prereqs: [radar-range-equation, signal-detection]
see_also: [swerling-target-models, cfar-detection, cell-averaging-cfar, rician-fading-channel, energy-detector, neyman-pearson-lemma, matched-filter, gaussian-q-function]
sources:
  - paper: doi:10.1109/PROC.1981.12082
    title: A closed-form approximation to Robertson's detection characteristics
    locator: "W. J. Albersheim, Proceedings of the IEEE 69(7), 1981, p. 839 (the formula, a one page letter)"
  - book: isbn:9780071444743
    title: "Mark A. Richards, Fundamentals of Radar Signal Processing, McGraw-Hill, 2005"
    locator: "Chapter 6, Section 6.3.3 (Albersheim's equation, its range of validity and its accuracy) and Section 6.3.5 (Shnidman's equation for the Swerling targets)"
  - book: isbn:9780072881387
    title: "Merrill I. Skolnik, Introduction to Radar Systems, third edition, McGraw-Hill, 2001"
    locator: "Chapter 5, Detection of Signals in Noise (the detection of a nonfluctuating target and the integration of pulses)"
---

The Albersheim equation gives, in closed form, the signal to noise ratio per pulse that a radar needs to detect a nonfluctuating target with a probability $P_d$ at a false alarm probability $P_{fa}$, after the noncoherent integration of $N$ pulses with a linear envelope detector. The exact answer needs the inverse of a generalized Marcum Q function, which has no closed form. Albersheim's formula is an empirical fit to the published detection curves, not a theorem, and it has no proof. Its value is that it is easy to compute and to invert inside the [radar range equation](/radar-range-equation/). For fluctuating targets, use the [Swerling models](/swerling-target-models/) instead.

## Statement

Let

$$A = \ln\frac{0.62}{P_{fa}}, \qquad B = \ln\frac{P_d}{1 - P_d}.$$

Then the SNR per pulse, in dB, is approximately

$$\mathrm{SNR}_{\mathrm{dB}} \approx -5\log_{10} N + \left(6.2 + \frac{4.54}{\sqrt{N + 0.44}}\right) \log_{10}\left(A + 0.12\, A B + 1.7\, B\right).$$

**Range.** A nonfluctuating target (Swerling case 0) in white Gaussian noise, a linear envelope detector, noncoherent integration of $N$ equal pulses, and $10^{-7} \le P_{fa} \le 10^{-3}$, $0.1 \le P_d \le 0.9$, $1 \le N \le 8096$.

**Accuracy (stated).** Within 0.2 dB of the exact value over that range. This is a property claimed for the fit, not a proven bound, and the comparison below shows that it fails at the low end of $P_d$.

**The label.** This is a fit, a rule of thumb with a stated range. It is not derived from the detection model.

## In plain words

To detect a steady target you need a certain SNR. It depends on how sure you want to be (a high $P_d$), how few false alarms you accept (a small $P_{fa}$) and how many pulses you add before you decide. The exact value comes from a hard integral. Albersheim fitted a short formula to the curves: $A$ grows as the false alarm probability gets smaller, $B$ grows as the detection probability gets larger, and the $-5\log_{10} N$ term says that each tenfold increase in the number of pulses saves about 5 dB per pulse. You get the answer with a pocket calculator, and you can solve it for $P_d$ when the SNR is given.

## Proof

There is no proof: the formula is a fit. What can be done is to compare it with the exact value. For $N = 1$, a linear and a square-law detector make the same decisions, because the square is monotone in the envelope. The envelope of a constant signal in complex Gaussian noise has the Rice distribution, and with the SNR $S$ and the threshold $T = \ln(1/P_{fa})$ on the normalized power, the exact detection probability is

$$P_d = Q_1\!\left(\sqrt{2S}, \sqrt{2T}\right),$$

with the Marcum Q function $Q_1$.

**The case $P_{fa} = 10^{-6}$, $P_d = 0.9$, $N = 1$.** Then $A = \ln(620\,000) = 13.338$ and $B = \ln 9 = 2.197$, so $A + 0.12AB + 1.7B = 20.590$, and the formula gives

$$\mathrm{SNR}_{\mathrm{dB}} = (6.2 + 4.54/\sqrt{1.44}) \log_{10} 20.590 = 9.983 \times 1.3137 = 13.11 \text{ dB}.$$

Solving $Q_1(\sqrt{2S}, \sqrt{2 \ln 10^6}) = 0.9$ numerically gives $S = 13.18$ dB. The fit is 0.069 dB low, inside the stated 0.2 dB. At 13.11 dB, the exact $P_d$ is 0.891, not 0.9.

**A grid at $N = 1$.** The table gives the exact SNR in dB and the error of the fit (the fit minus the exact value), computed in the same way.

| $P_{fa}$ | $P_d = 0.1$ | $0.2$ | $0.3$ | $0.5$ | $0.7$ | $0.9$ |
|---|---|---|---|---|---|---|
| $10^{-3}$ | 4.08 / $-4.08$ | 5.67 / $-0.90$ | 6.65 / $-0.29$ | 8.06 / $+0.01$ | 9.27 / $+0.02$ | 10.76 / $-0.04$ |
| $10^{-4}$ | 6.14 / $-1.84$ | 7.40 / $-0.49$ | 8.21 / $-0.16$ | 9.40 / $0.00$ | 10.44 / $-0.02$ | 11.75 / $-0.07$ |
| $10^{-5}$ | 7.60 / $-1.19$ | 8.68 / $-0.34$ | 9.37 / $-0.11$ | 10.42 / $-0.01$ | 11.35 / $-0.03$ | 12.53 / $-0.08$ |
| $10^{-6}$ | 8.73 / $-0.90$ | 9.68 / $-0.27$ | 10.30 / $-0.09$ | 11.24 / $-0.01$ | 12.09 / $-0.03$ | 13.18 / $-0.07$ |
| $10^{-7}$ | 9.65 / $-0.75$ | 10.50 / $-0.23$ | 11.07 / $-0.08$ | 11.94 / $-0.01$ | 12.72 / $-0.03$ | 13.74 / $-0.05$ |

For $P_d \ge 0.5$ the fit is within 0.1 dB at $N = 1$. At $P_d = 0.2$ it is 0.23 dB to 0.90 dB too low, and at $P_d = 0.1$ it is 0.75 dB to 4.08 dB too low. At $P_{fa} = 10^{-3}$ and $P_d = 0.1$, the argument of the logarithm is close to 1, and the fit gives $-0.004$ dB against the exact 4.08 dB. $\blacksquare$

## Consequences

- **Quick link budgets.** With $N = 1$, $P_{fa} = 10^{-6}$ and $P_d = 0.9$, the fit gives 13.11 dB. For $N = 10$ pulses it gives 4.99 dB per pulse, and for $N = 100$ pulses $-1.26$ dB per pulse. Put the value in the [radar range equation](/radar-range-equation/) to get the maximum range.
- **The integration gain.** The difference between $N = 1$ and $N$ pulses is the gain of noncoherent integration. From 1 to 10 pulses it is 8.12 dB, less than the 10 dB of coherent integration, and the gap grows with $N$.
- **The inverse.** With the SNR given, solve for $B$ and then $P_d = 1/(1 + e^{-B})$. This gives $P_d$ in closed form, which is useful inside optimization loops.
- **Fluctuating targets.** For the Swerling cases, Shnidman's equation is a fit of the same kind. Add the CFAR loss of the [CFAR detector](/cfar-detection/) used, for example 2.01 dB for [cell-averaging CFAR](/cell-averaging-cfar/) with 16 reference cells at $P_{fa} = 10^{-6}$ and a Swerling 1 target.

## Tightness

- **Low $P_d$.** The grid above shows that the 0.2 dB claim fails at $N = 1$ for $P_d = 0.1$ and $0.2$, with errors up to 4.08 dB. The fit is reliable for $P_d$ from about 0.3 to 0.9, which covers most design work.
- **The detector law.** The fit is for a linear detector. A square-law detector differs by a small amount for $N > 1$. At $N = 10$, $P_{fa} = 10^{-6}$ and $P_d = 0.9$, the exact square-law value is 5.27 dB against the 4.99 dB of the fit, a difference of 0.28 dB, part of which is the difference of the detector laws.
- **Outside the range.** For $P_{fa}$ above $10^{-3}$ or $P_d$ outside $[0.1, 0.9]$, the argument of the logarithm can be close to 0 or negative, and the formula has no meaning.
- **Fluctuating targets.** For a Swerling 1 target with $N = 1$, $P_{fa} = 10^{-6}$ and $P_d = 0.9$, the exact value is 21.14 dB, 8 dB above the value for a steady target. Albersheim's formula does not apply.

## History

Marcum computed the detection probability of a steady target with noncoherent integration in 1960, and later authors, Robertson among them, published detection curves for it. W. J. Albersheim fitted the closed form to Robertson's curves, as the title of his letter says, in a one page letter in the Proceedings of the IEEE in 1981. The IEEE record of the letter spells the author's name "Alberhseim". The formula became popular because it needs no tables, and Richards gives it with its range and its 0.2 dB accuracy.

## References
