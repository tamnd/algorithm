---
tag: M9NRR6
kind: theorem
slug: bang-bang-control
name: Bang-bang principle
aliases:
- bang-bang control
area: control/optimal-and-predictive-control
level: core
summary: For linear systems with box-bounded inputs, inputs at the bounds reach every reachable state. Time-optimal inputs are bang-bang if normal, with at most n - 1 switches if all eigenvalues are real.
prereqs: [time-optimal-control, pontryagin-maximum-principle, kalman-rank-condition]
see_also: [singular-arc, control-hamiltonian, controllability, reachable-set-computation, transversality-conditions, matrix-exponential, variation-of-constants-formula, sliding-mode-control]
sources:
  - paper: "J. P. LaSalle, The time optimal control problem, in Contributions to the Theory of Nonlinear Oscillations, Volume V, Annals of Mathematics Studies 45, Princeton University Press, 1960"
  - url: https://math.berkeley.edu/~evans/control.course.pdf
    title: Lawrence C. Evans, An Introduction to Mathematical Optimal Control Theory, lecture notes, University of California, Berkeley
    locator: Chapter 2 (the bang-bang principle, proved with the Krein-Milman theorem) and Chapter 3 (linear time-optimal control)
  - book: isbn:9780123426505
    title: Henry Hermes and Joseph P. LaSalle, Functional Analysis and Time Optimal Control, Academic Press, 1969
    locator: Part II (linear time optimal control)
  - book: isbn:9780691151878
    title: Daniel Liberzon, Calculus of Variations and Optimal Control Theory, A Concise Introduction, Princeton University Press, 2012
    locator: Section 4.4.2 (the bang-bang principle for linear systems)
  - paper: "A. A. Feldbaum, Optimal processes in automatic control systems, Avtomatika i Telemekhanika 14(6), 712-728, 1953 (in Russian)"
---

The bang-bang principle says that for a linear system $\dot x = A x + B u$ whose inputs lie in a box, nothing is lost by using only the corners of the box: every state that can be reached at time $t$ can also be reached at time $t$ with each input component at $+1$ or $-1$ at almost every moment. A second part says that the time-optimal input is itself of this form, and is unique with finitely many switches, when the system is normal. When all eigenvalues of $A$ are real and the input is scalar, the number of switches is at most $n - 1$. The name "bang-bang" comes from the sound of a relay that hits its stops.

## Statement

**Setting.** $\dot x = A x + B u$ with $A \in \mathbb{R}^{n \times n}$, $B = [b_1, \dots, b_m] \in \mathbb{R}^{n \times m}$, and inputs in the box $U = [-1, 1]^m$. An input is admissible on $[0, t]$ if it is measurable with values in $U$. It is **bang-bang** if $|u_i(s)| = 1$ for almost every $s$ and every $i$. The system is **normal** if $(A, b_i)$ is [controllable](/kalman-rank-condition/) for each $i = 1, \dots, m$.

**Theorem.**

1. **Bang-bang principle** (LaSalle 1960). For every $x_0$ and $t > 0$, the set of states reachable at time $t$ from $x_0$ with admissible inputs equals the set reachable at time $t$ with bang-bang inputs.
2. **Time-optimal inputs.** Suppose $x_0$ can be steered to 0 by some admissible input. Then a [time-optimal](/time-optimal-control/) input exists. If the system is normal, the time-optimal input $u^*$ on $[0, t^*]$ is unique, and there is $\eta \ne 0$ with

$$u_i^*(s) = \operatorname{sgn}\left( b_i^T e^{-A^T s} \eta \right) \quad \text{for almost every } s, \quad i = 1, \dots, m,$$

and each switching function $b_i^T e^{-A^T s} \eta$ has finitely many zeros on $[0, t^*]$. So $u^*$ is bang-bang with finitely many switches.

In the minimum form of the [maximum principle](/pontryagin-maximum-principle/), $\eta = -\lambda(0)$, and $b_i^T e^{-A^T s} \eta = -b_i^T \lambda(s)$ is the negative of the $i$th component of the switching function of the [Hamiltonian](/control-hamiltonian/) $H = \lambda_0 + \lambda^T (A x + B u)$.

## In plain words

Suppose you can push a linear system with a limited force in each direction. Part one says that any place you can reach at a given time with gentle, varying pushes, you can also reach at that time with pushes that are always full, only changing direction. Part two says that if you want to arrive as fast as possible, full pushes are not only allowed but required, as long as each input on its own can move the whole state. The direction of each push is set by the sign of a simple function of time, so it changes only a limited number of times. For systems without oscillation, that number is at most one less than the number of state variables.

## Proof

Write $M(s) = e^{-A s} B$. By the [variation of constants formula](/variation-of-constants-formula/), the state at time $t$ is

$$x(t) = e^{A t} \left( x_0 + \int_0^t M(s) u(s)\, ds \right),$$

so a state $z$ is reachable at time $t$ exactly when $\int_0^t M(s) u(s)\, ds = w$, with $w = e^{-A t} z - x_0$.

**Part 1.** Fix a reachable $z$ and let

$$\mathcal{K} = \left\{ u \in L^\infty([0, t]; \mathbb{R}^m) : u(s) \in U \text{ a.e.},\ \int_0^t M(s) u(s)\, ds = w \right\}.$$

$\mathcal{K}$ is not empty, and it is convex. The box condition defines a weak-star closed subset of a ball of $L^\infty = (L^1)^*$, and the map $u \mapsto \int_0^t M u\, ds$ is weak-star continuous because the entries of $M$ are in $L^1$. So $\mathcal{K}$ is weak-star compact by the Banach-Alaoglu theorem, and by the Krein-Milman theorem it has an extreme point $u^\circ$.

Suppose $u^\circ$ is not bang-bang. Then there are an index $i$, a number $\varepsilon > 0$ and a set $E \subseteq [0, t]$ of positive measure with $|u_i^\circ(s)| \le 1 - \varepsilon$ on $E$. The linear map $\beta \mapsto \int_E M(s) e_i \beta(s)\, ds$ goes from the infinite-dimensional space $L^\infty(E)$ to $\mathbb{R}^n$, so it has a nonzero element $\beta$ in its kernel; scale it so that $|\beta| \le 1$, and extend it by 0 outside $E$. Then $u^\circ + \varepsilon \beta e_i$ and $u^\circ - \varepsilon \beta e_i$ both lie in $\mathcal{K}$, and $u^\circ$ is their midpoint. This contradicts the choice of $u^\circ$ as an extreme point. So $u^\circ$ is a bang-bang input that reaches $z$ at time $t$.

**Part 2.** Let $\mathcal{R}(t) = \{ \int_0^t M u\, ds : u \text{ admissible} \}$. The state $x_0$ can be steered to 0 at time $t$ exactly when $-x_0 \in \mathcal{R}(t)$. Each $\mathcal{R}(t)$ is convex and compact (the image of the weak-star compact convex set of inputs under the continuous linear map above), and $\mathcal{R}(t)$ grows continuously with $t$ in the Hausdorff distance, since $|\int_t^{t'} M u\, ds| \le C |t' - t|$. Hence the set of $t$ with $-x_0 \in \mathcal{R}(t)$ is closed, and its smallest element $t^*$ exists: this is the existence of a time-optimal input.

The point $-x_0$ lies on the boundary of $\mathcal{R}(t^*)$. If it were in the interior, a ball around it would lie in $\mathcal{R}(t^*)$, and by the continuity in $t$, $-x_0 \in \mathcal{R}(t)$ for some $t < t^*$. So there is a supporting hyperplane: a vector $\eta \ne 0$ with $\eta^T (-x_0) \ge \eta^T r$ for all $r \in \mathcal{R}(t^*)$. Let $u^*$ be any time-optimal input. Then

$$\int_0^{t^*} \eta^T M(s) u^*(s)\, ds = \max_{u \text{ admissible}} \int_0^{t^*} \sum_{i=1}^m \varphi_i(s) u_i(s)\, ds = \int_0^{t^*} \sum_{i=1}^m |\varphi_i(s)|\, ds,$$

with $\varphi_i(s) = \eta^T e^{-A s} b_i = b_i^T e^{-A^T s} \eta$. The middle maximum is attained exactly by inputs with $u_i(s) = \operatorname{sgn} \varphi_i(s)$ wherever $\varphi_i(s) \ne 0$, so $u^*$ has this form almost everywhere outside the zero sets of the $\varphi_i$.

Now use normality. $\varphi_i$ is real analytic. If it had infinitely many zeros on $[0, t^*]$, it would vanish identically, and then all its derivatives at 0, $(-1)^k b_i^T (A^T)^k \eta$, would be zero. So $\eta$ would be orthogonal to $b_i, A b_i, \dots, A^{n-1} b_i$, which span $\mathbb{R}^n$ by the [Kalman rank condition](/kalman-rank-condition/), and $\eta = 0$, a contradiction. So each $\varphi_i$ has finitely many zeros, $u^*$ is determined almost everywhere by $\eta$, and it is bang-bang with finitely many switches. Fix one such $\eta$. Every time-optimal input reaches $-x_0$ in $\mathcal{R}(t^*)$, so it attains the maximum above for this $\eta$ and equals $\operatorname{sgn} \varphi_i$ almost everywhere. So all time-optimal inputs agree almost everywhere: the time-optimal input is unique. $\blacksquare$

## Consequences

**At most $n - 1$ switches with real eigenvalues** (Feldbaum 1953). Let $m = 1$, the system be normal, and all eigenvalues of $A$ be real. Then the time-optimal input has at most $n - 1$ switches.

*Proof.* With real eigenvalues $\mu_1, \dots, \mu_k$ of algebraic multiplicities $d_1, \dots, d_k$, $d_1 + \dots + d_k = n$, every entry of $e^{-A^T s}$, and so $\varphi(s) = b^T e^{-A^T s} \eta$, has the form $\sum_{j=1}^k p_j(s) e^{-\mu_j s}$ with polynomials $p_j$ of degree at most $d_j - 1$. Claim: such a function, if it is not identically zero, has at most $d_1 + \dots + d_k - 1$ real zeros. For $k = 1$ it is $e^{-\mu_1 s}$ times a nonzero polynomial of degree at most $d_1 - 1$. For $k > 1$, multiply by $e^{\mu_1 s}$, which keeps the zeros, and differentiate $d_1$ times. This removes the term $p_1$ and leaves $\psi(s) = \sum_{j \ge 2} q_j(s) e^{(\mu_1 - \mu_j) s}$ with $\deg q_j = \deg p_j$, because $\mu_j \ne \mu_1$. By Rolle's theorem, each derivative has at least one zero fewer than the function before it, so the number of zeros of $\varphi$ is at most the number of zeros of $\psi$ plus $d_1$. If $\psi \equiv 0$, then $e^{\mu_1 s} \varphi$ is a polynomial of degree at most $d_1 - 1$, with at most $d_1 - 1$ zeros. Otherwise, by induction, $\psi$ has at most $d_2 + \dots + d_k - 1$ zeros. Either way $\varphi$ has at most $n - 1$ zeros, so $u^* = \operatorname{sgn} \varphi$ changes sign at most $n - 1$ times. $\blacksquare$

- **The double integrator.** $n = 2$ with the double eigenvalue 0, so at most one switch. From $(1, 0)$ the time-optimal input is $-1$ for 1 s and then $+1$ for 1 s ([time-optimal control](/time-optimal-control/)).
- **A hand check of Part 1.** For $\dot x = u$, $|u| \le 1$, $x(0) = 0$, the state $1/2$ at $t = 1$ is reached by $u = 1/2$, and also by the bang-bang input $u = +1$ on $[0, 3/4]$ and $u = -1$ on $(3/4, 1]$, since $3/4 - 1/4 = 1/2$.
- **The reachable set.** By Part 1, the reachable set at time $t$ is the reachable set of the bang-bang inputs, and it is convex and compact. Its support function is $\int_0^t \|B^T e^{-A^T s} \eta\|_1\, ds$, which [reachable set computation](/reachable-set-computation/) uses.

## Tightness

**Complex eigenvalues.** For the harmonic oscillator $\dot x_1 = x_2$, $\dot x_2 = -x_1 + u$, the switching function is $\rho \sin(s + \phi)$, so the time-optimal input switches every $\pi$ seconds, and the number of switches grows without bound as $x_0$ moves away from 0. The bound $n - 1 = 1$ fails, and only the real-eigenvalue hypothesis excludes this.

**Without normality.** Take $\dot x = u$ in $\mathbb{R}^2$ with $B = I$ and $U = [-1, 1]^2$, from $x_0 = (1, 1/2)$. The minimum time is 1, because $x_1$ needs it. The input $u_1 = -1$, $u_2 = -1/2$ is time-optimal and is not bang-bang, and so is every $u_2$ with values in $[-1, 1]$ and integral $-1/2$. Here $(A, b_i) = (0, e_i)$ is not controllable in $\mathbb{R}^2$, so the system is not normal. Part 1 still holds: the bang-bang input $u_2 = -1$ on $[0, 3/4]$ and $+1$ after it also works.

**Nonlinear systems.** Part 1 needs dynamics that are linear in $u$. For $\dot x = u^2$ with $|u| \le 1$ and $x(0) = 0$, the reachable set at $t = 1$ is $[0, 1]$, but bang-bang inputs reach only the point 1. For nonlinear control-affine systems, the time-optimal input can also have [singular arcs](/singular-arc/) or chatter.

**Singular problems.** If some switching function vanishes on an interval, the sign rule does not fix the input there. Normality excludes this for linear time-optimal problems, but not for other costs, such as $\int x^2\, dt$ ([singular arc](/singular-arc/)).

## History

Bushaw (1952) solved the time-optimal problem of second-order systems with a relay input in his Princeton thesis, and Feldbaum (1953) stated the bound of $n - 1$ switches for systems with real eigenvalues. LaSalle (1960) proved the bang-bang principle for linear systems in general, and Gamkrelidze and Pontryagin's group obtained the time-optimal results as a case of the [maximum principle](/pontryagin-maximum-principle/). Hermes and LaSalle (1969) give the functional-analytic proof with the Krein-Milman theorem, and Evans's notes follow it.

## References
