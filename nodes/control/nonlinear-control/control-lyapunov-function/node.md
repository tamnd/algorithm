---
tag: DTH5R0
kind: definition
slug: control-lyapunov-function
name: Control Lyapunov function
aliases:
- CLF
area: control/nonlinear-control
level: core
summary: A positive definite function whose derivative some input can make negative at each nonzero state.
prereqs: [lyapunov-function, control-affine-system, lie-derivative]
see_also: [sontag-universal-formula, artstein-sontag-theorem, backstepping, control-barrier-function, lyapunov-direct-method, converse-lyapunov-theorem, input-to-state-stability, brockett-condition]
sources:
  - book: isbn:9780387984896
    title: Eduardo D. Sontag, Mathematical Control Theory, second edition, Springer, 1998
    locator: Section 5.7 (Lyapunov and control-Lyapunov functions) and Section 5.9 (introduction to nonlinear stabilization, with the universal formula)
  - book: isbn:9780471127321
    title: Miroslav Krstić, Ioannis Kanellakopoulos and Petar Kokotović, Nonlinear and Adaptive Control Design, Wiley, 1995
    locator: Section 2.1.2, control Lyapunov functions
  - paper: doi:10.1016/0362-546X(83)90049-4
    title: "Zvi Artstein, Stabilization with relaxed controls, Nonlinear Analysis: Theory, Methods and Applications 7(11), 1163-1173, 1983"
    locator: the equivalence between a smooth control Lyapunov function and stabilization by a feedback that is regular away from the origin
  - paper: doi:10.1016/0167-6911(89)90028-5
    title: "Eduardo D. Sontag, A 'universal' construction of Artstein's theorem on nonlinear stabilization, Systems and Control Letters 13(2), 117-123, 1989"
    locator: the small control property and the explicit feedback
  - paper: "Eduardo D. Sontag, A Lyapunov-like characterization of asymptotic controllability, SIAM Journal on Control and Optimization 21(3), 462-471, 1983"
    title: A Lyapunov-like characterization of asymptotic controllability
    locator: asymptotic controllability and the existence of a continuous control Lyapunov function
---

A control Lyapunov function (CLF) for a system with an input is a [Lyapunov function](/lyapunov-function/) candidate whose derivative some input can make negative at every state other than the equilibrium. A Lyapunov function proves that a system without an input has an asymptotically stable equilibrium. A CLF proves that the input can be chosen to get one. For a [control-affine system](/control-affine-system/) $\dot x = f(x) + g(x) u$, the condition is that $L_g V(x) = 0$ forces $L_f V(x) < 0$, a test at each state that does not involve a search over inputs. By [Artstein's theorem](/artstein-sontag-theorem/), a smooth CLF exists exactly when the system can be made globally asymptotically stable by a feedback that is smooth away from the origin, and [Sontag's universal formula](/sontag-universal-formula/) builds such a feedback from the CLF. [Backstepping](/backstepping/) is a method that constructs a CLF for systems with a special structure.

## Definition

**Setting.** The system is $\dot x = f(x) + g(x) u$ with state $x \in \mathbb{R}^n$, input $u \in \mathbb{R}^m$, smooth $f : \mathbb{R}^n \to \mathbb{R}^n$ and $g : \mathbb{R}^n \to \mathbb{R}^{n \times m}$, and $f(0) = 0$, so the origin is an equilibrium for $u = 0$. Smooth means $C^\infty$; continuously differentiable is enough for most of what follows. For a function $V$, the [Lie derivatives](/lie-derivative/) are $L_f V(x) = \nabla V(x)^T f(x)$ (a number) and $L_g V(x) = \nabla V(x)^T g(x)$ (a row of $m$ numbers). Along a solution with input $u$, $\dot V = L_f V(x) + L_g V(x)\, u$.

**Definition.** A continuously differentiable function $V : \mathbb{R}^n \to \mathbb{R}$ is a (global) control Lyapunov function if

1. $V$ is positive definite: $V(0) = 0$ and $V(x) > 0$ for $x \neq 0$;
2. $V$ is proper (radially unbounded): $V(x) \to \infty$ as $|x| \to \infty$;
3. for every $x \neq 0$ there is an input $u$ with $L_f V(x) + L_g V(x)\, u < 0$.

With unconstrained inputs, condition 3 is equivalent to

$$L_g V(x) = 0, \ x \neq 0 \quad \Longrightarrow \quad L_f V(x) < 0,$$

because if $L_g V(x) \neq 0$, the input $u = -s\, L_g V(x)^T$ with a large $s > 0$ makes the sum negative. So the condition only constrains $L_f V$ on the set where the input has no effect on $\dot V$.

**Small control property.** A CLF has the small control property if for every $\varepsilon > 0$ there is $\delta > 0$ such that every $x$ with $0 < |x| < \delta$ has an input $u$ with $|u| < \varepsilon$ and $L_f V(x) + L_g V(x)\, u < 0$. In words: near the origin, small inputs are enough. This is the condition that makes the feedback of Artstein's theorem continuous at the origin.

**Variants of the definition.**

- *Local CLF:* conditions 1 and 3 hold on a neighborhood of the origin, and condition 2 is dropped. It gives local results.
- *Bounded inputs:* in condition 3, $u$ is restricted to a set $U$. Then the test with $L_g V = 0$ no longer suffices.
- *General systems:* for $\dot x = F(x, u)$ the condition is $\inf_u \nabla V(x)^T F(x, u) < 0$ for $x \neq 0$. For systems that are not control-affine, the set of good inputs need not be convex, and Artstein's theorem uses relaxed controls.
- *Nonsmooth CLF:* Sontag (1983) showed that asymptotic controllability is equivalent to the existence of a continuous CLF in a sense with directional derivatives. A smooth CLF does not always exist; see the Brockett example below.

## Examples and non-examples

**Scalar system.** For $\dot x = x + u$ and $V = x^2 / 2$, $L_f V = x^2$ and $L_g V = x$. $L_g V = 0$ only at $x = 0$, so $V$ is a CLF. It has the small control property: at $x \neq 0$ the input $u = -2x$ gives $\dot V = -x^2 < 0$ and $|u| = 2|x|$. Sontag's formula gives $u = -(1 + \sqrt 2) x$ and the closed loop $\dot x = -\sqrt 2\, x$.

**Double integrator with the LQR weight.** For $\dot x_1 = x_2$, $\dot x_2 = u$, take $V = x^T P x$ with $P = \begin{bmatrix} \sqrt 3 & 1 \\ 1 & \sqrt 3 \end{bmatrix}$, the solution of the [Riccati equation](/continuous-algebraic-riccati-equation/) for $Q = I$, $R = 1$. Then $L_g V = 2 (x_1 + \sqrt 3 x_2)$ and $L_f V = 2 (\sqrt 3 x_1 + x_2) x_2$. On the line $L_g V = 0$, $x_1 = -\sqrt 3 x_2$, so $L_f V = 2(-3 + 1) x_2^2 = -4 x_2^2$, which is negative unless $x_2 = 0$, and then $x = 0$. So $V$ is a CLF. Every quadratic Lyapunov function of a stabilized linear system is a CLF in the same way.

**Non-example: the wrong function for a good system.** For the same double integrator, $V = \frac12 (x_1^2 + x_2^2)$ is positive definite and proper, but $L_g V = x_2$ and $L_f V = x_1 x_2$. On the line $x_2 = 0$ with $x_1 \neq 0$, $L_g V = 0$ and $L_f V = 0$, which is not negative. So $V$ is not a CLF, although the system is stabilizable. Whether a function is a CLF depends on the function, not only on the system.

**Non-example: a system with no CLF.** For $\dot x_1 = x_1$, $\dot x_2 = u$, no CLF exists. Suppose $V$ were one. Artstein's theorem gives a feedback $k$, smooth on $\mathbb{R}^2 \setminus \{0\}$, with $\dot V < 0$ along the closed loop away from the origin. Take $x(0) = (1, 0)$. The solution stays in the compact set $\{V \le V(x(0))\}$, because $V$ decreases and $V$ is proper. But $x_1(t) = e^t$ for every input. This is a contradiction. The unstable mode $x_1$ is not affected by the input.

**A CLF without the small control property.** For $\dot x = x + x^2 u$ and $V = x^2 / 2$, $L_f V = x^2$ and $L_g V = x^3$, which is nonzero for $x \neq 0$, so $V$ is a CLF. But $\dot V < 0$ needs $x^2 (1 + x u) < 0$, that is $|u| > 1 / |x|$ with the sign opposite to $x$. Near the origin the input must be large, so the small control property fails. In fact no feedback that is continuous at 0 makes the origin asymptotically stable: such a feedback would need $x (1 + x k(x)) < 0$ near 0, hence $|k(x)| > 1 / |x|$.

**Brockett's example.** The nonholonomic integrator $\dot x_1 = u_1$, $\dot x_2 = u_2$, $\dot x_3 = x_1 u_2 - x_2 u_1$ fails [Brockett's condition](/brockett-condition/), so no continuous feedback makes the origin asymptotically stable. By Artstein's theorem, it has no smooth CLF with the small control property. It is asymptotically controllable, so by Sontag (1983) it has a continuous, nonsmooth CLF.

## Related definitions

- **[Lyapunov function](/lyapunov-function/).** The special case without an input, or with a fixed feedback. If $V$ is a CLF and $k$ a feedback with $L_f V + L_g V\, k < 0$ away from 0, then $V$ is a Lyapunov function of the closed loop, and the [direct method](/lyapunov-direct-method/) gives asymptotic stability.
- **[Artstein's theorem](/artstein-sontag-theorem/).** A smooth CLF exists if and only if a feedback smooth away from the origin gives global asymptotic stability; with the small control property, the feedback is also continuous at the origin.
- **[Sontag's universal formula](/sontag-universal-formula/).** An explicit feedback built from $L_f V$ and $L_g V$.
- **[Converse Lyapunov theorems](/converse-lyapunov-theorem/).** For a closed loop that is asymptotically stable with a smooth feedback, the converse theorem gives a Lyapunov function, which is then a CLF of the open loop.
- **[Control barrier function](/control-barrier-function/).** The same idea for safety: some input keeps a function from falling too fast near the boundary of a safe set. A CLF and a CBF are often combined in one quadratic program.
- **ISS-CLF and robust CLF.** Versions with a disturbance input give [input-to-state stability](/input-to-state-stability/) or robustness to bounded uncertainty (Freeman and Kokotović 1996 relate robust CLFs to inverse optimality).
- **Small control property.** Defined above. It is a property of the pair $(V, \text{system})$, not of the system alone.

## References
