---
tag: N335YA
kind: algorithm
slug: tone-reservation
name: Tone reservation
aliases:
- peak-reduction tones
area: communications/ofdm-and-multicarrier
level: advanced
summary: "Lowers the PAPR of OFDM by keeping a few subcarriers free of data and filling them with a signal that cancels the peaks. The data subcarriers stay unchanged and no side information is sent."
model: real-ram
complexity:
  vars: {N: the number of subcarriers, L: the oversampling factor, K: the number of iterations}
  time: {worst: O(L N log(L N) + K L N)}
  space: {extra: O(L N)}
properties: {deterministic: true, distortionless: true, side_information: false, costs_subcarriers: true, adds_power: true}
history:
  year: 2000
  people: [Jose Tellado]
  note: "Tellado developed tone reservation for multicarrier DSL and wireless transmission in his work at Stanford, collected in his book of 2000."
prereqs: [peak-to-average-power-ratio, orthogonal-frequency-division-multiplexing]
see_also: [iterative-clipping-and-filtering, active-constellation-extension, selected-mapping, partial-transmit-sequence, second-order-cone-programming, linear-programming-problem, discrete-multitone, fast-fourier-transform]
sources:
  - book: isbn:9780792379881
    title: "Jose Tellado, Multicarrier Modulation with Low PAR: Applications to DSL and Wireless, Kluwer Academic Publishers, 2000"
    locator: "chapter PAR Reduction by Tone Reservation (the reserved tones, the optimization over them and the gradient algorithm with the peak-cancelling kernel)"
  - paper: doi:10.1109/MWC.2005.1421929
    title: "Seung Hee Han and Jae Hong Lee, An overview of peak-to-average power ratio reduction techniques for multicarrier transmission, IEEE Wireless Communications 12(2), 2005, pages 56 to 65"
    locator: "the section on tone reservation and tone injection"
---

Tone reservation lowers the [peak-to-average power ratio](/peak-to-average-power-ratio/) (PAPR) of an [OFDM](/orthogonal-frequency-division-multiplexing/) symbol by keeping a small set $R$ of subcarriers free of data. The transmitter fills these reserved tones with values $C[k]$ chosen so that the added time signal cancels the peaks. The data subcarriers are not touched, so the receiver demodulates them as usual, ignores the tones in $R$, and needs no side information. Finding the best $C$ is a convex problem. The common fast method, due to Tellado, uses a kernel: a time signal $p$ whose spectrum lies on $R$ and which has one tall peak at time 0. Each step shifts the kernel to the current largest sample and subtracts just enough of it to bring that sample down to a target magnitude $A$. The price is the $|R|$ subcarriers that carry no data and the extra power on them. The page uses the unitary DFT pair $F[k, n] = e^{-j 2\pi k n / N}/\sqrt N$, $j$ is the imaginary unit, and the data have $E|X[k]|^2 = 1$.

## In plain words

Some tones in the OFDM symbol are set aside and carry no data. The sender may put anything on them, because the receiver throws them away. The sender uses them to build a correction signal that pushes the tall peaks down. A good correction looks like one sharp spike with small ripples, so it can remove one peak without making new ones. The sender finds the tallest peak, puts the spike there with the right size and angle, and subtracts it. Then it looks for the next tallest peak and repeats a few times. The data tones never change, so the receiver does nothing new. The cost is the tones that carry no data and a little extra power.

## The problem

The input is a block of $N$ data symbols $X[0], \ldots, X[N-1]$ with $X[k] = 0$ on the reserved set $R$, an oversampling factor $L$, usually 4, a target peak magnitude $A$ and a number of iterations $K$. The output is a vector $C$ that is zero off $R$ and the oversampled symbol $y = x + c$ of $X + C$, where $x$ and $c$ are the symbols of $X$ and $C$. The goal is a small $\max_t |y[t]|$. The best $C$ minimizes $\max_t |x[t] + c[t]|$, which is a convex function of $C$. The algorithm below gives a good $C$ quickly but does not always reach that minimum.

## The algorithm

```pseudo id=main
TR(X[0..N-1], R, L, A, K)                      ▷ X[k] = 0 for k in R
L1  x ← √L · F_LNᴴ (X, with (L-1)N zeros in the middle)
L2  p ← (√N/|R|) · √L · F_LNᴴ (indicator of R, zeros in the middle)   ▷ p[0] = 1
L3  c ← 0, a vector of LN samples
L4  repeat K times
L5      m ← argmax_t |x[t] + c[t]|;  v ← x[m] + c[m]
L6      if |v| ≤ A then stop
L7      α ← v · (1 - A/|v|)
L8      c[t] ← c[t] - α · p[(t - m) mod LN] for every t
L9  return y = x + c and C = the N in-band values of F_LN c / √L
```

Line L1 is the oversampled OFDM symbol; the zeros go in the middle of the spectrum because the indices $k \ge N/2$ are the negative frequencies. Line L2 builds the kernel once per reserved set. It is the time signal of the indicator of $R$, scaled so that $p[0] = 1$. Every other sample has $|p[t]| \le 1$, and a good set $R$ makes them much smaller. A circular shift of $p$ by $m$ samples multiplies each tone by a phase, so the shifted kernel still lives on $R$. Line L5 finds the largest sample. Line L7 computes the excess over $A$ with the phase of that sample, and line L8 subtracts the shifted kernel times the excess, which sets the sample $m$ to magnitude $A$ exactly. The other samples change by at most $|v| - A$ each, so a new peak can appear; line L5 looks for it on the next pass. Line L9 returns the symbol and the reserved-tone values. The receiver reads the data tones and discards $R$.

## Example

Take $N = 64$ QPSK subcarriers, $L = 4$ and $|R| = 8$ reserved tones, $R = \{10, 28, 30, 31, 34, 37, 39, 41\}$. This set was the best of 200 random sets of 8 tones, by the largest kernel sidelobe $\max_{t \ne 0} |p[t]|$, which is 0.80 for it. Eight equally spaced tones give 1.0 and eight adjacent tones give 0.97. The target is $A^2 = 10^{\gamma/10}\, \sigma^2$, with $\sigma^2 = 56/64$ the mean power per sample of the data alone. The PAPR below is measured on $y$, with the reserved-tone power in the mean. Over 200 random blocks (Python `random.Random(2)`):

| target $\gamma$ | iterations $K$ | mean PAPR | 99 percent below | extra power on $R$ |
|---|---|---|---|---|
| none | 0 | 7.33 dB | 9.62 dB | 0 dB |
| 4 dB | 5 | 5.82 dB | 7.62 dB | 0.47 dB |
| 4 dB | 10 | 5.44 dB | 7.37 dB | 0.56 dB |
| 4 dB | 40 | 5.05 dB | 6.35 dB | 0.74 dB |
| 5 dB | 5 | 5.64 dB | 7.22 dB | 0.28 dB |
| 5 dB | 10 | 5.30 dB | 6.95 dB | 0.34 dB |
| 5 dB | 40 | 4.90 dB | 5.80 dB | 0.48 dB |
| 6 dB | 5 | 6.04 dB | 7.09 dB | 0.12 dB |
| 6 dB | 10 | 5.93 dB | 6.81 dB | 0.14 dB |
| 6 dB | 40 | 5.85 dB | 6.00 dB | 0.16 dB |

With the 6 dB target the result stays near the target and costs little power. A lower target lowers the PAPR further but spends more power on $R$, and with 4 dB the loop cannot reach the target in 40 passes. For a tiny case with $N = 8$, $L = 2$ and one reserved tone, where the convex optimum can be found by a direct search, setting $A$ to the optimal peak makes the loop reach that peak to within 0.1 percent in 200 passes.

## Correctness

The claim is that the output $y$ is the oversampled symbol of $X + C$ with $C$ zero off $R$, so the data tones are exactly $X$, and that each pass that reaches line L8 sets its selected sample to magnitude $A$. The invariant is that $c$ is always the symbol of a vector on $R$. It holds after line L3, and line L8 keeps it because a shifted kernel is the symbol of a phase-rotated indicator of $R$. The step is exact because $p[0] = 1$, so the sample $m$ becomes $v - \alpha = A\, v/|v|$. If the loop stops at line L6, every sample is at most $A$. The correction adds the mean power $\lVert C \rVert^2/N$ and nothing else. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

Lines L1 and L2 cost two inverse [FFTs](/fast-fourier-transform/) of size $LN$, $O(LN \log(LN))$, and the kernel can be stored once for a fixed $R$. Each pass of lines L5 to L8 costs $O(LN)$ for the search and the update. One block therefore costs $O(LN\log(LN) + KLN)$ operations in the real-RAM model, with $O(LN)$ memory. Ten passes for $N = 64$ and $L = 4$ are about 2560 complex multiply-adds plus the searches, similar to the inverse FFT itself.

## Properties

- **Distortionless.** The data subcarriers reach the receiver unchanged. There is no clipping noise in the band of the data.
- **No side information.** The receiver discards the reserved tones and needs no change.
- **Costs subcarriers.** The $|R|$ tones carry no data, here 8 of 64, a rate loss of 12.5 percent.
- **Adds power.** The correction carries power on $R$, between 0.1 and 0.8 dB in the example.
- **Depends on the set.** The kernel sidelobes, and with them the result, depend on which tones are reserved.
- **Not optimal.** The loop gives a valid correction for any $K$ but does not in general reach the convex optimum.

## Variants and improvements

- **Exact optimization.** Minimizing $\max_t |x[t] + c[t]|$ over $C$ on $R$ is a [second-order cone program](/second-order-cone-programming/). For the real-valued baseband signals of [DMT](/discrete-multitone/) in DSL it is a [linear program](/linear-programming-problem/), which is how Tellado first posed it. The solvers are slower than the kernel loop but give the optimum.
- **Clip and project.** Clip $x + c$ at $A$, take the FFT of the clipping noise, keep only its values on $R$ and subtract their time signal. This is a projected gradient step, like [clipping and filtering](/iterative-clipping-and-filtering/) with the band of the correction limited to $R$.
- **Several peaks per pass.** Cancel all samples above $A$ in one pass with one shifted kernel each. This needs fewer passes at the same cost per pass.
- **Tone injection.** Also from Tellado: instead of reserving tones, move some data points to equivalent points of a larger constellation, which the receiver maps back with a modulo operation. It costs no subcarriers but adds power.
- **Standards.** The DVB-T2 broadcasting standard includes tone reservation as an option, with fixed reserved sets.

## When to use it

Use tone reservation when the receiver must not change and no side information can be sent, and the system can spare a few percent of its subcarriers, for example tones that are already unused or are reserved by the standard. It suits DSL and broadcasting. If no tones can be spared, use [active constellation extension](/active-constellation-extension/), which also needs no receiver change. If some side information is acceptable, [selected mapping](/selected-mapping/) and [partial transmit sequences](/partial-transmit-sequence/) cost no subcarriers and no extra power.

## Pitfalls

- **A periodic reserved set.** Choosing $R = \{0, 8, 16, \ldots\}$ in line L2 gives a kernel that repeats 8 times, with sidelobes of magnitude 1, so line L8 creates peaks as tall as the one it removes. Choose $R$ in line L2 by a search for small sidelobes.
- **Data on the reserved tones.** If $X[k] \ne 0$ for some $k \in R$ in line L1, the correction changes those data. Set $X[k] = 0$ on $R$ before line L1; the code raises an error otherwise.
- **An unscaled kernel.** Line L7 assumes $p[0] = 1$. Without the factor $\sqrt N/|R|$ in line L2 the step overshoots or falls short. Keep the scale in line L2.
- **Nyquist-rate samples.** Line L1 with $L = 1$ cancels the sampled peaks only, and the analog peaks between them remain. Use $L \ge 4$ in lines L1 and L2.
- **A target that cannot be reached.** A value of $A$ in line L6 far below what $R$ can achieve makes the loop run all $K$ passes and spend more power on $R$ for little gain, as the 4 dB rows show. Set $A$ in line L6 near a target that the reserved set can reach.

## Implementations

## History

Tellado developed tone reservation in his work on peak reduction for multicarrier transmission at Stanford, first for DSL, where the signals are real and the problem is a linear program. His book of 2000 collects tone reservation, the kernel algorithm and tone injection, with applications to DSL and wireless. The overview of Han and Lee (2005) places it among the distortionless methods that need no side information. It later became an option in the DVB-T2 broadcasting standard.

## References
