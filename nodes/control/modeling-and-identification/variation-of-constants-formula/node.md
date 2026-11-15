---
tag: 8NKZ49
kind: theorem
slug: variation-of-constants-formula
name: Variation of constants formula
aliases:
- Lagrange formula for linear systems
- convolution solution of the state equation
area: control/modeling-and-identification
level: intro
summary: The state of x' = Ax + Bu is e^(At)x(0) plus the integral of e^(A(t-s))Bu(s), the free response plus the forced response.
prereqs: [matrix-exponential, state-space-representation]
see_also: [state-transition-matrix, zero-order-hold-discretization, impulse-response, convolution, transfer-function-matrix, controllability-gramian, gronwall-inequality, lyapunov-indirect-method]
sources:
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Chapter 4 (solution of the time-invariant and the time-varying state equations)
  - book: isbn:9780134412054
    title: Wilson J. Rugh, Linear System Theory, second edition, Prentice Hall, 1996
    locator: Chapter 3, State Equation Solution (the complete solution with an input, for time-varying systems)
  - book: isbn:9780691193984
    title: Karl J. Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: the chapter on linear systems (the matrix exponential and the convolution equation)
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 4.3, Linear Systems and Linearization (stability of x' = Ax through e^(At), and the linearization of a nonlinear system)
---

The variation of constants formula gives the solution of the linear state equation $\dot x = A x + B u$ in closed form: $x(t) = e^{A(t - t_0)} x(t_0) + \int_{t_0}^{t} e^{A(t - s)} B u(s)\, ds$. The first term is the free response to the initial state, and the second is the forced response to the input, a convolution of the input with $e^{At} B$. The formula holds for every locally integrable input, and with the [state-transition matrix](/state-transition-matrix/) $\Phi(t, s)$ in place of $e^{A(t - s)}$ it also holds for time-varying systems. Most results on linear systems start from it: the [impulse response](/impulse-response/), the transfer matrix, the [zero-order hold discretization](/zero-order-hold-discretization/) and the controllability gramian.

## Statement

**Theorem (time-invariant).** Let $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $C \in \mathbb{R}^{p \times n}$ and $D \in \mathbb{R}^{p \times m}$. Let $u : [t_0, \infty) \to \mathbb{R}^m$ be locally integrable, for example piecewise continuous. Then for every $x_0 \in \mathbb{R}^n$ the initial value problem

$$\dot x(t) = A x(t) + B u(t), \qquad x(t_0) = x_0$$

has exactly one solution in the sense of Carathéodory (an absolutely continuous $x$ that satisfies the equation for almost every $t$), and it is

$$x(t) = e^{A(t - t_0)} x_0 + \int_{t_0}^{t} e^{A(t - s)} B u(s)\, ds, \qquad t \ge t_0.$$

The output $y = C x + D u$ is

$$y(t) = C e^{A(t - t_0)} x_0 + \int_{t_0}^{t} C e^{A(t - s)} B u(s)\, ds + D u(t).$$

If $u$ is continuous, $x$ is $C^1$ and satisfies the equation at every $t$.

**Theorem (time-varying).** Let $A(\cdot)$ and $B(\cdot)$ be continuous on an interval $J$ that contains $t_0$, let $\Phi$ be the state-transition matrix of $\dot x = A(t) x$, and let $u$ be locally integrable on $J$. Then the unique solution of $\dot x = A(t) x + B(t) u$, $x(t_0) = x_0$, is

$$x(t) = \Phi(t, t_0) x_0 + \int_{t_0}^{t} \Phi(t, s) B(s) u(s)\, ds, \qquad t \in J.$$

**Discrete time.** For $x_{k+1} = A x_k + B u_k$, $x_k = A^k x_0 + \sum_{j=0}^{k-1} A^{k-1-j} B u_j$. This follows by induction on $k$.

## In plain words

A linear system responds to two things: where it starts and how it is pushed. Because the system is linear, these two effects simply add. The start fades or grows on its own, as the free motion of the system dictates. Each small push at an earlier moment also sets off its own free motion, which by now has run for the time since that push. The present state is the free motion from the start plus the sum of the free motions from all earlier pushes. The name comes from the method of proof: take the solution without input, and let its constants vary in time so that it also fits the input.

## Proof

*Time-invariant case.* Recall that $\frac{d}{dt} e^{-At} = -A e^{-At} = -e^{-At} A$, and that $e^{-At}$ is the inverse of $e^{At}$ (see [matrix exponential](/matrix-exponential/)).

**Existence.** Define $x(t)$ by the formula. Write it as $x(t) = e^{A(t - t_0)} c(t)$ with $c(t) = x_0 + \int_{t_0}^t e^{-A(s - t_0)} B u(s)\, ds$. This is the "variation of the constant" $c$: without the integral, $c = x_0$ and $x$ is the free solution. Since $u$ is locally integrable and $e^{-A(s - t_0)}$ is continuous, $c$ is absolutely continuous, and by the Lebesgue differentiation theorem $\dot c(t) = e^{-A(t - t_0)} B u(t)$ for almost every $t$. The product rule gives, for almost every $t$,

$$\dot x(t) = A e^{A(t - t_0)} c(t) + e^{A(t - t_0)} e^{-A(t - t_0)} B u(t) = A x(t) + B u(t),$$

and $x(t_0) = c(t_0) = x_0$. If $u$ is continuous, $c$ is $C^1$ by the fundamental theorem of calculus, and the equation holds at every $t$.

**Uniqueness.** Let $x$ be any Carathéodory solution and put $z(t) = e^{-A(t - t_0)} x(t)$. Then $z$ is absolutely continuous and, for almost every $t$,

$$\dot z = -A e^{-A(t - t_0)} x + e^{-A(t - t_0)} (A x + B u) = e^{-A(t - t_0)} B u(t),$$

because $A$ commutes with $e^{-A(t - t_0)}$. An absolutely continuous function is the integral of its derivative, so $z(t) = x_0 + \int_{t_0}^t e^{-A(s - t_0)} B u(s)\, ds$. Multiplying by $e^{A(t - t_0)}$ and using $e^{A(t - t_0)} e^{-A(s - t_0)} = e^{A(t - s)}$ gives the formula. So every solution equals it.

The output formula follows by substitution into $y = C x + D u$.

*Time-varying case.* The same two steps work with $\Phi(t, t_0)$ in place of $e^{A(t - t_0)}$. The needed facts are $\partial_t \Phi(t, t_0) = A(t) \Phi(t, t_0)$, $\partial_t \Phi(t_0, t) = -\Phi(t_0, t) A(t)$ and $\Phi(t, t_0) \Phi(t_0, s) = \Phi(t, s)$; they are on the [state-transition matrix](/state-transition-matrix/) page. With $z(t) = \Phi(t_0, t) x(t)$ one gets $\dot z = \Phi(t_0, t) B(t) u(t)$, and the rest is the same. $\square$

## Consequences

- **Superposition.** The free response is linear in $x_0$, and the forced response is linear in $u$. The response to $(x_0, u)$ is the sum of the response to $(x_0, 0)$ and to $(0, u)$. Each is a theorem, not an approximation.
- **Impulse response and transfer matrix.** With $x_0 = 0$ and $t_0 = 0$, $y = g * u$ with $g(t) = C e^{At} B$ for $t > 0$, plus the direct term $D u$. So the [impulse response](/impulse-response/) of the state model is $C e^{At} B + D \delta(t)$, and the forced response is a [convolution](/convolution/). The Laplace transform of $C e^{At} B + D \delta$ is $C (sI - A)^{-1} B + D$, the [transfer function matrix](/transfer-function-matrix/). The coefficients $C A^{k} B$ of its expansion are the [Markov parameters](/markov-parameters/).
- **Zero-order hold.** If $u$ is constant on $[kh, (k+1)h)$, the formula on one interval gives $x_{k+1} = e^{Ah} x_k + \int_0^h e^{As} ds\, B u_k$. This is the exact discrete model of [zero-order hold discretization](/zero-order-hold-discretization/).
- **Reachable states and the gramian.** From $x_0 = 0$, $x(T) = \int_0^T e^{A(T - s)} B u(s)\, ds$. The input $u(s) = B^T e^{A^T (T - s)} \eta$ gives $x(T) = W(T) \eta$ with $W(T) = \int_0^T e^{A\tau} B B^T e^{A^T \tau} d\tau$, the [controllability gramian](/controllability-gramian/). This is the start of the proof that $(A, B)$ is controllable if and only if $W(T)$ is invertible.
- **Bounds.** If $A$ is Hurwitz with $\|e^{At}\| \le c e^{-\alpha t}$, then $\|x(t)\| \le c e^{-\alpha (t - t_0)} \|x_0\| + \frac{c}{\alpha} \|B\| \sup_{s} \|u(s)\|$. So a bounded input gives a bounded state, and the effect of the initial state decays exponentially. This is the linear case of [input-to-state stability](/input-to-state-stability/).
- **Perturbed systems.** For $\dot x = A x + g(t, x)$, the formula with $B u$ replaced by $g(t, x(t))$ turns the equation into an integral equation, $x(t) = e^{A(t - t_0)} x_0 + \int_{t_0}^t e^{A(t - s)} g(s, x(s))\, ds$. With the [Grönwall inequality](/gronwall-inequality/) this gives the proof of [Lyapunov's indirect method](/lyapunov-indirect-method/) when $\|g(t, x)\| \le \gamma \|x\|$ for small $\|x\|$ and $\gamma$ is small enough. It is also the starting point of [exponential integrators](/exponential-integrators/) in numerical analysis.
- **Step response.** For $u(t) = \bar u$ constant and invertible $A$, $x(t) = e^{At} x_0 + A^{-1}(e^{At} - I) B \bar u$. For a Hurwitz $A$ this tends to $-A^{-1} B \bar u$, and the static gain is $-C A^{-1} B + D$.

**Example.** Take the scalar system $\dot x = -x + u$ with $x(0) = 2$ and $u(t) = 1$. The formula gives $x(t) = 2 e^{-t} + \int_0^t e^{-(t - s)} ds = 2 e^{-t} + 1 - e^{-t} = 1 + e^{-t}$. Check: $\dot x = -e^{-t}$ and $-x + u = -1 - e^{-t} + 1 = -e^{-t}$. At $t = 1$, $x = 1.3679$: the free response $2e^{-1} = 0.7358$ plus the forced response $1 - e^{-1} = 0.6321$.

## Tightness

- **Linearity is needed.** For a nonlinear $\dot x = f(x) + B u$ the free and forced responses do not add, and the integral form above is an equation in $x$, not a formula. For $\dot x = -x^3 + u$ with $x(0) = 1$ and $u = 1$, the solution stays at $x = 1$. The free response from $x(0) = 1$ with $u = 0$ is $1/\sqrt{1 + 2t}$, which is $0.5774$ at $t = 1$. The forced response from $x(0) = 0$ with $u = 1$ is $0.8230$ at $t = 1$ (RK4 with step 0.001). Their sum is $1.4004$, not 1.
- **The input must be locally integrable.** For $\dot x = u$ with $u(t) = 1/t$ on $(0, 1]$ and $x(0) = 0$, the integral $\int_0^t ds/s$ diverges, and no solution starts at $t = 0$. The formula has no meaning there, and none is expected.
- **The time-varying formula needs $\Phi$.** Replacing $\Phi(t, s)$ by $\exp(\int_s^t A(\sigma) d\sigma)$ is wrong unless $A(t)$ commutes with its integrals; the state-transition matrix page gives a $2 \times 2$ counterexample.
- **Impulses.** If $u$ contains a Dirac impulse $\delta(t - t_0)$, the solution jumps at $t_0$ by $B$ times the weight. The formula still holds if the integral starts at $t_0^-$, which is the 0- convention of the [Laplace transform](/laplace-transform/) pages.

## History

The method of variation of constants comes from celestial mechanics. Euler used the idea in his 1748 study of the mutual perturbation of Jupiter and Saturn, where the constants of a two-body orbit are allowed to change in time. Lagrange developed it in memoirs from the 1770s to 1810 into a general method for the variation of arbitrary constants, and in this way it became a standard method for linear differential equations with a forcing term. The matrix form with $e^{At}$ entered control with the state-space methods of Kalman and others around 1960, and it is the basic formula of the linear system theory books by Chen and by Rugh.

## References
