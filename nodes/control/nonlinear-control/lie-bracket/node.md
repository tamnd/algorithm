---
tag: DBWSSW
kind: definition
slug: lie-bracket
name: Lie bracket of vector fields
aliases:
- Jacobi-Lie bracket
area: control/nonlinear-control
level: core
summary: "The vector field [f, g] = (Dg) f - (Df) g. It measures how the flows of f and g fail to commute, and it gives the directions that a control system can reach by switching."
prereqs: [lie-derivative]
see_also: [lie-derivative, feedback-linearizability-conditions, lie-algebra-rank-condition, kalman-rank-condition, controllability, unicycle-model, nonholonomic-constraint, brockett-condition]
sources:
  - book: isbn:9783540199168
    title: Alberto Isidori, Nonlinear Control Systems, third edition, Springer, 1995
    locator: Chapter 1 (Local decompositions of control systems), the Lie bracket, distributions and the theorem of Frobenius
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 13.3, Full-State Linearization, where the bracket, the ad notation and involutive distributions are defined
  - book: isbn:9780130408907
    title: Jean-Jacques E. Slotine and Weiping Li, Applied Nonlinear Control, Prentice Hall, 1991
    locator: Section 6.2, Mathematical Tools
  - book: isbn:9780387984896
    title: Eduardo D. Sontag, Mathematical Control Theory, Deterministic Finite Dimensional Systems, second edition, Springer, 1998
    locator: Chapter 4 (Nonlinear controllability), Lie brackets and accessibility
---

The Lie bracket of two vector fields $f$ and $g$ is a third vector field $[f, g]$. It measures how much the flows of $f$ and $g$ fail to commute. Move a short time $t$ along $f$, then $t$ along $g$, then $t$ back along $f$, then $t$ back along $g$. In general the state does not come back to its start. To second order in $t$ it ends at $x + t^2 [f, g](x)$. For a control system this means that switching between two inputs creates motion in a new direction, which neither input gives alone. Brackets are the main tool of geometric nonlinear control: they decide [feedback linearizability](/feedback-linearizability-conditions/) and local accessibility through the [Lie algebra rank condition](/lie-algebra-rank-condition/), and for linear systems they reduce to the columns of the controllability matrix of the [Kalman rank condition](/kalman-rank-condition/).

## Definition

Let $U \subseteq \mathbb{R}^n$ be open, and let $f, g : U \to \mathbb{R}^n$ be smooth vector fields. The **Lie bracket** of $f$ and $g$ is the vector field

$$[f, g](x) = \frac{\partial g}{\partial x}(x)\, f(x) - \frac{\partial f}{\partial x}(x)\, g(x),$$

where $\frac{\partial g}{\partial x}$ and $\frac{\partial f}{\partial x}$ are the Jacobian matrices. This is the sign used by Isidori and by Khalil. Some books use the opposite sign, $[f, g] = \frac{\partial f}{\partial x} g - \frac{\partial g}{\partial x} f$. The two conventions give the same span of brackets, so rank and involutivity tests do not change, but formulas with signs, such as the ones below, change. Check the convention before you copy a formula.

**Iterated brackets.** Repeated brackets with the same first field are written with the ad notation:

$$\mathrm{ad}_f^0 g = g, \qquad \mathrm{ad}_f^k g = [f, \mathrm{ad}_f^{k-1} g] \quad (k \ge 1).$$

**Action on functions.** For a smooth function $h$, with the [Lie derivative](/lie-derivative/) $L$,

$$L_{[f,g]} h = L_f L_g h - L_g L_f h .$$

The proof is the product rule: in $L_f L_g h - L_g L_f h$ the terms with second derivatives of $h$ cancel, because they are symmetric, and the rest is $\frac{\partial h}{\partial x}\left( \frac{\partial g}{\partial x} f - \frac{\partial f}{\partial x} g \right)$.

**Algebraic rules.** For fields $f$, $g$, $k$, real numbers $a$, $b$, and smooth functions $\alpha$, $\beta$:

- bilinear over the real numbers: $[a f + b g, k] = a [f, k] + b [g, k]$;
- antisymmetric: $[f, g] = -[g, f]$, so $[f, f] = 0$;
- the Jacobi identity: $[f, [g, k]] + [g, [k, f]] + [k, [f, g]] = 0$;
- with functions: $[\alpha f, \beta g] = \alpha \beta [f, g] + \alpha (L_f \beta)\, g - \beta (L_g \alpha)\, f$.

The last rule shows that the bracket is not linear over functions. So a change of feedback, which multiplies input fields by functions, changes the brackets, but only by terms in the span of the fields themselves.

**Flows.** Let $\Phi^f_t$ be the flow of $f$. Then

$$\Phi^g_{-t} \circ \Phi^f_{-t} \circ \Phi^g_{t} \circ \Phi^f_{t}(x) = x + t^2 [f, g](x) + O(t^3).$$

The flows of $f$ and $g$ commute near a point if and only if $[f, g] = 0$ near that point.

**Change of coordinates.** If $z = T(x)$ for a diffeomorphism $T$, and $\tilde f(z) = \frac{\partial T}{\partial x} f(x)$, $\tilde g(z) = \frac{\partial T}{\partial x} g(x)$ at $z = T(x)$, then $[\tilde f, \tilde g](z) = \frac{\partial T}{\partial x} [f, g](x)$. So brackets are geometric objects, and tests built from them do not depend on the coordinates.

**Distributions and involutivity.** A distribution $\Delta(x) = \mathrm{span}\{f_1(x), \dots, f_k(x)\}$ assigns a subspace to each point. It is **involutive** if $[f_i, f_j](x) \in \Delta(x)$ for all $i$, $j$ and all $x$. The theorem of Frobenius says that a distribution of constant dimension $k$ is involutive if and only if, near each point, it is the set of tangent vectors to the level sets of $n - k$ functions with independent differentials.

## Examples and non-examples

**Linear field and constant field.** Let $f(x) = A x$ and $g(x) = b$. Then $\frac{\partial g}{\partial x} = 0$ and $\frac{\partial f}{\partial x} = A$, so $[A x, b] = -A b$ and

$$\mathrm{ad}_{Ax}^k b = (-1)^k A^k b .$$

So the span of $g, \mathrm{ad}_f g, \dots, \mathrm{ad}_f^{n-1} g$ is the span of $b, A b, \dots, A^{n-1} b$, the columns of the controllability matrix. With the opposite sign convention the factor $(-1)^k$ goes away. For $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$ and $b = (0, 1)$, $[A x, b] = (-1, 3)$.

**Two linear fields.** For $f(x) = A x$ and $g(x) = B x$, $[f, g](x) = (B A - A B) x$. The flows $e^{At}$ and $e^{Bt}$ commute exactly when $A B = B A$.

**Nonholonomic integrator.** Let $g_1 = (1, 0, -x_2)$ and $g_2 = (0, 1, x_1)$ on $\mathbb{R}^3$. Then

$$\frac{\partial g_2}{\partial x} g_1 = (0, 0, 1), \qquad \frac{\partial g_1}{\partial x} g_2 = (0, 0, -1), \qquad [g_1, g_2] = (0, 0, 2).$$

The inputs move only $x_1$ and $x_2$ directly, but a small loop in the $(x_1, x_2)$ plane changes $x_3$ by twice the signed area of the loop. This is the model behind many [nonholonomic constraints](/nonholonomic-constraint/), and the standard example of [Brockett's condition](/brockett-condition/).

**Unicycle.** For the [unicycle](/unicycle-model/) $\dot p_1 = v \cos\theta$, $\dot p_2 = v \sin\theta$, $\dot\theta = \omega$, the fields are $g_1 = (\cos\theta, \sin\theta, 0)$ and $g_2 = (0, 0, 1)$ in the state $(p_1, p_2, \theta)$. Then $[g_1, g_2] = -\frac{\partial g_1}{\partial x} g_2 = (\sin\theta, -\cos\theta, 0)$, the sideways direction. A car can park sideways by switching between forward motion and turning.

**Drift and input.** For $\dot x_1 = x_2^2$, $\dot x_2 = u$, with $f = (x_2^2, 0)$ and $g = (0, 1)$: $[f, g] = (-2 x_2, 0)$ and $[g, [f, g]] = (-2, 0)$. The brackets span the plane at $x = 0$ even though $[f, g](0) = 0$.

**Non-example: coordinate fields.** The fields $f = (1, 0)$ and $g = (0, 1)$ have $[f, g] = 0$. Their flows commute, and no new direction appears. More generally, constant fields always have zero bracket.

**Non-example: a distribution that is not involutive.** For $f = (x_2 + x_3^2, x_3, 0)$ and $g = (0, 0, 1)$, $\mathrm{ad}_f g = (-2 x_3, -1, 0)$ and $[g, \mathrm{ad}_f g] = (-2, 0, 0)$. At $x = 0$ the span of $g$ and $\mathrm{ad}_f g$ is the $(x_2, x_3)$ plane, and $(-2, 0, 0)$ is not in it. So $\mathrm{span}\{g, \mathrm{ad}_f g\}$ is not involutive, and by the [conditions for feedback linearizability](/feedback-linearizability-conditions/) this system is not feedback linearizable.

## Related definitions

- [Lie derivative](/lie-derivative/): the bracket is the commutator of two Lie derivatives.
- [Conditions for feedback linearizability](/feedback-linearizability-conditions/): rank and involutivity of $\{g, \mathrm{ad}_f g, \dots\}$.
- [Lie algebra rank condition](/lie-algebra-rank-condition/): the brackets of all orders span the state space.
- [Relative degree](/relative-degree/): the identity $L_{\mathrm{ad}_f^j g} L_f^i h = (-1)^j L_g L_f^{r-1} h$ for $i + j = r - 1$ links brackets and output derivatives.
- [Controllability](/controllability/) and the [Kalman rank condition](/kalman-rank-condition/): the linear case of the bracket tests.

## References
