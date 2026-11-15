---
tag: JNNGT0
kind: problem
slug: realization-problem
name: Realization problem
aliases:
- state-space realization problem
area: control/state-space-control
level: core
summary: Given a proper rational transfer matrix, find matrices A, B, C and D whose transfer matrix it is.
prereqs: [transfer-function-matrix, markov-parameters, controllable-canonical-form, observable-canonical-form]
see_also: [minimal-realization, ho-kalman-algorithm, eigensystem-realization-algorithm, kalman-decomposition, smith-mcmillan-form, subspace-identification, berlekamp-massey, pade-approximation]
sources:
  - paper: doi:10.1137/0301010
    title: R. E. Kalman, Mathematical description of linear dynamical systems, SIAM Journal on Control 1(2), 152-192, 1963
    locator: the realization problem for transfer matrices and impulse responses, and the role of the controllable and observable part
  - paper: doi:10.1137/0301009
    title: Elmer G. Gilbert, Controllability and observability in multivariable control systems, SIAM Journal on Control 1(2), 128-151, 1963
    locator: the minimal realization of a transfer matrix with simple poles from rank factorizations of its residues
  - paper: doi:10.1524/auto.1966.14.112.545
    title: B. L. Ho and R. E. Kalman, Effective construction of linear state-variable models from input/output functions, Regelungstechnik 14, 545-548, 1966
    locator: the construction of a minimal realization from the Hankel matrix of the Markov parameters
  - paper: doi:10.1109/TAC.1981.1102559
    title: Paul Van Dooren, The generalized eigenstructure problem in linear system theory, IEEE Transactions on Automatic Control 26(1), 111-129, 1981
    locator: staircase reductions with orthogonal transformations, used to remove the uncontrollable and unobservable parts of a realization
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 4.4 (realizations, and the block companion realization of a proper rational matrix), Section 7.5 (realizations from Markov parameters) and Section 7.7 (minimal realizations in the matrix case)
---

The realization problem asks, for a given transfer matrix $G(s)$, for a state-space model $(A, B, C, D)$ with $G(s) = C (sI - A)^{-1} B + D$. A solution exists exactly when $G$ is proper and rational, and then there are many, of many orders. This page is about the problem and its existence answer. The [minimal realization theorem](/minimal-realization/) describes the solutions of least order. The [Ho-Kalman algorithm](/ho-kalman-algorithm/) computes one from exact Markov parameters, and the [eigensystem realization algorithm](/eigensystem-realization-algorithm/) computes an approximate one from noisy data with a truncated SVD.

## In plain words

A transfer function says how a system answers its inputs, but not what goes on inside. A state-space model says both. The realization problem goes from the first description to the second: find a set of internal states and first order equations for them whose input to output behavior is the given one. This is possible exactly when the transfer function is a ratio of polynomials whose numerator degree is not larger than its denominator degree. Many models answer the question. The useful ones have as few states as possible, and all of those are the same model seen in different coordinates.

## Definition

**Input.** A $p \times m$ matrix $G(s)$ whose entries are functions of the complex variable $s$. Equivalently, for rational $G$, the constant term $D$ and the [Markov parameters](/markov-parameters/) $h_1, h_2, \dots$ in $G(s) = D + \sum_{k \ge 1} h_k s^{-k}$.

**Output.** An integer $n$ and real matrices $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $C \in \mathbb{R}^{p \times n}$, $D \in \mathbb{R}^{p \times m}$ with $G(s) = C (sI - A)^{-1} B + D$, or a statement that none exists. In Markov parameter terms the conditions are $C A^{k-1} B = h_k$ for every $k \ge 1$.

**Existence.** A realization exists if and only if $G$ is *proper rational*: each entry is a ratio of real polynomials with the numerator degree at most the denominator degree.

*Necessity.* $(sI - A)^{-1} = \operatorname{adj}(sI - A) / \det(sI - A)$. The entries of the adjugate are polynomials of degree at most $n - 1$, and $\det(sI - A)$ has degree $n$. So each entry of $C (sI - A)^{-1} B$ is rational with a numerator of lower degree than the denominator, and adding the constant $D$ keeps it proper.

*Sufficiency.* Let $d(s) = s^r + \alpha_1 s^{r-1} + \dots + \alpha_r$ be the monic least common denominator of the entries of $G(s) - G(\infty)$. Then $G(s) = D + N(s)/d(s)$ with $D = G(\infty)$ and $N(s) = N_1 s^{r-1} + N_2 s^{r-2} + \dots + N_r$, where each $N_k$ is a real $p \times m$ matrix. The block controllable form

$$A = \begin{bmatrix} 0 & I_m & & \\ & \ddots & \ddots & \\ & & 0 & I_m \\ -\alpha_r I_m & \cdots & -\alpha_2 I_m & -\alpha_1 I_m \end{bmatrix}, \quad B = \begin{bmatrix} 0 \\ \vdots \\ 0 \\ I_m \end{bmatrix}, \quad C = \begin{bmatrix} N_r & N_{r-1} & \cdots & N_1 \end{bmatrix}$$

of order $m r$ is a realization. To check it, solve $(sI - A) X = B$: the block rows give $X = (I_m, s I_m, \dots, s^{r-1} I_m)^T / d(s)$, and $C X = N(s)/d(s)$. The dual block observable form, with $A = \begin{bmatrix} 0 & & & -\alpha_r I_p \\ I_p & \ddots & & \vdots \\ & \ddots & 0 & -\alpha_2 I_p \\ & & I_p & -\alpha_1 I_p \end{bmatrix}$, $B = (N_r; N_{r-1}; \dots; N_1)$ and $C = [0, \dots, 0, I_p]$, has order $p r$. For $m = p = 1$ these are the [controllable canonical form](/controllable-canonical-form/) and the [observable canonical form](/observable-canonical-form/).

**Infinite sequences.** A sequence $h_1, h_2, \dots$ of $p \times m$ matrices is the sequence of Markov parameters of some finite realization if and only if its infinite block Hankel matrix, with blocks $h_{i+j-1}$, has finite rank. That rank is then the minimal order.

## Variants

- **Minimal realization.** Find a realization of least order. The answer is any realization that is controllable and observable, and its order is the McMillan degree of $G$; see [minimal realization](/minimal-realization/).
- **Realization from data.** The Markov parameters are measured, for example as samples of the impulse response of a discrete-time system, and contain noise. The exact problem is then ill posed, and the question becomes which low order model fits best. See the [eigensystem realization algorithm](/eigensystem-realization-algorithm/) and [subspace identification](/subspace-identification/).
- **Partial realization.** Only $h_1, \dots, h_N$ are given. Find a realization of least order whose first $N$ Markov parameters match. For scalar sequences this is the problem of the shortest linear recurrence that generates the sequence, which the [Berlekamp-Massey](/berlekamp-massey/) algorithm solves, and it is close to [Padé approximation](/pade-approximation/) at infinity. When the order is known to be at most $n$, the $2n$ parameters $h_1, \dots, h_{2n}$ fix the transfer matrix.
- **Discrete time.** For $x_{k+1} = A x_k + B u_k$ the problem is the same with $z$ in place of $s$, and the Markov parameters are the impulse response $h_k = C A^{k-1} B$.
- **Structured realizations.** Some applications ask for more, for example matrices with nonnegative entries for positive systems. Such problems are harder, and for positive systems the least order can exceed the McMillan degree.

## Examples

- **A scalar function.** $G(s) = (s + 3)/(s^2 + 3 s + 2)$ has the realization $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $B = (0, 1)^T$, $C = [3, 1]$, $D = 0$. It is minimal, because $s + 3$ and $s^2 + 3 s + 2$ have no common root.
- **A row of two functions.** $G(s) = [1/(s + 1), 1/(s + 2)]$, with $p = 1$ and $m = 2$. Here $d(s) = s^2 + 3 s + 2$ and $N(s) = [s + 2, s + 1] = [1, 1] s + [2, 1]$, so $N_1 = [1, 1]$ and $N_2 = [2, 1]$. The block controllable form has order $m r = 4$: $A = \begin{bmatrix} 0 & I_2 \\ -2 I_2 & -3 I_2 \end{bmatrix}$, $B = (0; I_2)$, $C = [2, 1, 1, 1]$. The block observable form has order $p r = 2$: $A = \begin{bmatrix} 0 & -2 \\ 1 & -3 \end{bmatrix}$, $B = \begin{bmatrix} 2 & 1 \\ 1 & 1 \end{bmatrix}$, $C = [0, 1]$. To check the second one, $C (sI - A)^{-1} = [1, s] / d(s)$ and $[1, s] B = [s + 2, s + 1]$. The residues at $-1$ and $-2$ are $[1, 0]$ and $[0, 1]$, each of rank 1, so the McMillan degree is 2, and the order 2 realization is minimal. The order 4 realization is controllable but not observable.
- **From Markov parameters.** $1/((s + 1)(s + 2)) = s^{-2} - 3 s^{-3} + 7 s^{-4} - 15 s^{-5} + \dots$, so $h_1, h_2, h_3, \dots = 0, 1, -3, 7, -15, \dots$. The Hankel matrix $\begin{bmatrix} 0 & 1 \\ 1 & -3 \end{bmatrix}$ has rank 2, and the $3 \times 3$ one has determinant $0$, in agreement with the minimal order 2.
- **Improper (non-example).** $G(s) = s$, the transfer function of a differentiator, has no realization: $C (sI - A)^{-1} B + D$ tends to $D$ as $s \to \infty$, while $s$ does not stay bounded.
- **Not rational (non-example).** $G(s) = e^{-s}$, a pure delay of one second, has no finite-dimensional realization, since every $C (sI - A)^{-1} B + D$ is rational. Rational approximations of the delay, such as [Padé approximants](/pade-approximation/), do have realizations.

## Known algorithms

- **Block companion forms.** Write $G = D + N(s)/d(s)$ and read off the block controllable form (order $m r$) or the block observable form (order $p r$). Choose the smaller one. The result need not be minimal.
- **Reduction to a minimal realization.** Remove the uncontrollable and then the unobservable part by the [Kalman decomposition](/kalman-decomposition/). With staircase reductions by orthogonal transformations (Van Dooren 1981) this is numerically stable, and it costs of the order of $n^3$ operations for a realization of order $n$ when $m$ and $p$ are at most $n$. The rank decisions need a tolerance.
- **Gilbert's method.** If $G(s) = D + \sum_{i=1}^{q} R_i / (s - p_i)$ with distinct poles, factor each residue as $R_i = U_i V_i$ with $\rho_i = \operatorname{rank} R_i$ columns in $U_i$. Then $A = \operatorname{diag}(p_1 I_{\rho_1}, \dots, p_q I_{\rho_q})$, $B = (V_1; \dots; V_q)$ and $C = [U_1, \dots, U_q]$ give a minimal realization of order $\sum_i \rho_i$ (Gilbert 1963). Complex conjugate poles give complex blocks, which a further change of coordinates turns into real $2 \times 2$ blocks.
- **Hankel factorization.** Build the block Hankel matrix of the Markov parameters, factor it as $\mathcal{O} \mathcal{C}$ by a rank factorization, and read $C$, $B$ and $A$ from the factors and the shifted Hankel matrix. This is the [Ho-Kalman algorithm](/ho-kalman-algorithm/) for exact data. With a truncated [singular value decomposition](/singular-value-decomposition/) in place of an exact factorization it becomes the [eigensystem realization algorithm](/eigensystem-realization-algorithm/) for noisy data.
- **Coprime fractions.** Write $G = N(s) D(s)^{-1}$ with right coprime polynomial matrices and $D(s)$ column reduced. A realization built from the column degrees of $D(s)$ has order $\deg \det D(s)$, which is the McMillan degree.

## Bounds

- **Lower bound.** Every realization has order at least the McMillan degree $\delta(G)$, and $\delta(G) = \operatorname{rank} H_N$ for $N$ large enough.
- **Upper bound from the forms.** $\delta(G) \le \min(m r, p r)$, where $r$ is the degree of the least common denominator, by the two block companion forms. For a scalar $G$ in lowest terms, $\delta(G) = r$.
- **Data needed.** If $\delta(G) \le n$ is known, the $2n$ Markov parameters $h_1, \dots, h_{2n}$ determine $G$, and the Hankel matrices $H_n$ and the shifted $H_n^{\sigma}$ built from them are enough to compute a minimal realization.
- **Cost.** A block companion form needs only the coefficients of $d(s)$ and $N(s)$, which come from a [polynomial gcd](/polynomial-gcd/) computation and polynomial products, and its matrices have $O((m r)^2 + p m r)$ entries. Reducing it to a minimal realization costs $O(n^3)$ more operations in the [real-RAM](/real-ram/) model, with $n = \min(m r, p r)$.

## Reductions

- **To Markov parameters.** For rational $G$, the Laurent expansion at $s = \infty$ turns the problem into one about the sequence $D, h_1, h_2, \dots$, and the Hankel rank condition decides it.
- **To controllability and observability.** Any realization, however obtained, reduces to a minimal one by removing the parts that are not controllable or not observable, so the minimal problem reduces to the existence problem plus the [Kalman decomposition](/kalman-decomposition/).
- **By transposition.** $(A, B, C, D)$ realizes $G$ if and only if $(A^T, C^T, B^T, D^T)$ realizes $G^T$. So a method for the case $m \le p$ also solves the case $m > p$.
- **To linear recurrences.** The scalar partial realization problem is the problem of the shortest linear recurrence for a finite sequence, the same problem that a [linear feedback shift register](/linear-feedback-shift-register/) synthesis algorithm solves over a finite field.

## Applications

- Simulation: an ordinary differential equation solver needs a state model, not a transfer function.
- Design: the state-space methods, such as the [LQR](/lqr-problem/), [pole placement](/pole-placement-theorem/) and the [Kalman filter](/kalman-filter/), start from $(A, B, C, D)$, while plant data often come as transfer functions or frequency responses.
- Implementation: a controller designed as a transfer matrix is run on a computer as a state recursion, and a minimal realization keeps the number of stored states small.
- Identification and model reduction: measured impulse responses are turned into state models by the Hankel based methods, and [balanced truncation](/balanced-truncation/) reduces them further.

## References
