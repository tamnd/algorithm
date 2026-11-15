---
tag: 0NXMFM
kind: algorithm
slug: n4sid
name: N4SID
aliases:
- numerical algorithms for subspace state space system identification
area: control/modeling-and-identification
level: advanced
summary: Subspace method that estimates a state sequence from input-output data by oblique projections and an SVD, then fits A, B, C, D and the noise covariances by least squares.
solves: [system-identification]
model: real-ram
complexity:
  vars: {N: the number of samples, i: the number of block rows in the past and in the future, n: the model order, m: the number of inputs, p: the number of outputs}
  time: {worst: O(N i^2 (m + p)^2 + i^3 (m + p)^3)}
  space: {extra: O(N i (m + p))}
properties: {deterministic: true, online: false, exact: true, iterative: false}
history:
  year: 1994
  people: [Peter Van Overschee, Bart De Moor]
  note: "Van Overschee and De Moor published N4SID in Automatica in 1994; their 1995 paper and 1996 book showed that N4SID, MOESP and CVA are one algorithm with different weightings."
prereqs: [subspace-identification, qr-decomposition, singular-value-decomposition]
see_also: [moesp, eigensystem-realization-algorithm, kalman-filter, persistent-excitation, prediction-error-method, least-squares-problem, pseudoinverse, closed-loop-identification]
sources:
  - paper: doi:10.1016/0005-1098(94)90230-5
    title: "Peter Van Overschee and Bart De Moor, N4SID: Subspace algorithms for the identification of combined deterministic-stochastic systems, Automatica 30(1), 75-93, 1994"
    locator: the oblique projection, the Kalman filter interpretation of the state sequences, and the algorithms that use them
  - book: doi:10.1007/978-1-4613-0465-4
    title: "Peter Van Overschee and Bart De Moor, Subspace Identification for Linear Systems: Theory, Implementation, Applications, Kluwer Academic Publishers, 1996 (ISBN 978-1-4613-8061-0)"
    locator: "Chapter 4 (Combined Deterministic-Stochastic Identification), pp. 95-134"
  - paper: doi:10.1016/0005-1098(95)00072-0
    title: "Peter Van Overschee and Bart De Moor, A unifying theorem for three subspace system identification algorithms, Automatica 31(12), 1853-1864, 1995"
    locator: N4SID, MOESP and CVA as weighted versions of one algorithm
  - paper: doi:10.1109/cdc.1990.203665
    title: "Wallace E. Larimore, Canonical variate analysis in identification, filtering, and adaptive control, Proceedings of the 29th IEEE Conference on Decision and Control, 596-604, 1990"
    locator: the canonical variate analysis (CVA) weighting
---

N4SID (numerical algorithms for subspace state space system identification) is a [subspace identification](/subspace-identification/) method. From measured inputs and outputs it estimates a model in innovation form, $x_{k+1} = A x_k + B u_k + K e_k$, $y_k = C x_k + D u_k + e_k$, without iterative search. Its main step is an oblique projection of the future outputs onto the past data, along the future inputs. The result is the extended observability matrix times a sequence of states, and an SVD splits the two factors. With two such state sequences, one step apart, all of $A$, $B$, $C$ and $D$ follow from one linear least squares problem, and its residuals give the noise covariances. [MOESP](/moesp/) is the other well known member of the family: it gets $A$ and $C$ from the observability matrix and fits $B$ and $D$ afterwards, while N4SID fits all four matrices together from estimated states.

## In plain words

Cut the data into a past window and a future window. The future outputs depend on the state at the start of the future window and on the future inputs. That state depends only on the past. So remove from the future outputs the part that the future inputs explain, and keep only the part that the past explains. What is left is the state at the start of the future, seen through the output. Its size shows how many states the system has, and the SVD splits it into "how the state shows in the output" and "the states". Do the same one step later. Now you have the states at two times and the inputs and outputs between them, so one ordinary least squares fit gives the four system matrices. What the fit cannot explain is the noise.

## The problem

**Input.** Samples $u_0, \ldots, u_{N-1} \in \mathbb{R}^m$ and $y_0, \ldots, y_{N-1} \in \mathbb{R}^p$, a number $i > n$ of block rows for the past and for the future, and the order $n$ or a threshold to choose it.

**Output.** $(A, B, C, D)$ of order $n$, the covariance of the residuals $\begin{pmatrix} Q & S \\ S^T & R \end{pmatrix}$, and the singular values used to choose $n$.

**Notation.** $U$ is the $2im \times j$ block Hankel matrix of the inputs with $2i$ block rows and $j = N - 2i + 1$ columns, block $(r, c)$ equal to $u_{r+c}$. The first $i$ block rows are the past $U_p$, the last $i$ are the future $U_f$. $U_p^+$ and $U_f^-$ move the border one block row down. $Y$ is the same for the outputs, and $W_p = \begin{pmatrix} U_p \\ Y_p \end{pmatrix}$. The oblique projection of the rows of $a$ along the row space of $b$ onto the row space of $c$ is $a /_b c = (a / b^\perp)(c / b^\perp)^{+} c$, where $a / b^\perp$ subtracts from each row of $a$ its orthogonal projection on the row space of $b$, and $^{+}$ is the [pseudoinverse](/pseudoinverse/).

## The algorithm

```pseudo id=main
N4SID(u, y, i, n)
L1  U, Y ← the block Hankel matrices with 2i block rows and j = N - 2i + 1 columns
L2  L ← the lower triangular factor of the LQ factorization [U; Y] = L Q
L3  O_i ← Y_f /_(U_f) W_p
L4  O_(i-1) ← Y_f^- /_(U_f^-) W_p^+
L5  (Us, σ) ← the SVD of O_i;  choose n (a gap in σ, or given), with 1 ≤ n < i
L6  G ← Us[:, 1:n] diag(σ_1, ..., σ_n)^(1/2);  G1 ← G without its last p rows
L7  X_i ← G⁺ O_i;  X_(i+1) ← G1⁺ O_(i-1)
L8  θ ← the least squares solution of [X_(i+1); Y_(i|i)] = θ [X_i; U_(i|i)]
L9  (A, B; C, D) ← the blocks of θ;  cov ← the residuals times their transpose, over j
L10 return (A, B, C, D, cov, σ)
```

$Y_{i|i}$ and $U_{i|i}$ are the block row $i$ of $Y$ and $U$, the first block row of the future. Every data row is the matching row of $L$ times $Q$, and $Q$ has orthonormal rows. So every inner product of data rows is the same inner product of rows of $L$, and L3 to L9 run on rows of length $2i(m + p)$ instead of $j$. The code never forms $Q$. L3 is the heart of the method: the future outputs are $Y_f = \Gamma_i X_f + \mathcal{T}_i U_f$, the state $X_f$ is a linear function of the past $W_p$, and the oblique projection keeps exactly the part along $W_p$, which is $\Gamma_i X_f$. L4 does the same with the border one block row later, so it gives $\Gamma_{i-1} X_{f}^+$, the next states. L6 chooses the balanced split $U_n \Sigma_n^{1/2}$ of the SVD; any other split gives the same model in other coordinates.

## Example

Take the second order system

$$A = \begin{pmatrix} 0.7 & 0.4 \\ -0.4 & 0.7 \end{pmatrix}, \quad B = \begin{pmatrix} 1 \\ 0.5 \end{pmatrix}, \quad C = \begin{pmatrix} 1 & 0 \end{pmatrix}, \quad D = 0.2,$$

with poles $0.7 \pm 0.4 i$ and initial state $(0.5, -1)$, driven by a Gaussian white input with unit variance (seed 7), with $N = 300$ and $i = 4$. Then $j = 293$, $[U; Y]$ is $16 \times 293$, and $O_i$ is $4 \times 16$ when computed on the rows of $L$.

**Noise-free data.** The singular values of $O_i$ are $34.9463$, $13.1263$, and then values below $3 \cdot 10^{-15}$. So $n = 2$. The estimated $A$ has the eigenvalues $0.7 \pm 0.4 i$, $D = 0.2$, and the residual covariance is below $10^{-20}$, as the proof predicts.

**Innovation noise (measurement).** Add process and output noise in innovation form with $K = (0.5, 0.2)^T$ and $e_k$ Gaussian with standard deviation $0.1$, and use $N = 2000$ and $i = 5$ (seed 1). The singular values are $93.7135$, $40.0487$, $0.3262$, and smaller. The gap is a factor of 120. The estimated poles are $0.69994 \pm 0.40146 i$, and the output block of the residual covariance is $R = 0.009697$, against the true noise variance $0.01$.

## Correctness

**Claim.** On noise-free data, with $(A, B)$ controllable, $(A, C)$ observable, $i > n$, and the excitation condition $\operatorname{rank} \begin{pmatrix} X_p \\ U_p \\ U_f \end{pmatrix} = n + 2im$, N4SID returns $(T^{-1} A T, T^{-1} B, C T, D)$ for a nonsingular $T$, and a zero residual covariance.

**Key invariant.** $O_i = \Gamma_i X_f$ and $O_{i-1} = \Gamma_{i-1} X_f^+$. This follows from one identity of the oblique projection: if $a = M c + P b$ and the row spaces of $b$ and $c$ meet only in 0, then $a /_b c = M c$.

The SVD then gives $G = \Gamma_i T$, so L7 returns $T^{-1} X_f$ and $T^{-1} X_f^+$. The state equations hold exactly between these two sequences, and the regressor has full row rank, so L8 returns the stated $\theta$. The full proof is below, including the reason why the computation on the rows of $L$ is the same as on the data.

## Complexity

In the [real RAM](/real-ram/), counting dense factorizations in the usual way. Let $d = 2i(m + p)$. L1 builds $O(N d)$ numbers. L2 is a Householder LQ factorization of the $d \times j$ matrix, $O(d^2 j) = O(N i^2 (m + p)^2)$. L3 and L4 work on rows of length $d$: each projection forms Gram matrices and pseudoinverses of at most $d \times d$ matrices, $O(d^3)$. L5 is an SVD of an $ip \times d$ matrix, $O(i^2 p^2 d)$. L7 to L9 cost $O(d (n + m + p)^2 + n^3)$. The total is $O(N i^2 (m + p)^2 + i^3 (m + p)^3)$, and for long records the LQ factorization dominates. The extra space is $O(N i (m + p))$ for the Hankel matrices; everything after L2 is of size $O(d^2)$.

## Properties

- **Exact for noise-free data (theorem).** Under the assumptions of the claim, the model has the true transfer function.
- **Kalman filter states (theorem).** With innovation noise, as $j \to \infty$, $O_i$ tends to $\Gamma_i \tilde X_i$, where $\tilde X_i$ is the state sequence of a bank of non-steady-state [Kalman filters](/kalman-filter/) started from the past data (Van Overschee and De Moor 1994). This is why N4SID handles process noise, unlike basic MOESP.
- **A bias of this version (theorem, cited).** The two state sequences of L7 come from Kalman filters with different initial conditions. Van Overschee and De Moor (1996, Chapter 4) show that this simple version is asymptotically biased unless the data are noise-free or the input is white noise, and give modified algorithms without this bias. The test of the code uses a white input.
- **Noise model.** The residuals of L8 estimate $Q$, $S$ and $R$, from which a steady-state Kalman gain follows by a Riccati equation.
- **No local minima.** There is no nonconvex search.
- **Not efficient.** The variance is larger than that of a [prediction error method](/prediction-error-method/), which is often started from the N4SID estimate.

## Variants and improvements

- **Weightings.** Multiply $O_i$ by weights before the SVD. Van Overschee and De Moor (1995) showed that N4SID, MOESP and CVA (Larimore 1990) differ only in these weights. The weights change the basis of the state and the finite-sample results, but not the limit.
- **The unbiased and robust combined algorithms.** The 1996 book gives versions that remove the bias of the simple version for general inputs; the robust one is the version used most in practice.
- **Closed-loop subspace methods.** The future inputs depend on past noise in [closed loop](/closed-loop-identification/), and the oblique projection is then biased. Predictor-based methods (SSARX, PBSID) avoid this.
- **[MOESP](/moesp/).** Uses an orthogonal projection and the observability matrix instead of the state sequence.
- **Deterministic and stochastic special cases.** Without inputs, the same projections give a stochastic realization of a time series; without noise, the method is an exact realization from input-output data.

## When to use it

Use N4SID to get a multivariable model with a noise model from open-loop data, with no starting value, and as the starting point of a prediction error fit. It gives the order from the singular values and handles many inputs and outputs. Do not use it as the final model when the best accuracy matters, or directly on closed-loop data.

## Pitfalls

- **Too few block rows.** The method needs $i > n$. With noise, $i$ must also be large enough for the Kalman filter states to be good, often several times the expected order.
- **Too few samples.** The LQ factorization needs $j \ge 2i(m + p)$, and the code rejects smaller $j$. Accuracy needs much more.
- **An input that is not rich enough.** The excitation condition needs the input to be [persistently exciting](/persistent-excitation/) of order about $2i$. A step or a few sines do not satisfy it.
- **Comparing matrices.** The result is in other coordinates. Compare poles, Markov parameters or frequency responses.
- **The order from a weak gap.** With colored noise and many block rows, the singular values decrease slowly. Check several orders by validation on fresh data.
- **Pseudoinverse thresholds.** In floating point, the projections need thresholds in the pseudoinverses. A threshold that is too small makes the projection amplify noise; the code uses $10^{-10}$ times the largest singular value.

## Implementations

## History

Akaike's work on canonical correlations in the 1970s and Larimore's canonical variate analysis of 1990 used projections of the future on the past for time series and for systems with inputs. Van Overschee and De Moor gave the oblique projection, the Kalman filter interpretation of the states, and the N4SID algorithms in Automatica in 1994. In 1995 they proved a unifying theorem that places N4SID, MOESP and CVA in one framework, and their 1996 book became the standard reference on subspace identification.

## References
