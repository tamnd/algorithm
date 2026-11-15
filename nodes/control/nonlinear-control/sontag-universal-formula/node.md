---
tag: B75HKW
kind: algorithm
slug: sontag-universal-formula
name: Sontag's universal formula
aliases:
- Sontag's formula
area: control/nonlinear-control
level: advanced
summary: Gives an explicit stabilizing feedback from a control Lyapunov function, smooth away from the origin.
model: real-ram
complexity:
  vars: {n: the number of states, m: the number of inputs}
  time: {worst: "O(n m)"}
  space: {extra: "O(m)"}
properties: {deterministic: true, exact: true, recursive: false, online: true}
history:
  year: 1989
  people: [Eduardo D. Sontag]
  note: "Artstein (1983) proved that a control Lyapunov function gives a stabilizing feedback but gave no formula. Sontag (1989) gave the explicit formula and showed that it is real-analytic away from the origin."
prereqs: [control-lyapunov-function, lie-derivative, control-affine-system]
see_also: [artstein-sontag-theorem, backstepping, cbf-safety-filter, lyapunov-direct-method, infinite-horizon-lqr, brockett-condition, input-to-state-stability, control-barrier-function]
sources:
  - paper: doi:10.1016/0167-6911(89)90028-5
    title: "Eduardo D. Sontag, A 'universal' construction of Artstein's theorem on nonlinear stabilization, Systems and Control Letters 13(2), 117-123, 1989"
    locator: the formula for control-affine systems and the proof that it is analytic where L_g V is not zero or L_f V is negative
  - book: isbn:9780387984896
    title: Eduardo D. Sontag, Mathematical Control Theory, second edition, Springer, 1998
    locator: Section 5.9 (Introduction to Nonlinear Stabilization), Proposition 5.9.10 and Exercise 5.9.11; Section 5.7 for control Lyapunov functions
  - book: isbn:9780471127321
    title: Miroslav Krstić, Ioannis Kanellakopoulos and Petar Kokotović, Nonlinear and Adaptive Control Design, Wiley, 1995
    locator: Section 2.1.2, Control Lyapunov functions
  - paper: doi:10.1137/S0363012993258732
    title: "Randy A. Freeman and Petar V. Kokotović, Inverse optimality in robust stabilization, SIAM Journal on Control and Optimization 34(4), 1365-1391, 1996"
    locator: robust control Lyapunov functions and the pointwise min-norm control laws
  - paper: "Y. Lin and E. D. Sontag, A universal formula for stabilization with bounded controls, Systems and Control Letters 16(6), 393-397, 1991"
    title: A universal formula for stabilization with bounded controls
    locator: the version of the formula with a bound on the norm of the input
  - paper: doi:10.1016/0362-546X(83)90049-4
    title: "Zvi Artstein, Stabilization with relaxed controls, Nonlinear Analysis: Theory, Methods and Applications 7(11), 1163-1173, 1983"
    locator: the existence result that the formula makes explicit
---

Sontag's universal formula turns a [control Lyapunov function](/control-lyapunov-function/) $V$ of a [control-affine system](/control-affine-system/) $\dot x = f(x) + g(x) u$ into a feedback $u = k(x)$ by one explicit expression in the two [Lie derivatives](/lie-derivative/) $L_f V$ and $L_g V$. The feedback makes $\dot V = -\sqrt{(L_f V)^2 + |L_g V|^4}$, which is negative at every nonzero state, and it is smooth everywhere except perhaps at the origin. It is the constructive half of [Artstein's theorem](/artstein-sontag-theorem/): Artstein proved that such a feedback exists, and the formula writes one down. The feedback is continuous at the origin exactly when $V$ has the small control property.

## In plain words

Suppose you already have an energy-like measure of how far the system is from rest, and you know that at every state some input can make that measure go down. You still need a rule that picks one input at each state. This rule is a single closed formula. At each state it looks at two numbers: how fast the measure changes when you do nothing, and how strongly the input can push the measure. If doing nothing already lowers the measure, the rule applies only a small push. If doing nothing raises it, the rule pushes hard against it. The rule never divides by zero in a bad way, it changes smoothly from state to state, and it always makes the measure fall. You do not tune anything. All the design work is in the choice of the measure.

## The problem

**Input.** Smooth maps $f : \mathbb{R}^n \to \mathbb{R}^n$ and $g : \mathbb{R}^n \to \mathbb{R}^{n \times m}$ with $f(0) = 0$, and a smooth, positive definite and proper (radially unbounded) function $V : \mathbb{R}^n \to \mathbb{R}$ that is a control Lyapunov function: at every $x \neq 0$, $L_g V(x) = 0$ implies $L_f V(x) < 0$. Smoothness makes $f + g k$ locally Lipschitz wherever $k$ is smooth, so solutions exist and are unique there (see the [Lipschitz condition](/lipschitz-condition/) and the [Picard-Lindelöf theorem](/picard-lindelof-theorem/)). Here $L_f V = \nabla V \cdot f$ is a number and $L_g V = \nabla V\, g$ is a row of $m$ numbers.

**Output.** A feedback $k : \mathbb{R}^n \to \mathbb{R}^m$ with $k(0) = 0$ such that

- $k$ is smooth on $\mathbb{R}^n \setminus \{0\}$;
- along $\dot x = f(x) + g(x) k(x)$, $\dot V(x) < 0$ for every $x \neq 0$;
- if $V$ also has the small control property, $k$ is continuous at $0$ and the origin of the closed loop is globally asymptotically stable.

The small control property says: for every $\varepsilon > 0$ there is a $\delta > 0$ such that each $x$ with $0 < |x| < \delta$ has some input $u$ with $|u| < \varepsilon$ and $L_f V(x) + L_g V(x) u < 0$. Norms here are Euclidean.

## The algorithm

```pseudo id=main
SONTAG(x)                                   ▷ f, g and ∇V are given
L1  a ← ∇V(x) · f(x)                        ▷ L_f V(x), a number
L2  b ← ∇V(x) g(x)                          ▷ L_g V(x), a row of m numbers
L3  β ← b b^T                               ▷ |b|^2
L4  if β = 0 then return u = 0
L5  s ← sqrt(a^2 + β^2); if a > 0 then φ ← (a + s)/β else φ ← β/(s - a)
L6  return u = -φ b^T
```

Lines L1 and L2 evaluate the two Lie derivatives at the current state. If the input has no effect on $V$ at this state (line L4), the formula returns zero; for a control Lyapunov function this happens only where the drift already lowers $V$. Otherwise line L5 computes the scalar gain

$$\varphi(a, \beta) = \frac{a + \sqrt{a^2 + \beta^2}}{\beta},$$

and line L6 pushes along $-b^T$, the direction in which the input lowers $V$ fastest. The two branches at line L5 are equal, because $(a + s)(s - a) = s^2 - a^2 = \beta^2$. The second branch avoids the cancellation in $a + s$ when $a$ is negative.

The gain $\varphi$ is the positive root of $\beta p^2 - 2 a p - \beta = 0$. With $u = -\varphi b^T$,

$$\dot V = a + b u = a - \varphi \beta = -\sqrt{a^2 + \beta^2}.$$

So the closed loop lowers $V$ at least at the rate $|a|$ and at least at the rate $\beta$. When the drift helps ($a < 0$ and $\beta$ small) the gain is $\varphi \approx \beta / (2 |a|)$, which is small. When the drift hurts ($a > 0$) the gain is about $2 a / \beta$, enough to cancel the drift twice over.

## Example

**The check value.** Take $\dot x = x + u$ and $V = x^2 / 2$. Then $a = x^2$, $b = x$ and $\beta = x^2$. Line L5 gives $\varphi = (x^2 + \sqrt{2} x^2)/x^2 = 1 + \sqrt 2$, so $u = -(1 + \sqrt 2) x$ and the closed loop is $\dot x = -\sqrt 2\, x$. For $\dot x = c x + u$ the same steps give $u = -(c + \sqrt{c^2 + 1}) x$, which is the [LQR gain](/infinite-horizon-lqr/) of the scalar Riccati equation $2 c P - P^2 + 1 = 0$. For $c = 1$ this is $P = 1 + \sqrt 2$.

**A nonlinear system.** Take

$$\dot x_1 = -x_1 + x_1^2 x_2, \qquad \dot x_2 = u, \qquad V = \tfrac12 (x_1^2 + x_2^2).$$

Then $a = -x_1^2 + x_1^3 x_2 = x_1^2 (x_1 x_2 - 1)$ and $b = x_2$. Where $b = 0$, $a = -x_1^2 < 0$ for $x_1 \neq 0$, so $V$ is a control Lyapunov function on the whole plane. The drift raises $V$ only where $x_1 x_2 > 1$. Start at $x(0) = (2, 1)$, where $a = 4$, $b = 1$ and line L5 gives $\varphi = 4 + \sqrt{17}$, so $u(0) = -8.12311$ and $\dot V(0) = -\sqrt{17} = -4.12311$. A 4th order Runge-Kutta simulation with step $0.01$, with the feedback evaluated inside the right side, gives:

| $t$ | $x_1$ | $x_2$ | $u$ | $V$ |
|---|---|---|---|---|
| 0 | 2 | 1 | -8.12311 | 2.5 |
| 0.5 | 2.03195 | 0.42643 | -0.06851 | 2.15533 |
| 1 | 1.84232 | 0.40220 | -0.03669 | 1.77796 |
| 2 | 1.23857 | 0.37134 | -0.03069 | 0.83597 |
| 4 | 0.26436 | 0.25125 | -0.10165 | 0.06651 |
| 6 | 0.03733 | 0.07237 | -0.05567 | 0.00332 |
| 8 | 0.00506 | 0.01374 | -0.01200 | 0.000107 |
| 10 | 0.00068 | 0.00229 | -0.00209 | 0.0000028 |

In the first half second the input is large, because the drift pushes $V$ up and the formula pushes $x_2$ down until $x_1 x_2 < 1$. After that the drift lowers $V$ by itself, and the input stays small. $V$ decreases at every one of the 1000 steps. Near the origin $x_1 x_2 < 1$, so $a \le 0$ and $|u| = \varphi |b| \le |b| = |x_2|$; this is why the feedback is continuous at $0$ here.

## Correctness

The full proof is in proofs/correctness.md. Its main steps:

- **The derivative.** With $u = k(x)$, $\dot V = -\sqrt{a^2 + \beta^2}$ when $\beta > 0$ and $\dot V = a$ when $\beta = 0$. For a control Lyapunov function both are negative at $x \neq 0$.
- **Smooth away from the origin.** On the open set $S = \{\beta > 0 \text{ or } a < 0\}$, $\varphi$ is the root of $\beta p^2 - 2 a p - \beta = 0$ at which the derivative in $p$ is $2 \sqrt{a^2 + \beta^2} > 0$ (or $-2a > 0$ on $\beta = 0$). The implicit function theorem makes $\varphi$ real-analytic on $S$. A control Lyapunov function keeps $(a(x), \beta(x))$ in $S$ for $x \neq 0$, so $k$ is smooth there.
- **Continuity at the origin.** If $a \le 0$, $\varphi \le 1$ and $|k| \le |b|$. If $a > 0$, the small control property gives $a < \varepsilon |b|$, and then $|k| < 2 \varepsilon + |b|$. Since $b(0) = 0$, $k(x) \to 0$. Conversely, if $k$ is continuous at $0$, the input $k(x)$ itself shows the small control property.
- **Global asymptotic stability.** With the small control property, the closed loop is continuous, solutions are unique, and $V$ is a Lyapunov function in the sense of [Lyapunov's direct method](/lyapunov-direct-method/).

The tests check the check value and the scalar LQR gain, the identity $a + b u = -\sqrt{a^2 + \beta^2}$ and the quadratic for $\varphi$ on 2000 random inputs with up to 3 entries, the table above within $10^{-5}$, that $V$ decreases at every step, the bound $|k| \le |x_2|$ near the origin, the unbounded feedback of the pitfall below, and a closed loop for the double integrator with the LQR matrix $P = \begin{bmatrix} \sqrt 3 & 1 \\ 1 & \sqrt 3 \end{bmatrix}$ as $V = x^T P x$.

## Complexity

Count real operations and one square root at unit cost, as in the real RAM, with $n$ states and $m$ inputs.

- **Line L1.** A dot product of length $n$: $O(n)$.
- **Line L2.** A row vector times an $n \times m$ matrix: $O(n m)$.
- **Lines L3 to L6.** $O(m)$ operations and one square root.

So one evaluation costs $O(n m)$ operations plus one evaluation each of $f(x)$, $g(x)$ and $\nabla V(x)$, which the bound does not count. The extra space is $O(m)$ for $b$ and $u$. A closed-loop simulation costs the number of steps times this, times 4 for the four stages of RK4.

## Properties

- **Explicit.** No optimization, no iteration and no tuning parameter. Every design choice is in $V$.
- **Smooth away from the origin.** The formula is real-analytic in $(a, \beta)$ on the set where $\beta > 0$ or $a < 0$, so $k$ is as smooth as $f$, $g$ and $\nabla V$ there.
- **Continuous at the origin if and only if** $V$ has the small control property.
- **Depends on the scaling of V.** Replacing $V$ by $c V$ with $c > 0$ changes $(a, \beta)$ to $(c a, c^2 \beta)$ and changes the feedback. The decrease $\dot V < 0$ holds for every scaling.
- **Related to optimal control.** In the scalar example the formula gives the LQR gain, and Sontag (1998, Exercise 5.9.11) relates the formula with an LQ problem in general. Freeman and Kokotović (1996) show that the pointwise min-norm laws, close relatives of the formula, are optimal for meaningful costs.

## Variants and improvements

- **A general gain function.** Sontag's paper allows $\varphi = (a + \sqrt{a^2 + \beta\, q(\beta)})/\beta$ with a real-analytic $q$ that is positive for $\beta > 0$ and $q(0) = 0$. The page uses $q(\beta) = \beta$. Other choices trade input size against the decay rate of $V$.
- **Bounded inputs.** Lin and Sontag (1991) give a version for $|u| \le 1$, with an extra scaling that keeps the input in the unit ball. It needs $V$ to have a decrease with bounded input, which is a stronger assumption.
- **Pointwise min-norm control.** Freeman and Kokotović (1996) choose at each state the input of least norm that makes $\dot V \le -\sigma(x)$ for a given positive function $\sigma$. This is a small quadratic program with one constraint, with the same closed form as the projection in the [CBF safety filter](/cbf-safety-filter/).
- **Where the control Lyapunov function comes from.** For a system in strict feedback form, [backstepping](/backstepping/) builds $V$ and a feedback together. For a polynomial system, [sum-of-squares programming](/sum-of-squares-programming/) can search for $V$. For a linear system, $V = x^T P x$ with $P$ from the [Riccati equation](/continuous-algebraic-riccati-equation/).

## When to use it

Use it when you have a control Lyapunov function and want a feedback with no further design, for example after backstepping or when $V$ comes from a physical energy. It is also a safe fallback inside a supervisor: whatever the state, it lowers $V$. It is not the best choice when the input is limited, because the gain grows where $a > 0$ and $\beta$ is small; use the bounded version or a quadratic program with input limits there. When the performance matters more than the simplicity, an optimal control design or [model predictive control](/model-predictive-control/) with $V$ as a terminal cost uses the same $V$ better.

## Pitfalls

- **Cancellation at line L5.** The direct form $(a + s)/\beta$ loses all digits when $a < 0$ and $\beta \ll |a|$. In IEEE double precision, $a = -1$ and $\beta = 10^{-8}$ give $s = 1$ exactly, and the direct form returns $\varphi = 0$; the true value is $\beta/(1 + \sqrt{1 + \beta^2}) \approx 5 \cdot 10^{-9}$. Use the second form of line L5 when $a \le 0$.
- **No small control property.** The formula is then discontinuous at the origin. For $\dot x = x + x^2 u$ with $V = x^2 / 2$: $a = x^2$ and $b = x^3$, and lines L5 and L6 give $u = -(1 + \sqrt{1 + x^8})/x$, so $|u| \ge 2 / |x|$, which is unbounded near $0$. The closed loop $\dot x = -x \sqrt{1 + x^8}$ is fine on its own, but the input is not. In this system no continuous feedback can do better: if $k$ is continuous, $x\, k(x) \to 0$, so $\dot x = x (1 + x k(x))$ has the sign of $x$ near $0$.
- **V that is not a control Lyapunov function.** Line L4 returns $0$ whenever $b = 0$, whatever $a$ is. For the double integrator $\dot x_1 = x_2$, $\dot x_2 = u$ with $V = x_1^2 + x_2^2$, $b = 2 x_2$ and $a = 2 x_1 x_2$, so on the line $x_2 = 0$ both vanish. Line L4 returns $u = 0$ there, and every point $(x_1, 0)$ is an equilibrium of the closed loop. Check the control Lyapunov function condition before you trust the formula.
- **Sampled implementation.** The proof assumes that line L6 is evaluated continuously. In the nonlinear example with the input held constant over intervals of $0.3$, $V$ increases on 7 of the 1000 simulation steps, and with a hold of $0.5$ the first input $-8.12$ drives $x_2$ to $-3.06$ and $V$ rises from $2.5$ to $4.95$. The state still went to the origin in these runs, but the decrease of $V$ is no longer guaranteed.

## Implementations

## History

Artstein (1983) proved that a control-affine system with a smooth control Lyapunov function has a feedback that is smooth away from the origin, by an argument with relaxed controls that does not give a formula. Sontag (1983) characterized asymptotic controllability by a Lyapunov-like function. In 1989 Sontag gave the explicit formula, called it "universal" because it depends only on $L_f V$ and $L_g V$, and proved that it is real-analytic away from the origin and continuous at it under the small control property. Lin and Sontag (1991) extended it to bounded inputs. Freeman and Kokotović (1996) showed that pointwise min-norm laws built from a control Lyapunov function are optimal for meaningful costs, which made this family of formulas part of the inverse optimal design method.

## References
