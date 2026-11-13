---
tag: 546JYA
kind: algorithm
slug: iir-filter
name: IIR filter
aliases:
- infinite impulse response filter
- recursive filter
area: graphics-and-signals/signal-processing
level: core
summary: "Compute y[n] from recent inputs and recent outputs, H(z) = B(z)/A(z). Few coefficients give a sharp response, but it is stable only if all poles are inside the unit circle."
solves: [digital-filtering]
model: real-ram
complexity:
  vars: {P: the filter order (the larger degree of B and A), N: the number of input samples}
  time: {worst: Θ(N P), average: Θ(N P), best: Θ(N P), per_sample: Θ(P)}
  space: {extra: Θ(P)}
properties: {causal: true, stable: "if and only if all poles are inside the unit circle", linear_phase: false, online: true, deterministic: true, recursive: true, in_place: false}
history:
  year: 1967
  people: [Charles M. Rader, Bernard Gold]
  note: Rader and Gold gave a systematic account of recursive digital filters and their design from the z-transform in 1967.
prereqs: [z-transform, transfer-function, fir-filter]
see_also: [bilinear-transform, butterworth-filter, digital-filter-design, bibo-stability, schur-cohn-test, minimum-phase, partial-fraction-decomposition, linear-prediction]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 6, Structures for Discrete-Time Systems (direct forms I and II, the transposed forms, cascade and parallel forms, and the effects of coefficient quantization), and Chapter 3, The z-Transform (the region of convergence and the stability of rational systems)
  - book: isbn:9780131873742
    title: John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007
    locator: the chapter on the implementation of discrete-time systems (structures for IIR systems and lattice structures), and the chapter on the z-transform (the Schur-Cohn stability test)
  - paper: doi:10.1109/PROC.1967.5434
    title: Charles M. Rader and Bernard Gold, Digital Filter Design Techniques in the Frequency Domain, Proceedings of the IEEE 55(2), 1967
    locator: pp. 149 to 171 (recursive digital filters, their design from analog filters and from frequency specifications)
---

An infinite impulse response (IIR) filter computes each output sample from the current and past inputs and from its own past outputs: $y[n] = \sum_{k=0}^{P} b[k]\, x[n-k] - \sum_{k=1}^{P} a[k]\, y[n-k]$. The feedback makes the [impulse response](/impulse-response/) last forever, and it lets a filter of low order $P$ reach a sharp cutoff that an [FIR filter](/fir-filter/) needs many more taps for. The cost is $2P + 1$ multiplies per output sample. The [transfer function](/transfer-function/) $H(z) = B(z)/A(z)$ has poles, and the filter is stable if and only if every pole is inside the unit circle $|z| < 1$. A causal and stable IIR filter cannot have exactly linear phase. Frequencies on this page are in radians per sample, $\omega \in [-\pi, \pi]$.

## In plain words

An IIR filter has a memory of its own output. Each new output is a mix of the new input, a few old inputs and a few old outputs. Because the output feeds back into itself, one spike at the input makes a response that dies away slowly but never quite stops.

The feedback makes the filter cheap. A few numbers can give a filter that cuts off very sharply. But feedback can also grow. If the old outputs get too much weight, the response gets larger at each step and the filter blows up. So you must check that the filter is stable before you use it. Also, the filter delays different tones by different amounts, so it changes the shape of a pulse.

## The problem

The input is a stream $x[0], x[1], \ldots$ and the coefficients of $B(z) = \sum_{k=0}^{P} b[k] z^{-k}$ and $A(z) = 1 + \sum_{k=1}^{P} a[k] z^{-k}$. Pad the shorter list with zeros so that both have length $P + 1$. If $a[0] \ne 1$, divide all coefficients by $a[0]$ first. Samples and outputs before $n = 0$ are zero. The output is the solution of the difference equation

$$y[n] + \sum_{k=1}^{P} a[k]\, y[n-k] = \sum_{k=0}^{P} b[k]\, x[n-k], \qquad n \ge 0,$$

which in the [z-transform](/z-transform/) domain is $A(z) Y(z) = B(z) X(z)$, so $H(z) = B(z)/A(z)$. This is one way to solve [digital filtering](/digital-filtering/).

## The algorithm

The transposed direct form II keeps $P$ state values $z[0 \ldots P-1]$. Each state is a partial sum of the terms of the difference equation that will be needed in later steps.

```pseudo id=main
IIR-FILTER(b[0 .. P], a[0 .. P], x)         ▷ a[0] = 1
L1  z[0 .. P − 1] ← 0                         ▷ the state
L2  for each new input v = x[n] do
L3      out ← b[0] · v + z[0]
L4      for i ← 0 to P − 2 do
L5          z[i] ← b[i + 1] · v − a[i + 1] · out + z[i + 1]
L6      z[P − 1] ← b[P] · v − a[P] · out
L7      output y[n] ← out
```

Line L5 reads $z[i+1]$ before the loop writes it, because $i$ goes up. The state is the only memory, so the form uses $P$ cells, not the $2P$ cells of the direct form I that stores $P$ inputs and $P$ outputs.

**Stability test.** The filter is [BIBO stable](/bibo-stability/) if and only if all roots of $z^P A(z)$ are inside the unit circle, when $B$ and $A$ have no common root. The Schur-Cohn step-down recursion decides this without finding the roots, see the [Schur-Cohn test](/schur-cohn-test/). Set $c = A$. While $c$ has degree $p \ge 1$, take the reflection coefficient $k_p = c[p]$. If $|k_p| \ge 1$, the filter is unstable. Else replace $c$ by the polynomial of degree $p - 1$ with $c'[i] = (c[i] - k_p c[p - i])/(1 - k_p^2)$. The filter is stable if and only if all $|k_p| < 1$. With rational coefficients this test is exact.

## Example

**One pole.** Take $b = [\tfrac12]$ and $a = [1, -\tfrac12]$, so $y[n] = \tfrac12 y[n-1] + \tfrac12 x[n]$ and $H(z) = \tfrac12 / (1 - \tfrac12 z^{-1})$. The pole is $z = \tfrac12$. The impulse response is $h[n] = (\tfrac12)^{n+1}$, which is never zero. The unit step $x = [1, 1, 1, 1, 1]$ gives

| $n$ | $z[0]$ before | $y[n]$ | $z[0]$ after $= \tfrac12 y[n]$ |
|---|---|---|---|
| 0 | 0 | $\tfrac12$ | $\tfrac14$ |
| 1 | $\tfrac14$ | $\tfrac34$ | $\tfrac38$ |
| 2 | $\tfrac38$ | $\tfrac78$ | $\tfrac{7}{16}$ |
| 3 | $\tfrac{7}{16}$ | $\tfrac{15}{16}$ | $\tfrac{15}{32}$ |
| 4 | $\tfrac{15}{32}$ | $\tfrac{31}{32}$ | $\tfrac{31}{64}$ |

The output approaches the gain $H(1) = 1$ and halves its distance to it at each step. One multiply per term of $B$ and one per term of $A$ give a smoothing filter with an infinitely long memory.

**Two poles.** Take $b = [1]$ and $A(z) = 1 - \tfrac32 z^{-1} + \tfrac{14}{25} z^{-2} = (1 - 0.7 z^{-1})(1 - 0.8 z^{-1})$. The step-down recursion gives $k_2 = \tfrac{14}{25}$, then $c' = [1, -\tfrac{25}{26}]$ and $k_1 = -\tfrac{25}{26}$. Both have modulus below 1, so the filter is stable. By partial fractions the impulse response is $h[n] = 8 (0.8)^n - 7 (0.7)^n$, which starts $1, \tfrac32, \tfrac{169}{100}, \tfrac{339}{200}$ and then decays. For $A(z) = 1 - \tfrac74 z^{-1} + \tfrac58 z^{-2}$, with poles $0.5$ and $1.25$, the recursion gives $k_2 = \tfrac58$ and $k_1 = -\tfrac{14}{13}$, so the filter is unstable, and its impulse response grows like $1.25^n$.

## Correctness

The proof uses one [loop invariant](/loop-invariant/). At the start of the step for $x[n]$, each state holds the part of the future difference equation that is already known:

$$z[i] = \sum_{k=i+1}^{P} \big(b[k]\, x[n+i-k] - a[k]\, y[n+i-k]\big), \qquad i = 0, \ldots, P-1.$$

For $i = 0$ this gives $b[0]\, x[n] + z[0] = y[n]$ at line L3, which is the difference equation. Lines L5 and L6 add the terms of $k = i + 1$, which use $x[n]$ and $y[n]$, to the shifted old state, which restores the invariant for $n + 1$. The stability test is correct because each step-down keeps the number of roots inside the unit circle when $|k_p| < 1$. The full proofs are in the proof file.

## Complexity

- **Per output sample:** at most $2P + 1$ multiplies and $2P$ additions, so $\Theta(P)$. This is the cost model of the area: an IIR filter costs $O(\text{order})$ per sample.
- **For $N$ samples:** $\Theta(NP)$ time.
- **Space:** $P$ state cells and $2P + 1$ coefficients.
- **Stability test:** $O(P^2)$ arithmetic operations, once, before filtering.

For a sharp magnitude specification, an IIR filter needs a lower order than an FIR filter needs taps, and the gap grows as the transition band gets narrower. The [digital filter design](/digital-filter-design/) page compares the two on one specification. The Chebyshev and elliptic families reach a given specification with a lower order than the Butterworth family. The IIR filter gives up linear phase for this saving.

## Properties

- **Causal.** The output $y[n]$ uses $x[n], \ldots, x[n-P]$ and $y[n-1], \ldots, y[n-P]$.
- **Stable if and only if all poles are inside the unit circle.** A pole outside makes a term $r^n$ with $|r| > 1$ in the impulse response, so $\sum |h[n]|$ is infinite. With all poles inside, $|h[n]| \le C \rho^n n^{P}$ for the largest pole modulus $\rho < 1$, and the sum is finite.
- **No exact linear phase.** A real causal filter with linear phase has $h[n] = \pm h[M - n]$ for some $M$, so a causal $h$ must end at $n = M$, and the filter is FIR.
- **Infinite memory.** One input sample affects all later outputs. A start-up transient decays like $\rho^n$, not in a fixed number of samples.
- **Sensitive to rounding.** The poles of a high order polynomial move a lot when its coefficients are rounded, and a pole can leave the unit circle.

## Variants and improvements

- **Direct form I and direct form II.** Direct form I stores $P$ inputs and $P$ outputs. Direct form II runs the poles first and the zeros second with one shared delay line. The transposed form II above has the same cost and keeps the partial sums small.
- **Cascade of second-order sections.** Factor $H(z)$ into sections of order 2, each with one pair of complex poles. Each section has small coefficients that place its poles well. This is the standard form for orders above about 4, see the pitfalls.
- **Parallel form.** Write $H(z)$ by [partial fraction decomposition](/partial-fraction-decomposition/) as a sum of first and second order sections and add their outputs.
- **Lattice form.** The reflection coefficients of the stability test are the multipliers of the lattice filter. The filter is stable exactly when each multiplier has modulus below 1, so the stability is easy to keep after quantization. The same coefficients appear in [linear prediction](/linear-prediction/).
- **Zero-phase filtering.** Run a stored signal through the filter forwards and then backwards. The phase cancels and the magnitude is squared. This is not causal.
- **Design.** Most IIR filters come from an analog prototype, such as a [Butterworth filter](/butterworth-filter/), mapped to the digital domain with the [bilinear transform](/bilinear-transform/). See [digital filter design](/digital-filter-design/).

## When to use it

Use an IIR filter when you need a sharp magnitude response at a low cost per sample and the phase does not matter, or matters only in the pass band: audio equalizers, tone detection, DC removal, control loops and sensor smoothing. Use a one-pole filter as a cheap smoother with an infinitely long memory. Use an [FIR filter](/fir-filter/) instead when you need linear phase, a guaranteed stable filter in fixed point arithmetic, or a polyphase multirate structure.

## Pitfalls

- **High order in one direct form.** The poles of a direct form filter of order 7 or more move a lot when the coefficients are rounded. For a digital Butterworth filter of order 7 with the cutoff $\omega_c = 0.2$, the error of the computed $|H|^2$ in one direct form reaches about $10^{-9}$ in double precision, millions of times the rounding unit. Use second-order sections.
- **Unchecked stability.** A design that is stable on paper can become unstable after the coefficients are rounded. Check the rounded coefficients, for example with the step-down test.
- **The sign of $a$.** Some texts write the feedback as $+\sum a[k]\, y[n-k]$. Check the convention before you copy coefficients.
- **Forgetting $a[0]$.** If $a[0] \ne 1$, all coefficients must be divided by it.
- **Limit cycles.** In fixed point arithmetic, rounding in the feedback can make a small oscillation that never decays, even with zero input.
- **Phase distortion.** The group delay of a sharp IIR filter peaks near the band edge. Pulses and transients change shape there.

## Implementations

## History

Recursive filters were used on sampled data in control and in radar in the 1950s. In 1967 Charles Rader and Bernard Gold published a systematic account of digital filters in the frequency domain. They described recursive filters through the z-transform, their design from analog filters and directly from a frequency specification. The lattice form and its link to the stability test followed in the 1970s with the work of Gray and Markel.

## References
