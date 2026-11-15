---
tag: 1DAMQQ
kind: definition
slug: coprime-factorization
name: Coprime factorization
aliases:
- coprime factorization over stable transfer functions
area: control/robust-and-adaptive-control
level: advanced
summary: "Writes a transfer matrix as G = N M^(-1) with N and M in RH-infinity and a Bezout identity X M - Y N = I. It makes internal stability and the set of stabilizing controllers algebraic."
prereqs: [transfer-function, stabilizability, detectability]
see_also: [youla-parametrization, h-infinity-loop-shaping, nu-gap-metric, model-uncertainty, linear-fractional-transformation, state-feedback, extended-euclidean-algorithm, h-infinity-norm]
sources:
  - book: isbn:026222027X
    title: M. Vidyasagar, Control System Synthesis, A Factorization Approach, MIT Press, 1985
    locator: the chapters on coprime factorizations over the ring of proper rational functions with all poles in the open left half plane and on the parametrization of all stabilizing controllers
  - paper: "Carl N. Nett, Charles A. Jacobson and Mark J. Balas, A connection between state-space and doubly coprime fractional representations, IEEE Transactions on Automatic Control 29(9), 1984"
    locator: the state-space formulas for doubly coprime factorizations from a stabilizing state feedback gain and a stabilizing observer gain
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: the sections on coprime factorization over RH-infinity, normalized coprime factorizations and the parametrization of stabilizing controllers
---

A coprime factorization writes a transfer function, possibly with poles in the right half plane, as a ratio of two transfer functions in $RH_\infty$ (proper, with all poles in the open left half plane) that have no common zeros in the closed right half plane: $G = N M^{-1}$. It is the analogue, for the ring $RH_\infty$, of writing a rational number as a reduced fraction. The right half plane poles of $G$ become zeros of the denominator $M$, and coprimeness, expressed by a Bezout identity $X M - Y N = I$ with $X, Y \in RH_\infty$, means that no right half plane pole was cancelled. This turns feedback stability into algebra: a loop is internally stable when a certain matrix of factors has an inverse in $RH_\infty$, every stabilizing controller is given by the [Youla parametrization](/youla-parametrization/), and perturbations of the factors are a natural model of uncertainty for unstable plants.

## Definition

**The ring.** $RH_\infty$ is the set of real rational transfer matrices that are proper and have all their poles in the open left half plane (see the [H-infinity norm](/h-infinity-norm/)). A square $U \in RH_\infty$ is a unit if $U^{-1}$ exists and is also in $RH_\infty$; for a scalar, this means no zeros in the closed right half plane and a nonzero value at $s = \infty$.

**Right coprime factorization.** Let $G$ be a $p \times m$ real rational proper transfer matrix. A right coprime factorization is a pair $N \in RH_\infty^{p \times m}$, $M \in RH_\infty^{m \times m}$ with

$$G = N M^{-1}, \qquad \det M \not\equiv 0,$$

such that $N$ and $M$ are right coprime: there are $X \in RH_\infty^{m \times m}$ and $Y \in RH_\infty^{m \times p}$ with the Bezout identity

$$X M - Y N = I .$$

Equivalently, $\begin{bmatrix} M(s) \\ N(s) \end{bmatrix}$ has full column rank $m$ at every $s$ with $\operatorname{Re} s \ge 0$ and at $s = \infty$: the factors have no common zero there. The identity proves one direction, since $X M - Y N = I$ cannot hold at a point where $M v = 0$ and $N v = 0$ for some $v \ne 0$.

**Left coprime factorization.** $G = \tilde M^{-1} \tilde N$ with $\tilde M, \tilde N \in RH_\infty$ and $\tilde M \tilde X - \tilde N \tilde Y = I$ for some $\tilde X, \tilde Y \in RH_\infty$. For a scalar $G$, left and right are the same.

**Uniqueness.** If $G = N M^{-1} = N_1 M_1^{-1}$ are two right coprime factorizations, then $N_1 = N U$ and $M_1 = M U$ for a unit $U$. So the factors are unique up to a factor that is in $RH_\infty$ together with its inverse.

**Existence and state-space formulas.** Let $G(s) = C (sI - A)^{-1} B + D$ with $(A, B)$ [stabilizable](/stabilizability/) and $(C, A)$ [detectable](/detectability/), and choose $F$ and $L$ such that $A + B F$ and $A + L C$ are Hurwitz. Write $[\,\mathcal{A}, \mathcal{B}, \mathcal{C}, \mathcal{D}\,]$ for $\mathcal{C}(sI - \mathcal{A})^{-1}\mathcal{B} + \mathcal{D}$. Then (Nett, Jacobson and Balas 1984)

$$M = [\,A + B F,\ B,\ F,\ I\,], \qquad N = [\,A + B F,\ B,\ C + D F,\ D\,],$$

$$X = [\,A + L C,\ -(B + L D),\ F,\ I\,], \qquad Y = [\,A + L C,\ -L,\ F,\ 0\,],$$

$$\tilde M = [\,A + L C,\ L,\ C,\ I\,], \qquad \tilde N = [\,A + L C,\ B + L D,\ C,\ D\,],$$

give $G = N M^{-1} = \tilde M^{-1} \tilde N$ and $X M - Y N = I$, with all factors in $RH_\infty$. The factor $M$ is the map from an external input $v$ to $u$ under the state feedback $u = F x + v$, and $N$ is the map from $v$ to $y$. The controller $u = X^{-1} Y y$ is the observer-based controller with gains $F$ and $L$ (see [state feedback](/state-feedback/)), and it stabilizes $G$. Since every proper rational matrix has a minimal realization, which is stabilizable and detectable, every such $G$ has right and left coprime factorizations.

**Normalized coprime factorization.** A right coprime factorization is normalized if $M^\sim M + N^\sim N = I$, where $M^\sim(s) = M(-s)^T$. On the imaginary axis this says $M(j\omega)^H M(j\omega) + N(j\omega)^H N(j\omega) = I$: the stacked factor $\begin{bmatrix} M \\ N \end{bmatrix}$ is an isometry at every frequency. For $D = 0$, it is obtained from the formulas above with $F = -B^T X_c$, where $X_c$ is the stabilizing solution of the control Riccati equation $A^T X_c + X_c A - X_c B B^T X_c + C^T C = 0$ (see the [continuous algebraic Riccati equation](/continuous-algebraic-riccati-equation/)). It is unique up to a constant orthogonal matrix on the right.

**Internal stability.** In the loop $u = -K y$ with $G = \tilde M^{-1} \tilde N$ and $K = U V^{-1}$ (left and right coprime), the loop is internally stable if and only if $\tilde M V + \tilde N U$ is a unit of $RH_\infty$. For scalars this is the familiar fact that the closed-loop characteristic function $m v + n u$ must have no zeros in the closed right half plane and must not vanish at infinity.

## Examples and non-examples

- **An unstable first-order plant, the check value.** $G(s) = 1/(s - 1)$. Take $N = 1/(s + 1)$ and $M = (s - 1)/(s + 1)$: both are in $RH_\infty$, and $N/M = 1/(s - 1)$. The unstable pole of $G$ is the zero of $M$ at $s = 1$. The Bezout identity holds with constants: $2 N + M = (2 + s - 1)/(s + 1) = 1$. With $F = -2$ and $L = -2$, the state-space formulas give the same $M$ and $N$, and $X = (s + 3)/(s + 1)$, $Y = -4/(s + 1)$, with $X M - Y N = \bigl((s + 3)(s - 1) + 4\bigr)/(s + 1)^2 = 1$. The controller $u = X^{-1} Y y = -\frac{4}{s + 3} y$ gives the closed-loop polynomial $(s - 1)(s + 3) + 4 = (s + 1)^2$.
- **Normalized factors.** For the same plant, $N = 1/(s + a)$ and $M = (s - 1)/(s + a)$ give $|N(j\omega)|^2 + |M(j\omega)|^2 = (2 + \omega^2)/(a^2 + \omega^2)$, which is 1 for all $\omega$ exactly when $a = \sqrt 2$. The Riccati equation $2 x - x^2 + 1 = 0$ has the stabilizing root $x = 1 + \sqrt 2$, so $F = -(1 + \sqrt 2)$ and $A + B F = -\sqrt 2$, in agreement.
- **A plant with no unstable poles.** If $G \in RH_\infty$, then $N = G$, $M = I$ is a right coprime factorization, with $X = I$, $Y = 0$.
- **Non-example: a common unstable zero.** $N = (s - 1)/(s + 1)^2$ and $M = (s - 1)^2/(s + 1)^2$ are in $RH_\infty$ and $N/M = 1/(s - 1)$, but both vanish at $s = 1$. For any $X, Y \in RH_\infty$, $X M - Y N$ is 0 at $s = 1$, so the Bezout identity fails. The factors hide an unstable cancellation.
- **Non-example: a common zero at infinity.** $N = 1/(s + 1)^2$ and $M = (s - 1)/(s + 1)^2$ also give $1/(s - 1)$, and they have no common zero in the finite right half plane, but both tend to 0 as $s \to \infty$. Then $X M - Y N \to 0$ for bounded $X$, $Y$, so they are not coprime. This is why $\infty$ counts as a point of the closed right half plane here.
- **The polynomial analogue.** Over the ring of polynomials, $n(s)$ and $m(s)$ are coprime when $x n + y m = 1$ for polynomials $x$, $y$, which the [extended Euclidean algorithm](/extended-euclidean-algorithm/) computes. Polynomial fractions describe all poles; the factorization over $RH_\infty$ cares only about the unstable ones.

## Related definitions

- [Youla parametrization](/youla-parametrization/): every stabilizing controller in terms of the coprime factors and a free $Q \in RH_\infty$. For a scalar plant with $X M - Y N = 1$ and the loop $u = K y$, the controllers are $K = (Y + M Q)/(X + N Q)$, because then $M (X + N Q) - N (Y + M Q) = 1$. The closed-loop maps are affine in $Q$.
- [Model uncertainty](/model-uncertainty/): coprime factor perturbations $(M + \Delta_M)^{-1}(N + \Delta_N)$ describe uncertain unstable plants without fixing the number of unstable poles.
- [H-infinity loop shaping](/h-infinity-loop-shaping/): robust stabilization against normalized coprime factor uncertainty.
- [Nu-gap metric](/nu-gap-metric/): a distance between plants defined with normalized coprime factors.
- [Linear fractional transformation](/linear-fractional-transformation/): the controller set of the Youla parametrization is an LFT in $Q$.
- [Stabilizability](/stabilizability/) and [detectability](/detectability/): the conditions on a realization under which the state-space formulas apply.

## References
