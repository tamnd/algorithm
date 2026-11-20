---
tag: FDWZTR
kind: algorithm
slug: minimum-entropy-deconvolution
name: Minimum entropy deconvolution
aliases:
- MED
area: imaging-and-inverse-problems/seismic-imaging
level: advanced
summary: "Find the filter whose output is most spiky, measured by the varimax norm, by a fixed-point iteration. It needs no minimum-phase wavelet and no white reflectivity."
model: real-ram
complexity:
  vars: {n: the number of samples of each trace, m: the number of traces, L: the number of filter taps, k: the number of iterations}
  time: {worst: O(k (m n L + L^3)), average: O(k (m n L + L^3)), best: O(m n L + L^3)}
  space: {extra: O(m (n + L^2))}
properties: {deterministic: true, linear_in_data: false, assumes: "sparse reflectivity", phase_assumption: none, ascent: "not guaranteed", global_maximum: "not guaranteed"}
history:
  year: 1978
  people: [Ralph A. Wiggins]
  note: Wiggins (1978) proposed to choose the deconvolution filter that maximizes the varimax norm of the output, a measure of simplicity, and solved for it by an iteration in which each step solves a Toeplitz system.
prereqs: [predictive-deconvolution, seismic-reflection-model]
see_also: [fixed-point-iteration, independent-component-analysis, sparse-signal-recovery, discrete-convolution, toeplitz-system-solving, iteratively-reweighted-least-squares, minimum-phase, cepstrum]
sources:
  - paper: doi:10.1016/0016-7142(78)90005-4
    title: Ralph A. Wiggins, Minimum entropy deconvolution, Geoexploration 16(1-2), 1978, 21 to 35
    locator: the varimax norm as a measure of simplicity of the output, and the iterative solution for the filter that maximizes it over several traces
  - paper: doi:10.1111/j.1365-2478.1979.tb00979.x
    title: M. Ooe and T. J. Ulrych, Minimum entropy deconvolution with an exponential transformation, Geophysical Prospecting 27(2), 1979, 458 to 473
    locator: a change of the simplicity measure by an exponential transformation of the output
  - paper: doi:10.1190/1.1441919
    title: Carlos A. Cabrelli, Minimum entropy deconvolution and simplicity, a noniterative algorithm, Geophysics 50(3), 1985, 394 to 413
    locator: a different simplicity measure and an algorithm without iteration
---

Minimum entropy deconvolution (MED) designs a deconvolution filter without a model of the wavelet. It assumes only that the reflectivity is sparse, a few strong spikes with small values in between, and looks for the filter that makes the output as spiky as possible. Spikiness is measured by the varimax norm, the sum of fourth powers of the output divided by the square of the sum of squares. The filter comes from a [fixed-point iteration](/fixed-point-iteration/): each step solves a Toeplitz system built from the current output. Unlike [predictive deconvolution](/predictive-deconvolution/), it does not assume a minimum-phase wavelet or a white reflectivity, so it can compress a mixed-phase wavelet in the [convolutional model of a trace](/seismic-reflection-model/).

## In plain words

A trace is a list of sharp echoes, smeared by the shape of the sound pulse. Smearing spreads each echo over many samples, so the trace looks busy and even. A good filter undoes the smear and leaves a few big samples among many small ones. The method gives every candidate filter a score: high when a few samples hold most of the energy, low when the energy is spread evenly. It then looks for the filter with the highest score. It starts from a filter that changes nothing, sees which output samples are big, builds a new filter that makes those samples bigger still, and repeats. It does not need to know anything about the shape of the pulse, only that the true echoes are few.

## The problem

Input: traces $x_1, \ldots, x_m$ of $n$ samples; the filter length $L$; the number of iterations. Output: a filter $f$ of $L$ taps with $\|f\| = 1$ and the outputs $y_i = f * x_i$ (full convolutions). The filter should maximize
$$\Phi(f) = \sum_{i=1}^{m} V(y_i), \qquad V(y) = \frac{\sum_t y_t^4}{\big(\sum_t y_t^2\big)^2}.$$
For an output of $T$ samples, $V$ lies between $1/T$ (all samples of equal size) and $1$ (one nonzero sample). $V$ does not change when $f$ is scaled, so only the direction of $f$ matters, and the output is fixed only up to a scale, a sign and a time shift. The varimax norm is a fourth moment over the square of a second moment, a kurtosis-like measure, which is why MED is related to [independent component analysis](/independent-component-analysis/), which also maximizes such a contrast.

## The algorithm

```pseudo id=main
MED(x_1 … x_m, L, iters)
L1  f ← spike at tap ⌊L/2⌋;  R_i ← autocorrelation matrix of x_i (L × L, Toeplitz)
L2  repeat iters times, or until f stops changing
L3      y_i ← f * x_i for every trace
L4      E_i ← Σ_t y_it²;  F_i ← Σ_t y_it⁴;  w_i ← F_i / E_i³
L5      A ← Σ_i w_i R_i
L6      c ← Σ_i b_i / E_i²,  where b_ik = Σ_t y_it³ x_i,t-k
L7      f ← the solution of A f = c, scaled to unit length
L8  return f
```

The gradient of $\Phi$ is $4\sum_i (b_i E_i - F_i R_i f)/E_i^3$, so it is zero exactly when $A f = c$ with $A$ and $c$ taken at $f$. Line L7 solves this equation with $A$ and $c$ frozen at the current filter, and the next step updates them. The vector $b_i$ is the cross-correlation of the cubed output with the input: cubing makes the large samples dominate, so each step pulls the filter toward the one that predicts the current large samples. The start at the center tap lets the filter shift the output both ways, which a mixed-phase inverse needs.

## Example

**The measure.** For $T = 4$ samples, $V(1, 0, 0, 0) = 1$, $V(1, -1, 0, 0) = 2/4 = 0.5$ and $V(1, 1, 1, 1) = 4/16 = 0.25 = 1/T$.

**A mixed-phase wavelet.** A reflectivity of 300 samples has a Gaussian value with probability 0.05 and zero otherwise (seed 6). It is convolved with the wavelet $(0.3, -0.8, 1.0, -0.4)$. The polynomial $0.3 - 0.8z + z^2 - 0.4z^3$ has the zero $1.5$ outside the unit circle and the zeros $0.5 \pm 0.5i$ inside it, so the wavelet is mixed phase and a minimum-phase method would not compress it correctly. MED with $L = 15$ taps gives:

| | reflectivity | trace | MED output |
|---|---|---|---|
| varimax norm $V$ | 0.1948 | 0.0813 | 0.2144 |
| best normalized correlation with the reflectivity | 1 | 0.733 | 0.964 |

The correlation is the largest over time shifts, with the sign ignored, because MED fixes neither. The values of $\Phi$ over the iterations were $0.0813$, $0.1433$, $0.2067$, $0.2144$, and then stayed at $0.2144$ to four digits; the iteration stopped after 23 steps, when the change of $f$ fell below $10^{-12}$, with a gradient of size $4.5 \times 10^{-13}$. The output has a higher varimax norm than the true reflectivity: the filter found a spikier signal than the earth's own. These numbers are measurements on one seed.

## Correctness

The varimax norm lies in $[1/T, 1]$, with $1$ for a single spike and $1/T$ for samples of equal size (a theorem, by the Cauchy-Schwarz inequality). $\Phi$ does not change when $f$ is scaled. The gradient has the closed form above. The matrix $A$ is a positive combination of autocorrelation matrices of nonzero traces, so it is symmetric positive definite and line L7 has exactly one solution. A unit filter is a fixed point of lines L3 to L7 if and only if the gradient of $\Phi$ is zero there; so a limit of the iteration is a stationary point of $\Phi$. These are theorems; the proofs are in proofs/correctness.md. They do not say that the iteration converges, that $\Phi$ grows at each step, or that the stationary point is the global maximum. Fast convergence and a growing $\Phi$ are measurements on test data.

## Complexity

In the real-RAM model one iteration costs $O(m n L)$ for the convolutions and the cross terms, $O(m L^2)$ to form $A$, and $O(L^3)$ for a dense solve. $A$ is a weighted sum of Toeplitz matrices and so is Toeplitz, and the [Levinson-Durbin recursion](/levinson-durbin-recursion/) solves it in $O(L^2)$. With $k$ iterations the total is $O(k (m n L + L^3))$, or $O(k\, m n L)$ with Levinson when $L \le n$. The code stores the $m$ autocorrelation matrices, $O(m (n + L^2))$ space.

## Properties

- No phase assumption: the filter can be mixed phase, and so can the wavelet (the example above is a measurement).
- The output is fixed only up to a scale, a sign and a time shift (a theorem: scaling $f$ or changing its sign does not change $\Phi$, and moving the taps of $f$ within the $L$ taps only shifts the full output, so it does not change $\Phi$ either).
- Not linear: the filter depends on the data through the fourth powers of the output.
- One filter for many traces: the sum over traces makes the filter fit the common wavelet and not the details of one trace.
- Sensitive to noise and to the filter length: a long filter can make a noise burst into a spike (a heuristic, seen in practice).

## Variants and improvements

- Other simplicity measures: Ooe and Ulrych (1979) apply an exponential transformation to the output; Cabrelli (1985) uses a different norm and an algorithm without iteration.
- Gradient ascent or Newton steps on $\Phi$, with a line search that makes each step increase $\Phi$.
- Sparse deconvolution with an $\ell_1$ penalty on the output, solved by [iteratively reweighted least squares](/iteratively-reweighted-least-squares/) or other methods of [sparse signal recovery](/sparse-signal-recovery/); it fits a known or estimated wavelet and asks for a sparse reflectivity.
- Phase estimation: maximize a kurtosis-like measure over a single parameter, a constant phase rotation of the output of another deconvolution, in place of a full filter (a heuristic with far fewer unknowns).

## When to use it

Use it when the wavelet is not minimum phase, the reflectivity has a few strong contrasts, and there are several traces with the same wavelet. Prefer predictive deconvolution when the reflectivity is close to white and the wavelet is minimum phase, because it is linear in the autocorrelation, fast and well understood.

## Pitfalls

- The sparsest output is not always the true reflectivity. A long filter can concentrate energy in a few samples that are not reflections, and on a short record the output can be spikier than the reflectivity, as in the example.
- The iteration can stop at a stationary point that is not the global maximum. Try several starting filters, for example spikes at different taps.
- The time shift of the output is not fixed: compare outputs with a reference only after an alignment.
- On a single short trace the result varies a lot from record to record; use as many traces as possible with the same wavelet.
- Noise bursts and spikes in the input are amplified: edit them out first.

## Implementations

## History

Wiggins (1978) named the method minimum entropy deconvolution, with the idea that a spiky output is simple and has low entropy, and used the varimax norm, a measure taken from factor analysis, to score the output. He maximized the sum of the norms over several traces with an iteration that solves a Toeplitz system at each step. Ooe and Ulrych (1979) changed the measure with an exponential transformation, and Cabrelli (1985) proposed another simplicity norm with an algorithm that needs no iteration.

## References
