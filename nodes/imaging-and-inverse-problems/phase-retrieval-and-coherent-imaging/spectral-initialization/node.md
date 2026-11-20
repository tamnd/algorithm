---
tag: 5K2MNA
kind: algorithm
slug: spectral-initialization
name: Spectral initialization for phase retrieval
aliases:
- spectral method for phase retrieval
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: research
summary: "Estimate a signal from y_r = |a_r^* x|^2, up to a global phase, as the top eigenvector of (1/m) sum y_r a_r a_r^* scaled to the estimated norm. It gives the start for Wirtinger flow."
solves: [phase-retrieval]
model: real-ram
complexity:
  vars: {n: the length of the signal, m: the number of measurements, K: the number of power iterations}
  time: {worst: O(K m n)}
  space: {extra: O(n)}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 2015
  people: [Praneeth Netrapalli, Prateek Jain, Sujay Sanghavi, Emmanuel Candès, Xiaodong Li, Mahdi Soltanolkotabi]
  note: Netrapalli, Jain and Sanghavi used the top eigenvector of the weighted sum to start alternating minimization, and Candès, Li and Soltanolkotabi used it to start Wirtinger flow and proved that it is close to the signal for about n log n Gaussian measurements.
prereqs: [phase-retrieval, power-iteration]
see_also: [wirtinger-flow, phaselift, principal-component-analysis, davis-kahan-theorem, rayleigh-quotient, lanczos-algorithm, law-of-large-numbers, eigenvalue]
sources:
  - paper: doi:10.1109/TIT.2015.2399924
    title: Emmanuel J. Candès, Xiaodong Li and Mahdi Soltanolkotabi, Phase retrieval via Wirtinger flow, theory and algorithms, IEEE Transactions on Information Theory 61(4), 2015, 1985 to 2007
    locator: Algorithm 1 (the initialization with lambda^2 = n sum y_r / sum ||a_r||^2), Section 2.3 (the mean I + 2 x x^T in the real Gaussian model), Definition 3.1 (the Gaussian model) and Theorem 3.3 (dist(z_0, x) <= ||x|| / 8 for m >= c_0 n log n) (preprint arXiv 1407.1065)
  - paper: doi:10.1109/TSP.2015.2448516
    title: Praneeth Netrapalli, Prateek Jain and Sujay Sanghavi, Phase retrieval using alternating minimization, IEEE Transactions on Signal Processing 63(18), 2015, 4814 to 4826
    locator: Algorithm 1, step 1 (the start of AltMinPhase from the top singular vector of the sum of y_i^2 a_i a_i^T, with y_i the measured magnitudes) and Theorem 4.1 (accuracy for m >= C n log^3 n) (preprint arXiv 1306.0160)
  - paper: doi:10.1002/cpa.21638
    title: Yuxin Chen and Emmanuel J. Candès, Solving random quadratic systems of equations is nearly as easy as solving linear systems, Communications on Pure and Applied Mathematics 70(5), 2017, 822 to 883
    locator: Section 2.2, truncated spectral initialization, equation (29), with the heavy tail argument and the default alpha_y = 3 (preprint arXiv 1505.05114)
---

Spectral initialization is a way to get a first estimate in [phase retrieval](/phase-retrieval/) with known random sampling vectors. The data are $y_r = |a_r^* x|^2$ for $r = 1, \dots, m$. The method forms the matrix $Y = \frac1m \sum_r y_r a_r a_r^*$, takes its top eigenvector, and scales it to an estimate of $\|x\|$. For Gaussian $a_r$ the mean of $Y$ is $\|x\|^2 I + x x^*$, so with enough measurements the top eigenvector points almost along $x$. The result is used to start nonconvex methods such as [Wirtinger flow](/wirtinger-flow/), which need a start close to the signal.

## In plain words

Each measurement tells you how strongly the unknown signal lines up with one known random direction, but not the sign or phase. Directions that line up well give large values.

So add up all the directions, each with the weight of its measurement. Directions close to the signal get large weights, and the sum leans toward the signal. The direction in which this weighted sum is largest is a good guess for the direction of the signal. The average of the measurements gives a guess for its length. The phase of the whole signal stays unknown, and no method can find it from these data.

## The problem

The input is $m$ sampling vectors $a_r \in \mathbb{C}^n$ and the values $y_r = |a_r^* x|^2$ for an unknown $x$. The output is a vector $z_0$ with a small $\operatorname{dist}(z_0, x) = \min_\varphi \|z_0 - e^{i\varphi} x\|$. The data are the same for $x$ and $e^{i\varphi} x$, so this distance is the right measure of error.

## The algorithm

```pseudo id=main
SPECTRAL-INIT(a₁, …, a_m, y, K, α_y)
L1  λ ← sqrt(n · Σ_r y_r / Σ_r ‖a_r‖²)
L2  T ← {r : y_r ≤ α_y² · mean(y)}            ▷ all r if α_y is not given
L3  v ← a random unit vector
L4  for k ← 1 to K do
L5      w ← (1/m) Σ_{r ∈ T} y_r a_r (a_r* v)
L6      v ← w / ‖w‖
L7  return λ v
```

Line L1 estimates $\|x\|$: for Gaussian vectors $\mathbb{E}[y_r] = \|x\|^2$ and $\mathbb{E}\|a_r\|^2 = n$. Lines L4 to L6 are [power iteration](/power-iteration/) for $Y$, and line L5 applies $Y$ without forming it, with two passes over the vectors. Line L2 is the truncation of Chen and Candès (2017), who leave out the largest values; without $\alpha_y$ it is the plain method of Candès, Li and Soltanolkotabi (2015).

## Example

A small real case by hand. Take $x = (2, 1)$ and the four vectors $e_1$, $e_2$, $(1, 1)$, $(1, -1)$. The data are $y = (4, 1, 9, 1)$, and

$$Y = \frac14 \Bigl[ 4 e_1 e_1^T + e_2 e_2^T + 9 \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix} + \begin{pmatrix} 1 & -1 \\ -1 & 1 \end{pmatrix} \Bigr] = \begin{pmatrix} 3.5 & 2 \\ 2 & 2.75 \end{pmatrix}.$$

Its eigenvalues are $(25 \pm \sqrt{265})/8$, that is $5.160$ and $1.090$. The top eigenvector is $(0.769, 0.639)$, about $13$ degrees from the direction $(0.894, 0.447)$ of $x$. The scale is $\lambda^2 = 2 \cdot 15 / 6 = 5 = \|x\|^2$. So $z_0 = (1.720, 1.428)$, and $\operatorname{dist}(z_0, x) = 0.511$. The implementation finds the same values, up to a global phase.

Random measurements. Take a unit $x \in \mathbb{C}^n$ and complex Gaussian $a_r$, and average $\operatorname{dist}(z_0, x)$ over ten seeds (measurements of the implementation):

| $m / n$ | 2 | 4 | 8 | 16 | 32 |
|---|---|---|---|---|---|
| $n = 8$ | 0.87 | 0.75 | 0.66 | 0.47 | 0.36 |
| $n = 32$ | 1.05 | 0.88 | 0.73 | 0.53 | 0.39 |

The error falls as $m / n$ grows. At these sizes the truncation with $\alpha_y = 3$ changed the mean error by less than 0.005; for complex Gaussian vectors and $\|x\| = 1$, a single $y_r$ is above $9$ with probability $e^{-9}$.

## Correctness

The proof page shows these facts.

- **$Y$ is positive semidefinite,** so power iteration finds its top eigenvector. The error angle shrinks by the factor $\mu_2 / \mu_1$ per step.
- **The mean.** For complex Gaussian vectors $\mathbb{E}[Y] = \|x\|^2 I + x x^*$; for real ones $\|x\|^2 I + 2 x x^T$. The top eigenvector of the mean is $x / \|x\|$.
- **Perturbation.** If $\|Y - \mathbb{E}[Y]\| \le \varepsilon$, then the top eigenvector $v$ of $Y$ has $|u^* v|^2 \ge 1 - 2\varepsilon / \|x\|^2$ with $u = x / \|x\|$.

Candès, Li and Soltanolkotabi (2015, Theorem 3.3) show that $m \ge c_0\, n \log n$ Gaussian measurements give $\operatorname{dist}(z_0, x) \le \frac18 \|x\|$ with high probability. This is cited, not proved here.

## Complexity

Each power step reads all $m$ vectors twice, $O(m n)$ work, and $K$ steps cost $O(K m n)$. The eigenvalue ratio of the mean is $1/2$ (complex) or $1/3$ (real), so a few tens of steps are enough in practice. The extra space is $O(n)$. For coded diffraction measurements the products with $a_r$ are [fast Fourier transforms](/fast-fourier-transform/), and a step costs $O(m \log n)$.

## Properties

- **Up to a global phase.** No method can do better with these data.
- **Not exact.** The estimate is only near $x$; a refinement method must follow.
- **Needs random or generic vectors.** The analysis uses the Gaussian model.
- **Deterministic** once the start of the power iteration is fixed.

## Variants and improvements

- **Truncated spectral method.** Chen and Candès (2017) leave out the $y_r$ above $\alpha_y^2$ times the mean, with $\alpha_y = 3$ by default, because the terms $y_r a_r a_r^*$ have heavy tails. Their truncated Wirtinger flow then needs $m$ of order $n$.
- **Other weights.** The weight $y_r$ can be replaced by another function of $y_r$; the choice changes how many measurements are needed.
- **[Lanczos](/lanczos-algorithm/) in place of power iteration.** Fewer products for the same accuracy.
- **Refinement.** [Wirtinger flow](/wirtinger-flow/), alternating minimization, or a convex method such as [PhaseLift](/phaselift/).

## When to use it

Use the spectral method to start a nonconvex phase retrieval method when the sampling vectors are random or close to random, such as Gaussian vectors or random coded diffraction patterns. The analysis does not cover the classical Fourier problem with a support; the methods for that problem, such as [hybrid input-output](/hybrid-input-output/), usually start from random images.

## Pitfalls

- **Comparing without the phase.** Measure the error with $\operatorname{dist}$, not with $\|z_0 - x\|$.
- **Too few measurements.** With $m$ a small multiple of $n$, the estimate can be far from $x$, as the table shows.
- **Forming $Y$.** It costs $O(m n^2)$ time and $O(n^2)$ space. Apply it as in line L5 instead.
- **Real or complex.** The mean has $2 x x^T$ in the real case and $x x^*$ in the complex case; the gap of the eigenvalues differs.

## Implementations

## History

Netrapalli, Jain and Sanghavi (2015) started their alternating minimization method for phase retrieval with the top singular vector of the sum of $a_i a_i^T$ weighted by the measured intensities. They called this start the new part of their method and showed that it is accurate for $m$ of order $n \log^3 n$ complex Gaussian measurements. Candès, Li and Soltanolkotabi (2015) used the same kind of start for Wirtinger flow, with the scale $\lambda$, and proved that it is within $\|x\|/8$ of the signal for $m$ of order $n \log n$. Chen and Candès (2017) added the truncation, which brings the number of measurements down to the order of $n$.

## References
