---
tag: BC8K3Y
kind: technique
slug: mixed-sensitivity-design
name: Mixed sensitivity design
aliases:
- S/KS/T design
- mixed sensitivity H-infinity design
area: control/robust-and-adaptive-control
level: advanced
summary: Shapes the sensitivity, control sensitivity and complementary sensitivity by weights, and solves the result as an H-infinity problem.
prereqs: [h-infinity-control-problem, sensitivity-function, complementary-sensitivity-function]
see_also: [dgkf-h-infinity-synthesis, lmi-h-infinity-synthesis, h-infinity-loop-shaping, loop-shaping, bode-sensitivity-integral, model-uncertainty, youla-parametrization, dk-iteration]
sources:
  - paper: doi:10.1016/0005-1098(93)90122-A
    title: Huibert Kwakernaak, Robust control and H-infinity optimization, tutorial paper, Automatica 29(2), 255-273, 1993
    locator: the mixed sensitivity problem, the choice of weights, and its solution as a standard H-infinity problem
  - paper: doi:10.1109/TAC.1981.1102603
    title: George Zames, Feedback and optimal sensitivity, model reference transformations, multiplicative seminorms, and approximate inverses, IEEE Transactions on Automatic Control 26(2), 301-320, 1981
    locator: the weighted sensitivity problem that mixed sensitivity extends
  - paper: doi:10.1109/9.29425
    title: John C. Doyle, Keith Glover, Pramod P. Khargonekar and Bruce A. Francis, State-space solutions to standard H2 and H-infinity control problems, IEEE Transactions on Automatic Control 34(8), 831-847, 1989
    locator: the state-space solution used for the stacked problem
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, second edition, Wiley, 2005
    locator: Chapter 2, the section on shaping closed-loop transfer functions, with the weight W_P and the stacked S/KS problem, and Chapter 9, H-infinity mixed sensitivity design
---

Mixed sensitivity design turns a list of frequency domain requirements on a feedback loop into one [H-infinity control problem](/h-infinity-control-problem/). The designer chooses weights $W_1$, $W_2$ and $W_3$ and stacks the weighted [sensitivity function](/sensitivity-function/) $W_1 S$, the weighted control sensitivity $W_2 K S$ and the weighted [complementary sensitivity](/complementary-sensitivity-function/) $W_3 T$ into one column. A synthesis method, such as [two-Riccati synthesis](/dgkf-h-infinity-synthesis/) or [LMI synthesis](/lmi-h-infinity-synthesis/), then finds the controller that minimizes the H-infinity norm of the stack. If the optimum $\gamma_{\rm opt}$ is below 1, every weighted map is below 1 at every frequency, so the requirements hold. If it is above 1, the requirements conflict, and the designer relaxes the weights. Zames (1981) posed the weighted sensitivity problem, and Kwakernaak (1993) gives the method and its practice in a tutorial form.

## In plain words

You write down what you want from the loop as curves. The error should be small at low frequency, so $|S|$ must stay under one curve. The control signal should not be too large, so $|K S|$ must stay under a second curve. The loop should ignore noise and model errors at high frequency, so $|T|$ must stay under a third curve. Each curve is the inverse of a weight. You put the three weighted maps in one stack and ask an H-infinity solver for the controller that makes the worst weighted gain as small as possible. A result below 1 means all the curves are met. A result above 1 tells you that the wishes fight each other, for example because of a zero or pole in the right half plane.

## When it applies

- The plant is linear and time invariant, and you have a model of it, possibly with several inputs and outputs.
- The requirements are bounds on closed loop gains as functions of frequency: tracking and disturbance rejection on $S$, actuator use and input noise on $K S$, and noise rejection and robustness to multiplicative [model uncertainty](/model-uncertainty/) on $T$.
- Each weight is a proper rational function with all poles in the open left half plane. The generalized plant must satisfy the assumptions of the chosen solver.
- An order of the controller equal to the plant order plus the weight orders is acceptable, or you plan to reduce it afterwards.

## The template

The loop uses negative feedback: the reference $r$ enters, the error is $e = r - y$, the controller is $u = K e$, and $y = P u$. Then $e = S r$, $u = K S r$ and $y = T r$, with

$$S = (I + P K)^{-1}, \qquad T = P K (I + P K)^{-1}, \qquad S + T = I.$$

1. **Choose the weights.** A common first choice for a scalar loop (rule of thumb; Skogestad and Postlethwaite 2005, chapter 2) is
$$W_1(s) = \frac{s/M + \omega_b}{s + \omega_b A}, \qquad W_2 = \text{a constant or a high pass filter}, \qquad W_3(s) = \frac{s + \omega_t/M_t}{A_t s + \omega_t}.$$
The bound $|W_1 S| < 1$ asks for $|S| < A$ at low frequency, a bandwidth of about $\omega_b$, and a peak of $|S|$ below $M$. Typical values are $M = 2$ and $A$ between $10^{-4}$ and $10^{-2}$. In the same way, $|W_3 T| < 1$ asks for $|T| < M_t$ at low frequency and $|T| < A_t$ well above $\omega_t$. Use $A > 0$, not a pure integrator, for the reason under Pitfalls.
2. **Build the generalized plant.** Take $w = r$, the measurement $y_K = e$, and the stacked error $z = (W_1 e, W_2 u, W_3 y)$. Then the closed loop is
$$T_{zw} = \begin{bmatrix} W_1 S \\ W_2 K S \\ W_3 T \end{bmatrix}.$$
Drop the rows you do not need: S/KS design uses the first two, and S/T design the first and the last. The states of the generalized plant are those of $P$, $W_1$, $W_2$ and $W_3$.
3. **Solve the H-infinity problem.** Compute $\gamma_{\rm opt}$ and a controller at a level a little above it. The controller has the order of the generalized plant.
4. **Read the result.** If $\gamma < 1$, then $|S(j\omega)| < 1/|W_1(j\omega)|$, $|K S(j\omega)| < 1/|W_2(j\omega)|$ and $|T(j\omega)| < 1/|W_3(j\omega)|$ at every frequency. If $\gamma > 1$, at least one bound fails somewhere. Plot each map against its bound to see which one.
5. **Iterate.** Relax the weight that limits, for example lower $\omega_b$, or push it harder if $\gamma$ is far below 1. Then check the design in time domain simulations and against the uncertainty that the weights did not model.

## Classic examples

**The price of an unstable pole.** Let $P(s) = 1/(s - 1)$, with a pole at $s = 1$, and use the constant weights $W_1 = \rho$ and $W_2 = 1$ (S/KS design). The constant controller $K = 2$ gives $S = (s - 1)/(s + 1)$ and $K S = 2(s - 1)/(s + 1)$. Their gains are 1 and 2 at every frequency, so $|\rho S|^2 + |K S|^2 = \rho^2 + 4$ at every frequency and the stack has norm $\sqrt{\rho^2 + 4}$. The LMI method of the [LMI page](/lmi-h-infinity-synthesis/) gives $\gamma_{\rm opt} = 2.00000$, $2.06155$, $2.23607$ and $2.82843$ for $\rho = 0$, $0.5$, $1$ and $2$, which equals $\sqrt{\rho^2 + 4}$ to 8 digits (measurement). So $K = 2$ is optimal for each $\rho$, and a constant weight on $S$ buys nothing. Two facts explain this. Every stabilizing controller has $\|K S\|_\infty \ge 2$: $K S = (s + 1) T \cdot (s - 1)/(s + 1)$, the function $(s + 1) T$ is analytic and bounded in the right half plane, and $T(1) = 1$, so the maximum modulus principle gives $\|K S\|_\infty \ge 2$ (theorem). And $S(\infty) = 1$ for any proper controller, because $P$ is strictly proper. A useful $W_1$ must therefore be large at low frequency and small at high frequency.

**A weight that shapes S.** Same plant, now with $W_1(s) = (s/2 + \omega_b)/(s + 0.01\,\omega_b)$ (so $M = 2$ and $A = 0.01$) and $W_2 = 0.1$, so the bound on $|K S|$ is 10. The generalized plant has two states, and the LMI method gives these values (measurement, frequency grid of 241 points from $10^{-3}$ to $10^3$ rad/s, controller at $1.01\,\gamma_{\rm opt}$):

| $\omega_b$ | $\gamma_{\rm opt}$ | $\max_\omega \lvert S\rvert$ | $\lvert S(0)\rvert$ | $\max_\omega \lvert K S\rvert$ | first $\omega$ with $\lvert S\rvert \ge 0.707$ |
|---|---|---|---|---|---|
| 0.5 | 0.577 | 1.003 | 0.0047 | 2.92 | 0.94 |
| 1 | 0.618 | 1.003 | 0.0045 | 3.66 | 1.68 |
| 2 | 0.699 | 1.002 | 0.0042 | 4.89 | 2.99 |
| 4 | 0.841 | 1.001 | 0.0035 | 6.74 | 5.01 |
| 8 | 1.071 | 1.000 | 0.0025 | 9.38 | 7.50 |

As $\omega_b$ grows, the loop gets faster and $|K S|$ grows. Up to $\omega_b = 4$ the optimum is below 1 and all the bounds hold. At $\omega_b = 8$ it is above 1: the controller cannot give that bandwidth with $|K S| \le 10$ and the low frequency bound together. The value $|S(0)|$ stays below $\gamma A$, as the weight requires.

**A limit from a right half plane zero.** The [H-infinity problem page](/h-infinity-control-problem/) solves the one-block problem $\min \|W S\|_\infty$ for $P = (1 - s)/(1 + s)$ in closed form. The zero at $s = 1$ gives $\|W S\|_\infty \ge |W(1)|$ for every stabilizing controller, so a weight that asks for a bandwidth well above the zero gives $\gamma_{\rm opt} > 1$.

## Variations

- **S/KS design** for disturbance rejection at the plant output with a bound on the control effort. It is the most used form.
- **S/T design** when the main uncertainty is multiplicative at the output: $|W_3 T| < 1$ with $|W_3|$ above the relative model error gives robust stability by the small gain theorem.
- **Signal based design.** The generalized plant takes disturbances and noise at their real entry points, each shaped by its own weight. This is more general than the three-block stack, and it is the form in Skogestad and Postlethwaite (2005, chapter 9).
- **Four-block or two degree of freedom forms** add an input disturbance or a reference model to the stack.
- **Mixed sensitivity with mu.** If the uncertainty is structured, the stack is one block of a larger problem, and [D-K iteration](/dk-iteration/) handles the structure.
- **Discrete time.** The same template with weights in the $z$ domain and a discrete-time H-infinity solver.

## Pitfalls

- **S + T = I.** Since $1 = |S + T| \le |S| + |T|$ for a scalar loop, the bounds $|W_1 S| < 1$ and $|W_3 T| < 1$ can hold together only where $1/|W_1| + 1/|W_3| > 1$ (theorem). Weights that are both large at the same frequency make the problem infeasible.
- **Weights with poles on the imaginary axis.** A weight state is driven by the loop signals but never reaches the measurement $e$. So $(C_2, A)$ is not detectable if a weight has a pole with real part 0 or more, and no controller can stabilize the generalized plant. Use $A > 0$ in $W_1$ instead of a pure integrator. The same holds for a $W_3$ that is not proper: realize it with a far pole, or use the product $W_3 P$, if it is proper, as a weight on $u$, since $W_3 T = (W_3 P) K S$.
- **Rank conditions.** The two-Riccati method needs $D_{12}$ of full column rank, so S/T design without a weight on $u$ needs a small constant $W_2$, or the LMI method.
- **Pole cancellation.** In practice the S/KS design often cancels the stable poles of the plant with zeros of the controller. Then a disturbance at the plant input still shows the slow plant poles (rule of thumb). Use a signal based design with an input disturbance if those poles are slow or lightly damped.
- **The stack is conservative.** The norm of the stack is the largest singular value of a column, so $\max_i \|W_i X_i\|_\infty \le \|T_{zw}\|_\infty \le \sqrt 3 \max_i \|W_i X_i\|_\infty$ for three blocks (theorem). A $\gamma$ slightly above 1 can still meet each bound alone.
- **High order.** The controller order is the plant order plus all the weight orders. Keep the weights low order, and reduce the controller afterwards with a check of the reduced loop.

## Exercises

1. For $P(s) = 1/(s - a)$ with $a > 0$, show that every stabilizing controller has $\|K S\|_\infty \ge 2a$, and that $K = 2a$ reaches it. *Hint:* $T(a) = 1$, and $K S = T/P$.
2. Show that the bounds $|S| < 0.1$ and $|T| < 0.5$ cannot hold at the same frequency.
3. Take $W_1(s) = (s/2 + 1)/(s + 0.01)$. Find $|W_1(0)|$ and $|W_1(j\infty)|$, and say what the bound $|W_1 S| < 1$ asks of $|S|$ at those two ends.
4. Write the matrices $A$, $B_1$, $B_2$, $C_1$, $D_{11}$, $D_{12}$, $C_2$ and $D_{21}$ of the generalized plant of the second example for $\omega_b = 1$. Check that the weight state is not observable from $e$, and that $(C_2, A)$ is not detectable when the weight has $A = 0$.

## References
