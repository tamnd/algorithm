---
tag: 66MNEX
kind: definition
slug: transfer-function-matrix
name: Transfer function matrix
aliases:
- MIMO transfer function
- transfer matrix of a multivariable system
area: control/modeling-and-identification
level: core
summary: The p by m matrix G(s) = C(sI - A)^(-1)B + D whose entry (i, j) is the transfer function from input j to output i of a linear time-invariant system with m inputs and p outputs.
prereqs: [transfer-function, state-space-representation]
see_also: [transmission-zero, smith-mcmillan-form, minimal-realization, realization-problem, markov-parameters, relative-gain-array, h-infinity-norm, block-diagram-reduction]
sources:
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, second edition, Wiley, 2005
    locator: Chapter 3, Introduction to Multivariable Control (transfer matrices, feedback rules and singular values), and Chapter 4, Elements of Linear System Theory (Sections 4.4 and 4.5, poles and zeros)
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 3, Linear Dynamical Systems (state-space realizations of transfer matrices, and Section 3.11, Multivariable System Poles and Zeros)
  - book: isbn:0135369614
    title: Thomas Kailath, Linear Systems, Prentice Hall, 1980
    locator: Chapter 6, State-Space and Matrix-Fraction Descriptions of Multivariable Systems
---

A transfer function matrix describes a linear time-invariant system with several inputs and several outputs. It is a matrix $G(s)$ of [transfer functions](/transfer-function/): the entry in row $i$ and column $j$ is the transfer function from input $j$ to output $i$ when all other inputs are zero. Because the system is linear, the Laplace transforms of the outputs are $Y(s) = G(s)\, U(s)$ for a system at rest. For a [state-space representation](/state-space-representation/) $x' = Ax + Bu$, $y = Cx + Du$, the matrix is $G(s) = C(sI - A)^{-1}B + D$. Many ideas of the scalar case carry over, but poles and zeros need a new definition, because the zeros of the matrix are not the zeros of its entries.

## Definition

**Notation.** The system has $m$ inputs, $p$ outputs and $n$ states. $\mathbb{R}(s)$ is the field of rational functions with real coefficients, and $\mathbb{R}(s)^{p \times m}$ the set of $p \times m$ matrices over it.

**Definition.** The transfer function matrix of a linear time-invariant system at rest is the $G \in \mathbb{R}(s)^{p \times m}$ (or, with delays, a matrix of more general functions of $s$) with

$$Y(s) = G(s)\, U(s)$$

for every input $u$ whose transform exists. Its entry $G_{ij}(s)$ is the transfer function from $u_j$ to $y_i$. Equivalently, $G$ is the Laplace transform of the matrix impulse response $g(t)$, whose column $j$ is the output for the input $\delta(t)\, e_j$.

$G$ is *proper* if every entry is proper, so that $G(\infty) = \lim_{s \to \infty} G(s)$ exists, and *strictly proper* if $G(\infty) = 0$.

**From a state-space model.** Transform $x' = Ax + Bu$ with $x(0^-) = 0$ to get $sX = AX + BU$, so $X = (sI - A)^{-1}BU$ and

$$G(s) = C (sI - A)^{-1} B + D = D + \sum_{k \ge 1} C A^{k - 1} B\, s^{-k}.$$

The matrices $C A^{k - 1} B$ are the [Markov parameters](/markov-parameters/). So $G$ is proper with $G(\infty) = D$, and each entry has a denominator that divides $\det(sI - A)$. Conversely, every proper $G \in \mathbb{R}(s)^{p \times m}$ has a state-space realization; this is the [realization problem](/realization-problem/). The least state dimension among the realizations is the *McMillan degree* of $G$, and a realization of that dimension is a [minimal realization](/minimal-realization/).

**Poles and zeros.** The set of poles of $G$ is the union of the poles of its entries. The multiplicities, and the zeros, are not read from the entries: they come from the [Smith-McMillan form](/smith-mcmillan-form/). The poles of $G$ with multiplicity are the eigenvalues of $A$ of a minimal realization, and the McMillan degree is their number. The zeros of $G$ are its [transmission zeros](/transmission-zero/).

**Frequency response and size.** For a system whose poles are all in the open left half plane, $G(i\omega)$ is the steady-state gain matrix for sinusoidal inputs of frequency $\omega$. Its largest and smallest singular values bound the gain of $G(i\omega)$ over all input directions, and the largest one over all $\omega$ is the [H-infinity norm](/h-infinity-norm/). The steady-state gain for constant inputs is $G(0) = -CA^{-1}B + D$ when $A$ is invertible.

**Feedback.** With a controller $K$ and $u = K(r - y)$, the output is $y = (I + GK)^{-1} G K\, r$, and $S = (I + GK)^{-1}$ is the sensitivity matrix. The order of the factors matters: $(I + GK)^{-1}$ is $p \times p$ and $(I + KG)^{-1}$ is $m \times m$.

## Examples and non-examples

- **From a state-space model.** Take $A = \begin{pmatrix} 0 & 1 \\ -2 & -3 \end{pmatrix}$, $B = C = I$, $D = 0$. Then $\det(sI - A) = s^2 + 3s + 2$ and
$$G(s) = \frac{1}{s^2 + 3s + 2} \begin{pmatrix} s + 3 & 1 \\ -2 & s \end{pmatrix}.$$
Each entry has the poles $-1$ and $-2$.
- **Same entries, different degree.** $G_1 = \operatorname{diag}(1/(s + 1), 1/(s + 1))$ has McMillan degree 2: it needs two states, $A = -I_2$. $G_2 = \begin{pmatrix} 1/(s + 1) & 1/(s + 1) \end{pmatrix}$ has McMillan degree 1: $A = -1$, $B = \begin{pmatrix} 1 & 1 \end{pmatrix}$, $C = 1$. Both have the single pole $-1$, but with multiplicity 2 for $G_1$ and 1 for $G_2$.
- **A zero that no entry has.** Let
$$G(s) = \begin{pmatrix} \dfrac{1}{s + 1} & \dfrac{2}{s + 3} \\[2mm] \dfrac{1}{s + 1} & \dfrac{1}{s + 1} \end{pmatrix}, \qquad \det G(s) = \frac{1 - s}{(s + 1)^2 (s + 3)}.$$
No entry is zero at $s = 1$, but $G(1) = \begin{pmatrix} 1/2 & 1/2 \\ 1/2 & 1/2 \end{pmatrix}$ has rank 1, and the input direction $(1, -1)$ is blocked there: $s = 1$ is a transmission zero in the right half plane, which limits the performance of any feedback loop around $G$. The steady-state gain is $G(0) = \begin{pmatrix} 1 & 2/3 \\ 1 & 1 \end{pmatrix}$.
- **Non-example: an improper matrix.** $\begin{pmatrix} s & 1 \end{pmatrix}$ is rational, but its first entry is a differentiator, which is not proper. It can describe an ideal model, but no $(A, B, C, D)$ model has it as its transfer matrix, since $C(sI - A)^{-1}B + D$ is always proper.
- **Non-example: a time-varying system.** A [linear time-varying system](/linear-time-varying-system/) $x' = A(t)x + B(t)u$ has no transfer matrix: the response to $e^{st}$ is not a multiple of $e^{st}$, and $Y(s) = G(s)U(s)$ fails for every fixed $G$.
- **Non-example: the entries alone.** The list of entries, each read as a separate scalar system, does not show the poles and zeros of the matrix. In the zero example above, every entry is minimum phase, yet the matrix has a right half plane zero. Interaction measures such as the [relative gain array](/relative-gain-array/) are used to judge when the entries can be treated one by one.

## Related definitions

- [Transfer function](/transfer-function/): the case $m = p = 1$.
- [Transmission zero](/transmission-zero/): a value of $s$ where $G$ loses rank below its normal rank.
- [Smith-McMillan form](/smith-mcmillan-form/): the diagonal form that gives the poles and zeros of $G$ with multiplicities.
- [Minimal realization](/minimal-realization/): a state-space model of $G$ with the least number of states, the McMillan degree.
- [Markov parameters](/markov-parameters/): the coefficients $C A^{k - 1} B$ of the expansion of $G$ at $s = \infty$.
- [H-infinity norm](/h-infinity-norm/): the peak over frequency of the largest singular value of $G(i\omega)$.
- [Relative gain array](/relative-gain-array/): a measure of the interaction between the loops of a square $G$.

## References
