---
tag: VH21RF
kind: algorithm
slug: input-output-linearization
name: Input-output linearization
aliases:
- input-output feedback linearization
area: control/nonlinear-control
level: core
summary: "Differentiates the output until the input appears, at the relative degree r, and sets u = (v - L_f^r h) / (L_g L_f^(r-1) h), so that y^(r) = v. The zero dynamics must be checked apart."
solves: [output-regulation-problem]
model: real-ram
complexity:
  vars: {n: the number of states, p: the largest number of terms of a function L_f^k h for k at most r, q: the largest number of terms of an entry of f or g (operations on exact rationals at unit cost)}
  time: {worst: "O(n^3 p q)"}
  space: {extra: "O(n^2 p)"}
properties: {deterministic: true, exact: true, recursive: false, online: false}
history:
  year: 1981
  people: [Alberto Isidori, Arthur J. Krener, Claudio Gori-Giorgi, Salvatore Monaco]
  note: "Isidori, Krener, Gori-Giorgi and Monaco (1981) solved nonlinear decoupling by feedback with differential geometric tools; the normal form and the zero dynamics of Byrnes and Isidori made the method complete for single-input single-output systems."
prereqs: [relative-degree, zero-dynamics, lie-derivative]
see_also: [feedback-linearization, relative-degree, zero-dynamics, computed-torque-control, backstepping, sliding-mode-control, high-gain-observer, jacobian-linearization]
sources:
  - book: isbn:9783540199168
    title: Alberto Isidori, Nonlinear Control Systems, third edition, Springer, 1995
    locator: Chapter 4 (Nonlinear feedback for single-input single-output systems), the normal form, the zero dynamics and asymptotic output tracking; Chapter 5 for several inputs and outputs
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 13.2, Input-Output Linearization, and Section 13.4, State Feedback Control (stabilization and tracking)
  - book: isbn:9780130408907
    title: Jean-Jacques E. Slotine and Weiping Li, Applied Nonlinear Control, Prentice Hall, 1991
    locator: Chapter 6, Feedback Linearization; Section 6.1.3 for the idea of input-output linearization
  - paper: "A. Isidori, A. J. Krener, C. Gori-Giorgi and S. Monaco, Nonlinear decoupling via feedback: a differential geometric approach, IEEE Transactions on Automatic Control 26(2), 331-345, 1981"
    title: "Nonlinear decoupling via feedback: a differential geometric approach"
    locator: the decoupling problem for systems with several inputs and outputs, solved with the derivatives of the outputs along the system
  - paper: "C. I. Byrnes and A. Isidori, Asymptotic stabilization of minimum phase nonlinear systems, IEEE Transactions on Automatic Control 36(10), 1122-1137, 1991"
    title: Asymptotic stabilization of minimum phase nonlinear systems
    locator: the minimum phase condition that makes the cancelling feedback safe for the internal state
---

Input-output linearization is a feedback design for a nonlinear [control-affine system](/control-affine-system/) $\dot x = f(x) + g(x) u$ with output $y = h(x)$. It differentiates the output along the system, with [Lie derivatives](/lie-derivative/), until the input appears. This happens at the [relative degree](/relative-degree/) $r$, where $y^{(r)} = L_f^r h(x) + L_g L_f^{r-1} h(x)\, u$. Then the feedback $u = (v - L_f^r h(x)) / L_g L_f^{r-1} h(x)$ cancels the nonlinear terms and leaves $y^{(r)} = v$, a chain of $r$ integrators from the new input $v$ to the output. A linear law for $v$ then places the poles of the tracking error. The method is exact, not an approximation around a point, but it is local: it needs a relative degree, and it needs $L_g L_f^{r-1} h \neq 0$ along the motion. It also hides $n - r$ states from the output. Their behavior is given by the [zero dynamics](/zero-dynamics/), and the method is safe only when these are stable.

## In plain words

Take the output and ask how it changes. If the input does not appear in its rate of change, ask how that rate changes, and so on. After a few steps the input appears, multiplied by some factor and added to other terms that depend on the state. Choose the input so that it removes those other terms and divides out the factor. What is left is a very simple machine: the output is the input passed through a fixed number of integrators. That machine is easy to control with the usual linear tools. The price is that some parts of the state are no longer visible in the output. Before you use the method, check that those hidden parts settle by themselves, or the output will look fine while the state runs away.

## The problem

**Input.** Smooth $f$, $g : U \to \mathbb{R}^n$ and $h : U \to \mathbb{R}$ on an open set $U \subseteq \mathbb{R}^n$, and a point $x_0 \in U$. Smoothness makes $f + g u$ locally Lipschitz, so the solutions exist and are unique by the [Picard-Lindelöf theorem](/picard-lindelof-theorem/). For the control law, also a reference $y_d(t)$ with $r$ continuous derivatives, and real numbers $c_0, \dots, c_{r-1}$ such that $s^r + c_{r-1} s^{r-1} + \dots + c_0$ is Hurwitz.

**Output.** One of three answers:

- the relative degree $r$ at $x_0$, the functions $\xi_i = L_f^i h$ for $i = 0, \dots, r - 1$, $a = L_g L_f^{r-1} h$ with $a(x_0) \neq 0$, and $b = L_f^r h$, together with the feedback $u(t, x)$ that makes the tracking error $e = y - y_d$ obey $e^{(r)} + c_{r-1} e^{(r-1)} + \dots + c_0 e = 0$;
- UNDEFINED, if no relative degree exists at $x_0$;
- NO INPUT EFFECT, if $L_g L_f^k h = 0$ near $x_0$ for all $k < n$, so the input does not reach the output.

This is output tracking with a known reference and known derivatives, a special case of the [output regulation problem](/output-regulation-problem/). The algorithm makes the error equation linear. Internal stability of the other states is a separate condition.

## The algorithm

```pseudo id=main
IO-LINEARIZE(f, g, h, x0)
L1  φ ← h; ξ ← empty list
L2  for k ← 0 to n - 1
L3      append φ to ξ                         ▷ now ξ[k] = L_f^k h
L4      a ← L_g φ
L5      if a(x0) ≠ 0
L6          b ← L_f φ
L7          return (r = k + 1, ξ, a, b)
L8      if a is not zero near x0 then return UNDEFINED
L9      φ ← L_f φ
L10 return NO INPUT EFFECT
CONTROL(t, x)                                 ▷ uses r, ξ, a, b, c, y_d
L11 v ← y_d^(r)(t) - Σ_{i<r} c_i (ξ[i](x) - y_d^(i)(t)); return u = (v - b(x)) / a(x)
```

Lines L2 to L9 compute the output derivatives one by one. At the start of pass $k$, $\varphi = L_f^k h$, and every earlier $L_g L_f^j h$ vanishes near $x_0$. So $y^{(k)} = \varphi(x)$, and $y^{(k+1)} = L_f \varphi(x) + L_g \varphi(x)\, u$. Line L4 takes the coefficient of $u$. If it is not zero at $x_0$ (line L5), the relative degree is $k + 1$ and line L6 takes the rest of the derivative. If it is zero at $x_0$ but not on a neighborhood of $x_0$ (line L8), no relative degree exists at $x_0$. Otherwise the input does not appear yet, and line L9 moves to the next derivative. The loop stops after $n$ passes at most, because a relative degree is never larger than $n$.

Line L11 is the control law. It sets $y^{(r)} = v$ and chooses $v$ as the reference term $y_d^{(r)}$ plus a linear feedback of the errors $e^{(i)} = \xi[i](x) - y_d^{(i)}(t)$. It divides by $a(x)$, so it is valid only while $a(x) \neq 0$.

The implementation works with polynomial $f$, $g$ and $h$ with exact rational coefficients, and it differentiates exactly. For a polynomial, "zero near $x_0$" is the same as "the zero polynomial", so the test at line L8 is exact. With general smooth functions, the test needs symbolic computation or a proof by hand.

## Example

Take the system with three states

$$\dot x_1 = x_2, \qquad \dot x_2 = x_1 x_3 - x_2^3 + (1 + x_1^2)\, u, \qquad \dot x_3 = -x_3 + x_1^2, \qquad y = x_1,$$

and $x_0 = 0$. The algorithm runs as follows.

| pass $k$ | $\varphi$ (line L3) | $a = L_g \varphi$ (line L4) | $a(x_0)$ | action |
|---|---|---|---|---|
| 0 | $x_1$ | $0$ | $0$ | $a$ is the zero polynomial, line L9: $\varphi \leftarrow x_2$ |
| 1 | $x_2$ | $1 + x_1^2$ | $1$ | line L6: $b = x_1 x_3 - x_2^3$, return $r = 2$ |

So $r = 2$, $\xi = (x_1, x_2)$, $a = 1 + x_1^2$ and $b = x_1 x_3 - x_2^3$. Because $a \ge 1$ everywhere, the law at line L11 is defined at every state. The third state is internal. With $y$ held at zero it obeys $\dot x_3 = -x_3$, so the system is minimum phase.

Choose $c_0 = 2$ and $c_1 = 3$, so the error polynomial is $s^2 + 3 s + 2 = (s + 1)(s + 2)$, and track $y_d = \sin t$. Line L11 becomes

$$u = \frac{-\sin t - 2 (x_1 - \sin t) - 3 (x_2 - \cos t) - x_1 x_3 + x_2^3}{1 + x_1^2}.$$

Start at $x(0) = (1, 0, 0)$. Then $e(0) = 1$ and $\dot e(0) = 0 - 1 = -1$, and the solution of $\ddot e + 3 \dot e + 2 e = 0$ is exactly $e(t) = e^{-t}$. A 4th order Runge-Kutta simulation with step $0.01$, with the feedback evaluated inside the right side, gives:

| $t$ | $x_1$ | $x_2$ | $x_3$ | $e = x_1 - \sin t$ | $u$ |
|---|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 1 | 0.5 |
| 1 | 1.20935 | 0.17242 | 0.78337 | 0.36788 | -0.57495 |
| 2 | 1.04463 | -0.55148 | 1.16292 | 0.13534 | -1.03120 |
| 3 | 0.19091 | -1.03978 | 0.68541 | 0.04979 | -1.29899 |
| 4 | -0.73849 | -0.67196 | 0.38791 | 0.01832 | 0.49061 |
| 5 | -0.95219 | 0.27692 | 0.70636 | 0.00674 | 0.87036 |

The error column is $e^{-t}$: $0.36788 = e^{-1}$, $0.13534 = e^{-2}$, and so on. Over the whole run, $x_1$ differs from $\sin t + e^{-t}$ by at most $4 \cdot 10^{-10}$, which is the error of the integrator. The internal state $x_3$ stays bounded, because it is driven by $x_1^2$ through the stable dynamics $\dot x_3 = -x_3$.

## Correctness

The full proof is in proofs/correctness.md. Its main steps:

- **Termination.** The loop runs at most $n$ times.
- **The three answers are right.** At the start of pass $k$, $\varphi = L_f^k h$ and $L_g L_f^j h$ vanishes near $x_0$ for $j < k$. A return at line L7 then matches the definition of the relative degree. A return at line L8 is right, because no $r$ can satisfy the definition when $L_g L_f^k h$ is zero at $x_0$ but not near it. A return at line L10 is right, because a relative degree is at most $n$. That bound comes from the identity $L_{\mathrm{ad}_f^j g} L_f^i h = (-1)^j L_g L_f^{r-1} h$ for $i + j = r - 1$ (and $0$ for $i + j < r - 1$), proved by induction on $j$ with $L_{[f,g]} = L_f L_g - L_g L_f$. It makes an $r \times r$ matrix of rank $r$ that factors through $\mathbb{R}^n$.
- **The closed loop.** While the state stays where $a \neq 0$ and the lower $L_g L_f^k h$ vanish, $y^{(i)} = \xi[i](x)$ for $i < r$ and $y^{(r)} = b(x) + a(x) u = v$. So the error obeys $e^{(r)} + c_{r-1} e^{(r-1)} + \dots + c_0 e = 0$.

The tests check the example, compare $r$, $a$ and $b$ with the Markov parameters $C A^{k} B$ and the rows $C A^r$ for 60 random integer linear systems, check the Lie derivative against the slope of $h(x_0 + t f(x_0))$ and the bracket identity on random polynomials, and check that the simulated error equals $e^{-t}$ within $10^{-8}$.

## Complexity

Count operations on exact rationals as unit cost, as in the real RAM. A polynomial with $p$ terms in $n$ variables takes $O(n p)$ space, for its exponent vectors.

- **One Lie derivative.** $L_f \varphi = \sum_i \frac{\partial \varphi}{\partial x_i} f_i$ takes $n$ partial derivatives, $O(n p)$ each, and $n$ products of a polynomial with at most $p$ terms by one with at most $q$ terms. Each product forms $p q$ exponent vectors of length $n$. So one Lie derivative costs $O(n^2 p q)$.
- **The loop.** Each pass computes at most two Lie derivatives and one evaluation at $x_0$, which costs $O(n p)$. There are at most $n$ passes, so the time is $O(n^3 p q)$.
- **Space.** The list $\xi$ holds at most $n$ polynomials of at most $p$ terms, so $O(n^2 p)$.
- **The control law.** Line L11 evaluates $r + 2$ polynomials, $O(n^2 p)$ per sample for the polynomial representation.

The number $p$ is the weak point. Each Lie derivative multiplies by the entries of $f$, so the degree grows with $k$ and the number of terms can grow fast. This is [expression swell](/expression-swell/). A [sparse polynomial](/sparse-polynomial/) representation, as here, helps when the system has few terms. Coefficient sizes of the exact rationals can also grow, which the unit cost model hides.

## Properties

- **Exact, not approximate.** The cancellation holds on a whole region, not only at $x_0$, unlike a design on the [Jacobian linearization](/jacobian-linearization/).
- **Local.** It needs the relative degree to exist and $a(x) \neq 0$ along the motion. In the example $a \ge 1$, so the result is global for the output.
- **Model based.** The feedback cancels $b(x)$ and divides by $a(x)$. Model errors leave terms that the linear law for $v$ must tolerate.
- **Blind to the internal state.** The closed loop has the zero dynamics as an unobservable part. The output behaves well whatever these do.
- **Invariant.** The relative degree, $a(x_0) \neq 0$ and the zero dynamics do not depend on the choice of coordinates.

## Variants and improvements

- **Full-state linearization.** If $r = n$, there are no internal states. The coordinates $(h, L_f h, \dots, L_f^{n-1} h)$ and the same feedback make the whole system linear. This is the case of [feedback linearization](/feedback-linearization/), and the [conditions for feedback linearizability](/feedback-linearizability-conditions/) say when some output with $r = n$ exists.
- **Several inputs and outputs.** With $m$ inputs and $m$ outputs, take $r_i$ derivatives of $y_i$. If the $m \times m$ decoupling matrix $L_{g_j} L_f^{r_i - 1} h_i$ is nonsingular, one feedback makes each output a separate chain of integrators. This is noninteracting control (Isidori, Chapter 5). When the matrix is singular, dynamic extension adds integrators at the inputs and can make it nonsingular.
- **Robot arms.** For $M(q) \ddot q + C(q, \dot q) \dot q + G(q) = \tau$ with output $q$, every joint has relative degree 2, and the decoupling matrix is $M(q)^{-1}$, which is always invertible. The feedback is the [computed torque method](/computed-torque-control/).
- **Output feedback.** The law needs $\xi = (y, \dot y, \dots, y^{(r-1)})$. A [high-gain observer](/high-gain-observer/) estimates these derivatives from $y$.
- **Robust versions.** [Sliding mode control](/sliding-mode-control/) uses the same normal form with a switching law that tolerates bounded model errors. [Backstepping](/backstepping/) avoids cancelling useful terms and handles systems in strict feedback form.

## When to use it

Use it when the model is accurate, the relative degree is defined on the whole operating region, $L_g L_f^{r-1} h$ stays away from zero there, and the system is minimum phase for the chosen output. Then it gives the same error dynamics at every operating point, which a design on one Jacobian linearization cannot.

Prefer a linear design on the Jacobian linearization when the state stays near one equilibrium. Prefer [sliding mode control](/sliding-mode-control/) or [backstepping](/backstepping/) when the model has large errors or when some nonlinear terms help stability and should not be cancelled. Prefer [nonlinear MPC](/nonlinear-mpc/) when input or state limits matter, since the cancelling input can be large. For a non-minimum phase output, do not use it directly: choose another output, or use a method that accounts for the zero dynamics.

## Pitfalls

- **Testing only at the point.** If line L8 is left out, a coefficient that is zero at $x_0$ but not near it is skipped. For $\dot x_1 = x_2 + x_3^2$, $\dot x_2 = x_3$, $\dot x_3 = u$, $y = x_1$, pass 1 has $a = 2 x_3$ with $a(0) = 0$, and the loop without line L8 goes on to report $r = 3$ with $a = 1$. But near $0$ the input already appears in $\ddot y = x_3 + 2 x_3 u$, so the feedback is wrong. Keep line L8: it returns UNDEFINED here.
- **Finite differences.** Computing lines L4, L6 and L9 with difference quotients loses accuracy at each level, and the test at line L5 then compares noise with zero. Differentiate exactly (symbolic or automatic differentiation), as the implementation does.
- **Ignoring the zero dynamics.** Line L11 makes the output follow $y_d$ whatever the internal state does. For $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $C = \begin{bmatrix} -1 & 1 \end{bmatrix}$, with $G(s) = (s - 1)/(s^2 + 3 s + 2)$, $r = 1$ and the zero dynamics are $\dot\eta = \eta$. Holding $y = 0$ makes $x_1$ grow like $e^t$. Check the zero dynamics before you apply line L11.
- **Division by a small $a(x)$.** Line L11 divides by $a(x)$. If the motion approaches a point where $a = 0$, the input grows without bound. The result holds only on the region where $a \neq 0$. Keep the motion away from the singular set, or saturate and accept the loss of exactness.
- **Sampled implementation.** The proof assumes that line L11 is evaluated continuously. If $u$ is computed at samples and held, the cancellation is not exact. In the example, with the input held over each RK4 step of $0.01$, the deviation of $x_1$ from $\sin t + e^{-t}$ reaches $0.0032$; with a hold of $0.05$ it reaches $0.016$. The error still decays, but it no longer equals $e^{-t}$.

## Implementations

## History

The computed torque method for robot arms uses the same cancellation in a special case. Isidori, Krener, Gori-Giorgi and Monaco (1981) solved the nonlinear decoupling problem by feedback with the tools of differential geometry, and the paper led to the idea of the zeros of a nonlinear system. Byrnes and Isidori then introduced the normal form and the zero dynamics, and their 1991 paper stated the minimum phase condition under which the cancelling feedback stabilizes the whole state. The method is standard in the textbooks of Isidori (1995, Chapter 4), Slotine and Li (1991, Chapter 6) and Khalil (2002, Chapter 13).

## References
