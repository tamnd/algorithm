---
tag: 6J62KD
kind: algorithm
slug: fastica
name: FastICA
aliases:
- fast ICA
- fixed-point ICA
area: machine-learning/dimensionality-reduction
level: advanced
summary: "A fixed-point ICA method: after whitening, w ← E[z g(wᵀz)] − E[g'(wᵀz)] w, then normalize. It converges cubically with the kurtosis nonlinearity and needs no step size."
solves: [blind-source-separation]
model: real-ram
complexity:
  vars: {n: the number of observations, d: the dimension, k: the number of components, I: the number of iterations per component}
  time: {worst: "O(n d^2 + d^3 + n d k I)"}
  space: {extra: "Θ(n d + d^2)"}
properties: {deterministic: false, online: false, exact: false, recursive: false, supervised: false, linear: true}
history:
  year: 1997
  people: [Aapo Hyvärinen, Erkki Oja]
  note: Hyvärinen and Oja gave the fixed-point rule for kurtosis in 1997. Hyvärinen extended it to general negentropy approximations, with deflation and symmetric versions, in 1999.
prereqs: [independent-component-analysis, whitening]
see_also: [blind-source-separation, projection-pursuit, principal-component-analysis, gram-schmidt-process, power-iteration, deflation, newton-method-for-systems, factor-analysis]
sources:
  - paper: doi:10.1162/neco.1997.9.7.1483
    title: Aapo Hyvärinen and Erkki Oja, A fast fixed-point algorithm for independent component analysis, Neural Computation 9(7), 1997
    locator: pp. 1483 to 1492 (the kurtosis fixed-point rule and its cubic convergence)
  - paper: doi:10.1109/72.761722
    title: Aapo Hyvärinen, Fast and robust fixed-point algorithms for independent component analysis, IEEE Transactions on Neural Networks 10(3), 1999
    locator: pp. 626 to 634 (negentropy approximations, the general nonlinearities, deflation and symmetric orthogonalization)
  - book: isbn:9780471405405
    title: Aapo Hyvärinen, Juha Karhunen and Erkki Oja, Independent Component Analysis, Wiley, 2001
    locator: Chapter 8 (ICA by maximization of non-Gaussianity, FastICA for kurtosis and for negentropy, estimation of several components)
  - paper: doi:10.1016/S0893-6080(00)00026-5
    title: Aapo Hyvärinen and Erkki Oja, Independent component analysis, algorithms and applications, Neural Networks 13(4-5), 2000
    locator: pp. 411 to 430 (Section 6, the FastICA algorithm)
  - paper: "Erkki Oja and Zhijian Yuan, The FastICA algorithm revisited, convergence analysis, IEEE Transactions on Neural Networks 17(6), 2006"
    locator: pp. 1370 to 1381 (convergence of the one-unit and symmetric versions)
---

FastICA is an algorithm for [independent component analysis](/independent-component-analysis/). After the data are [whitened](/whitening/), it finds a unit vector $w$ such that $w^{\top} z$ is as far from Gaussian as possible, with the fixed-point rule
$$ w \leftarrow E[z\, g(w^{\top} z)] - E[g'(w^{\top} z)]\, w , \qquad w \leftarrow w / \lVert w \rVert , $$
where $g$ is the derivative of a contrast function. The rule is an approximate Newton step, so it needs no learning rate. With $g(u) = u^3$, which maximizes the absolute kurtosis, it converges cubically. Several components are found one at a time with Gram-Schmidt deflation, or all at once with symmetric decorrelation. FastICA is the most widely used ICA method.

## In plain words

FastICA looks for one direction at a time in which the data look least like a bell curve. It starts from a random direction. At each step it looks at how the data project on the current direction, makes a new direction from that, and scales it to length one. This is similar to the power method for eigenvectors, and it settles very fast: once the direction is close, the error drops to about its cube at each step.

To find more than one source, it repeats the search, and each time it removes the parts of the new direction that point along the directions found before. In another version, it moves all directions at once and then makes them perpendicular together, so no direction is favored.

## The problem

The input is $n$ observations $x_t \in \mathbb{R}^d$ of the ICA model $x = A s$ with independent, non-Gaussian, unit-variance sources, and a number $k \le d$ of components to extract. After whitening, $z = V(x - \mu) = Q s$ with $Q$ orthogonal. The task is to find orthonormal vectors $w_1, \ldots, w_k$ such that each $w_p^{\top} z$ is one source up to sign.

**Contrasts.** One unit finds a local extremum of $E[G(w^{\top} z)]$ on the sphere $\lVert w \rVert = 1$, which approximates the negentropy $J(w^{\top} z) \approx c\,(E[G(w^{\top} z)] - E[G(\nu)])^2$ with $\nu$ standard Gaussian. The standard choices of $g = G'$ are:

| name | $G(u)$ | $g(u)$ | $g'(u)$ | use |
|---|---|---|---|---|
| pow3 (kurtosis) | $u^4/4$ | $u^3$ | $3u^2$ | fastest, sensitive to outliers |
| logcosh | $\frac{1}{a}\log\cosh(a u)$ | $\tanh(a u)$ | $a(1 - \tanh^2(a u))$ | good general choice, $1 \le a \le 2$ |
| exp | $-e^{-u^2/2}$ | $u e^{-u^2/2}$ | $(1 - u^2) e^{-u^2/2}$ | robust, for very peaked sources |

## The algorithm

The deflation version:

```pseudo id=main
FASTICA(X, k, g)
L1  z_t ← V (x_t − μ) for all t                                       ▷ whitening, E[z zᵀ] = I
L2  for p = 1 to k do
L3      w ← a random unit vector
L4      repeat
L5          w⁺ ← mean_t[z_t g(wᵀ z_t)] − mean_t[g′(wᵀ z_t)] w
L6          w⁺ ← w⁺ − Σ_{q<p} (w⁺ᵀ w_q) w_q                             ▷ Gram-Schmidt deflation
L7          w⁺ ← w⁺ / ‖w⁺‖;  done ← (|w⁺ᵀ w| ≈ 1);  w ← w⁺
L8      until done;  w_p ← w
L9  return B = [w_1 … w_k]ᵀ V                                            ▷ the sources are B (x − μ)
```

The symmetric version replaces the inner loop. It updates all rows of $W = [w_1 \ldots w_k]^{\top}$ with line L5 at the same time, and then sets
$$ W \leftarrow (W W^{\top})^{-1/2} W , $$
computed from the eigendecomposition $W W^{\top} = E D E^{\top}$ as $E D^{-1/2} E^{\top} W$. It stops when every row satisfies $|w_p^{+\top} w_p| \approx 1$.

The test in line L7 uses the absolute value because $w$ and $-w$ give the same source, and for a source with negative kurtosis the sign of $w$ flips at every step.

## Example

**The population iteration.** Take two whitened sources, a uniform one ($\kappa_1 = -1.2$) and a Laplace one ($\kappa_2 = 3$), and $g(u) = u^3$. In source coordinates $q = Q^{\top} w$, line L5 is exactly $q_i \leftarrow \kappa_i q_i^3$ (Lemma 1 of the proof). Start at $q = (\cos 60°, \sin 60°) = (0.5, 0.866)$:

| step | $q$ | error $\sqrt{1 - q_2^2}$ |
|---|---|---|
| 0 | (0.5, 0.866) | 0.5 |
| 1 | (−0.0768, 0.9971) | 0.0768 |
| 2 | (0.000182, 1.0000) | 0.000182 |
| 3 | (−2.4 × 10⁻¹², 1) | 2.4 × 10⁻¹² |

The number of correct digits roughly triples at each step. The first coordinate changes sign each time, because $\kappa_1 < 0$. The source that is found depends on $u_i = |\kappa_i|^{1/2} |q_i|$. Here $u_2 = 1.5 > u_1 = 0.548$, so the Laplace source wins. From $q = (\cos 30°, \sin 30°)$ instead, $u_1 = 0.949 > u_2 = 0.866$, and the iteration converges to the uniform source, slowly at first because the two values are close.

**A sample.** Mix 3000 such samples with $A = \begin{pmatrix} 1 & 0.7 \\ 0.5 & 1 \end{pmatrix}$. With the logcosh nonlinearity and deflation, the first unit converges in 5 iterations and the second in 2; the second unit has only one direction left after line L6. The result is
$$ B A \approx \begin{pmatrix} -1.021 & -0.018 \\ 0.007 & 1.029 \end{pmatrix} , $$
a signed permutation up to estimation error. The symmetric version takes 4 iterations and gives the same two sources in the other order.

## Correctness

The rule comes from the Lagrange condition $E[z\, g(w^{\top} z)] = \beta w$ for an extremum of $E[G(w^{\top} z)]$ on the sphere. For white data, the Jacobian $E[z z^{\top} g'(w^{\top} z)]$ is approximated by $E[g'(w^{\top} z)] I$, and the resulting Newton step, rescaled, is line L5. For $g(u) = u^3$ and independent sources, the expectations can be computed exactly: in source coordinates the step is $q_i \leftarrow \kappa_i q_i^3$. With $u_i = |\kappa_i|^{1/2} |q_i|$, every ratio $u_i / u_m$ is cubed at each step, so the iterate converges to the source with the largest $u_i$, with error $\varepsilon_{t+1} \le C \varepsilon_t^3 / |q_m|^3$ and $C = \max_{i \ne m} |\kappa_i| / |\kappa_m|$. Deflation keeps the coordinates of the sources already found at 0, and $\kappa_i \cdot 0^3 = 0$, so each source is found once. The full proofs are below.

## Complexity

The model is the [real RAM](/real-ram/), and the costs count arithmetic operations.

- **Whitening.** $\Theta(n d^2)$ for the covariance and to transform the data, and $O(d^3)$ for the eigendecomposition.
- **One iteration of one unit.** $\Theta(n d)$ for line L5 and $\Theta(p d)$ for line L6.
- **Total.** $O(n d^2 + d^3 + n d k I)$ for $I$ iterations per unit. With pow3, $I$ is often below 10; with logcosh, the convergence is quadratic in general and $I$ is still small. The symmetric version costs $\Theta(n d k + k^3)$ per iteration.
- **Memory.** $\Theta(n d + d^2)$ for the whitened data and the matrices.

## Properties

- **No step size.** Unlike gradient methods such as infomax, there is no learning rate to tune.
- **Fast convergence.** Cubic for pow3 when the model holds, and at least quadratic for the other standard nonlinearities (Hyvärinen 1999).
- **Batch method.** Each step uses all the data. There is no natural online version.
- **Random start.** The result depends on the start only through which source is found first and its sign. The set of starts that do not converge to a source has measure zero.
- **Sub- and super-Gaussian sources.** The same rule finds both, because it seeks extrema of $E[G]$ in both directions. Gradient rules need to know the sign of the kurtosis.

## Variants and improvements

- **Deflation against symmetric.** Deflation can stop after $k < d$ components, but errors in early units pass to later units. The symmetric version treats all units alike and is usually more accurate when all components are needed.
- **Stabilized FastICA.** Hyvärinen (1999) adds a step size $\mu$ to the Newton step, $w \leftarrow w - \mu [E[z g] - \beta w] / [E[g'] - \beta]$, which helps when the iteration oscillates.
- **Complex FastICA.** Bingham and Hyvärinen gave a version for complex-valued signals, used for frequency-domain separation.
- **Reduction first.** For $k < d$, do PCA to $k$ dimensions in line L1. This removes noise directions and reduces the cost.

## When to use it

Use FastICA as the default method for linear ICA in batch mode: EEG and MEG artifact removal, fMRI, feature extraction from image patches, and the separation of instantaneous audio mixtures. Use logcosh unless you know that the sources are well behaved, in which case pow3 is faster. Use a time-structure method instead when the sources are close to Gaussian but have different spectra; see [blind source separation](/blind-source-separation/).

## Pitfalls

- **No whitening.** The rule assumes $E[z z^{\top}] = I$. On unwhitened data it does not converge to the sources.
- **Testing $w^{+\top} w \approx 1$.** With a negative-kurtosis source, $w$ flips sign each step and this test never succeeds. Test the absolute value.
- **Gaussian sources.** If two sources are Gaussian, the iteration wanders in their plane and the result is arbitrary.
- **Outliers with pow3.** The cube amplifies large values, and a few outliers can become a component. Use logcosh or exp.
- **Too few samples.** The fixed points of the sample iteration are close to the population fixed points only when $n$ is large compared with $d$. With small $n$ and large $d$, FastICA can produce spiky components that fit noise.
- **Unordered output.** The components come in no meaningful order. Sort them by negentropy or by the variance they explain if an order is needed.

## Implementations

## History

Aapo Hyvärinen and Erkki Oja presented the fixed-point rule for kurtosis in 1997, as a faster alternative to the gradient rules of the time, and showed its cubic convergence. Hyvärinen generalized it in 1999 to the family of negentropy approximations, gave the deflation and symmetric versions, and analyzed it as an approximate Newton method. The FastICA software package for MATLAB made the method standard in signal processing and neuroimaging. Oja and Yuan published a full convergence analysis in 2006.

## References
