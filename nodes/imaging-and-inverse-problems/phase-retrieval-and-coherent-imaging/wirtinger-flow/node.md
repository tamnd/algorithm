---
tag: E17F69
kind: algorithm
slug: wirtinger-flow
name: Wirtinger flow
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: research
summary: "Phase retrieval from y_r = |a_r^* x|^2 by gradient descent on the squared misfit, with Wirtinger derivatives, from a spectral start. For Gaussian a_r it converges linearly to x up to a global phase."
solves: [phase-retrieval]
model: real-ram
complexity:
  vars: {n: the length of the signal, m: the number of measurements, K: the number of iterations}
  time: {worst: O(K m n)}
  space: {extra: O(n)}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 2015
  people: [Emmanuel Candès, Xiaodong Li, Mahdi Soltanolkotabi]
  note: Candès, Li and Soltanolkotabi gave the method and proved that, for about n log n Gaussian measurements, the spectral start followed by gradient steps converges to the signal at a geometric rate.
prereqs: [phase-retrieval, gradient-descent, spectral-initialization]
see_also: [phaselift, error-reduction-algorithm, gerchberg-saxton-algorithm, stochastic-gradient-descent, backtracking-line-search, compressed-sensing, coherent-diffraction-imaging, power-iteration]
sources:
  - paper: doi:10.1109/TIT.2015.2399924
    title: Emmanuel J. Candès, Xiaodong Li and Mahdi Soltanolkotabi, Phase retrieval via Wirtinger flow, theory and algorithms, IEEE Transactions on Information Theory 61(4), 2015, 1985 to 2007
    locator: equations (2.1), (2.2) and (2.5) (the loss, the update and the step schedule), Theorem 3.3 (Gaussian model), Sections 4.2 and 4.3 (experiments), Theorem 5.1 (coded diffraction model), Section 6 (Wirtinger derivatives), Condition 7.9 and Lemma 7.10 (the regularity condition) (preprint arXiv 1407.1065)
  - paper: doi:10.1002/cpa.21638
    title: Yuxin Chen and Emmanuel J. Candès, Solving random quadratic systems of equations is nearly as easy as solving linear systems, Communications on Pure and Applied Mathematics 70(5), 2017, 822 to 883
    locator: the truncated Wirtinger flow and its guarantee for a number of equations of the order of n (preprint arXiv 1505.05114)
---

Wirtinger flow is a nonconvex method for [phase retrieval](/phase-retrieval/) with known sampling vectors. The data are $y_r = |a_r^* x|^2$ for $r = 1, \dots, m$, and the method minimizes the squared misfit

$$f(z) = \frac{1}{2m} \sum_{r=1}^m \bigl(|a_r^* z|^2 - y_r\bigr)^2$$

by gradient steps. The function $f$ is real and not holomorphic, so the gradient is taken with Wirtinger derivatives, which is the same as the ordinary gradient in the real and imaginary parts. The start is the [spectral initialization](/spectral-initialization/). Candès, Li and Soltanolkotabi (2015) proved that for about $n \log n$ Gaussian sampling vectors the start is close to the signal and the steps converge to it at a geometric rate, up to a global phase.

## In plain words

You must find an unknown list of complex numbers. For each of many known random lists you are told how strongly it lines up with the unknown list, but not the phase. Any guess can be scored by how badly it fits these numbers.

Wirtinger flow first makes a good guess from the data alone. Then it goes downhill on the score, step by step, like water that runs down a slope. The score has many dips, and a downhill walk can stop in a wrong one. The theory shows that, with enough random measurements, the land near the true answer slopes straight to it, and the first guess lands there. The phase of the whole answer stays unknown, and no method can find it.

## The problem

The input is $m$ vectors $a_r \in \mathbb{C}^n$ and the values $y_r = |a_r^* x|^2$ for an unknown $x$. The output is a $z$ with a small $\operatorname{dist}(z, x) = \min_\varphi \|z - e^{i\varphi} x\|$. The data are the same for $x$ and $e^{i\varphi} x$, so this is the right measure of error. In the Gaussian model of the theory, the entries of $a_r$ are independent $\mathcal{N}(0, 1/2) + i\,\mathcal{N}(0, 1/2)$.

## The algorithm

```pseudo id=main
WIRTINGER-FLOW(a₁, …, a_m, y, K, τ₀, μ_max)
L1  z ← SPECTRAL-INIT(a₁, …, a_m, y)
L2  s ← ‖z‖²
L3  for τ ← 1 to K do
L4      μ ← min(1 − exp(−τ/τ₀), μ_max)
L5      g ← (1/m) Σ_r (|a_r* z|² − y_r) a_r (a_r* z)
L6      z ← z − (μ / s) g
L7  return z
```

Line L1 is the top eigenvector of $\frac1m \sum_r y_r a_r a_r^*$, scaled to the estimate $\lambda^2 = n \sum_r y_r / \sum_r \|a_r\|^2$ of $\|x\|^2$. Line L5 is the Wirtinger gradient $\partial f / \partial \bar z$. It needs one pass to form the values $a_r^* z$ and one pass to add up the vectors. Line L6 divides the step by $\|z_0\|^2$, which makes the method the same for every scale of $x$. Line L4 is the schedule of the authors: small steps first, then the cap $\mu_{\max}$. They suggest $\tau_0 \approx 330$ and $\mu_{\max} \approx 0.4$ in (2.5), and they used $0.2$ in their experiments with Gaussian vectors. The theorem is for a constant step $\mu \le c_1 / n$.

## Example

Take $n = 8$, $m = 64$, a unit vector $x \in \mathbb{C}^8$ and complex Gaussian vectors, all from seed 1. The table gives $\operatorname{dist}(z_\tau, x)$ for two caps of the step, with $\tau_0 = 330$ (measurements of the implementation):

| step $\tau$ | 0 | 50 | 100 | 200 | 300 | 500 | 1000 |
|---|---|---|---|---|---|---|---|
| $\mu_{\max} = 0.3$ | 0.67 | 0.17 | 0.0099 | 1.7e-5 | 3.0e-8 | 9.3e-14 | 1.9e-16 |
| $\mu_{\max} = 0.4$ | 0.67 | 0.17 | 0.0099 | 4.7e-6 | 9.1e-10 | 1.0e-7 | 0.078 |

The spectral start is $0.67$ from $x$. With the cap $0.3$, the error falls at a steady geometric rate once the steps reach the cap, and it ends at the level of rounding errors. With the cap $0.4$, it falls faster at first. Then the error grows again, and the iterates stay at a distance of $0.078$ up to step 2500.

The reason is the curvature at the solution. Near $x$ the method is gradient descent with the step $\mu / (2\|z_0\|^2)$ on the real and imaginary parts, and $x$ is a stable fixed point only if this step is below $2 / \lambda$, where $\lambda$ is the largest eigenvalue of the real Hessian of $f$ at $x$. That is $\mu < 4\|z_0\|^2 / \lambda$. For seed 1 this limit is $0.387$, so the cap $0.4$ is too large, and the rounding errors grow. Over seeds 1 to 5 the limit was $0.35$ to $0.45$. With the cap $0.4$, seeds 1 and 4 failed. With the cap $0.3$, all five reached a distance below $10^{-15}$ by step 1000. For large $m$ the Hessian is close to its mean, whose largest eigenvalue is $8\|x\|^2$, and the limit is near $0.5$.

## Correctness

The proof page shows these facts.

- **The gradient.** For a real $t$, $\frac{d}{dt} f(z + t d) = 2 \operatorname{Re}\langle g(z), d \rangle$ at $t = 0$. So $-g$ is the steepest descent direction, and line L6 is gradient descent on $\mathbb{R}^{2n}$.
- **Solutions and stationary points.** $f \ge 0$, and $f(z) = 0$ exactly when $z$ fits all the data. Every $e^{i\varphi} x$ is a zero of $f$ and of $g$. The point $z = 0$ is also a stationary point, but not a solution, so the start matters.
- **Descent.** A small enough step decreases $f$.
- **Linear convergence.** If $\operatorname{Re}\langle g(z), z - e^{i\varphi(z)} x \rangle \ge \frac1\alpha \operatorname{dist}^2(z, x) + \frac1\beta \|g(z)\|^2$ near the solutions, then every step $\mu \le 2/\beta$ shrinks $\operatorname{dist}^2$ by the factor $1 - 2\mu/\alpha$.

Candès, Li and Soltanolkotabi (2015, Theorem 3.3) show that for $m \ge c_0\, n \log n$ Gaussian vectors this condition holds and the spectral start is within $\frac18\|x\|$ of the signal, with high probability. With a constant step $\mu \le c_1 / n$, this gives

$$\operatorname{dist}(z_\tau, x) \le \frac18 \Bigl(1 - \frac\mu4\Bigr)^{\tau/2} \|x\| .$$

This theorem is cited, not proved here.

## Complexity

One step costs $O(m n)$ for general vectors: two passes over the $m$ vectors of length $n$. $K$ steps cost $O(K m n)$, and the extra space is $O(n)$ for $z$ and $g$. With $\mu = c_1 / n$, the theorem needs $O(n \log(1/\varepsilon))$ steps for the accuracy $\varepsilon$, so $O(m n^2 \log(1/\varepsilon))$ in total. For coded diffraction patterns with $L$ masks, $m = L n$, and the products with the $a_r$ are [fast Fourier transforms](/fast-fourier-transform/). One step then costs $O(L n \log n)$. Theorem 5.1 of the same paper gives a constant step there, with $L \ge c_0 (\log n)^4$ patterns.

## Properties

- **Up to a global phase.** No method can do better with these data.
- **Nonconvex.** $f$ is a quartic with stationary points that are not solutions, such as $z = 0$. The guarantee depends on the start and on random vectors.
- **Linear convergence** near the signal, in theory with a step of order $1/n$ for Gaussian vectors.
- **Deterministic** once the start of the power iteration is fixed.
- **Simple steps.** Only products with the $a_r$ and $a_r^*$; no matrix of size $n \times n$ is formed.

## Variants and improvements

- **Truncated Wirtinger flow.** Chen and Candès (2017) leave out the terms with large values in the start and in the gradient. Their method needs a number of equations of the order of $n$, which removes the $\log n$ factor.
- **Coded diffraction patterns.** Candès, Li and Soltanolkotabi (2015) give a variant of the method with a theorem for random masks and Fourier measurements (Theorem 5.1).
- **Other losses.** The misfit can use the magnitudes $|a_r^* z|$ in place of their squares, or another loss of the two values.
- **Step rules.** A [backtracking line search](/backtracking-line-search/) in place of the fixed schedule. A [stochastic](/stochastic-gradient-descent/) version uses one or a few $r$ per step.
- **Convex relaxation.** [PhaseLift](/phaselift/) solves a semidefinite program in place of the nonconvex problem. It needs order $n$ measurements but works with $n \times n$ matrices.

## When to use it

Use Wirtinger flow when the sampling vectors are random or close to random, such as Gaussian vectors or random coded diffraction patterns, and the signal is too large for a semidefinite program. Candès, Li and Soltanolkotabi report that about $4.5 n$ Gaussian measurements were enough for exact recovery with high probability in their trials with $n = 128$ (Section 4.2), and they recovered photographs of more than a million pixels from 20 coded diffraction patterns (Section 4.3). For the classical Fourier problem with a support, as in [coherent diffraction imaging](/coherent-diffraction-imaging/), the theory does not apply, and the projection methods such as [error reduction](/error-reduction-algorithm/) are more common.

## Pitfalls

- **Comparing without the phase.** Measure the error with $\operatorname{dist}$, not with $\|z - x\|$.
- **A step that is too large.** The example shows a cap of $0.4$ that loses a solution it had found to $10^{-9}$. The safe step depends on the curvature at $x$, which changes with $m$ and the seed. If the error grows again, lower $\mu_{\max}$.
- **A bad start.** From a random start the method can stop at a stationary point that is not a solution, such as near $z = 0$.
- **Too few measurements.** With fewer than $2n$ real values, a signal in $\mathbb{C}^n$ cannot be determined. For a small multiple of $n$ the method can fail even from the spectral start.
- **Real or complex.** For real signals and real vectors the same code works, but the phase is only a sign, and the mean of the spectral matrix is different.

## Implementations

## History

Candès, Li and Soltanolkotabi put the method on arXiv in 2014 and published it in 2015. The proof shows convergence to the signal from a start that can be computed, for a method that works on vectors of length $n$ and not on $n \times n$ matrices as PhaseLift does. Their paper also gives a variant for coded diffraction patterns, and recovers large images from such data. Chen and Candès (2017) added truncation to the start and the gradient and showed that a number of measurements of the order of $n$ is enough.

## References
