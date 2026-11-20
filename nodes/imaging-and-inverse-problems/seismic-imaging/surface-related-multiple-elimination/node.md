---
tag: JC2TNG
kind: algorithm
slug: surface-related-multiple-elimination
name: Surface-related multiple elimination
aliases:
- SRME
area: imaging-and-inverse-problems/seismic-imaging
level: advanced
summary: "Predict the surface multiples by convolving the recorded data with itself over the surface positions, then remove them, exactly by one inverse per frequency or by iteration."
model: real-ram
complexity:
  vars: {f: the number of frequencies, s: the number of surface positions, K: the number of iterations}
  time: {worst: O(f s^3), average: O(f s^3), best: O(f s^3)}
  space: {extra: O(f s^2)}
properties: {deterministic: true, data_driven: true, needs_subsurface_model: false, exact_under_model: true, iteration_converges: "if the spectral radius of aP is below 1", adaptive_subtraction: heuristic}
history:
  year: 1992
  people: [D. J. Verschuur, A. J. Berkhout, C. P. A. Wapenaar]
  note: Verschuur, Berkhout and Wapenaar (1992) gave surface-related multiple elimination as a data-driven method. It predicts the surface multiples from the data themselves, with the free surface as the only reflector it needs to know, and removes them with an adaptive estimate of the source and surface terms.
prereqs: [seismic-reflection-model, convolution-theorem, neumann-series]
see_also: [predictive-deconvolution, parabolic-radon-transform, spectral-radius, fixed-point-iteration, seismic-migration, seismic-interferometry, full-waveform-inversion, wave-equation]
sources:
  - paper: doi:10.1190/1.1443330
    title: D. J. Verschuur, A. J. Berkhout and C. P. A. Wapenaar, Adaptive surface-related multiple elimination, Geophysics 57(9), 1992, 1166 to 1177
    locator: the matrix model of surface multiples, their prediction by a multidimensional convolution of the data with itself, the series and iterative forms, and the adaptive estimate of the surface operator
  - book: isbn:9781560800941
    title: Oz Yilmaz, Seismic Data Analysis, Society of Exploration Geophysicists, 2001, Investigations in Geophysics 10
    locator: the chapter on multiple attenuation (surface-related multiple elimination)
---

Surface-related multiple elimination (SRME) removes from marine seismic data the multiples that bounced at least once at the sea surface. It needs no model of the earth. Every surface multiple is a path from the source down and up to the surface, a reflection at the surface, and a second path down and up to the receiver. Both paths are already in the data, so the data convolved with themselves, summed over all surface positions, predict the multiples. At one frequency this is a matrix product, and the data without surface multiples are $P_0 = P (I + aP)^{-1}$, which one linear solve per frequency gives, or a [Neumann series](/neumann-series/) whose terms the iteration adds one by one. It works on the [convolutional model](/seismic-reflection-model/) extended to many sources and receivers, and it removes multiples whose period and moveout change from trace to trace, which [predictive deconvolution](/predictive-deconvolution/) cannot.

## In plain words

At sea, sound from the source goes down, comes back up, hits the sea surface and goes down again. So each echo is followed by weaker copies: echoes of echoes. These copies confuse the picture of the rocks. Each copy is made of two trips that the recording already holds: one trip from the source to some point on the sea surface, and one from that point to the receiver. So the method builds the copies by joining every recorded trip with every other recorded trip that starts where the first ended, and adds up over all meeting points. This guess of the copies is then removed from the data. Repeating the guess with the cleaned data makes it better each time, until only the first echoes are left.

## The problem

Input: the data $p(t; x_r, x_s)$ for receivers and sources on one regular grid of $s$ surface positions; the surface operator $a(\omega)$, which holds the free-surface reflection coefficient (about $-1$), the inverse of the source spectrum and the grid step. In practice $a$ is not known and is estimated. Output: the data $P_0$ without surface multiples. After the DFT in time, the data at one frequency form the $s \times s$ matrix $P$ (rows: receivers, columns: sources), and the model is
$$P = P_0 + a\, P_0\, P.$$
The product $P_0 P$ sums over the surface position $l$ where the multiple meets the surface: an event of $P$ from the source to $l$, then an event of $P_0$ from $l$ to the receiver. By the [convolution theorem](/convolution-theorem/) the product of spectra is a convolution in time, so the matrix product is a convolution in time and a sum in space. The model is a physical model of the surface multiples for point sources and receivers at the surface, not a theorem about real data; the direct wave, the ghosts and missing near offsets must be handled first.

## The algorithm

```pseudo id=main
SRME(P(ω) for every ω, a(ω), iterations K)
L1  for each frequency ω do
L2      P₀ ← P                                     ▷ the start: the data
L3      repeat K times
L4          P₀ ← P - a P₀ P                         ▷ predict the multiples and subtract
L5      append P₀ to the output                     ▷ or P₀ ← P (I + a P)⁻¹ by one solve
L6  return the output, back in time by the inverse DFT
```

After one step, $P_0 = P - aP^2$: the prediction is the data convolved with themselves, which removes the first-order surface multiples exactly and leaves the higher orders with wrong amplitudes. Each later step adds the next term of the series $P_0 = \sum_j (-a)^j P^{j+1}$. The direct form solves $X (I + aP) = P$ for $X$ once per frequency. In practice the operator $a$ is unknown, the data are not perfect, and the prediction is subtracted with a short filter fitted so that the result has the least energy: adaptive subtraction, a heuristic.

## Example

**One reflector.** A flat reflector with coefficient $r = 0.5$ lies $\tau = 8$ samples below the surface, the surface coefficient is $-1$ and the source is a unit impulse, so $a = -1$ and $P = rz/(1 + rz)$ with $z = e^{-i\omega\tau}$. The trace has $r, -r^2, r^3, \ldots$ at $\tau, 2\tau, 3\tau, \ldots$; on a periodic axis of 64 samples the series wraps and each value gets the factor $1/(1 - r^8)$.

| time | $\tau$ | $2\tau$ | $3\tau$ | $4\tau$ | $5\tau$ |
|---|---|---|---|---|---|
| data | 0.502 | $-0.251$ | 0.125 | $-0.063$ | 0.031 |
| one step, $P + P^2$ | 0.486 | 0.008 | $-0.129$ | 0.127 | $-0.095$ |
| direct, $P (I - P)^{-1}$ | 0.5 | 0 | 0 | 0 | 0 |

Without the wrap, one step gives exactly $(-1)^{m+1}(2 - m) r^m$ at $m\tau$: $r$, $0$, $-r^3$, $2r^4$, $-3r^5$. The first-order multiple is gone, and the later orders are not. The direct form returns the primary alone, exact to rounding.

**The iteration.** With $r = 0.4$, $\tau = 4$ and 32 samples, the largest error of the output after $k$ steps is $0.064$ ($k = 1$), $0.031$ (2), $6.2 \times 10^{-3}$ (5), $6.5 \times 10^{-4}$ (10), $1.0 \times 10^{-5}$ (20) and $3.0 \times 10^{-9}$ (40). The ratio over the last 20 steps is $3 \times 10^{-4} \approx (2/3)^{20}$, the rate of Claim 4 of the proof, $r/(1 - r) = 2/3$ at the worst frequency. For $r = 0.5$ the worst rate is $1$, and the iteration does not converge at that frequency, while the direct form still works.

**Adaptive subtraction.** On the $r = 0.5$ trace, start from $P_0 = P$, predict $M = P_0 P$, and pick the scalar $s$ that minimizes $\|P - sM\|^2$, six times. The scalars are $-0.633$, $-0.829$, $-0.971$, $-0.941$, $-0.942$ and $-0.958$, close to but not equal to the true $-1$, and residual multiples of about 0.02 remain. These numbers are measurements; they show why adaptive subtraction is a heuristic.

## Correctness

Under the model, the data without surface multiples are $P (I + aP)^{-1}$ whenever $I + aP$ is invertible, and it is invertible whenever the data were made from some $P_0$ with $I - aP_0$ invertible; the direct form is then exact. The iteration computes the partial sums of the Neumann series, and its error after $k$ steps is $(-1)^k a^{k+1} P_0 P^{k+1}$, so it converges when the spectral radius of $aP$ is below 1, which holds exactly when every eigenvalue of $aP_0$ has real part below $1/2$. The first prediction is the multidimensional autoconvolution of the data. These are theorems, proved in proofs/correctness.md. The model itself, and the estimate of $a$ by adaptive subtraction, are not theorems: the first is a physical model, the second a heuristic.

## Complexity

In the real-RAM model, with $f$ frequencies and $s$ surface positions, the direct form costs $O(f s^3)$: one dense solve with $s$ right-hand sides per frequency. $K$ steps of the iteration cost $O(K f s^3)$. The transforms of the $s^2$ traces add $O(s^2 n \log n)$ for $n$ time samples with an FFT. Space is $O(f s^2)$ for the data at all frequencies. For 3D surveys $s$ counts the sources and receivers in two dimensions, so the cost is large, and the data must first be interpolated to the grid.

## Properties

- Data-driven: no velocities, no subsurface model (a property of the model, not an approximation).
- Exact under the model, with the direct form (a theorem).
- Removes surface multiples of all orders and all moveouts, including multiples from dipping and curved reflectors (a consequence of the model).
- Does not remove internal multiples, which bounce only between layers below the surface.
- Needs dense sources and receivers on the same grid, including the near offsets that the recording usually misses.

## Variants and improvements

- Adaptive subtraction with short filters in time and space windows, to absorb errors of the source wavelet, the surface coefficient and the data (a heuristic).
- Estimation of primaries by sparse inversion (EPSI): treat $P_0$ and the source as unknowns of an inversion with a sparsity prior, in place of prediction and subtraction.
- Internal multiple prediction with the same idea, using a chosen layer boundary in place of the surface.
- 3D SRME with interpolation of the missing sources and receivers.
- The same matrix calculus underlies [seismic interferometry](/seismic-interferometry/), which correlates in place of convolving.

## When to use it

Use it on marine data with a strong sea floor and a free surface, where surface multiples dominate. It is usually the first step of multiple removal, before the [parabolic Radon transform](/parabolic-radon-transform/) cleans up what remains, and before [migration](/seismic-migration/), which would otherwise image the multiples as false reflectors.

## Pitfalls

- Missing near offsets and coarse source sampling break the sum over surface positions; interpolate first.
- The direct wave and the source ghost must be removed or modeled, or they enter the prediction.
- Adaptive subtraction can remove primaries that overlap the multiples; keep the filters short and the windows large.
- The iteration diverges at frequencies where the spectral radius of $aP$ is 1 or more, as for a sea floor with a strong reflection; the direct form or adaptive damping is then needed.
- 3D effects: a 2D SRME on 3D data predicts multiples at wrong times when the surface paths leave the plane of the line.

## Implementations

## History

Verschuur, Berkhout and Wapenaar (1992) published surface-related multiple elimination in its adaptive form. They wrote the data at one frequency as a matrix, modeled the surface multiples as a feedback of the data through the free surface, and removed them by a series or an iteration, with the source and surface terms estimated from the data by minimum energy. The method became a standard way to remove surface multiples from marine data.

## References
