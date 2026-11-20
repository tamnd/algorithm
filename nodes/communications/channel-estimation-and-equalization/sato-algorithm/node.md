---
tag: 2220NN
kind: algorithm
slug: sato-algorithm
name: Sato algorithm
aliases:
- Sato blind equalizer
area: communications/channel-estimation-and-equalization
level: advanced
summary: "The first blind equalizer (1975): an LMS update with the error z - gamma sgn(z), gamma = E a^2 / E|a|, for multilevel PAM. A per-axis form works for square QAM."
solves: [blind-equalization]
model: real-ram
complexity:
  vars: {N: the number of equalizer taps, K: the number of samples}
  time: {worst: O(K N)}
  space: {extra: O(N)}
properties: {deterministic: true, online: true, blind: true, phase_independent: false, global_convergence: false}
history:
  year: 1975
  people: [Yoichi Sato]
  note: "Sato proposed self-recovering equalization of multilevel amplitude modulation in 1975, the first blind equalizer. Benveniste, Goursat and Ruget generalized it and studied its convergence in 1980."
prereqs: [blind-equalization, lms-algorithm]
see_also: [constant-modulus-algorithm, adaptive-equalization, pulse-amplitude-modulation, quadrature-amplitude-modulation, carrier-recovery, tong-xu-kailath-identification, mmse-linear-equalizer]
sources:
  - paper: "Yoichi Sato, A method of self-recovering equalization for multilevel amplitude-modulation systems, IEEE Transactions on Communications 23(6), 1975, pages 679 to 682"
    locator: "the error z - gamma sgn(z) and the self-recovering adjustment of a linear equalizer"
  - paper: "Albert Benveniste, Maurice Goursat and Gabriel Ruget, Robust identification of a nonminimum phase system: blind adjustment of a linear equalizer in data communications, IEEE Transactions on Automatic Control 25(3), 1980, pages 385 to 399"
    locator: "the generalization of the Sato algorithm and its convergence for an equalizer of unbounded length"
  - paper: doi:10.1109/5.720246
    title: "C. Richard Johnson, Jr., Philip Schniter, Thomas J. Endres, James D. Behm, Donald R. Brown and Raul A. Casas, Blind equalization using the constant modulus criterion: a review, Proceedings of the IEEE 86(10), 1998, starting at page 1927"
    locator: "the background on Bussgang-type blind equalizers, of which Sato is one"
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Chapter 10 (adaptive equalization), the section on blind equalization"
---

The Sato algorithm is the first blind equalizer, published by Yoichi Sato in 1975 for multilevel PAM. It runs the LMS update of a linear equalizer, but with a made-up target: in place of the unknown symbol, it uses $\gamma\, \mathrm{sgn}(z)$, where $z$ is the equalizer output and $\gamma = E a^2 / E|a|$ is a constant of the alphabet. So the equalizer treats every symbol as if it were binary, with the level $\pm\gamma$. The error is large while the channel smears the symbols and has mean zero at a perfect equalizer. Like the [constant modulus algorithm](/constant-modulus-algorithm/), it solves the [blind equalization](/blind-equalization/) problem by a stochastic gradient step that costs $O(N)$ per sample. The difference is the error. CMA looks only at $|z|$, so it ignores the carrier phase. Sato looks at the sign of each axis, so for QAM it also turns the output back to the axes of the grid, up to a multiple of 90 degrees. Sato is rarely used today. CMA usually converges more reliably, and the [Tong-Xu-Kailath](/tong-xu-kailath-identification/) and subspace methods give batch estimates from second-order statistics.

## In plain words

A receiver must undo the echoes of a channel without a training sequence. The Sato method pretends that each symbol is either a fixed positive value or the same negative value, chosen by the sign of the equalizer output. It then adjusts the equalizer as if this guess were the truth. The guess is wrong for most symbols of a multilevel signal, but the errors balance out on average when the equalizer is right, and they do not balance while echoes remain. So the equalizer drifts toward the setting that removes the echoes. The fixed value is chosen so that the output has the right size at that point. For a two-dimensional signal, the method does the same on each axis.

## The problem

The input is the received sequence $y[k] = \sum_l h_l\, a[k-l] + w[k]$ at one sample per symbol, the number of taps $N$ and a step size $\mu > 0$. The channel $h$ is unknown. The symbols are independent and identically distributed with a symmetric distribution, for example $M$-PAM. The equalizer output is $z[k] = \sum_{i=0}^{N-1} c_i\, y[k-i]$. The goal is taps $c$ with $z[k] \approx \pm a[k - d]$ for some delay $d$. For PAM the sign is the only ambiguity, because the cost below is even in $z$.

The constant is
$$\gamma = \frac{E a^2}{E|a|}.$$
For 2-PAM, $\gamma = 1$. For the raw 4-PAM levels $\pm 1, \pm 3$, $\gamma = 5/2$; for unit-energy 4-PAM, $\gamma = \sqrt 5 / 2 = 1.1180$. For the raw 8-PAM levels $\pm 1, \ldots, \pm 7$, $\gamma = 21/4 = 5.25$. For real signals, the algorithm is a stochastic gradient method on $J(c) = E[z^2/2 - \gamma |z|]$.

## The algorithm

```pseudo id=main
SATO(y, N, μ, γ)
L1  c ← (0, ..., 0);  c[⌊N/2⌋] ← 1              ▷ the center spike
L2  for k ← N - 1 to K - 1 do
L3      u ← (y[k], y[k-1], ..., y[k-N+1])
L4      z[k] ← Σ_i c[i] u[i]
L5      e ← z[k] - γ csgn(z[k])                  ▷ csgn(z) = sgn(Re z) + j sgn(Im z)
L6      c[i] ← c[i] - μ e conj(u[i])  for all i
L7  return c, z
```

Line L1 starts from a single tap in the middle, so that the equalizer can reach a delay near $N/2$. Lines L3 and L4 are the filter. Line L5 is the Sato error. For PAM the imaginary parts are zero, $\mathrm{csgn}(z) = \mathrm{sgn}(z)$, and the error is $z - \gamma\, \mathrm{sgn}(z)$, the derivative of $z^2/2 - \gamma|z|$. For square QAM, line L5 applies the PAM rule to each axis, with $\gamma = E[(\mathrm{Re}\, a)^2] / E|\mathrm{Re}\, a|$. Line L6 is the LMS update with this error. Compared with decision-directed LMS, line L5 replaces the decision by $\gamma$ times its sign. Compared with CMA, line L5 replaces $z(|z|^2 - R_2)$.

## Example

**The constant.** For unit-energy 4-PAM, the levels are $\pm 1/\sqrt 5$ and $\pm 3/\sqrt 5$. Then $E a^2 = 1$ and $E|a| = 2/\sqrt 5$, so $\gamma = \sqrt 5/2 = 1.1180$. A symbol $a = 3/\sqrt 5 = 1.342$ at a perfect equalizer gives the error $1.342 - 1.118 = 0.224$, and $a = 1/\sqrt 5 = 0.447$ gives $0.447 - 1.118 = -0.671$. The errors are not zero, but their mean times the symbol is $\frac12 (1.342 \times 0.224 + 0.447 \times (-0.671)) = 0$.

**4-PAM through $h = (1, 0.5)$.** Use $N = 11$, $\mu = 0.002$, no noise and seed 2. The residual ISI of the combined response $g = c * h$ falls slowly:

| samples | 1000 | 2000 | 4000 | 8000 |
|---|---|---|---|---|
| residual ISI | 0.222 | 0.176 | 0.055 | 0.0066 |
| largest tap $g_5$ | 0.888 | 0.900 | 0.922 | 0.973 |

At the end, the taps $(\ldots, 0.974, -0.515, 0.226, -0.136, \ldots)$ from tap 5 on approximate the inverse $1, -0.5, 0.25, -0.125$ of the channel, and the last 2000 decisions have no errors.

**16-QAM with a carrier phase.** Rotate the channel $(1, 0.3 + 0.2j)$ by 25 degrees and run the QAM form with $\mu = 0.0005$ for 12000 samples. The largest tap of $g$ ends at the phase 0.97 degrees: the per-axis sign has turned the output back to the grid. With a rotation of 70 degrees, it ends at 89.7 degrees, which is the grid turned by 90 degrees, a symmetry of square QAM. CMA, on the same input, would keep the rotation.

## Correctness

**Claim (the perfect equalizer is a fixed point).** Let the symbols be independent with a symmetric distribution, with no noise, and let $\gamma = E a^2 / E|a|$. If the combined response is $g = \pm e_d$, then the mean update of line L6 is zero. If $g = \beta e_d$ with $\beta > 0$ and $\beta \ne 1$, it is not zero. This is a theorem, and the tests check it with exact fractions for 4-PAM.

**Key step.** The mean update is $-\mu E[e\, \bar u]$, and $u$ is a linear function of the symbols, so it is enough that $E[e\, a[k-j]] = 0$ for every $j$. With $g = \beta e_d$, $z = \beta a[k-d]$ and $e = \beta a[k-d] - \gamma\, \mathrm{sgn}(a[k-d])$. For $j \ne d$, $a[k-j]$ is independent of $e$ and has mean zero. For $j = d$, $E[e\, a] = \beta E a^2 - \gamma E|a| = (\beta - 1) E a^2$, which is zero only for $\beta = 1$. So $\gamma$ fixes the output scale. The proofs folder has the details and the gradient form of line L5.

**What is not claimed.** A fixed point is not always reached. Benveniste, Goursat and Ruget (1980) proved convergence for an equalizer of unbounded length under conditions on the input distribution. For a finite equalizer, convergence to a perfect equalizer is not guaranteed, and Sato, like CMA, can stop at a poor point. The convergence in the example is a measurement.

## Complexity

Lines L3 to L6 cost $O(N)$ operations per sample. $K$ samples cost $O(K N)$ time in the [real RAM](/real-ram/) and $O(N)$ extra space. Line L5 needs only two sign tests, so the algorithm is as cheap as LMS.

## Properties

- **Blind.** It needs only $\gamma$, which depends on the alphabet and not on the data.
- **A sign ambiguity for PAM.** The cost is even in $z$, and a negated input gives the same taps and a negated output.
- **Phase sensitive for QAM.** The per-axis sign is not invariant under rotation, so the complex taps also remove a carrier phase, up to a multiple of 90 degrees. This needs the phase to be fixed while the equalizer converges; a phase that moves fast spoils the convergence.
- **Never quiet.** For $M$-PAM with $M > 2$, the error of line L5 is not zero even at a perfect equalizer, so the taps keep moving around their target, more so for a larger $\mu$.
- **Works on nonminimum-phase channels.** The sign is a nonlinear function, so the update uses more than second-order statistics.

## Variants and improvements

- **Stop-and-go.** Update only when the Sato error and the decision-directed error have the same sign. This makes the steps less noisy.
- **Generalized Sato.** Benveniste, Goursat and Ruget replaced the sign by other odd functions and gave conditions for convergence.
- **Switch to decision-directed mode.** After the eye opens, replace $\gamma\, \mathrm{sgn}(z)$ by the decision; see [adaptive equalization](/adaptive-equalization/).
- **CMA.** The [constant modulus algorithm](/constant-modulus-algorithm/) replaces the error by $z(|z|^2 - R_2)$, which does not depend on the carrier phase.

## When to use it

Use the Sato algorithm for real PAM, or for QAM when the carrier phase is fixed and the equalizer should also remove it. It is a teaching example of how a nonlinear error makes a blind LMS work. In practice, CMA is the usual choice for QAM because it can run before carrier recovery. With a training sequence, a trained LMS or RLS equalizer converges faster.

## Pitfalls

- **The wrong scale for γ in line L5.** $\gamma$ must match the scale of the received signal. With $\gamma$ for raw levels and a unit-energy signal, the equalizer still converges, but to taps that scale the output by $\gamma_{\text{raw}} / \gamma_{\text{unit}}$, and a fixed slicer then fails.
- **Using the complex form with a moving phase.** The QAM form of line L5 needs a fixed phase. If the carrier phase drifts while the taps converge, the taps chase the phase and the residual ISI stays high.
- **A step that is too large in line L6.** The error never goes to zero, so a large $\mu$ gives a large excess error. Pick a small step, and switch to decision-directed LMS for the final error.
- **A spike at the edge in line L1.** As with CMA, a spike on the first tap allows only a small delay, which does not suit a nonminimum-phase channel.

## Implementations

## History

Yoichi Sato published the method in 1975 as self-recovering equalization of multilevel amplitude modulation. It was the first blind equalizer. Benveniste, Goursat and Ruget (1980) generalized the error function and studied convergence for an equalizer of unbounded length. Godard (1980) gave the dispersion criteria that led to CMA, which replaced Sato in most QAM receivers.

## References
