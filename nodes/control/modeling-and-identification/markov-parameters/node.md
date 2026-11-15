---
tag: TH80MD
kind: definition
slug: markov-parameters
name: Markov parameters
aliases:
- impulse response coefficients of a state-space model
area: control/modeling-and-identification
level: core
summary: The matrices D, CB, CAB, CA^2B and so on, the impulse response of a discrete state-space system, which fill its Hankel matrix.
prereqs: [state-space-representation, impulse-response]
see_also: [realization-problem, minimal-realization, ho-kalman-algorithm, eigensystem-realization-algorithm, hankel-singular-values, transfer-function, z-transform, zero-order-hold-discretization]
sources:
  - book: isbn:9780195117776
    title: "Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999"
    locator: "Chapter 7 (minimal realizations), the section on realization from Markov parameters"
  - paper: doi:10.1524/auto.1966.14.112.545
    title: "B. L. Ho and Rudolf E. Kalman, Effective construction of linear state-variable models from input/output functions, Regelungstechnik 14(1-12), 545-548, 1966"
    locator: the sequence of Markov parameters as the input-output data, and the block Hankel matrix built from it
  - book: isbn:9780130792112
    title: "Jer-Nan Juang, Applied System Identification, Prentice Hall, 1994"
    locator: the chapters on the Markov parameters of discrete-time models and their computation from input-output data
---

The Markov parameters of a discrete-time state-space system $x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$ are the matrices $h_0 = D$ and $h_k = C A^{k-1} B$ for $k \ge 1$. They are the [impulse response](/impulse-response/) of the system: with zero initial state, a unit pulse in input $j$ at time 0 gives the output $y_k$ equal to column $j$ of $h_k$. They do not depend on the choice of state coordinates, so they are the part of $(A, B, C, D)$ that input-output data can show. Arranged in a block Hankel matrix, they are the data of the [realization problem](/realization-problem/), which asks for $(A, B, C, D)$ with given Markov parameters. The [minimal realization](/minimal-realization/) theorem says that the rank of that Hankel matrix is the smallest possible state dimension.

## Definition

**Notation.** The system has $n$ states, $m$ inputs and $p$ outputs, so $A$ is $n \times n$, $B$ is $n \times m$, $C$ is $p \times n$ and $D$ is $p \times m$. Time is discrete.

**Definition.** The Markov parameters of $(A, B, C, D)$ are the $p \times m$ matrices

$$h_0 = D, \qquad h_k = C A^{k-1} B \quad (k = 1, 2, \ldots).$$

**The impulse response.** With $x_0 = 0$, the output is the convolution

$$y_k = \sum_{t=0}^{k} h_{k-t} u_t.$$

To see this, iterate the state equation: $x_k = \sum_{t=0}^{k-1} A^{k-1-t} B u_t$, so $y_k = \sum_{t=0}^{k-1} C A^{k-1-t} B u_t + D u_k$. For $u_t$ equal to the unit vector $e_j$ at $t = 0$ and zero after, $y_k = h_k e_j$.

**The transfer function.** The [transfer function](/transfer-function/) is the [z-transform](/z-transform/) of the Markov parameters:

$$G(z) = D + C (z I - A)^{-1} B = \sum_{k=0}^{\infty} h_k z^{-k},$$

for $|z|$ larger than the spectral radius of $A$. This follows from $(z I - A)^{-1} = \sum_{k \ge 1} A^{k-1} z^{-k}$.

**Invariance.** For a nonsingular $T$, the system $(T^{-1} A T, T^{-1} B, C T, D)$ has the same Markov parameters, because $C T (T^{-1} A T)^{k-1} T^{-1} B = C A^{k-1} B$. So the Markov parameters are a property of the input-output map, not of one state-space form.

**The Hankel matrix.** For integers $r, s \ge 1$, the block Hankel matrix of size $rp \times sm$ has the block $h_{i+j-1}$ in block row $i$ and block column $j$, for $i = 1, \ldots, r$ and $j = 1, \ldots, s$. It factors as

$$H_{r,s} = \begin{pmatrix} C \\ C A \\ \vdots \\ C A^{r-1} \end{pmatrix} \begin{pmatrix} B & A B & \cdots & A^{s-1} B \end{pmatrix},$$

the product of the extended [observability](/observability/) matrix and the extended [controllability](/controllability/) matrix. Its rank is at most $n$. If $(A, B)$ is controllable, $(A, C)$ is observable, and $r, s \ge n$, the rank is exactly $n$.

**The recurrence.** Let $\det(z I - A) = z^n + a_1 z^{n-1} + \cdots + a_n$. By the Cayley-Hamilton theorem, $A^n = -a_1 A^{n-1} - \cdots - a_n I$, and so

$$h_{k+n} = -a_1 h_{k+n-1} - a_2 h_{k+n-2} - \cdots - a_n h_k \qquad (k \ge 1).$$

Every Markov parameter after $h_n$ follows from the $n$ before it. For a system of known order $n$, the parameters $h_1, \ldots, h_{2n}$ determine the whole sequence, because they fix a minimal realization (see the [Ho-Kalman algorithm](/ho-kalman-algorithm/)).

**Continuous time.** For $\dot x = A x + B u$, $y = C x + D u$, the matrices $C A^{k} B$ are also called Markov parameters. They are the coefficients of the expansion $G(s) = D + \sum_{k \ge 0} C A^{k} B s^{-k-1}$ at $s = \infty$, and the derivatives at $t = 0^+$ of the impulse response $C e^{A t} B$. The index is shifted by one compared with the discrete case.

## Examples and non-examples

**A second order system.** Take

$$A = \begin{pmatrix} 0.7 & 0.4 \\ -0.4 & 0.7 \end{pmatrix}, \quad B = \begin{pmatrix} 1 \\ 0.5 \end{pmatrix}, \quad C = \begin{pmatrix} 1 & 0 \end{pmatrix}, \quad D = 0.2.$$

Then $A B = (0.9, -0.05)^T$ and $A^2 B = (0.61, -0.395)^T$, so

$$h_0 = 0.2, \quad h_1 = 1, \quad h_2 = 0.9, \quad h_3 = 0.61, \quad h_4 = 0.269, \quad h_5 = -0.0199.$$

The characteristic polynomial is $z^2 - 1.4 z + 0.65$, and the recurrence $h_{k+2} = 1.4 h_{k+1} - 0.65 h_k$ checks the values: $1.4 \cdot 0.9 - 0.65 \cdot 1 = 0.61$, $1.4 \cdot 0.61 - 0.65 \cdot 0.9 = 0.269$ and $1.4 \cdot 0.269 - 0.65 \cdot 0.61 = -0.0199$. The $2 \times 2$ Hankel matrix $\begin{pmatrix} 1 & 0.9 \\ 0.9 & 0.61 \end{pmatrix}$ has determinant $-0.2$, so it has rank 2, and the $3 \times 3$ Hankel matrix of $h_1, \ldots, h_5$ has determinant 0 because of the recurrence. The minimal order is 2.

**A scalar first order system.** For $x_{k+1} = a x_k + b u_k$, $y_k = c x_k$, the Markov parameters are $h_0 = 0$ and $h_k = c b a^{k-1}$, a geometric sequence. All Hankel matrices have rank 1.

**Non-example: a hidden mode.** For $A = \operatorname{diag}(0.5, 0.9)$, $B = (1, 1)^T$, $C = (1, 0)$ and $D = 0$, the Markov parameters are $h_k = 0.5^{k-1}$, the same as those of the first order system $a = 0.5$, $b = c = 1$. The mode at $0.9$ is not observable, and the Markov parameters do not see it. They describe only the controllable and observable part, as in the [Kalman decomposition](/kalman-decomposition/).

**Non-example: samples of a continuous impulse response.** For $\dot x = -x + u$, $y = x$, the impulse response is $g(t) = e^{-t}$. With [zero-order hold discretization](/zero-order-hold-discretization/) and sampling period $h$, the discrete system is $A_d = e^{-h}$, $B_d = 1 - e^{-h}$, and its Markov parameters are $h_k = e^{-(k-1)h} (1 - e^{-h}) = \int_{(k-1)h}^{kh} g(t)\, dt$, the change of the step response over one period. They are not the samples $g(kh)$: for $h = 0.1$, $h_1 = 0.0952$ but $g(0.1) = 0.9048$.

**Non-example: moments.** The expansion of $G$ around $z = 1$ (or of a continuous $G$ around $s = 0$) gives the moments of the impulse response, which describe low frequencies. The Markov parameters come from the expansion at infinity and describe the response at short times.

## Related definitions

- The [realization problem](/realization-problem/) asks for $(A, B, C, D)$ with given Markov parameters. The [minimal realization](/minimal-realization/) theorem gives the minimal order as the rank of the block Hankel matrix.
- The [Ho-Kalman algorithm](/ho-kalman-algorithm/) builds a minimal realization from exact Markov parameters. The [eigensystem realization algorithm](/eigensystem-realization-algorithm/) does the same for noisy Markov parameters with an SVD.
- The [Hankel singular values](/hankel-singular-values/) are the singular values of the infinite block Hankel matrix of an asymptotically stable system.
- The [impulse response](/impulse-response/) of a linear time-invariant system is the same sequence without reference to a state-space form, and the [transfer function](/transfer-function/) is its z-transform.
- In subspace methods such as [MOESP](/moesp/), the Markov parameters fill the block Toeplitz matrix of the data equation.

## References
