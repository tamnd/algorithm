---
tag: AFY7TQ
kind: algorithm
slug: cell-averaging-cfar
name: Cell-averaging CFAR
aliases:
- CA-CFAR
area: communications/radar-waveforms
level: core
summary: "Sets the threshold of each cell as a multiple of the sum of nearby reference cells, skipping guard cells, with a running sum. Pfa = (1 + tau)^(-N) for every noise power."
solves: [cfar-detection]
model: real-ram
complexity:
  vars: {n: the number of cells, N: the number of reference cells}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, online: true, scale_invariant: true, constant_false_alarm_rate_in_homogeneous_noise: true, exact_for_rational_input: true}
history:
  year: 1968
  people: [H. M. Finn, R. S. Johnson]
  note: "Finn and Johnson set the radar threshold from the mean of nearby range cells and computed its loss. Gandhi and Kassam proved in 1994 that it is a uniformly most powerful CFAR detector for a Swerling 1 target in exponential noise."
prereqs: [cfar-detection, sliding-window]
see_also: [ordered-statistic-cfar, swerling-target-models, range-doppler-processing, albersheim-equation, energy-detector, neyman-pearson-lemma, sufficient-statistic, signal-detection]
sources:
  - paper: "H. M. Finn and R. S. Johnson, RCA Review 29(3), 1968, pp. 414 to 464"
    title: Adaptive detection mode with threshold control as a function of spatially sampled clutter-level estimates
    locator: "the whole paper (the threshold from the mean of the reference cells, and its loss against a fixed threshold)"
  - paper: "P. P. Gandhi and S. A. Kassam, IEEE Transactions on Information Theory 40(4), 1994, pp. 1226 to 1228"
    title: Optimality of the cell averaging CFAR detector
    locator: "the whole paper (CA-CFAR is a uniformly most powerful CFAR detector for a Swerling 1 target in exponential noise of unknown power)"
  - paper: "P. P. Gandhi and S. A. Kassam, IEEE Transactions on Aerospace and Electronic Systems 24(4), 1988, pp. 427 to 445"
    title: Analysis of CFAR processors in nonhomogeneous background
    locator: "the whole paper (the CA, GO and SO processors at clutter edges and with interfering targets)"
  - book: isbn:9780071444743
    title: "Mark A. Richards, Fundamentals of Radar Signal Processing, McGraw-Hill, 2005"
    locator: "Chapter 7, Section 7.2 (cell-averaging CFAR, the threshold and the CFAR loss) and Section 7.4 (interfering targets and clutter edges)"
---

Cell-averaging CFAR (CA-CFAR) is the standard [CFAR detector](/cfar-detection/) of radar. For each range cell it adds the powers of $N$ reference cells around it, skips a few guard cells next to it, and declares a target when the cell's power is more than $\tau$ times that sum. With a running sum the cost is $O(1)$ per cell. In homogeneous exponential noise the false alarm probability is exactly $(1 + \tau)^{-N}$, whatever the noise power, so $\tau = P_{fa}^{-1/N} - 1$. It is the best CFAR rule in that model, and it fails in a known way when a second target or a clutter edge enters the window.

## In plain words

Slide a window along the list of powers. The window has a hole in the middle: the cell you test, plus a guard cell or two on each side, so that the target's own energy does not leak into the noise estimate. Add up the cells in the two halves of the window. If the tested cell is larger than a fixed multiple of that total, report a target. To move the window one cell, add the cell that enters each half and subtract the cell that leaves. The multiple depends only on the number of reference cells and the false alarm rate you want.

## The problem

The input is a list $x[0], \dots, x[n-1]$ of square-law powers, an even number $N = 2h$ of reference cells, a number $G \ge 0$ of guard cells on each side and a factor $\tau > 0$. For a cell $i$ with $G + h \le i \le n - 1 - G - h$, the reference window is the lagging cells $i - G - h, \dots, i - G - 1$ and the leading cells $i + G + 1, \dots, i + G + h$. Its sum is $Z_i$. The output is the list of cells $i$ with $x[i] > \tau Z_i$. Cells closer than $G + h$ to an end have no full window and are not tested. The design value $P_{fa}$ sets $\tau = P_{fa}^{-1/N} - 1$, and the threshold on the mean of the reference cells is $\alpha = N\tau$.

## The algorithm

```pseudo id=main
CA-CFAR(x[0..n-1], N, G, tau)
L1  h <- N / 2
L2  z <- sum of x[0 .. h-1] + sum of x[2G+h+1 .. 2G+2h]       ▷ the window of the first cell i = G + h
L3  for i <- G + h to n - 1 - G - h
L4      t <- tau * z
L5      if x[i] > t then report i
L6      z <- z + x[i - G] - x[i - G - h]                       ▷ the lagging half moves one cell right
L7      z <- z + x[i + G + h + 1] - x[i + G + 1]               ▷ the leading half moves one cell right
```

Line L2 sums the window of the first testable cell. Lines L4 and L5 compare the cell with the threshold. Lines L6 and L7 change $z$ to the sum of the next window: the cell $i - G$ leaves the guard zone and enters the lagging half, the cell $i + G + 1$ leaves the leading half and enters the guard zone, and one cell leaves at each outer edge. After the last cell, lines L6 and L7 are skipped, because the next window would run past the end.

## Example

Take $x = (3, 1, 2, 2, 1, 30, 9, 2, 1, 3, 2, 1, 2)$, so $n = 13$, with $N = 4$, $G = 1$ and $P_{fa} = 10^{-2}$. Then $h = 2$ and $\tau = 10^{2/4} - 1 = 2.16228$. Cells 3 to 9 have a full window.

| $i$ | lagging cells | leading cells | $Z_i$ | $\tau Z_i$ | $x[i]$ | decision |
|---|---|---|---|---|---|---|
| 3 | 3, 1 | 30, 9 | 43 | 92.98 | 2 | no |
| 4 | 1, 2 | 9, 2 | 14 | 30.27 | 1 | no |
| 5 | 2, 2 | 2, 1 | 7 | 15.14 | 30 | target |
| 6 | 2, 1 | 1, 3 | 7 | 15.14 | 9 | no |
| 7 | 1, 30 | 3, 2 | 36 | 77.84 | 2 | no |
| 8 | 30, 9 | 2, 1 | 42 | 90.82 | 1 | no |
| 9 | 9, 2 | 1, 2 | 14 | 30.27 | 3 | no |

At the end of the iteration for $i = 4$, line L6 adds $x[3] = 2$ and subtracts $x[1] = 1$, and line L7 adds $x[8] = 1$ and subtracts $x[6] = 9$. So $z$ goes from 14 to $14 + 1 - 8 = 7$, the sum of the window of cell 5. The guard cells keep the 30 out of the windows of cells 4 and 6. Cells 7 and 8 have high thresholds because the 30 is in their windows, which is the start of the masking problem described below.

## Correctness

The invariant of the loop is $z = Z_i$ at the start of the iteration for cell $i$. Line L2 sets it for the first cell. The window of $i + 1$ differs from the window of $i$ by one cell in and one cell out at each half, and lines L6 and L7 add and subtract exactly those four cells. So lines L4 and L5 compare $x[i]$ with $\tau Z_i$ for every testable $i$, and the output is the definition. With integer or rational powers the result is exact.

In the homogeneous model, the cell under test and the reference cells are independent and exponential with the same mean $\mu$. Then $Z_i$ is a gamma variable, $P(x[i] > \tau z) = e^{-\tau z/\mu}$, and the expectation over $Z_i$ is $(1 + \tau)^{-N}$: $\mu$ cancels. A Swerling 1 target of mean SNR $S$ gives $P_d = (1 + \tau/(1+S))^{-N}$. The full proofs are in the [correctness proof](proofs/correctness.md).

## Complexity

**Time.** Line L2 reads $N$ cells once. Each of the $n - 2G - N$ iterations of the loop does a fixed number of additions, one multiplication and one comparison. The total is $\Theta(n)$ for $N \le n$, in the best, average and worst case alike, because no step depends on the values. Recomputing the sum for each cell would cost $\Theta(nN)$.

**Space.** $\Theta(1)$ beyond the input and the list of detections.

## Properties

- **Constant false alarm rate (theorem, homogeneous exponential noise).** $P_{fa} = (1 + \tau)^{-N}$ for every noise power. In a simulation with $N = 8$, $G = 1$ and $P_{fa} = 0.05$, 4000 windows each at noise powers 1 and 50 (seed 4103), the design value was inside the 99.9 percent Wilson interval of the measured rate for both powers.
- **Scale invariance (theorem, any input).** Multiplying all powers by the same $c > 0$ does not change any decision.
- **The CFAR loss (closed form).** At $P_{fa} = 10^{-6}$, $\alpha$ is 36.99 for $N = 8$, 21.94 for $N = 16$, 17.28 for $N = 32$ and 15.42 for $N = 64$, against the ideal $\ln(10^6) = 13.82$. For a Swerling 1 target with $N = 16$, $P_d = 0.9$ needs 23.15 dB against 21.14 dB with a known noise power, a loss of 2.01 dB. At 20 dB, $P_d$ is 0.806 against 0.872.
- **Optimal in its model (theorem).** For a Swerling 1 target in homogeneous exponential noise, Gandhi and Kassam (1994) proved that CA-CFAR is a uniformly most powerful CFAR detector.
- **The sum is a sufficient statistic** for $\mu$ in the exponential model, which is why averaging is the right noise estimate there (see [sufficient statistic](/sufficient-statistic/)).

## Variants and improvements

- **Greatest of (GO-CFAR).** Use $2\max(Z_{\text{lag}}, Z_{\text{lead}})$ in place of $Z$, with a new $\tau$. It limits false alarms at the edge of a clutter region, at a small extra loss.
- **Smallest of (SO-CFAR).** Use the smaller half. It keeps a second target in one half from masking the first, but it gives many false alarms at clutter edges.
- **Ordered statistic.** Use the $k$-th smallest reference value: see [ordered-statistic CFAR](/ordered-statistic-cfar/). It resists up to $N - k$ interfering targets at a loss of about 0.5 to 1 dB in homogeneous noise.
- **Censored or trimmed mean.** Drop the largest few reference values and average the rest.
- **Two dimensions.** On the output of [range-Doppler processing](/range-doppler-processing/), the window is a ring of cells around the cell under test in range and Doppler. A two-dimensional prefix sum gives each window sum in $O(1)$.
- **Noncoherent integration.** If each cell is a sum of $M$ pulses, the noise is gamma with shape $M$, and $\tau$ must be computed from that distribution, not from $(1 + \tau)^{-N}$.

## When to use it

Use CA-CFAR when the noise is close to homogeneous over the window, for example thermal noise or wide areas of uniform clutter, and targets are sparse. It has the smallest loss and the lowest cost of the common rules. Use OS-CFAR when targets come in groups, for example in automotive radar or in dense traffic, and GO-CFAR when clutter edges cause false alarms. Choose $N$ as large as the extent of homogeneous clutter allows: 16 to 32 cells is common.

## Pitfalls

- **The factor on the sum and the factor on the mean.** Line L4 multiplies the sum by $\tau = P_{fa}^{-1/N} - 1$. Using $\alpha = N\tau$ with the sum, or $\tau$ with the mean, puts the threshold $N$ times too high or too low. Using the known-noise value $\ln(1/P_{fa})$ on the mean gives too many false alarms: with $N = 16$ the real rate is $(1 + 13.82/16)^{-16} = 4.8 \times 10^{-5}$, not $10^{-6}$.
- **Updating the window too early.** Lines L6 and L7 must come after line L5. If they run before line L4, cell $i$ is compared with the window of cell $i + 1$, and with $G = 0$ that window holds $x[i]$ itself.
- **Wrong indices in lines L6 and L7.** Adding $x[i - G + 1]$ in line L6, or $x[i + G]$ in line L7, lets a guard cell or the cell under test into the window. A strong target then raises its own threshold. The tests compare the running sum with a fresh sum on 600 random inputs, exactly.
- **Masking by a second target.** With $x = (2, 1, 3, 1, 2, 1, 2, 30, 1, 2, 24, 2, 1, 3, 1, 2, 1, 2)$, $N = 8$, $G = 1$ and $P_{fa} = 10^{-2}$, the target 24 at cell 10 has the 30 in its window, the threshold is 31.91, and CA-CFAR misses it. [Ordered-statistic CFAR](/ordered-statistic-cfar/) finds both.
- **Drift of the running sum in floating point.** After a very large value enters and leaves the window, the subtraction leaves a rounding error, which can make $z$ slightly wrong or even negative in a quiet region. Recompute the sum from scratch every few thousand cells, or use integer powers.
- **The wrong noise model.** $(1 + \tau)^{-N}$ assumes exponential cells, which is a square-law detector on complex Gaussian noise. With a linear detector, integrated pulses, or Weibull or K-distributed clutter, the false alarm rate is different.

## Implementations

## History

H. M. Finn and R. S. Johnson described the cell-averaging threshold in 1968, in the RCA Review, and computed its loss against a fixed threshold. In the 1970s and 1980s, the GO and SO variants were analyzed for clutter edges and multiple targets. H. Rohling introduced the ordered statistic rule in 1983. P. P. Gandhi and S. A. Kassam compared the processors in nonhomogeneous backgrounds in 1988, and in 1994 proved that the cell-averaging detector is a uniformly most powerful CFAR detector for a Swerling 1 target in exponential noise.

## References
