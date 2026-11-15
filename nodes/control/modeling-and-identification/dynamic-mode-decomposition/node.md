---
tag: BZWTTE
kind: algorithm
slug: dynamic-mode-decomposition
name: Dynamic mode decomposition
aliases:
- DMD
area: control/modeling-and-identification
level: research
summary: Fits a linear operator that maps each snapshot of a system to the next by a truncated SVD, and returns its eigenvalues and modes.
solves: [system-identification]
model: real-ram
complexity:
  vars: {q: the length of a snapshot, M: the number of snapshot pairs, r: the rank kept}
  time: {worst: "O(q M min(q, M) + q M r + r^4)"}
  space: {extra: O(q M)}
properties: {deterministic: true, online: false, exact: true, iterative: false}
history:
  year: 2010
  people: [Peter J. Schmid]
  note: "Schmid introduced dynamic mode decomposition for flow data in the Journal of Fluid Mechanics in 2010; Tu, Rowley, Luchtenburg, Brunton and Kutz defined exact DMD in 2014."
prereqs: [singular-value-decomposition, eigenvalue, pseudoinverse]
see_also: [eigensystem-realization-algorithm, sindy, principal-component-analysis, prony-method, arnoldi-iteration, least-squares-problem, system-identification, model-order-reduction]
sources:
  - paper: doi:10.1017/s0022112010001217
    title: "Peter J. Schmid, Dynamic mode decomposition of numerical and experimental data, Journal of Fluid Mechanics 656, 5-28, 2010"
    locator: the definition of DMD from a sequence of snapshots and the SVD-based computation of the projected operator
  - paper: doi:10.3934/jcd.2014.1.391
    title: "Jonathan H. Tu, Clarence W. Rowley, Dirk M. Luchtenburg, Steven L. Brunton and J. Nathan Kutz, On dynamic mode decomposition: Theory and applications, Journal of Computational Dynamics 1(2), 391-421, 2014"
    locator: the definition of exact DMD, the theorem that its eigenpairs are eigenpairs of X' X^+, and the relation to linear consistency
  - paper: doi:10.1017/s0022112009992059
    title: "Clarence W. Rowley, Igor Mezic, Shervin Bagheri, Philipp Schlatter and Dan S. Henningson, Spectral analysis of nonlinear flows, Journal of Fluid Mechanics 641, 115-127, 2009"
    locator: the relation between the Arnoldi-type snapshot method and the eigenvalues of the Koopman operator
  - book: isbn:9781611974492
    title: "J. Nathan Kutz, Steven L. Brunton, Bingni W. Brunton and Joshua L. Proctor, Dynamic Mode Decomposition: Data-Driven Modeling of Complex Systems, SIAM, 2016"
    locator: the chapter that introduces the DMD algorithm, and the chapter on DMD with control
---

Dynamic mode decomposition (DMD) takes a sequence of snapshots $x_0, x_1, \ldots, x_M$ of a system, taken at equal time steps $h$, and fits the linear map $A$ with $x_{k+1} \approx A x_k$ in the least squares sense. The snapshots can be long, for example a flow field with $q = 10^6$ values, so DMD never forms $A$. It projects $A$ onto the leading left singular vectors of the data, which gives a small $r \times r$ matrix, and returns its eigenvalues and the matching modes in the full space. Each eigenvalue gives a frequency and a growth or decay rate, and each mode gives a spatial shape. DMD differs from the [eigensystem realization algorithm](/eigensystem-realization-algorithm/), which uses Markov parameters of a system with inputs and returns a state-space model, and from [SINDy](/sindy/), which fits a sparse nonlinear model. DMD has no input in its basic form and gives only a linear model of the snapshots.

## In plain words

Put the snapshots side by side as the columns of a matrix $X$, and the same snapshots one step later as the columns of $X'$. Look for one matrix that moves every column of $X$ to the matching column of $X'$. The snapshots are usually much longer than they are many, so first compress them: the SVD gives a few directions that describe the data well. Write the one-step map in these few directions. Its eigenvalues tell how each pattern turns and decays from one snapshot to the next, and each eigenvector, taken back to the full space, is a pattern that only changes by a factor at each step.

## The problem

**Input.** Snapshots $x_0, \ldots, x_M \in \mathbb{R}^q$ at equal time steps $h$, and a rank $r$ or a threshold to choose it.

**Output.** Eigenvalues $\lambda_1, \ldots, \lambda_r$ and modes $\varphi_1, \ldots, \varphi_r \in \mathbb{C}^q$, and the singular values of the data. The continuous-time eigenvalues are $\omega_l = \ln(\lambda_l) / h$.

**Notation.** $X = (x_0, \ldots, x_{M-1})$ and $X' = (x_1, \ldots, x_M)$, both $q \times M$. $X^{+}$ is the [pseudoinverse](/pseudoinverse/).

## The algorithm

```pseudo id=main
EXACT-DMD(x_0, ..., x_M, r)
L1  X ← (x_0, ..., x_(M-1));  X' ← (x_1, ..., x_M)
L2  (U, S, V) ← the SVD of X
L3  choose r (the numerical rank of X, or given)
L4  Ã ← U_r^T X' V_r S_r⁻¹
L5  (λ_1, ..., λ_r) ← the eigenvalues of Ã
L6  for each λ_l ≠ 0, with Ã w_l = λ_l w_l: φ_l ← X' V_r S_r⁻¹ w_l / λ_l
L7  return (λ, φ, S)
```

The least squares map of minimum norm with $A X = X'$ is $A = X' X^{+}$. With $X = U_r S_r V_r^T$, $\tilde A = U_r^T A U_r$ is its compression to the range of $U_r$, an $r \times r$ matrix. L6 gives the exact DMD modes of Tu et al. (2014): every pair $(\lambda_l, \varphi_l)$ with $\lambda_l \ne 0$ is an eigenpair of $X' X^{+}$. Schmid's original projected DMD uses the modes $U_r w_l$ instead; for linear data with an invariant range the two are the same.

The code computes the SVD with the one-sided Jacobi method, the eigenvalues as the roots of the characteristic polynomial of $\tilde A$, and each $w_l$ by two steps of inverse iteration. For a model of the data, solve for amplitudes $b$ with $x_0 \approx \sum_l b_l \varphi_l$; then $x_k \approx \sum_l b_l \lambda_l^k \varphi_l$.

## Example

Take $q = 32$ points $g_i = 2 \pi i / 32$ on a circle and the snapshots

$$x_k(g_i) = \operatorname{Re}\big(\mu_1^k e^{\mathrm{i} g_i}\big) + 0.5 \operatorname{Re}\big(\mu_2^k e^{3 \mathrm{i} g_i}\big), \qquad \mu_1 = e^{(-0.1 + 2 \mathrm{i}) h}, \quad \mu_2 = e^{(-0.3 + 5 \mathrm{i}) h},$$

with $h = 0.1$ and $k = 0, \ldots, 20$. These are two waves that turn and decay at different rates. The data lie in the 4-dimensional space spanned by $\cos g$, $\sin g$, $\cos 3g$ and $\sin 3g$, and the map from one snapshot to the next is linear on that space.

**Exact data.** The singular values of the $32 \times 20$ matrix $X$ are

$$12.648775, \quad 10.407223, \quad 5.010935, \quad 4.580128, \quad 0, \ldots$$

So $r = 4$. The continuous-time eigenvalues $\ln(\lambda) / h$ are $-0.1 \pm 2 \mathrm{i}$ and $-0.3 \pm 5 \mathrm{i}$ to 13 digits.

**Noisy data (measurement).** Add Gaussian noise with standard deviation $0.05$ to every value and keep $r = 4$. With seed 1 the eigenvalues are $-0.0891 \pm 2.0079 \mathrm{i}$ and $-0.3284 \pm 5.0044 \mathrm{i}$. With seeds 2 and 3 they are $-0.1161 \pm 1.9914 \mathrm{i}$, $-0.3338 \pm 4.9795 \mathrm{i}$ and $-0.1059 \pm 2.0090 \mathrm{i}$, $-0.3162 \pm 5.0322 \mathrm{i}$. The frequencies are good to about 1 percent; the decay rates have larger errors, and for the fast wave all three seeds give too much damping.

## Correctness

**Claim.** With $r$ equal to the rank of $X$, every returned pair with $\lambda \ne 0$ is an eigenpair of $X' X^{+}$. If the snapshots satisfy $x_{k+1} = A x_k$ and $x_M$ lies in the span of $x_0, \ldots, x_{M-1}$, then every returned $\lambda$ is an eigenvalue of $A$ and $\varphi$ is an eigenvector of $A$ for it.

**Key invariant.** $\tilde A = U_r^T X' X^{+} U_r$, and $U_r^T \varphi = w$. For linear data with an invariant range, $A U_r = U_r \tilde A$.

The first statement follows from $X' X^{+} \varphi = X' V_r S_r^{-1} U_r^T \varphi = X' V_r S_r^{-1} w = \lambda \varphi$. For the second, $X' = A X$ gives $X' V_r S_r^{-1} = A U_r$. The full proof is below.

## Complexity

In the [real RAM](/real-ram/). L2 is an SVD of a $q \times M$ matrix, $O(q M \min(q, M))$ in the usual dense count. The Jacobi method of the code does this much work per sweep, and the number of sweeps depends on the data. L4 costs $O(q M r)$. L5 uses the Faddeev-LeVerrier recursion, $O(r^4)$, and a polynomial root finder; a [QR algorithm](/qr-algorithm/) would cost $O(r^3)$. L6 costs $O(q r^2)$. The extra space is $O(q M)$ for the matrices.

For $q \gg M$, the cost is linear in $q$, which is why DMD works on large flow fields. The method of snapshots computes the SVD from the $M \times M$ matrix $X^T X$ for the same reason, with a loss of accuracy for small singular values.

## Properties

- **Exact for linear data (theorem).** If $x_{k+1} = A x_k$ and the range of $X$ is invariant under $A$, the eigenvalues are eigenvalues of $A$ and the modes are its eigenvectors.
- **Eigenpairs of the least squares map (theorem).** For any data, the exact DMD pairs are eigenpairs of $X' X^{+}$ (Tu et al. 2014).
- **Only the excited modes.** DMD finds only the eigenvalues whose modes appear in the data. A mode that $x_0$ does not excite is not found.
- **Biased by noise (measurement).** Noise in the snapshots biases the eigenvalues, mainly the decay rates, as in the example. The noise enters $X$ as well as $X'$, so this is an errors-in-variables problem, and plain least squares is biased.
- **Linear model.** For a nonlinear system, DMD fits a linear model to the data. Rowley et al. (2009) relate the eigenvalues to the eigenvalues of the Koopman operator, which acts linearly on functions of the state; whether the linear model is accurate depends on the observables in the snapshots.
- **Standing waves need more.** A standing wave $x_k = \cos(\omega k h) v$ gives data of rank 1, and DMD returns one real eigenvalue, not the pair $e^{\pm \mathrm{i} \omega h}$. Stack delayed snapshots (Hankel DMD) to get enough rank.

## Variants and improvements

- **Projected DMD.** Schmid's original modes $U_r w$. They are in the range of the data but are not eigenvectors of $X' X^{+}$ in general.
- **Total least squares DMD and forward-backward DMD.** Reduce the noise bias by treating $X$ and $X'$ symmetrically.
- **Optimized DMD.** Fits $x_k \approx \sum_l b_l e^{\omega_l k h} \varphi_l$ by [nonlinear least squares](/nonlinear-least-squares/), with less noise bias, at the cost of an iterative search.
- **DMD with control.** Fits $x_{k+1} \approx A x_k + B u_k$ from snapshots and inputs.
- **Extended DMD.** Uses a dictionary of nonlinear functions of the state as observables, as an approximation of the Koopman operator.
- **Hankel DMD.** Uses delayed copies of a short measurement vector, which connects DMD with the [eigensystem realization algorithm](/eigensystem-realization-algorithm/) and the [Prony method](/prony-method/).
- **Streaming and compressed DMD.** Update the SVD as snapshots arrive, or work on random projections of very long snapshots.

## When to use it

Use DMD to find the dominant frequencies, growth rates and spatial patterns in a large set of snapshots, for example from a flow simulation or a video, when there is no input or the input is not recorded. It is fast, needs only linear algebra, and has one tuning choice, the rank. It is a good first look at the data. For a model with inputs, use DMD with control or a subspace method. For noisy data and accurate damping, use a variant with less bias. For nonlinear dynamics with few states, a sparse model from SINDy can be more accurate.

## Pitfalls

- **The rank.** A rank that is too high fits the noise and gives spurious eigenvalues; a rank that is too low merges modes. Look at the singular values.
- **Too few snapshots.** If $x_M$ is not in the span of the earlier snapshots, Theorem 2 of the proof does not apply, and the eigenvalues can be wrong even without noise.
- **Transient and steady data.** A mean value in the data is a mode with $\lambda = 1$. Subtract the mean if you do not want it, and know that this changes the problem.
- **Eigenvalues and time step.** $\omega = \ln(\lambda) / h$ is defined up to multiples of $2 \pi \mathrm{i} / h$. A frequency above the Nyquist limit $\pi / h$ aliases.
- **Zero eigenvalues.** The exact mode is not defined for $\lambda = 0$; the code rejects it. Use the projected mode or lower the rank.
- **Interpreting modes.** Modes are not orthogonal and their scale is arbitrary. Compare amplitudes $b_l$, not the norms of the modes.

## Implementations

## History

Schmid published dynamic mode decomposition in the Journal of Fluid Mechanics in 2010, as a way to extract coherent structures and their frequencies from flow data. Rowley, Mezic, Bagheri, Schlatter and Henningson (2009) related the method to the spectral analysis of the Koopman operator for nonlinear systems. Tu, Rowley, Luchtenburg, Brunton and Kutz (2014) defined exact DMD and proved that its eigenpairs are those of the least squares operator. Kutz, Brunton, Brunton and Proctor wrote a book on the method in 2016. The algebra is close to older methods: Prony's method, the Arnoldi iteration and realization from a Hankel matrix.

## References
