---
tag: VVPHQA
kind: algorithm
slug: fourier-amplitude-sensitivity-test
name: Fourier amplitude sensitivity test
area: scientific-computing/uncertainty-quantification
level: advanced
summary: Varies all inputs along a curve with distinct frequencies and reads each input's share of variance from the Fourier spectrum of the output.
solves: [forward-uncertainty-propagation]
model: real-ram
complexity:
  vars: {d: the number of inputs, R: "the number n_r of curves per input", n: "the number n_s of points per curve", F: the cost of one model run}
  time: {worst: O(d R n (F + d + n))}
  space: {extra: O(d n)}
properties: {deterministic: false, randomized: true, exact: false, iterative: false}
history:
  year: 1973
  people: [R. I. Cukier, C. M. Fortuin, Kurt E. Shuler, A. G. Petschek, J. H. Schaibly, Andrea Saltelli, Stefano Tarantola, Karen Chan]
  note: Cukier and coauthors proposed FAST for the sensitivity of chemical reaction systems in 1973. Saltelli, Tarantola and Chan gave the extended form with total indices and random phases in 1999.
prereqs: [sobol-indices, discrete-fourier-transform]
see_also: [hoeffding-sobol-decomposition, saltelli-sampling-scheme, morris-method, parseval-theorem, fast-fourier-transform, aliasing, uniform-distribution, monte-carlo-integration]
sources:
  - paper: doi:10.1063/1.1680571
    title: R. I. Cukier, C. M. Fortuin, K. E. Shuler, A. G. Petschek and J. H. Schaibly, Study of the sensitivity of coupled reaction systems to uncertainties in rate coefficients. I Theory, Journal of Chemical Physics 59(8), 1973, 3873-3878
    locator: the search curve with incommensurate frequencies and the partial variances from the Fourier coefficients at the harmonics of each frequency
  - paper: doi:10.1080/00401706.1999.10485594
    title: A. Saltelli, S. Tarantola and K. P.-S. Chan, A quantitative model-independent method for global sensitivity analysis of model output, Technometrics 41(1), 1999, 39-56
    locator: the extended FAST, the search curve 1/2 + arcsin(sin(omega s + phi))/pi, the total index from the low frequency band, the frequency rules and the resampling with random phases
  - book: isbn:9780470059975
    title: Andrea Saltelli, Marco Ratto, Terry Andres, Francesca Campolongo, Jessica Cariboni, Debora Gatelli, Michaela Saisana and Stefano Tarantola, Global Sensitivity Analysis, The Primer, Wiley, 2008
    locator: Chapter 4 (FAST and the extended FAST among the variance-based methods)
---

The Fourier amplitude sensitivity test (FAST) estimates the [Sobol indices](/sobol-indices/) of a model by moving all inputs together along one periodic curve through the input space, each input at its own integer frequency. The output along the curve is a periodic signal, and the [discrete Fourier transform](/discrete-fourier-transform/) of that signal splits its variance by frequency: the power at the frequency of an input and its first few harmonics is the variance due to that input alone. The extended form (eFAST) gives one input a high frequency and all others low ones, so that the same spectrum also gives the total index. The cost is $d\, n_r\, n_s$ model runs for $d$ inputs, and the method is exact only for models whose spectrum fits in the bands it reads.

## In plain words

Turn every knob of a model back and forth at the same time, each knob at its own speed. One knob turns fast, and the others turn slowly. Record the output over one full cycle.

If the output wiggles at the fast speed, the fast knob is causing it. If the output only drifts slowly, the slow knobs are causing it. A frequency analysis of the recording tells how much of the output's spread sits at the fast speed and how much sits at the slow speeds. The share at the fast speed is what the fast knob does alone. The share at the slow speeds is what the other knobs do without it, so everything else belongs to the fast knob, alone or together with others.

Do this once for each knob, and each time make that knob the fast one.

## The problem

The input is a model $y = f(x)$ with $d$ independent inputs, each uniform on $[0, 1]$ after a transformation, and a budget of model runs. The output is an estimate of the first order and total Sobol indices

$$S_i = \frac{\mathrm{Var}(\mathbb{E}[y \mid x_i])}{\mathrm{Var}(y)}, \qquad S_{Ti} = 1 - \frac{\mathrm{Var}(\mathbb{E}[y \mid x_{\sim i}])}{\mathrm{Var}(y)},$$

where $x_{\sim i}$ is all inputs except $x_i$. Inputs with other laws are handled by the inverse transform $x_i \mapsto F_i^{-1}(x_i)$ of [inverse transform sampling](/inverse-transform-sampling/).

## The algorithm

For input $i$, the curve is

$$x_k(s) = \frac{1}{2} + \frac{1}{\pi}\arcsin\big(\sin(\omega_k s + \varphi_k)\big), \qquad s \in (-\pi, \pi),$$

with $\omega_i = \omega_{\max}$ and low frequencies $\omega_k \le \omega_{\max}/(2M)$ for $k \ne i$. Each $x_k(s)$ is a triangle wave, and it is uniform on $[0, 1]$ when $s$ is uniform. $M$ is the number of harmonics read, usually 4, and $n_s \ge 2M\omega_{\max} + 1$ is odd. The power at frequency $p$ is $\Lambda_p = (A_p^2 + B_p^2)/2$, where $A_p$ and $B_p$ are the cosine and sine coefficients of the samples.

```pseudo id=main
EFAST(f, d, ω_max, M, n_r, n_s)
L1  for i = 1..d do                                  ▷ input i is the fast one
L2      ω ← ω_max for input i, and d - 1 low frequencies, spread over 1..⌊ω_max / (2M)⌋, for the others
L3      repeat n_r times, with new phases φ_k uniform on [0, 2π):
L4          x^(j) ← the curve at s_j = π(2j - n_s - 1) / n_s, j = 1..n_s
L5          y_j ← f(x^(j)) for j = 1..n_s
L6          Λ_p ← (A_p^2 + B_p^2) / 2 for p = 1..(n_s - 1) / 2
L7          D ← Σ_p Λ_p                                     ▷ the variance of the y_j
L8          D_i ← Σ_{q=1..M} Λ_(q ω_max)                    ▷ the harmonics of input i
L9          D_~i ← Σ_{p=1..⌊ω_max/2⌋} Λ_p                    ▷ the band of the other inputs
L10     S_i, S_Ti ← the averages over the n_r curves of D_i / D and 1 - D_~i / D
    return S, S_T and the run count d n_r n_s
```

Line L5 is the only step that runs the model. Lines L6 to L9 read the spectrum: the first order part at the multiples of $\omega_{\max}$ up to $M\omega_{\max}$, and the part of the other inputs in the low band. Line L10 averages over the random phases. The classic FAST of Cukier and coauthors uses one curve for all inputs, with a set of frequencies chosen so that their low harmonics do not collide, and reads only the first order indices.

## Example

**By hand.** Let $f = u_1 + 2u_2 + u_1u_2$ with $u_k = 2x_k - 1$ uniform on $[-1, 1]$. Its Hoeffding-Sobol terms are $u_1$, $2u_2$ and $u_1u_2$ with variances $1/3$, $4/3$ and $1/9$, so $D = 16/9$, $S_1 = 3/16$, $S_2 = 3/4$, $S_{T1} = 1/4$ and $S_{T2} = 13/16$. With $\omega_{\max} = 64$, $M = 4$, $n_s = 513$ and one curve per input, the frequencies are $(64, 1)$ for input 1 and $(1, 64)$ for input 2. A run with `random.Random(1)` gives, as a measurement:

| index | exact | eFAST |
|---|---|---|
| $S_1$ | 0.1875 | 0.1856 |
| $S_2$ | 0.75 | 0.7535 |
| $S_{T1}$ | 0.25 | 0.2457 |
| $S_{T2}$ | 0.8125 | 0.8084 |

The cost is $2 \cdot 513 = 1026$ runs. The small errors are not sampling noise: $u_1$ along the curve is a triangle wave, whose harmonics decay like $1/q^2$ and go on above $q = M$, so some power falls outside the bands of lines L8 and L9 or aliases above $n_s/2$.

**The Ishigami function.** With $f(x) = \sin x_1 + 7\sin^2 x_2 + 0.1\, x_3^4 \sin x_1$ on $[-\pi, \pi]^3$, the same parameters, the low frequencies 1 and 8, and `random.Random(1)`, eFAST gives, as a measurement:

| input | $S_i$ exact | $S_i$ eFAST | $S_{Ti}$ exact | $S_{Ti}$ eFAST |
|---|---|---|---|---|
| $x_1$ | 0.3139 | 0.3126 | 0.5576 | 0.5365 |
| $x_2$ | 0.4424 | 0.4437 | 0.4424 | 0.4890 |
| $x_3$ | 0 | 0.0221 | 0.2437 | 0.2433 |

The run count is $3 \cdot 513 = 1539$. The first order indices are close, and the gap $S_{T3} - S_3$ shows the interaction of $x_3$ with $x_1$. The total indices carry a band bias of a few hundredths, which more phases do not remove.

## Correctness

The proof file shows four facts. Each $x_k(s)$ is uniform on $[0, 1]$. For odd $n_s$, the sum of line L7 is exactly the sample variance of the $y_j$ (the discrete [Parseval theorem](/parseval-theorem/)). Along the curve, the main effect $f_i(x_i(s))$ depends on $s$ only through $\omega_{\max}s$, so all its power is at the multiples of $\omega_{\max}$. And $\cos(2\pi m x_k(s)) = \pm\cos(2m(\omega_k s + \varphi_k))$ is a pure harmonic. From these, the theorem: if $M$ is even and $f$ is an additive sum of cosines $\cos(2\pi m x_k)$ with $2m \le M$, and the frequencies $2m\omega_k$ are distinct, then eFAST returns the exact $S_i$ and $S_{Ti}$ from one curve. For a general model, three errors remain: the power of $f_i$ above $M\omega_{\max}$ (truncation), the power of interaction terms that falls on the harmonics of line L8 or in the band of line L9 (interference), and aliasing of frequencies above $n_s/2$. The method is consistent only in the band-limited sense of the theorem, and it gives no error bar.

## Complexity

The method makes $d\, n_r\, n_s$ model runs, with $n_s \ge 2M\omega_{\max} + 1$, for example $3 \cdot 513 = 1539$ for the Ishigami example. Building one point costs $O(d)$, and the spectrum of line L6 by direct sums costs $O(n_s^2)$ per curve, so the total time is $O(d\, n_r\, n_s(F + d + n_s))$ in the [real RAM](/real-ram/) model. A [fast Fourier transform](/fast-fourier-transform/) reduces the spectrum to $O(n_s \log n_s)$, but the model runs dominate in practice. The extra space is $O(d\, n_s)$ for the points of one curve. The run count does not depend on the number of interactions, and it is comparable to the $N(d + 2)$ runs of the [Saltelli sampling scheme](/saltelli-sampling-scheme/) for $N$ close to $n_s$.

## Properties

- **First order and total indices from one spectrum.** eFAST reads $S_i$ and $S_{Ti}$ from the same $n_s$ runs of curve $i$.
- **Deterministic sampling.** The points are on a curve, not random; only the phases are random.
- **Exact for band-limited additive models**, as in the theorem of the proof file.
- **Biased for general models.** The truncation and interference errors are systematic; averaging over phases reduces only the part that changes with the phases.
- **Inputs must be independent.** The variance split uses the Hoeffding-Sobol decomposition, which needs independent inputs.

## Variants and improvements

- **Classic FAST.** Cukier and coauthors (1973) use one curve with incommensurate, or in practice integer and interference-free, frequencies for all $d$ inputs and read only the first order indices. The needed $\omega_{\max}$ grows fast with $d$, which limits classic FAST to a few tens of inputs.
- **Extended FAST.** Saltelli, Tarantola and Chan (1999) give each input its own curve with one high frequency, read the total index from the low band, and repeat with random phases.
- **Random balance designs.** One curve with the same frequency for all inputs, with the points permuted independently for each input; the first order indices of all inputs come from $n_s$ runs in total.
- **Other curves.** The curve of Cukier and coauthors was $x_k = G_k(\sin \omega_k s)$ with a transformation $G_k$ chosen for the input law; the triangle wave of eFAST makes the marginals exactly uniform.

## When to use it

Use eFAST when the model has a few to a few tens of independent inputs, runs are cheap enough for a few thousand evaluations, and the first order and total indices are both needed. The [Saltelli sampling scheme](/saltelli-sampling-scheme/) has error bars by the [central limit theorem](/central-limit-theorem/) and no band bias, so it is the safer choice when an error estimate matters. With many inputs, screen first with the [Morris method](/morris-method/). With a smooth model, a [polynomial chaos expansion](/polynomial-chaos-expansion/) gives all Sobol indices from its coefficients.

## Pitfalls

- **Low frequencies too close.** If the low frequencies of the other inputs are small and close, the curve covers their subcube badly and their interference changes with the phases. For the Ishigami function with low frequencies 1 and 2, $S_2$ came out between 0.35 and 0.40 depending on the phases, against 0.4424, a measurement; spreading them to 1 and 8 in line L2 fixed it.
- **An even number of points.** With $n_s$ even, the frequency $n_s/2$ has only a cosine term, and the sum of line L7 is no longer the sample variance. Keep $n_s$ odd.
- **Too few points.** If $n_s < 2M\omega_{\max} + 1$, the harmonics $q\omega_{\max}$ alias onto lower frequencies, and line L8 reads the wrong power.
- **Too few harmonics.** A main effect with strong harmonics above $M\omega_{\max}$ loses that power from $D_i$, so $S_i$ is too low. Raise $M$ and $\omega_{\max}$ together.
- **Reading the error as noise.** The gaps in the examples are biases from the bands, not sampling error. More phases ($n_r$) do not reduce them; only a larger $\omega_{\max}$ and $M$ with more points do.

## Implementations

## History

Cukier, Fortuin, Shuler, Petschek and Schaibly proposed FAST in 1973 in the Journal of Chemical Physics, to measure how uncertain rate constants change the concentrations of coupled chemical reactions. Schaibly and Shuler and later Cukier, Levine and Shuler developed the frequency choices and the theory in the 1970s. Saltelli, Tarantola and Chan (1999) showed how to get the total index from the low band and introduced the triangle wave curve and the random phases, which is the extended FAST in common use.

## References
