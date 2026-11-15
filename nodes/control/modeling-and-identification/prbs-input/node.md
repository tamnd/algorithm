---
tag: YHRB09
kind: technique
slug: prbs-input
name: Pseudo-random binary sequence input
aliases:
- PRBS
- maximum-length binary input
area: control/modeling-and-identification
level: intro
summary: An input signal for identification that switches between two levels by a maximum-length shift register sequence, with a near white spectrum.
prereqs: [persistent-excitation, linear-feedback-shift-register]
see_also: [primitive-polynomial, de-bruijn-sequence, empirical-transfer-function-estimate, least-squares-arx-identification, autocorrelation, walsh-hadamard-transform, impulse-response, system-identification]
sources:
  - book: isbn:9780136564140
    title: "Keith Godfrey (editor), Perturbation Signals for System Identification, Prentice Hall, 1993"
    locator: the chapters on maximum-length binary sequences, their correlation and spectral properties, and their use as test signals
  - book: isbn:9780138812362
    title: "Torsten Söderström and Petre Stoica, System Identification, Prentice Hall, 1989"
    locator: "Chapter 5 (input signals: the pseudo-random binary sequence, its covariance function and its order of persistent excitation)"
  - book: isbn:9780136566953
    title: "Lennart Ljung, System Identification: Theory for the User, second edition, Prentice Hall, 1999"
    locator: "Chapter 13 (experiment design and the choice of input signals)"
---

A pseudo-random binary sequence (PRBS) input is a test signal for [system identification](/system-identification/) that takes only two values, $u_0 + a$ and $u_0 - a$, and switches between them in the pattern of a maximum-length sequence from a [linear feedback shift register](/linear-feedback-shift-register/). With a register of $r$ bits and a [primitive](/primitive-polynomial/) feedback polynomial, the sequence repeats after $M = 2^r - 1$ steps. Over one period its autocorrelation takes only two values, so its spectrum is flat at every nonzero harmonic of $2\pi/M$. It is therefore close to white noise, but it is deterministic, periodic, and has the smallest possible peak value for its power. A PRBS of period $M$ is [persistently exciting](/persistent-excitation/) of order exactly $M$.

## In plain words

To learn how a machine responds, you want to push it at all speeds, slow and fast, with equal force. Random noise does that, but it has spikes, and many plants can only take a limited push. A PRBS is a switch that flips between "high" and "low" in a pattern that looks random but is made by a simple shift register. Because it only ever sits at the two levels, it gives the most energy for a given limit on the push. Because the pattern repeats exactly, you can average over repeats to cut noise, and you know beforehand which frequencies it contains. Holding each value for several samples moves the energy toward slow motions.

## When it applies

- The plant tolerates two-level switching of the input, for example a valve, a heater power or a motor voltage around an operating point.
- The model is linear, or is linear for small deviations around $u_0$; the amplitude $a$ must stay inside that range.
- The number of parameters to be estimated is less than $M$, since the order of persistent excitation is $M$.
- The experiment can run for at least one full period after the transient, so that the periodic properties hold for the recorded data.

## The template

```pseudo id=main
PRBS-EXPERIMENT(⟨p⟩, ⟨a⟩, ⟨u0⟩, ⟨P⟩, ⟨m⟩)
L1  r ← the degree of the primitive polynomial ⟨p⟩; M ← 2^r - 1
L2  s(0), ..., s(r - 1) ← any bits that are not all 0
L3  for n ← r to m·M - 1 do s(n) ← XOR of s(n - r + i) over the terms x^i, i < r, of ⟨p⟩
L4  for n ← 0 to m·M - 1 do
L5      hold u ← ⟨u0⟩ + ⟨a⟩·(2 s(n) - 1) for ⟨P⟩ samples
L6  record y while u is applied; drop the first period as a transient
L7  return u and y for ⟨the estimator⟩
```

The holes are the feedback polynomial $p$, which fixes the register length $r$ and the taps, the amplitude $a$ and operating point $u_0$, the clock period $P$ in samples, the number of periods $m$, and the estimator that will use the data.

**The sequence (L1 to L3).** The recursion of L3 has $p$ as its characteristic polynomial. When $p$ is primitive of degree $r$, every nonzero start state runs through all $2^r - 1$ nonzero states of the register before it repeats, so $s$ has period exactly $M$. For $r = 4$ and $x^4 + x + 1$ the recursion is $s(n) = s(n-3) \oplus s(n-4)$, and the start $1111$ gives one period

$$1\ 1\ 1\ 1\ 0\ 0\ 0\ 1\ 0\ 0\ 1\ 1\ 0\ 1\ 0,$$

with 8 ones and 7 zeros. In every period there are $2^{r-1}$ ones and $2^{r-1} - 1$ zeros.

**The correlation (theorem).** Map the bits to $\pm a$ as in L5 with $P = 1$ and take the mean over one period. Then

$$r_u(\tau) = \begin{cases} a^2 & \tau \equiv 0 \pmod M, \\ -a^2 / M & \text{otherwise.} \end{cases}$$

The reason is the shift-and-add property of maximum-length sequences: $s(n) \oplus s(n + \tau)$ is again a shift of $s$ for $\tau \not\equiv 0$, so it has $2^{r-1}$ ones and $2^{r-1} - 1$ zeros, and the product of the two $\pm 1$ signals sums to $-1$ over a period.

**The spectrum (theorem).** Over one period the discrete Fourier transform of the $\pm a$ signal has $\lvert U_0 \rvert^2 = a^2$ and $\lvert U_l \rvert^2 = a^2 (M + 1)$ for $l = 1, \ldots, M - 1$. For $r = 4$ and $a = 1$, the values are $1$ and $16$. So the power is the same at every nonzero harmonic $2\pi l/M$, and the mean is only $a/M$.

**The clock period (L5).** Holding each bit for $P > 1$ samples multiplies the line spectrum by the envelope $\big(\sin(\omega P/2) / (P \sin(\omega/2))\big)^2$, which has its first zero at $\omega = 2\pi/P$. A rule of thumb is to pick $P$ so that this first zero lies a few times above the bandwidth of the plant, and to pick $M P h$ longer than the settling time of the plant, so that one period of the response does not wrap onto the next.

**Persistent excitation.** For $n \le M$ the covariance matrix $\bar R_n = a^2\big((1 + \tfrac{1}{M}) I - \tfrac{1}{M} \mathbf{1}\mathbf{1}^T\big)$ has the eigenvalues $a^2(1 + \tfrac{1}{M})$ and $a^2 (M + 1 - n)/M$, all positive. At $n = M + 1$ the second one is $0$. The order of persistent excitation is exactly $M$.

## Classic examples

- **Correlation analysis of the [impulse response](/impulse-response/).** With $P = 1$ and a plant whose impulse response $g$ dies out within $M$ samples, the periodic cross-correlation of $y$ with $u$ is $r_{yu}(\tau) = a^2 (1 + \tfrac{1}{M})\, g(\tau) - \tfrac{a^2}{M} \sum_j g(j)$. So $g$ is read off from $r_{yu}$ up to a small known offset, without solving any equations. The correlation can be computed fast with the [Walsh-Hadamard transform](/walsh-hadamard-transform/) after a permutation of the samples.
- **[Empirical transfer function estimate](/empirical-transfer-function-estimate/).** With a whole number of periods in steady state, the input has power only at the harmonics $2\pi l/M$, the ratio $Y_l/U_l$ there has no leakage, and averaging over the $m$ periods lowers the noise variance by a factor $m$.
- **[Least-squares identification of ARX models](/least-squares-arx-identification/) and the [prediction error method](/prediction-error-method/).** A PRBS with $M$ larger than the number of input coefficients gives a nonsingular normal matrix, and its low crest factor gives the most input power under an amplitude limit.
- **Dither in [closed-loop identification](/closed-loop-identification/).** A small PRBS added to the reference makes the closed-loop data informative while the controller keeps the plant near its operating point.

## Variations

- **Random binary signal.** Flip a fair coin at each clock instant. It is persistently exciting of every order, but its spectrum on a finite record is not flat.
- **Generalized binary noise.** Switch the level with a fixed probability at each sample, which sets the mean time between switches and so shapes the low-frequency power.
- **[De Bruijn sequences](/de-bruijn-sequence/).** Add the all-zero state to get period $2^r$; the correlation is then no longer two-valued.
- **Inverse-repeat PRBS.** Apply the sequence and then its negative. The period doubles, and the response to even-order nonlinearities cancels in the average.
- **Multilevel and ternary sequences.** Sequences over more than two levels from shift registers over a finite field reveal static nonlinearities that a binary signal cannot see.
- **Multisine.** A sum of sinusoids at chosen harmonics with phases picked to keep the peak low. It gives full control over the spectrum, at the cost of a higher crest factor than a binary signal.

## Pitfalls

- **A polynomial that is not primitive.** At L1, the polynomial $x^4 + x^2 + 1 = (x^2 + x + 1)^2$ gives period 6 from the start $1111$, and $x^4 + x^3 + x^2 + x + 1$ gives period 5. The order of persistent excitation drops with the period. Take $p$ from a table of primitive polynomials, or check that the period is $2^r - 1$.
- **An all-zero start.** At L2, the all-zero state maps to itself and the sequence is constant. Any other start works.
- **A period shorter than the response.** If $M P h$ is shorter than the settling time, the periodic correlation in L7 returns $\sum_l g(\tau + l M)$ instead of $g(\tau)$. Choose $M$ so that one period covers the settling time.
- **A clock period that is too short.** With $P = 1$ and a slow plant, most of the input power is above the bandwidth of the plant and the low-frequency fit has a poor signal-to-noise ratio. Raise $P$ at L5.
- **A record that is not a whole number of periods.** The two-valued correlation and the flat line spectrum hold over whole periods only. Record $m$ full periods after the transient at L6.
- **The nonzero mean.** The mean of the $\pm a$ sequence is $a/M$, not $0$. Remove the sample means of $u$ and $y$ before estimating, or include an offset in the model.

## Exercises

1. Show that the matrix $(1 + \tfrac{1}{M}) I - \tfrac{1}{M} \mathbf{1}\mathbf{1}^T$ of size $n$ has the eigenvalues $1 + \tfrac{1}{M}$ and $(M + 1 - n)/M$, and conclude that the order of persistent excitation of a PRBS is $M$.
2. Generate the sequence of $x^5 + x^2 + 1$ from the start $11111$ and check that its period is 31.
3. For a plant with impulse response $g(j) = 0.5^j$ for $j \ge 1$ and a PRBS with $M = 15$ and $a = 1$, compute the periodic cross-correlation at $\tau = 1$ and recover $g(1)$ from it.

## References
