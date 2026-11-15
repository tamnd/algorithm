---
tag: 8Q2BQ4
kind: algorithm
slug: eigensystem-realization-algorithm
name: Eigensystem realization algorithm
aliases:
- ERA
area: control/modeling-and-identification
level: advanced
summary: Fits a state-space model to measured impulse response data by a truncated SVD of their block Hankel matrix; exact and balanced on noise-free data.
solves: [realization-problem]
model: real-ram
complexity:
  vars: {N: the number of block rows and block columns of the Hankel matrix, n: the chosen order, m: the number of inputs, p: the number of outputs}
  time: {worst: O(N^3 m p (m + p))}
  space: {extra: O(N^2 m p)}
properties: {deterministic: true, online: false, exact: true, iterative: false}
history:
  year: 1985
  people: [Jer-Nan Juang, Richard S. Pappa]
  note: "Juang and Pappa introduced ERA in 1985 for the modal identification of flexible spacecraft structures, building on the SVD form of Ho-Kalman realization by Zeiger and McEwen (1974) and Kung (1978)."
prereqs: [ho-kalman-algorithm, singular-value-decomposition, markov-parameters]
see_also: [realization-problem, minimal-realization, balanced-realization, hankel-singular-values, subspace-identification, prony-method, dynamic-mode-decomposition, eigenvalue]
sources:
  - paper: doi:10.2514/3.20031
    title: "Jer-Nan Juang and Richard S. Pappa, An eigensystem realization algorithm for modal parameter identification and model reduction, Journal of Guidance, Control, and Dynamics 8(5), 620-627, 1985"
    locator: the algorithm, the choice of order from the singular values, and the modal accuracy indicators
  - book: isbn:9780130792112
    title: "Jer-Nan Juang, Applied System Identification, Prentice Hall, 1994"
    locator: the chapter on system realization (ERA and its variants)
  - paper: doi:10.1524/auto.1966.14.112.545
    title: "B. L. Ho and Rudolf E. Kalman, Effective construction of linear state-variable models from input/output functions, Regelungstechnik 14(1-12), 545-548, 1966"
    locator: the exact realization from the Hankel matrix that ERA extends to noisy data
---

The eigensystem realization algorithm (ERA) fits a discrete-time state-space model $x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$ to measured samples of the [impulse response](/impulse-response/), the [Markov parameters](/markov-parameters/) $h_0 = D$ and $h_k = C A^{k-1} B$. It puts the samples in a block Hankel matrix, takes its singular value decomposition, keeps the $n$ largest singular values, and computes $A$, $B$ and $C$ from the kept factors. The [Ho-Kalman algorithm](/ho-kalman-algorithm/) does the same with an exact rank and needs exact data. ERA replaces the exact rank by a truncated SVD, so it works on noisy measurements, and the size of the dropped singular values shows how much of the data the model leaves out. On noise-free data ERA returns a minimal realization that is balanced over the data window. The name comes from its first use: the eigenvalues and eigenvectors of $A$ give the frequencies, damping ratios and mode shapes of a vibrating structure.

## In plain words

Tap a structure and record the response at a few sensors. Write the samples in a table where each row is the row above it moved one step in time. If the structure has a few modes, the table is almost a sum of a few simple patterns, and the rest is noise. The singular value decomposition sorts the patterns by size. Keep the large ones and drop the small ones. The kept patterns, taken from the table and from the same table moved one step, give a small model. Its eigenvalues are the modes of the structure.

## The problem

**Input.** Measured matrices $h_0, h_1, \ldots, h_{2N}$ of size $p \times m$ (the response at $p$ outputs to a unit pulse at each of $m$ inputs, sampled with period $h$), the number $N$ of block rows, and the order $n$ or a rule to choose it.

**Output.** $(A, B, C, D)$ of order $n$ whose Markov parameters $C A^{k-1} B$ are close to the data, and the singular values of the Hankel matrix.

The block Hankel matrix $H$ has block $(i, j)$ equal to $h_{i+j-1}$ for $i, j = 1, \ldots, N$, so it is $Np \times Nm$. The shifted matrix $H_s$ has block $(i, j)$ equal to $h_{i+j}$. There is no separate page for the Hankel matrix; the [Ho-Kalman](/ho-kalman-algorithm/) page shows its layout.

## The algorithm

```pseudo id=main
ERA(h, N, n)
L1  H ← the block Hankel matrix of h_1, ..., h_(2N-1)
L2  Hs ← the shifted block Hankel matrix of h_2, ..., h_(2N)
L3  (U, Σ, V) ← the singular value decomposition of H
L4  if n is not given then n ← the number of σ_k above tol · σ_1
L5  Un, Vn ← the first n columns of U and V;  Σn ← diag(σ_1, ..., σ_n)
L6  A ← Σn^(-1/2) Unᵀ Hs Vn Σn^(-1/2)
L7  B ← the first m columns of Σn^(1/2) Vnᵀ
L8  C ← the first p rows of Un Σn^(1/2)
L9  D ← h_0
L10 return (A, B, C, D, Σ)
```

L3 is the only expensive step. The implementation uses a one-sided Jacobi method, which orthogonalizes the columns of $H$ by plane rotations. L4 is the order choice: on exact data the singular values after the $n$-th are zero, and on noisy data the user looks for a gap. L6 is the least squares solution of $U_n \Sigma_n^{1/2} A \, \Sigma_n^{1/2} V_n^T = H_s$: the shifted Hankel matrix is the same product of factors with one extra $A$ in the middle. L7 and L8 take the first block column and the first block row of the factors, as in Ho-Kalman.

## Example

Take a structure with two lightly damped modes, $(\omega, \zeta) = (2\ \text{rad/s}, 0.05)$ and $(5\ \text{rad/s}, 0.02)$, one input and two outputs, sampled with $h = 0.1$ s. The true model is the real modal form with blocks $\begin{pmatrix} \operatorname{Re} z & \operatorname{Im} z \\ -\operatorname{Im} z & \operatorname{Re} z \end{pmatrix}$ for $z = e^{s h}$, $s = -\zeta \omega + i \omega \sqrt{1 - \zeta^2}$, with $B = (1, 0, 1, 0)^T$, $C = \begin{pmatrix} 1 & 0 & 0.5 & 0 \\ 0 & 1 & 0 & 1 \end{pmatrix}$ and $D = 0$. With $N = 10$, $H$ is $20 \times 10$ and uses $h_1, \ldots, h_{19}$.

**Exact data.** The singular values are

$$7.452986, \quad 4.507395, \quad 3.448610, \quad 1.240241, \quad 0, \ldots, 0.$$

So L4 picks $n = 4$. The eigenvalues of $A$ are $0.86890 \pm 0.47457 i$ and $0.97036 \pm 0.19645 i$. Mapped back by $s = \ln(z) / h$, they give $\omega = 5$, $\zeta = 0.02$ and $\omega = 2$, $\zeta = 0.05$, correct to about $10^{-14}$. The result reproduces $h_k$ also for $k$ beyond the data, and its 10-step observability and controllability gramians are both $\operatorname{diag}(7.452986, 4.507395, 3.448610, 1.240241)$.

**Noisy data (measurement).** Add Gaussian noise with standard deviation $0.01$ to every entry of $h_1, \ldots, h_{20}$, with seed 1. The singular values become

$$7.4412, \quad 4.4975, \quad 3.4678, \quad 1.2309, \quad 0.0496, \quad 0.0422, \ldots$$

The gap after the fourth value is a factor of 25, so $n = 4$ is clear. The recovered modes are $\omega = 4.9905$, $\zeta = 0.02486$ and $\omega = 1.9896$, $\zeta = 0.04882$. Over the seeds 1 to 10, the largest error of a discrete eigenvalue was between $0.0016$ and $0.0085$. The damping ratio of the lighter mode is the least accurate number, which is usual for ERA.

## Correctness

**Claim.** If the data are exact Markov parameters of a system of order at most $N$ and $n$ is the rank of $H$, ERA returns a minimal realization of the data. Its $N$-step observability and controllability gramians are both $\Sigma_n$. With noise whose Hankel matrix $E$ has $\lVert E \rVert_2 < \sigma_n / 2$, the gap after $\sigma_n$ survives.

**Key invariant.** $H = \mathcal{O} \mathcal{C}$ and $H_s = \mathcal{O} A_0 \mathcal{C}$ for the observability and controllability matrices of a minimal realization. The SVD factors $P = U_n \Sigma_n^{1/2}$ and $Q = \Sigma_n^{1/2} V_n^T$ are $\mathcal{O} T$ and $T^{-1} \mathcal{C}$ for one nonsingular $T$.

L6 then gives $T^{-1} A_0 T$, L7 gives $T^{-1} B_0$ and L8 gives $C_0 T$. The gramians are $P^T P = Q Q^T = \Sigma_n$ because $U_n$ and $V_n$ have orthonormal columns. The noise statement is Weyl's inequality for singular values. The full proof is below.

## Complexity

In the [real RAM](/real-ram/), counting a dense SVD of an $a \times b$ matrix with $a \ge b$ as $O(a b^2)$ operations, as for the other dense factorizations. Here $a = N \max(m, p)$ and $b = N \min(m, p)$, so L3 costs $O(N^3 m p \min(m, p))$, which is at most $O(N^3 m p (m + p))$. L6 forms $U_n^T H_s V_n$ in $O(N^2 m p n)$. L7 and L8 cost $O(N n (m + p))$. The SVD dominates. The extra space is $O(N^2 m p)$ for $H$, $H_s$ and the factors.

The SVD is iterative in every real implementation. For the one-sided Jacobi method of the code, one sweep costs $O(a b^2)$. The number of sweeps is a measurement, not a bound: the code stops when every pair of columns is orthogonal to a relative tolerance of $10^{-15}$, and it allows at most 80 sweeps.

## Properties

- **Exact on exact data (theorem).** The result is a minimal realization, as with Ho-Kalman.
- **Balanced over the window (theorem).** The $N$-step gramians are equal and diagonal. For a system with $A$ Schur they tend to the infinite gramians as $N$ grows, so the singular values approach the [Hankel singular values](/hankel-singular-values/) and the result approaches a [balanced realization](/balanced-realization/).
- **Built-in model reduction.** Keeping fewer than the rank of $H$ drops the weakest states of the balanced form, much like [balanced truncation](/balanced-truncation/).
- **Order gap under noise (theorem).** If the noise in the Hankel matrix has induced 2-norm below $\sigma_n / 2$, the gap at the true order is visible.
- **Biased under noise.** For a fixed noise level the eigenvalues are biased, and the damping ratios are the most affected numbers. The bias goes to zero with the noise level (the continuity part of the proof), but the method gives no bound on it for a fixed noise level.
- **Deterministic and not recursive.** New data need a new SVD.

## Variants and improvements

- **Rectangular Hankel matrices.** Use $r$ block rows and $c$ block columns with $r p$ and $c m$ both larger than $n$. Using more columns than rows averages the noise. This is the form in Juang and Pappa 1985.
- **ERA/DC.** ERA with data correlations (Juang, Cooper and Wright, 1988) applies the SVD to products of Hankel matrices, which reduces the effect of noise.
- **OKID and ERA.** Observer/Kalman filter identification estimates the Markov parameters from general input-output data, not only from pulse responses, and then runs ERA.
- **Modal accuracy indicators.** Juang and Pappa added the modal amplitude coherence and the modal phase collinearity to separate true modes from noise modes.
- **Shift with the observability factor.** Compute $A$ from $P[1{:}(N-1)p, :] \, A = P[p{+}1{:}Np, :]$ by least squares. This uses only $H$ and needs no $H_s$. It is the form of Kung's method and of [MOESP](/moesp/).
- **[Subspace identification](/subspace-identification/).** Avoids the estimate of the Markov parameters and works directly on input-output data.

## When to use it

Use ERA for modal analysis of structures and flexible systems from impact or pulse tests, for a state-space model from a measured or simulated impulse response, and as a reduction step after an FIR or high-order ARX fit. It is a direct method with no iteration and no starting value, so it also gives starting values for the [prediction error method](/prediction-error-method/). Do not use it with input-output data from a general input without first estimating the Markov parameters, or use a subspace method directly.

## Pitfalls

- **The order from a bad gap.** Real data often show no clean gap. Taking too many states adds noise modes with random damping; taking too few merges close modes. Check the modes with a stabilization diagram (the poles for a range of $n$) or the modal accuracy indicators.
- **Too few block rows.** The method needs $N p \ge n$ and $N m \ge n$, and in practice much more, so that every mode appears in many rows. With $N$ too small the singular values do not separate.
- **Leaving $h_0$ in the Hankel matrix.** $H$ starts at $h_1$. A direct feedthrough $D$ that enters $H$ adds a spurious state.
- **A mode that is lightly excited.** A mode that one input barely excites, or that one output barely sees, has a small singular value and can fall below the noise. Add inputs or sensors.
- **Continuous poles from discrete ones.** $s = \ln(z) / h$ is correct only for poles below the Nyquist frequency $\pi / h$; a faster mode is aliased.
- **Large problems.** A full SVD of a large $H$ is expensive. Use a randomized or Lanczos SVD for the leading singular values only.

## Implementations

## History

Ho and Kalman gave the exact realization from the Hankel matrix in 1966. Zeiger and McEwen used the singular value decomposition with Ho's algorithm in 1974, and Kung presented an SVD method for identification and model reduction in 1978. Juang and Pappa, at NASA Langley, combined these ideas with modal accuracy indicators and published ERA in the Journal of Guidance, Control, and Dynamics in 1985. Their aim was the modal survey of large flexible space structures. ERA and its descendants (ERA/DC, OKID) became standard tools of experimental modal analysis.

## References
