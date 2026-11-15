---
tag: 7ZZDNB
kind: algorithm
slug: moesp
name: MOESP
aliases:
- multivariable output-error state space
area: control/modeling-and-identification
level: advanced
summary: Subspace method that gets a state-space model from input-output data by an LQ factorization and an SVD of block Hankel matrices; consistent for white output noise.
solves: [system-identification]
model: real-ram
complexity:
  vars: {N: the number of samples, i: the number of block rows, n: the model order, m: the number of inputs, p: the number of outputs}
  time: {worst: O(N i^2 (m + p)^2 + i^3 p^3 + N n^3 m + N p (n m + p m + n)^2)}
  space: {extra: O(N i (m + p))}
properties: {deterministic: true, online: false, exact: true, iterative: false}
history:
  year: 1992
  people: [Michel Verhaegen, Patrick Dewilde]
  note: "Verhaegen and Dewilde introduced the MOESP class of subspace algorithms in two papers in the International Journal of Control in 1992; Verhaegen added the instrumental variable versions PI-MOESP and PO-MOESP in 1993 and 1994."
prereqs: [subspace-identification, qr-decomposition, singular-value-decomposition]
see_also: [n4sid, eigensystem-realization-algorithm, ho-kalman-algorithm, output-error-model, persistent-excitation, observability, prediction-error-method, least-squares-problem]
sources:
  - paper: doi:10.1080/00207179208934363
    title: "Michel Verhaegen and Patrick Dewilde, Subspace model identification Part 1. The output-error state-space model identification class of algorithms, International Journal of Control 56(5), 1187-1210, 1992"
    locator: the data equation, the LQ factorization of the block Hankel matrices, and the estimate of A and C from the observability matrix
  - paper: doi:10.1080/00207179208934364
    title: "Michel Verhaegen and Patrick Dewilde, Subspace model identification Part 2. Analysis of the elementary output-error state-space model identification algorithm, International Journal of Control 56(5), 1211-1241, 1992"
    locator: the analysis of the algorithm with noise on the output
  - paper: doi:10.1080/00207179308923017
    title: "Michel Verhaegen, Subspace model identification Part 3. Analysis of the ordinary output-error state-space model identification algorithm, International Journal of Control 58(3), 555-586, 1993"
    locator: the analysis of ordinary MOESP and the instrumental variable version with past inputs
  - book: isbn:9780521875127
    title: "Michel Verhaegen and Vincent Verdult, Filtering and System Identification: A Least Squares Approach, Cambridge University Press, 2007"
    locator: the chapter on subspace model identification (MOESP, PI-MOESP and PO-MOESP)
---

MOESP (multivariable output-error state space) is a [subspace identification](/subspace-identification/) method. It takes measured inputs and outputs of a linear system $x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$ and returns $A$, $B$, $C$ and $D$ without an iterative search. It stacks the data in block Hankel matrices, removes the part of the outputs that the future inputs explain with one LQ factorization, and finds the extended observability matrix from an SVD of what is left. The shift structure of that matrix gives $A$ and $C$, and one linear least squares fit gives $B$, $D$ and the initial state. MOESP and [N4SID](/n4sid/) are the two best known members of the subspace family. MOESP estimates the observability matrix and then $B$ and $D$; N4SID estimates a state sequence and then all four matrices in one regression. Basic MOESP is consistent when the noise is white and on the output only; for process noise use its variants PI-MOESP and PO-MOESP, or N4SID.

## In plain words

Write the input and the output records as tables in which each column is a short window of the data, and the next column is the same window one step later. The outputs in a window depend on two things: the state at the start of the window and the inputs inside the window. Remove everything that the inputs inside the window can explain. What is left comes from the start states, so its columns all lie in a space with as many dimensions as the system has states. The SVD finds this space and shows its size. From the space you read how the state shows up in the output, one step after another, and from that the state matrix. A last fit on the data gives the input matrices.

## The problem

**Input.** Samples $u_0, \ldots, u_{N-1} \in \mathbb{R}^m$ and $y_0, \ldots, y_{N-1} \in \mathbb{R}^p$, a number $i$ of block rows with $i > n$, and the order $n$ or a threshold to choose it.

**Output.** $(A, B, C, D)$ of order $n$ and an initial state $x_0$ such that the model output fits the data, and the singular values used to choose $n$.

**Assumptions.** The data come from a system of order $n$ with $(A, C)$ observable. The input is rich enough: the matrix $\begin{pmatrix} X \\ U \end{pmatrix}$ of the state sequence and the input Hankel matrix has full row rank $n + im$. This holds, for example, for a white noise input that is [persistently exciting](/persistent-excitation/) of order $i + n$ and a controllable $(A, B)$. Noise, if any, is white, of equal variance on all outputs, and independent of the input.

**Notation.** $U$ is the $im \times j$ block Hankel matrix with block $(r, c)$ equal to $u_{r+c}$, for $r = 0, \ldots, i-1$ and $c = 0, \ldots, j-1$, with $j = N - i + 1$. $Y$ is the same for $y$. $\Gamma_i$ stacks $C, C A, \ldots, C A^{i-1}$.

## The algorithm

```pseudo id=main
MOESP(u, y, i, n)
L1  U, Y ← the block Hankel matrices of u and y, i block rows, j = N - i + 1 columns
L2  [L11 0; L21 L22] ← the triangular factor of the LQ factorization [U; Y] = L Q
L3  (Ul, σ) ← the left singular vectors and singular values of L22
L4  choose n (a gap in σ, or given), with 1 ≤ n < i
L5  G ← the first n columns of Ul          (G = Γ_i T for some nonsingular T)
L6  C ← the first p rows of G
L7  A ← (G without its last p rows)⁺ · (G without its first p rows)
L8  (x0, B, D) ← the least squares fit of y_k = C A^k x0 + Σ_(t<k) C A^(k-1-t) B u_t + D u_k
L9  return (A, B, C, D, x0, σ)
```

The data equation $Y = \Gamma_i X + \mathcal{T}_i U$ holds, where $X$ is the state sequence and $\mathcal{T}_i$ is the block Toeplitz matrix of the [Markov parameters](/markov-parameters/). L2 computes only the triangular factor $L$, with Householder reflections, and never stores $Q$. Because $U = L_{11} Q_1$ and $Q_1 Q_2^T = 0$, the block $L_{22} = Y Q_2^T$ is the part of $Y$ that is orthogonal to the inputs in the window, and it equals $\Gamma_i X Q_2^T$. So the column space of $L_{22}$ is the column space of $\Gamma_i$. L7 uses the shift structure: $\Gamma_i$ without its last block row, times $A$, is $\Gamma_i$ without its first block row. L8 is linear in $x_0$, $B$ and $D$ once $A$ and $C$ are fixed; the code builds each regressor column by a short simulation.

## Example

Take the second order system

$$A = \begin{pmatrix} 0.7 & 0.4 \\ -0.4 & 0.7 \end{pmatrix}, \quad B = \begin{pmatrix} 1 \\ 0.5 \end{pmatrix}, \quad C = \begin{pmatrix} 1 & 0 \end{pmatrix}, \quad D = 0.2,$$

with poles $0.7 \pm 0.4 i$, the initial state $x_0 = (0.5, -1)$, and a Gaussian white input with unit variance (seed 7), $N = 300$ samples and $i = 4$ block rows. Then $j = 297$, and $[U; Y]$ is $8 \times 297$.

**Noise-free data.** The singular values of the $4 \times 4$ block $L_{22}$ are

$$34.5398, \quad 13.0589, \quad 1.0 \cdot 10^{-14}, \quad 4.7 \cdot 10^{-15}.$$

So $n = 2$. The estimated $A$ is $\begin{pmatrix} 0.6336 & 0.7223 \\ -0.2276 & 0.7664 \end{pmatrix}$, not the true matrix, but similar to it: its eigenvalues are $0.7 \pm 0.4 i$ to 15 digits. The fit gives $D = 0.2$, and the model output with the fitted $x_0$ matches the data to $3 \cdot 10^{-15}$.

**White output noise (measurement).** With $N = 2000$, $i = 6$, zero initial state, and Gaussian output noise with standard deviation $0.1$ (seed 1), the singular values are

$$95.276, \quad 41.754, \quad 4.420, \quad 4.381, \quad 4.376, \quad 4.229.$$

The four small values are almost equal, about $0.1 \sqrt{j} = 4.47$: this is the $\sigma^2 I$ term of the proof. The estimated poles are $0.6995 \pm 0.4008 i$ and $D = 0.2010$. With the seeds 2 and 3 the poles are $0.6999 \pm 0.4005 i$ and $0.6993 \pm 0.4008 i$.

## Correctness

**Claim.** On noise-free data, with $(A, C)$ observable, $i > n$, the excitation condition $\operatorname{rank} \begin{pmatrix} X \\ U \end{pmatrix} = n + im$ and a full rank regressor in L8, MOESP returns $(T^{-1} A T, T^{-1} B, C T, D)$ for a nonsingular $T$. With white output noise of equal variance on all outputs, the estimated column space tends to the column space of $\Gamma_i$ as $N \to \infty$.

**Key invariant.** $L_{22} = \Gamma_i X Q_2^T$, and $X Q_2^T$ has full row rank $n$. With noise, $\frac{1}{j} L_{22} L_{22}^T \to \Gamma_i M \Gamma_i^T + \sigma^2 I$ with $M$ positive definite.

So the first $n$ left singular vectors span the column space of $\Gamma_i$, and $G = \Gamma_i T$. Shift invariance gives $\hat A = T^{-1} A T$ and $\hat C = C T$, and the true $(T^{-1} x_0, T^{-1} B, D)$ is a zero-residual point of the least squares problem of L8. The full proof is below.

## Complexity

In the [real RAM](/real-ram/), counting dense factorizations in the usual way. L2 factors a $d \times j$ matrix with $d = i(m + p)$ by Householder reflections in $O(d^2 j) = O(N i^2 (m + p)^2)$. L3 is an SVD of the $ip \times ip$ block $L_{22}$ in $O(i^3 p^3)$. L7 is a pseudoinverse of an $(i-1)p \times n$ matrix, $O(i p n^2)$. L8 builds $n + nm$ regressor columns by simulations of $N$ steps, in $O(N n^3 m)$ for the code's simple loops, and solves a least squares problem with $Np$ rows and $q = n + nm + pm$ unknowns in $O(N p q^2)$. The extra space is $O(N i (m + p))$ for the Hankel matrices; the LQ factor is only $d \times d$.

For long records, L2 dominates. The SVD and the pseudoinverse are iterative inside, so the counts above are the usual dense counts, as for the other factorizations in this area.

## Properties

- **Exact for noise-free data (theorem).** Under the assumptions above the model has the true transfer function, in other state coordinates.
- **Consistent for white output noise (theorem).** The column space of $\Gamma_i$, and so $A$ and $C$, are consistent when the noise is white, has equal variance on all outputs, and is independent of the input (Verhaegen and Dewilde 1992, Part 2).
- **Biased for process noise.** With noise in the state equation, or colored output noise, basic MOESP is biased. PI-MOESP and PO-MOESP remove the bias with instruments.
- **No local minima.** There is no nonconvex search, so no starting value is needed.
- **Not optimal.** The estimate is not the maximum likelihood estimate, and its variance is larger than that of a [prediction error method](/prediction-error-method/).
- **The order is a choice.** The singular values give a visual aid, not a test. A gap that is clear on noise-free data can be hard to see on real data.

## Variants and improvements

- **PI-MOESP.** Uses the past inputs as instruments. It is consistent for output noise that is colored but independent of the input (Verhaegen 1993, Part 3).
- **PO-MOESP.** Uses the past inputs and the past outputs as instruments. It is consistent for innovation form models with process noise (Verhaegen, Automatica, 1994).
- **[N4SID](/n4sid/).** Uses an oblique projection to get a state sequence and then fits all matrices in one least squares problem. Van Overschee and De Moor (1995) showed that MOESP, N4SID and CVA are the same algorithm with different weightings of the SVD.
- **[ERA](/eigensystem-realization-algorithm/).** The same shift idea applied to a Hankel matrix of Markov parameters, not of raw data.
- **Closed loop.** Basic MOESP is biased in [closed loop](/closed-loop-identification/), because the input depends on past noise. Predictor-based subspace methods address this.
- **Recursive MOESP.** Updates the LQ factor and the subspace as data arrive, for tracking slowly changing systems.

## When to use it

Use MOESP to get a multivariable state-space model from open-loop data in one step, when there is no good starting value for a prediction error method, or as the starting value for one. It handles many inputs and outputs at the same cost as one, and it gives the order from the singular values. With strong process noise, prefer PO-MOESP or N4SID. With feedback in the data, use a closed-loop method.

## Pitfalls

- **Too few block rows.** The method needs $i > n$, and in practice $i$ two or three times the expected order. With $i$ too small, L7 has no unique solution.
- **Too few samples.** The LQ factorization needs $j \ge i(m + p)$, and the estimate is poor long before that limit. The code rejects $j < i(m + p)$.
- **An input that is not rich enough.** A step or a sum of a few sines does not satisfy the excitation condition for large $i$. Then $L_{22}$ contains input effects and the rank is wrong.
- **Unequal noise on the outputs.** The proof needs the same noise variance on every output. Scale the outputs to equal noise levels before L1.
- **Offsets.** A constant offset in the data acts as an extra input. Remove the means first.
- **Comparing matrices.** The estimate is in other coordinates. Compare eigenvalues, Markov parameters or frequency responses, never the entries of $A$.

## Implementations

## History

Subspace identification grew out of realization theory: Ho and Kalman (1966), then the SVD methods of Kung (1978) and of Juang and Pappa (1985) worked on Markov parameters. In 1992, Verhaegen and Dewilde published the MOESP class in two parts in the International Journal of Control. They worked directly on input-output data with an LQ factorization and an SVD. Verhaegen analysed ordinary MOESP and introduced PI-MOESP in Part 3 (1993), and PO-MOESP for models in innovation form in 1994. At the same time Van Overschee and De Moor developed N4SID, and in 1995 they showed that both are special cases of one weighted algorithm.

## References
