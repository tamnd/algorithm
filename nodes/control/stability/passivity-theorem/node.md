---
tag: VPAXMV
kind: theorem
slug: passivity-theorem
name: Passivity theorem
aliases:
- feedback passivity theorem
area: control/stability
level: advanced
summary: The negative feedback loop of two passive systems is passive. If both parts are output strictly passive, the loop has a finite L2 gain; stability needs some strictness.
prereqs: [passivity, lasalle-invariance-principle]
see_also: [passivity, dissipativity, small-gain-theorem, kalman-yakubovich-popov-lemma, circle-criterion, passivity-based-control, port-hamiltonian-system, ida-pbc]
sources:
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 6.4 (L2 and Lyapunov stability of passive systems) and Section 6.5 (feedback systems, the passivity theorems and loop transformations)
  - book: isbn:9780898716702
    title: "Charles A. Desoer and M. Vidyasagar, Feedback Systems: Input-Output Properties, SIAM Classics in Applied Mathematics, 2009 (reprint of the Academic Press edition of 1975)"
    locator: Chapter 6 (the passivity theorem for input-output maps, with one passive part and one strictly passive part of finite gain)
  - paper: doi:10.1109/TAC.1966.1098316
    title: George Zames, On the input-output stability of time-varying nonlinear feedback systems, Part I, Conditions derived using concepts of loop gain, conicity, and positivity, IEEE Transactions on Automatic Control 11(2), 228-238, 1966
    locator: the positivity (passivity) theorem for feedback loops
  - paper: doi:10.1016/0005-1098(77)90020-6
    title: David J. Hill and Peter J. Moylan, Stability results for nonlinear feedback systems, Automatica 13(4), 377-382, 1977
    locator: stability of feedback loops of dissipative systems, with passivity as a special case
  - book: isbn:9783319499918
    title: Arjan van der Schaft, L2-Gain and Passivity Techniques in Nonlinear Control, third edition, Springer, 2017
    locator: Chapter 2 (small-gain and passivity for input-output maps) and Chapter 4 (passive state space systems)
---

The passivity theorem is about the negative feedback loop of two [passive](/passivity/) systems, systems that cannot produce energy. The loop is again passive, because the energy that one part gives to the other is taken from the other in the same amount. Passivity alone does not make the loop stable: two lossless parts can trade energy for ever. Each stability result therefore needs some strictness, and this page names it every time: if both parts are output strictly passive, the loop has a finite L2 gain; if one part is passive and the other input strictly passive with a finite gain, the same holds; and with zero inputs, strict passivity or output strict passivity with observability gives asymptotic stability. The page is about the analysis of a given loop. [Dissipativity](/dissipativity/) is the general notion behind it, and [passivity-based control](/passivity-based-control/), [port-Hamiltonian systems](/port-hamiltonian-system/) and [IDA-PBC](/ida-pbc/) use it to design a controller as the second passive part.

## Statement

**Loop.** Two systems $H_1$ and $H_2$, each a state model $\dot x_i = f_i(x_i, e_i)$, $y_i = h_i(x_i, e_i)$ or a memoryless map $y_i = h_i(t, e_i)$, with $e_i, y_i \in \mathbb{R}^m$. They are connected in negative feedback with external inputs $u_1, u_2$:

$$e_1 = u_1 - y_2, \qquad e_2 = u_2 + y_1.$$

The loop is assumed well posed: for every input, the closed loop equations have a unique solution for all $t \ge 0$. Write $u = (u_1, u_2)$, $y = (y_1, y_2)$ and $x = (x_1, x_2)$.

**Passivity indices.** $H_i$ has the storage function $V_i \ge 0$ and the constants $\varepsilon_i \ge 0$, $\delta_i \ge 0$ if

$$e_i^T y_i \ \ge\ \dot V_i + \varepsilon_i |e_i|^2 + \delta_i |y_i|^2.$$

With $\varepsilon_i = \delta_i = 0$ this is passivity; $\varepsilon_i > 0$ is input strict passivity and $\delta_i > 0$ is output strict passivity. For a memoryless part, $V_i = 0$.

**Theorem 1 (the loop is passive).** If $H_1$ and $H_2$ are passive, then the loop with input $u$ and output $y$ is passive, with the storage function $V_1 + V_2$.

**Theorem 2 (finite L2 gain).** If $\varepsilon_1 + \delta_2 > 0$ and $\varepsilon_2 + \delta_1 > 0$, then the loop from $u$ to $y$ is finite-gain $L_2$ stable. With $a = \min(\varepsilon_1 + \delta_2,\ \varepsilon_2 + \delta_1)$ and $k = 1 + 2\max(\varepsilon_1, \varepsilon_2)$,

$$\|y_T\|_{L_2} \ \le\ \frac{k}{a}\, \|u_T\|_{L_2} + \sqrt{\frac{2\,(V_1(x_1(0)) + V_2(x_2(0)))}{a}} \qquad \text{for every } T \ge 0.$$

Two named cases:
- (a) both parts output strictly passive ($\delta_1, \delta_2 > 0$): the $L_2$ gain is at most $1/\min(\delta_1, \delta_2)$;
- (b) one part passive and the other input strictly passive with a finite $L_2$ gain (Desoer and Vidyasagar): if $\langle e, y \rangle_T \ge \varepsilon \|e_T\|^2 - \beta$ and $\|y_T\| \le \gamma \|e_T\|$, then $\langle e, y \rangle_T \ge \frac{\varepsilon}{2}\|e_T\|^2 + \frac{\varepsilon}{2\gamma^2}\|y_T\|^2 - \beta$. So that part has both indices positive in the integral form, and the general condition holds.

Here $\langle e, y \rangle_T = \int_0^T e^T y\, dt$. The proof below uses the pointwise inequalities; the same steps work for the integral forms.

**Theorem 3 (asymptotic stability).** Let $u = 0$, let both parts be state models with $f_i(0, 0) = 0$, $h_i(0, 0) = 0$ and continuously differentiable storage functions. The origin of the loop is asymptotically stable if
- (a) both parts are strictly passive, with $e_i^T y_i \ge \dot V_i + \psi_i(x_i)$ and $\psi_i$ positive definite; or
- (b) both parts are output strictly passive and zero-state observable; or
- (c) one part is strictly passive and the other is output strictly passive and zero-state observable.

A system is zero-state observable if $e = 0$ and $y(t) = 0$ for all $t \ge 0$ imply $x(t) = 0$. A passive memoryless part has no state; in (a) and (c) it counts as a strictly passive part, and $V$ is then the storage of the other part alone. If in addition $V_1 + V_2$ is radially unbounded, the origin is globally asymptotically stable.

## In plain words

Think of two machines that are connected so that each one drives the other. If neither machine can create energy, the pair cannot create energy either, because whatever one gives, the other receives. That alone does not make the pair settle down: two perfect springs can swap energy back and forth for ever. To make every motion die out or stay small, at least one machine must lose energy in the right way, for example by friction that grows with its output. Then energy that goes around the loop is burnt off, and the size of the signals inside the loop is bounded by the size of what comes in from outside. The theorem states exactly how much loss is enough.

## Proof

**Theorem 1.** On the loop, $e_1^T y_1 + e_2^T y_2 = (u_1 - y_2)^T y_1 + (u_2 + y_1)^T y_2 = u_1^T y_1 + u_2^T y_2 = u^T y$, because the terms $-y_2^T y_1$ and $y_1^T y_2$ cancel. Add the two passivity inequalities: $u^T y \ge \dot V_1 + \dot V_2$. $\square$

**Theorem 2.** Adding the two inequalities and using the cancellation above gives

$$u^T y \ \ge\ \dot V + \varepsilon_1 |u_1 - y_2|^2 + \varepsilon_2 |u_2 + y_1|^2 + \delta_1 |y_1|^2 + \delta_2 |y_2|^2, \qquad V = V_1 + V_2.$$

Expand the squares and drop $\varepsilon_1 |u_1|^2 + \varepsilon_2 |u_2|^2 \ge 0$:

$$(\varepsilon_2 + \delta_1)|y_1|^2 + (\varepsilon_1 + \delta_2)|y_2|^2 \ \le\ u^T y + 2\varepsilon_1 u_1^T y_2 - 2\varepsilon_2 u_2^T y_1 - \dot V.$$

The left side is at least $a|y|^2$. The first three terms on the right are $u^T K y$ for a matrix $K$ with induced 2-norm at most $k$, so they are at most $k|u||y| \le \frac{k^2}{2a}|u|^2 + \frac{a}{2}|y|^2$. Hence $\frac{a}{2}|y|^2 \le \frac{k^2}{2a}|u|^2 - \dot V$. Integrate over $[0, T]$ and use $V(x(T)) \ge 0$:

$$\int_0^T |y|^2\, dt \ \le\ \frac{k^2}{a^2} \int_0^T |u|^2\, dt + \frac{2}{a} V(x(0)).$$

Take square roots and use $\sqrt{p + q} \le \sqrt p + \sqrt q$. In case (a), $\varepsilon_1 = \varepsilon_2 = 0$, so $k = 1$ and $a = \min(\delta_1, \delta_2)$. In case (b), split $\varepsilon \|e_T\|^2$ into two halves and bound one half below by $\frac{\varepsilon}{2\gamma^2}\|y_T\|^2$, which uses $\|e_T\| \ge \|y_T\| / \gamma$. $\square$

**Theorem 3.** Let $V = V_1 + V_2$. With $u = 0$, Theorem 1 and the strict inequalities give $\dot V \le -\psi_1(x_1) - \psi_2(x_2)$ in case (a), $\dot V \le -\delta_1|y_1|^2 - \delta_2|y_2|^2$ in case (b), and a mix of the two in case (c).

First, $V$ is positive definite. In case (a), take a solution of $H_i$ with $e_i = 0$ from $x_i(0) \ne 0$. Then $V_i(x_i(0)) \ge V_i(x_i(0)) - V_i(x_i(t)) \ge \int_0^t \psi_i(x_i(s))\, ds > 0$, because $\psi_i(x_i(s)) > 0$ for small $s$. In case (b), take a solution of $H_i$ with $e_i = 0$ from $x_i(0) \ne 0$. Then $V_i(x_i(0)) \ge V_i(x_i(0)) - V_i(x_i(t)) \ge \delta_i \int_0^t |y_i|^2\, ds$, and zero-state observability makes $y_i$ not identically $0$, so $V_i(x_i(0)) > 0$.

In case (a), $\dot V$ is negative definite, and [Lyapunov's direct method](/lyapunov-direct-method/) gives asymptotic stability. In case (b), $\dot V \le 0$, and on the set where $\dot V = 0$ we have $y_1 = y_2 = 0$, hence $e_1 = -y_2 = 0$ and $e_2 = y_1 = 0$. A solution that stays in this set is a solution of each $H_i$ with zero input and zero output, so zero-state observability gives $x = 0$. The [LaSalle invariance principle](/lasalle-invariance-principle/) then gives asymptotic stability, and global asymptotic stability if $V$ is radially unbounded. Case (c) combines the two arguments. $\square$

## Consequences

**Worked example, both parts output strictly passive.** Take $H_1 = H_2 = 1/(s + 1)$, each with the state model $\dot x = -x + e$, $y = x$, the storage $\frac{1}{2}x^2$ and $\delta = 1$. Theorem 2(a) gives an $L_2$ gain of at most $1$ from $(u_1, u_2)$ to $(y_1, y_2)$. Solving the loop with $H = 1/(s + 1)$ gives

$$\begin{bmatrix} y_1 \\ y_2 \end{bmatrix} = \frac{1}{1 + H^2} \begin{bmatrix} H & -H^2 \\ H^2 & H \end{bmatrix} \begin{bmatrix} u_1 \\ u_2 \end{bmatrix}.$$

This matrix has the form $aI + bJ$ with $J = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$, so its singular values are $|a \pm jb|$, and $a + jb = H/(1 - jH) = 1/(s + 1 - j)$. At $s = j\omega$ its modulus is $1/|1 + j(\omega - 1)|$, which reaches $1$ at $\omega = 1$ rad/s. The [H-infinity norm](/h-infinity-norm/) of the loop is exactly $1$, so the bound of Theorem 2 is reached here.

**Worked example, one output strictly passive part.** Take $H_1 = 1/(s + 1)$ with $\delta_1 = 1$ and the lossless integrator $H_2 = 1/s$, and let $u_2 = 0$. Here Theorem 2 does not apply, because $\varepsilon_1 + \delta_2 = 0$. A one-sided form still holds: with $u_2 = 0$, $u_1^T y_1 = e_1^T y_1 + e_2^T y_2 \ge \dot V + \delta_1 |y_1|^2$, and the steps of the proof give a gain of at most $1/\delta_1 = 1$ from $u_1$ to $y_1$. The closed loop is $y_1 = \frac{s}{s^2 + s + 1} u_1$, and $|j\omega / (1 - \omega^2 + j\omega)| \le 1$ with equality at $\omega = 1$ rad/s, so this bound is also reached.

**Positive real transfer functions.** For linear parts, passivity is positive realness, and the [Kalman-Yakubovich-Popov lemma](/kalman-yakubovich-popov-lemma/) gives the storage functions. For single-input single-output parts with minimal realizations, a loop of a positive real $G_1$ and a strictly positive real $G_2$ is exponentially stable. The proof is the LaSalle step of Theorem 3: $G_2$ is strictly passive, so $\dot V = 0$ forces $x_2 = 0$; then $B_2 e_2 = 0$ with $B_2 \ne 0$ gives $e_2 = 0$ and $y_2 = 0$, so $G_1$ has zero input and zero output, and its observability gives $x_1 = 0$.

**Sector nonlinearities.** A memoryless nonlinearity in the sector $[0, \infty]$ is passive, and one in the sector $[\varepsilon, \infty]$ is input strictly passive. A loop of a map in the sector $[0, \infty]$ and a minimal strictly positive real $G$ is covered by Theorem 3(a), with the map counted as a strictly passive part. This is the limit case $k_1 = 0$, $k_2 = \infty$ of the [circle criterion](/circle-criterion/).

**Design.** The theorem shows how to make a loop stable by design: render the plant passive with respect to some output, and close the loop with a strictly passive controller. This is the idea of [passivity-based control](/passivity-based-control/). The conditions $\varepsilon_1 + \delta_2 > 0$ and $\varepsilon_2 + \delta_1 > 0$ show that the strictness can sit in either part. Khalil (2002, Section 6.5) also shows how a loop transformation lets the excess of passivity of one part make up for a shortage in the other.

**Passivity and small gain.** Both are cases of the rule for loops of [dissipative](/dissipativity/) systems: passivity uses the supply rate $u^T y$, and the [small-gain theorem](/small-gain-theorem/) uses $\gamma^2|u|^2 - |y|^2$. A loop of two linear parts can satisfy one test and fail the other, so neither is stronger.

## Tightness

**Passivity alone gives no stability.** Take two lossless integrators, $H_1 = H_2 = 1/s$. With $u_2 = 0$, the map from $u_1$ to $y_1$ is $\frac{1/s}{1 + 1/s^2} = \frac{s}{s^2 + 1}$, with poles at $\pm j$. The input $u_1 = \sin t$, which is bounded, gives an output that grows like $t$, and the loop has no finite $L_2$ gain. With $u = 0$, the states oscillate for ever: the origin is Lyapunov stable but not asymptotically stable.

**One strictly passive part is not enough without observability.** Take $H_1$ the strictly passive $\dot x_1 = -x_1 + e_1$, $y_1 = x_1$, and $H_2$ with the state $z$, $\dot z = 0$ and $y_2 = 0$. $H_2$ is passive with $V_2 = z^2$, since $\dot V_2 = 0 = e_2 y_2$. In the loop, $z$ stays at its initial value, so the origin is not asymptotically stable. Case (c) of Theorem 3 needs the second part to be output strictly passive and zero-state observable, and here $H_2$ is not observable.

**Both conditions of Theorem 2 are needed.** Take $H_1 = 0$, the zero map, which is output strictly passive with every $\delta_1 > 0$ because $y_1 = 0$, and the integrator $H_2 = 1/s$. Then $\varepsilon_2 + \delta_1 > 0$ holds and $\varepsilon_1 + \delta_2 = 0$. The loop gives $y_2 = \frac{1}{s} u_2$, and the input $u_2 = e^{-t}$, which is in $L_2$, gives $y_2 = 1 - e^{-t}$, which is not.

## History

Positivity of operators in feedback loops comes from network theory, where a loop of passive electrical networks cannot produce energy. Zames (1966) stated the positivity theorem for input-output maps in the same paper as the small-gain theorem. Desoer and Vidyasagar (1975) gave the form with one passive part and one strictly passive part of finite gain. Willems (1972) placed both results in the theory of dissipative systems, and Hill and Moylan (1976, 1977) gave stability results for feedback loops of dissipative systems with state models. Khalil's text gives the state form with the indices $\varepsilon_i$ and $\delta_i$ and the observability conditions used above.

## References
