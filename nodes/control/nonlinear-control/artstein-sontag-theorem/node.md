---
tag: HW83BH
kind: theorem
slug: artstein-sontag-theorem
name: Artstein's theorem
aliases:
- Artstein-Sontag theorem
area: control/nonlinear-control
level: advanced
summary: A control-affine system has a smooth control Lyapunov function with the small control property exactly when a feedback smooth away from 0 and continuous at 0 makes 0 globally asymptotically stable.
history:
  year: 1983
  people: [Zvi Artstein, Eduardo D. Sontag]
  note: "Artstein (1983) proved the equivalence between a smooth control Lyapunov function and stabilization, with relaxed controls for general systems; Sontag (1989) gave an explicit feedback for control-affine systems and the small control property for continuity at the origin."
prereqs: [control-lyapunov-function, lyapunov-direct-method, converse-lyapunov-theorem]
see_also: [sontag-universal-formula, brockett-condition, control-affine-system, backstepping, lyapunov-function, asymptotic-stability, input-to-state-stability, feedback-linearization]
sources:
  - paper: doi:10.1016/0362-546X(83)90049-4
    title: "Zvi Artstein, Stabilization with relaxed controls, Nonlinear Analysis: Theory, Methods and Applications 7(11), 1163-1173, 1983"
    locator: the main theorem (a smooth control Lyapunov function exists if and only if the system is stabilizable by relaxed controls; for control-affine systems, by a feedback regular away from the origin)
  - paper: doi:10.1016/0167-6911(89)90028-5
    title: "Eduardo D. Sontag, A 'universal' construction of Artstein's theorem on nonlinear stabilization, Systems and Control Letters 13(2), 117-123, 1989"
    locator: the explicit feedback, its analyticity away from the origin, and continuity at the origin under the small control property
  - book: isbn:9780387984896
    title: Eduardo D. Sontag, Mathematical Control Theory, second edition, Springer, 1998
    locator: Section 5.7 (control-Lyapunov functions) and Section 5.9 (Proposition 5.9.10 and Exercise 5.9.11, the universal formula)
  - book: isbn:9780471127321
    title: Miroslav Krstić, Ioannis Kanellakopoulos and Petar Kokotović, Nonlinear and Adaptive Control Design, Wiley, 1995
    locator: Section 2.1.2, control Lyapunov functions and Sontag's formula
---

Artstein's theorem says that, for a control-affine system $\dot x = f(x) + g(x) u$, two things are the same: a smooth [control Lyapunov function](/control-lyapunov-function/) exists, and a feedback that is smooth away from the origin makes the origin globally asymptotically stable. One direction is a [converse Lyapunov theorem](/converse-lyapunov-theorem/). The other turns a function into a feedback, which is the useful direction for design. Artstein (1983) proved it without a formula. Sontag (1989) gave an explicit feedback, [Sontag's universal formula](/sontag-universal-formula/), and showed that it is continuous at the origin exactly when the control Lyapunov function has the small control property. The form on this page, with continuity at the origin, needs that property, and it is often called the Artstein-Sontag theorem.

## Statement

**Setting.** The system is $\dot x = f(x) + g(x) u$, $x \in \mathbb{R}^n$, $u \in \mathbb{R}^m$, with $f$ and $g$ smooth ($C^\infty$) and $f(0) = 0$. A control Lyapunov function (CLF) is a smooth $V : \mathbb{R}^n \to \mathbb{R}$ that is positive definite, proper, and has, for every $x \neq 0$, some $u$ with $L_f V(x) + L_g V(x)\, u < 0$. It has the small control property if for every $\varepsilon > 0$ there is $\delta > 0$ such that each $x$ with $0 < |x| < \delta$ has such a $u$ with $|u| < \varepsilon$.

**Theorem.**

1. If $V$ is a smooth CLF, there is a feedback $k : \mathbb{R}^n \setminus \{0\} \to \mathbb{R}^m$, smooth (in fact real-analytic in $L_f V$ and $L_g V$), with $L_f V(x) + L_g V(x)\, k(x) < 0$ for every $x \neq 0$.
2. If $V$ also has the small control property, then $k$, extended by $k(0) = 0$, is continuous on $\mathbb{R}^n$, and the origin of $\dot x = f(x) + g(x) k(x)$ is globally asymptotically stable.
3. Conversely, if a feedback $k : \mathbb{R}^n \to \mathbb{R}^m$ that is continuous, smooth on $\mathbb{R}^n \setminus \{0\}$ and zero at $0$ makes the origin of the closed loop globally asymptotically stable, then the system has a smooth CLF with the small control property.

So a smooth CLF with the small control property exists if and only if a feedback smooth away from the origin and continuous at it gives global asymptotic stability.

## In plain words

A control Lyapunov function is a measure of distance to the target such that, at every point away from the target, some push makes the distance shrink. The theorem says that such a measure is all you need. From it you can build one fixed rule that tells the system which push to use at each point, and that rule changes smoothly from point to point. With that rule the system goes to the target from anywhere and stays near it once it is close. The reverse is also true: if such a rule exists, so does such a measure. One condition is needed at the target itself. Near the target, small pushes must be enough. Without that, the rule can demand huge pushes close to the target, and it jumps there.

## Proof

The proof of parts 1 and 2 uses the explicit feedback of Sontag (1989). The full details are in the proof of [Sontag's universal formula](/sontag-universal-formula/); the steps are as follows.

**Part 1.** Write $a(x) = L_f V(x)$, $b(x) = L_g V(x)$ and $\beta(x) = |b(x)|^2$. The CLF condition says that $\beta(x) = 0$ and $x \neq 0$ imply $a(x) < 0$, because otherwise no input could make $a + b u$ negative. Define

$$\varphi(a, \beta) = \frac{a + \sqrt{a^2 + \beta^2}}{\beta} \ (\beta > 0), \qquad \varphi(a, 0) = 0, \qquad k(x) = -\varphi(a(x), \beta(x))\, b(x)^T.$$

Then $a + b k = -\sqrt{a^2 + \beta^2}$ when $\beta > 0$, and $a + b k = a$ when $\beta = 0$. Both are negative for $x \neq 0$. For smoothness, let $S = \{(a, \beta) : \beta > 0 \text{ or } a < 0\}$, an open set that contains $(a(x), \beta(x))$ for every $x \neq 0$. On $S$, $p = \varphi(a, \beta)$ solves $\beta p^2 - 2 a p - \beta = 0$, and the derivative of the left side in $p$ is $2 \sqrt{a^2 + \beta^2}$ at $\beta > 0$ and $-2a$ at $\beta = 0$, both positive. By the real-analytic implicit function theorem, $\varphi$ is real-analytic on $S$; near $\beta = 0$ this can also be seen from the equal form $\varphi = \beta / (\sqrt{a^2 + \beta^2} - a)$. So $k$ is smooth on $\mathbb{R}^n \setminus \{0\}$.

**Part 2.** Since $V$ has a minimum at 0, $\nabla V(0) = 0$, so $b(0) = 0$. Let $\varepsilon > 0$, take $\delta$ from the small control property, and let $x \neq 0$ be close enough to 0 that also $|b(x)| < \varepsilon$. If $a(x) \le 0$, then $\varphi \le 1$ by the second form, so $|k(x)| \le |b(x)| < \varepsilon$. If $a(x) > 0$, the small control property gives a $u$ with $|u| < \varepsilon$ and $a + b u < 0$, so $a < |b| \varepsilon$ by the Cauchy-Schwarz inequality. With $\sqrt{a^2 + \beta^2} \le a + \beta$ this gives $|k(x)| \le 2a / |b| + |b| < 3 \varepsilon$. So $k(x) \to 0$ as $x \to 0$, and $k$ is continuous.

The closed loop $F = f + g k$ is then continuous on $\mathbb{R}^n$ and smooth on $\mathbb{R}^n \setminus \{0\}$, so solutions are unique while they stay away from 0 (see the [Picard-Lindelöf theorem](/picard-lindelof-theorem/)). Along any solution, $\frac{d}{dt} V(x(t)) < 0$ while $x(t) \neq 0$, and $\nabla V(0) = 0$, so a solution that reaches 0 stays there. $V$ is proper, so each solution stays in the compact set $\{V \le V(x(0))\}$ and exists for all $t \ge 0$. [Lyapunov's direct method](/lyapunov-direct-method/), whose proof uses only these facts, gives global asymptotic stability.

**Part 3.** Let $F = f + g k$. It is continuous and $F(0) = 0$. A solution that starts at 0 stays in every ball around 0, by the stability part of the hypothesis, so it stays at 0. By the converse Lyapunov theorem of Kurzweil (1956) for continuous vector fields with a globally asymptotically stable equilibrium, there is a smooth $V$, positive definite and proper, with $\nabla V(x)^T F(x) < 0$ for $x \neq 0$. This says $L_f V(x) + L_g V(x)\, k(x) < 0$, so $u = k(x)$ shows that $V$ is a CLF. For the small control property, let $\varepsilon > 0$. Since $k$ is continuous and $k(0) = 0$, there is $\delta > 0$ with $|k(x)| < \varepsilon$ for $|x| < \delta$, and then $u = k(x)$ is the required small input. $\blacksquare$

## Consequences

- **A formula, not only existence.** Part 1 is constructive: Sontag's formula depends only on $L_f V$ and $L_g V$ at the current state. Every design method that produces a CLF, such as [backstepping](/backstepping/) or a quadratic Lyapunov function of a linearization, gives a feedback this way.
- **An obstruction.** If a system fails [Brockett's condition](/brockett-condition/), it has no continuous feedback that gives asymptotic stability (Brockett 1983 for $C^1$ feedback, with a later extension to continuous feedback). By part 2, it then has no smooth CLF with the small control property. The nonholonomic integrator $\dot x_1 = u_1$, $\dot x_2 = u_2$, $\dot x_3 = x_1 u_2 - x_2 u_1$ is the standard example.
- **Linear systems.** For $\dot x = A x + B u$, a quadratic CLF $x^T P x$ exists if and only if $(A, B)$ is stabilizable: if $A + BK$ is Hurwitz, the solution of the Lyapunov equation of $A + BK$ is one, and conversely Sontag's formula with a quadratic CLF stabilizes.
- **Design by CLF.** Because a CLF is enough, many nonlinear design methods aim only at finding a CLF and then use the formula or a pointwise optimization of the input, such as the CLF quadratic program.
- **Rule of thumb, not part of the theorem.** The feedback of part 1 can use large inputs where $L_g V$ is small. The theorem says nothing about input size or robustness; inverse optimality results (Freeman and Kokotović 1996) address this for related formulas.

## Tightness

- **The small control property is needed for continuity at 0.** For $\dot x = x + x^2 u$, $V = x^2 / 2$ is a smooth CLF, because $L_g V = x^3 \neq 0$ for $x \neq 0$. The feedback $k(x) = -2/x$ gives $\dot x = -x$, smooth away from 0. But $\dot V < 0$ needs $|u| > 1/|x|$, so the small control property fails, and no feedback continuous at 0 gives asymptotic stability: it would need $x(1 + x k(x)) < 0$ near 0, so $|k(x)| > 1/|x|$. So part 1 holds and part 2 fails.
- **Smoothness of V is needed.** The nonholonomic integrator is asymptotically controllable, and by Sontag (1983) it has a continuous CLF in a sense with directional derivatives. It has no continuous stabilizing feedback. So a nonsmooth CLF does not give a continuous feedback. Nonsmooth CLFs give discontinuous feedbacks, with solutions in a special sense (Clarke, Ledyaev, Sontag and Subbotin 1997).
- **The affine structure is needed.** For $\dot x = F(x, u)$ that is not affine in $u$, the inputs that make $\dot V$ negative at a state need not form a convex set, and a continuous selection may not exist. Artstein's theorem then holds with relaxed controls, which is how Artstein (1983) states it.
- **The converse needs continuity of the feedback at 0 for the small control property.** A feedback that gives asymptotic stability but is unbounded near 0, as in the first example, gives a CLF without the small control property.

## History

Artstein (1983) proved that a nonlinear system has a smooth control Lyapunov function if and only if it can be stabilized with relaxed controls, and that for control-affine systems the relaxed controls are not needed. The proof used a partition of unity and gave no formula. In the same year Sontag characterized asymptotic controllability by a Lyapunov-like function that need not be smooth. Sontag (1989) gave the explicit, "universal" feedback for control-affine systems, proved that it is real-analytic away from the origin, and introduced the small control property for continuity at the origin. The converse part rests on the smooth converse Lyapunov theorem of Kurzweil (1956). Brockett's condition, from the same year as Artstein's paper, showed which systems cannot have such a feedback.

## References
