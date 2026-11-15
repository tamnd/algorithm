---
tag: HRD81W
kind: definition
slug: zero-dynamics
name: Zero dynamics
aliases:
- zero dynamics of a nonlinear system
area: control/nonlinear-control
level: advanced
summary: The dynamics that remain when an input holds the output at zero. They extend the transmission zeros to nonlinear systems; asymptotically stable zero dynamics define a minimum phase system.
prereqs: [relative-degree, asymptotic-stability, transmission-zero]
see_also: [relative-degree, input-output-linearization, transmission-zero, minimum-phase, asymptotic-stability, input-to-state-stability, hybrid-zero-dynamics, output-regulation-problem]
sources:
  - paper: "C. I. Byrnes and A. Isidori, Asymptotic stabilization of minimum phase nonlinear systems, IEEE Transactions on Automatic Control 36(10), 1122-1137, 1991"
    title: Asymptotic stabilization of minimum phase nonlinear systems
    locator: the definition of a minimum phase nonlinear system through the zero dynamics, and its use for stabilization
  - book: isbn:9783540199168
    title: Alberto Isidori, Nonlinear Control Systems, third edition, Springer, 1995
    locator: Chapter 4 (Nonlinear feedback for single-input single-output systems), the normal form and the zero dynamics
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 13.2, Input-Output Linearization, the normal form, the internal dynamics, the zero dynamics and the minimum phase property
---

The zero dynamics of a system are the dynamics that remain when the input is chosen to keep the output exactly at zero. A [relative degree](/relative-degree/) $r$ splits the $n$ states into $r$ coordinates that the output fixes and $n - r$ coordinates that the output does not see. If the output and its first $r - 1$ derivatives are held at zero, the first group is zero, and the second group still moves. This motion is the zero dynamics. For a linear system its eigenvalues are the [zeros](/transmission-zero/) of the transfer function, so the zero dynamics are the nonlinear version of the zeros. A system whose zero dynamics are [asymptotically stable](/asymptotic-stability/) is called minimum phase. This property decides whether [input-output linearization](/input-output-linearization/) is safe: the feedback makes the output behave well, and the zero dynamics decide what the rest of the state does.

## Definition

**Setting.** The system is $\dot x = f(x) + g(x) u$, $y = h(x)$, with $x$ in an open set $U \subseteq \mathbb{R}^n$, scalar $u$ and $y$, and $f$, $g$, $h$ smooth ($C^\infty$), so solutions exist and are unique by the [Picard-Lindelöf theorem](/picard-lindelof-theorem/). Let $x_0$ be an equilibrium, $f(x_0) = 0$, with $h(x_0) = 0$, and let the system have relative degree $r < n$ at $x_0$.

**Normal form.** Near $x_0$ the functions $\xi_i = L_f^{i-1} h$ for $i = 1, \dots, r$ have linearly independent differentials. One can add $n - r$ functions $\eta = (\eta_1, \dots, \eta_{n-r})$ with $\eta(x_0) = 0$ and $L_g \eta_j = 0$ near $x_0$, such that $x \mapsto (\xi, \eta)$ is a change of coordinates near $x_0$ (Isidori, Chapter 4). In these coordinates the system is

$$\dot\xi_1 = \xi_2, \quad \dots, \quad \dot\xi_{r-1} = \xi_r, \quad \dot\xi_r = b(\xi, \eta) + a(\xi, \eta)\, u, \quad \dot\eta = q(\xi, \eta), \quad y = \xi_1,$$

where $b = L_f^r h$, $a = L_g L_f^{r-1} h$ with $a(0, 0) \neq 0$, and $q = L_f \eta$, all written in the new coordinates. The equation $\dot\eta = q(\xi, \eta)$ is the **internal dynamics**. The input does not enter it, because $L_g \eta = 0$.

**Zero dynamics.** The output is zero for all $t$ if and only if $\xi(t) = 0$ for all $t$. Then $\dot\xi_r = 0$ forces the input

$$u^*(\eta) = -\frac{b(0, \eta)}{a(0, \eta)},$$

and $\eta$ obeys

$$\dot\eta = q(0, \eta).$$

This $(n - r)$-dimensional system is the **zero dynamics** of the system at $x_0$. Without coordinates: the set $Z^* = \{x : h(x) = L_f h(x) = \dots = L_f^{r-1} h(x) = 0\}$ is a smooth manifold of dimension $n - r$ near $x_0$, the feedback $u^*(x) = -L_f^r h(x) / L_g L_f^{r-1} h(x)$ is the only one that keeps the state in $Z^*$, and the zero dynamics are $\dot x = f(x) + g(x) u^*(x)$ restricted to $Z^*$. They do not depend on the choice of $\eta$.

**Minimum phase.** The system is **minimum phase** at $x_0$ if $\eta = 0$ is an asymptotically stable equilibrium of the zero dynamics (Byrnes and Isidori 1991). It is **globally minimum phase** if the zero dynamics are globally asymptotically stable, and **exponentially minimum phase** if they are exponentially stable. Otherwise the system is **non-minimum phase**. The name comes from the linear case, where a stable system with all its zeros in the open left half-plane has the least phase lag for its gain; the [minimum phase](/minimum-phase/) page treats the discrete-time version of the linear property.

**Linear case.** For $\dot x = A x + B u$, $y = C x$ with relative degree $r$, the zero dynamics are a linear system of dimension $n - r$. Its characteristic polynomial is the numerator of $C\, \mathrm{adj}(sI - A)\, B$, which has degree $n - r$. When the realization is minimal, its roots are the zeros of $G(s) = C (sI - A)^{-1} B$.

## Examples and non-examples

**A minimum phase system.** Take $\dot x_1 = x_2$, $\dot x_2 = x_1 x_3 - x_2^3 + (1 + x_1^2) u$, $\dot x_3 = -x_3 + x_1^2$ and $y = x_1$. The relative degree is $2$ everywhere, $\xi = (x_1, x_2)$, and $\eta = x_3$ has $L_g \eta = 0$. With $\xi = 0$ the zero dynamics are $\dot\eta = -\eta$. They are globally exponentially stable, so the system is globally minimum phase. The zero-holding input is $u^* = 0$ here, because $b(0, \eta) = 0$.

**A linear non-minimum phase system.** Take $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ and $C = \begin{bmatrix} -1 & 1 \end{bmatrix}$, so that $G(s) = (s - 1)/(s^2 + 3 s + 2)$. Here $C B = 1$, so $r = 1$, and $\eta = x_1$ has $L_g \eta = 0$. On $Z^* = \{x_2 = x_1\}$ the zero dynamics are $\dot\eta = x_2 = \eta$. The eigenvalue $1$ is the zero of $G$. The system is non-minimum phase: holding $y = 0$ makes $x_1$ grow like $e^t$.

**Asymptotically stable, but not exponentially.** Take $\dot x_1 = x_2^3 + u$, $\dot x_2 = u$ and $y = x_1$. Then $L_g h = 1$, so $r = 1$, and $\eta = x_2 - x_1$ has $L_g \eta = 0$. With $x_1 = 0$ the input is $u^* = -x_2^3$, and the zero dynamics are $\dot x_2 = -x_2^3$. They are globally asymptotically stable, so the system is minimum phase. Their linearization is $\dot\eta = 0$. The [Jacobian linearization](/jacobian-linearization/) of the system at $0$ has $C\, \mathrm{adj}(sI - A)\, B = s$, an invariant zero at $s = 0$, so it cannot decide the question.

**Non-example: the internal dynamics are not the zero dynamics.** In the first example the internal dynamics are $\dot\eta = -\eta + \xi_1^2$. They depend on the output. When the output tracks a reference that is not zero, $\eta$ is driven by $\xi$, and its behavior is not fixed by the zero dynamics alone. Asymptotic stability of $\dot\eta = q(0, \eta)$ gives bounded $\eta$ only for small $\xi$. For large references one needs more, for example that $\dot\eta = q(\xi, \eta)$ is [input-to-state stable](/input-to-state-stability/) with $\xi$ as its input.

**Non-example: the dynamics with zero input.** The system $\dot x = f(x)$ with $u = 0$ is the free motion. It is not the zero dynamics. In the linear example above, the free motion has eigenvalues $-1$ and $-2$, while the zero dynamics have eigenvalue $1$.

**Non-example: relative degree $n$.** If $r = n$, there is no $\eta$, and the zero dynamics are empty. Then the system is feedback linearizable with this output, and the question of minimum phase does not arise.

## Related definitions

- [Relative degree](/relative-degree/): it fixes the split into $\xi$ and $\eta$.
- [Transmission zero](/transmission-zero/) and [poles and zeros](/poles-and-zeros/): the linear case.
- [Input-output linearization](/input-output-linearization/): it makes the $\xi$ part linear and leaves the zero dynamics unchanged.
- [Hybrid zero dynamics](/hybrid-zero-dynamics/): the same idea for walking robots with impacts.
- [Output regulation problem](/output-regulation-problem/): the regulator equations ask for an invariant manifold on which the error is zero, which is a zero dynamics question.

## References
