---
tag: XE6NMD
kind: definition
slug: matrix-exponential
name: Matrix exponential
aliases:
- exponential of a matrix
- e^(At)
area: control/modeling-and-identification
level: core
summary: The sum of the series I + A + A^2/2! + ..., which gives the solution x(t) = e^(At)x(0) of the linear system x' = Ax.
prereqs: [eigenvalue, ode-initial-value-problem]
see_also: [state-transition-matrix, variation-of-constants-formula, zero-order-hold-discretization, cayley-hamilton-theorem, jordan-normal-form, pade-approximation, hurwitz-matrix, aalen-johansen-estimator]
sources:
  - paper: doi:10.1137/1020098
    title: Cleve Moler and Charles Van Loan, Nineteen dubious ways to compute the exponential of a matrix, SIAM Review 20(4), 801-836, 1978
    locator: the series, Padé, scaling and squaring, ODE, polynomial and matrix decomposition methods, and why each can fail
  - paper: doi:10.1137/S00361445024180
    title: Cleve Moler and Charles Van Loan, Nineteen dubious ways to compute the exponential of a matrix, twenty-five years later, SIAM Review 45(1), 3-49, 2003
    locator: the update of the 1978 survey, with scaling and squaring as the method of choice and Krylov methods for e^(A)v
  - paper: doi:10.1137/04061101X
    title: Nicholas J. Higham, The scaling and squaring method for the matrix exponential revisited, SIAM Journal on Matrix Analysis and Applications 26(4), 1179-1193, 2005
    locator: the backward error analysis that chooses the scaling and the degree 13 Padé approximant
  - book: isbn:9780898716467
    title: Nicholas J. Higham, Functions of Matrices, Theory and Computation, SIAM, 2008
    locator: Chapter 10, Matrix Exponential (properties, conditioning, and the scaling and squaring algorithm)
  - book: isbn:9780134412054
    title: Wilson J. Rugh, Linear System Theory, second edition, Prentice Hall, 1996
    locator: Chapter 5, Two Important Cases (the time-invariant case and the representations of e^(At))
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Chapter 3 (functions of a square matrix) and Chapter 4 (solution of the state equation)
---

The matrix exponential of a square matrix $A$ is $e^A = I + A + \frac{A^2}{2!} + \frac{A^3}{3!} + \cdots$, the power series of the scalar exponential with powers of the matrix in place of powers of a number. Its main use is the solution of linear differential equations: the solution of $\dot x = A x$ with $x(0) = x_0$ is $x(t) = e^{At} x_0$. The same object gives the transition probabilities $e^{Qt}$ of a continuous-time [Markov chain](/markov-chain/), the rigid motions $e^{\hat\xi \theta}$ of the [SE(3) exponential map](/se3-exponential-map/) in robotics, and the limit of the product integral behind the [Aalen-Johansen estimator](/aalen-johansen-estimator/). Unlike the scalar case, $e^{A + B} = e^A e^B$ holds when $A$ and $B$ commute, and fails in general when they do not.

## Definition

Let $A \in \mathbb{C}^{n \times n}$. The *matrix exponential* of $A$ is

$$e^A = \exp(A) = \sum_{k=0}^{\infty} \frac{A^k}{k!}, \qquad A^0 = I.$$

**The series converges for every $A$.** Take any submultiplicative matrix norm (see [matrix norms](/matrix-norms/)). Then $\|A^k / k!\| \le \|A\|^k / k!$, and $\sum_k \|A\|^k / k! = e^{\|A\|}$ is finite. So the series converges absolutely, entry by entry, and $\|e^A\| \le e^{\|A\|}$. The same bound on $\|At\|$ shows that $t \mapsto e^{At}$ is a power series in $t$ with infinite radius of convergence, so it can be differentiated term by term:

$$\frac{d}{dt} e^{At} = \sum_{k \ge 1} \frac{k t^{k-1} A^k}{k!} = A e^{At} = e^{At} A.$$

**Equivalent characterizations.** Each of these defines the same matrix:

1. *Differential equation.* $X(t) = e^{At}$ is the unique solution of $\dot X = A X$, $X(0) = I$. The derivative above shows that it is a solution, and the equation is linear, so it has only one solution by the [Picard-Lindelöf theorem](/picard-lindelof-theorem/). This is why $x(t) = e^{At} x_0$ solves $\dot x = A x$.
2. *Limit.* $e^A = \lim_{k \to \infty} (I + A/k)^k$. This is [Euler's method](/euler-method/) with step $1/k$ on $\dot X = A X$.
3. *Laplace transform.* For $\operatorname{Re} s$ larger than every real part of an eigenvalue of $A$, $\int_0^\infty e^{-st} e^{At}\, dt = (sI - A)^{-1}$. So $e^{At}$ is the inverse [Laplace transform](/laplace-transform/) of the resolvent, entry by entry.
4. *Jordan form.* If $A = T J T^{-1}$ with $J$ in [Jordan normal form](/jordan-normal-form/), then $e^{At} = T e^{Jt} T^{-1}$, and for a Jordan block $J_k(\lambda) = \lambda I + N$ of size $k$, $e^{J_k(\lambda) t} = e^{\lambda t} \sum_{j=0}^{k-1} \frac{t^j}{j!} N^j$, because $\lambda I$ and $N$ commute and $N^k = 0$. For a diagonalizable $A = V \Lambda V^{-1}$, $e^{At} = V \operatorname{diag}(e^{\lambda_i t}) V^{-1}$.
5. *Polynomial.* By the [Cayley-Hamilton theorem](/cayley-hamilton-theorem/), $A^n$ and all higher powers are combinations of $I, A, \dots, A^{n-1}$, so $e^{At} = \sum_{j=0}^{n-1} \alpha_j(t) A^j$ for scalar functions $\alpha_j$. The functions depend on $A$ through its eigenvalues.

**Properties.** These follow from the series or from characterization 1. Let $A, B \in \mathbb{C}^{n \times n}$ and $s, t$ scalars.

- $e^{0} = I$, $e^{A(s + t)} = e^{As} e^{At}$, and $e^{A}$ is invertible with $(e^A)^{-1} = e^{-A}$. So $e^{At}$ is never singular.
- *Similarity.* $e^{T A T^{-1}} = T e^A T^{-1}$ for invertible $T$, because $(T A T^{-1})^k = T A^k T^{-1}$. Also $(e^A)^T = e^{A^T}$ and $(e^A)^* = e^{A^*}$.
- *Eigenvalues.* If $\lambda_1, \dots, \lambda_n$ are the eigenvalues of $A$ with multiplicity, the eigenvalues of $e^A$ are $e^{\lambda_1}, \dots, e^{\lambda_n}$, with the same eigenvectors. So $\det e^A = e^{\operatorname{tr} A}$.
- *Sums.* If $AB = BA$, then $e^{A + B} = e^A e^B$. Proof: the binomial formula $(A + B)^k = \sum_j \binom{k}{j} A^j B^{k-j}$ holds because the matrices commute, and the Cauchy product of the two absolutely convergent series gives the result. Without commutation the formula fails; see the examples. The converse is false: for $A = \begin{bmatrix} 0 & 0 \\ 0 & 2\pi i \end{bmatrix}$ and $B = \begin{bmatrix} 0 & 1 \\ 0 & 2\pi i \end{bmatrix}$, $AB \ne BA$, but $e^A$, $e^B$ and $e^{A+B}$ are all equal to $I$, because each of the three matrices is diagonalizable with eigenvalues in $2\pi i \mathbb{Z}$.
- *Decay.* $e^{At} \to 0$ as $t \to \infty$ if and only if every eigenvalue of $A$ has negative real part, that is, $A$ is a [Hurwitz matrix](/hurwitz-matrix/). Then there are $c \ge 1$ and $\alpha > 0$ with $\|e^{At}\| \le c e^{-\alpha t}$ for all $t \ge 0$; any $\alpha$ below the smallest $|\operatorname{Re} \lambda_i|$ works, with a $c$ that depends on $\alpha$. In control this is the exponential stability of $\dot x = A x$ (see [exponential stability](/exponential-stability/)).

The time-varying system $\dot x = A(t) x$ has a [state-transition matrix](/state-transition-matrix/) $\Phi(t, t_0)$ in place of $e^{A(t - t_0)}$; in general $\Phi(t, t_0) \ne e^{\int_{t_0}^{t} A(\sigma) d\sigma}$.

**Computation.** The defining series is a poor algorithm in floating point. The standard method is *scaling and squaring*: choose $s$ with $\|A / 2^s\|$ small, approximate $e^{A / 2^s}$ by a [Padé approximant](/pade-approximation/) $r(A/2^s)$, and square the result $s$ times, since $e^A = (e^{A/2^s})^{2^s}$. Higham (2005) chose the Padé degree (up to 13) and the scaling from a backward error bound; current libraries use this method or a refinement of it. In the [real RAM](/real-ram/) the cost is $O(n^3)$ flops per matrix product, and the number of products is $O(\log_2 \|A\|)$ plus a constant. For a large sparse $A$, one needs $e^{At} v$ and not $e^{At}$; [Krylov subspace](/krylov-subspace/) methods give it without forming the matrix (Moler and Van Loan 2003). Methods based on eigenvectors are accurate only when the eigenvector matrix is well conditioned, and fail for defective $A$.

## Examples and non-examples

**Diagonal.** $e^{\operatorname{diag}(\lambda_1, \dots, \lambda_n) t} = \operatorname{diag}(e^{\lambda_1 t}, \dots, e^{\lambda_n t})$. The modes do not interact.

**Nilpotent: the double integrator.** For $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $A^2 = 0$, so the series stops: $e^{At} = I + At = \begin{bmatrix} 1 & t \\ 0 & 1 \end{bmatrix}$. The position is $x_1(t) = x_1(0) + t\, x_2(0)$. The entries grow like $t$, not like an exponential: this is the effect of a Jordan block of size 2 at $\lambda = 0$.

**Rotation.** For $A = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$, $A^2 = -I$, so the even terms give $\cos t$ and the odd terms give $\sin t$:

$$e^{At} = I \cos t + A \sin t = \begin{bmatrix} \cos t & \sin t \\ -\sin t & \cos t \end{bmatrix}.$$

The eigenvalues are $\pm i$, and $\det e^{At} = 1 = e^{\operatorname{tr}(A) t}$. This is a harmonic oscillator.

**Jordan block.** For $A = \begin{bmatrix} \lambda & 1 \\ 0 & \lambda \end{bmatrix}$, $e^{At} = e^{\lambda t}\begin{bmatrix} 1 & t \\ 0 & 1 \end{bmatrix}$. For $\lambda = -1$ the entry $t e^{-t}$ first grows to $e^{-1}$ at $t = 1$, then decays.

**Transient growth of a Hurwitz matrix.** For $A = \begin{bmatrix} -1 & 10 \\ 0 & -2 \end{bmatrix}$, with eigenvalues $-1$ and $-2$,

$$e^{At} = \begin{bmatrix} e^{-t} & 10(e^{-t} - e^{-2t}) \\ 0 & e^{-2t} \end{bmatrix}.$$

At $t = 1$ the top right entry is $10(0.36788 - 0.13534) = 2.3254$. The spectral norm $\|e^{At}\|_2$ starts at 1, rises to about $2.563$ near $t = 0.663$, and only then decays. The eigenvalues fix the rate of decay for large $t$, not the size of the transient. The cause is that $A$ is far from normal.

**$e^{A+B} \ne e^A e^B$.** Take $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$ and $B = \begin{bmatrix} 0 & 0 \\ 1 & 0 \end{bmatrix}$. Then $AB = \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix} \ne BA = \begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix}$, and

$$e^A e^B = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 \\ 1 & 1 \end{bmatrix} = \begin{bmatrix} 2 & 1 \\ 1 & 1 \end{bmatrix}, \qquad e^{A + B} = \begin{bmatrix} \cosh 1 & \sinh 1 \\ \sinh 1 & \cosh 1 \end{bmatrix} = \begin{bmatrix} 1.5431 & 1.1752 \\ 1.1752 & 1.5431 \end{bmatrix}.$$

The product is not even symmetric, while $A + B$ is symmetric and so is its exponential.

**Non-example: the entrywise exponential.** Applying $\exp$ to each entry of $A$ is a different operation. For the double integrator matrix above it gives $\begin{bmatrix} 1 & e \\ 1 & 1 \end{bmatrix}$, not $\begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$. The two agree only for very special $A$, such as $A = 0$.

**Non-example as an algorithm: the summed series.** In double precision, summing the Taylor series of the $1 \times 1$ matrix $A = [-49]$ term by term until the terms vanish gives $-30.53$. The true value is $e^{-49} = 5.24 \times 10^{-22}$. The terms grow to about $10^{20}$ before they shrink, and their rounding errors swamp the result. Moler and Van Loan (1978) discuss this failure of the series. Scaling and squaring avoids the cancellation.

**Non-example: the exponential of the integral.** For a time-varying $A(t)$, $\exp(\int_0^t A(\sigma)\, d\sigma)$ is the solution matrix of $\dot x = A(t) x$ only when $A(t)$ commutes with its integral; the [state-transition matrix](/state-transition-matrix/) page gives a counterexample.

## Related definitions

- **State-transition matrix.** The solution matrix $\Phi(t, t_0)$ of $\dot x = A(t) x$. For a constant $A$, $\Phi(t, t_0) = e^{A(t - t_0)}$. See [state-transition matrix](/state-transition-matrix/).
- **Variation of constants.** The solution of $\dot x = A x + B u$ is $e^{At} x_0 + \int_0^t e^{A(t - s)} B u(s)\, ds$. See [variation of constants formula](/variation-of-constants-formula/). The integral $\int_0^h e^{As} ds$ is the second block of the exponential of a block matrix, which is how [zero-order hold discretization](/zero-order-hold-discretization/) computes the input matrix of a sampled system.
- **Matrix logarithm.** A matrix $L$ with $e^L = M$. It exists for every invertible complex $M$ and is not unique. A real invertible $M$ has a real logarithm if and only if each Jordan block of a negative eigenvalue occurs an even number of times. Identifying a continuous model from a sampled one needs this logarithm, and the sampling period must avoid the pathological values of the [sampled-data system](/sampled-data-system/) page.
- **Product integral.** For a time-varying generator, the limit of ordered products $\prod (I + A(t_j)\, \Delta t)$ gives the transition matrix. With a constant $A$ it gives $e^{At}$, by characterization 2. The [Aalen-Johansen estimator](/aalen-johansen-estimator/) is a product integral of estimated transition intensities.
- **Exponential map of a Lie group.** For a matrix Lie group, $\exp$ maps the Lie algebra to the group: skew-symmetric matrices to rotations, and twists to rigid motions, as in the [SE(3) exponential map](/se3-exponential-map/) and the [product of exponentials formula](/product-of-exponentials-formula/).
- **Exponential integrators.** Numerical methods for $\dot x = A x + g(t, x)$ that use $e^{hA}$ and related functions to integrate the stiff linear part exactly. See [exponential integrators](/exponential-integrators/).
- **Hurwitz and Schur matrices.** $A$ is Hurwitz if all its eigenvalues have negative real parts. Then $e^{Ah}$ is a Schur matrix, with all eigenvalues inside the unit circle, for every $h > 0$.

## References
