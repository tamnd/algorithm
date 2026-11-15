---
tag: D7850W
kind: definition
slug: transmission-zero
name: Transmission zero
aliases:
- multivariable zero
- invariant zero
area: control/modeling-and-identification
level: advanced
summary: "A zero of a transfer matrix: a root of the numerators of its Smith-McMillan form. Away from the poles the matrix falls below its normal rank there, and an input e^(zt) u0 can give zero output."
prereqs: [transfer-function-matrix, poles-and-zeros]
see_also: [transfer-function-matrix, smith-mcmillan-form, poles-and-zeros, minimum-phase, zero-dynamics, generalized-eigenvalue-problem, qz-algorithm, kalman-decomposition]
sources:
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Section 3.11, Multivariable System Poles and Zeros (transmission zeros, invariant zeros and the system matrix)
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, second edition, Wiley, 2005
    locator: Section 4.5, Zeros, and Section 4.6, Some important remarks on poles and zeros
  - paper: doi:10.1016/0005-1098(82)90070-X
    title: A. Emami-Naeini and P. Van Dooren, Computation of zeros of linear multivariable systems, Automatica 18(4), 1982
    locator: pp. 415 to 430 (a backward stable reduction of the system pencil, for nonsquare and degenerate systems)
  - book: isbn:0177810025
    title: H. H. Rosenbrock, State-Space and Multivariable Theory, Nelson, London, 1970
    locator: the whole book (the system matrix and the zeros of multivariable systems)
---

A transmission zero of a linear system with several inputs and outputs is a complex number $z$ at which the [transfer function matrix](/transfer-function-matrix/) $G(s)$ loses rank, in the precise sense given by its [Smith-McMillan form](/smith-mcmillan-form/). At such a $z$ (if it is not also a pole), some input direction $u_0$ is blocked: the input $u_0 e^{zt}$, from the right initial state, gives the output zero for all time. Transmission zeros play the role that the zeros of a scalar [transfer function](/transfer-function/) play: a transmission zero in the right half plane limits what any feedback controller can do, and a controller that inverts the plant would cancel it with an unstable pole. The zeros of the matrix are in general not the zeros of its entries.

## Definition

**Notation.** $G \in \mathbb{R}(s)^{p \times m}$ is a rational matrix. Its *normal rank* $r$ is its rank as a matrix over the field $\mathbb{R}(s)$; equivalently, the rank of $G(s)$ at all but finitely many $s$.

**Definition.** Let the Smith-McMillan form of $G$ be $\operatorname{diag}(\varepsilon_1/\psi_1, \dots, \varepsilon_r/\psi_r)$, padded with zeros, with $\varepsilon_i$ and $\psi_i$ coprime monic polynomials. The *zero polynomial* of $G$ is $z(s) = \varepsilon_1(s) \varepsilon_2(s) \cdots \varepsilon_r(s)$. The *transmission zeros* of $G$ are the roots of $z(s)$, and the multiplicity of a zero is its multiplicity as a root of $z$.

**The rank test.** If $z$ is not a pole of $G$, then $z$ is a transmission zero if and only if $\operatorname{rank} G(z) < r$. The test fails at a pole, where $G(z)$ is not defined, and a zero can sit at the same point as a pole of another part of the matrix (see the examples).

**The system matrix.** For a realization $x' = Ax + Bu$, $y = Cx + Du$, the Rosenbrock system matrix is

$$P(s) = \begin{pmatrix} sI - A & -B \\ C & D \end{pmatrix}.$$

The *invariant zeros* of the realization are the $z$ with $\operatorname{rank} P(z)$ less than the normal rank of $P$. If the realization is [minimal](/minimal-realization/), the invariant zeros are exactly the transmission zeros of $G$, with the same multiplicities. If it is not minimal, the invariant zeros can also include uncontrollable or unobservable modes (the input and output decoupling zeros), which are not zeros of $G$. So "invariant zero" is a property of a realization and "transmission zero" a property of $G$; the two names agree only for minimal realizations.

**Blocking.** Let $G$ have full column rank $m$ as a rational matrix, and let $z$ be a transmission zero that is not an eigenvalue of $A$. Then $\operatorname{rank} G(z) < m$, so there is $u_0 \ne 0$ with $G(z) u_0 = 0$. Take $x_0 = (zI - A)^{-1} B u_0$ and $u(t) = u_0 e^{zt}$. Then $x(t) = x_0 e^{zt}$ solves $x' = Ax + Bu$, since $z x_0 = A x_0 + B u_0$, and

$$y(t) = (C x_0 + D u_0)\, e^{zt} = G(z)\, u_0\, e^{zt} = 0.$$

In matrix form, $P(z) \begin{pmatrix} x_0 \\ u_0 \end{pmatrix} = 0$. The vector $u_0$ is the input zero direction.

**Computation.** Write $P(s) = sE - M$ with $E = \begin{pmatrix} I & 0 \\ 0 & 0 \end{pmatrix}$ and $M = \begin{pmatrix} A & B \\ -C & -D \end{pmatrix}$. For a square system ($m = p$) with $\det P \not\equiv 0$, the invariant zeros are the finite eigenvalues of the [generalized eigenvalue problem](/generalized-eigenvalue-problem/) $M v = z E v$, which the [QZ algorithm](/qz-algorithm/) computes in a backward stable way. For a nonsquare or degenerate system, Emami-Naeini and Van Dooren (1982) first reduce the pencil by orthogonal transformations to a square regular part with the same finite zeros. If $D$ is square and invertible, the Schur complement of $D$ gives $\det P(s) = \det D \cdot \det(sI - A + B D^{-1} C)$, so the invariant zeros are the eigenvalues of $A - B D^{-1} C$.

**Why "invariant".** State feedback $u = -Kx + v$ changes $(A, C)$ to $(A - BK, C - DK)$, and

$$\begin{pmatrix} sI - A + BK & -B \\ C - DK & D \end{pmatrix} = P(s) \begin{pmatrix} I & 0 \\ -K & I \end{pmatrix}.$$

The right factor is invertible for every $s$, so the rank of the system matrix does not change at any $s$: state feedback moves the poles but never the invariant zeros. The same holds for output injection and for invertible changes of the input and output coordinates.

## Examples and non-examples

- **A zero that no entry has.** For
$$G(s) = \begin{pmatrix} 1/(s + 1) & 2/(s + 3) \\ 1/(s + 1) & 1/(s + 1) \end{pmatrix}, \qquad \det G = \frac{1 - s}{(s + 1)^2 (s + 3)},$$
the Smith-McMillan form is $\operatorname{diag}\bigl(1/((s + 1)(s + 3)),\ (s - 1)/(s + 1)\bigr)$, so $s = 1$ is a transmission zero. Indeed $G(1) = \tfrac12 \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$, with $u_0 = (1, -1)$. No entry of $G$ vanishes at $s = 1$.
- **A zero of an entry that is not a zero of the matrix.** For $G = \frac{1}{s + 1} \begin{pmatrix} 1 & s - 2 \\ 1 & 1 \end{pmatrix}$, the entry $(s - 2)/(s + 1)$ vanishes at $s = 2$, but $G(2) = \tfrac13 \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$ has full rank. The determinant of the numerator matrix is $3 - s$, so the only transmission zero is $s = 3$.
- **The scalar case through the system matrix.** $G(s) = (s + 3)/(s^2 + 3s + 2)$ has the minimal realization $A = \begin{pmatrix} 0 & 1 \\ -2 & -3 \end{pmatrix}$, $B = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$, $C = \begin{pmatrix} 3 & 1 \end{pmatrix}$, $D = 0$. Expanding $\det P(s)$ along the last column gives $\det P(s) = s + 3$, whose root $-3$ is the zero of $G$. In general, for one input and one output, $\det P(s) = \det(sI - A)\, G(s)$.
- **A zero at the location of a pole.** $G = \operatorname{diag}\bigl((s + 1)/(s + 2),\ (s + 2)/(s + 1)\bigr)$ has the transmission zeros $-1$ and $-2$ and the poles $-2$ and $-1$. Yet $\det G = 1$ for all $s$, and the rank test at $-1$ or $-2$ does not apply, because those points are poles. Only the Smith-McMillan form shows these zeros.
- **Non-example: a blocking direction for every $s$.** $G = \begin{pmatrix} 1/(s + 1) & 1/(s + 1) \end{pmatrix}$ has $G(s) (1, -1)^{\mathsf T} = 0$ for all $s$. Its normal rank is 1, its Smith-McMillan form is $\begin{pmatrix} 1/(s + 1) & 0 \end{pmatrix}$, and it has no transmission zero. The direction $(1, -1)$ is a null space of the rational matrix, not a zero.
- **Non-example: a hidden mode.** The realization $A = \operatorname{diag}(-1, -2)$, $B = (0, 1)^{\mathsf T}$, $C = (1, 1)$, $D = 0$ has $G = 1/(s + 2)$, which has no zero. But the mode $-1$ is uncontrollable, and $P(-1)$ has a zero first row, so $-1$ is an invariant zero of this realization and not a transmission zero of $G$.

## Related definitions

- [Poles and zeros](/poles-and-zeros/): the scalar case, where the transmission zeros are the roots of the numerator in lowest terms.
- [Smith-McMillan form](/smith-mcmillan-form/): the form whose numerators define the transmission zeros and their multiplicities.
- [Transfer function matrix](/transfer-function-matrix/): the object whose zeros these are.
- [Minimum phase](/minimum-phase/): a stable system whose transmission zeros all lie in the open left half plane.
- [Zero dynamics](/zero-dynamics/): the dynamics left when the output is held at zero; for a square, minimal linear system with a well-defined relative degree, their eigenvalues are the transmission zeros.
- [Kalman decomposition](/kalman-decomposition/): the split of a realization that separates the decoupling zeros from the transmission zeros.
- [Generalized eigenvalue problem](/generalized-eigenvalue-problem/): the form $(M - zE)v = 0$ in which zeros are computed.

## References
