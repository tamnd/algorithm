---
tag: 5J6KMF
kind: algorithm
slug: parabolic-radon-transform
name: Parabolic Radon transform
aliases:
- Hampson multiple attenuation
area: imaging-and-inverse-problems/seismic-imaging
level: advanced
summary: "Decompose a moveout-corrected gather into parabolic events by damped least squares, one frequency at a time, then keep the flat primaries and subtract the curved multiples."
model: real-ram
complexity:
  vars: {n: the number of time samples, m: the number of traces, k: the number of curvatures}
  time: {worst: O(n (m k^2 + k^3) + n^2 (m + k)), average: O(n (m k^2 + k^3) + n^2 (m + k)), best: O(n (m k^2 + k^3) + n^2 (m + k))}
  space: {extra: O(n (m + k) + m k + k^2)}
properties: {deterministic: true, linear_in_data: true, least_squares: true, exact_shifts: "periodic time axis, odd n", primaries_plus_multiples_equal_data: true}
history:
  year: 1986
  people: [Dan Hampson]
  note: Thorson and Claerbout (1985) posed the velocity stack as a least-squares inverse problem over hyperbolas. Hampson (1986) replaced the hyperbolas of a moveout-corrected gather by parabolas, which makes the problem separate by frequency and cheap enough for routine multiple removal.
prereqs: [normal-moveout-correction, tikhonov-regularization, discrete-fourier-transform]
see_also: [radon-transform, semblance-velocity-analysis, surface-related-multiple-elimination, predictive-deconvolution, normal-equations, toeplitz-system-solving, forward-operator, sparse-signal-recovery]
sources:
  - paper: "Dan Hampson, Inverse velocity stacking for multiple elimination, Journal of the Canadian Society of Exploration Geophysicists 22(1), 1986, 44 to 55"
    title: Dan Hampson, Inverse velocity stacking for multiple elimination, Journal of the Canadian Society of Exploration Geophysicists 22(1), 1986, 44 to 55
    locator: the parabolic approximation of the residual moveout after NMO, the least-squares transform solved frequency by frequency, and the subtraction of the multiples
  - paper: doi:10.1190/1.1893060
    title: Dan Hampson, Inverse velocity stacking for multiple elimination, SEG Technical Program Expanded Abstracts 1986, 422 to 424
    locator: the short conference version of the method
  - paper: doi:10.1190/1.1441893
    title: John R. Thorson and Jon F. Claerbout, Velocity-stack and slant-stack stochastic inversion, Geophysics 50(12), 1985, 2727 to 2741
    locator: the velocity stack and the slant stack posed as inverse problems with a least-squares fit and a model prior
  - book: isbn:9781560800941
    title: Oz Yilmaz, Seismic Data Analysis, Society of Exploration Geophysicists, 2001, Investigations in Geophysics 10
    locator: the chapter on multiple attenuation (the parabolic Radon transform and its use to separate primaries and multiples)
---

The parabolic Radon transform removes multiples from a common-midpoint gather by their moveout. After [normal moveout correction](/normal-moveout-correction/) with the velocity of the primaries, a primary is flat, and a multiple, which travels slower, still curves down, close to a parabola $t = \tau + q x^2$. The method writes the gather as a sum of parabolic events, one model trace for each curvature $q$, and finds the model by damped least squares. The model traces with large $q$ are the multiples: the method maps them back to the gather and subtracts them. Because a parabola is a time shift that does not depend on $\tau$, the least-squares problem splits into one small system per frequency. It is a seismic relative of the [Radon transform](/radon-transform/) of tomography, which integrates an image along straight lines; here the curves are parabolas in time and offset, and the transform is inverted by least squares, not by a filtered back projection.

## In plain words

After the usual correction for distance, the echoes that went straight down and up line up flat across the record. Echoes that bounced several times arrive with a bend that remains. The method tries to explain the whole record as a sum of simple curved shapes, from flat to strongly bent. It picks the strength of every shape so that the sum matches the record as closely as possible, with a small penalty that keeps the strengths modest. Then it keeps only the strongly bent shapes, rebuilds the record they make, and subtracts it. What is left is the flat part, the echoes we want. The work is done one frequency at a time, which makes each piece small and fast.

## The problem

Input: a gather $d_i(t)$ with offsets $x_i$, already corrected for normal moveout with the primary velocity; curvatures $q_1 < \cdots < q_k$; a damping $\mu > 0$; a cut $q_{\text{cut}}$. Output: the model $m_j(\tau)$, the predicted multiples and the primaries. The forward operator is
$$d_i(t) = \sum_j m_j(t - q_j x_i^2),$$
and the model minimizes $\|Lm - d\|^2 + \mu\|m\|^2$, a [Tikhonov](/tikhonov-regularization/) problem. Why parabolas: a multiple with rms velocity $v_m$ and zero-offset time $t_0$ arrives at $\sqrt{t_0^2 + x^2/v_m^2}$. NMO with the primary velocity $v_p$ moves it to $\sqrt{t_0^2 + x^2 (1/v_m^2 - 1/v_p^2)}$, whose Taylor expansion in $x$ starts with $t_0 + q x^2$, $q = (1/v_m^2 - 1/v_p^2)/(2 t_0)$. The parabola is an approximation (a theorem for small offsets, a heuristic at far offsets, where it can be off by a large part of a period). Its gain is that a parabola is a shift by $q x^2$ for every $\tau$, so the DFT turns the forward operator into the matrices $(L_\omega)_{ij} = e^{-i\omega q_j x_i^2}$, one per frequency. A hyperbola $\sqrt{\tau^2 + x^2/v^2}$ shifts different $\tau$ by different amounts, and its operator does not split this way.

## The algorithm

```pseudo id=main
PARABOLIC-RADON-DEMULTIPLE(d, x, q, Δt, μ, q_cut)
L1  D_i ← DFT(d_i) for every trace
L2  for each frequency ω do
L3      L_ij ← exp(-i ω q_j x_i²)
L4      M(ω) ← solution of (Lᴴ L + μ I) M = Lᴴ D(ω)
L5      K_j ← M_j(ω) if q_j > q_cut, else 0
L6      N(ω) ← L K                                ▷ predicted multiples
L7  m ← inverse DFT of M; multiples ← inverse DFT of N
L8  return (m, d - multiples, multiples)
```

The adjoint $L^H$ alone, without the solve, is the plain parabolic stack: the sum of the data along each parabola. It smears each event over many curvatures, because the parabolas through one event all collect some of its energy. The least-squares solve of line L4 focuses the model, so that the multiples can be cut from the primaries in $q$. The damping $\mu$ keeps the system solvable at low frequencies, where the columns of $L$ are nearly equal (at $\omega = 0$ they are all equal), and controls the amplification of noise.

## Example

**The parabolic approximation.** A primary with $v_p = 2500$ m/s and a multiple with $v_m = 2000$ m/s at $t_0 = 1$ s. At $x = 2000$ m the exact residual moveout after NMO is $\sqrt{1 + 2000^2 (1/2000^2 - 1/2500^2)} - 1 = 0.16619$ s. The parabola has $q = (2.5 \times 10^{-7} - 1.6 \times 10^{-7})/2 = 4.5 \times 10^{-8}$ s/m² and predicts $q x^2 = 0.18$ s, 14 ms too much. This error is a fixed property of the approximation; the method accepts it, or it uses a $q$ grid wide enough to absorb it.

**Separating a multiple.** A gather of 16 traces at offsets 0 to 1500 m, 63 samples at $\Delta t = 8$ ms, a 20 Hz Ricker wavelet. The primary is flat at $\tau = 0.15$ s. The multiple has amplitude $-0.7$ at $\tau = 0.2$ s and $q = 4 \times 10^{-8}$ s/m², so its moveout at 1500 m is 0.09 s, about two periods of the wavelet. The data are made with the forward operator itself, on the grid of 14 curvatures from $-1 \times 10^{-8}$ to $5.5 \times 10^{-8}$ in steps of $0.5 \times 10^{-8}$ s/m². With $q_{\text{cut}} = 1.2 \times 10^{-8}$:

| damping $\mu$ | 0.01 | 0.1 | 1 |
|---|---|---|---|
| relative error of the primaries | 0.113 | 0.124 | 0.145 |

Before the removal, the gather differs from the true primaries by a relative error of 0.700. With $\mu = 0.01$, 65 percent of the model energy is at the three curvatures nearest the primary and 27 percent at the three nearest the multiple; for the plain stack $L^H d$ the shares are 42 and 22 percent, the rest smeared over the other curvatures. The model is not the true model (its relative error is 0.75): one step in $q$ moves the far trace by only 11 ms, about a fifth of the 50 ms period, so neighboring curvatures are not resolved and the energy spreads over them. These numbers are measurements on this synthetic gather.

## Correctness

For odd $n$ on a periodic time axis, the forward operator is a sum of exact band-limited shifts, its adjoint is the frequency-wise $L^H$, and the frequency-wise solve of line L4 gives the unique minimizer of $\|Lm - d\|^2 + \mu\|m\|^2$ over real models, the same model as the dense time-domain normal equations. The predicted multiples are $L$ applied to the model traces above the cut, and the returned primaries and multiples add up to the data exactly; the misfit stays with the primaries. At zero frequency every model trace gets the same mean, whatever the data. These are theorems, proved in proofs/correctness.md. That the cut in $q$ separates primaries from multiples is a heuristic: it needs the residual moveouts to be parabolic enough and to differ by more than about a period at the far offset.

## Complexity

In the real-RAM model each frequency costs $O(m k^2)$ for the normal matrix and $O(k^3)$ for the solve, so the solves cost $O(n (m k^2 + k^3))$. The code uses a direct DFT for odd $n$, $O(n^2)$ per trace; with an FFT the transforms cost $O((m + k)\, n \log n)$. With equally spaced curvatures the normal matrix is Hermitian Toeplitz, and a Levinson-type solver costs $O(k^2)$ per frequency. Space is $O(n (m + k))$ for the spectra plus $O(m k + k^2)$ for one frequency.

## Properties

- Linear in the data for fixed $q$ grid, $\mu$ and $q_{\text{cut}}$ (a theorem).
- Primaries plus predicted multiples equal the data (a theorem), so nothing is lost: what the model does not explain stays in the primaries.
- Resolution in $q$ grows with the frequency and with the square of the largest offset; events whose far-offset moveouts differ by much less than a period are not separated (a heuristic).
- Time-invariant: one system per frequency serves all times, so the cost does not grow with the number of events.
- Works on gathers with irregular offsets, since the $x_i$ enter only through the matrix entries.

## Variants and improvements

- High-resolution or sparse Radon transforms: replace the $\|m\|^2$ penalty by a sparsity penalty and solve by reweighted least squares, so that each event focuses at one curvature ([sparse signal recovery](/sparse-signal-recovery/)).
- Time-domain hyperbolic Radon transforms, as in Thorson and Claerbout (1985): exact hyperbolas, at the cost of a large coupled system solved by iterative methods.
- Linear Radon transform (slant stack) for events that are straight lines in the gather, such as ground roll and refractions.
- Apex-shifted parabolas for diffracted multiples.
- Subtract the multiples with an adaptive filter in place of the plain subtraction of line L8.

## When to use it

Use it in processing before stacking, on gathers where multiples and primaries differ clearly in stacking velocity, usually at medium and far offsets and at later times. It is a standard step for marine data, often after [surface-related multiple elimination](/surface-related-multiple-elimination/) has removed most of the surface multiples. It does not need a model of the surface or the source, only the moveout difference.

## Pitfalls

- At near offsets the moveout difference is small, so multiples there are not removed; this is a basic limit of the method.
- A $q$ grid that is too narrow cannot hold the multiples, and a grid too coarse misses their curvatures.
- The cut $q_{\text{cut}}$ must lie between the residual moveouts of primaries and multiples; a primary with a wrong NMO velocity curves and can be cut with the multiples.
- Too little damping amplifies noise at low frequencies; too much damping smears the model and lets energy leak across the cut.
- Aliasing in offset: if $\omega q x^2$ changes by more than $\pi$ between neighboring traces at the highest frequency, the transform maps energy to wrong curvatures.
- On a periodic time axis an event near the end of the record wraps to the start; pad the traces with zeros.

## Implementations

## History

Thorson and Claerbout (1985) described the velocity stack and the slant stack as inverse problems: the model is the set of events in velocity or ray parameter, and it is found by fitting the data in the least-squares sense with a prior on the model. Hampson (1986) proposed to work on gathers after NMO correction, where the residual moveout of multiples is close to a parabola. A parabolic moveout is a pure time shift, so the least-squares problem splits by frequency into small systems. This made the method fast enough for production processing, and the parabolic Radon demultiple became a standard step in seismic processing.

## References
