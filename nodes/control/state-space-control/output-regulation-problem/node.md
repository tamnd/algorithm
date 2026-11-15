---
tag: ANRTEC
kind: problem
slug: output-regulation-problem
name: Output regulation problem
aliases:
- servomechanism problem
area: control/state-space-control
level: advanced
summary: Design a feedback so that the loop is internally stable and the output tracks references and rejects disturbances that a known autonomous exosystem generates.
prereqs: [state-space-representation, stabilizability, internal-model-principle]
see_also: [regulator-equations, internal-model-principle, integral-state-feedback, disturbance-decoupling-problem, sylvester-equation, transmission-zero, feedforward-control, two-degree-of-freedom-control]
sources:
  - paper: doi:10.1137/0315033
    title: B. A. Francis, The linear multivariable regulator problem, SIAM Journal on Control and Optimization 15(3), 486-505, 1977
    locator: the statement of the regulator problem with full information and with error feedback, and its solution by a pair of linear matrix equations
  - paper: doi:10.1109/TAC.1976.1101137
    title: E. J. Davison, The robust control of a servomechanism problem for linear time-invariant multivariable systems, IEEE Transactions on Automatic Control 21(1), 25-34, 1976
    locator: the robust servomechanism problem, its existence conditions, and the servocompensator built from the modes of the exosystem
  - paper: doi:10.1007/BF01447855
    title: B. A. Francis and W. M. Wonham, The internal model principle for linear multivariable regulators, Applied Mathematics and Optimization 2(2), 170-194, 1975
    locator: the internal model principle for regulation that is kept under perturbations of the plant
  - paper: doi:10.1109/9.45168
    title: A. Isidori and C. I. Byrnes, Output regulation of nonlinear systems, IEEE Transactions on Automatic Control 35(2), 131-140, 1990
    locator: the nonlinear output regulation problem and the partial differential equations that replace the linear regulator equations
  - book: isbn:9781852333164
    title: Harry L. Trentelman, Anton A. Stoorvogel and Malo Hautus, Control Theory for Linear Systems, Springer, 2001
    locator: Chapter 9, Tracking and regulation
---

The output regulation problem, also called the servomechanism problem, asks for a feedback controller that makes a closed loop internally stable and makes the tracking error $e(t)$ go to zero for every reference and disturbance in a known class. The class is the set of all outputs of an autonomous linear model, the *exosystem* $\dot w = S w$: constants come from $S = 0$, ramps from a Jordan block, and sinusoids of frequency $\omega$ from $S = \begin{bmatrix} 0 & \omega \\ -\omega & 0 \end{bmatrix}$. Francis (1977) proved that the problem is solvable exactly when the plant can be stabilized and two linear matrix equations, the [regulator equations](/regulator-equations/), have a solution. Davison (1976) and Francis and Wonham (1975) showed that a regulator that keeps working under small plant changes must contain a copy of the exosystem, which is the [internal model principle](/internal-model-principle/). Integral action for step references, [integral state feedback](/integral-state-feedback/), is the case $S = 0$.

## In plain words

You want a machine to follow a signal of a known type, such as a constant level, a steady ramp or a sine wave of known frequency, and to ignore a push of a known type. You do not know the size or the timing of these signals, only their type. The type is described by a small model that produces the signals by itself. The task is to design a controller that keeps the whole loop calm and makes the error die out for every signal of that type. The answer has two parts. First, the machine must be able to produce, in steady motion, the exact output that cancels the error; this is a linear equation. Second, a controller that is robust must copy the signal model inside it, for example an integrator for constant signals.

## Definition

**Data.** A plant and an exosystem

$$\dot x = A x + B u + P w, \qquad \dot w = S w, \qquad e = C x + Q w,$$

with $x \in \mathbb{R}^n$, $u \in \mathbb{R}^m$, $e \in \mathbb{R}^p$ and $w \in \mathbb{R}^q$. The exosystem state $w$ holds the references and the disturbances; $e$ is the error, for example $y - r$. The standard assumptions are:

- (H1) every eigenvalue of $S$ has real part $\ge 0$. Modes that decay on their own need no regulation, so this loses no generality.
- (H2) $(A, B)$ is [stabilizable](/stabilizability/).
- (H3), for error feedback only: the pair $\left(\begin{bmatrix} C & Q \end{bmatrix}, \begin{bmatrix} A & P \\ 0 & S \end{bmatrix}\right)$ is [detectable](/detectability/).

**Full information problem.** Find $K$ and $L$ such that, with $u = -K x + L w$:

1. (stability) $A - BK$ is [Hurwitz](/hurwitz-matrix/);
2. (regulation) $e(t) \to 0$ as $t \to \infty$ for every $x(0)$ and $w(0)$.

**Error feedback problem.** Find a controller $\dot \xi = F \xi + G e$, $u = H \xi$ such that the closed loop with $w = 0$ is internally stable, that is the matrix $\begin{bmatrix} A & BH \\ GC & F \end{bmatrix}$ is Hurwitz, and $e(t) \to 0$ for every initial state of plant, controller and exosystem.

**Solvability (Francis 1977).** Under (H1) and (H2), the full information problem is solvable if and only if there are matrices $\Pi \in \mathbb{R}^{n \times q}$ and $\Gamma \in \mathbb{R}^{m \times q}$ with

$$\Pi S = A \Pi + B \Gamma + P, \qquad 0 = C \Pi + Q.$$

Under (H1), (H2) and (H3) the same condition decides the error feedback problem. The proofs, the controllers, and the condition for solvability for all $P$ and $Q$, namely $\operatorname{rank} \begin{bmatrix} A - \lambda I & B \\ C & 0 \end{bmatrix} = n + p$ for every eigenvalue $\lambda$ of $S$, are on the [regulator equations](/regulator-equations/) page. The meaning of the equations: the subspace $x = \Pi w$ is invariant under the steady-state input $u = \Gamma w$, and on it the error is zero.

## Variants

- **Robust regulation.** Ask that regulation hold for all plants $(A, B, C, P, Q)$ in a neighbourhood of the nominal one, as long as the loop stays internally stable. This is the servomechanism problem of Davison (1976). Its solution uses error feedback with an internal model: $p$ copies of the minimal polynomial of $S$ in the controller (Francis and Wonham 1975). When the measured output is the error itself, a robust regulator exists if $(A, B)$ is stabilizable, $(C, A)$ is detectable, and the rank condition above holds at every eigenvalue of $S$; the rank condition needs $m \ge p$.
- **Structurally stable but not robust.** A full information controller $u = -Kx + (\Gamma + K\Pi) w$ regulates only the nominal plant. If $A$, $B$ or $C$ change, $\Pi$ and $\Gamma$ change, and the error has a nonzero steady state in general.
- **Tracking only or rejection only.** Tracking of $r = R w$ is the case $Q = -R$, $P = 0$. Rejection of a disturbance $d = D w$ at the input is $P = B D$, $Q = 0$.
- **Discrete time.** For $x_{k+1} = A x_k + B u_k + P w_k$, $w_{k+1} = S w_k$, the equations have the same form, and (H1) becomes: every eigenvalue of $S$ has modulus $\ge 1$.
- **Nonlinear output regulation (Isidori and Byrnes 1990).** For $\dot x = f(x, u, w)$, $\dot w = s(w)$, $e = h(x, w)$, the matrices $\Pi$ and $\Gamma$ become maps $\pi(w)$ and $c(w)$ that solve the partial differential equations $\frac{\partial \pi}{\partial w} s(w) = f(\pi(w), c(w), w)$ and $0 = h(\pi(w), w)$. Under their hypotheses, the local problem is solvable if and only if these equations have a solution near $w = 0$; the proof uses a center manifold.
- **Periodic signals of known period.** An exosystem for all signals with period $T$ has infinitely many modes $2\pi k i / T$. The internal model is then a delay loop, which is repetitive control.

## Examples

- **A sinusoidal reference for a first-order plant.** $\dot x = x + u$, $e = x - w_1$, with $\dot w_1 = w_2$, $\dot w_2 = -w_1$, so $S = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$, $P = 0$ and $Q = \begin{bmatrix} -1 & 0 \end{bmatrix}$. The second regulator equation gives $\Pi = \begin{bmatrix} 1 & 0 \end{bmatrix}$. The first gives $\Pi S = \begin{bmatrix} 0 & 1 \end{bmatrix} = \Pi + \Gamma$, so $\Gamma = \begin{bmatrix} -1 & 1 \end{bmatrix}$. With $K = 2$ the controller is $u = -2x + (\Gamma + K \Pi) w = -2x + w_1 + w_2$. Check: $z = x - w_1$ satisfies $\dot z = x + u - w_2 = -x + w_1 = -z$, so $e = z$ decays like $e^{-t}$. The rank condition holds at $\lambda = \pm i$, because $\det \begin{bmatrix} 1 - \lambda & 1 \\ 1 & 0 \end{bmatrix} = -1 \ne 0$.
- **A zero on the exosystem spectrum (non-example).** Let $G(s) = s / ((s + 1)(s + 2))$, with $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $C = \begin{bmatrix} 0 & 1 \end{bmatrix}$, and a constant reference: $S = 0$, $P = 0$, $Q = -1$. The equations are $0 = A \Pi + B \Gamma$ and $\pi_2 = 1$. The first row of $A\Pi + B\Gamma = 0$ says $\pi_2 = 0$. So there is no solution, and no controller tracks a step. The reason is the plant zero at $s = 0$, which equals the exosystem eigenvalue; the rank condition fails there, because rows 1 and 3 of $\begin{bmatrix} A & B \\ C & 0 \end{bmatrix}$ are equal. A plant that differentiates cannot hold a constant nonzero output with a bounded state.
- **Step references and integral action.** For $S = 0$ the equations become $\begin{bmatrix} A & B \\ C & 0 \end{bmatrix} \begin{bmatrix} \Pi \\ \Gamma \end{bmatrix} = -\begin{bmatrix} P \\ Q \end{bmatrix}$. They have a solution for every $P$, $Q$ exactly when this matrix has full row rank $n + p$, that is when the plant has no [transmission zero](/transmission-zero/) at 0 and $m \ge p$. The robust controller adds one integrator per error channel, which is [integral state feedback](/integral-state-feedback/).

## Known algorithms

- **Full information design.** Solve the regulator equations, choose $K$ with $A - BK$ Hurwitz by [pole placement](/pole-placement-theorem/) or LQR, and set $L = \Gamma + K \Pi$. The regulator equations are a linear system of $(n + p) q$ equations in $(n + m) q$ unknowns. Solved as one Kronecker system it costs $O((n + m)^3 q^3)$; with $S$ in real [Schur form](/schur-decomposition/) it splits into $q$ systems of size $n + p$ by $n + m$, one per column, for $O(q (n + m)^3 + q^3 + q^2 n)$ operations. See [Sylvester equation](/sylvester-equation/) for the same idea.
- **Observer-based error feedback.** Build an observer for the augmented state $(x, w)$ from $e$, which exists under (H3), and apply the full information law to the estimates. The controller has order $n + q$. It is not robust.
- **Internal model design.** Put $p$ copies of the minimal polynomial of $S$ in the controller (the servocompensator of Davison 1976), then stabilize the plant with this compensator by any method, for example LQR on the augmented state and an observer. The controller is robust in the sense of the variant above.

A problem without a cost has no optimal algorithm in the usual sense. What is proved is the criterion: Francis (1977) gives necessary and sufficient conditions, and every algorithm above finds a controller whenever one exists, in a finite number of linear algebra steps.

## Bounds

- **Order of the controller.** An error feedback regulator exists with order at most $n + q$, by the observer-based design. A robust regulator needs at least $p$ times the degree of the minimal polynomial of $S$ internal model states (the internal model principle, Francis and Wonham 1975); the internal model design attains this plus the order of a stabilizer.
- **Rate.** With the full information law, $z = x - \Pi w$ satisfies $\dot z = (A - BK) z$ and $e = C z$, so the error decays at the rate set by the eigenvalues of $A - BK$. This rate can be made arbitrarily fast when $(A, B)$ is controllable, at the price of large gains.
- **Necessity of the rank condition.** If $\operatorname{rank} \begin{bmatrix} A - \lambda I & B \\ C & 0 \end{bmatrix} < n + p$ for some eigenvalue $\lambda$ of $S$, there are $P$ and $Q$ for which the problem has no solution. This is a theorem, proved on the [regulator equations](/regulator-equations/) page.

## Reductions

- **To a linear equation and a stabilization problem.** By the theorem of Francis, the full information problem reduces to the regulator equations plus the choice of a stabilizing $K$.
- **To stabilization of an augmented plant.** The robust problem reduces, after the internal model is connected to the error, to the stabilization of the plant in series with the internal model. This plant is stabilizable exactly when (H2) and the rank condition hold.
- **From step tracking.** Integral action for constant references and disturbances is the case $S = 0$; the rank condition becomes the absence of a zero at the origin.
- **Compared with disturbance decoupling.** The [disturbance decoupling problem](/disturbance-decoupling-problem/) asks for zero effect of every disturbance signal. Output regulation asks only that the error decay, and only for exosystem signals. The second is much weaker and is solvable in many cases where the first is not.

## Applications

- **Servo systems.** Position and speed loops in machine tools, robots and drives track steps and ramps without steady-state error by integral action, the case $S = 0$ or a double integrator.
- **Rejection of periodic disturbances.** Disk drives reject the runout of a rotating disk, and helicopters and wind turbines reject vibrations at the rotor frequency, with internal models of known frequencies.
- **Power electronics.** Grid-connected converters track sinusoidal currents at the grid frequency with resonant controllers, which are internal models of $\pm i\omega$.
- **Active noise and vibration control.** Tonal noise at known frequencies is cancelled with internal models of those tones.
- **Nonlinear systems.** Isidori and Byrnes (1990) extended the problem to nonlinear plants, where it is used for tracking in aircraft and in robots.

## References
