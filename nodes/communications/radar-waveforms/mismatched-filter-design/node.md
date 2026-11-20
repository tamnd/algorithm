---
tag: T4GZMK
kind: algorithm
slug: mismatched-filter-design
name: Mismatched filter design
aliases:
- sidelobe suppression filter
- least squares mismatched filter
area: communications/radar-waveforms
level: advanced
summary: "Designs a receive filter that is not the matched filter, by least squares or linear programming, to cut the range sidelobes of a code at a small loss in SNR."
solves: [least-squares-problem]
model: real-ram
complexity:
  vars: {N: the length of the code, L: the length of the filter}
  time: {worst: Θ(N² + L³), average: Θ(N² + L³), best: Θ(N² + L³)}
  space: {extra: Θ(L²)}
properties: {deterministic: true, linear: true, exact_for_rational_codes: true, minimizes_isl: true}
history:
  year: 1973
  people: [M. H. Ackroyd, F. Ghani]
  note: "Ackroyd and Ghani gave the receive filter of least integrated sidelobe energy for a phase code, found from a Toeplitz system of linear equations. Zoraster in 1980 minimized the peak sidelobe instead, by linear programming."
prereqs: [autocorrelation, matched-filter, least-squares-problem, normal-equations]
see_also: [pulse-compression, barker-code, frank-code, phase-coded-waveform, levinson-durbin-recursion, linear-programming-problem, tikhonov-regularization, window-functions]
sources:
  - paper: "M. H. Ackroyd and F. Ghani, IEEE Transactions on Aerospace and Electronic Systems 9(2), 1973, pp. 214 to 218"
    title: Optimum mismatched filters for sidelobe suppression
    locator: "the whole paper (the filter of least integrated sidelobe energy at a fixed peak, from the normal equations of the code)"
  - paper: "S. Zoraster, IEEE Transactions on Aerospace and Electronic Systems 16(1), 1980, pp. 112 to 115"
    title: Minimum peak range sidelobe filters for binary phase-coded waveforms
    locator: "the whole paper (the filter of least peak sidelobe, as a linear program)"
  - book: isbn:9780471473787
    title: "Nadav Levanon and Eli Mozeson, Radar Signals, Wiley, 2004"
    locator: "Chapter 6, Phase-Coded Pulse (binary and polyphase codes and their sidelobes)"
---

A mismatched filter is a receive filter for a [phase-coded waveform](/phase-coded-waveform/) that is chosen to give low range sidelobes, not the largest signal to noise ratio. The [matched filter](/matched-filter/) of [pulse compression](/pulse-compression/) gives the best signal to noise ratio, but its output has the sidelobes of the code's [autocorrelation](/autocorrelation/). A longer filter, designed by least squares, trades a small loss in signal to noise ratio, usually a few tenths of a dB, for sidelobes that are 10 to 30 dB lower. The least squares filter minimizes the integrated sidelobe level, and a linear program minimizes the peak sidelobe level instead.

## In plain words

A radar sends a coded pulse and correlates the echo with a copy of the code. The result has a tall peak where the target is, but also small bumps on each side. A large target's bumps can hide a small target nearby. You can replace the copy of the code with a different, slightly longer set of weights. You choose these weights so that the output is as close as possible to a single spike, with nothing on either side. This is a standard fitting problem with a direct solution. The peak becomes a little weaker against the noise, and the bumps become much smaller. If the longest bump matters more than the total, you can choose the weights for that goal.

## The problem

The code is $s[0], \dots, s[N-1]$, with $s$ not all zero. The filter is $h[0], \dots, h[L-1]$, and its output is the convolution $y[m] = \sum_i h[i]\, s[m-i]$ for $m = 0, \dots, N + L - 2$. Choose a peak index $c$, by default $c = \lfloor (N + L - 2)/2 \rfloor$ (the center). Find $h$ that minimizes

$$\sum_{m} |y[m] - \delta[m - c]|^2,$$

and scale it to $y[c] = 1$. The quality measures are the peak sidelobe level $\mathrm{PSL} = \max_{m \ne c} |y[m]|^2 / |y[c]|^2$, the integrated sidelobe level $\mathrm{ISL} = \sum_{m \ne c} |y[m]|^2 / |y[c]|^2$, and the loss in signal to noise ratio against the matched filter in white noise, $\ell = |y[c]|^2 / (\|h\|^2 \|s\|^2)$. With $L = N$ and $h[i] = \overline{s[N-1-i]}/\|s\|^2$, the filter is the matched filter, and $\ell = 1$.

## The algorithm

The normal equations of the least squares problem are a Toeplitz system built from the code's aperiodic autocorrelation.

```pseudo id=main
LS-MISMATCHED-FILTER(s[0..N-1], L, c)
L1  r[k] <- sum over n of s[n + k] * conj(s[n]),  k = 0 .. N-1
L2  R[i][j] <- r[i - j] if i >= j, conj(r[j - i]) if i < j, 0 if |i - j| >= N,  0 <= i, j < L
L3  e[i] <- conj(s[c - i]) if 0 <= c - i < N, else 0,  i = 0 .. L-1
L4  g <- the solution of R g = e
L5  p <- sum over i of conj(e[i]) * g[i]                  ▷ p = e^H R^-1 e, real and positive
L6  return h = g / p                                       ▷ scaled so that y[c] = 1
```

Line L4 is solved by Gaussian elimination in the implementation. Because $R$ is Toeplitz and positive definite, the [Levinson-Durbin recursion](/levinson-durbin-recursion/) or a [Cholesky decomposition](/cholesky-decomposition/) also works. The least integrated sidelobe level that results is $1/p - 1$, with no need to compute the output.

## Example

Take the Barker code of length 3, $s = (1, 1, -1)$, and a filter of length $L = 3$, so $c = 2$. Line L1 gives $r = (3, 0, -1)$, and lines L2 and L3 give

$$R = \begin{pmatrix} 3 & 0 & -1 \\ 0 & 3 & 0 \\ -1 & 0 & 3 \end{pmatrix}, \qquad e = (-1, 1, 1).$$

Line L4 gives $g = (-\tfrac14, \tfrac13, \tfrac14)$, line L5 gives $p = \tfrac14 + \tfrac13 + \tfrac14 = \tfrac56$, and line L6 returns $h = (-\tfrac{3}{10}, \tfrac25, \tfrac{3}{10})$. The two filters give:

| Filter | Output $y$ | PSL | ISL | Loss |
|---|---|---|---|---|
| matched, $(-1, 1, 1)/3$ | $(-\tfrac13, 0, 1, 0, -\tfrac13)$ | $-9.54$ dB | $\tfrac29$ ($-6.53$ dB) | 0 dB |
| least squares, $L = 3$ | $(-\tfrac{3}{10}, \tfrac{1}{10}, 1, -\tfrac{1}{10}, -\tfrac{3}{10})$ | $-10.46$ dB | $\tfrac15$ ($-6.99$ dB) | 0.086 dB |
| least squares, $L = 5$ | $(\tfrac{2}{13}, -\tfrac{3}{26}, \tfrac{1}{26}, 1, -\tfrac{1}{26}, -\tfrac{3}{26}, -\tfrac{2}{13})$ | $-16.26$ dB | $\tfrac{1}{13}$ ($-11.14$ dB) | 0.849 dB |

The ISL of $\tfrac15$ equals $1/p - 1 = \tfrac65 - 1$, and the loss for $L = 3$ is exactly $\tfrac{50}{51}$. For $L = 5$ the filter is $h = (\tfrac{2}{13}, -\tfrac{7}{26}, \tfrac{6}{13}, \tfrac{7}{26}, \tfrac{2}{13})$ and the loss is $\tfrac{338}{411}$. The least squares filter puts small nonzero values where the matched output was zero, and lowers the two outer sidelobes more.

## Correctness

The output is $y = Ch$ with the convolution matrix $C[m][i] = s[m-i]$. Then $C^H C = R$, the matrix of line L2, and the column of $C^H$ at index $c$ is $e$, the vector of line L3. So line L4 solves the normal equations of the least squares problem. $R$ is positive definite, because the convolution of a nonzero filter with a nonzero code is never all zero, so the solution is unique. For every filter, $y[c] = e^H h$ and the energy of the output is $h^H R h$. The Cauchy-Schwarz inequality in the inner product $u^H R v$ then gives $\mathrm{ISL} \ge 1/(e^H R^{-1} e) - 1$, with equality only for multiples of $g$. So the least squares filter is also the filter of least ISL at a fixed peak (a theorem). The loss is at most 1, with equality only for the matched filter, and the least ISL never rises when $L$ grows. The full proofs are below.

## Complexity

**Time.** Line L1 costs $\Theta(N^2)$ and line L2 costs $\Theta(L^2)$. Gaussian elimination in line L4 costs $\Theta(L^3)$, which gives $\Theta(N^2 + L^3)$ in total. The Levinson-Durbin recursion uses the Toeplitz form and solves line L4 in $\Theta(L^2)$. Line L1 can use the FFT and cost $O(N \log N)$.

**Space.** $\Theta(L^2)$ for the matrix, or $\Theta(L)$ with the Levinson-Durbin recursion, which needs only the first row.

## Properties

The values below are measurements made with the implementation, in exact rational arithmetic for the binary codes. The loss is the loss in signal to noise ratio against the matched filter. The matched filter of the Barker code of length 13 gives a PSL of $-22.28$ dB, an ISL of $-11.49$ dB and no loss. The matched filter of the [Frank code](/frank-code/) of length 16 gives a PSL of $-21.07$ dB and an ISL of $-9.03$ dB.

| Code | $L$ | PSL | ISL | Loss |
|---|---|---|---|---|
| Barker 13 | 13 | $-24.00$ dB | $-15.68$ dB (exactly $\tfrac{1}{37}$) | 0.143 dB |
| Barker 13 | 21 | $-27.20$ dB | $-17.92$ dB | 0.159 dB |
| Barker 13 | 27 | $-28.28$ dB | $-19.77$ dB | 0.179 dB |
| Barker 13 | 39 | $-38.47$ dB | $-30.03$ dB | 0.204 dB |
| Barker 13 | 51 | $-48.37$ dB | $-40.67$ dB | 0.213 dB |
| Barker 13 | 65 | $-58.59$ dB | $-49.60$ dB | 0.214 dB |
| Frank 16 | 16 | $-20.32$ dB | $-11.07$ dB | 0.210 dB |
| Frank 16 | 47 | $-30.76$ dB | $-18.77$ dB | 0.664 dB |

- **Least ISL at unit peak (theorem).** No filter of the same length and peak index has a lower ISL. In 200 random exact changes of the filter for the Barker code of length 7 with $L = 11$ that kept the peak at 1 (seed 7301), every change raised the ISL.
- **The least ISL is $1/(e^H R^{-1} e) - 1$ (closed form).** It agreed exactly with the ISL of the output for the Barker codes of lengths 3, 7, 11 and 13 and the filter lengths $L = N, N + 2, \dots, 2N + 1$.
- **A longer filter is never worse (theorem).** A filter of length $L$ padded with one zero is a filter of length $L + 1$ with the same output. For the Barker code of length 13, the least ISL is $\tfrac{1}{37}$ for $L = 13, 14, 15$ and falls at every step after that, up to $L = 65$.
- **The loss stays small for the good codes (measurement).** For Barker 13 it stays near 0.2 dB as $L$ grows. Codes with poor sidelobes to start with, such as Barker 11 at large $L$ (0.94 dB at $L = 39$), lose more.
- **Linear and exact.** The filter is an [FIR filter](/fir-filter/), and for a code with rational chips every value is rational.

## Variants and improvements

- **Minimum peak sidelobe by linear programming.** To minimize the largest sidelobe, minimize $t$ subject to $y[c] = 1$ and $|y[m]| \le t$ for $m \ne c$. For a real code these are linear constraints, a [linear program](/linear-programming-problem/) (Zoraster, 1980). For a complex code the constraints are second order cones.
- **Weighted least squares.** Give more weight to the sidelobes near the peak, or to a region of range where weak targets are expected. The normal equations keep the same form with a diagonal weight in the output.
- **Doppler tolerance.** A filter designed at zero Doppler can lose its low sidelobes for a moving target. Design over a set of Doppler shifts, by stacking the least squares problems for several shifted copies of the code.
- **A noise term.** Minimize $\|Ch - d\|^2 + \lambda \|h\|^2$. This is [Tikhonov regularization](/tikhonov-regularization/), which adds $\lambda$ to the diagonal of $R$ and limits the loss in signal to noise ratio.
- **Amplitude weighting.** For a chirp, a [window](/window-functions/) on the matched filter is the simple form of a mismatched filter. A Hamming weight gives about $-43$ dB sidelobes at a loss of 1.34 dB.

## When to use it

Use a mismatched filter when a strong echo can mask a weak one nearby in range and the code is fixed, for example a Barker or polyphase code in a pulse radar, a sonar or a channel sounder. Use the least squares form when the total sidelobe energy matters, for example with extended clutter, and the linear program when one sidelobe matters, for example a single strong target. If the signal to noise ratio is the only goal, keep the matched filter. If the code can be changed, a better code, such as a polyphase code with low autocorrelation sidelobes, is often the cheaper fix.

## Pitfalls

- **Expecting the peak sidelobe to fall.** Least squares minimizes the ISL, not the PSL. For the Barker code of length 11 with $L = 11$, the ISL falls from $-10.83$ dB to $-11.14$ dB, but the PSL rises from $-20.83$ dB to $-19.78$ dB.
- **Doppler mismatch.** The design assumes the echo is the code itself. A Doppler shift changes the phase across the code, and the low sidelobes can rise again. Check the filter on the [ambiguity function](/ambiguity-function/) of the code, not only at zero Doppler.
- **The peak index.** With $c$ far from the center, the filter cannot cancel the sidelobes on one side and the result is poor. Use the center unless there is a reason not to.
- **Forgetting the conjugates in lines L2 and L3.** For a polyphase code, $R$ is Hermitian, not symmetric, and $e$ holds the conjugated code. Without the conjugates the system is wrong, although a binary code gives the right answer.
- **Measuring the loss against the wrong reference.** The loss compares with the matched filter of the same code in white noise. It is not the change in the peak value, which depends on the scale of $h$.

## Implementations

## History

The matched filter of North (1943) was the starting point for pulse compression. Barker codes (1953) gave binary codes with sidelobes of magnitude 1, which no binary code can improve with its matched filter. In 1973, M. H. Ackroyd and F. Ghani gave the filter of least integrated sidelobe energy for a phase code as the solution of a linear system built from the autocorrelation of the code. In 1980, S. Zoraster formulated the filter of least peak sidelobe for a binary code as a linear program. Later work added Doppler tolerance, weights and constraints from convex optimization.

## References
