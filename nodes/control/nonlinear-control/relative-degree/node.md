---
tag: 1JKEF2
kind: definition
slug: relative-degree
name: Relative degree
aliases:
- relative degree of a nonlinear system
area: control/nonlinear-control
level: core
summary: "The number r of times the output must be differentiated before the input appears: L_g L_f^k h = 0 near x0 for k < r - 1 and L_g L_f^(r-1) h(x0) is not 0. It may not exist at some points."
prereqs: [lie-derivative, transfer-function]
see_also: [lie-derivative, zero-dynamics, input-output-linearization, feedback-linearizability-conditions, markov-parameters, transfer-function, poles-and-zeros, lie-bracket]
sources:
  - book: isbn:9783540199168
    title: Alberto Isidori, Nonlinear Control Systems, third edition, Springer, 1995
    locator: Chapter 4 (Nonlinear feedback for single-input single-output systems), the definition of the relative degree and the lemma on the independence of dh, ..., dL_f^(r-1) h; Chapter 5 for the vector relative degree
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 13.2, Input-Output Linearization
  - book: isbn:9780130408907
    title: Jean-Jacques E. Slotine and Weiping Li, Applied Nonlinear Control, Prentice Hall, 1991
    locator: Chapter 6; the relative degree first appears in Section 6.1.3 (input-output linearization)
---

The relative degree of a system with input $u$ and output $y$ is the number of times one must differentiate $y$ before $u$ appears in the result. For a linear system it is the difference between the degree of the denominator and the degree of the numerator of the [transfer function](/transfer-function/). For a nonlinear [control-affine system](/control-affine-system/) it is defined with [Lie derivatives](/lie-derivative/), and it is a local property: it is defined at a point, and it may not exist at some points. When it exists, it is the number of integrators between the input and the output after a change of coordinates and a feedback. It tells [input-output linearization](/input-output-linearization/) how many derivatives to take, and it splits the state into $r$ coordinates that the output controls and $n - r$ coordinates that form the [zero dynamics](/zero-dynamics/).

## Definition

**Setting.** The system is

$$\dot x = f(x) + g(x)\, u, \qquad y = h(x),$$

with $x \in U$, an open subset of $\mathbb{R}^n$, a scalar input $u$ and a scalar output $y$. The fields $f$, $g$ and the function $h$ are smooth ($C^\infty$) on $U$. Smoothness makes $f + g u$ locally Lipschitz for each fixed $u$, so solutions exist and are unique by the [Picard-Lindelöf theorem](/picard-lindelof-theorem/).

The system has **relative degree $r$ at $x_0 \in U$** if

1. $L_g L_f^k h(x) = 0$ for all $x$ in a neighborhood of $x_0$ and all $k = 0, \dots, r - 2$, and
2. $L_g L_f^{r-1} h(x_0) \neq 0$.

If $r$ exists, it is unique. If it exists at $x_0$, it exists and has the same value at all points near $x_0$, because $L_g L_f^{r-1} h$ is continuous. The system has relative degree $r$ **on a set** if it has relative degree $r$ at each point of the set.

**What it means.** Let $r$ be the relative degree at $x_0$. Near $x_0$, along any solution,

$$y^{(k)} = L_f^k h(x) \quad (k = 0, \dots, r - 1), \qquad y^{(r)} = L_f^r h(x) + L_g L_f^{r-1} h(x)\, u .$$

So $r$ is the first derivative of $y$ in which $u$ appears, and it appears there with a coefficient that is not zero.

**Bound.** If the relative degree $r$ exists at $x_0$, then $r \le n$, and the row vectors $dh(x_0), dL_f h(x_0), \dots, dL_f^{r-1} h(x_0)$ are linearly independent. The proof uses the identity

$$L_{\mathrm{ad}_f^j g} L_f^i h = \begin{cases} 0 & i + j \le r - 2, \\ (-1)^j L_g L_f^{r-1} h & i + j = r - 1, \end{cases}$$

which follows from $L_{[f,g]} = L_f L_g - L_g L_f$ by induction on $j$ (see the [Lie bracket](/lie-bracket/)). Then the $r \times r$ matrix with entries $dL_f^i h(x_0) \cdot \mathrm{ad}_f^j g(x_0)$ is zero above its anti-diagonal and has nonzero entries on it, so it has rank $r$, and so do its $r$ rows $dL_f^i h(x_0)$. The full proof is on the [input-output linearization](/input-output-linearization/) page, in its proof of correctness. A consequence: if $L_g L_f^k h = 0$ near $x_0$ for $k = 0, \dots, n - 1$, then no point near $x_0$ has a relative degree. Some books then say that the relative degree is infinite.

**Invariance.** The relative degree does not change under a change of coordinates $z = T(x)$, and it does not change under a feedback $u = \alpha(x) + \beta(x) v$ with $\beta(x) \neq 0$. For the feedback, $L_{f + g\alpha}^k h = L_f^k h$ for $k \le r - 1$, and $L_{g\beta} L_{f+g\alpha}^{r-1} h = \beta\, L_g L_f^{r-1} h$.

**Several inputs and outputs.** For $m$ inputs and $m$ outputs, the system has **vector relative degree** $(r_1, \dots, r_m)$ at $x_0$ if $L_{g_j} L_f^k h_i = 0$ near $x_0$ for all $j$ and all $k < r_i - 1$, and the $m \times m$ decoupling matrix with entries $L_{g_j} L_f^{r_i - 1} h_i(x_0)$ is nonsingular. Isidori treats this case in Chapter 5.

## Examples and non-examples

**Linear system.** For $f(x) = A x$, $g = B$ and $h(x) = C x$, $L_g L_f^k h = C A^k B$, a constant. So $r$ is the first $k$ with $C A^{k-1} B \neq 0$, and it is the same at every point. The numbers $C A^{k-1} B$ are the [Markov parameters](/markov-parameters/), the coefficients of $G(s) = C (sI - A)^{-1} B = \sum_{k \ge 1} C A^{k-1} B\, s^{-k}$. So $r$ is the degree of the denominator minus the degree of the numerator of $G$. For $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ and $C = \begin{bmatrix} -1 & 1 \end{bmatrix}$, $C B = 1$, so $r = 1$, and indeed $G(s) = (s - 1)/(s^2 + 3 s + 2)$.

**A nonlinear system with $r = 2$ everywhere.** Take $\dot x_1 = x_2$, $\dot x_2 = x_1 x_3 - x_2^3 + (1 + x_1^2) u$, $\dot x_3 = -x_3 + x_1^2$ and $y = x_1$. Then $L_g h = 0$ and $L_g L_f h = 1 + x_1^2 > 0$, so $r = 2$ at every point. The third state does not appear in $y$, $\dot y$ or the coefficient of $u$; it is the internal state that the [zero dynamics](/zero-dynamics/) describe.

**Pendulum with a torque.** For $\dot x_1 = x_2$, $\dot x_2 = -\sin x_1 + u$, the output $y = x_1$ (the angle) has $r = 2 = n$, and the output $y = x_2$ (the angular velocity) has $r = 1$. The relative degree depends on the output, not only on the system.

**Undefined at some points.** Let $f(x) = (x_2, 0)$, $g(x) = (x_1, 1)$ and $h(x) = x_1$. Then $L_g h = x_1$. At $x_0 = (1, 0)$ it is not zero, so $r = 1$. At $x_0 = (0, 1)$ it is zero, but it is not zero on any neighborhood of $x_0$. So condition 1 fails for every $r \ge 2$, and condition 2 fails for $r = 1$. No relative degree exists at the points with $x_1 = 0$.

**Different from the linearization.** Take $\dot x_1 = x_2 + x_3^2$, $\dot x_2 = x_3$, $\dot x_3 = u$ and $y = x_1$. The [Jacobian linearization](/jacobian-linearization/) at $0$ is a chain of three integrators with relative degree $3$. But $L_g h = 0$ and $L_g L_f h = 2 x_3$, which is zero at $0$ and not zero near $0$. So the nonlinear system has no relative degree at $0$.

**Non-example: no input effect.** For $\dot x_1 = u$, $\dot x_2 = -x_2$ and $y = x_2$, all $L_g L_f^k h$ are zero. The input never reaches the output, and no relative degree exists anywhere.

## Related definitions

- [Lie derivative](/lie-derivative/): the derivatives $L_f^k h$ and $L_g L_f^k h$ in the definition.
- [Zero dynamics](/zero-dynamics/): the $n - r$ dimensional dynamics that remain when $y$ is held at zero.
- [Input-output linearization](/input-output-linearization/): the algorithm that finds $r$ and uses it.
- [Conditions for feedback linearizability](/feedback-linearizability-conditions/): a system is feedback linearizable if and only if some output has relative degree $n$.
- [Transfer function](/transfer-function/) and [poles and zeros](/poles-and-zeros/): the linear relative degree is the pole excess.

## References
