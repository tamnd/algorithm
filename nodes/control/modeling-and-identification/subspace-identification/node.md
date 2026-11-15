---
tag: 6HHT7D
kind: technique
slug: subspace-identification
name: Subspace identification
aliases:
- subspace state-space system identification
area: control/modeling-and-identification
level: advanced
summary: Identifies a state-space model from input-output data by projections of block Hankel matrices and an SVD, with no nonlinear optimization.
prereqs: [system-identification, state-space-representation, singular-value-decomposition, qr-decomposition]
see_also: [moesp, n4sid, eigensystem-realization-algorithm, ho-kalman-algorithm, prediction-error-method, canonical-correlation-analysis, closed-loop-identification, persistent-excitation]
sources:
  - book: doi:10.1007/978-1-4613-0465-4
    title: "Peter Van Overschee and Bart De Moor, Subspace Identification for Linear Systems: Theory, Implementation, Applications, Kluwer Academic Publishers, 1996 (ISBN 978-1-4613-8061-0)"
    locator: "Chapter 4 (Combined Deterministic-Stochastic Identification), pp. 95-134"
  - paper: doi:10.1016/0005-1098(95)00072-0
    title: "Peter Van Overschee and Bart De Moor, A unifying theorem for three subspace system identification algorithms, Automatica 31(12), 1853-1864, 1995"
    locator: N4SID, MOESP and CVA as one algorithm with different weighting matrices before the SVD
  - paper: doi:10.1080/00207179208934363
    title: "Michel Verhaegen and Patrick Dewilde, Subspace model identification Part 1. The output-error state-space model identification class of algorithms, International Journal of Control 56(5), 1187-1210, 1992"
    locator: the data equation and the MOESP class of algorithms
  - paper: doi:10.1109/cdc.1990.203665
    title: "Wallace E. Larimore, Canonical variate analysis in identification, filtering, and adaptive control, Proceedings of the 29th IEEE Conference on Decision and Control, 596-604, 1990"
    locator: the canonical variate analysis (CVA) method
  - book: isbn:9780521875127
    title: "Michel Verhaegen and Vincent Verdult, Filtering and System Identification: A Least Squares Approach, Cambridge University Press, 2007"
    locator: the chapter on subspace model identification
---

Subspace identification is a family of methods that compute a linear state-space model $x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$ (with noise) directly from measured inputs and outputs. They stack the data in block Hankel matrices, remove the effect of the future inputs by a projection, and use an SVD to find the order $n$ and either the extended observability matrix or a sequence of states. Then $A$, $B$, $C$ and $D$ follow from linear least squares. There is no iterative search, no starting value and no local minimum, and many inputs and outputs cost little more than one. The best known members are [MOESP](/moesp/), [N4SID](/n4sid/) and CVA (canonical variate analysis). They differ in the projection and in the weights before the SVD. The [Ho-Kalman algorithm](/ho-kalman-algorithm/) and the [eigensystem realization algorithm](/eigensystem-realization-algorithm/) use the same SVD and shift ideas, but on [Markov parameters](/markov-parameters/), not on raw input-output data.

## In plain words

The state of a linear system is the memory that connects the past to the future. Everything the past inputs and outputs can tell about the future outputs passes through the $n$ numbers of the state. So arrange the data into windows of past and future, take away the part of the future outputs that the future inputs cause, and look at what is left. It is a linear function of the past, but only $n$ directions of it matter. The SVD finds these directions, and so the order and a state in some coordinates. With the state known, the state equations are linear in $A$, $B$, $C$ and $D$, and least squares gives them.

## When it applies

- You have data from a linear time-invariant system, or a system near an operating point, with several inputs and outputs, and you want a state-space model.
- You do not know the order, or you want the data to suggest it.
- You have no good starting value for a [prediction error method](/prediction-error-method/), or you want one.
- The data are from an open loop experiment, and the input is [persistently exciting](/persistent-excitation/) of a high enough order. For closed loop data, use a variant made for it.
- The record is long compared with the number of block rows times the number of signals.

## The template

1. **Stack the data.** Choose $i > n$, often two or three times the expected order. Build block Hankel matrices with $i$ block rows of past inputs $U_p$, past outputs $Y_p$, future inputs $U_f$ and future outputs $Y_f$. Column $c$ of $Y_f$ is $(y_{i+c}, \ldots, y_{2i-1+c})$. Write $W_p$ for $U_p$ and $Y_p$ stacked.
2. **Project.** Remove the effect of $U_f$ from $Y_f$. MOESP projects $Y_f$ onto the orthogonal complement of the row space of $U_f$. N4SID projects $Y_f$ along the row space of $U_f$ onto the row space of $W_p$ (an oblique projection). Compute it on the triangular factor of one LQ factorization of all the data.
3. **Weight and decompose.** Compute the SVD $W_1 O W_2 = U S V^T$ of the projected matrix $O$ with weights $W_1$ and $W_2$. Choose $n$ from a gap in the singular values.
4. **Read the subspace.** $\Gamma = W_1^{-1} U_n S_n^{1/2}$ is the extended observability matrix in some coordinates. For N4SID, $S_n^{1/2} V_n^T W_2^{+}$ is a state sequence in the same coordinates.
5. **Fit the matrices.** Get $A$ and $C$ from the shift structure of $\Gamma$, then $B$, $D$ and the initial state by linear least squares (MOESP). Or regress the next states and the outputs on the states and the inputs to get all four matrices at once (N4SID).
6. **Noise model.** The residuals of step 5 estimate the noise covariances. A Riccati equation gives the Kalman gain of an innovation form model.

Steps 1 to 5 as a procedure:

```pseudo id=main
SUBSPACE-ID(u, y, i, W1, W2)
L1  U_p, Y_p, U_f, Y_f ← the block Hankel matrices with i block rows each
L2  O ← the part of Y_f that U_f does not explain (orthogonal or oblique projection)
L3  (U, S, V) ← the SVD of W1 · O · W2
L4  n ← the number of singular values above the gap
L5  Γ ← W1⁻¹ · (the first n columns of U) · S_n^(1/2)
L6  (A, C) ← from the shift structure of Γ, or (A, B, C, D) from a state regression
L7  (B, D) ← by linear least squares, if not found in L6
L8  return (A, B, C, D, n, S)
```

**Why it works.** Iterating the state equations gives the data equation

$$Y_f = \Gamma_i X_f + \mathcal{T}_i U_f + (\text{noise terms}),$$

where $\Gamma_i$ stacks $C, C A, \ldots, C A^{i-1}$, $X_f = (x_i, x_{i+1}, \ldots)$ is the state sequence, and $\mathcal{T}_i$ is the block Toeplitz matrix of the Markov parameters. After the projection of L2, the term $\mathcal{T}_i U_f$ is gone. For noise-free data, what is left is $\Gamma_i$ times a matrix of full row rank $n$, so its column space is that of $\Gamma_i$ and its rank is $n$. The weights in L3 are nonsingular, so they do not change the rank. With $\Gamma = \Gamma_i T$ for a nonsingular $T$, $\Gamma$ without its first block row equals $\Gamma$ without its last block row times $T^{-1} A T$, and that gives $A$ up to similarity. With noise, the past data act as instruments: the future noise is uncorrelated with the past, so the projection on the past keeps the state part and averages the noise out as the record grows. The proofs on the [MOESP](/moesp/) and [N4SID](/n4sid/) pages give the details for each method.

Van Overschee and De Moor (1995) showed that N4SID, MOESP and CVA are this one template with different weights. N4SID uses no weights. MOESP weights on the right with the projection onto the orthogonal complement of the future inputs. CVA also weights on the left with the inverse square root of the covariance of the future outputs, after the future inputs are removed, so that its singular values are canonical correlations, as in [canonical correlation analysis](/canonical-correlation-analysis/).

**Cost.** With $N$ samples, $i$ block rows, $m$ inputs and $p$ outputs, the LQ factorization of the stacked data costs $O(N i^2 (m + p)^2)$ and dominates for long records. The SVD costs $O(i^3 (m + p)^3)$ or less, and the least squares fits are small. The memory is $O(N i (m + p))$ for the Hankel matrices, and less if the triangular factor is accumulated block by block.

## Classic examples

**A second order system, noise-free.** Take $A = \begin{pmatrix} 0.7 & 0.4 \\ -0.4 & 0.7 \end{pmatrix}$, $B = (1, 0.5)^T$, $C = (1, 0)$, $D = 0.2$, a Gaussian white input with unit variance, $N = 300$ samples and $i = 4$. MOESP finds the singular values $34.5398$, $13.0589$, $1.0 \cdot 10^{-14}$ and $4.7 \cdot 10^{-15}$, and N4SID finds $34.9463$, $13.1263$ and values below $3 \cdot 10^{-15}$. Both show $n = 2$, and both return a matrix $A$ with the eigenvalues $0.7 \pm 0.4 i$. The two matrices $A$ are different, because each method uses its own state coordinates.

**The same system with noise (measurement).** With white output noise of standard deviation $0.1$, $N = 2000$ and $i = 6$, MOESP gives the poles $0.6995 \pm 0.4008 i$. With process and output noise in innovation form, $N = 2000$ and $i = 5$, N4SID gives $0.69994 \pm 0.40146 i$ and estimates the output noise variance as $0.009697$ against the true $0.01$. The details are on the method pages.

**Impulse response data.** If the input is a unit pulse and the system starts at rest, the outputs are the Markov parameters, and the block Hankel matrix of the outputs is the matrix that the [Ho-Kalman algorithm](/ho-kalman-algorithm/) factors. Subspace identification with general inputs extends this idea to any persistently exciting input.

## Variations

- **[MOESP](/moesp/).** Orthogonal projection, the observability matrix, then $B$ and $D$ by least squares. Consistent for white output noise. PI-MOESP and PO-MOESP add past inputs or past outputs as instruments for colored noise and process noise.
- **[N4SID](/n4sid/).** Oblique projection on the past, a state sequence, then one regression for all matrices and the noise covariances.
- **CVA.** Larimore's canonical variate analysis, with weights that give canonical correlations between past and future. Its states have a statistical meaning as the canonical variates of the past.
- **Closed loop methods.** Basic methods are biased with feedback, because the future inputs depend on past noise. Predictor-based methods estimate a high order ARX model first and use its Markov parameters; see [closed-loop identification](/closed-loop-identification/).
- **Stochastic subspace identification.** For output-only data, such as vibrations of a structure under unknown excitation, the same template on the outputs gives the modes and the noise model.
- **Frequency-domain subspace methods.** Use samples of the frequency response in place of time data.
- **Recursive subspace methods.** Update the subspace as new data arrive, for slowly changing systems.

## Pitfalls

- **The choice of i.** Too few block rows give a biased subspace and no rank gap; too many give large matrices and more variance. Try two or three values.
- **The order from the singular values.** On real data the gap is often not clear. Compare models of several orders on validation data.
- **Not the most accurate estimate.** Subspace estimates are not maximum likelihood estimates. Use them as starting values for a prediction error method when accuracy matters.
- **Offsets and scaling.** Remove the means of all signals. Scale the inputs and outputs to similar sizes, because the SVD depends on the scaling.
- **Feedback.** Data from a closed loop violate the assumption that the future inputs are uncorrelated with the past noise. The result can be badly biased.
- **Comparing matrices.** Each method returns the model in its own coordinates. Compare poles, Markov parameters or frequency responses, not the entries of $A$.
- **Too short a record.** The LQ factorization needs more columns than rows, and the noise averages out only slowly. A rule of thumb is a number of columns many times $i(m + p)$.

## Exercises

1. Derive the data equation $Y_f = \Gamma_i X_f + \mathcal{T}_i U_f$ for noise-free data from the state equations.
2. Show that if $(A, C)$ is observable and $i \ge n$, then $\Gamma_i$ has full column rank, and the column space of $\Gamma_i X$ is that of $\Gamma_i$ for every $X$ of full row rank $n$.
3. Show that $\Gamma_i$ without its first block row equals $\Gamma_{i-1} A$, and use this to compute $A$ from $\Gamma_i T$ for an unknown nonsingular $T$.
4. Show that the models $(A, B, C, D)$ and $(T^{-1} A T, T^{-1} B, C T, D)$ have the same Markov parameters and the same transfer function.
5. A single sine wave is used as input. Explain why the excitation condition of MOESP fails when $i$ is large, and what happens to the singular values.

## References
