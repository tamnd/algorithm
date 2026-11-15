---
tag: 03Q3RF
kind: definition
slug: lie-derivative
name: Lie derivative
aliases:
- Lie derivative of a function along a vector field
area: control/nonlinear-control
level: core
summary: "The derivative of a scalar function along a vector field: L_f h = (dh/dx) f, the rate of change of h along the solutions of x' = f(x)."
prereqs: [gradient, control-affine-system]
see_also: [lie-bracket, relative-degree, input-output-linearization, lyapunov-direct-method, control-affine-system, markov-parameters, observability, zero-dynamics]
sources:
  - book: isbn:9783540199168
    title: Alberto Isidori, Nonlinear Control Systems, third edition, Springer, 1995
    locator: Chapter 1 (Local decompositions of control systems), where the Lie derivative is defined with the other tools of differential geometry; Chapter 4 uses it for the relative degree
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 13.2, Input-Output Linearization, where the notation L_f h is introduced
  - book: isbn:9780130408907
    title: Jean-Jacques E. Slotine and Weiping Li, Applied Nonlinear Control, Prentice Hall, 1991
    locator: Section 6.2, Mathematical Tools
---

The Lie derivative of a scalar function $h$ along a vector field $f$ is the directional derivative of $h$ in the direction $f(x)$, at each point $x$. It is written $L_f h$. If $x(t)$ is a solution of $\dot x = f(x)$, then $\frac{d}{dt} h(x(t)) = L_f h(x(t))$. So $L_f h$ tells how fast $h$ changes along the motion, without solving the equation. In nonlinear control it is the basic notation for derivatives of an output. For the [control-affine system](/control-affine-system/) $\dot x = f(x) + g(x) u$ with output $y = h(x)$, the first derivative of the output is $\dot y = L_f h(x) + L_g h(x)\, u$. Repeated Lie derivatives give the [relative degree](/relative-degree/), and with them [input-output linearization](/input-output-linearization/) builds its feedback. The derivative of a [Lyapunov function](/lyapunov-function/) along the solutions is also a Lie derivative.

## Definition

Let $U \subseteq \mathbb{R}^n$ be open, let $f : U \to \mathbb{R}^n$ be a vector field, and let $h : U \to \mathbb{R}$ be continuously differentiable. The **Lie derivative of $h$ along $f$** is the function

$$L_f h(x) = \frac{\partial h}{\partial x}(x)\, f(x) = \sum_{i=1}^n \frac{\partial h}{\partial x_i}(x)\, f_i(x) = \langle \nabla h(x), f(x) \rangle .$$

Here $\frac{\partial h}{\partial x}$ is the row vector of partial derivatives, the transpose of the [gradient](/gradient/). If $f$ and $h$ are smooth ($C^\infty$), then $L_f h$ is smooth, and the **iterated Lie derivatives** are defined by

$$L_f^0 h = h, \qquad L_f^k h = L_f\left(L_f^{k-1} h\right) \quad (k \ge 1).$$

For two fields $f$ and $g$, the mixed derivative $L_g L_f h$ means $L_g (L_f h)$: first along $f$, then along $g$. For a vector-valued $h = (h_1, \dots, h_p)$, the Lie derivative is taken entry by entry.

**Derivative along solutions.** Let $f$ be locally Lipschitz, so that $\dot x = f(x)$ has a unique solution for each initial state, by the [Picard-Lindelöf theorem](/picard-lindelof-theorem/) (see the [Lipschitz condition](/lipschitz-condition/)). Write $\Phi_t(x_0)$ for this solution at time $t$. The chain rule gives

$$\frac{d}{dt} h(\Phi_t(x_0)) = L_f h(\Phi_t(x_0)), \qquad L_f h(x_0) = \left. \frac{d}{dt} h(\Phi_t(x_0)) \right|_{t=0} .$$

The second formula does not use coordinates. So $L_f h$ does not depend on the choice of coordinates: if $z = T(x)$ for a diffeomorphism $T$, and $\tilde f$ and $\tilde h$ are $f$ and $h$ written in $z$, then $L_{\tilde f} \tilde h(T(x)) = L_f h(x)$.

**Rules.** For functions $h_1$, $h_2$, fields $f$, $g$ and a function $\alpha$: $L_f(h_1 + h_2) = L_f h_1 + L_f h_2$, $L_f(h_1 h_2) = h_1 L_f h_2 + h_2 L_f h_1$, $L_{f+g} h = L_f h + L_g h$ and $L_{\alpha f} h = \alpha\, L_f h$. The order of two Lie derivatives matters. The difference is a third Lie derivative, along the [Lie bracket](/lie-bracket/): $L_f L_g h - L_g L_f h = L_{[f,g]} h$.

**Derivatives of the output.** For $\dot x = f(x) + g(x) u$ and $y = h(x)$, the chain rule gives $\dot y = L_f h(x) + L_g h(x)\, u$. If $L_g h = 0$ near a point, then $\dot y = L_f h(x)$ and $\ddot y = L_f^2 h(x) + L_g L_f h(x)\, u$, and so on, until a term $L_g L_f^k h$ is not zero. This is the computation behind the relative degree.

## Examples and non-examples

**Linear system.** Let $f(x) = A x$, $g(x) = B$ (a constant field) and $h(x) = C x$. Then $L_f^k h(x) = C A^k x$ and $L_g L_f^k h = C A^k B$. These constants are the [Markov parameters](/markov-parameters/) of the system. The output derivatives are $y^{(k)} = C A^k x + \sum_{j<k} C A^{k-1-j} B u^{(j)}$.

**A system with three states.** Let

$$f(x) = \begin{bmatrix} x_2 \\ x_1 x_3 - x_2^3 \\ -x_3 + x_1^2 \end{bmatrix}, \qquad g(x) = \begin{bmatrix} 0 \\ 1 + x_1^2 \\ 0 \end{bmatrix}, \qquad h(x) = x_1 .$$

Then $L_g h = 0$, $L_f h = x_2$, $L_g L_f h = 1 + x_1^2$ and $L_f^2 h = x_1 x_3 - x_2^3$. So $\dot y = x_2$ and $\ddot y = x_1 x_3 - x_2^3 + (1 + x_1^2)\, u$. The [input-output linearization](/input-output-linearization/) page uses this system.

**Energy of a pendulum.** For $\dot x_1 = x_2$, $\dot x_2 = -\sin x_1$ and $E(x) = \frac12 x_2^2 + 1 - \cos x_1$, $L_f E = (\sin x_1)\, x_2 + x_2 (-\sin x_1) = 0$. So $E$ is constant along every solution. A function with $L_f h = 0$ is a conserved quantity of the system.

**Lyapunov function.** For $\dot x = A x$ and $V(x) = x^T P x$ with $P = P^T$, $L_f V(x) = x^T (A^T P + P A) x$. The [direct method of Lyapunov](/lyapunov-direct-method/) asks for $L_f V < 0$ away from the equilibrium.

**Non-example: the order is not free.** Let $f(x) = (x_2, 0)$, $g(x) = (0, 1)$ and $h(x) = x_1$. Then $L_g h = 0$, so $L_f L_g h = 0$. But $L_f h = x_2$, so $L_g L_f h = 1$. The two mixed derivatives differ, and the difference $-1$ equals $L_{[f,g]} h$ with $[f, g] = (-1, 0)$.

**Non-example: a time-varying function.** For $h(t, x)$ the derivative along solutions is $\frac{\partial h}{\partial t} + L_f h$, not $L_f h$ alone. The Lie derivative of this page is for functions of $x$ only.

**Non-example: a vector field along a vector field.** The Lie derivative of a vector field $g$ along $f$ is a different object. It is the Lie bracket $[f, g]$, with its own page.

## Related definitions

- [Lie bracket](/lie-bracket/): the field that measures the difference $L_f L_g - L_g L_f$.
- [Relative degree](/relative-degree/): the first $k$ with $L_g L_f^{k} h \neq 0$, plus one.
- [Zero dynamics](/zero-dynamics/): the dynamics that remain when the Lie derivatives of the output are held at zero.
- [Observability](/observability/): for nonlinear systems, observability at a point is tested with the differentials of $h, L_f h, L_f^2 h, \dots$.
- [Lyapunov function](/lyapunov-function/): a function whose Lie derivative along the system is negative.
- [Gradient](/gradient/): $L_f h$ is the inner product of the gradient of $h$ with $f$.

## References
