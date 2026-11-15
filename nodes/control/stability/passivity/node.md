---
tag: P9JMQ6
kind: definition
slug: passivity
name: Passivity
aliases:
- passive system
area: control/stability
level: core
summary: A system is passive if it cannot produce energy. The energy it gives out is at most the energy supplied through the product of input and output plus the energy stored at the start.
prereqs: [lyapunov-function, transfer-function]
see_also: [dissipativity, passivity-theorem, kalman-yakubovich-popov-lemma, passivity-based-control, port-hamiltonian-system, ida-pbc, prima, bounded-real-lemma]
sources:
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 6.1 (passive memoryless functions), Section 6.2 (passivity of state models and the strict forms), Section 6.3 (positive real transfer functions) and Section 6.4 (L2 and Lyapunov stability of passive systems)
  - paper: doi:10.1007/BF00276493
    title: Jan C. Willems, Dissipative dynamical systems, Part I, General theory, Archive for Rational Mechanics and Analysis 45(5), 321-351, 1972
    locator: the storage function and the dissipation inequality, with passivity as the case of the supply rate u^T y
  - paper: doi:10.1002/sapm1931101191
    title: Otto Brune, Synthesis of a finite two-terminal network whose driving-point impedance is a prescribed function of frequency, Journal of Mathematics and Physics 10, 191-236, 1931
    locator: the positive real condition on the impedance of a network of resistors, inductors, capacitors and transformers
  - book: isbn:9780898716702
    title: "Charles A. Desoer and M. Vidyasagar, Feedback Systems: Input-Output Properties, SIAM Classics in Applied Mathematics, 2009 (reprint of the Academic Press edition of 1975)"
    locator: Chapter 6 (passivity of input-output maps)
---

A passive system cannot produce energy. Over any time interval, the energy that it gives out is at most the energy that came in through its inputs plus the energy that it held at the start. An electric network of resistors, inductors, capacitors and transformers is passive: with the port currents as inputs and the port voltages as outputs, the product of input and output is the power into the network, and the stored energy is the energy in the inductors and the capacitors. Model reduction methods for such networks, such as [PRIMA](/prima/), keep this property, because a reduced model that is not passive can give out energy, and a simulation that connects it to other passive parts can grow without bound. This page defines passivity for state models, for input-output maps and for transfer functions, where it is called positive realness. [Dissipativity](/dissipativity/) is the general notion with any supply rate, and passivity is one case of it. The [passivity theorem](/passivity-theorem/) is about feedback loops of two passive systems. [Passivity-based control](/passivity-based-control/), [port-Hamiltonian systems](/port-hamiltonian-system/) and [IDA-PBC](/ida-pbc/) are a design method, a model class and a design procedure that use the property.

## Definition

**Setting.** A state model $\dot x = f(x, u)$, $y = h(x, u)$, with state $x \in \mathbb{R}^n$, and input $u$ and output $y$ of the same size, $u, y \in \mathbb{R}^m$. The map $f$ is locally Lipschitz (see [Lipschitz condition](/lipschitz-condition/)), $h$ is continuous, and $f(0, 0) = 0$, $h(0, 0) = 0$. The product $u^T y$ is the supply rate: the power that goes into the system.

**Definition (passive).** The system is passive if there is a continuously differentiable function $V : \mathbb{R}^n \to \mathbb{R}$ with $V(x) \ge 0$ for all $x$, called a storage function, such that

$$u^T y \ \ge\ \dot V = \frac{\partial V}{\partial x}(x)\, f(x, u) \qquad \text{for all } (x, u) \in \mathbb{R}^n \times \mathbb{R}^m.$$

Integration along a solution gives the dissipation inequality

$$V(x(t)) - V(x(0)) \ \le\ \int_0^t u(s)^T y(s)\, ds \qquad \text{for all inputs, all } x(0) \text{ and all } t \ge 0.$$

The stored energy can increase only by the energy that was supplied. The integral form does not need $V$ to be differentiable, and Willems (1972) uses it as the definition; see [dissipativity](/dissipativity/).

**Strict forms.** Let $V$ be a storage function as above. The system is
- *lossless* if $u^T y = \dot V$;
- *input strictly passive* if $u^T y \ge \dot V + u^T \varphi(u)$ with $u^T \varphi(u) > 0$ for every $u \ne 0$, usually $\varphi(u) = \varepsilon u$ with $\varepsilon > 0$;
- *output strictly passive* if $u^T y \ge \dot V + y^T \rho(y)$ with $y^T \rho(y) > 0$ for every $y \ne 0$, usually $\rho(y) = \delta y$ with $\delta > 0$;
- *strictly passive* if $u^T y \ge \dot V + \psi(x)$ with $\psi$ positive definite.

These are the definitions of Khalil (2002, Section 6.2). The words differ between books: some write "strictly passive" for what is "input strictly passive" here. Say which one is meant.

**Memoryless maps.** A static map $y = h(t, u)$ is passive if $u^T h(t, u) \ge 0$ for all $t$ and $u$. For $m = 1$ this says that the graph of $h(t, \cdot)$ lies in the first and third quadrants, that is, $h$ is in the sector $[0, \infty]$ of the [Lur'e problem](/lure-problem/).

**Input-output maps.** Let $L_{2e}$ be the signals on $[0, \infty)$ whose restriction to every $[0, T]$ has finite energy, and write $\langle u, y \rangle_T = \int_0^T u^T y\, dt$. A causal map $H : L_{2e}^m \to L_{2e}^m$ is passive if there is a constant $\beta \ge 0$ with $\langle u, Hu \rangle_T \ge -\beta$ for every $u$ and every $T \ge 0$. It is input strictly passive if $\langle u, Hu \rangle_T \ge \varepsilon \langle u, u \rangle_T - \beta$, and output strictly passive if $\langle u, Hu \rangle_T \ge \delta \langle Hu, Hu \rangle_T - \beta$, with $\varepsilon, \delta > 0$. The constant $\beta$ is the energy that the system can give at the start; for a state model it is $V(x(0))$.

**Transfer functions.** An $m \times m$ proper rational [transfer function](/transfer-function/) $G(s)$ is *positive real* if
1. no element of $G$ has a pole with $\operatorname{Re} s > 0$;
2. $G(j\omega) + G(j\omega)^* \ge 0$ for every real $\omega$ where $j\omega$ is not a pole of an element of $G$;
3. every pole $j\omega_0$ on the imaginary axis is simple, and the residue matrix $\lim_{s \to j\omega_0} (s - j\omega_0) G(s)$ is Hermitian and positive semidefinite.

$G$ is *strictly positive real* if $G(s - \varepsilon)$ is positive real for some $\varepsilon > 0$. A minimal realization $\dot x = Ax + Bu$, $y = Cx + Du$ of $G$ is passive with the quadratic storage $V(x) = \frac{1}{2} x^T P x$, $P > 0$, if and only if $G$ is positive real. This is the positive real case of the [Kalman-Yakubovich-Popov lemma](/kalman-yakubovich-popov-lemma/), which turns the frequency condition into a matrix inequality for $P$. For $m = 1$ and $G$ with all poles in $\operatorname{Re} s < 0$, the test is short: $G$ is positive real if and only if $\operatorname{Re} G(j\omega) \ge 0$ for every $\omega$, so the Nyquist plot stays in the closed right half plane. The phase of a positive real $G$ stays in $[-90°, 90°]$, so its relative degree is $0$ or $1$.

**Two properties used on other pages.**
- *Zero input.* If the storage $V$ is positive definite, then with $u = 0$ we get $\dot V \le 0$, so $V$ is a [Lyapunov function](/lyapunov-function/) and the origin of $\dot x = f(x, 0)$ is Lyapunov stable.
- *L2 gain.* If the system is output strictly passive with $\rho(y) = \delta y$, then it has L2 gain at most $1/\delta$. From $\delta |y|^2 \le u^T y - \dot V$ and $u^T y \le \frac{1}{2\delta}|u|^2 + \frac{\delta}{2}|y|^2$ we get $\frac{\delta}{2}|y|^2 \le \frac{1}{2\delta}|u|^2 - \dot V$. Integrate over $[0, T]$ and use $V \ge 0$: $\int_0^T |y|^2 \le \frac{1}{\delta^2} \int_0^T |u|^2 + \frac{2}{\delta} V(x(0))$, so $\|y\|_{L_2[0,T]} \le \frac{1}{\delta} \|u\|_{L_2[0,T]} + \sqrt{2 V(x(0)) / \delta}$.

## Examples and non-examples

- **Integrator.** $\dot x = u$, $y = x$, $V = \frac{1}{2}x^2$: $\dot V = xu = uy$, so the integrator is lossless. Its transfer function $1/s$ is positive real: the pole at $0$ is simple with residue $1$.
- **Series RLC circuit.** A voltage source $u$ drives a resistor $R$, an inductor $L$ and a capacitor $C$ in series, and the output is the current $i$. The equations are $L \dot i = u - R i - v_C$ and $C \dot v_C = i$. With the stored energy $V = \frac{1}{2} L i^2 + \frac{1}{2} C v_C^2$, $\dot V = i(u - Ri - v_C) + v_C i = ui - R i^2$. The circuit is output strictly passive with $\delta = R$ (resistance in ohms), so its L2 gain from volts to amperes is at most $1/R$. With $R = 0$ it is lossless. A mass, spring and damper driven by a force, with the velocity as output, has the same equations.
- **First-order lag.** $\dot x = -x + u$, $y = x$ (time constant 1 s), $V = \frac{1}{2}x^2$: $\dot V = uy - y^2$. It is output strictly passive with $\delta = 1$, so its L2 gain is at most $1$. This bound is exact, because the [H-infinity norm](/h-infinity-norm/) of $G(s) = 1/(s + 1)$ is $1$. Also $\operatorname{Re} G(j\omega) = 1/(1 + \omega^2) > 0$, and $G$ is strictly positive real.
- **Resistor and saturation.** The resistor $y = R u$ with $R > 0$ is input strictly passive with $\varepsilon = R$. The saturation $y = \operatorname{sat}(u)$ is passive, because $u \operatorname{sat}(u) \ge 0$. It is not input strictly passive: for $|u| > 1/\varepsilon$, $u \operatorname{sat}(u) = |u| < \varepsilon u^2$.
- **Non-example, relative degree 2.** $G(s) = 1/(s+1)^2$ has $\operatorname{Re} G(j\omega) = (1 - \omega^2)/(1 + \omega^2)^2$, which is negative for $\omega > 1$. At $\omega = 2$ rad/s it is $-3/25$. From the zero state, the input $u = \sin 2t$ gives in steady state an average power $\frac{1}{2}\operatorname{Re} G(2j) = -0.06$, so $\int_0^T u y\, dt$ goes to $-\infty$ as $T$ grows. No storage function can satisfy the dissipation inequality, so no realization of $G$ is passive. The same holds for the mass and spring with the position as output.
- **Non-example, an unstable lag.** $\dot x = x + u$, $y = x$. With the feedback $u = -kx$, $k > 1$, the state is $x(t) = x(0) e^{(1-k)t}$ and the energy taken out is $\int_0^\infty (-u y)\, dt = \frac{k\, x(0)^2}{2(k - 1)}$. This grows without bound as $k$ goes down to $1$. A storage function would have to be at least this large at $x(0)$, so none exists. Also $1/(s - 1)$ has a pole in the right half plane and is not positive real.
- **Non-example, a time delay.** $y(t) = u(t - \tau)$, with zero input before $t = 0$. The input $u(t) = \sin(\pi t / \tau)$ gives $y(t) = -u(t)$ for $t \ge \tau$, so $\langle u, y \rangle_T$ decreases like $-T/2$. The delay is not passive, although it keeps the energy of the signal.

## Related definitions

- [Dissipativity](/dissipativity/): the same inequality with a general supply rate $w(u, y)$. Passivity is $w = u^T y$, and finite L2 gain $\gamma$ is $w = \gamma^2 |u|^2 - |y|^2$.
- [Passivity theorem](/passivity-theorem/): the negative feedback loop of two passive systems is passive, and strict forms give finite L2 gain or asymptotic stability.
- [Kalman-Yakubovich-Popov lemma](/kalman-yakubovich-popov-lemma/): the equivalence of positive realness and a linear matrix inequality for a quadratic storage.
- [Bounded real lemma](/bounded-real-lemma/): the matching result for the L2 gain.
- [Passivity-based control](/passivity-based-control/), [port-Hamiltonian system](/port-hamiltonian-system/) and [IDA-PBC](/ida-pbc/): design with a storage function as the Lyapunov function.
- [PRIMA](/prima/) and [Padé via Lanczos](/pade-via-lanczos/): reduction of large RLC models. PRIMA keeps passivity by a congruence projection; the Padé via Lanczos method does not guarantee it.

## References
