---
tag: TDAR9X
kind: algorithm
slug: zero-order-hold-discretization
name: Zero-order hold discretization
aliases:
- ZOH discretization
- step-invariant discretization
area: control/modeling-and-identification
level: core
summary: Turns a continuous LTI system into the exact discrete one for inputs held constant between samples, with A_d = e^(Ah).
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {n: the number of states, m: the number of inputs, s: the number of squarings in the matrix exponential}
  time: {worst: "O((n + m)^3 (s + 1))"}
  space: {extra: "O((n + m)^2)"}
properties: {deterministic: true, exact: true, recursive: false, online: false}
history:
  year: 1978
  people: [Charles F. Van Loan]
  note: "The model x_(k+1) = e^(Ah) x_k + B_d u_k was standard in the state-space theory of sampled systems by the early 1960s; Van Loan showed in 1978 that one exponential of a block matrix gives both matrices."
prereqs: [matrix-exponential, variation-of-constants-formula, state-space-representation]
see_also: [sampled-data-system, controller-discretization, bilinear-transform, z-transform, euler-method, exponential-integrators, poles-and-zeros, aliasing]
sources:
  - paper: doi:10.1109/TAC.1978.1101743
    title: Charles F. Van Loan, Computing integrals involving the matrix exponential, IEEE Transactions on Automatic Control 23(3), 395-404, 1978
    locator: the block triangular matrix whose exponential contains the integrals of e^(As), applied to the discretization of linear systems
  - book: isbn:9780486486130
    title: Karl J. Åström and Björn Wittenmark, Computer-Controlled Systems, Theory and Design, third edition, Prentice Hall, 1997 (Dover reprint, 2011)
    locator: Section 2.3, Sampling a Continuous-Time State-Space System; Section 2.8, Poles and Zeros; Section 2.9, Selection of Sampling Rate
  - paper: doi:10.1016/0005-1098(84)90062-1
    title: Karl J. Åström, Per Hagander and Jan Sternby, Zeros of sampled systems, Automatica 20(1), 31-38, 1984
    locator: the limits of the zeros of the sampled system as h goes to 0, and the unstable sampling zeros for relative degree above 2
  - paper: doi:10.1137/S00361445024180
    title: Cleve Moler and Charles Van Loan, Nineteen dubious ways to compute the exponential of a matrix, twenty-five years later, SIAM Review 45(1), 3-49, 2003
    locator: the scaling and squaring method and the methods based on block exponentials
  - paper: doi:10.1137/04061101X
    title: Nicholas J. Higham, The scaling and squaring method for the matrix exponential revisited, SIAM Journal on Matrix Analysis and Applications 26(4), 1179-1193, 2005
    locator: the choice of the scaling and of the Padé degree used by current libraries
  - paper: "R. E. Kalman, Y. C. Ho and K. S. Narendra, Controllability of linear dynamical systems, Contributions to Differential Equations 1, 189-213, 1963"
    locator: the section on the loss of controllability and observability due to sampling
---

Zero-order hold (ZOH) discretization turns the continuous linear time-invariant model $\dot x = A x + B u$, $y = C x + D u$ into the discrete model $x_{k+1} = A_d x_k + B_d u_k$, $y_k = C x_k + D u_k$, with $A_d = e^{Ah}$ and $B_d = \left(\int_0^h e^{As}\, ds\right) B$, for the sampling period $h$. The discrete model is exact, not an approximation: if the input is held constant between samples, $x_k$ equals the continuous state $x(kh)$ for every $k$. One [matrix exponential](/matrix-exponential/) of the block matrix $\begin{bmatrix} A & B \\ 0 & 0 \end{bmatrix} h$ gives both matrices (Van Loan 1978). It differs from [controller discretization](/controller-discretization/) by Tustin or matched poles, which approximate a continuous controller, and from the [bilinear transform](/bilinear-transform/), which is an approximate map of $s$ to $z$.

## In plain words

A computer controls a physical system. At each tick of its clock it reads the sensors, computes a new command, and sends it to a device that keeps that command fixed until the next tick. Between two ticks the system therefore moves under a constant push. For a linear system, the move over one tick depends only on where the system started and on the size of the push, and both effects are linear. This method computes the two matrices that describe that one-tick move. With these matrices, the computer sees the system as a simple step-by-step rule that gives the correct state at every tick. The model says nothing about the motion between ticks; for that you need the continuous model.

## The problem

Input: $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$ and a sampling period $h > 0$. Output: $A_d \in \mathbb{R}^{n \times n}$ and $B_d \in \mathbb{R}^{n \times m}$ such that every solution of $\dot x = A x + B u$ with a zero-order hold input, $u(t) = u_k$ for $kh \le t < (k+1)h$, satisfies $x((k+1)h) = A_d\, x(kh) + B_d\, u_k$ for all $k \ge 0$, all initial states and all input sequences.

The output matrices $C$ and $D$ do not change, because $y_k = y(kh) = C x(kh) + D u_k$ when the output is read at the sampling instant. Both matrices are unique: the solution over one period is linear in $(x(kh), u_k)$, and its matrix is fixed by the plant (see [variation of constants formula](/variation-of-constants-formula/)). Notation follows the [state-space representation](/state-space-representation/) page.

## The algorithm

```pseudo id=main
ZOH(A, B, h)
L1  M ← [[A·h, B·h], [0, 0]]                       ▷ (n + m) by (n + m), last m rows zero
L2  E ← exp(M)                                     ▷ any accurate matrix exponential
L3  A_d ← E[1..n, 1..n]
L4  B_d ← E[1..n, n+1..n+m]; return (A_d, B_d)
```

Line L1 builds the block matrix of Van Loan (1978), already multiplied by $h$. Line L2 takes its exponential. The implementation uses scaling and squaring with a Taylor series; libraries use scaling and squaring with a Padé approximant (Higham 2005). Lines L3 and L4 read the two top blocks. The bottom right block of $E$ is the identity $I_m$, and the bottom left block is zero; the code does not use them.

The reason is the identity

$$\exp\left(\begin{bmatrix} A & B \\ 0 & 0 \end{bmatrix} h\right) = \begin{bmatrix} e^{Ah} & \int_0^h e^{As}\, ds\, B \\ 0 & I_m \end{bmatrix},$$

which is proved in proofs/correctness.md. It avoids the formula $B_d = A^{-1}(e^{Ah} - I) B$, which fails when $A$ is singular, for example for an integrator, and loses accuracy when $A$ is close to singular.

## Example

**Double integrator.** Take $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, a mass pushed by a force, and $h = 0.5$. Line L1 gives

$$M = \begin{bmatrix} 0 & 0.5 & 0 \\ 0 & 0 & 0.5 \\ 0 & 0 & 0 \end{bmatrix}, \qquad M^2 = \begin{bmatrix} 0 & 0 & 0.25 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{bmatrix}, \qquad M^3 = 0.$$

So the series stops, and line L2 gives $E = I + M + M^2/2 = \begin{bmatrix} 1 & 0.5 & 0.125 \\ 0 & 1 & 0.5 \\ 0 & 0 & 1 \end{bmatrix}$. Lines L3 and L4 read $A_d = \begin{bmatrix} 1 & 0.5 \\ 0 & 1 \end{bmatrix}$ and $B_d = \begin{bmatrix} 0.125 \\ 0.5 \end{bmatrix}$. For a general $h$ these are $A_d = \begin{bmatrix} 1 & h \\ 0 & 1 \end{bmatrix}$ and $B_d = \begin{bmatrix} h^2/2 \\ h \end{bmatrix}$: in one period a unit force moves the mass by $h^2/2$ and changes the velocity by $h$. Here $A$ is singular, so $A^{-1}(e^{Ah} - I) B$ cannot be used.

**Oscillator.** For $A = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ and $h = 0.1$, the code returns $A_d = \begin{bmatrix} 0.995004 & 0.099833 \\ -0.099833 & 0.995004 \end{bmatrix}$, which is the rotation $\begin{bmatrix} \cos h & \sin h \\ -\sin h & \cos h \end{bmatrix}$, and $B_d = \begin{bmatrix} 0.004996 \\ 0.099833 \end{bmatrix} = \begin{bmatrix} 1 - \cos h \\ \sin h \end{bmatrix}$.

**Poles and zeros.** For $G(s) = 1/(s(s+1))$ with $A = \begin{bmatrix} 0 & 1 \\ 0 & -1 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $C = \begin{bmatrix} 1 & 0 \end{bmatrix}$ and $h = 1$, the pulse transfer function $C(zI - A_d)^{-1} B_d$ is

$$H(z) = \frac{0.3679\, z + 0.2642}{(z - 1)(z - 0.3679)}.$$

The poles are $e^{0 \cdot h} = 1$ and $e^{-1 \cdot h} = 0.3679$. The continuous system has no finite zero, but $H$ has a zero at $-0.7183$. With $h = 0.1$ the zero moves to $-0.9672$, close to $-1$. For the triple integrator $1/s^3$ the result is

$$H(z) = \frac{h^3}{6} \cdot \frac{z^2 + 4z + 1}{(z - 1)^3},$$

with zeros $-2 \pm \sqrt 3$, that is $-3.7321$ and $-0.2679$, for every $h$. One zero is outside the unit circle. The tests compute these numerators as $\det(zI - A_d + B_d C) - \det(zI - A_d)$.

## Correctness

The full proof is in proofs/correctness.md. In short: on one period the input is a constant $u_k$, and the solution of $\dot x = A x + B u_k$ from $x(kh)$ is $e^{A\tau} x(kh) + \int_0^\tau e^{As}\, ds\, B u_k$ by the variation of constants formula. At $\tau = h$ this is $A_d x_k + B_d u_k$. The block identity follows because $E(\tau) = \begin{bmatrix} e^{A\tau} & \int_0^\tau e^{As} ds\, B \\ 0 & I \end{bmatrix}$ satisfies $E' = M E$ and $E(0) = I$, which defines $e^{M\tau}$. The tests check the result against the double integrator values, against $A^{-1}(e^{Ah} - I)B$ for invertible $A$, against the identity $A_d(2h) = A_d(h)^2$, $B_d(2h) = A_d(h) B_d(h) + B_d(h)$, and against an RK4 simulation with step $h/100$ and the input held over each period, which agrees to $10^{-9}$.

## Complexity

In the [real RAM](/real-ram/), with dense matrices of size $N = n + m$:

- Line L1 costs $O(N^2)$.
- Line L2 costs $O(N^3)$ per matrix product. Scaling and squaring needs $s = \max(0, \lceil \log_2(2 \|Mh\|_\infty) \rceil)$ squarings and a fixed number of products for the Taylor or Padé part, so the cost is $O(N^3 (s + 1))$ flops. The number $s$ grows like $\log_2 (h \|[A, B]\|)$.
- Lines L3 and L4 cost $O(N^2)$.

The extra space is $O(N^2)$. The computation runs once, offline, for a fixed $h$. The discrete model then costs $O(n^2 + nm)$ per step, the same as any explicit linear recursion. Exploiting the zero rows of $M$ saves a constant factor only.

## Properties

- **Poles map by $z = e^{sh}$.** This is a theorem: if $A v = \lambda v$, then $e^{Ah} v = e^{\lambda h} v$, and the eigenvalues of $A_d$ are the numbers $e^{\lambda h}$ with the same algebraic multiplicities. So a Hurwitz $A$ gives a Schur $A_d$, because $|e^{\lambda h}| = e^{h \operatorname{Re} \lambda} < 1$ exactly when $\operatorname{Re} \lambda < 0$.
- **Zeros do not map by $e^{sh}$.** The sampled system has, in general, $n - 1$ finite zeros whatever the continuous zeros are. If $G(s)$ has $r$ finite zeros and relative degree $d = n - r$, then as $h \to 0$ the $r$ zeros of $H(z)$ tend to $e^{z_i h}$ and the other $d - 1$ zeros, the *sampling zeros*, tend to the zeros of a fixed polynomial that depends only on $d$ (Åström, Hagander and Sternby 1984). For $d = 2$ the limit is $-1$; for $d \ge 3$ the limits include a zero outside the unit circle, $-3.7321$ for $d = 3$. So the sampled model of a minimum phase plant with relative degree 3 or more is not [minimum phase](/minimum-phase/) for short sampling periods.
- **Step invariance.** The step response of the discrete model equals the samples of the continuous step response. This is the reason for the name "step-invariant". The static gain is kept: if $A$ is invertible and 1 is not an eigenvalue of $A_d$, then $C(I - A_d)^{-1} B_d + D = -C A^{-1} B + D$, because $B_d = A^{-1}(A_d - I) B$ and $A^{-1}$ commutes with $A_d$.
- **Controllability can be lost.** If two eigenvalues of $A$ differ by $2\pi i k / h$ for a nonzero integer $k$, the pair $(A_d, B_d)$ can lose controllability although $(A, B)$ is controllable. If no two eigenvalues differ in that way, controllability is kept (Kalman, Ho and Narendra 1963). The [sampled-data system](/sampled-data-system/) page has the example.
- **Exact for any $h$.** There is no step-size limit and no stiffness problem, unlike [Euler's method](/euler-method/) with $A_d \approx I + Ah$, which is only first order accurate and can turn a stable plant into an unstable model when $h$ is large.

## Variants and improvements

- **Output and cost integrals.** Van Loan's paper is about general integrals of matrix exponentials. Larger block matrices give the sampled cost matrices of a continuous quadratic cost, which [finite-horizon LQR](/finite-horizon-lqr/) on the sampled model needs, and the covariance $\int_0^h e^{As} Q e^{A^T s}\, ds$ of sampled process noise, which a discrete [Kalman filter](/kalman-filter/) needs.
- **Time delay.** An input delay of $\tau = \ell h + \tau'$ with $0 \le \tau' < h$ splits the input matrix into two parts, $\int_0^{h - \tau'} e^{As} ds\, B$ for $u_{k - \ell}$ and $e^{A(h - \tau')}\int_0^{\tau'} e^{As} ds\, B$ for $u_{k - \ell - 1}$, and adds the old inputs to the state (Åström and Wittenmark, Chapter 2). See [time-delay system](/time-delay-system/).
- **Other holds.** A first-order or a triangle hold interpolates the input linearly between samples. The same block exponential method works with one more block row. These holds are less common in hardware.
- **Approximate maps.** Forward Euler, backward Euler and the [bilinear transform](/bilinear-transform/) give rational approximations of $e^{Ah}$. They are cheaper and exact for no input class; the bilinear transform is used for controllers, not for plant models.
- **The exponential itself.** Moler and Van Loan (2003) compare the methods. Scaling and squaring with Padé approximants (Higham 2005) is the standard. SciPy's `cont2discrete` with method `zoh` builds the same block matrix and calls its `expm`.
- **Exponential integrators.** In numerical analysis, the same matrices give the exponential Euler method for $\dot x = A x + g(t, x)$, with $g$ frozen over a step; see [exponential integrators](/exponential-integrators/).

## When to use it

Use ZOH discretization to get the plant model for digital control design when the actuator holds the command between updates, which is what a digital-to-analog converter does. The discrete model is then exact, and pole placement, LQR, MPC and Kalman filtering in discrete time apply to it directly. It is also the right tool to simulate a linear plant with a piecewise constant input: it is exact at any step size, so a stiff plant does not force a small step.

Do not use it to discretize a continuous controller that was designed in continuous time; the input of a controller is a sampled measurement, not a held signal. Use [controller discretization](/controller-discretization/) with Tustin or matched poles and zeros. Do not use it for a nonlinear plant without a check: for $\dot x = f(x, u)$ it applies only to the [linearization about an equilibrium](/jacobian-linearization/).

## Pitfalls

- **The model is exact only at the samples.** Between samples the state is $x(kh + \tau) = e^{A\tau} x_k + \int_0^\tau e^{As} ds\, B u_k$. A controller that makes the samples converge can still leave an oscillation between them, for example a deadbeat controller that cancels a sampling zero near $-1$. Check the continuous response, or compute $x(kh + \tau)$ with the same method for a few $\tau$.
- **The input must really be held.** If the actuator has its own dynamics, add them to the plant. If the computation takes a large part of the period, the new input acts with a delay; model it as in the delay variant above.
- **Sampling zeros.** Do not cancel the zeros of $H(z)$ with the controller when $H$ has a sampling zero outside the unit circle or near $-1$. The cancellation is unstable or rings between samples.
- **Do not map zeros by $e^{sh}$.** That is the matched pole-zero method, an approximation. The exact ZOH model has the zeros of the Example section.
- **Pathological periods.** For lightly damped modes, avoid $h$ near $\pi / \omega$ and its multiples, where $\omega$ is the frequency of the mode. The model then loses controllability or observability of that mode. See [aliasing](/aliasing/).
- **Very short periods.** As $h \to 0$, $A_d \to I$ and $B_d \to 0$, and the poles all crowd near $z = 1$. The coefficients of $H(z)$ then lose relative precision in floating point. Keep the state-space form, or use the scaled form $(A_d - I)/h$.
- **The choice of $h$ is a design rule, not a theorem.** Rules of thumb tie $h$ to the rise time or to the closed-loop bandwidth; Åström and Wittenmark discuss them in Section 2.9. The [sampling theorem](/sampling-theorem/) is about the reconstruction of band-limited signals and gives no bound on control performance.
- **$B_d$ by inversion.** The formula $A^{-1}(e^{Ah} - I)B$ is correct only for invertible $A$ and is inaccurate when $A$ has an eigenvalue near 0. The block exponential has no such condition.

## Implementations

## History

The model $x_{k+1} = e^{Ah} x_k + \int_0^h e^{As} ds\, B u_k$ is a direct use of the solution formula of linear differential equations. It was standard in the state-space theory of sampled systems by the early 1960s; Kalman, Ho and Narendra (1963) used it to study the loss of controllability by sampling. Van Loan (1978) showed that integrals of this kind are blocks of the exponential of a larger block triangular matrix, which reduced the computation to one call of a matrix exponential routine. Åström, Hagander and Sternby (1984) described the zeros of sampled systems and showed the unstable sampling zeros for relative degree above 2.

## References
