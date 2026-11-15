---
tag: W3MV92
kind: definition
slug: dissipativity
name: Dissipativity
aliases:
- dissipative system
- Willems dissipativity
area: control/stability
level: advanced
summary: A system is dissipative for a supply rate if a nonnegative storage function exists whose increase over any interval is at most the integral of the supply over that interval.
prereqs: [passivity]
see_also: [passivity, passivity-theorem, small-gain-theorem, kalman-yakubovich-popov-lemma, bounded-real-lemma, port-hamiltonian-system, passivity-based-control, linear-matrix-inequality]
sources:
  - paper: doi:10.1007/BF00276493
    title: Jan C. Willems, Dissipative dynamical systems, Part I, General theory, Archive for Rational Mechanics and Analysis 45(5), 321-351, 1972
    locator: the definition with a supply rate and a storage function, the available storage and the required supply, and the convex set of storage functions
  - paper: doi:10.1007/BF00276494
    title: Jan C. Willems, Dissipative dynamical systems, Part II, Linear systems with quadratic supply rates, Archive for Rational Mechanics and Analysis 45(5), 352-393, 1972
    locator: quadratic storage functions of linear systems, the frequency domain condition and the extreme solutions of the Riccati inequality
  - paper: doi:10.1109/TAC.1976.1101352
    title: David J. Hill and Peter J. Moylan, The stability of nonlinear dissipative systems, IEEE Transactions on Automatic Control 21(5), 708-711, 1976
    locator: the quadratic (Q, S, R) supply rates and the stability of dissipative systems
  - paper: doi:10.1016/0016-0032(80)90026-5
    title: "David J. Hill and Peter J. Moylan, Dissipative dynamical systems: Basic input-output and state properties, Journal of the Franklin Institute 309(5), 327-357, 1980"
    locator: input-output and state properties of dissipative systems
  - book: isbn:9783319499918
    title: Arjan van der Schaft, L2-Gain and Passivity Techniques in Nonlinear Control, third edition, Springer, 2017
    locator: Chapter 3 (dissipative systems theory)
---

Dissipativity is the general form of [passivity](/passivity/). A system comes with a supply rate $w(u, y)$, a function of the input and the output that measures what goes into the system per unit time. The system is dissipative if some nonnegative storage function can never grow by more than the supply that came in. Passivity is the case $w = u^T y$, and a finite L2 gain $\gamma$ is the case $w = \gamma^2 |u|^2 - |y|^2$, so one theory covers both. The [passivity theorem](/passivity-theorem/) and the [small-gain theorem](/small-gain-theorem/) are both instances of one rule for feedback loops of dissipative systems, given below. [Passivity-based control](/passivity-based-control/), [port-Hamiltonian systems](/port-hamiltonian-system/) and [IDA-PBC](/ida-pbc/) use the case $w = u^T y$ for design, with a physical energy as the storage.

## Definition

**Setting.** A state model $\dot x = f(x, u)$, $y = h(x, u)$ with $x \in \mathbb{R}^n$, $u \in \mathbb{R}^m$ and $y \in \mathbb{R}^p$; the sizes $m$ and $p$ can differ. The map $f$ is locally Lipschitz, $h$ is continuous, and solutions exist for the inputs considered. A supply rate is a function $w : \mathbb{R}^m \times \mathbb{R}^p \to \mathbb{R}$ such that $w(u(t), y(t))$ is locally integrable along every solution.

**Definition (Willems 1972).** The system is dissipative with respect to $w$ if there is a function $S : \mathbb{R}^n \to [0, \infty)$, the storage function, such that for every initial state, every input and every $t_0 \le t_1$,

$$S(x(t_1)) \ \le\ S(x(t_0)) + \int_{t_0}^{t_1} w(u(t), y(t))\, dt.$$

This is the dissipation inequality. If $S$ is continuously differentiable, it is the same as the pointwise inequality $\frac{\partial S}{\partial x}(x)\, f(x, u) \le w(u, h(x, u))$ for all $x$ and $u$. The system is lossless if equality holds.

**Available storage.** For a state $x$, let

$$S_a(x) = \sup_{u,\ T \ge 0} \left( -\int_0^T w(u(t), y(t))\, dt \right), \qquad x(0) = x.$$

It is the most energy that can be taken out of the system from the state $x$. Willems proved: the system is dissipative if and only if $S_a(x) < \infty$ for every $x$. Then $S_a$ is itself a storage function, and it is the smallest one: $S_a \le S$ for every storage $S$. The bound follows from the dissipation inequality, which gives $-\int_0^T w\, dt \le S(x) - S(x(T)) \le S(x)$.

**Required supply.** If every state can be reached from $0$, let $S_r(x)$ be the infimum of $\int_{-T}^0 w\, dt$ over all $T \ge 0$ and all inputs that move the state from $x(-T) = 0$ to $x(0) = x$. If the system is dissipative and $S_a(0) = 0$, then $S_r$ is a storage function, and every storage $S$ with $S(0) = 0$ lies between the two: $S_a \le S \le S_r$. The storage functions form a convex set.

**Common supply rates.**
- Passivity: $w = u^T y$, with $m = p$. See [passivity](/passivity/).
- Output strict passivity: $w = u^T y - \delta |y|^2$ with $\delta > 0$.
- L2 gain at most $\gamma$: $w = \gamma^2 |u|^2 - |y|^2$. Dissipativity gives $\int_0^T |y|^2 \le \gamma^2 \int_0^T |u|^2 + S(x(0))$ for every $T$.
- $(Q, S, R)$ supply rates (Hill and Moylan 1976): $w = y^T Q y + 2 y^T S u + u^T R u$ with symmetric $Q$ and $R$. The three rates above are cases of it. For a scalar static map, the sector $[a, b]$ condition is $w = (y - a u)(b u - y) \ge 0$ with zero storage.
- Linear systems with quadratic supply rates (Willems 1972, Part II): for $\dot x = Ax + Bu$ and a quadratic $w$, dissipativity with a quadratic storage $x^T P x$ is a [linear matrix inequality](/linear-matrix-inequality/) in $P$. The [Kalman-Yakubovich-Popov lemma](/kalman-yakubovich-popov-lemma/) links it to a frequency condition, and the [bounded real lemma](/bounded-real-lemma/) is the case of the L2 gain.

**Feedback loops.** Connect two systems with $u_1 = -y_2$ and $u_2 = y_1$, where system $i$ is dissipative with supply $w_i$ and storage $S_i$. If there are $\alpha_1, \alpha_2 > 0$ with $\alpha_1 w_1(-y_2, y_1) + \alpha_2 w_2(y_1, y_2) \le 0$ for all $y_1, y_2$, then $\alpha_1 S_1 + \alpha_2 S_2$ does not increase along the solutions of the loop, and it is a candidate [Lyapunov function](/lyapunov-function/).
- With $w_i = u_i^T y_i$: $w_1 + w_2 = -y_1^T y_2 + y_2^T y_1 = 0$. This is the first part of the [passivity theorem](/passivity-theorem/).
- With $w_i = \gamma_i^2 |u_i|^2 - |y_i|^2$: $w_1 + \alpha w_2 = (\alpha \gamma_2^2 - 1)|y_1|^2 + (\gamma_1^2 - \alpha)|y_2|^2$. A number $\alpha$ with $\gamma_1^2 < \alpha < 1/\gamma_2^2$ exists if and only if $\gamma_1 \gamma_2 < 1$, and then the sum is negative definite. This is the [small-gain theorem](/small-gain-theorem/) in its state form.

## Examples and non-examples

- **A first-order lag with the L2 gain supply.** Take $\dot x = -x + u$, $y = x$ and $w = \gamma^2 u^2 - y^2$. A quadratic storage $S = p x^2$ works if and only if $2p x(-x + u) \le \gamma^2 u^2 - x^2$ for all $x, u$, that is, if and only if
  $$\begin{bmatrix} 1 - 2p & p \\ p & -\gamma^2 \end{bmatrix} \le 0.$$
  This needs $p \ge 1/2$ and $p^2 - 2\gamma^2 p + \gamma^2 \le 0$, so $p \in [\gamma^2 - \gamma\sqrt{\gamma^2 - 1},\ \gamma^2 + \gamma\sqrt{\gamma^2 - 1}]$. There is a solution exactly when $\gamma \ge 1$, so the L2 gain is $1$, which is the [H-infinity norm](/h-infinity-norm/) of $1/(s + 1)$. For $\gamma = 1$ the only quadratic storage is $p = 1$. For $\gamma = 2$ the interval is $[4 - 2\sqrt 3,\ 4 + 2\sqrt 3] = [0.53590,\ 7.46410]$, the roots of $p^2 - 8p + 4 = 0$. The left end is the available storage $S_a = (4 - 2\sqrt 3) x^2$ and the right end is the required supply $S_r = (4 + 2\sqrt 3) x^2$; the minimum of $\int_0^\infty (4u^2 - x^2)\, dt$ is $\pi x(0)^2$ with $\pi^2 + 8\pi + 4 = 0$, and the two ends are $-\pi$ for the two roots $\pi = -4 \pm 2\sqrt 3$.
- **The same lag with the passivity supply.** With $w = uy$, $S = p x^2$ needs $\begin{bmatrix} -2p & p - \frac{1}{2} \\ p - \frac{1}{2} & 0 \end{bmatrix} \le 0$, which forces $p = \frac{1}{2}$. Here $S_a = S_r = \frac{1}{2}x^2$: the storage is unique, and it is the energy of a unit capacitor.
- **A static sector map.** $y = \varphi(u)$ with $a u^2 \le u\varphi(u) \le b u^2$ is dissipative with zero storage for $w = (y - au)(bu - y)$. This is the form that the [circle criterion](/circle-criterion/) uses.
- **Non-example.** $\dot x = x + u$, $y = x$ with $w = uy$. The feedback $u = -kx$, $k > 1$, takes out the energy $k x(0)^2 / (2(k - 1))$, which grows without bound as $k$ goes down to $1$. So $S_a(x) = \infty$ for $x \ne 0$, and the system is not dissipative for this supply rate.
- **Non-example, a negative storage.** For the integrator $\dot x = u$, $y = x$ with $w = -uy$, the function $S = -\frac{1}{2}x^2$ satisfies the dissipation inequality with equality. It is not a storage function, because it is negative. Some authors drop the condition $S \ge 0$; they call the result cyclo-dissipativity. Without $S \ge 0$, the dissipation inequality alone does not bound the state or the output.

## Related definitions

- [Passivity](/passivity/): the case $w = u^T y$, with its strict forms and positive real transfer functions.
- [Passivity theorem](/passivity-theorem/) and [small-gain theorem](/small-gain-theorem/): the two classic results on feedback loops, both cases of the rule above.
- [Kalman-Yakubovich-Popov lemma](/kalman-yakubovich-popov-lemma/) and [bounded real lemma](/bounded-real-lemma/): quadratic storage functions of linear systems as solutions of linear matrix inequalities.
- [Lyapunov function](/lyapunov-function/): a positive definite storage of a system with $w(0, y) \le 0$ is a Lyapunov function of the system with zero input.
- [Input-to-state stability](/input-to-state-stability/): an ISS-Lyapunov function satisfies a dissipation inequality with the rate $\sigma(|u|) - \alpha(|x|)$. This rate depends on the state, so it is a small extension of the definition above.
- [Port-Hamiltonian system](/port-hamiltonian-system/): a model class in which the Hamiltonian is a storage function for $w = u^T y$.

## References
